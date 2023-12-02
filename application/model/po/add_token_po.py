from typing import Optional

from pydantic import BaseModel


class AddTokenPo(BaseModel):
    user_id: Optional[int] = 0
    status: Optional[int] = 1
    name: str
    expired_time: Optional[str] = None
