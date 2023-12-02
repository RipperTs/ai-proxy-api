from datetime import datetime, timedelta

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from application.common import config
from application.model.entity.users_entity import UsersEntity
from passlib.context import CryptContext
from jose import jwt

from application.model.po.register_user_po import RegisterUserPo

SECRET_KEY = config.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = config.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/ai-proxy/api/v1/user/login-user")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


async def create_user(data: RegisterUserPo):
    if data.password != data.re_password:
        raise AssertionError("两次密码不一致")

    query = UsersEntity.filter(email=data.email)
    user_exists = await query.exists()
    if user_exists is True:
        raise AssertionError("邮箱已存在")
    hashed_password = get_password_hash(data.password)
    user = UsersEntity(username=data.username, email=data.email, password=hashed_password, status=2)
    await user.save()
    return user.id


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def login_for_access_token(email: str, password: str):
    query = UsersEntity.filter(email=email)
    user_exists = await query.exists()
    if user_exists is False:
        raise AssertionError("用户名或密码错误")

    users = await query.first()
    if not verify_password(password, users.password):
        raise AssertionError("用户名或密码错误")

    if users.status != 1:
        raise AssertionError("用户已被禁用")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": users.username, "email": users.email, "user_id": users.id}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer", "username": users.username,
            "email": users.email, "user_id": users.id}


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        return None


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload.get("username")
    email = payload.get("email")
    user_id = payload.get("user_id")
    if not username or not email:
        raise HTTPException(status_code=401, detail="Invalid token")
    # todo: 验证用户是否存在或已被禁用
    user = {"username": username, "email": email, "user_id": user_id}
    return user


async def do_update_password(user_id: int, password: str, re_password: str):
    if password != re_password:
        raise AssertionError("两次密码不一致")

    query = UsersEntity.filter(id=user_id)
    user_exists = await query.exists()
    if user_exists is False:
        raise AssertionError("用户不存在")

    user = await query.first()

    hashed_password = get_password_hash(password)
    user.password = hashed_password
    await user.save()
    return user.id
