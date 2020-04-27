from fastapi import APIRouter
from datasource import DataSource
from models.aroio import *

############
# Settings router
############
router = APIRouter()
datasource = DataSource()

@router.get("/settings", tags=["settings"])
async def read_item():
    """Get saved Aroio from system"""
    return datasource.load_aroio()


@router.patch("/settings", tags=["settings"])
async def update_aroio(aroio: Aroio):
    """Update the complete configuration"""
    return datasource.sync(aroio=aroio)


@router.patch("/settings/network", tags=["settings"])
async def update_item(network_config: NetworkConfig):
    """Update the network configuration"""
    return datasource.sync(network_config=network_config)


@router.patch("/settings/convolver", tags=["settings"])
async def update_item(convolver: ConvolverConfig):
    """Update the Convolver configuration"""
    return datasource.sync(convolver=convolver)


@router.get("/filters")
async def load_filters():
    return datasource.load_aroio().configuration.convolver.filters


@router.get("/translations/{lang}")
async def read_item(lang: str):
    """Get saved Aroio from system"""
    return datasource.load_translations(lang=lang)
