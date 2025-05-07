from fastapi import APIRouter
from src.services.monitor_service import buscar_novas_movimentacoes


router = APIRouter()

@router.get("/ultimas-movimentacoes")
async def get_ultimas_movimentacoes():
    return await buscar_novas_movimentacoes()