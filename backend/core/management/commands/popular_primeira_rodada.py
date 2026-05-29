from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from core.models import Grupo, Time, Partida


JOGOS = [
    ("Grupo A", "2026-06-11T16:00:00-03:00", "México", "África do Sul", "Estádio Azteca"),
    ("Grupo A", "2026-06-11T23:00:00-03:00", "Coreia do Sul", "Chéquia", "Estádio Akron"),
    ("Grupo B", "2026-06-12T16:00:00-03:00", "Canadá", "Bósnia e Herzegovina", "BMO Field"),
    ("Grupo D", "2026-06-12T22:00:00-03:00", "Estados Unidos", "Paraguai", "SoFi Stadium"),
    ("Grupo B", "2026-06-13T16:00:00-03:00", "Catar", "Suíça", "Levi's Stadium"),
    ("Grupo C", "2026-06-13T19:00:00-03:00", "Brasil", "Marrocos", "MetLife Stadium"),
    ("Grupo C", "2026-06-13T22:00:00-03:00", "Haiti", "Escócia", "Gillette Stadium"),
    ("Grupo D", "2026-06-14T01:00:00-03:00", "Austrália", "Turquia", "BC Place Stadium"),
    ("Grupo E", "2026-06-14T14:00:00-03:00", "Alemanha", "Curaçau", "NRG Stadium"),
    ("Grupo F", "2026-06-14T17:00:00-03:00", "Países Baixos", "Japão", "AT&T Stadium"),
    ("Grupo E", "2026-06-14T20:00:00-03:00", "Costa do Marfim", "Equador", "Lincoln Financial Field"),
    ("Grupo F", "2026-06-14T23:00:00-03:00", "Suécia", "Tunísia", "Estádio BBVA"),
    ("Grupo H", "2026-06-15T13:00:00-03:00", "Espanha", "Cabo Verde", "Mercedes-Benz Stadium"),
    ("Grupo G", "2026-06-15T16:00:00-03:00", "Bélgica", "Egito", "Lumen Field"),
    ("Grupo H", "2026-06-15T19:00:00-03:00", "Arábia Saudita", "Uruguai", "Hard Rock Stadium"),
    ("Grupo G", "2026-06-15T22:00:00-03:00", "Irã", "Nova Zelândia", "SoFi Stadium"),
    ("Grupo I", "2026-06-16T16:00:00-03:00", "França", "Senegal", "MetLife Stadium"),
    ("Grupo I", "2026-06-16T19:00:00-03:00", "Iraque", "Noruega", "Gillette Stadium"),
    ("Grupo J", "2026-06-16T22:00:00-03:00", "Argentina", "Argélia", "GEHA Field at Arrowhead Stadium"),
    ("Grupo J", "2026-06-17T01:00:00-03:00", "Áustria", "Jordânia", "Levi's Stadium"),
    ("Grupo K", "2026-06-17T14:00:00-03:00", "Portugal", "República Democrática do Congo", "NRG Stadium"),
    ("Grupo L", "2026-06-17T17:00:00-03:00", "Inglaterra", "Croácia", "AT&T Stadium"),
    ("Grupo L", "2026-06-17T20:00:00-03:00", "Gana", "Panamá", "BMO Field"),
    ("Grupo K", "2026-06-17T23:00:00-03:00", "Uzbequistão", "Colômbia", "Estádio Azteca"),
]


class Command(BaseCommand):
    help = "Popula grupos, times e jogos da primeira rodada"

    def handle(self, *args, **options):
        for grupo_nome, data, casa, fora, estadio in JOGOS:
            grupo, _ = Grupo.objects.get_or_create(nome=grupo_nome)

            time_casa, _ = Time.objects.get_or_create(
                nome=casa,
                defaults={"sigla": casa[:3].upper()}
            )

            time_fora, _ = Time.objects.get_or_create(
                nome=fora,
                defaults={"sigla": fora[:3].upper()}
            )

            Partida.objects.update_or_create(
                grupo=grupo,
                time_casa=time_casa,
                time_fora=time_fora,
                rodada=1,
                defaults={
                    "data_jogo": parse_datetime(data),
                    "estadio": estadio,
                }
            )

            self.stdout.write(self.style.SUCCESS(f"{grupo_nome}: {casa} x {fora}"))

        self.stdout.write(self.style.SUCCESS("Primeira rodada populada com sucesso."))
