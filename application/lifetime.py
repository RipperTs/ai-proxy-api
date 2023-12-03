from typing import Awaitable, Callable

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from application.common import config
from application.model.database import init_database, close_database
from application.scheduler.balance_job import sync_balance

scheduler = AsyncIOScheduler()


def register_startup_event(
        app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("startup")
    async def _startup() -> None:  # noqa: WPS430
        await init_database()
        if config.sync_balance_interval > 0 and not scheduler.running:
            scheduler.add_job(sync_balance, 'interval', seconds=config.sync_balance_interval)
            scheduler.start()

    return _startup


def register_shutdown_event(
        app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: WPS430
        await close_database()
        if scheduler.running:
            scheduler.shutdown()

    return _shutdown
