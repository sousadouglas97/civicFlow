import os
import logging
from configparser import ConfigParser
from typing import Dict

# special exception that suppresses stack traces when it happens
class UserError(Exception):
    '''
    Classe especial para suprimir "stack traces"
    '''

logging.basicConfig(format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Arquivo de configuração (pode ser adicionado o caminho absoluto)
ARQUIVO_CONFIG = "treap.conf"

class Config():
    '''
    Retorna informações de configuração, como nome de usuário, senha, etc.
    A prioridade é dada a valores armazenada em variáveis de ambientes e,
    em segundo lugar, ao arquivo de configuração "treap.conf" (pode ser
    modificado pela variável "ARQUIVO_CONFIG").
    '''
    def __init__(self, caminho_conf : str) -> None:
        if os.path.isfile(caminho_conf):
            self._config_file = ConfigParser()
            self._config_file.read(caminho_conf)
            logger.info("Lendo configuração do arquivo: %s", caminho_conf)
        else: 
            raise UserError(f"Arquivo {caminho_conf} não encontrado.")

    def _get_env(self, componente:str, opcao: str) -> str:
        '''
        Retorna a variável de ambiente da seção desejada.
        Formato: SEÇÃO_OPÇÃO
        '''
        env_name = f"{componente.upper()}_{opcao.upper}"
        env_value = os.getenv(env_name, None)
        if env_value is not None:
            logger.info('Componente %s utilizando variável de ambiente para a opção: %s'
                        , componente, opcao)
        return env_value

    def get_opcao(self, componente: str, opcao: str) -> str:
        '''
        Retorna uma string com a opção do componente informado. 
        Variáveis de ambientes possuem precedência sobre os arquivos de configuração.
        '''
        env_value = self._get_env(componente, opcao)
        if env_value is not None:
            return env_value
        if not self._config_file.has_option(componente, opcao):
            raise UserError(f"Opção {opcao} não encontrado no componente {componente}")
        return self._config_file.get(section=componente, option=opcao)

    def get_secao(self, componente: str) -> Dict:
        ''' 
        Retorna um dicionário com toda a seção do componente informado. 
        Variáveis de ambientes não são consideradas neste método.
        '''
        if not self._config_file.has_section(componente):
            raise UserError(f"Componente {componente} não encontrado no arquivo de configuração.")
        return Dict(self._config_file.items(componente))
