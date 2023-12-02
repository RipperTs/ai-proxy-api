from tortoise import Tortoise

from application.common import config
from application.model.entity import load_all_models


async def init_database():
    """
    Initialize database connection.
    """
    await Tortoise.init(db_url=config.db_url,
                        modules={"models": load_all_models()},
                        timezone="Asia/Shanghai")
    await Tortoise.generate_schemas()


async def close_database():
    """
    Close database connection.
    """
    await Tortoise.close_connections()
