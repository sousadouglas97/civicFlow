import asyncio
from fastapi import APIRouter
from src.services.monitor_service import MonitorService


router = APIRouter()

@router.on_event("startup")
async def startup_event():
    monitor = MonitorService()
    # Inicia o monitoramento em segundo plano
    asyncio.create_task(monitor.monitorar_movimentacoes())


@router.get("/monitor/start")
async def start_monitoring():
    return {"message": "Monitoramento de movimentações iniciado. Verifique o console para acompanhar."}