from fastapi import FastAPI
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import json
import configparser, os


##########################
# Userconfig.txt parser
##########################

# config = configparser.ConfigParser()
# config.read_file(open('userconfig.txt'))
# config.read(['site.cfg', os.path.expanduser('~/.myapp.cfg')])

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


class Aroio(BaseModel):
    name: str
    timestamp: datetime
    description: str
    network: NetworkConfig
    system: SystemConfig
    streaming: StreamingConfig
    audio: AudioConfig
    convolver: ConvolverConfig


##########################
# DB Configuration
##########################
with open('aroio_db.json') as json_file:
    aroio_db = json.load(json_file)

##########################
# API Configuration
##########################
aroio_api = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
]

aroio_api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@aroio_api.get("/settings")
async def read_item():
    return aroio_db


@aroio_api.patch("/settings}", response_model=Aroio)
async def update_item(aroioSettings: Aroio):
    update_item_encoded = jsonable_encoder(aroioSettings)
    with open('aroio_db.json', 'w') as outfile:
        json.dump(update_item_encoded, outfile)
    return update_item_encoded


@aroio_api.get("/filters")
async def root():
    return aroio_db


@aroio_api.patch("/filters/{filter_id}")
async def root():
    return {"message": "ABACUS Aroio API for Webinterfaces and App-Connections"}
