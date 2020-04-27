from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

import json
import yaml
import configparser, os
from models.aroio import Aroio, NetworkConfig, ConvolverConfig
from security import Security
from database import DataSource


##########################
# API Configuration
##########################
aroio_api = FastAPI()
datasource = DataSource()


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
    return datasource.load_aroio()


@aroio_api.post("/settings")
async def upsert_aroio(aroio: Aroio):
    """Sync Aroio sent within request body"""
    return datasource.sync_aroio(aroio=aroio)


@aroio_api.patch("/settings")
async def update_item(aroio: Aroio):
    """Update the complete configuration"""
    datasource.sync_aroio(aroio=aroio)

@aroio_api.patch("/settings/network")
async def update_item(network_config: NetworkConfig):
    """Update the network configuration"""
    datasource.sync_network_config(network_config=network_config)


@aroio_api.patch("/settings/convolver")
async def update_item(convolver: ConvolverConfig):
    """Update the Convolver configuration"""
    datasource.sync_convolver(convolver=convolver)


@aroio_api.get("/filters")
async def root():
    return datasource.load_aroio()


@aroio_api.on_event("shutdown")
def shutdown_event():
    """Persist all information in database in the userconfig.txt file"""
    # TODO - persist it
    pass


@aroio_api.get("/translations/{lang}")
async def read_item(lang: str):
    """Get saved Aroio from system"""
    return datasource.load_translations(lang=lang)
