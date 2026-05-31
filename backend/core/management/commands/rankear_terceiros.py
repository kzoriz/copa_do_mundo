from django.core.management.base import BaseCommand

from core.models import Grupo
from core.api import calcular_classificacao_grupo_obj


class Command(BaseCommand):
    help = "Rankeia os terceiros colocados da fase de grupos"

    def handle(self, *args, **options):
        terceiros = []

        for grupo in Grupo.objects.order_by("nome"):
            classificacao = calcular_classificacao_grupo_obj(grupo)

            if len(classificacao) < 3:
                continue

            terceiro = classificacao[2]
            letra = grupo.nome.replace("Grupo ", "").strip()

            terceiros.append({
                "grupo": letra,
                "time": terceiro["time"],
                "pontos": terceiro["pontos"],
                "saldo": terceiro["saldo"],
                "gols_pro": terceiro["gols_pro"],
                "jogos": terceiro["jogos"],
            })

        terceiros_ordenados = sorted(
            terceiros,
            key=lambda x: (
                -x["pontos"],
                -x["saldo"],
                -x["gols_pro"],
                x["time"],
            )
        )

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Ranking dos terceiros colocados"))
        self.stdout.write("-" * 70)

        for index, item in enumerate(terceiros_ordenados, start=1):
            status = "CLASSIFICADO" if index <= 8 and item["jogos"] > 0 else "ELIMINADO"

            self.stdout.write(
                f"{index:02d}. Grupo {item['grupo']} - "
                f"{item['time']} | "
                f"Pts: {item['pontos']} | "
                f"SG: {item['saldo']} | "
                f"GP: {item['gols_pro']} | "
                f"J: {item['jogos']} | "
                f"{status}"
            )

        self.stdout.write("-" * 70)

        classificados = terceiros_ordenados[:8]

        self.stdout.write(self.style.SUCCESS("8 melhores terceiros:"))

        for item in classificados:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Grupo {item['grupo']} - {item['time']}"
                )
            )