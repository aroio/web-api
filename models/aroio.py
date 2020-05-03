import datetime
from typing import List, Optional

from pydantic import BaseModel

from auth import Authentication
from exceptions import ForbiddenException
from data.validation import Validator

from .network import NetworkConfig
from .system import SystemConfig
from .streaming import StreamingConfig
from .audio import AudioConfig
from .convolver import ConvolverConfig
from .webinterface import WebinterfaceConfig


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
