from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from fastapi.responses import ORJSONResponse

import json
import yaml
import configparser, os
from models.aroio import Aroio, NetworkConfig, ConvolverConfig, from_json_to_aroio, get_new_aroio

##########################
# relevant files
##########################
AROIO_DB = 'aroio_db.json'
AROIO_LANG_DE = 'translations/messages.de.yml'
AROIO_LANG_EN = 'translations/messages.en.yml'


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
    try:
        with open(AROIO_DB, "r") as json_file:
            return from_json_to_aroio(json_file)
    except IOError:
        print("Database not accessible, generate Database.")
        return sync_aroio(get_new_aroio())


def load_translations(lang: str):
    """Loading the aroio translations from system"""
    print(lang)
    if lang == "DE" or lang == "de":
        with open(AROIO_LANG_DE, "r") as yml_file:
            return yaml.load(yml_file)
    elif lang == "EN" or lang == "en":
        with open(AROIO_LANG_EN, "r") as yml_file:
            return yaml.load(yml_file)


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


@aroio_api.patch("/settings")
async def update_item(formData: Aroio):
    """Update the complete configuration"""
    sync_aroio(aroio=formData)

@aroio_api.patch("/settings/network")
async def update_item(formData: NetworkConfig):
    """Update the network configuration"""
    aroio = load_aroio()
    aroio.configuration.network = formData
    sync_aroio(aroio=aroio)


@aroio_api.patch("/settings/convolver")
async def update_item(formData: ConvolverConfig):
    """Update the Convolver configuration"""
    aroio = load_aroio()
    aroio.configuration.convolver = formData
    sync_aroio(aroio=aroio)


@aroio_api.get("/filters")
async def root():
    return load_aroio()


@aroio_api.on_event("shutdown")
def shutdown_event():
    """Persist all information in database in the userconfig.txt file"""
    # TODO - persist it
    pass


@aroio_api.get("/translations/{lang}")
async def read_item(lang: str):
    """Get saved Aroio from system"""
    return load_translations(lang=lang)
