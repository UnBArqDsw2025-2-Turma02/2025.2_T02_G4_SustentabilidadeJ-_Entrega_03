"""
Módulo de Serviços de Tokens

Este módulo implementa:
- Padrão Singleton (Criacional): TokenService
- Padrão Strategy (Comportamental): TokenStrategy e suas implementações

Classes disponíveis:
- TokenService: Serviço singleton para gerenciamento de tokens
- TokenStrategy: Interface para estratégias de cálculo de tokens
- ReciclagemStrategy, TransporteStrategy, EconomiaRecursosStrategy,
  DescarteCorretoStrategy, PlantioArvoreStrategy: Estratégias concretas
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
