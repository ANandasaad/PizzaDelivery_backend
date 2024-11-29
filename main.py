from fastapi import FastAPI
from Models import models
from Database.db import engine
from Routers.user import user_router
from Routers.menu import menu_router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(menu_router)