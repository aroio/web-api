from fastapi import APIRouter
from database import DataSource
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


@router.post("/settings", tags=["settings"])
async def upsert_aroio(aroio: Aroio):
    """Sync Aroio sent within request body"""
    return datasource.sync_aroio(aroio=aroio)


@router.patch("/settings", tags=["settings"])
async def update_item(aroio: Aroio):
    """Update the complete configuration"""
    datasource.sync_aroio(aroio=aroio)


@router.patch("/settings/network", tags=["settings"])
async def update_item(network_config: NetworkConfig):
    """Update the network configuration"""
    datasource.sync_network_config(network_config=network_config)


@router.patch("/settings/convolver", tags=["settings"])
async def update_item(convolver: ConvolverConfig):
    """Update the Convolver configuration"""
    datasource.sync_convolver(convolver=convolver)


@router.get("/filters")
async def root():
    return datasource.load_aroio()


@router.get("/translations/{lang}")
async def read_item(lang: str):
    """Get saved Aroio from system"""
    return datasource.load_translations(lang=lang)
