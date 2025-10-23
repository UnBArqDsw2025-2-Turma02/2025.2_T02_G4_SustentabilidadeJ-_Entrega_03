"""Testes standalone dos padroes GoF."""

from abc import ABC, abstractmethod


class Usuario:
    """Modelo de usuario."""

    def __init__(self, nome):
        self.nome = nome
        self.saldoTokens = 0

    def save(self):
        print(f"Usuario {self.nome} com saldo {self.saldoTokens} salvo")


class AcaoSustentavel:
    """Modelo de acao sustentavel."""

    def __init__(self, tipoAcao):
        self.tipoAcao = tipoAcao
        self.validada = False

    def save(self):
        print(f"Acao '{self.tipoAcao}' salva")


class TokenStrategy(ABC):
    """Interface para estrategias de calculo de tokens."""

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


class TokenService:
    """Singleton que gerencia tokens usando Strategy."""
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


class RegistraAcaoService:
    """Servico para registrar acoes."""

    def __init__(self, token_service):
        self.token_service = token_service

    def registrar_acao(self, usuario, acao):
        acao.save()
        tokens_gerados = self.token_service.registrar_tokens(usuario, acao)
        return tokens_gerados


class AcaoDecorator:
    """Decorator base."""

    def __init__(self, componente):
        self._componente = componente

    def registrar_acao(self, usuario, acao):
        return self._componente.registrar_acao(usuario, acao)


class LogDecorator(AcaoDecorator):
    """Decorator de logging."""

    def registrar_acao(self, usuario, acao):
        print(f"[LOG] Registrando acao '{acao.tipoAcao}' de {usuario.nome}")
        return super().registrar_acao(usuario, acao)


class BonusDecorator(AcaoDecorator):
    """Decorator de bonus."""

    def registrar_acao(self, usuario, acao):
        tokens = super().registrar_acao(usuario, acao)
        if tokens >= 20:
            usuario.saldoTokens += 5
            print(f"[BONUS] {usuario.nome} ganhou 5 tokens extras")
        return tokens


def print_separator(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_singleton_pattern():
    print_separator("TESTE 1: Padrao Singleton")
    service1 = TokenService()
    service2 = TokenService()
    service3 = TokenService()

    print(f"service1 is service2? {service1 is service2}")
    print(f"service2 is service3? {service2 is service3}")
    print(f"ID service1: {id(service1)}")
    print(f"ID service2: {id(service2)}")
    print(f"ID service3: {id(service3)}")

    if service1 is service2 is service3:
        print("\nSingleton OK - Instancias identicas")
    else:
        print("\nERRO - Singleton nao funcionando")

    return service1


def test_strategy_pattern(token_service):
    print_separator("TESTE 2: Padrao Strategy")
    usuario = Usuario("Maria Silva")
    print(f"\nUsuario: {usuario.nome}")
    print(f"Saldo inicial: {usuario.saldoTokens} tokens")

    acoes_teste = [
        ("Reciclagem", 10),
        ("Transporte", 15),
        ("EconomiaRecursos", 20),
        ("DescarteCorreto", 15),
        ("PlantioArvore", 25),
    ]

    print("\nTestando estrategias:")
    for tipo_acao, tokens_esperados in acoes_teste:
        acao = AcaoSustentavel(tipo_acao)
        tokens = token_service.registrar_tokens(usuario, acao)
        status = "OK" if tokens == tokens_esperados else "ERRO"
        print(f"  {tipo_acao:20s} -> {tokens:2d} tokens (esperado: {tokens_esperados}) {status}")

    print(f"\nSaldo final: {usuario.saldoTokens} tokens")
    print(f"Total esperado: {sum(t[1] for t in acoes_teste)} tokens")

    if usuario.saldoTokens == sum(t[1] for t in acoes_teste):
        print("Strategy OK - Calculos corretos")
    else:
        print("ERRO - Calculos incorretos")

    return usuario


def test_decorator_pattern():
    print_separator("TESTE 3: Padrao Decorator")
    usuario = Usuario("Joao Santos")
    print(f"\nUsuario: {usuario.nome}")
    print(f"Saldo inicial: {usuario.saldoTokens} tokens\n")

    token_service = TokenService()
    servico_base = RegistraAcaoService(token_service)
    servico_decorado = BonusDecorator(LogDecorator(servico_base))

    print("Testando decoradores:\n")

    print("1. Reciclagem (10 tokens - sem bonus):")
    acao1 = AcaoSustentavel("Reciclagem")
    tokens1 = servico_decorado.registrar_acao(usuario, acao1)
    print(f"   Tokens: {tokens1}")
    print(f"   Saldo: {usuario.saldoTokens} tokens\n")

    print("2. PlantioArvore (25 tokens - com bonus +5):")
    acao2 = AcaoSustentavel("PlantioArvore")
    tokens2 = servico_decorado.registrar_acao(usuario, acao2)
    print(f"   Tokens: {tokens2}")
    print(f"   Saldo: {usuario.saldoTokens} tokens\n")

    saldo_esperado = 10 + 25 + 5
    print(f"Saldo final: {usuario.saldoTokens} tokens")
    print(f"Saldo esperado: {saldo_esperado} tokens")

    if usuario.saldoTokens == saldo_esperado:
        print("\nDecorator OK - Log e bonus aplicados")
    else:
        print("\nERRO - Decoradores nao funcionaram")


def test_integrated_system():
    print_separator("TESTE 4: Sistema Integrado")
    token_service = TokenService()
    servico_base = RegistraAcaoService(token_service)
    servico_decorado = BonusDecorator(LogDecorator(servico_base))

    usuario = Usuario("Ana Costa")
    print(f"\nUsuario: {usuario.nome}")
    print(f"Saldo inicial: {usuario.saldoTokens} tokens\n")

    acoes = [
        AcaoSustentavel("Reciclagem"),
        AcaoSustentavel("PlantioArvore"),
        AcaoSustentavel("EconomiaRecursos"),
        AcaoSustentavel("Transporte"),
        AcaoSustentavel("PlantioArvore"),
    ]

    print("Registrando acoes:\n")
    for i, acao in enumerate(acoes, 1):
        print(f"{i}. Acao: {acao.tipoAcao}")
        servico_decorado.registrar_acao(usuario, acao)
        print()

    print(f"Saldo final: {usuario.saldoTokens} tokens")
    print(f"Total esperado: 110 tokens")

    if usuario.saldoTokens == 110:
        print("\nSistema integrado OK")
    else:
        print(f"\nERRO - Saldo incorreto: {usuario.saldoTokens}")


def main():
    print("\n" + "=" * 70)
    print("  TESTES DOS PADROES GoF")
    print("=" * 70)

    try:
        token_service = test_singleton_pattern()
        test_strategy_pattern(token_service)
        test_decorator_pattern()
        test_integrated_system()

        print_separator("RESUMO")
        print("\nOK - Padrao Singleton")
        print("OK - Padrao Strategy")
        print("OK - Padrao Decorator\n")

    except Exception as e:
        print(f"\nERRO: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
