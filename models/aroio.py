import datetime
from typing import List, Optional

from pydantic import BaseModel

from auth import Authentication
from exceptions import ForbiddenException
from data.validation import Validator

class LAN(BaseModel):
    dhcp: bool = True
    ipaddr: Optional[str] = None
    netmask: Optional[str] = None
    dnsserv: Optional[str] = None
    gateway: Optional[str] = None

    def valid_ipv4_addresses_or_none(self):
        """Returns if all addresses of LAN are IPv4 addresses, when dhcp is set to False."""
        if self.dhcp:
            return True
        
        for addr in [self.ipaddr, self.netmask, self.dnsserv, self.gateway]:
            if not Validator.ipv4(address=addr):
                return False
        return True


class WLAN(LAN):
    ssid: Optional[str] = None
    pwd: Optional[str] = None


class NetworkConfig(BaseModel):
    hostname: str = "Aroio"
    wifi: bool = False
    lan: LAN = LAN()
    wlan: WLAN = WLAN()


class SystemConfig(BaseModel):
    updateserver: str = "http://www.abacus-electronics.de/aroio-4"
    usebeta: bool = False
    platform: str = "AroioSU"
    known_version: str = "4.16.82"
    btkey: str = "2107"


class WebinterfaceConfig(BaseModel):
    display_rotate: bool = False
    dark_mode: bool = False
    initial_setup: bool = True
    advanced_configuration: bool = False


class StreamingConfig(BaseModel):
    servername: Optional[str] = None
    serverport: Optional[int] = None
    squeezeuser: Optional[str] = None
    squeezepwd: Optional[str] = None
    playername: str = "Aroio Player"


class PlayerConfig(BaseModel):
    mscoding: bool = False
    measurement_output: str = "vol-plug-ms"
    squeezelite: bool = False
    gmediarender: bool = False
    shairportsync: bool = False
    bluealsaaplay: bool = False
    input: bool = False
    netjack: bool = False


class OutputConfig(BaseModel):
    audio_output: str = "vol-plug"
    rate: int = 44100
    direct_config: PlayerConfig = PlayerConfig()
    bus_config: PlayerConfig = PlayerConfig()
    convolver_config: PlayerConfig = PlayerConfig()


class AudioConfig(BaseModel):
    audioplayer: str = None
    channels: int = 2
    soundcard: str = "AroioDAC"
    resampling: str = "speexrate_medium"
    volume_start: int = -15
    debug: bool = False
    jackbuffer: int = 4096
    jackperiod: int = 3
    raw_player: str = "shairportsync"
    raw_playerms: str = "squeezelite"
    squeeze_maxfrequency: int = 192000
    squeeze_alsabuffer: int = 16384
    squeeze_alsaperiod: int = 4
    squeeze_intbuffer: int = 16384
    squeeze_outbuffer: int = 8192
    sp_outbuffer: int = 32768
    sp_period: int = 2
    sp_samplerate: int = 44100
    bf_partitions: int = 2
    output_configuration: OutputConfig = OutputConfig()


class Filter(BaseModel):
    is_active: bool = False
    coeff_name: Optional[str] = None
    coeff_comment: Optional[str] = None
    coeff_att: Optional[str] = None
    coeff_delay: Optional[str] = None


class FilterInDb(Filter):
    id: int = 0


class ConvolverConfig(BaseModel):
    debug: bool = False
    load_prefilter: bool = False
    brutefir: bool = False
    def_coeff: Optional[int] = 0
    filters: List[FilterInDb] = []


class Configuration(BaseModel):
    network: NetworkConfig = NetworkConfig()
    system: SystemConfig = SystemConfig()
    streaming: StreamingConfig = StreamingConfig()
    audio: AudioConfig = AudioConfig()
    convolver: ConvolverConfig = ConvolverConfig()
    webinterface: WebinterfaceConfig = WebinterfaceConfig()


class Aroio(BaseModel):
    name: str = "aroio"
    password: str = Authentication.hash_password("abacus")  # default password
    authentication_enabled: bool = True
    timestamp: float = datetime.datetime.now().timestamp()
    description: str = "This is a raw Aroio Configuration without any device specifications. ÜÄÖ"
    configuration: Configuration = Configuration()
