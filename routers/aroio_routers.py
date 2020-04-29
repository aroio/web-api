from fastapi import APIRouter, Depends
from data import datasource
from typing import List

from .oauth_routers import get_auth_aroio
from models import (
    Aroio,
    Configuration,
    NetworkConfig,
    ConvolverConfig,
    Filter
)


router = APIRouter()

@router.get("/aroio", tags=["aroio"])
async def get_aroio(aroio: Aroio = Depends(get_auth_aroio)):
    """Get saved Aroio from system."""
    return aroio


@router.patch("/config", tags=["config"])
async def update_configuration(config: Configuration, aroio: Aroio = Depends(get_auth_aroio)):
    """Update the complete configuration. Returns the updated configuration."""
    aroio.configuration = config
    datasource.save(aroio=aroio)
    return aroio.configuration


@router.patch("/config/network", tags=["config"])
async def update_network_config(network_config: NetworkConfig, aroio: Aroio = Depends(get_auth_aroio)):
    """Update the network configuration. Returns the updated network configuration."""
    aroio.configuration.network = network_config
    datasource.save(aroio=aroio)
    return aroio.configuration.network


@router.patch("/config/convolver", tags=["config"])
async def update_convolver_config(convolver: ConvolverConfig, aroio: Aroio = Depends(get_auth_aroio)):
    """Update the Convolver configuration."""
    aroio.configuration.convolver = convolver
    datasource.save(aroio=aroio)
    return aroio.configuration.convolver


@router.get("/filters", tags=["filter"])
async def load_filters(aroio: Aroio = Depends(get_auth_aroio)):
    """Get all filters of Aroio system."""
    return aroio.configuration.convolver.filters


@router.patch("/filters", tags=["filter"])
async def update_filters(filters: List[Filter], aroio: Aroio = Depends(get_auth_aroio)):
    """Updating all filters with the input param filters."""
    aroio.configuration.convolver.filters = filters
    datasource.save(aroio=aroio)
    return aroio.configuration.convolver.filters
