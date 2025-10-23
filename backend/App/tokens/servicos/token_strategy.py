from abc import ABC, abstractmethod


class TokenStrategy(ABC):
    """Classe base para estratégias de cálculo de tokens."""

    @abstractmethod
    def calcular_tokens(self, acao):
        """Calcula tokens para a ação."""
        pass


class ReciclagemStrategy(TokenStrategy):
    """Estratégia para ações de reciclagem."""

    def calcular_tokens(self, acao):
        return 10


class TransporteStrategy(TokenStrategy):
    """Estratégia para transporte sustentável."""

    def calcular_tokens(self, acao):
        return 15


class EconomiaRecursosStrategy(TokenStrategy):
    """Estratégia para economia de recursos."""

    def calcular_tokens(self, acao):
        return 20


class DescarteCorretoStrategy(TokenStrategy):
    """Estratégia para descarte correto."""

    def calcular_tokens(self, acao):
        return 15


class PlantioArvoreStrategy(TokenStrategy):
    """Estratégia para plantio de árvores."""

    def calcular_tokens(self, acao):
        return 25
