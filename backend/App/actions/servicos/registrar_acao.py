
from tokens.servicos.token_service import TokenService
class RegistraAcaoService:
    def __init__(self, token_service: TokenService):
        self.token_service = token_service

    def registrar_acao(self, usuario, acao):
        #salva a ação no DB
        acao.save() 
        #gera tokens usando Strategy
        tokens_gerados = self.token_service.registrar_tokens(usuario, acao)
        return tokens_gerados
