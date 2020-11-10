from pydantic import BaseModel


class SystemConfig(BaseModel):
    updateserver: str = "http://www.abacus-electronics.de/aroio-4"
    usebeta: bool = False
    platform: str = "AroioSU"
    known_version: str = "4.16.82"
    btkey: str = "2107"
