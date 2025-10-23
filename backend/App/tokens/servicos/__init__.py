"""
M�dulo de Servi�os de Tokens

Este m�dulo implementa:
- Padr�o Singleton (Criacional): TokenService
- Padr�o Strategy (Comportamental): TokenStrategy e suas implementa��es

Classes dispon�veis:
- TokenService: Servi�o singleton para gerenciamento de tokens
- TokenStrategy: Interface para estrat�gias de c�lculo de tokens
- ReciclagemStrategy, TransporteStrategy, EconomiaRecursosStrategy,
  DescarteCorretoStrategy, PlantioArvoreStrategy: Estrat�gias concretas
"""

from .token_servico import TokenService
from .token_strategy import (
    TokenStrategy,
    ReciclagemStrategy,
    TransporteStrategy,
    EconomiaRecursosStrategy,
    DescarteCorretoStrategy,
    PlantioArvoreStrategy
)

__all__ = [
    'TokenService',
    'TokenStrategy',
    'ReciclagemStrategy',
    'TransporteStrategy',
    'EconomiaRecursosStrategy',
    'DescarteCorretoStrategy',
    'PlantioArvoreStrategy'
]
