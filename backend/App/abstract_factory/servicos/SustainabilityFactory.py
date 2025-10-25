from abc import ABC, abstractmethod

class ActionLogger(ABC):
    @abstractmethod
    def logAction(self, userId: str, payload: dict) -> bool:
        pass


class TokenCalculator(ABC):
    @abstractmethod
    def calculateTokens(self, payload: dict) -> int:
        pass


class RewardIssuer(ABC):
    @abstractmethod
    def issueReward(self, userId: str, tokens: int) -> str:
        pass


class SustainabilityFactory(ABC):
    @abstractmethod
    def createLogger(self) -> ActionLogger:
        pass

    @abstractmethod
    def createCalculator(self) -> TokenCalculator:
        pass

    @abstractmethod
    def createRewardIssuer(self) -> RewardIssuer:
        pass
