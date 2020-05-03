from fastapi import APIRouter, Depends, status
from data import datasource
from typing import List

from exceptions import ForbiddenException, NotFoundException
from .oauth_routers import get_auth_aroio
from models import (
    Aroio,
    Configuration,
    NetworkConfig,
    ConvolverConfig,
    SystemConfig,
    StreamingConfig,
    AudioConfig,
    WebinterfaceConfig,
    Filter,
    FilterInDb
)

router = APIRouter()


#########
# AROIO #
#########

@router.get("/aroio", tags=["aroio"])
async def get_aroio(aroio: Aroio = Depends(get_auth_aroio)):
    """Get saved Aroio from system."""
    return aroio


##########
# CONFIG #
##########

@router.patch("/config", tags=["config"])
async def update_configuration(config: Configuration, aroio: Aroio = Depends(get_auth_aroio)):
    """Update the complete configuration. Returns the updated configuration."""
    aroio.configuration = config
    datasource.save(aroio=aroio)
    return aroio.configuration


@router.patch("/config/network", tags=["config"])
async def update_network_config(network_config: NetworkConfig, aroio: Aroio = Depends(get_auth_aroio)):
    """Update the network configuration. Returns the updated network configuration."""
    if not network_config.lan.valid_ipv4_addresses_or_none():
        raise ForbiddenException(detail="Incorrect format of IPv4 addresses.")

    aroio.configuration.network = network_config
    datasource.save(aroio=aroio)
    return aroio.configuration.network


@router.patch("/config/convolver", tags=["config"])
async def update_convolver_config(convolver: ConvolverConfig, aroio: Aroio = Depends(get_auth_aroio)):
    """Update the Convolver configuration."""
    aroio.configuration.convolver = convolver
    datasource.save(aroio=aroio)
    return aroio.configuration.convolver


@router.patch("/config/system", tags=["config"])
async def update_system_config(system_config: SystemConfig, aroio: Aroio = Depends(get_auth_aroio)):
    """Update the system configuration."""
    aroio.configuration.system = system_config
    datasource.save(aroio=aroio)
    return aroio.configuration.system


@router.patch("/config/streaming", tags=["config"])
async def update_streaming_config(streaming_config: StreamingConfig, aroio: Aroio = Depends(get_auth_aroio)):
    """Update the streaming configuration."""
    aroio.configuration.streaming = streaming_config
    datasource.save(aroio=aroio)
    return aroio.configuration.streaming


@router.patch("/config/audio", tags=["config"])
async def update_audio_config(audio_config: AudioConfig, aroio: Aroio = Depends(get_auth_aroio)):
    """Update the streaming configuration."""
    aroio.configuration.audio = audio_config
    datasource.save(aroio=aroio)
    return aroio.configuration.audio


@router.patch("/config/webinterface", tags=["config"])
async def update_audio_config(webinterface_config: WebinterfaceConfig, aroio: Aroio = Depends(get_auth_aroio)):
    """Update the webinterface configuration."""
    aroio.configuration.webinterface = webinterface_config
    datasource.save(aroio=aroio)
    return aroio.configuration.webinterface


##########
# FILTER #
##########
@router.get("/filters", tags=["filter"])
async def load_filters(aroio: Aroio = Depends(get_auth_aroio)):
    """Get all filters of Aroio system."""
    return aroio.configuration.convolver.filters


@router.get("/filters/{filter_id}", tags=["filter"])
async def load_filter(filter_id: int, aroio: Aroio = Depends(get_auth_aroio)):
    """Get filter with filter_id"""
    filters = aroio.configuration.convolver.filters
    if filter_id not in [f.id for f in filters]:
        raise NotFoundException(detail=f'Not fount filter with id {filter_id}')

    for filter in filters:
        if filter.id == filter_id:
            return filter


@router.post("/filters", tags=["filter"], status_code=status.HTTP_201_CREATED)
async def create_filter(filter: Filter, aroio: Aroio = Depends(get_auth_aroio)):
    """Creates a new filter in the database. Returns the created filter with its id"""
    filters = aroio.configuration.convolver.filters
    if len(filters) >= 10:
        raise ForbiddenException(detail="Only 10 filters are allowed with the userconfig.txt pattern")

    # compute next possible filter id by maximum id
    filter_id = max([f.id for f in filters]) + 1
    filter_in_db = FilterInDb(id=filter_id, **filter.dict())
    aroio.configuration.convolver.filters.append(filter_in_db)
    datasource.save(aroio=aroio)
    return filter_in_db


@router.delete("/filters", tags=["filter"], status_code=status.HTTP_200_OK)
async def delete_filter(filter_id: int, aroio: Aroio = Depends(get_auth_aroio)):
    """Deletes filter with the given filter_id."""
    filter_to_delete = -1
    for idx, f in enumerate(aroio.configuration.convolver.filters):
        if f.id == filter_id:
            filter_to_delete = idx

    if filter_to_delete == -1:
        raise NotFoundException(detail=f'Filter to delete not found. Filter id: {filter_to_delete}')

    aroio.configuration.convolver.filters.pop(filter_to_delete)
    datasource.save(aroio=aroio)
