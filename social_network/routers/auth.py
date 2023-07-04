from fastapi import APIRouter, Depends, status, HTTPException, Response
from social_network import schemas
from sqlalchemy.orm import Session

from social_network.db.db import get_db
from social_network.schemas import UserResponse, Token, UserLoginData
from social_network.utils.crud import UserCrud
from social_network.utils.auth import create_access_token, hash, verify

router = APIRouter(
    prefix='/api',
    tags=['Users']
)

@router.post('/register', response_model=UserResponse)
def register(userdata: schemas.UserRegistration, db: Session = Depends(get_db)):
    crud = UserCrud(db)
    userdata.password = hash(userdata.password)
    if crud.get(userdata.email, 'email'):
        raise HTTPException(status_code=400)

    result = crud.post(userdata)
    if result:
        return result
    else:
        return Response(status_code=500)
    

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
