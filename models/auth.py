from pydantic import BaseModel
from typing import Optional, List

class Token(BaseModel):
    token: str
    token_type: str
    roles: Optional[List] = ['ROLE_ADMIN']
