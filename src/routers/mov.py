from fastapi import FastAPI
from src.services.monitor_service import buscar_novas_movimentacoes


app = FastAPI()

@app.get("/ultimas-movimentacoes")
async def get_ultimas_movimentacoes():
    return await buscar_novas_movimentacoes()