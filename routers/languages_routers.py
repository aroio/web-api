from fastapi import APIRouter
from data import datasource

router = APIRouter()

@router.get("/translations/{lang}", tags=["language"])
async def get_translations(lang: str):
    """Get saved Aroio from system"""
    return datasource.load_translations(lang=lang)