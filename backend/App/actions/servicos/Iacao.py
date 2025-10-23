from abc import ABC, abstractmethod

class IAcao(ABC):
    """Interface comum para AcaoReal e AcaoProxy."""
    
    @abstractmethod
    def registrarAcao(self) -> str:
        """Método para registrar a ação sustentável."""
        pass