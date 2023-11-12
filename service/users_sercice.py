from fastapi.security import OAuth2PasswordBearer

from common import config
from model.entity.users_entity import UsersEntity
from passlib.context import CryptContext

SECRET_KEY = config.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/ai-proxy/api/token")

# 配置密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(username, email, password):
    users = UsersEntity.get_by_email(email)
    if users is not None:
        raise Exception("用户已存在")
    hashed_password = get_password_hash(password)
    return UsersEntity.add_user(username, email, hashed_password, 2)


if __name__ == '__main__':
    print(create_user("admin", "wangyifani@foxmail.com", "123456"))
