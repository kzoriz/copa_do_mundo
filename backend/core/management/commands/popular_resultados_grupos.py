from django.core.management.base import BaseCommand
from core.models import Partida


RESULTADOS = {
    # Grupo A
    1: (2, 1),
    2: (1, 1),
    25: (2, 0),
    28: (3, 1),
    55: (0, 2),
    56: (1, 1),

    # Grupo B
    3: (2, 0),
    5: (1, 2),
    26: (2, 1),
    27: (3, 0),
    51: (1, 1),
    52: (2, 0),

    # Grupo C
    6: (1, 0),
    7: (0, 1),
    30: (0, 1),
    31: (1, 0),
    49: (1, 0),
    50: (1, 0),

    # Grupo D
    4: (2, 1),
    8: (1, 1),
    29: (2, 0),
    32: (1, 2),
    57: (1, 0),
    58: (2, 2),

    # Grupo E
    9: (1, 1),
    11: (2, 1),
    34: (2, 2),
    35: (1, 0),
    53: (0, 2),
    54: (1, 1),

    # Grupo F
    10: (2, 1),
    12: (1, 0),
    33: (1, 1),
    36: (0, 2),
    59: (1, 2),
    60: (2, 2),

    # Grupo G
    14: (3, 1),
    16: (1, 1),
    38: (2, 0),
    40: (1, 2),
    65: (0, 2),
    66: (1, 1),

    # Grupo H
    13: (2, 0),
    15: (1, 2),
    37: (3, 1),
    39: (2, 0),
    63: (1, 1),
    64: (0, 2),

    # Grupo I
    17: (2, 1),
    18: (1, 1),
    41: (3, 0),
    42: (2, 2),
    61: (1, 0),
    62: (0, 2),

    # Grupo J
    19: (3, 1),
    20: (0, 0),
    43: (2, 0),
    44: (1, 1),
    67: (0, 3),
    68: (2, 1),

    # Grupo K
    21: (2, 0),
    24: (1, 2),
    45: (3, 1),
    48: (2, 2),
    69: (1, 2),
    70: (0, 1),

    # Grupo L
    22: (2, 1),
    23: (1, 1),
    46: (2, 0),
    47: (1, 2),
    71: (0, 3),
    72: (1, 1),
}


class Command(BaseCommand):
    help = "Popula resultados simulados de todas as partidas da fase de grupos"

    def handle(self, *args, **options):
        atualizadas = 0
        nao_encontradas = []

        for numero_jogo, (gols_casa, gols_fora) in RESULTADOS.items():
            try:
                partida = Partida.objects.get(numero_jogo=numero_jogo)
            except Partida.DoesNotExist:
                nao_encontradas.append(numero_jogo)
                continue

            partida.gols_casa = gols_casa
            partida.gols_fora = gols_fora
            partida.save(update_fields=["gols_casa", "gols_fora"])

            atualizadas += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"Jogo {numero_jogo}: {partida.time_casa} {gols_casa} x {gols_fora} {partida.time_fora}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"{atualizadas} resultados atualizados com sucesso."
            )
        )

        if nao_encontradas:
            self.stdout.write(
                self.style.WARNING(
                    f"Partidas não encontradas: {nao_encontradas}"
                )
            )