from typing import Optional

from pydantic import BaseModel


class AddChannelPo(BaseModel):
    type: int
    key: str
    name: str
    base_url: Optional[str] = None
    models: str
    weight: Optional[int] = 1
    manage_key: Optional[str] = None
