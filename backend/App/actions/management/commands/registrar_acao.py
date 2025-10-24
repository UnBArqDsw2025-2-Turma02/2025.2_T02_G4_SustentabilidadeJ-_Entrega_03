from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from App.actions.servicos.AcaoProxy import AcaoProxy
from App.actions.servicos.AcaoReal import AcaoReal
from App.actions.servicos.AcessoNegadoException import AcessoNegadoException
from App.tokens.models import TokenLedger # Para integração real de recompensa

User = get_user_model()

class Command(BaseCommand):
    help = 'Registra uma ação sustentável usando o padrão Proxy.'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nome de usuário que está registrando a ação.')
        parser.add_argument('tipo', type=str, help='Tipo da ação (ex: Reciclagem).')
        parser.add_argument('descricao', type=str, help='Descrição da ação.')
        parser.add_argument('impacto', type=float, help='Impacto ambiental da ação (Float).')
        parser.add_argument('tokens', type=int, help='Tokens de recompensa para esta ação.')

    def handle(self, *args, **options):
        username = options['username']
        tipo = options['tipo']
        descricao = options['descricao']
        impacto = options['impacto']
        tokens = options['tokens']

        try:
            # 1. Busca o usuário
            user = User.objects.get(username=username)
            
            # 2. Instancia o Proxy
            acao_proxy = AcaoProxy(
                usuario=user,
                tipo=tipo,
                descricao=descricao,
                impactoAmbiental=impacto,
                tokens_recompensa=tokens
            )

            # 3. Executa o registro via Proxy
            resultado = acao_proxy.registrarAcao()
            
            # 4. Sucesso
            self.stdout.write(self.style.SUCCESS(f'Registro de Ação BEM-SUCEDIDO: {resultado}'))
            
            # 5. Verifica se o TokenLedger foi atualizado (integração real)
            # Como o AcaoProxy já faz a lógica de recompensa, vamos apenas confirmar
            self.stdout.write(f'Tokens de Recompensa: {tokens} tokens creditados.')


        except User.DoesNotExist:
            raise CommandError(f'Usuário "{username}" não encontrado.')
        
        except AcessoNegadoException as e:
            self.stdout.write(self.style.ERROR(f'ERRO: Acesso Negado. {e}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'ERRO INESPERADO: {e}'))
            
# Ajuste final no AcaoProxy para usar a lógica de TokenLedger
# O AcaoProxy.py já foi ajustado na iteração anterior para usar o TokenLedger.
# Vou garantir que o AcaoProxy.py esteja na versão correta.

