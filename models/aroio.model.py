class NetworkConfig:
    hostname: str
    dhcp: str
    ipaddr: str
    netmask: str
    dnsserv: str
    gateway: str
    wlanssid: str
    wlanpwd: str


class SystemConfig:
    updateserver: str
    betaserver: str
    usebeta: str
    platform: str
    userpasswd: str


class StreamingConfig:
    servername: str
    serverport: str
    squeezeuser: str
    squeezepwd: str
    playername: str


class AudioConfig:
    audioplayer: str
    rate: str
    channels: str
    mscoding: str
    volume: str
    jackbuffer: str
    soundcard: str


class ConvolverConfig:
    debug: str
    load_prefilter: str
    brutefir: str
    def_coeff: str
    def_scoeff: str


class Aroio(BaseModel):
    name: str
    timestamp: datetime
    description: str
    network: NetworkConfig
    system: SystemConfig
    streaming: StreamingConfig
    audio: AudioConfig
    convolver: ConvolverConfig
