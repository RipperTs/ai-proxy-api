import logging
from datetime import datetime, timedelta

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from common import config
from model.entity.users_entity import UsersEntity
from passlib.context import CryptContext
from jose import jwt, JWTError

SECRET_KEY = config.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = config.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/ai-proxy/api/login-user")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(username, email, password):
    users = UsersEntity.get_by_email(email)
    if users is not None:
        raise Exception("用户已存在")
    hashed_password = get_password_hash(password)
    return UsersEntity.add_user(username, email, hashed_password, 2)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def login_for_access_token(email, password):
    users = UsersEntity.get_by_email(email)
    if users is None:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    if not verify_password(password, users['password']):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": users['username'], "email": users['email']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    username = payload.get("username")
    email = payload.get("email")
    if not username or not email:
        raise HTTPException(status_code=401, detail="Invalid token")
    # todo: 验证用户是否存在或已被禁用
    user = {"username": username, "email": email}
    return user


if __name__ == '__main__':
    print(get_current_user("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZW1haWwiOiJ3YW5neWlmYW5pQGZveG1haWwuY29tIiwiZXhwIjoxNjk5NzYzNTM4fQ.wAIVtC7AHqRYlOuCtLCfnR45ITYv9wjib8-G-s5-GUM"))
