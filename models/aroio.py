import json

class NetworkConfig:
    def __init__(self, hostname: str, dhcp: str, ipaddr: str, netmask: str, dnsserv: str, gateway: str, wlanssid: str, wlanpwd: str):
        self.hostname = hostname
        self.dhcp = dhcp
        self.ipaddr = ipaddr
        self.netmask = netmask
        self.dnsserv = dnsserv
        self.gateway = gateway
        self.wlanssid = wlanssid
        self.wlanpwd = wlanpwd


class SystemConfig:
    def __init__(self, updateserver: str, betaserver: str, usebeta: str, platform: str, userpasswd: str):
        self.updateserver = updateserver
        self.betaserver = betaserver
        self.usebeta = usebeta
        self.platform = platform
        self.userpasswd = userpasswd


class StreamingConfig:
    def __init__(self, servername: str, serverport: str, squeezeuser: str, squeezepwd: str, playername: str):
        self.servername = servername
        self.serverport = serverport
        self.squeezeuser = squeezeuser
        self.squeezepwd = squeezepwd
        self.playername = playername


class AudioConfig:
    def __init__(self, audioplayer: str, rate: str, channels: str, mscoding: str, volume: str, jackbuffer: str,
                 soundcard: str):
        self.audioplayer = audioplayer
        self.rate = rate
        self.channels = channels
        self.mscoding = mscoding
        self.volume = volume
        self.jackbuffer = jackbuffer
        self.soundcard = soundcard


class ConvolverConfig:
    def __init__(self, debug: str, load_prefilter: str, brutefir: str, def_coeff: str, def_scoeff: str):
        self.debug = debug
        self.load_prefilter = load_prefilter
        self.brutefir = brutefir
        self.def_coeff = def_coeff
        self.def_scoeff = def_scoeff

class Configuration:
    def __init__(self, network: NetworkConfig, system: SystemConfig, streaming: StreamingConfig, audio: AudioConfig, convolver: ConvolverConfig):
        self.network = network
        self.system = system
        self.streaming = streaming
        self.audio = audio
        self.convolver = convolver

class Aroio:
    def __init__(self, name: str, timestamp: str, description: str, configuration: Configuration):
        self.name = name
        self.timestamp = timestamp
        self.description = description
        self.configuration = configuration

    @classmethod
    def from__json(cls, json_string):
        aroio_db = json.load(json_string)
        return cls(**aroio_db)
#
# from pydantic import BaseModel
# from datetime import datetime
#
#
# class NetworkConfig(BaseModel):
#     hostname: str
#     dhcp: str
#     ipaddr: str
#     netmask: str
#     dnsserv: str
#     gateway: str
#     wlanssid: str
#     wlanpwd: str
#
#
# class SystemConfig(BaseModel):
#     updateserver: str
#     betaserver: str
#     usebeta: str
#     platform: str
#     userpasswd: str
#
#
# class StreamingConfig(BaseModel):
#     servername: str
#     serverport: str
#     squeezeuser: str
#     squeezepwd: str
#     playername: str
#
#
# class AudioConfig(BaseModel):
#     audioplayer: str
#     rate: str
#     channels: str
#     mscoding: str
#     volume: str
#     jackbuffer: str
#     soundcard: str
#
#
# class ConvolverConfig(BaseModel):
#     debug: str
#     load_prefilter: str
#     brutefir: str
#     def_coeff: str
#     def_scoeff: str
#
#
# class Aroio(BaseModel):
#     name: str
#     timestamp: datetime
#     description: str
#     network: NetworkConfig
#     system: SystemConfig
#     streaming: StreamingConfig
#     audio: AudioConfig
#     convolver: ConvolverConfig
