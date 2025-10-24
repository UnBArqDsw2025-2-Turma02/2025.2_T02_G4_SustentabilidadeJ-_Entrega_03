from .Iacao import IAcao
from .AcaoReal import AcaoReal
from .AcessoNegadoException import AcessoNegadoException
# from django.contrib.auth.models import User # Assumindo Django User model para autenticação
from datetime import datetime

class AcaoProxy(IAcao):
    """
    Proxy que controla o acesso e implementa Lazy Loading e Cache para o registro de ações.
    
    Funcionalidades:
    - Controle de Acesso: Apenas usuários autenticados podem registrar ações.
    - Lazy Loading: A AcaoReal é instanciada apenas no momento do registro.
    - Cache: Armazena ações registradas para evitar registros duplicados (simulação).
    - Recompensa: Adiciona tokens ao usuário após o registro bem-sucedido.
    """
    
    # Cache estático para simular o armazenamento de ações já registradas (Map)
    _acoes_cache = {}
    
    def __init__(self, usuario, tipo: str, descricao: str, impactoAmbiental: float, tokens_recompensa: int):
        self.usuario = usuario
        self.tipo = tipo
        self.descricao = descricao
        self.impactoAmbiental = impactoAmbiental
        self.tokens_recompensa = tokens_recompensa
        # Lazy Load: AcaoReal é None até ser necessária
        self.acao_real = None

    def registrarAcao(self) -> str:
        # 1. Controle de Acesso (Autenticação)
        if not getattr(self.usuario, 'is_authenticated', True):
            raise AcessoNegadoException(f"[Proxy] Acesso negado. Usuário '{getattr(self.usuario, 'username', 'Desconhecido')}' não está autenticado.")

        # 2. Verificação de Cache Persistente (Usando TokenLedger como registro de histórico)
        from App.tokens.models import TokenLedger
        
        # Cria uma chave única para a ação
        cache_key = f"{getattr(self.usuario, 'username', 'Desconhecido')}_{self.tipo}_{self.descricao}"
        
        # Verifica se já existe um crédito de tokens para esta ação
        acao_existente = TokenLedger.objects.filter(
            user=self.usuario,
            source=TokenLedger.SOURCE_ACTION,
            description=f"Recompensa por ação sustentável: {self.tipo}"
        ).exists()

        if acao_existente:
            resultado = f"[AcaoReal] Ação '{self.tipo}' registrada com sucesso. Impacto: {self.impactoAmbiental}."
            print(f"[Proxy] Ação '{self.tipo}' já registrada anteriormente por '{getattr(self.usuario, 'username', 'Desconhecido')}'. Usando Cache Persistente (TokenLedger).")
            # O Proxy retorna o resultado sem chamar AcaoReal e sem dar nova recompensa
            return resultado

        # 3. Lazy Loading: Instancia AcaoReal apenas agora
        if self.acao_real is None:
            print("[Proxy] Lazy Loading: Instanciando AcaoReal.")
            self.acao_real = AcaoReal(self.tipo, self.descricao, self.impactoAmbiental)

        # 4. Execução da Ação Real
        resultado = self.acao_real.registrarAcao()

        # 5. Recompensa (Integração com o modelo TokenLedger)
        # Cria o registro no TokenLedger, que agora também serve como "cache"
        TokenLedger.objects.create(
            user=self.usuario,
            amount=self.tokens_recompensa,
            type=TokenLedger.TYPE_CREDIT,
            source=TokenLedger.SOURCE_ACTION,
            description=f"Recompensa por ação sustentável: {self.tipo}"
        )
        print(f"[Proxy] Recompensa: {self.tokens_recompensa} tokens creditados ao usuário '{getattr(self.usuario, 'username', 'Desconhecido')}' via TokenLedger.")
            
        # 6. Logging
        from datetime import datetime
        print(f"[LOG] Usuário '{getattr(self.usuario, 'username', 'Desconhecido')}' registrou '{self.tipo}' em {datetime.now()}")

        return resultado

