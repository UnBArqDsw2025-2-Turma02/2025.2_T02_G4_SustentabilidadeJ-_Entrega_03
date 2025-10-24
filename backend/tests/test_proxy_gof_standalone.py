from datetime import datetime
import unittest
import sys
from io import StringIO

sys.path.append('/home/ubuntu/sustentabilidade_ja/2025.2_T02_G4_SustentabilidadeJ-_Entrega_03/backend/App/actions/servicos/')

# Importando classes do Proxy
from Iacao import IAcao
from AcaoReal import AcaoReal
from AcaoProxy import AcaoProxy
from AcessoNegadoException import AcessoNegadoException

# Mock para a classe User do Django para simular autenticação e o método adicionarTokens
class MockUser:
    def __init__(self, username, is_authenticated, has_add_tokens=True):
        self.username = username
        self.is_authenticated = is_authenticated
        self.tokens_adicionados = 0
        if has_add_tokens:
            # Define a função adicionarTokens se has_add_tokens for True
            def add_tokens(qtd):
                self.tokens_adicionados += qtd
            self.adicionarTokens = add_tokens
        # Se has_add_tokens for False, o método adicionarTokens não é definido, o que causa AttributeError ao ser chamado.
        
    def __str__(self):
        return self.username
        
    def adicionarTokens(self, qtd):
        self.tokens_adicionados += qtd
        print(f"MockUser: {qtd} tokens adicionados. Saldo total: {self.tokens_adicionados}")

class TestAcaoProxy(unittest.TestCase):

    def setUp(self):
        # Resetar o cache para cada teste
        AcaoProxy._acoes_cache = {}
        
        # Usuários mock
        self.usuario_autenticado = MockUser("Alice", True)
        self.usuario_nao_autenticado = MockUser("Bob", False)
        
        # Dados da Ação
        self.tipo = "Reciclagem de Plástico"
        self.descricao = "Reciclagem de 5kg de plástico"
        self.impacto = 0.5
        self.tokens = 10
        
        # Captura de stdout para verificar logs e prints
        self.held_stdout = sys.stdout
        self.captured_output = StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        # Restaura stdout
        sys.stdout = self.held_stdout
        
    def test_01_acesso_negado_nao_autenticado(self):
        """Testa se o acesso é negado para usuário não autenticado."""
        proxy = AcaoProxy(self.usuario_nao_autenticado, self.tipo, self.descricao, self.impacto, self.tokens)
        with self.assertRaises(AcessoNegadoException) as context:
            proxy.registrarAcao()
        self.assertIn("não está autenticado", str(context.exception))

    def test_02_registro_bem_sucedido_e_lazy_loading(self):
        """Testa o registro bem-sucedido e a aplicação do Lazy Loading."""
        proxy = AcaoProxy(self.usuario_autenticado, self.tipo, self.descricao, self.impacto, self.tokens)
        
        # Antes do registro, acao_real deve ser None (Lazy Loading)
        self.assertIsNone(proxy.acao_real)
        
        resultado = proxy.registrarAcao()
        
        # Após o registro, acao_real deve ter sido instanciada
        self.assertIsNotNone(proxy.acao_real)
        self.assertIsInstance(proxy.acao_real, AcaoReal)
        self.assertIn("[AcaoReal] Ação 'Reciclagem de Plástico' registrada", resultado)
        
        # Verifica se o cache foi atualizado
        cache_key = f"{self.usuario_autenticado.username}_{self.tipo}_{self.descricao}"
        self.assertIn(cache_key, AcaoProxy._acoes_cache)
        
        # Verifica se a mensagem de Lazy Loading foi exibida
        self.assertIn("[Proxy] Lazy Loading: Instanciando AcaoReal.", self.captured_output.getvalue())

    def test_03_cache_aplicado(self):
        """Testa se o cache é utilizado no segundo registro da mesma ação."""
        proxy1 = AcaoProxy(self.usuario_autenticado, self.tipo, self.descricao, self.impacto, self.tokens)
        proxy1.registrarAcao() # Primeiro registro (popula cache)
        
        # Limpa a saída para o segundo teste
        self.captured_output.truncate(0)
        self.captured_output.seek(0)
        
        # Segundo registro com a mesma chave
        proxy2 = AcaoProxy(self.usuario_autenticado, self.tipo, self.descricao, self.impacto, self.tokens)
        
        # O AcaoReal não deve ser instanciado novamente
        self.assertIsNone(proxy2.acao_real)
        
        resultado = proxy2.registrarAcao()
        
        # Verifica se a mensagem de cache foi exibida
        self.assertIn("Usando cache", self.captured_output.getvalue())
        self.assertNotIn("[Proxy] Lazy Loading: Instanciando AcaoReal.", self.captured_output.getvalue())
        self.assertIn("[AcaoReal] Ação 'Reciclagem de Plástico' registrada", resultado)

    def test_04_recompensa_simulada_sem_metodo(self):
        """Testa se a mensagem de aviso de recompensa é exibida quando o método não existe."""
        # Cria um MockUser que não tem o método adicionarTokens
        class MockUserSemMetodo:
            def __init__(self, username, is_authenticated):
                self.username = username
                self.is_authenticated = is_authenticated
            # Não define adicionarTokens, causando AttributeError
        usuario_sem_metodo = MockUserSemMetodo("Carlos", True)
        
        proxy = AcaoProxy(usuario_sem_metodo, self.tipo, self.descricao, self.impacto, self.tokens)
        
        proxy.registrarAcao()
        
        # Verifica se a mensagem de aviso foi exibida
        self.assertIn("Aviso: Não foi possível adicionar tokens. O modelo de Usuário precisa do método 'adicionarTokens'.", self.captured_output.getvalue())

if __name__ == '__main__':
    unittest.main()
