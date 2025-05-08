import logging
import requests
from codex_config import Config

logging.basicConfig(format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)

class BearerAuth(requests.auth.AuthBase): #pylint: disable=too-few-public-methods
    '''
    Responsável por guardar o token de autenticação com o Codex
    '''
    def __init__(self, token_sessao: str, auth_schema: str="Bearer") -> None:
        self.token_sessao = token_sessao
        self.auth_scheme = auth_schema

    def __call__(self, request) -> requests.Request:
        request.headers["Authorization"] = f'{self.auth_scheme} {self.token_sessao}'
        return request

class CodexSessao(): #pylint: disable=too-few-public-methods
    '''
    Responsável por criar, armazenar e manter ativa a sessão de request com a
    plataforma Codex. Utiliza as informações obtidas pelo objeto config (classe
    Config) para se autenticar ao serviço Codex.
    '''
    
    def __init__(self, base_url : str, usuario : str, senha : str, duracao_token_minutos : str, caminho_token : str) -> None:
        self._token: BearerAuth = None
        
        self._base_url = base_url
        self._usuario = usuario
        self._senha = senha
        self._duracao_token_minutos = duracao_token_minutos
        
        self._caminho_token = caminho_token
        self._session = requests.Session()    
        self.token = self._load_token()
        if self._token is None:
            self._token = self._get_token()
        
        self._session.auth = self._token
        # Adiciona a função de validação de sessão como hook de response.
        self._session.hooks['response'].append(self._valida_sessao)


    def _load_token(self) -> str:
        try:
            with open(self._caminho_token, "r", encoding="utf_8") as f:
                token_str = f.read()
                
                if len(token_str) > 1:
                    logger.debug(f"Utilizando o token encontrado no arquivo {self._caminho_token}")
                    return BearerAuth(token_str)
        
                else:
                    logger.debug(f"Arquivo {self._caminho_token} em branco.")
                    
        except OSError:
            logger.debug("Não encontrou arquivo com token.")
        finally: 
            return None

    def _get_token(self) -> BearerAuth:
        ''' 
        Realiza a autenticação de usuário com as informações carregadas na 
        inicialização da objeto e retorna um token de autenticação. 
        '''
        
        form = {
            'login': self._usuario,
            'senha': self._senha,
            'duracaoTokenEmMinutos': self._duracao_token_minutos
        }

        resp = requests.post(f'{self._base_url}/usuario/autenticarUsuario', data=form, timeout=(5, 10))
        
        if resp.status_code != 200:
            raise ValueError({resp.text})
        try:
            with open(self._caminho_token, "w", encoding="utf_8") as f:
                f.write(resp.text)
        except OSError as e:
            logger.debug("Não foi possível escrever o token no arquivo token.json. %s", e)
        
        return BearerAuth(resp.text)

    def _valida_sessao(self, res: requests.Response, *args, **kwargs) -> requests.Response: # pylint: disable=unused-argument
        ''' 
        Hook para validar token de autenticação, deve ser adicionada ao response. 
        Verifica o código de estado e atualiza o token de autentica quando 
        necessário. Evita entrar em um loop infinito através do header REATTEMPT.
        '''
        
        if res.status_code == 401:
            if res.request.headers.get('REATTEMPT'):
                logger.error("Validação do Token falhou.")
                raise ValueError(res.text)
            logger.debug("Token expirado/invalido, revalidando a sessão.'")
            self._session.auth = self._get_token()
            req = res.request
            req.headers['REATTEMPT'] = 1
            req = self._session.auth(req)
            return self._session.send(req)
        if res.status_code != 200:
            raise ValueError(res.text)
        #raise ValueError("Nunca deve chegar neste ponto.")

    def get(self, url: str) -> requests.Response:
        ''' 
        Retorna as informações de endpoints do Codex. A URL 
        encontrada no arquivo de configuração irá preceder
        o endereço informado.
        '''
        return self._session.get(self._base_url + url)
    
    
    def post(self, url: str) -> requests.Response:
        ''' 
        Retorna as informações de endpoints do Codex. A URL 
        encontrada no arquivo de configuração irá preceder
        o endereço informado.
        '''
        return self._session.post(self._base_url + url)