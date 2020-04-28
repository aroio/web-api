from pydantic import BaseModel
from typing import Optional, List
import json
import datetime
from auth import Authentication


class NetworkConfig(BaseModel):
    hostname: str = "Aroio"
    wifi: bool = False
    lan_dhcp: Optional[bool] = True
    lan_ipaddr: Optional[str] = None
    lan_netmask: Optional[str] = None
    lan_dnsserv: Optional[str] = None
    lan_gateway: Optional[str] = None
    wlan_dhcp: Optional[bool] = True
    wlan_ipaddr: Optional[str] = None
    wlan_netmask: Optional[str] = None
    wlan_dnsserv: Optional[str] = None
    wlan_gateway: Optional[str] = None
    wlanssid: Optional[str] = None
    wlanpwd: Optional[str] = None


class SystemConfig(BaseModel):
    updateserver: str = "http://www.abacus-electronics.de/aroio-4"
    usebeta: bool = False
    platform: str = "AroioSU"
    userpasswd: str = Authentication.hash_password("abacus")  # default password
    known_version: str = "4.16.82"
    btkey: str = "2107"
    advanced: bool = False
    display_rotate: bool = False


class StreamingConfig(BaseModel):
    servername: Optional[str] = None
    serverport: Optional[int] = None
    squeezeuser: Optional[str] = None
    squeezepwd: Optional[str] = None
    playername: str = "Aroio Player"


class AudioConfig(BaseModel):
    rate: int = 176400
    sprate: int = 44100
    channels: int = 2
    mscoding: bool = False
    soundcard: str = "AroioDAC"
    resampling: str = "speexrate_medium"
    volume_start: int = -15
    audio_output: str = "jack-bfms"
    measurement_output: str = "vol-plug-ms"
    debug: bool = False
    jackbuffer: int = 8192
    jackperiod: int = 3
    raw_player: str = "shairportsync"
    raw_playerms: str = "squeezelite"
    squeeze_maxfrequency: int = 192000
    squeeze_intbuffer: int = 4096
    squeeze_outbuffer: int = 4096
    sp_outbuffer: int = 32768
    sp_period: int = 2
    bf_partitions: int = 2
    dmix_squeezelite: Optional[bool] = False
    dmix_gmediarender: Optional[bool] = False
    dmix_shairportsync: Optional[bool] = False
    dmix_bluealsaaplay: Optional[bool] = False
    dmixms_squeezelite: Optional[bool] = False
    dmixms_gmediarender: Optional[bool] = False
    dmixms_shairportsync: Optional[bool] = False
    dmixms_bluealsaaplay: Optional[bool] = False
    jack_squeezelite: Optional[bool] = False
    jack_gmediarender: Optional[bool] = False
    jack_shairportsync: Optional[bool] = False
    jack_bluealsaaplay: Optional[bool] = False
    jack_netjack: Optional[bool] = False
    jack_input: Optional[bool] = False
    jackms_squeezelite: Optional[bool] = False
    jackms_gmediarender: Optional[bool] = False
    jackms_shairportsync: Optional[bool] = False
    jackms_bluealsaaplay: Optional[bool] = False
    jackms_netjack: Optional[bool] = False
    jackms_input: Optional[bool] = False
    jackbf_squeezelite: Optional[bool] = False
    jackbf_gmediarender: Optional[bool] = False
    jackbf_shairportsync: Optional[bool] = False
    jackbf_bluealsaaplay: Optional[bool] = False
    jackbf_netjack: Optional[bool] = False
    jackbf_input: Optional[bool] = False
    jackbfms_squeezelite: Optional[bool] = False
    jackbfms_gmediarender: Optional[bool] = False
    jackbfms_shairportsync: Optional[bool] = False
    jackbfms_bluealsaaplay: Optional[bool] = False
    jackbfms_netjack: Optional[bool] = False
    jackbfms_input: Optional[bool] = False


class Filter(BaseModel):
    coeff_name: Optional[str] = None
    coeff_comment: Optional[str] = None
    coeff_att: Optional[str] = None
    coeff_delay: Optional[str] = None


class ConvolverConfig(BaseModel):
    debug: bool = False
    load_prefilter: bool = False
    brutefir: bool = False
    def_coeff: Optional[int] = 0
    filters: List[Filter] = []


class Configuration(BaseModel):
    network: NetworkConfig = NetworkConfig()
    system: SystemConfig = SystemConfig()
    streaming: StreamingConfig = StreamingConfig()
    audio: AudioConfig = AudioConfig()
    convolver: ConvolverConfig = ConvolverConfig()


class Aroio(BaseModel):
    name: str = "aroio"
    timestamp: float = datetime.datetime.now().timestamp()
    description: str = "This is a raw Aroio Configuration without any device specifications. ÜÄÖ"
    initial_config: bool = True
    configuration: Configuration = Configuration()

    @staticmethod
    def initial_aroio():
        return Aroio()

    @staticmethod
    def create_from_json(json_str: str):
        aroio_db = json.load(json_str)
        return Aroio(**aroio_db)
