from django.core.management.base import BaseCommand
from App.abstract_factory.servicos.RecyclingFactory import RecyclingFactory

class Command(BaseCommand):
    help = "Registra uma ação sustentável utilizando o padrão Abstract Factory."

    def handle(self, *args, **options):
        factory = RecyclingFactory()

        payload = {"kg": 2.5}
        logger = factory.createLogger()
        calc = factory.createCalculator()
        reward = factory.createRewardIssuer()

        logger.logAction("user001", payload)
        tokens = calc.calculateTokens(payload)
        self.stdout.write(self.style.SUCCESS(reward.issueReward("user001", tokens)))
