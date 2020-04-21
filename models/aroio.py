from pydantic import BaseModel
from typing import Optional
import json

class NetworkConfig(BaseModel):
        hostname: str
        dhcp: bool
        wifi: bool
        ipaddr: Optional[str] = None
        netmask: Optional[str] = None
        dnsserv: Optional[str] = None
        gateway: Optional[str] = None
        wlanssid: Optional[str] = None
        wlanpwd: Optional[str] = None


class SystemConfig(BaseModel):
    updateserver: str
    betaserver: str
    usebeta: str
    platform: str
    userpasswd: str


class StreamingConfig(BaseModel):
    servername: Optional[str] = None
    serverport: Optional[str] = None
    squeezeuser: Optional[str] = None
    squeezepwd: Optional[str] = None
    playername: str


class AudioConfig(BaseModel):
    audioplayer: str
    rate: str
    channels: str
    mscoding: str
    volume: str
    jackbuffer: str
    soundcard: str


class ConvolverConfig(BaseModel):
    debug: str
    load_prefilter: str
    brutefir: str
    def_coeff: str
    def_scoeff: str


class Configuration(BaseModel):
    network: NetworkConfig
    system: SystemConfig
    streaming: StreamingConfig
    audio: AudioConfig
    convolver: ConvolverConfig


class Aroio(BaseModel):
    name: str
    timestamp: str
    description: str
    configuration: Configuration

    
def from_json_to_aroio(json_string: str) -> Aroio:
    aroio_db = json.load(json_string)
    return Aroio(**aroio_db)
