from pydantic import BaseModel
from typing import Optional, List
import json

class NetworkConfig(BaseModel):
        hostname: str
        wifi: bool
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
    updateserver: str
    betaserver: str
    usebeta: bool
    platform: str
    userpasswd: str
    known_version: str
    btkey: str
    advanced: bool
    display_rotate: bool

class StreamingConfig(BaseModel):
    servername: Optional[str] = None
    serverport: Optional[str] = None
    squeezeuser: Optional[str] = None
    squeezepwd: Optional[str] = None
    playername: str


class AudioConfig(BaseModel):
    audioplayer: str
    rate: str
    sprate: str
    channels: str
    mscoding: bool
    volume: str
    soundcard: str
    resampling: str
    volume_start: str
    audio_output: str
    measurement_output: str
    debug: str
    jackbuffer: str
    jackperiod: str
    raw_player: str
    raw_playerms: str
    squeeze_maxfrequency: str
    squeeze_intbuffer: str
    squeeze_outbuffer: str
    sp_outbuffer: str
    sp_period: str
    bf_partitions: str
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
    def_coeff: Optional[str] = "0"
    filters: List[Filter] = []

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
