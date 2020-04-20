from pydantic import BaseModel
import json

class NetworkConfig(BaseModel):
        hostname: str
        dhcp: str
        ipaddr: str
        netmask: str
        dnsserv: str
        gateway: str
        wlanssid: str
        wlanpwd: str


class SystemConfig(BaseModel):
    updateserver: str
    betaserver: str
    usebeta: str
    platform: str
    userpasswd: str


class StreamingConfig(BaseModel):
    servername: str
    serverport: str
    squeezeuser: str
    squeezepwd: str
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
