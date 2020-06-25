from typing import Optional
from pydantic import BaseModel


class Command(BaseModel):
    value: Optional[bool]
    message: Optional[str]
    command: str
