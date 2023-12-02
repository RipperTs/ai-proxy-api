from pydantic import BaseModel


class UpdatePasswordPo(BaseModel):
    password: str
    re_password: str
