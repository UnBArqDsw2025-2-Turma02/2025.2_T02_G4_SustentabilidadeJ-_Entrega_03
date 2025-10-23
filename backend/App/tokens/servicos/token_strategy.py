# strategies.py
from abc import ABC, abstractmethod

class TokenStrategy(ABC):
    @abstractmethod
    def calcular_tokens(self, acao):
        #retorna a quantidade de tokens para a ação
        pass

class ReciclagemStrategy(TokenStrategy):
    def calcular_tokens(self, acao):
        return 10

class TransporteStrategy(TokenStrategy):
    def calcular_tokens(self, acao):
        return 15

class EconomiaRecursosStrategy(TokenStrategy):
    def calcular_tokens(self, acao):
        return 20

class DescarteCorretoStrategy(TokenStrategy):
    def calcular_tokens(self, acao):
        return 15

class PlantioArvoreStrategy(TokenStrategy):
    def calcular_tokens(self, acao):
        return 25
