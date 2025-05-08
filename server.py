from fastapi import FastAPI
from src.routers import monitor_router

app = FastAPI()

app.include_router(monitor_router.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Sistema de monitoramento de processos"}