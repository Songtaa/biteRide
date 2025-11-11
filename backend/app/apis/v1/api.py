from fastapi import APIRouter
from app.apis.v1.endpoints import users, restaurants, orders, delivery, auth, health

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(restaurants.router, prefix="/restaurants", tags=["restaurants"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(delivery.router, prefix="/delivery", tags=["delivery"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
