from pydantic import BaseModel
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str
    roles: Optional[List] = ['ROLE_ADMIN']
