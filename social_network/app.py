from fastapi import FastAPI

from social_network.routers import auth, posts, likes

app = FastAPI()

origins = ['*']

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(likes.router)
