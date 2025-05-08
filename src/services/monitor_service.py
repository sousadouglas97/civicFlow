import os
import time
import json
import asyncio
from datetime import date
from src.codex.config import Config
from src.codex.sessao import CodexSessao
from src.database.repository.mov_repository import buscar_novas_movimentacoes


class MonitorService:
    def __init__(self):
        self.ultima_data = date.today()
        self.ultima_hora = str(time.strftime("%H%M%S"))
    
    
    def obter_dados_codex(self):
        data_session = {
            'usuario': os.getenv('CODEX_USER'), 
            'senha': os.getenv('CODEX_PASSWORD'), 
            'duracao_token_minutos': os.getenv('TIME_TOKEN'),
            'base_url': os.getenv('CODEX_URL')
        }
        
        session = CodexSessao(caminho_token='token\\token.json', **data_session) 
        return session


    def obter_por_processo(self, numero_processo):
        r = self.obter_dados_codex.get(f'/processo/recuperarCoordenadasPorNumero/{numero_processo}')        
        return json.loads(r.content)[1] 
    
     
    async def monitorar_movimentacoes(self):
        while True:
            novas_movimentacoes = await buscar_novas_movimentacoes(self.ultima_data, self.ultima_hora)
            
            if novas_movimentacoes:
                print(f"Novas movimentações encontradas: {len(novas_movimentacoes)}")
                
                self.ultima_data = date.today()
                self.ultima_hora = str(time.strftime("%H%M%S"))
    
                await self.processar_movimentacoes(novas_movimentacoes)
            
            await asyncio.sleep(3)
    
    
#    async def processar_movimentacoes(self, mov):
#        print(mov)
#        return await mov
#    
