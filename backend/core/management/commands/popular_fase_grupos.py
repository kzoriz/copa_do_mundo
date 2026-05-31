from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime

from core.models import Grupo, Fase, Rodada, Time, Partida


JOGOS = [
    # Rodada 1 - jogos 1 a 24
    (1, "Grupo A", "2026-06-11T16:00:00-03:00", "MEX", "RSA", "Estádio Azteca"),
    (1, "Grupo A", "2026-06-11T23:00:00-03:00", "KOR", "CZE", "Estádio Akron"),
    (1, "Grupo B", "2026-06-12T16:00:00-03:00", "CAN", "BIH", "BMO Field"),
    (1, "Grupo D", "2026-06-12T22:00:00-03:00", "USA", "PAR", "SoFi Stadium"),
    (1, "Grupo B", "2026-06-13T16:00:00-03:00", "QAT", "SUI", "Levi's Stadium"),
    (1, "Grupo C", "2026-06-13T19:00:00-03:00", "BRA", "MAR", "MetLife Stadium"),
    (1, "Grupo C", "2026-06-13T22:00:00-03:00", "HAI", "SCO", "Gillette Stadium"),
    (1, "Grupo D", "2026-06-14T01:00:00-03:00", "AUS", "TUR", "BC Place Stadium"),
    (1, "Grupo E", "2026-06-14T14:00:00-03:00", "GER", "CUW", "NRG Stadium"),
    (1, "Grupo F", "2026-06-14T17:00:00-03:00", "NED", "JPN", "AT&T Stadium"),
    (1, "Grupo E", "2026-06-14T20:00:00-03:00", "CIV", "ECU", "Lincoln Financial Field"),
    (1, "Grupo F", "2026-06-14T23:00:00-03:00", "SWE", "TUN", "Estádio BBVA"),
    (1, "Grupo H", "2026-06-15T13:00:00-03:00", "ESP", "CPV", "Mercedes-Benz Stadium"),
    (1, "Grupo G", "2026-06-15T16:00:00-03:00", "BEL", "EGY", "Lumen Field"),
    (1, "Grupo H", "2026-06-15T19:00:00-03:00", "KSA", "URU", "Hard Rock Stadium"),
    (1, "Grupo G", "2026-06-15T22:00:00-03:00", "IRN", "NZL", "SoFi Stadium"),
    (1, "Grupo I", "2026-06-16T16:00:00-03:00", "FRA", "SEN", "MetLife Stadium"),
    (1, "Grupo I", "2026-06-16T19:00:00-03:00", "IRQ", "NOR", "Gillette Stadium"),
    (1, "Grupo J", "2026-06-16T22:00:00-03:00", "ARG", "ALG", "GEHA Field at Arrowhead Stadium"),
    (1, "Grupo J", "2026-06-17T01:00:00-03:00", "AUT", "JOR", "Levi's Stadium"),
    (1, "Grupo K", "2026-06-17T14:00:00-03:00", "POR", "COD", "NRG Stadium"),
    (1, "Grupo L", "2026-06-17T17:00:00-03:00", "ENG", "CRO", "AT&T Stadium"),
    (1, "Grupo L", "2026-06-17T20:00:00-03:00", "GHA", "PAN", "BMO Field"),
    (1, "Grupo K", "2026-06-17T23:00:00-03:00", "UZB", "COL", "Estádio Azteca"),

    # Rodada 2 - jogos 25 a 48
    (2, "Grupo A", "2026-06-18T13:00:00-03:00", "CZE", "RSA", "Mercedes-Benz Stadium"),
    (2, "Grupo B", "2026-06-18T16:00:00-03:00", "SUI", "BIH", "SoFi Stadium"),
    (2, "Grupo B", "2026-06-18T19:00:00-03:00", "CAN", "QAT", "BC Place Stadium"),
    (2, "Grupo A", "2026-06-18T22:00:00-03:00", "MEX", "KOR", "Estádio Akron"),
    (2, "Grupo D", "2026-06-19T16:00:00-03:00", "USA", "AUS", "Lumen Field"),
    (2, "Grupo C", "2026-06-19T19:00:00-03:00", "SCO", "MAR", "Gillette Stadium"),
    (2, "Grupo C", "2026-06-19T21:30:00-03:00", "BRA", "HAI", "Lincoln Financial Field"),
    (2, "Grupo D", "2026-06-20T00:00:00-03:00", "TUR", "PAR", "Levi's Stadium"),
    (2, "Grupo F", "2026-06-20T14:00:00-03:00", "NED", "SWE", "NRG Stadium"),
    (2, "Grupo E", "2026-06-20T17:00:00-03:00", "GER", "CIV", "BMO Field"),
    (2, "Grupo E", "2026-06-20T21:00:00-03:00", "ECU", "CUW", "GEHA Field at Arrowhead Stadium"),
    (2, "Grupo F", "2026-06-21T01:00:00-03:00", "TUN", "JPN", "Estádio BBVA"),
    (2, "Grupo H", "2026-06-21T13:00:00-03:00", "ESP", "KSA", "Mercedes-Benz Stadium"),
    (2, "Grupo G", "2026-06-21T16:00:00-03:00", "BEL", "IRN", "SoFi Stadium"),
    (2, "Grupo H", "2026-06-21T19:00:00-03:00", "URU", "CPV", "Hard Rock Stadium"),
    (2, "Grupo G", "2026-06-21T22:00:00-03:00", "NZL", "EGY", "BC Place Stadium"),
    (2, "Grupo I", "2026-06-22T13:00:00-03:00", "FRA", "IRQ", "MetLife Stadium"),
    (2, "Grupo I", "2026-06-22T16:00:00-03:00", "NOR", "SEN", "Lincoln Financial Field"),
    (2, "Grupo J", "2026-06-22T19:00:00-03:00", "ARG", "AUT", "AT&T Stadium"),
    (2, "Grupo J", "2026-06-22T22:00:00-03:00", "ALG", "JOR", "Lumen Field"),
    (2, "Grupo K", "2026-06-23T13:00:00-03:00", "POR", "UZB", "NRG Stadium"),
    (2, "Grupo L", "2026-06-23T16:00:00-03:00", "ENG", "GHA", "Gillette Stadium"),
    (2, "Grupo L", "2026-06-23T19:00:00-03:00", "PAN", "CRO", "BMO Field"),
    (2, "Grupo K", "2026-06-23T22:00:00-03:00", "COL", "COD", "Estádio Akron"),

    # Rodada 3 - jogos 49 a 72
    (3, "Grupo C", "2026-06-24T19:00:00-03:00", "SCO", "BRA", "Hard Rock Stadium"),
    (3, "Grupo C", "2026-06-24T19:00:00-03:00", "MAR", "HAI", "Mercedes-Benz Stadium"),
    (3, "Grupo B", "2026-06-24T22:00:00-03:00", "SUI", "CAN", "SoFi Stadium"),
    (3, "Grupo B", "2026-06-24T22:00:00-03:00", "BIH", "QAT", "BC Place Stadium"),
    (3, "Grupo E", "2026-06-25T17:00:00-03:00", "ECU", "GER", "MetLife Stadium"),
    (3, "Grupo E", "2026-06-25T17:00:00-03:00", "CUW", "CIV", "Lincoln Financial Field"),
    (3, "Grupo A", "2026-06-25T22:00:00-03:00", "CZE", "MEX", "Estádio Azteca"),
    (3, "Grupo A", "2026-06-25T22:00:00-03:00", "RSA", "KOR", "Estádio Akron"),
    (3, "Grupo D", "2026-06-26T17:00:00-03:00", "PAR", "AUS", "NRG Stadium"),
    (3, "Grupo D", "2026-06-26T17:00:00-03:00", "TUR", "USA", "AT&T Stadium"),
    (3, "Grupo F", "2026-06-26T21:00:00-03:00", "TUN", "NED", "GEHA Field at Arrowhead Stadium"),
    (3, "Grupo F", "2026-06-26T21:00:00-03:00", "JPN", "SWE", "Lumen Field"),
    (3, "Grupo I", "2026-06-26T23:00:00-03:00", "SEN", "IRQ", "BMO Field"),
    (3, "Grupo I", "2026-06-26T23:00:00-03:00", "NOR", "FRA", "Gillette Stadium"),
    (3, "Grupo H", "2026-06-27T14:00:00-03:00", "URU", "ESP", "Estádio Akron"),
    (3, "Grupo H", "2026-06-27T14:00:00-03:00", "CPV", "KSA", "NRG Stadium"),
    (3, "Grupo G", "2026-06-27T17:00:00-03:00", "NZL", "BEL", "BC Place Stadium"),
    (3, "Grupo G", "2026-06-27T17:00:00-03:00", "EGY", "IRN", "Lumen Field"),
    (3, "Grupo J", "2026-06-27T19:30:00-03:00", "JOR", "ARG", "Levi's Stadium"),
    (3, "Grupo J", "2026-06-27T19:30:00-03:00", "ALG", "AUT", "SoFi Stadium"),
    (3, "Grupo K", "2026-06-27T22:00:00-03:00", "COL", "POR", "Hard Rock Stadium"),
    (3, "Grupo K", "2026-06-27T22:00:00-03:00", "COD", "UZB", "Mercedes-Benz Stadium"),
    (3, "Grupo L", "2026-06-27T23:59:00-03:00", "PAN", "ENG", "MetLife Stadium"),
    (3, "Grupo L", "2026-06-27T23:59:00-03:00", "GHA", "CRO", "Lincoln Financial Field"),
]


class Command(BaseCommand):
    help = "Popula todas as partidas da fase de grupos usando siglas dos times"

    def handle(self, *args, **options):
        fase_grupos = Fase.objects.get(nome="Fase de Grupos")

        numero_jogo = 1

        for ordem_rodada, grupo_nome, data, sigla_casa, sigla_fora, estadio in JOGOS:
            grupo, _ = Grupo.objects.get_or_create(nome=grupo_nome)

            rodada, _ = Rodada.objects.get_or_create(
                fase=fase_grupos,
                ordem=ordem_rodada,
                defaults={"nome": f"{ordem_rodada}ª Rodada"}
            )

            time_casa = Time.objects.get(sigla=sigla_casa)
            time_fora = Time.objects.get(sigla=sigla_fora)

            partida, created = Partida.objects.update_or_create(
                fase=fase_grupos,
                numero_jogo=numero_jogo,
                defaults={
                    "rodada": rodada,
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
            self.style.SUCCESS("Fase de grupos populada com sucesso!")
        )