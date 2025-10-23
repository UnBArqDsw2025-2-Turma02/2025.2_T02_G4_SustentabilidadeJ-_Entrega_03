from .token_strategy import (
    ReciclagemStrategy, TransporteStrategy,
    EconomiaRecursosStrategy, DescarteCorretoStrategy,
    PlantioArvoreStrategy
)

class TokenService:
    """Serviço de gerenciamento de tokens usando padrões Singleton e Strategy."""

    _instance = None

    def __new__(cls):
        """Implementa padrão Singleton."""
        if cls._instance is None:
            cls._instance = super(TokenService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Inicializa estratégias de cálculo de tokens."""
        if not hasattr(self, "estrategias"):
            self.estrategias = {
                "Reciclagem": ReciclagemStrategy(),
                "Transporte": TransporteStrategy(),
                "EconomiaRecursos": EconomiaRecursosStrategy(),
                "DescarteCorreto": DescarteCorretoStrategy(),
                "PlantioArvore": PlantioArvoreStrategy()
            }
            self.strategies = self.estrategias

    def registrar_tokens(self, usuario, acao):
        """Calcula e atribui tokens ao usuário baseado na ação."""
        estrategia = self.estrategias.get(acao.tipoAcao)

        if not estrategia:
            return 0

        tokens = estrategia.calcular_tokens(acao)
        usuario.saldoTokens += tokens

        return tokens

    def obter_estrategia(self, tipo_acao):
        """Retorna a estratégia de cálculo para um tipo de ação."""
        return self.estrategias.get(tipo_acao)

    def listar_tipos_disponiveis(self):
        """Lista tipos de ações disponíveis."""
        return list(self.estrategias.keys())
