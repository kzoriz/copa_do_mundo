from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime

from core.models import Grupo, Fase, Rodada, Time, Partida


JOGOS = [
    ("Grupo C", "2026-06-24T19:00:00-03:00", 62, 59, "Hard Rock Stadium"),
    ("Grupo C", "2026-06-24T19:00:00-03:00", 60, 61, "Mercedes-Benz Stadium"),
    ("Grupo B", "2026-06-24T22:00:00-03:00", 58, 53, "SoFi Stadium"),
    ("Grupo B", "2026-06-24T22:00:00-03:00", 54, 57, "BC Place Stadium"),

    ("Grupo E", "2026-06-25T17:00:00-03:00", 70, 65, "MetLife Stadium"),
    ("Grupo E", "2026-06-25T17:00:00-03:00", 66, 69, "Lincoln Financial Field"),
    ("Grupo A", "2026-06-25T22:00:00-03:00", 52, 49, "Estádio Azteca"),
    ("Grupo A", "2026-06-25T22:00:00-03:00", 50, 51, "Estádio Akron"),

    ("Grupo D", "2026-06-26T17:00:00-03:00", 56, 63, "NRG Stadium"),
    ("Grupo D", "2026-06-26T17:00:00-03:00", 64, 55, "AT&T Stadium"),
    ("Grupo F", "2026-06-26T21:00:00-03:00", 72, 67, "GEHA Field at Arrowhead Stadium"),
    ("Grupo F", "2026-06-26T21:00:00-03:00", 68, 71, "Lumen Field"),

    ("Grupo I", "2026-06-26T23:00:00-03:00", 82, 83, "BMO Field"),
    ("Grupo I", "2026-06-26T23:00:00-03:00", 84, 81, "Gillette Stadium"),
    ("Grupo H", "2026-06-27T14:00:00-03:00", 78, 73, "Estádio Akron"),
    ("Grupo H", "2026-06-27T14:00:00-03:00", 74, 77, "NRG Stadium"),

    ("Grupo G", "2026-06-27T17:00:00-03:00", 80, 75, "BC Place Stadium"),
    ("Grupo G", "2026-06-27T17:00:00-03:00", 76, 79, "Lumen Field"),
    ("Grupo J", "2026-06-27T19:30:00-03:00", 88, 85, "Levi's Stadium"),
    ("Grupo J", "2026-06-27T19:30:00-03:00", 86, 87, "SoFi Stadium"),

    ("Grupo K", "2026-06-27T22:00:00-03:00", 96, 89, "Hard Rock Stadium"),
    ("Grupo K", "2026-06-27T22:00:00-03:00", 90, 95, "Mercedes-Benz Stadium"),
    ("Grupo L", "2026-06-27T23:59:00-03:00", 94, 91, "MetLife Stadium"),
    ("Grupo L", "2026-06-27T23:59:00-03:00", 93, 92, "Lincoln Financial Field"),
]


class Command(BaseCommand):
    help = "Popula os jogos da terceira rodada da fase de grupos"

    def handle(self, *args, **options):
        fase_grupos = Fase.objects.get(nome="Fase de Grupos")

        rodada_3, _ = Rodada.objects.get_or_create(
            fase=fase_grupos,
            ordem=3,
            defaults={"nome": "3ª Rodada"}
        )

        numero_jogo = 49

        for grupo_nome, data, time_casa_id, time_fora_id, estadio in JOGOS:
            grupo = Grupo.objects.get(nome=grupo_nome)

            time_casa = Time.objects.get(id=time_casa_id)
            time_fora = Time.objects.get(id=time_fora_id)

            partida, created = Partida.objects.update_or_create(
                fase=fase_grupos,
                numero_jogo=numero_jogo,
                defaults={
                    "rodada": rodada_3,
                    "grupo": grupo,
                    "time_casa": time_casa,
                    "time_fora": time_fora,
                    "data_jogo": parse_datetime(data),
                    "estadio": estadio,
                }
            )

            acao = "Criado" if created else "Atualizado"

            self.stdout.write(
                self.style.SUCCESS(
                    f"{acao} - Jogo {numero_jogo}: {time_casa.nome} x {time_fora.nome}"
                )
            )

            numero_jogo += 1

        self.stdout.write(
            self.style.SUCCESS("Terceira rodada populada com sucesso!")
        )