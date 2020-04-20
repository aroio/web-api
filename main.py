from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

import json
import configparser, os
from models.aroio import Aroio, ConvolverConfig

##########################
# Userconfig.txt parser
##########################

# config = configparser.ConfigParser()
# config.read_file(open('userconfig.txt'))
# config.read(['site.cfg', os.path.expanduser('~/.myapp.cfg')])

##########################
# DB Configuration
##########################
with open('aroio_db.json') as json_file:
    # Parse JSON into an object with attributes corresponding to dict keys.
    aroio_db = Aroio.from__json(json_file)


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

#
# @aroio_api.patch("/settings}", response_class=Aroio)
# async def update_item(aroioSettings: Aroio):
#     update_item_encoded = jsonable_encoder(aroioSettings)
#     with open('aroio_db.json', 'w') as outfile:
#         json.dump(update_item_encoded, outfile)
#     return update_item_encoded
#

@aroio_api.get("/filters")
async def root():
    return aroio_db


# @aroio_api.patch("/filters/{filter_id}")
# async def root():
#     return {"message": "ABACUS Aroio API for Webinterfaces and App-Connections"}

class Item(BaseModel):
    id: str

@aroio_api.patch("/filters/{filter_id}")
async def update_filter(filter_id: str, item: Item):
    return item