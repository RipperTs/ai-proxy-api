'''
全局配置公共类
'''

from dotenv import load_dotenv
import os
import logging

load_dotenv()

__all__ = [
    'server_name',
    'server_port',
    'log_level',
    'default_openai_base_url',
    'db_host',
    'db_port',
    'db_user',
    'db_password',
    'db_database',
]

# 重置系统变量，在不需要设置的时候不设置环境变量，以免引起全局代理报错
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""

os.environ['TOKENIZERS_PARALLELISM'] = "false"

# 系统服务及端口配置
server_name = os.environ.get("SERVER_NAME", '0.0.0.0')
server_port = int(os.environ.get("SERVER_PORT", 3000))

log_level = os.environ.get("LOG_LEVEL", "WARNING")

logging.basicConfig(
    level=log_level,
    format="%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
)

# 默认openai配置
default_openai_base_url = os.environ.get('DEFAULT_OPENAI_BASE_URL', 'https://api.openai.com')

# 数据库配置
db_host = os.environ.get('DB_HOST', 'localhost')
db_port = int(os.environ.get('DB_PORT', 3306))
db_user = os.environ.get('DB_USER', 'root')
db_password = os.environ.get('DB_PASSWORD', 'root')
db_database = os.environ.get('DB_DATABASE', '123456')
