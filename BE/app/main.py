from fastapi import Depends, FastAPI

from BE.app.controllers import authentication

app = FastAPI()


app.include_router(authentication.router)