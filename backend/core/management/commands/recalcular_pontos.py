from django.core.management.base import BaseCommand
from core.models import Palpite


class Command(BaseCommand):
    help = "Recalcula os pontos de todos os palpites"

    def handle(self, *args, **options):
        total = 0

        for palpite in Palpite.objects.select_related("partida"):
            palpite.pontos = palpite.calcular_pontos()
            palpite.save(update_fields=["pontos", "placar_exato", "vencedor_correto"])
            total += 1

        self.stdout.write(
            self.style.SUCCESS(f"{total} palpites recalculados com sucesso.")
        )
