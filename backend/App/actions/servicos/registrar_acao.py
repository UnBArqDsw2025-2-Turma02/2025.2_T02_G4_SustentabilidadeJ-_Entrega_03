from ...tokens.servicos.token_servico import TokenService


class RegistraAcaoService:
    """
    Serviço para Registrar Ações Sustentáveis.

    Este serviço é responsável por:
    1. Salvar a ação no banco de dados
    2. Calcular e dar tokens ao usuário
    3. Retornar quantos tokens foram dados

    É o ponto central onde tudo acontece quando alguém faz uma ação sustentável!
    """

    def __init__(self, servico_tokens: TokenService):
        """
        Inicializa o serviço de registro de ações.

        Parâmetros:
            servico_tokens: O serviço de tokens que vai calcular as recompensas
        """
        self.servico_tokens = servico_tokens
        # Mantém compatibilidade com código antigo
        self.token_service = servico_tokens

    def registrar_acao(self, usuario, acao):
        """
        Registra uma nova ação sustentável e dá tokens ao usuário.

        Fluxo de execução:
        1. Salva a ação no banco de dados para manter histórico
        2. Usa o TokenService para calcular e dar os tokens
        3. Retorna quantos tokens foram dados

        Parâmetros:
            usuario: A pessoa que fez a ação
            acao: A ação sustentável realizada

        Retorna:
            Quantidade de tokens que o usuário ganhou

        Exemplo:
            >>> servico = RegistraAcaoService(TokenService())
            >>> acao = AcaoSustentavel("Reciclagem")
            >>> tokens = servico.registrar_acao(maria, acao)
            >>> print(f"Parabéns! Você ganhou {tokens} tokens!")
        """
        # Salva a ação no banco de dados
        acao.save()

        # Calcula e dá os tokens usando o padrão Strategy
        tokens_dados = self.servico_tokens.registrar_tokens(usuario, acao)

        return tokens_dados
