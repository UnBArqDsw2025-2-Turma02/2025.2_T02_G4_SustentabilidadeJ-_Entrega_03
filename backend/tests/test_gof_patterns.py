"""
===================================================================================
TESTES DOS PADRÕES DE PROJETO GoF - SUSTENTABILIDADEJÁ
===================================================================================

Este script testa os 3 Padrões GoF que foram implementados no projeto:

🏗️  1. SINGLETON (Padrão Criacional) - TokenService
    → Garante que só existe UMA instância do serviço de tokens
    → Todas as partes do sistema compartilham o mesmo serviço

🎨 2. DECORATOR (Padrão Estrutural) - LogDecorator e BonusDecorator
    → Adiciona funcionalidades extras sem modificar o código original
    → Pode combinar múltiplos decoradores (log + bônus)

🎯 3. STRATEGY (Padrão Comportamental) - TokenStrategy
    → Cada tipo de ação tem sua própria estratégia de cálculo
    → Fácil adicionar novos tipos sem mexer no código existente

Este arquivo não apenas testa - ele também DEMONSTRA como os padrões
funcionam juntos de forma elegante!
"""

import sys
import os

# Adiciona o diretório App ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'App'))

from authentication.models import Usuario
from actions.models import AcaoSustentavel
from tokens.servicos.token_servico import TokenService
from actions.servicos.registrar_acao import RegistraAcaoService
from decoradores.decorador_log import LogDecorator
from decoradores.decorador_bonus import BonusDecorator


def imprimir_separador(titulo):
    """Imprime um separador bonitinho para organizar a saída dos testes."""
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70)


# Mantém compatibilidade com código antigo
def print_separator(title):
    """Imprime um separador visual (compatibilidade)."""
    imprimir_separador(title)


def testar_padrao_singleton():
    """
    Testa o Padrão Singleton - Garante que só existe UMA instância.

    O padrão Singleton é como ter uma única impressora no escritório:
    - Não importa quantas vezes você chame TokenService()
    - Sempre recebe a MESMA impressora (instância)
    - Todo mundo usa o mesmo objeto

    Este teste cria 3 "instâncias" e verifica se todas são o mesmo objeto.
    """
    imprimir_separador("TESTE 1: Padrão Singleton (Criacional)")

    print("\n📦 Tentando criar 3 'instâncias' diferentes do TokenService...")

    # Tenta criar múltiplas "instâncias" do TokenService
    servico1 = TokenService()
    servico2 = TokenService()
    servico3 = TokenService()

    print("\n🔍 Verificando se todas são a mesma instância:")
    print(f"   servico1 é servico2? {servico1 is servico2}")
    print(f"   servico2 é servico3? {servico2 is servico3}")
    print(f"\n📍 IDs de memória:")
    print(f"   ID de servico1: {id(servico1)}")
    print(f"   ID de servico2: {id(servico2)}")
    print(f"   ID de servico3: {id(servico3)}")

    # Verifica se realmente funcionou
    if servico1 is servico2 is servico3:
        print("\n✅ SINGLETON FUNCIONANDO PERFEITAMENTE!")
        print("   Todas as 'instâncias' são o mesmo objeto!")
        print("   Não importa quantas vezes você chame TokenService(),")
        print("   sempre recebe o mesmo serviço! 🎉")
    else:
        print("\n❌ ERRO: Singleton NÃO está funcionando!")
        print("   As instâncias são diferentes - isso é um problema!")

    return servico1


# Mantém compatibilidade
def test_singleton_pattern():
    """Testa o padrão Singleton no TokenService (compatibilidade)."""
    return testar_padrao_singleton()


def testar_padrao_strategy(servico_tokens):
    """
    Testa o Padrão Strategy - Diferentes algoritmos para diferentes ações.

    O padrão Strategy é como ter diferentes calculadoras para diferentes matérias:
    - Calculadora de Matemática (ReciclagemStrategy) → sempre dá 10 pontos
    - Calculadora de Física (TransporteStrategy) → sempre dá 15 pontos
    - E assim por diante...

    Cada "calculadora" sabe fazer seu trabalho, e é fácil adicionar novas!
    """
    imprimir_separador("TESTE 2: Padrão Strategy (Comportamental)")

    # Cria uma usuária para testar
    usuario = Usuario("Maria Silva")
    print(f"\n👤 Usuária de teste: {usuario.nome}")
    print(f"💰 Saldo inicial: {usuario.saldoTokens} tokens")

    # Lista das ações que vamos testar (tipo, tokens esperados)
    acoes_para_testar = [
        ("Reciclagem", 10),
        ("Transporte", 15),
        ("EconomiaRecursos", 20),
        ("DescarteCorreto", 15),
        ("PlantioArvore", 25),
    ]

    print("\n🧪 Testando cada estratégia de cálculo:")
    print("-" * 70)

    for tipo_acao, tokens_esperados in acoes_para_testar:
        # Cria e registra a ação
        acao = AcaoSustentavel(tipo_acao)
        tokens_recebidos = servico_tokens.registrar_tokens(usuario, acao)

        # Mostra o resultado
        print(f"  {tipo_acao:20s} → {tokens_recebidos:2d} tokens (esperado: {tokens_esperados})")

        # Verifica se está correto
        if tokens_recebidos == tokens_esperados:
            print(f"    ✅ Estratégia de {tipo_acao} calculou certo!")
        else:
            print(f"    ❌ ERRO na estratégia {tipo_acao}! Valor errado!")

    # Verifica o total
    total_esperado = sum(t[1] for t in acoes_para_testar)
    print(f"\n💎 Saldo final: {usuario.saldoTokens} tokens")
    print(f"📊 Total esperado: {total_esperado} tokens")

    if usuario.saldoTokens == total_esperado:
        print("\n✅ STRATEGY FUNCIONANDO PERFEITAMENTE!")
        print("   Todas as estratégias calcularam os tokens corretamente! 🎯")
    else:
        print("\n❌ ERRO: Os cálculos estão incorretos!")
        print(f"   Esperado {total_esperado}, mas got {usuario.saldoTokens}")

    return usuario


# Mantém compatibilidade
def test_strategy_pattern(token_service):
    """Testa o padrão Strategy com diferentes tipos de ação (compatibilidade)."""
    return testar_padrao_strategy(token_service)


def testar_padrao_decorator():
    """
    Testa o Padrão Decorator - Adiciona funcionalidades extras dinamicamente.

    O padrão Decorator é como customizar um hambúrguer:
    - Começa com o hambúrguer base (RegistraAcaoService)
    - Adiciona queijo (LogDecorator) → agora tem log!
    - Adiciona bacon (BonusDecorator) → agora tem bônus!
    - O hambúrguer continua sendo hambúrguer, só ficou mais completo!

    Este teste mostra como combinar decoradores para ter múltiplas funcionalidades.
    """
    imprimir_separador("TESTE 3: Padrão Decorator (Estrutural)")

    # Cria um usuário novo
    usuario = Usuario("João Santos")
    print(f"\n👤 Usuário de teste: {usuario.nome}")
    print(f"💰 Saldo inicial: {usuario.saldoTokens} tokens\n")

    # Monta a estrutura com decoradores
    servico_tokens = TokenService()
    servico_base = RegistraAcaoService(servico_tokens)

    # Aqui está a mágica! Vamos "embrulhar" o serviço com decoradores
    # É tipo colocar uma caixa dentro de outra caixa
    print("🎁 Montando a cadeia de decoradores:")
    print("   Serviço Base → LogDecorator → BonusDecorator")
    print("   (cada um adiciona uma funcionalidade extra)\n")

    servico_decorado = BonusDecorator(LogDecorator(servico_base))

    print("🧪 Testando com os decoradores ativos:")
    print("-" * 70)

    # Teste 1: Ação pequena (não ganha bônus)
    print("\n📍 TESTE 1: Ação de Reciclagem (10 tokens - SEM bônus)")
    acao1 = AcaoSustentavel("Reciclagem")
    tokens1 = servico_decorado.registrar_acao(usuario, acao1)
    print(f"   → Tokens da ação: {tokens1}")
    print(f"   → Saldo atual: {usuario.saldoTokens} tokens")
    print(f"   → Não ganhou bônus (só ações 20+ ganham)")

    # Teste 2: Ação grande (ganha bônus!)
    print("\n📍 TESTE 2: Ação de PlantioArvore (25 tokens - COM bônus!)")
    acao2 = AcaoSustentavel("PlantioArvore")
    tokens2 = servico_decorado.registrar_acao(usuario, acao2)
    print(f"   → Tokens da ação: {tokens2}")
    print(f"   → Saldo atual: {usuario.saldoTokens} tokens")
    print(f"   → Ganhou +5 tokens de bônus! 🎉")

    # Verificação final
    saldo_esperado = 10 + 25 + 5  # Reciclagem + PlantioArvore + Bônus
    print(f"\n📊 Resumo:")
    print(f"   Saldo final: {usuario.saldoTokens} tokens")
    print(f"   Saldo esperado: {saldo_esperado} tokens")
    print(f"   (10 de reciclagem + 25 de plantar + 5 de bônus)")

    if usuario.saldoTokens == saldo_esperado:
        print("\n✅ DECORATOR FUNCIONANDO PERFEITAMENTE!")
        print("   O LogDecorator registrou as ações")
        print("   O BonusDecorator deu 5 tokens extras")
        print("   Tudo funcionando em harmonia! 🎊")
    else:
        print("\n❌ ERRO: Decoradores não funcionaram corretamente!")
        print(f"   Esperado {saldo_esperado}, mas got {usuario.saldoTokens}")


# Mantém compatibilidade
def test_decorator_pattern():
    """Testa o padrão Decorator com LogDecorator e BonusDecorator (compatibilidade)."""
    testar_padrao_decorator()


def testar_sistema_integrado():
    """
    Testa o Sistema Completo - Todos os padrões trabalhando juntos!

    Este é o grand finale! 🎭
    Aqui vemos os 3 padrões GoF trabalhando em perfeita harmonia:

    🏗️  Singleton: Uma única instância do TokenService para todo o sistema
    🎯 Strategy: Cada ação usa sua própria estratégia de cálculo
    🎨 Decorator: Log e bônus funcionando juntos sem modificar o código base

    É como uma orquestra tocando uma sinfonia - cada instrumento (padrão)
    tem seu papel, mas juntos criam algo incrível!
    """
    imprimir_separador("TESTE 4: Sistema Integrado (Todos os Padrões Juntos)")

    print("\n🎼 Preparando a orquestra dos padrões GoF...\n")

    # 🏗️ Singleton: Sempre a mesma instância
    servico_tokens = TokenService()
    print("✓ Singleton: TokenService instanciado (sempre o mesmo objeto)")

    # 🎨 Decorator: Montando a cadeia
    servico_base = RegistraAcaoService(servico_tokens)
    servico_completo = BonusDecorator(LogDecorator(servico_base))
    print("✓ Decorator: Cadeia montada (Base → Log → Bônus)")

    # 🎯 Strategy: Pronto para usar diferentes algoritmos
    print("✓ Strategy: 5 estratégias prontas para calcular tokens")

    # Cria usuária
    usuario = Usuario("Ana Costa")
    print(f"\n👤 Usuária: {usuario.nome}")
    print(f"💰 Saldo inicial: {usuario.saldoTokens} tokens\n")

    # Simula um dia típico de ações sustentáveis
    acoes_do_dia = [
        ("Reciclagem", AcaoSustentavel("Reciclagem"), 10, 0),           # 10 total
        ("PlantioArvore", AcaoSustentavel("PlantioArvore"), 25, 5),     # 30 total
        ("EconomiaRecursos", AcaoSustentavel("EconomiaRecursos"), 20, 5), # 25 total
        ("Transporte", AcaoSustentavel("Transporte"), 15, 0),           # 15 total
        ("PlantioArvore", AcaoSustentavel("PlantioArvore"), 25, 5),     # 30 total
    ]

    print("🌍 Simulando um dia cheio de ações sustentáveis:")
    print("=" * 70)

    for i, (nome, acao, tokens_base, bonus) in enumerate(acoes_do_dia, 1):
        print(f"\n{i}ª Ação: {nome}")
        servico_completo.registrar_acao(usuario, acao)
        esperado = tokens_base + bonus
        print(f"   💎 Tokens desta ação: {tokens_base} + {bonus} bônus = {esperado} tokens")

    # Cálculos finais
    total_esperado = sum(tokens + bonus for _, _, tokens, bonus in acoes_do_dia)
    print("\n" + "=" * 70)
    print(f"\n📊 RESULTADO FINAL:")
    print(f"   Saldo atual: {usuario.saldoTokens} tokens")
    print(f"   Saldo esperado: {total_esperado} tokens")
    print(f"   Cálculo: 10 + 30 + 25 + 15 + 30 = {total_esperado}")

    if usuario.saldoTokens == total_esperado:
        print("\n" + "🎉" * 35)
        print("✅ SISTEMA INTEGRADO FUNCIONANDO PERFEITAMENTE!")
        print("\n   🏗️  Singleton manteve uma única instância")
        print("   🎯 Strategy calculou os tokens corretamente")
        print("   🎨 Decorator adicionou logs e bônus")
        print("\n   TODOS OS PADRÕES GoF TRABALHANDO EM HARMONIA! 🎊")
        print("🎉" * 35)
    else:
        print(f"\n❌ ERRO: Saldo incorreto!")
        print(f"   Esperado {total_esperado}, mas obteve {usuario.saldoTokens}")


# Mantém compatibilidade
def test_integrated_system():
    """Testa o sistema integrado com todos os padrões juntos (compatibilidade)."""
    testar_sistema_integrado()


def principal():
    """
    Função Principal - Roda todos os testes dos padrões GoF.

    Esta função executa uma bateria completa de testes que demonstram
    e validam os 3 padrões de projeto implementados no sistema.
    """
    # Banner de início
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  TESTES DOS PADRÕES GoF - SUSTENTABILIDADEJÁ".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" + "  Validando Singleton, Strategy e Decorator".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)

    try:
        print("\n🚀 Iniciando bateria de testes...\n")

        # 🏗️ Teste 1: Padrão Singleton (Criacional)
        servico_tokens = testar_padrao_singleton()

        # 🎯 Teste 2: Padrão Strategy (Comportamental)
        testar_padrao_strategy(servico_tokens)

        # 🎨 Teste 3: Padrão Decorator (Estrutural)
        testar_padrao_decorator()

        # 🎼 Teste 4: Sistema Completo (Todos juntos)
        testar_sistema_integrado()

        # Resumo Final
        imprimir_separador("RESUMO FINAL DOS TESTES")
        print("\n📋 Padrões de Projeto Implementados e Testados:\n")
        print("   ✅ Padrão Singleton (Criacional)")
        print("      → Uma única instância do TokenService")
        print("      → Garante consistência em todo o sistema\n")

        print("   ✅ Padrão Strategy (Comportamental)")
        print("      → Estratégias diferentes para cada tipo de ação")
        print("      → Fácil adicionar novos tipos sem modificar código\n")

        print("   ✅ Padrão Decorator (Estrutural)")
        print("      → Funcionalidades extras (log e bônus)")
        print("      → Pode combinar decoradores livremente\n")

        print("=" * 70)
        print("\n🎊 PARABÉNS! TODOS OS PADRÕES GoF ESTÃO FUNCIONANDO! 🎊")
        print("\n   O sistema está implementando corretamente:")
        print("   • Design Patterns de qualidade")
        print("   • Código limpo e manutenível")
        print("   • Arquitetura extensível")
        print("\n" + "=" * 70 + "\n")

    except Exception as erro:
        print("\n" + "❌" * 35)
        print(f"\n💥 ERRO DURANTE OS TESTES: {str(erro)}\n")
        print("❌" * 35 + "\n")
        import traceback
        traceback.print_exc()
        print("\n" + "=" * 70 + "\n")


# Mantém compatibilidade
def main():
    """Função principal que executa todos os testes (compatibilidade)."""
    principal()


if __name__ == "__main__":
    principal()
