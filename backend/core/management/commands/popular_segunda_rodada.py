from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime

from core.models import Grupo, Fase, Rodada, Time, Partida


JOGOS = [
    ("Grupo A", "2026-06-18T13:00:00-03:00", 52, 50, "Mercedes-Benz Stadium"),
    ("Grupo B", "2026-06-18T16:00:00-03:00", 58, 54, "SoFi Stadium"),
    ("Grupo B", "2026-06-18T19:00:00-03:00", 53, 57, "BC Place Stadium"),
    ("Grupo A", "2026-06-18T22:00:00-03:00", 49, 51, "Estádio Akron"),

    ("Grupo D", "2026-06-19T16:00:00-03:00", 55, 63, "Lumen Field"),
    ("Grupo C", "2026-06-19T19:00:00-03:00", 62, 60, "Gillette Stadium"),
    ("Grupo C", "2026-06-19T21:30:00-03:00", 59, 61, "Lincoln Financial Field"),
    ("Grupo D", "2026-06-20T00:00:00-03:00", 64, 56, "Levi's Stadium"),

    ("Grupo F", "2026-06-20T14:00:00-03:00", 67, 71, "NRG Stadium"),
    ("Grupo E", "2026-06-20T17:00:00-03:00", 65, 69, "BMO Field"),
    ("Grupo E", "2026-06-20T21:00:00-03:00", 70, 66, "GEHA Field at Arrowhead Stadium"),
    ("Grupo F", "2026-06-21T01:00:00-03:00", 72, 68, "Estádio BBVA"),

    ("Grupo H", "2026-06-21T13:00:00-03:00", 73, 77, "Mercedes-Benz Stadium"),
    ("Grupo G", "2026-06-21T16:00:00-03:00", 75, 79, "SoFi Stadium"),
    ("Grupo H", "2026-06-21T19:00:00-03:00", 78, 74, "Hard Rock Stadium"),
    ("Grupo G", "2026-06-21T22:00:00-03:00", 80, 76, "BC Place Stadium"),

    ("Grupo I", "2026-06-22T13:00:00-03:00", 81, 83, "MetLife Stadium"),
    ("Grupo I", "2026-06-22T16:00:00-03:00", 84, 82, "Lincoln Financial Field"),

    ("Grupo J", "2026-06-22T19:00:00-03:00", 85, 87, "AT&T Stadium"),
    ("Grupo J", "2026-06-22T22:00:00-03:00", 86, 88, "Lumen Field"),

    ("Grupo K", "2026-06-23T13:00:00-03:00", 89, 95, "NRG Stadium"),
    ("Grupo L", "2026-06-23T16:00:00-03:00", 91, 93, "Gillette Stadium"),
    ("Grupo L", "2026-06-23T19:00:00-03:00", 94, 92, "BMO Field"),
    ("Grupo K", "2026-06-23T22:00:00-03:00", 96, 90, "Estádio Akron"),
]


class Command(BaseCommand):
    help = "Popula os jogos da segunda rodada da fase de grupos"

    def handle(self, *args, **options):
        fase_grupos = Fase.objects.get(nome="Fase de Grupos")

        rodada_2, _ = Rodada.objects.get_or_create(
            fase=fase_grupos,
            ordem=2,
            defaults={
                "nome": "2ª Rodada"
            }
        )

        numero_jogo = 25

        for grupo_nome, data, time_casa_id, time_fora_id, estadio in JOGOS:
            grupo = Grupo.objects.get(nome=grupo_nome)

            time_casa = Time.objects.get(id=time_casa_id)
            time_fora = Time.objects.get(id=time_fora_id)

            partida, created = Partida.objects.update_or_create(
                fase=fase_grupos,
                numero_jogo=numero_jogo,
                defaults={
                    "rodada": rodada_2,
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
                    f"{acao} - Jogo {numero_jogo}: "
                    f"{time_casa.nome} x {time_fora.nome}"
                )
            )

            numero_jogo += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Segunda rodada populada com sucesso!"
            )
        )