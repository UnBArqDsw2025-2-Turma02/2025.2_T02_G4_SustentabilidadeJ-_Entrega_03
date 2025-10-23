# teste_tokens.py
from App.actions.servicos.registrar_acao import RegistraAcaoService
from App.tokens.servicos.token_servico import TokenService
from App.authentication.models import Usuario
from App.actions.models import AcaoSustentavel


# Criar usuário e serviço
usuario = Usuario("Lucas")
token_service = TokenService()
registra_service = RegistraAcaoService(token_service)

# Criar ações
acoes = [
    AcaoSustentavel("Reciclagem"),
    AcaoSustentavel("Transporte"),
    AcaoSustentavel("PlantioArvore")
]

# Registrar ações e gerar tokens
for acao in acoes:
    tokens = registra_service.registrar_acao(usuario, acao)
    print(f"Ação {acao.tipoAcao} gerou {tokens} tokens.")

print(f"Saldo final do usuário: {usuario.saldoTokens}")
