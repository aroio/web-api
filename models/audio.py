from pydantic import BaseModel

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
