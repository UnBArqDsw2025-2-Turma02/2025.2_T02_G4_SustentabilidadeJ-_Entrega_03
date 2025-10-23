"""Testes dos padroes GoF - Singleton, Strategy e Decorator."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'App'))

from authentication.models import Usuario
from actions.models import AcaoSustentavel
from tokens.servicos.token_servico import TokenService
from actions.servicos.registrar_acao import RegistraAcaoService
from decoradores.decorador_log import LogDecorator
from decoradores.decorador_bonus import BonusDecorator


def imprimir_separador(titulo):
    """Imprime separador visual."""
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70)


def print_separator(title):
    """Compatibilidade."""
    imprimir_separador(title)


def testar_padrao_singleton():
    """Testa padrao Singleton."""
    imprimir_separador("TESTE 1: Padrao Singleton")

    print("\nCriando 3 instancias do TokenService...")

    servico1 = TokenService()
    servico2 = TokenService()
    servico3 = TokenService()

    print("\nVerificando se sao a mesma instancia:")
    print(f"   servico1 is servico2? {servico1 is servico2}")
    print(f"   servico2 is servico3? {servico2 is servico3}")
    print(f"\nIDs de memoria:")
    print(f"   ID servico1: {id(servico1)}")
    print(f"   ID servico2: {id(servico2)}")
    print(f"   ID servico3: {id(servico3)}")

    if servico1 is servico2 is servico3:
        print("\nSingleton OK - Mesma instancia")
    else:
        print("\nERRO - Instancias diferentes")

    return servico1


def test_singleton_pattern():
    """Compatibilidade."""
    return testar_padrao_singleton()


def testar_padrao_strategy(servico_tokens):
    """Testa padrao Strategy."""
    imprimir_separador("TESTE 2: Padrao Strategy")

    usuario = Usuario("Maria Silva")
    print(f"\nUsuario: {usuario.nome}")
    print(f"Saldo inicial: {usuario.saldoTokens} tokens")

    acoes_para_testar = [
        ("Reciclagem", 10),
        ("Transporte", 15),
        ("EconomiaRecursos", 20),
        ("DescarteCorreto", 15),
        ("PlantioArvore", 25),
    ]

    print("\nTestando estrategias:")
    print("-" * 70)

    for tipo_acao, tokens_esperados in acoes_para_testar:
        acao = AcaoSustentavel(tipo_acao)
        tokens_recebidos = servico_tokens.registrar_tokens(usuario, acao)

        print(f"  {tipo_acao:20s} -> {tokens_recebidos:2d} tokens (esperado: {tokens_esperados})")

        if tokens_recebidos == tokens_esperados:
            print(f"    OK - Estrategia {tipo_acao} correta")
        else:
            print(f"    ERRO - Estrategia {tipo_acao} incorreta")

    total_esperado = sum(t[1] for t in acoes_para_testar)
    print(f"\nSaldo final: {usuario.saldoTokens} tokens")
    print(f"Total esperado: {total_esperado} tokens")

    if usuario.saldoTokens == total_esperado:
        print("\nStrategy OK - Calculos corretos")
    else:
        print(f"\nERRO - Esperado {total_esperado}, obteve {usuario.saldoTokens}")

    return usuario


def test_strategy_pattern(token_service):
    """Compatibilidade."""
    return testar_padrao_strategy(token_service)


def testar_padrao_decorator():
    """Testa padrao Decorator."""
    imprimir_separador("TESTE 3: Padrao Decorator")

    usuario = Usuario("Joao Santos")
    print(f"\nUsuario: {usuario.nome}")
    print(f"Saldo inicial: {usuario.saldoTokens} tokens\n")

    servico_tokens = TokenService()
    servico_base = RegistraAcaoService(servico_tokens)

    print("Montando cadeia de decoradores:")
    print("   Base -> LogDecorator -> BonusDecorator\n")

    servico_decorado = BonusDecorator(LogDecorator(servico_base))

    print("Testando decoradores:")
    print("-" * 70)

    print("\nTESTE 1: Reciclagem (10 tokens - sem bonus)")
    acao1 = AcaoSustentavel("Reciclagem")
    tokens1 = servico_decorado.registrar_acao(usuario, acao1)
    print(f"   Tokens: {tokens1}")
    print(f"   Saldo: {usuario.saldoTokens} tokens")

    print("\nTESTE 2: PlantioArvore (25 tokens - com bonus)")
    acao2 = AcaoSustentavel("PlantioArvore")
    tokens2 = servico_decorado.registrar_acao(usuario, acao2)
    print(f"   Tokens: {tokens2}")
    print(f"   Saldo: {usuario.saldoTokens} tokens")

    saldo_esperado = 10 + 25 + 5
    print(f"\nResumo:")
    print(f"   Saldo final: {usuario.saldoTokens} tokens")
    print(f"   Saldo esperado: {saldo_esperado} tokens")

    if usuario.saldoTokens == saldo_esperado:
        print("\nDecorator OK - Log e bonus funcionando")
    else:
        print(f"\nERRO - Esperado {saldo_esperado}, obteve {usuario.saldoTokens}")


def test_decorator_pattern():
    """Compatibilidade."""
    testar_padrao_decorator()


def testar_sistema_integrado():
    """Testa sistema completo."""
    imprimir_separador("TESTE 4: Sistema Integrado")

    print("\nPreparando sistema...\n")

    servico_tokens = TokenService()
    print("OK - Singleton: TokenService instanciado")

    servico_base = RegistraAcaoService(servico_tokens)
    servico_completo = BonusDecorator(LogDecorator(servico_base))
    print("OK - Decorator: Cadeia montada")

    print("OK - Strategy: 5 estrategias prontas")

    usuario = Usuario("Ana Costa")
    print(f"\nUsuario: {usuario.nome}")
    print(f"Saldo inicial: {usuario.saldoTokens} tokens\n")

    acoes_do_dia = [
        ("Reciclagem", AcaoSustentavel("Reciclagem"), 10, 0),
        ("PlantioArvore", AcaoSustentavel("PlantioArvore"), 25, 5),
        ("EconomiaRecursos", AcaoSustentavel("EconomiaRecursos"), 20, 5),
        ("Transporte", AcaoSustentavel("Transporte"), 15, 0),
        ("PlantioArvore", AcaoSustentavel("PlantioArvore"), 25, 5),
    ]

    print("Simulando acoes:")
    print("=" * 70)

    for i, (nome, acao, tokens_base, bonus) in enumerate(acoes_do_dia, 1):
        print(f"\n{i}. {nome}")
        servico_completo.registrar_acao(usuario, acao)
        esperado = tokens_base + bonus
        print(f"   Tokens: {tokens_base} + {bonus} bonus = {esperado} tokens")

    total_esperado = sum(tokens + bonus for _, _, tokens, bonus in acoes_do_dia)
    print("\n" + "=" * 70)
    print(f"\nResultado:")
    print(f"   Saldo atual: {usuario.saldoTokens} tokens")
    print(f"   Saldo esperado: {total_esperado} tokens")

    if usuario.saldoTokens == total_esperado:
        print("\nSistema integrado OK - Todos os padroes funcionando")
    else:
        print(f"\nERRO - Esperado {total_esperado}, obteve {usuario.saldoTokens}")


def test_integrated_system():
    """Compatibilidade."""
    testar_sistema_integrado()


def principal():
    """Funcao principal - executa todos os testes."""
    print("\n" + "=" * 70)
    print("  TESTES DOS PADROES GoF - SUSTENTABILIDADEJA")
    print("=" * 70)

    try:
        print("\nIniciando testes...\n")

        servico_tokens = testar_padrao_singleton()
        testar_padrao_strategy(servico_tokens)
        testar_padrao_decorator()
        testar_sistema_integrado()

        imprimir_separador("RESUMO")
        print("\nPadroes testados:\n")
        print("   OK - Padrao Singleton")
        print("   OK - Padrao Strategy")
        print("   OK - Padrao Decorator\n")
        print("=" * 70 + "\n")

    except Exception as erro:
        print(f"\nERRO: {str(erro)}\n")
        import traceback
        traceback.print_exc()
        print("\n" + "=" * 70 + "\n")


def main():
    """Compatibilidade."""
    principal()


if __name__ == "__main__":
    principal()
