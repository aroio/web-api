from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from fastapi.responses import ORJSONResponse


import json
import configparser, os
from models.aroio import Aroio, ConvolverConfig, NetworkConfig, from_json_to_aroio

##########################
# relevant files
##########################
AROIO_DB = 'aroio_db.json'

##########################
# Userconfig.txt parser
##########################

# config = configparser.ConfigParser()
# config.read_file(open('userconfig.txt'))
# config.read(['site.cfg', os.path.expanduser('~/.myapp.cfg')])

##########################
# DB Configuration
##########################
def load_aroio() -> Aroio:
    """Loading the aroio json from system"""
    with open(AROIO_DB, "r") as json_file:
        return from_json_to_aroio(json_file)


def sync_aroio(aroio: Aroio) -> Aroio:
    """Keeping the aroio_db in memory and in json file in sync"""
    with open(AROIO_DB, 'w+') as db:
        db.write(json.dumps(aroio.dict()))
        db.close()
    return aroio

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

##########################
# Routing Setup
##########################

@aroio_api.get("/settings")
async def read_item():
    """Get saved Aroio from system"""
    return load_aroio()


@aroio_api.post("/settings")
async def upsert_aroio(aroio: Aroio):
    """Sync Aroio sent within request body"""
    return sync_aroio(aroio=aroio)


@aroio_api.patch("/settings/network")
async def update_item(formData: NetworkConfig):
    """Update the network configuration"""
    aroio = load_aroio()
    aroio.configuration.network = formData
    sync_aroio(aroio=aroio)


@aroio_api.get("/filters")
async def root():
    return load_aroio()
