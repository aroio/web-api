from fastapi import APIRouter
from data import datasource
from models.aroio import *

############
# Settings router
############
router = APIRouter()

@router.get("/settings", tags=["settings"])
async def get_aroio():
    """Get saved Aroio from system"""
    return datasource.load_aroio()


@router.patch("/settings", tags=["settings"])
async def update_aroio(aroio: Aroio):
    """Update the complete configuration"""
    return datasource.sync(aroio=aroio)


@router.patch("/settings/network", tags=["settings"])
async def update_network_config(network_config: NetworkConfig):
    """Update the network configuration"""
    return datasource.sync(network_config=network_config)


@router.patch("/settings/convolver", tags=["settings"])
async def update_convolver_config(convolver: ConvolverConfig):
    """Update the Convolver configuration"""
    return datasource.sync(convolver=convolver)


@router.get("/filters", tags=["settings"])
async def load_filters():
    return datasource.load_aroio().configuration.convolver.filters


@router.patch("/filters", tags=["settings"])
async def update_filters(filters: List[Filter]):
    return datasource.sync(filters=filters)


@router.get("/translations/{lang}", tags=["language"])
async def get_translations(lang: str):
    """Get saved Aroio from system"""
    return datasource.load_translations(lang=lang)
