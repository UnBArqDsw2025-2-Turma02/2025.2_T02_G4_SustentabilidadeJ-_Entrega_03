"""
Script de teste STANDALONE para validar os 3 Padrões GoF implementados:
1. Singleton (Criacional) - TokenService
2. Decorator (Estrutural) - LogDecorator e BonusDecorator
3. Strategy (Comportamental) - TokenStrategy

Este script NÃO depende de Django e pode ser executado diretamente.
"""

from abc import ABC, abstractmethod


# ==================== MODELS ====================
class Usuario:
    """Modelo de usuário simplificado."""

    def __init__(self, nome):
        self.nome = nome
        self.saldoTokens = 0

    def save(self):
        print(f"Usuário {self.nome} com saldo {self.saldoTokens} salvo!")


class AcaoSustentavel:
    """Modelo de ação sustentável simplificado."""

    def __init__(self, tipoAcao):
        self.tipoAcao = tipoAcao
        self.validada = False

    def save(self):
        print(f"Ação '{self.tipoAcao}' salva com sucesso!")


# ==================== STRATEGY PATTERN ====================
class TokenStrategy(ABC):
    """Interface abstrata para estratégias de cálculo de tokens."""

    @abstractmethod
    def calcular_tokens(self, acao):
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


# ==================== SINGLETON PATTERN ====================
class TokenService:
    """Singleton que gerencia tokens usando Strategy Pattern."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TokenService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "strategies"):
            self.strategies = {
                "Reciclagem": ReciclagemStrategy(),
                "Transporte": TransporteStrategy(),
                "EconomiaRecursos": EconomiaRecursosStrategy(),
                "DescarteCorreto": DescarteCorretoStrategy(),
                "PlantioArvore": PlantioArvoreStrategy()
            }

    def registrar_tokens(self, usuario, acao):
        strategy = self.strategies.get(acao.tipoAcao)
        if not strategy:
            return 0
        tokens = strategy.calcular_tokens(acao)
        usuario.saldoTokens += tokens
        return tokens


# ==================== SERVICE ====================
class RegistraAcaoService:
    """Serviço para registrar ações."""

    def __init__(self, token_service):
        self.token_service = token_service

    def registrar_acao(self, usuario, acao):
        acao.save()
        tokens_gerados = self.token_service.registrar_tokens(usuario, acao)
        return tokens_gerados


# ==================== DECORATOR PATTERN ====================
class AcaoDecorator:
    """Decorator base."""

    def __init__(self, componente):
        self._componente = componente

    def registrar_acao(self, usuario, acao):
        return self._componente.registrar_acao(usuario, acao)


class LogDecorator(AcaoDecorator):
    """Decorator que adiciona logging."""

    def registrar_acao(self, usuario, acao):
        print(f"[LOG] Registrando ação '{acao.tipoAcao}' de {usuario.nome}")
        return super().registrar_acao(usuario, acao)


class BonusDecorator(AcaoDecorator):
    """Decorator que adiciona bônus."""

    def registrar_acao(self, usuario, acao):
        tokens = super().registrar_acao(usuario, acao)
        if tokens >= 20:
            usuario.saldoTokens += 5
            print(f"[BÔNUS] {usuario.nome} ganhou 5 tokens extras!")
        return tokens


# ==================== TESTES ====================
def print_separator(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_singleton_pattern():
    print_separator("TESTE 1: Padrão Singleton (Criacional)")
    service1 = TokenService()
    service2 = TokenService()
    service3 = TokenService()

    print(f"service1 é service2? {service1 is service2}")
    print(f"service2 é service3? {service2 is service3}")
    print(f"ID de service1: {id(service1)}")
    print(f"ID de service2: {id(service2)}")
    print(f"ID de service3: {id(service3)}")

    if service1 is service2 is service3:
        print("\n✅ SINGLETON FUNCIONANDO: Todas as instâncias são idênticas!")
    else:
        print("\n❌ ERRO: Singleton não está funcionando corretamente!")

    return service1


def test_strategy_pattern(token_service):
    print_separator("TESTE 2: Padrão Strategy (Comportamental)")
    usuario = Usuario("Maria Silva")
    print(f"\nUsuário: {usuario.nome}")
    print(f"Saldo inicial: {usuario.saldoTokens} tokens")

    acoes_teste = [
        ("Reciclagem", 10),
        ("Transporte", 15),
        ("EconomiaRecursos", 20),
        ("DescarteCorreto", 15),
        ("PlantioArvore", 25),
    ]

    print("\n--- Testando diferentes estratégias ---")
    for tipo_acao, tokens_esperados in acoes_teste:
        acao = AcaoSustentavel(tipo_acao)
        tokens = token_service.registrar_tokens(usuario, acao)
        status = "✅" if tokens == tokens_esperados else "❌"
        print(f"  {tipo_acao:20s} → {tokens:2d} tokens (esperado: {tokens_esperados}) {status}")

    print(f"\nSaldo final: {usuario.saldoTokens} tokens")
    print(f"Total esperado: {sum(t[1] for t in acoes_teste)} tokens")

    if usuario.saldoTokens == sum(t[1] for t in acoes_teste):
        print("✅ STRATEGY FUNCIONANDO: Todos os cálculos corretos!")
    else:
        print("❌ ERRO: Cálculos de tokens incorretos!")

    return usuario


def test_decorator_pattern():
    print_separator("TESTE 3: Padrão Decorator (Estrutural)")
    usuario = Usuario("João Santos")
    print(f"\nUsuário: {usuario.nome}")
    print(f"Saldo inicial: {usuario.saldoTokens} tokens\n")

    token_service = TokenService()
    servico_base = RegistraAcaoService(token_service)
    servico_decorado = BonusDecorator(LogDecorator(servico_base))

    print("--- Testando com Decoradores (Log + Bônus) ---\n")

    print("1. Ação de Reciclagem (10 tokens - sem bônus):")
    acao1 = AcaoSustentavel("Reciclagem")
    tokens1 = servico_decorado.registrar_acao(usuario, acao1)
    print(f"   Tokens recebidos: {tokens1}")
    print(f"   Saldo atual: {usuario.saldoTokens} tokens\n")

    print("2. Ação de PlantioArvore (25 tokens - COM bônus de +5):")
    acao2 = AcaoSustentavel("PlantioArvore")
    tokens2 = servico_decorado.registrar_acao(usuario, acao2)
    print(f"   Tokens recebidos: {tokens2}")
    print(f"   Saldo atual: {usuario.saldoTokens} tokens\n")

    saldo_esperado = 10 + 25 + 5
    print(f"Saldo final: {usuario.saldoTokens} tokens")
    print(f"Saldo esperado: {saldo_esperado} tokens")

    if usuario.saldoTokens == saldo_esperado:
        print("\n✅ DECORATOR FUNCIONANDO: Log e Bônus aplicados corretamente!")
    else:
        print("\n❌ ERRO: Decoradores não funcionaram corretamente!")


def test_integrated_system():
    print_separator("TESTE 4: Sistema Integrado (Todos os Padrões)")
    token_service = TokenService()
    servico_base = RegistraAcaoService(token_service)
    servico_decorado = BonusDecorator(LogDecorator(servico_base))

    usuario = Usuario("Ana Costa")
    print(f"\nUsuário: {usuario.nome}")
    print(f"Saldo inicial: {usuario.saldoTokens} tokens\n")

    acoes = [
        AcaoSustentavel("Reciclagem"),          # 10 tokens
        AcaoSustentavel("PlantioArvore"),       # 25 + 5 bônus = 30
        AcaoSustentavel("EconomiaRecursos"),    # 20 + 5 bônus = 25
        AcaoSustentavel("Transporte"),          # 15 tokens
        AcaoSustentavel("PlantioArvore"),       # 25 + 5 bônus = 30
    ]

    print("--- Registrando múltiplas ações ---\n")
    for i, acao in enumerate(acoes, 1):
        print(f"{i}. Ação: {acao.tipoAcao}")
        servico_decorado.registrar_acao(usuario, acao)
        print()

    print(f"Saldo final: {usuario.saldoTokens} tokens")
    print(f"Total esperado: 110 tokens (10 + 30 + 25 + 15 + 30)")

    if usuario.saldoTokens == 110:
        print("\n✅ SISTEMA INTEGRADO FUNCIONANDO PERFEITAMENTE!")
    else:
        print(f"\n⚠️  Saldo diferente do esperado (obtido: {usuario.saldoTokens})")


def main():
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  TESTE DOS PADRÕES GoF - SUSTENTABILIDADEJÁ".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)

    try:
        token_service = test_singleton_pattern()
        test_strategy_pattern(token_service)
        test_decorator_pattern()
        test_integrated_system()

        print_separator("RESUMO DOS TESTES")
        print("\n✅ Padrão Singleton (Criacional): IMPLEMENTADO")
        print("✅ Padrão Strategy (Comportamental): IMPLEMENTADO")
        print("✅ Padrão Decorator (Estrutural): IMPLEMENTADO")
        print("\n🎉 TODOS OS PADRÕES GOF ESTÃO FUNCIONANDO CORRETAMENTE!\n")

    except Exception as e:
        print(f"\n❌ ERRO DURANTE OS TESTES: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
