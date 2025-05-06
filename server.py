import asyncio
from fastapi import FastAPI
from src.services.monitor_service import MonitorService
from src.routers import mov


app = FastAPI()
monitor_service = MonitorService()

@app.on_event("startup")
async def startup_event():
    # Inicia o monitoramento em background
    asyncio.create_task(monitor_service.monitorar_movimentacoes())

app.include_router(mov.router)