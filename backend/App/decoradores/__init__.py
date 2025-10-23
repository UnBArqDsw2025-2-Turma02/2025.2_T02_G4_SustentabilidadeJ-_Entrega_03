"""
Módulo de Decoradores - Padrão GoF Estrutural: Decorator

Este módulo implementa o padrão Decorator para adicionar funcionalidades
dinamicamente ao registro de ações sustentáveis.

Decoradores disponíveis:
- AcaoDecorator: Classe base para todos os decoradores
- LogDecorator: Adiciona logging ao registro de ações
- BonusDecorator: Adiciona bônus de tokens para ações que geram 20+ tokens
"""

from .decorador_base import AcaoDecorator
from .decorador_log import LogDecorator
from .decorador_bonus import BonusDecorator

__all__ = ['AcaoDecorator', 'LogDecorator', 'BonusDecorator']
