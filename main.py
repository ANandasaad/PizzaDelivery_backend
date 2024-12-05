from fastapi import FastAPI
from Models import models
from Database.db import engine
from Routers.user import user_router
from Routers.menu import menu_router
from Routers.pizza import pizza_router
from Routers.customization import customization_router
from Routers.order import order_router
from Routers.payment import payment_router
from Routers.deliveryPersonal import deliveryPersonal_router
from Routers.auth import auth_router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(menu_router)
app.include_router(pizza_router)
app.include_router(customization_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(deliveryPersonal_router)
app.include_router(auth_router)