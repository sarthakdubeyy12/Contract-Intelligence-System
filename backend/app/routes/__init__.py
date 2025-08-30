from fastapi import APIRouter
from app.controllers import scoring_controller

api_router = APIRouter()
api_router.include_router(scoring_controller.router)