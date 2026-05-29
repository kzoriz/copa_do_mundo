from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime

from core.models import Grupo, Fase, Rodada, Time, Partida


FASES = [
    (1, "Fase de Grupos"),
    (2, "16 Avos de Final"),
    (3, "Oitavas de Final"),
    (4, "Quartas de Final"),
    (5, "Semifinal"),
    (6, "Disputa do 3º Lugar"),
    (7, "Final"),
]


JOGOS_PRIMEIRA_RODADA = [
    (1, "Grupo A", "2026-06-11T16:00:00-03:00", "México", "África do Sul", "Estádio Azteca"),
    (2, "Grupo A", "2026-06-11T23:00:00-03:00", "Coreia do Sul", "Chéquia", "Estádio Akron"),
    (3, "Grupo B", "2026-06-12T16:00:00-03:00", "Canadá", "Bósnia e Herzegovina", "BMO Field"),
    (4, "Grupo D", "2026-06-12T22:00:00-03:00", "Estados Unidos", "Paraguai", "SoFi Stadium"),
    (5, "Grupo B", "2026-06-13T16:00:00-03:00", "Catar", "Suíça", "Levi's Stadium"),
    (6, "Grupo C", "2026-06-13T19:00:00-03:00", "Brasil", "Marrocos", "MetLife Stadium"),
    (7, "Grupo C", "2026-06-13T22:00:00-03:00", "Haiti", "Escócia", "Gillette Stadium"),
    (8, "Grupo D", "2026-06-14T01:00:00-03:00", "Austrália", "Turquia", "BC Place Stadium"),
    (9, "Grupo E", "2026-06-14T14:00:00-03:00", "Alemanha", "Curaçau", "NRG Stadium"),
    (10, "Grupo F", "2026-06-14T17:00:00-03:00", "Países Baixos", "Japão", "AT&T Stadium"),
    (11, "Grupo E", "2026-06-14T20:00:00-03:00", "Costa do Marfim", "Equador", "Lincoln Financial Field"),
    (12, "Grupo F", "2026-06-14T23:00:00-03:00", "Suécia", "Tunísia", "Estádio BBVA"),
    (13, "Grupo H", "2026-06-15T13:00:00-03:00", "Espanha", "Cabo Verde", "Mercedes-Benz Stadium"),
    (14, "Grupo G", "2026-06-15T16:00:00-03:00", "Bélgica", "Egito", "Lumen Field"),
    (15, "Grupo H", "2026-06-15T19:00:00-03:00", "Arábia Saudita", "Uruguai", "Hard Rock Stadium"),
    (16, "Grupo G", "2026-06-15T22:00:00-03:00", "Irã", "Nova Zelândia", "SoFi Stadium"),
    (17, "Grupo I", "2026-06-16T16:00:00-03:00", "França", "Senegal", "MetLife Stadium"),
    (18, "Grupo I", "2026-06-16T19:00:00-03:00", "Iraque", "Noruega", "Gillette Stadium"),
    (19, "Grupo J", "2026-06-16T22:00:00-03:00", "Argentina", "Argélia", "GEHA Field at Arrowhead Stadium"),
    (20, "Grupo J", "2026-06-17T01:00:00-03:00", "Áustria", "Jordânia", "Levi's Stadium"),
    (21, "Grupo K", "2026-06-17T14:00:00-03:00", "Portugal", "República Democrática do Congo", "NRG Stadium"),
    (22, "Grupo L", "2026-06-17T17:00:00-03:00", "Inglaterra", "Croácia", "AT&T Stadium"),
    (23, "Grupo L", "2026-06-17T20:00:00-03:00", "Gana", "Panamá", "BMO Field"),
    (24, "Grupo K", "2026-06-17T23:00:00-03:00", "Uzbequistão", "Colômbia", "Estádio Azteca"),
]


SIGLAS = {
    "México": "MEX",
    "África do Sul": "RSA",
    "Coreia do Sul": "KOR",
    "Chéquia": "CZE",
    "Canadá": "CAN",
    "Bósnia e Herzegovina": "BIH",
    "Catar": "QAT",
    "Suíça": "SUI",
    "Brasil": "BRA",
    "Marrocos": "MAR",
    "Haiti": "HAI",
    "Escócia": "SCO",
    "Estados Unidos": "USA",
    "Paraguai": "PAR",
    "Austrália": "AUS",
    "Turquia": "TUR",
    "Alemanha": "GER",
    "Curaçau": "CUW",
    "Costa do Marfim": "CIV",
    "Equador": "ECU",
    "Países Baixos": "NED",
    "Japão": "JPN",
    "Suécia": "SWE",
    "Tunísia": "TUN",
    "Bélgica": "BEL",
    "Egito": "EGY",
    "Irã": "IRN",
    "Nova Zelândia": "NZL",
    "Espanha": "ESP",
    "Cabo Verde": "CPV",
    "Arábia Saudita": "KSA",
    "Uruguai": "URU",
    "França": "FRA",
    "Senegal": "SEN",
    "Iraque": "IRQ",
    "Noruega": "NOR",
    "Argentina": "ARG",
    "Argélia": "ALG",
    "Áustria": "AUT",
    "Jordânia": "JOR",
    "Portugal": "POR",
    "República Democrática do Congo": "COD",
    "Inglaterra": "ENG",
    "Croácia": "CRO",
    "Gana": "GHA",
    "Panamá": "PAN",
    "Uzbequistão": "UZB",
    "Colômbia": "COL",
}


class Command(BaseCommand):
    help = "Popula fases, rodadas, grupos, times e jogos da Copa 2026"

    def handle(self, *args, **options):
        for ordem, nome in FASES:
            Fase.objects.update_or_create(
                ordem=ordem,
                defaults={"nome": nome}
            )

        fase_grupos = Fase.objects.get(nome="Fase de Grupos")

        for ordem in range(1, 4):
            Rodada.objects.update_or_create(
                fase=fase_grupos,
                ordem=ordem,
                defaults={"nome": f"{ordem}ª Rodada"}
            )

        rodada_1 = Rodada.objects.get(fase=fase_grupos, ordem=1)

        for letra in "ABCDEFGHIJKL":
            Grupo.objects.get_or_create(nome=f"Grupo {letra}")

        for numero_jogo, grupo_nome, data, casa, fora, estadio in JOGOS_PRIMEIRA_RODADA:
            grupo = Grupo.objects.get(nome=grupo_nome)

            time_casa, _ = Time.objects.update_or_create(
                nome=casa,
                defaults={"sigla": SIGLAS.get(casa, casa[:3].upper())}
            )

            time_fora, _ = Time.objects.update_or_create(
                nome=fora,
                defaults={"sigla": SIGLAS.get(fora, fora[:3].upper())}
            )

            Partida.objects.update_or_create(
                numero_jogo=numero_jogo,
                defaults={
                    "fase": fase_grupos,
                    "rodada": rodada_1,
                    "grupo": grupo,
                    "time_casa": time_casa,
                    "time_fora": time_fora,
                    "data_jogo": parse_datetime(data),
                    "estadio": estadio,
                }
            )

            self.stdout.write(self.style.SUCCESS(f"Jogo {numero_jogo}: {casa} x {fora}"))

        self.stdout.write(self.style.SUCCESS("Carga inicial finalizada."))