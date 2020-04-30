from pydantic import BaseModel

class Token(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    aroio_name: str = None