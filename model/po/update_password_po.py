
from pydantic import BaseModel


class UpdatePasswordPo(BaseModel):
    email: str
    old_password: str
    new_password: str