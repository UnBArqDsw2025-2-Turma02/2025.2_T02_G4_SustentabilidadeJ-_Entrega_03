from ...tokens.servicos.token_servico import TokenService


class RegistraAcaoService:
    """Serviço para registrar ações sustentáveis e atribuir tokens."""

    def __init__(self, servico_tokens: TokenService):
        """Inicializa o serviço com TokenService."""
        self.servico_tokens = servico_tokens
        self.token_service = servico_tokens

    def registrar_acao(self, usuario, acao):
        """Registra ação e atribui tokens ao usuário."""
        acao.save()
        tokens_dados = self.servico_tokens.registrar_tokens(usuario, acao)
        return tokens_dados
