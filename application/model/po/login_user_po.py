
from pydantic import BaseModel


class LoginUserPo(BaseModel):
    email: str
    password: str