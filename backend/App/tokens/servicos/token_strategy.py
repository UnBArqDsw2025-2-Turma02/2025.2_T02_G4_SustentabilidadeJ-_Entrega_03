# Padrão de Projeto Comportamental: Strategy (Estratégia)
#
# Este padrão define uma família de algoritmos que podem ser trocados entre si.
# Cada estratégia calcula tokens de forma diferente, mas todas seguem a mesma interface.
# Isso permite adicionar novos tipos de ações sem modificar o código existente.

from abc import ABC, abstractmethod


class TokenStrategy(ABC):
    """
    Classe base para todas as estratégias de cálculo de tokens.

    Cada tipo de ação sustentável tem sua própria estratégia que determina
    quantos tokens serão dados ao usuário. Por exemplo:
    - Reciclagem dá 10 tokens
    - Plantio de árvore dá 25 tokens

    Para criar uma nova estratégia, basta herdar desta classe e implementar
    o método calcular_tokens().
    """

    @abstractmethod
    def calcular_tokens(self, acao):
        """
        Calcula quantos tokens o usuário deve ganhar por esta ação.

        Parâmetros:
            acao: A ação sustentável que foi realizada pelo usuário

        Retorna:
            Quantidade de tokens (número inteiro)
        """
        pass


class ReciclagemStrategy(TokenStrategy):
    """
    Estratégia de cálculo para ações de reciclagem.

    Quando alguém recicla (papel, plástico, vidro, etc.), ganha 10 tokens.
    É uma ação básica mas muito importante para o meio ambiente!
    """

    def calcular_tokens(self, acao):
        """Reciclou algo? Ganhe 10 tokens!"""
        return 10


class TransporteStrategy(TokenStrategy):
    """
    Estratégia de cálculo para transporte sustentável.

    Usou bicicleta, transporte público ou carona? Você merece 15 tokens!
    Menos carros nas ruas = menos poluição + mais saúde.
    """

    def calcular_tokens(self, acao):
        """Foi de bike ou ônibus? Ganhe 15 tokens!"""
        return 15


class EconomiaRecursosStrategy(TokenStrategy):
    """
    Estratégia de cálculo para economia de recursos.

    Economizou água ou energia? Isso vale 20 tokens!
    Recursos naturais são preciosos e você está ajudando a preservá-los.
    """

    def calcular_tokens(self, acao):
        """Economizou água ou luz? Ganhe 20 tokens!"""
        return 20


class DescarteCorretoStrategy(TokenStrategy):
    """
    Estratégia de cálculo para descarte correto de resíduos.

    Descartou pilhas, eletrônicos ou óleo no lugar certo? Parabéns, 15 tokens!
    Isso evita contaminação do solo e da água.
    """

    def calcular_tokens(self, acao):
        """Descartou corretamente? Ganhe 15 tokens!"""
        return 15


class PlantioArvoreStrategy(TokenStrategy):
    """
    Estratégia de cálculo para plantio de árvores.

    Plantou uma árvore? WOW! Isso vale 25 tokens - a maior recompensa!
    Árvores purificam o ar, fornecem sombra e são lar para animais.
    Cada árvore plantada faz uma diferença enorme para o planeta.
    """

    def calcular_tokens(self, acao):
        """Plantou uma árvore? Você é incrível! Ganhe 25 tokens!"""
        return 25
