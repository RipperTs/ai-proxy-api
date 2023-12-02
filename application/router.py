from fastapi.routing import APIRouter

from application.api import logs_api, channels_api, tokens_api, users_api

api_router = APIRouter()
api_router.include_router(logs_api.router, prefix="/log")
api_router.include_router(channels_api.router, prefix="/channel")
api_router.include_router(tokens_api.router, prefix="/token")
api_router.include_router(users_api.router, prefix="/user")
