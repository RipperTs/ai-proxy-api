from pydantic import BaseModel


class RegisterUserPo(BaseModel):
    username: str
    email: str
    password: str
    re_password: str
