from fastapi import APIRouter, Depends, status, HTTPException, Response
from social_network import schemas
from sqlalchemy.orm import Session
import asyncio

from social_network.db.db import get_db
from social_network.schemas import UserResponse, Token, UserLoginData
from social_network.utils.crud import UserCrud
from social_network.utils.auth import create_access_token, hash, verify
from social_network.utils.enrichment_api import get_enrichment_data, save_enrichment_data
from social_network.utils.hunter_api import get_hunter_data, validate_email
from social_network.config import get_settings

router = APIRouter(
    prefix='/api',
    tags=['Users']
)

@router.post('/register', response_model=UserResponse)
async def register(userdata: schemas.UserRegistration, db: Session = Depends(get_db), settings = Depends(get_settings)):
    crud = UserCrud(db)
    userdata.password = hash(userdata.password)
    if crud.get(userdata.email, 'email'):
        raise HTTPException(status_code=400, detail='User with this email already exists')
    enrichment_task = asyncio.create_task(get_enrichment_data(userdata.email))
    hunter_task = asyncio.create_task(get_hunter_data(userdata.email))

    result = crud.post(userdata)
    if result:
        data = await enrichment_task
        if settings.email_validation:
            email_data = await hunter_task
            try: # In case of invalid API key so that the app still works
                if not validate_email(email_data):
                    raise HTTPException(status_code=422, detail='Invalid email')
            except KeyError:
                pass
        else:
            if not hunter_task.done():
                hunter_task.cancel()
        try: # had to do this as I dont have a valid API key
            save_enrichment_data(data=data, db=db, id=result.id)
        except KeyError:
            pass
        return result
    else:
        for task in [enrichment_task, hunter_task]:
            if not enrichment_task.done():
                enrichment_task.cancel()
        return HTTPException(status_code=500, detail='Error while saving userdata')
    

@router.post('/login', response_model=Token)
def login(user_credentials: UserLoginData, db: Session = Depends(get_db)):
    user_crud = UserCrud(db)
    user = user_crud.get(user_credentials.email, 'email')

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
