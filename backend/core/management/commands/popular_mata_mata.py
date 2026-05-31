from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime

from core.models import Fase, Partida


JOGOS_MATA_MATA = [
    ("16 Avos de Final", 73, "2026-06-28T13:00:00-03:00", "SoFi Stadium - Los Angeles", "2º Grupo A", "2º Grupo B"),
    ("16 Avos de Final", 74, "2026-06-29T14:30:00-03:00", "Gillette Stadium - Boston", "1º Grupo E", "3º A/B/C/D/F"),
    ("16 Avos de Final", 75, "2026-06-29T19:00:00-03:00", "Estádio BBVA - Monterrey", "1º Grupo F", "2º Grupo C"),
    ("16 Avos de Final", 76, "2026-06-29T23:00:00-03:00", "NRG Stadium - Houston", "1º Grupo C", "2º Grupo F"),
    ("16 Avos de Final", 77, "2026-06-30T15:00:00-03:00", "MetLife Stadium - Nova York/NJ", "1º Grupo I", "3º C/D/F/G/H"),
    ("16 Avos de Final", 78, "2026-06-30T11:00:00-03:00", "AT&T Stadium - Dallas", "2º Grupo E", "2º Grupo I"),
    ("16 Avos de Final", 79, "2026-06-30T19:00:00-03:00", "Estádio Azteca - Cidade do México", "1º Grupo A", "3º C/E/F/H/I"),
    ("16 Avos de Final", 80, "2026-07-01T10:00:00-03:00", "BMO Field - Toronto", "1º Grupo L", "3º E/H/I/J/K"),
    ("16 Avos de Final", 81, "2026-07-01T18:00:00-03:00", "Levi's Stadium - San Francisco Bay Area", "1º Grupo D", "3º B/E/F/I/J"),
    ("16 Avos de Final", 82, "2026-07-01T14:00:00-03:00", "Lumen Field - Seattle", "1º Grupo G", "3º A/E/H/I/J"),
    ("16 Avos de Final", 83, "2026-07-02T17:00:00-03:00", "Hard Rock Stadium - Miami", "2º Grupo K", "2º Grupo L"),
    ("16 Avos de Final", 84, "2026-07-02T13:00:00-03:00", "Mercedes-Benz Stadium - Atlanta", "1º Grupo H", "2º Grupo J"),
    ("16 Avos de Final", 85, "2026-07-02T21:00:00-03:00", "BC Place - Vancouver", "1º Grupo B", "3º E/F/G/I/J"),
    ("16 Avos de Final", 86, "2026-07-03T16:00:00-03:00", "GEHA Field at Arrowhead - Kansas City", "1º Grupo J", "2º Grupo H"),
    ("16 Avos de Final", 87, "2026-07-03T19:30:00-03:00", "Lincoln Financial Field - Filadélfia", "1º Grupo K", "3º D/E/I/J/L"),
    ("16 Avos de Final", 88, "2026-07-03T12:00:00-03:00", "Estádio Akron - Guadalajara", "2º Grupo D", "2º Grupo G"),


    # Oitavas - 89 a 96
    ("Oitavas de Final", 89, "2026-07-04T16:00:00-03:00", "A definir"),
    ("Oitavas de Final", 90, "2026-07-04T19:00:00-03:00", "A definir"),
    ("Oitavas de Final", 91, "2026-07-05T16:00:00-03:00", "A definir"),
    ("Oitavas de Final", 92, "2026-07-05T19:00:00-03:00", "A definir"),
    ("Oitavas de Final", 93, "2026-07-06T16:00:00-03:00", "A definir"),
    ("Oitavas de Final", 94, "2026-07-06T19:00:00-03:00", "A definir"),
    ("Oitavas de Final", 95, "2026-07-07T16:00:00-03:00", "A definir"),
    ("Oitavas de Final", 96, "2026-07-07T19:00:00-03:00", "A definir"),

    # Quartas - 97 a 100
    ("Quartas de Final", 97, "2026-07-09T16:00:00-03:00", "A definir"),
    ("Quartas de Final", 98, "2026-07-09T19:00:00-03:00", "A definir"),
    ("Quartas de Final", 99, "2026-07-10T16:00:00-03:00", "A definir"),
    ("Quartas de Final", 100, "2026-07-10T19:00:00-03:00", "A definir"),

    # Semifinal - 101 e 102
    ("Semifinal", 101, "2026-07-14T16:00:00-03:00", "A definir"),
    ("Semifinal", 102, "2026-07-15T16:00:00-03:00", "A definir"),

    # 3º Lugar e Final
    ("Disputa do 3º Lugar", 103, "2026-07-18T16:00:00-03:00", "A definir"),
    ("Final", 104, "2026-07-19T16:00:00-03:00", "A definir"),
]


class Command(BaseCommand):
    help = "Cria previamente as partidas do mata-mata sem times definidos"

    def handle(self, *args, **options):
        for item in JOGOS_MATA_MATA:
            if len(item) == 6:
                fase_nome, numero_jogo, data_jogo, estadio, mandante_ref, visitante_ref = item
            else:
                fase_nome, numero_jogo, data_jogo, estadio = item
                mandante_ref = "A definir"
                visitante_ref = "A definir"

            fase = Fase.objects.get(nome=fase_nome)

            partida, created = Partida.objects.update_or_create(
                fase=fase,
                numero_jogo=numero_jogo,
                defaults={
                    "rodada": None,
                    "grupo": None,
                    "time_casa": None,
                    "time_fora": None,
                    "data_jogo": parse_datetime(data_jogo),
                    "estadio": estadio,
                }
            )

            acao = "criada" if created else "atualizada"
            self.stdout.write(
                self.style.SUCCESS(
                    f"Partida {numero_jogo} - {fase_nome} {acao}: {mandante_ref} vs {visitante_ref}"
                )
            )