from pydantic import BaseModel
from typing import Optional

class StreamingConfig(BaseModel):
    servername: Optional[str] = None
    serverport: Optional[int] = None
    squeezeuser: Optional[str] = None
    squeezepwd: Optional[str] = None
    playername: str = "Aroio Player"