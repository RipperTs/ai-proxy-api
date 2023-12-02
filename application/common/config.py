'''
全局配置公共类
'''

from dotenv import load_dotenv
import os

load_dotenv()

__all__ = [
    'server_name',
    'server_port',
    "use_azure_model",
    "azure_chat_model",
    "secret_key",
    "access_token_expire_minutes",
    "server_workers",
    "reload",
    "db_url",
]

# 重置系统变量，在不需要设置的时候不设置环境变量，以免引起全局代理报错
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""

os.environ['TOKENIZERS_PARALLELISM'] = "false"

# 系统服务及端口配置
server_name = os.environ.get("SERVER_NAME", '0.0.0.0')
server_port = int(os.environ.get("SERVER_PORT", 4000))
server_workers = int(os.environ.get("SERVER_WORKERS", 1))
reload = bool(os.environ.get("RELOAD", 'false').lower() == 'true')

# 数据库配置(tortoise-orm+aiomysql)
db_url = os.environ.get("DATABASE_URL", "mysql://username:password@localhost/db_name?charset=utf8mb4")

use_azure_model = bool(os.environ.get("USE_AZURE_MODEL", 'false').lower() == 'true')
azure_chat_model = os.environ.get("AZURE_CHAT_MODEL")

secret_key = os.environ.get('SECRET_KEY')
access_token_expire_minutes = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
