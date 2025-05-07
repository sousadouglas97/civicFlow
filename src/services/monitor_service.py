import asyncio
from datetime import datetime
from src.database.repository.mov_repository import buscar_novas_movimentacoes


class MonitorService:
    def __init__(self):
        self.ultima_data = datetime.now().strftime('%d-%m-%Y')  
        self.ultima_hora = datetime.now().strftime("%H:%M:%S")
    
        
    async def processar_movimentacoes(self, mov):
        print(mov)
        return await mov
    
    
    async def monitorar_movimentacoes(self):
        while True:
            novas_movimentacoes = await buscar_novas_movimentacoes(self.ultima_data, self.ultima_hora)
            
            if novas_movimentacoes:
                print(f"Novas movimentações encontradas: {len(novas_movimentacoes)}")
                
                self.ultima_data = datetime.now().strftime('%d-%m-%Y')  
                self.ultima_hora = datetime.now().strftime("%H:%M:%S")
    
                await self.processar_movimentacoes(novas_movimentacoes)
            
            await asyncio.sleep(30)
    