from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse

import json
import configparser, os
from models.aroio import Aroio

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


# @aroio_api.post("/settings/network")
# async def create_item(item: Aroio):
#     return Aroio

@aroio_api.patch("/settings/network")
async def update_item(formData):
    aroio_db.configuration.network = formData
    json_string = json.dumps(aroio_db.__dict__)
    with open('aroio_db.json', 'w') as outfile:
        json.dump(json_string, outfile)

    with open('aroio_db.json') as json_file:
        return Aroio.from__json(json_file)

# @aroio_api.patch("/settings/network", response_model=Aroio)
# async def update_item(item_id: str, item: Aroio):
#     stored_item_model = Aroio(**item)
#     update_data = item.dict(exclude_unset=True)
#     updated_item = stored_item_model.copy(update=update_data)
#     items[item_id] = jsonable_encoder(updated_item)
#     return updated_item


@aroio_api.get("/filters")
async def root():
    return aroio_db


@aroio_api.patch("/filters/{filter_id}")
async def root():
    return {"message": "ABACUS Aroio API for Webinterfaces and App-Connections"}
