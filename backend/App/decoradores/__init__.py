"""
M�dulo de Decoradores - Padr�o GoF Estrutural: Decorator

Este m�dulo implementa o padr�o Decorator para adicionar funcionalidades
dinamicamente ao registro de a��es sustent�veis.

Decoradores dispon�veis:
- AcaoDecorator: Classe base para todos os decoradores
- LogDecorator: Adiciona logging ao registro de a��es
- BonusDecorator: Adiciona b�nus de tokens para a��es que geram 20+ tokens
"""

from .decorador_base import AcaoDecorator
from .decorador_log import LogDecorator
from .decorador_bonus import BonusDecorator

__all__ = ['AcaoDecorator', 'LogDecorator', 'BonusDecorator']
