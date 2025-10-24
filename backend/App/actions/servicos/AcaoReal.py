from .Iacao import IAcao

class AcaoReal(IAcao):
    """Objeto real que contém a lógica pesada de registro da ação sustentável."""
    
    def __init__(self, tipo: str, descricao: str, impactoAmbiental: float):
        self.tipo = tipo
        self.descricao = descricao
        self.impactoAmbiental = impactoAmbiental
        
    def registrarAcao(self) -> str:
        """Simula o registro da ação sustentável no sistema."""
        # Lógica de persistência ou processamento real
        return f"[AcaoReal] Ação '{self.tipo}' registrada com sucesso. Impacto: {self.impactoAmbiental}."
