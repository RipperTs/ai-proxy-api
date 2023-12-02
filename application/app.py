from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import UJSONResponse

from application.common.logging import configure_logging
from application.handler.exception_handler import register_exception, register_middleware
from application.lifetime import register_startup_event, register_shutdown_event
from application.router import api_router


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()

    app = FastAPI(
        title="AI Proxy API",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Add global exception interceptor
    register_exception(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Add global middleware
    register_middleware(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/ai-proxy/api/v1")

    return app
