'''
全局配置公共类
'''

from dotenv import load_dotenv
import os

from handler.log_handler import register_log_handler

load_dotenv()
register_log_handler()

__all__ = [
    'server_name',
    'server_port',
    'db_host',
    'db_port',
    'db_user',
    'db_password',
    'db_database',
    "use_azure_model",
    "azure_chat_model",
    "secret_key",
    "access_token_expire_minutes"
]

# 重置系统变量，在不需要设置的时候不设置环境变量，以免引起全局代理报错
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""

os.environ['TOKENIZERS_PARALLELISM'] = "false"

# 系统服务及端口配置
server_name = os.environ.get("SERVER_NAME", '0.0.0.0')
server_port = int(os.environ.get("SERVER_PORT", 3000))

# 数据库配置
db_host = os.environ.get('DB_HOST', 'localhost')
db_port = int(os.environ.get('DB_PORT', 3306))
db_user = os.environ.get('DB_USER', 'root')
db_password = os.environ.get('DB_PASSWORD', 'root')
db_database = os.environ.get('DB_DATABASE', '123456')

use_azure_model = bool(os.environ.get("USE_AZURE_MODEL", 'false').lower() == 'true')
azure_chat_model = os.environ.get("AZURE_CHAT_MODEL")

secret_key = os.environ.get('SECRET_KEY')
access_token_expire_minutes = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
