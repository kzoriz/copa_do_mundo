import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime

from core.models import Grupo, Fase, Rodada, Time, Partida


FASES = [(1, 'Fase de Grupos'),
 (2, '16 Avos de Final'),
 (3, 'Oitavas de Final'),
 (4, 'Quartas de Final'),
 (5, 'Semifinal'),
 (6, 'Disputa do 3º Lugar'),
 (7, 'Final')]


TIMES = [('México', 'MEX'),
 ('África do Sul', 'RSA'),
 ('Coreia do Sul', 'KOR'),
 ('Chéquia', 'CZE'),
 ('Canadá', 'CAN'),
 ('Bósnia e Herzegovina', 'BIH'),
 ('Catar', 'QAT'),
 ('Suíça', 'SUI'),
 ('Brasil', 'BRA'),
 ('Marrocos', 'MAR'),
 ('Haiti', 'HAI'),
 ('Escócia', 'SCO'),
 ('Estados Unidos', 'USA'),
 ('Paraguai', 'PAR'),
 ('Austrália', 'AUS'),
 ('Turquia', 'TUR'),
 ('Alemanha', 'GER'),
 ('Curaçau', 'CUW'),
 ('Costa do Marfim', 'CIV'),
 ('Equador', 'ECU'),
 ('Países Baixos', 'NED'),
 ('Japão', 'JPN'),
 ('Suécia', 'SWE'),
 ('Tunísia', 'TUN'),
 ('Bélgica', 'BEL'),
 ('Egito', 'EGY'),
 ('Irã', 'IRN'),
 ('Nova Zelândia', 'NZL'),
 ('Espanha', 'ESP'),
 ('Cabo Verde', 'CPV'),
 ('Arábia Saudita', 'KSA'),
 ('Uruguai', 'URU'),
 ('França', 'FRA'),
 ('Senegal', 'SEN'),
 ('Iraque', 'IRQ'),
 ('Noruega', 'NOR'),
 ('Argentina', 'ARG'),
 ('Argélia', 'ALG'),
 ('Áustria', 'AUT'),
 ('Jordânia', 'JOR'),
 ('Portugal', 'POR'),
 ('República Democrática do Congo', 'COD'),
 ('Uzbequistão', 'UZB'),
 ('Colômbia', 'COL'),
 ('Inglaterra', 'ENG'),
 ('Croácia', 'CRO'),
 ('Gana', 'GHA'),
 ('Panamá', 'PAN')]


JOGOS_FASE_GRUPOS = [(1, 'Grupo A', '2026-06-11T16:00:00-03:00', 'MEX', 'RSA', 'Estádio Azteca'),
 (1, 'Grupo A', '2026-06-11T23:00:00-03:00', 'KOR', 'CZE', 'Estádio Akron'),
 (1, 'Grupo B', '2026-06-12T16:00:00-03:00', 'CAN', 'BIH', 'BMO Field'),
 (1, 'Grupo D', '2026-06-12T22:00:00-03:00', 'USA', 'PAR', 'SoFi Stadium'),
 (1, 'Grupo B', '2026-06-13T16:00:00-03:00', 'QAT', 'SUI', "Levi's Stadium"),
 (1, 'Grupo C', '2026-06-13T19:00:00-03:00', 'BRA', 'MAR', 'MetLife Stadium'),
 (1, 'Grupo C', '2026-06-13T22:00:00-03:00', 'HAI', 'SCO', 'Gillette Stadium'),
 (1, 'Grupo D', '2026-06-14T01:00:00-03:00', 'AUS', 'TUR', 'BC Place Stadium'),
 (1, 'Grupo E', '2026-06-14T14:00:00-03:00', 'GER', 'CUW', 'NRG Stadium'),
 (1, 'Grupo F', '2026-06-14T17:00:00-03:00', 'NED', 'JPN', 'AT&T Stadium'),
 (1, 'Grupo E', '2026-06-14T20:00:00-03:00', 'CIV', 'ECU', 'Lincoln Financial Field'),
 (1, 'Grupo F', '2026-06-14T23:00:00-03:00', 'SWE', 'TUN', 'Estádio BBVA'),
 (1, 'Grupo H', '2026-06-15T13:00:00-03:00', 'ESP', 'CPV', 'Mercedes-Benz Stadium'),
 (1, 'Grupo G', '2026-06-15T16:00:00-03:00', 'BEL', 'EGY', 'Lumen Field'),
 (1, 'Grupo H', '2026-06-15T19:00:00-03:00', 'KSA', 'URU', 'Hard Rock Stadium'),
 (1, 'Grupo G', '2026-06-15T22:00:00-03:00', 'IRN', 'NZL', 'SoFi Stadium'),
 (1, 'Grupo I', '2026-06-16T16:00:00-03:00', 'FRA', 'SEN', 'MetLife Stadium'),
 (1, 'Grupo I', '2026-06-16T19:00:00-03:00', 'IRQ', 'NOR', 'Gillette Stadium'),
 (1, 'Grupo J', '2026-06-16T22:00:00-03:00', 'ARG', 'ALG', 'GEHA Field at Arrowhead Stadium'),
 (1, 'Grupo J', '2026-06-17T01:00:00-03:00', 'AUT', 'JOR', "Levi's Stadium"),
 (1, 'Grupo K', '2026-06-17T14:00:00-03:00', 'POR', 'COD', 'NRG Stadium'),
 (1, 'Grupo L', '2026-06-17T17:00:00-03:00', 'ENG', 'CRO', 'AT&T Stadium'),
 (1, 'Grupo L', '2026-06-17T20:00:00-03:00', 'GHA', 'PAN', 'BMO Field'),
 (1, 'Grupo K', '2026-06-17T23:00:00-03:00', 'UZB', 'COL', 'Estádio Azteca'),
 (2, 'Grupo A', '2026-06-18T13:00:00-03:00', 'CZE', 'RSA', 'Mercedes-Benz Stadium'),
 (2, 'Grupo B', '2026-06-18T16:00:00-03:00', 'SUI', 'BIH', 'SoFi Stadium'),
 (2, 'Grupo B', '2026-06-18T19:00:00-03:00', 'CAN', 'QAT', 'BC Place Stadium'),
 (2, 'Grupo A', '2026-06-18T22:00:00-03:00', 'MEX', 'KOR', 'Estádio Akron'),
 (2, 'Grupo D', '2026-06-19T16:00:00-03:00', 'USA', 'AUS', 'Lumen Field'),
 (2, 'Grupo C', '2026-06-19T19:00:00-03:00', 'SCO', 'MAR', 'Gillette Stadium'),
 (2, 'Grupo C', '2026-06-19T21:30:00-03:00', 'BRA', 'HAI', 'Lincoln Financial Field'),
 (2, 'Grupo D', '2026-06-20T00:00:00-03:00', 'TUR', 'PAR', "Levi's Stadium"),
 (2, 'Grupo F', '2026-06-20T14:00:00-03:00', 'NED', 'SWE', 'NRG Stadium'),
 (2, 'Grupo E', '2026-06-20T17:00:00-03:00', 'GER', 'CIV', 'BMO Field'),
 (2, 'Grupo E', '2026-06-20T21:00:00-03:00', 'ECU', 'CUW', 'GEHA Field at Arrowhead Stadium'),
 (2, 'Grupo F', '2026-06-21T01:00:00-03:00', 'TUN', 'JPN', 'Estádio BBVA'),
 (2, 'Grupo H', '2026-06-21T13:00:00-03:00', 'ESP', 'KSA', 'Mercedes-Benz Stadium'),
 (2, 'Grupo G', '2026-06-21T16:00:00-03:00', 'BEL', 'IRN', 'SoFi Stadium'),
 (2, 'Grupo H', '2026-06-21T19:00:00-03:00', 'URU', 'CPV', 'Hard Rock Stadium'),
 (2, 'Grupo G', '2026-06-21T22:00:00-03:00', 'NZL', 'EGY', 'BC Place Stadium'),
 (2, 'Grupo I', '2026-06-22T13:00:00-03:00', 'FRA', 'IRQ', 'MetLife Stadium'),
 (2, 'Grupo I', '2026-06-22T16:00:00-03:00', 'NOR', 'SEN', 'Lincoln Financial Field'),
 (2, 'Grupo J', '2026-06-22T19:00:00-03:00', 'ARG', 'AUT', 'AT&T Stadium'),
 (2, 'Grupo J', '2026-06-22T22:00:00-03:00', 'ALG', 'JOR', 'Lumen Field'),
 (2, 'Grupo K', '2026-06-23T13:00:00-03:00', 'POR', 'UZB', 'NRG Stadium'),
 (2, 'Grupo L', '2026-06-23T16:00:00-03:00', 'ENG', 'GHA', 'Gillette Stadium'),
 (2, 'Grupo L', '2026-06-23T19:00:00-03:00', 'PAN', 'CRO', 'BMO Field'),
 (2, 'Grupo K', '2026-06-23T22:00:00-03:00', 'COL', 'COD', 'Estádio Akron'),
 (3, 'Grupo C', '2026-06-24T19:00:00-03:00', 'SCO', 'BRA', 'Hard Rock Stadium'),
 (3, 'Grupo C', '2026-06-24T19:00:00-03:00', 'MAR', 'HAI', 'Mercedes-Benz Stadium'),
 (3, 'Grupo B', '2026-06-24T22:00:00-03:00', 'SUI', 'CAN', 'SoFi Stadium'),
 (3, 'Grupo B', '2026-06-24T22:00:00-03:00', 'BIH', 'QAT', 'BC Place Stadium'),
 (3, 'Grupo E', '2026-06-25T17:00:00-03:00', 'ECU', 'GER', 'MetLife Stadium'),
 (3, 'Grupo E', '2026-06-25T17:00:00-03:00', 'CUW', 'CIV', 'Lincoln Financial Field'),
 (3, 'Grupo A', '2026-06-25T22:00:00-03:00', 'CZE', 'MEX', 'Estádio Azteca'),
 (3, 'Grupo A', '2026-06-25T22:00:00-03:00', 'RSA', 'KOR', 'Estádio Akron'),
 (3, 'Grupo D', '2026-06-26T17:00:00-03:00', 'PAR', 'AUS', 'NRG Stadium'),
 (3, 'Grupo D', '2026-06-26T17:00:00-03:00', 'TUR', 'USA', 'AT&T Stadium'),
 (3, 'Grupo F', '2026-06-26T21:00:00-03:00', 'TUN', 'NED', 'GEHA Field at Arrowhead Stadium'),
 (3, 'Grupo F', '2026-06-26T21:00:00-03:00', 'JPN', 'SWE', 'Lumen Field'),
 (3, 'Grupo I', '2026-06-26T23:00:00-03:00', 'SEN', 'IRQ', 'BMO Field'),
 (3, 'Grupo I', '2026-06-26T23:00:00-03:00', 'NOR', 'FRA', 'Gillette Stadium'),
 (3, 'Grupo H', '2026-06-27T14:00:00-03:00', 'URU', 'ESP', 'Estádio Akron'),
 (3, 'Grupo H', '2026-06-27T14:00:00-03:00', 'CPV', 'KSA', 'NRG Stadium'),
 (3, 'Grupo G', '2026-06-27T17:00:00-03:00', 'NZL', 'BEL', 'BC Place Stadium'),
 (3, 'Grupo G', '2026-06-27T17:00:00-03:00', 'EGY', 'IRN', 'Lumen Field'),
 (3, 'Grupo J', '2026-06-27T19:30:00-03:00', 'JOR', 'ARG', "Levi's Stadium"),
 (3, 'Grupo J', '2026-06-27T19:30:00-03:00', 'ALG', 'AUT', 'SoFi Stadium'),
 (3, 'Grupo K', '2026-06-27T22:00:00-03:00', 'COL', 'POR', 'Hard Rock Stadium'),
 (3, 'Grupo K', '2026-06-27T22:00:00-03:00', 'COD', 'UZB', 'Mercedes-Benz Stadium'),
 (3, 'Grupo L', '2026-06-27T23:59:00-03:00', 'PAN', 'ENG', 'MetLife Stadium'),
 (3, 'Grupo L', '2026-06-27T23:59:00-03:00', 'GHA', 'CRO', 'Lincoln Financial Field')]


# Chaveamento atualizado conforme o padrão usado no app/api.py:
# 16 avos:
# - Lado esquerdo visual: 73, 74, 75, 79, 80, 81, 85, 87
# - Lado direito visual: 76, 77, 78, 82, 83, 84, 86, 88
#
# Oitavas:
# 89 = vencedor 74 x vencedor 75
# 90 = vencedor 73 x vencedor 85
# 91 = vencedor 80 x vencedor 87
# 92 = vencedor 81 x vencedor 79
# 93 = vencedor 76 x vencedor 77
# 94 = vencedor 78 x vencedor 88
# 95 = vencedor 83 x vencedor 84
# 96 = vencedor 82 x vencedor 86
JOGOS_MATA_MATA = [('16 Avos de Final', 73, '2026-06-28T13:00:00-03:00', 'SoFi Stadium - Los Angeles', '2º Grupo A', '2º Grupo B'),
 ('16 Avos de Final', 74, '2026-06-29T14:30:00-03:00', 'Gillette Stadium - Boston', '1º Grupo E', '3º A/B/C/D/F'),
 ('16 Avos de Final', 75, '2026-06-30T15:00:00-03:00', 'MetLife Stadium - Nova York/NJ', '1º Grupo I', '3º C/D/F/G/H'),
 ('16 Avos de Final', 76, '2026-06-29T23:00:00-03:00', 'NRG Stadium - Houston', '1º Grupo C', '2º Grupo F'),
 ('16 Avos de Final', 77, '2026-06-30T11:00:00-03:00', 'AT&T Stadium - Dallas', '2º Grupo E', '2º Grupo I'),
 ('16 Avos de Final',
  78,
  '2026-06-30T19:00:00-03:00',
  'Estádio Azteca - Cidade do México',
  '1º Grupo A',
  '3º C/E/F/H/I'),
 ('16 Avos de Final', 79, '2026-07-01T14:00:00-03:00', 'Lumen Field - Seattle', '1º Grupo G', '3º A/E/H/I/J'),
 ('16 Avos de Final', 80, '2026-07-02T17:00:00-03:00', 'Hard Rock Stadium - Miami', '2º Grupo K', '2º Grupo L'),
 ('16 Avos de Final',
  81,
  '2026-07-01T18:00:00-03:00',
  "Levi's Stadium - San Francisco Bay Area",
  '1º Grupo D',
  '3º B/E/F/I/J'),
 ('16 Avos de Final', 82, '2026-07-02T21:00:00-03:00', 'BC Place - Vancouver', '1º Grupo B', '3º E/F/G/I/J'),
 ('16 Avos de Final',
  83,
  '2026-07-03T16:00:00-03:00',
  'GEHA Field at Arrowhead - Kansas City',
  '1º Grupo J',
  '2º Grupo H'),
 ('16 Avos de Final', 84, '2026-07-03T12:00:00-03:00', 'Estádio Akron - Guadalajara', '2º Grupo D', '2º Grupo G'),
 ('16 Avos de Final', 85, '2026-06-29T19:00:00-03:00', 'Estádio BBVA - Monterrey', '1º Grupo F', '2º Grupo C'),
 ('16 Avos de Final',
  86,
  '2026-07-03T19:30:00-03:00',
  'Lincoln Financial Field - Filadélfia',
  '1º Grupo K',
  '3º D/E/I/J/L'),
 ('16 Avos de Final', 87, '2026-07-02T13:00:00-03:00', 'Mercedes-Benz Stadium - Atlanta', '1º Grupo H', '2º Grupo J'),
 ('16 Avos de Final', 88, '2026-07-01T10:00:00-03:00', 'BMO Field - Toronto', '1º Grupo L', '3º E/H/I/J/K'),
 ('Oitavas de Final', 89, '2026-07-04T16:00:00-03:00', 'A definir'),
 ('Oitavas de Final', 90, '2026-07-04T19:00:00-03:00', 'A definir'),
 ('Oitavas de Final', 91, '2026-07-05T16:00:00-03:00', 'A definir'),
 ('Oitavas de Final', 92, '2026-07-05T19:00:00-03:00', 'A definir'),
 ('Oitavas de Final', 93, '2026-07-06T16:00:00-03:00', 'A definir'),
 ('Oitavas de Final', 94, '2026-07-06T19:00:00-03:00', 'A definir'),
 ('Oitavas de Final', 95, '2026-07-07T16:00:00-03:00', 'A definir'),
 ('Oitavas de Final', 96, '2026-07-07T19:00:00-03:00', 'A definir'),
 ('Quartas de Final', 97, '2026-07-09T16:00:00-03:00', 'A definir'),
 ('Quartas de Final', 98, '2026-07-09T19:00:00-03:00', 'A definir'),
 ('Quartas de Final', 99, '2026-07-10T16:00:00-03:00', 'A definir'),
 ('Quartas de Final', 100, '2026-07-10T19:00:00-03:00', 'A definir'),
 ('Semifinal', 101, '2026-07-14T16:00:00-03:00', 'A definir'),
 ('Semifinal', 102, '2026-07-15T16:00:00-03:00', 'A definir'),
 ('Disputa do 3º Lugar', 103, '2026-07-18T16:00:00-03:00', 'A definir'),
 ('Final', 104, '2026-07-19T16:00:00-03:00', 'A definir')]


class Command(BaseCommand):
    help = "Popula a base inicial completa da Copa 2026: times, bandeiras, grupos, fases e partidas"

    def add_arguments(self, parser):
        parser.add_argument(
            "--sem-bandeiras",
            action="store_true",
            help="Não carrega/copiar bandeiras da pasta static/img para media/bandeiras.",
        )

    def handle(self, *args, **options):
        self.criar_fases()
        self.criar_rodadas()
        self.criar_grupos()
        self.criar_times()
        self.criar_partidas_fase_grupos()
        self.criar_partidas_mata_mata()

        if not options["sem_bandeiras"]:
            self.carregar_bandeiras()

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Base inicial da Copa 2026 populada com sucesso."))

    def criar_fases(self):
        self.stdout.write("")
        self.stdout.write(self.style.NOTICE("Criando/atualizando fases..."))

        for ordem, nome in FASES:
            Fase.objects.update_or_create(
                ordem=ordem,
                defaults={"nome": nome},
            )

        self.stdout.write(self.style.SUCCESS("Fases processadas."))

    def criar_rodadas(self):
        self.stdout.write("")
        self.stdout.write(self.style.NOTICE("Criando/atualizando rodadas da fase de grupos..."))

        fase_grupos = Fase.objects.get(nome="Fase de Grupos")

        for ordem in range(1, 4):
            Rodada.objects.update_or_create(
                fase=fase_grupos,
                ordem=ordem,
                defaults={"nome": f"{ordem}ª Rodada"},
            )

        self.stdout.write(self.style.SUCCESS("Rodadas processadas."))

    def criar_grupos(self):
        self.stdout.write("")
        self.stdout.write(self.style.NOTICE("Criando/atualizando grupos..."))

        for letra in "ABCDEFGHIJKL":
            Grupo.objects.get_or_create(nome=f"Grupo {letra}")

        self.stdout.write(self.style.SUCCESS("Grupos processados."))

    def criar_times(self):
        self.stdout.write("")
        self.stdout.write(self.style.NOTICE("Criando/atualizando seleções..."))

        for nome, sigla in TIMES:
            time, created = Time.objects.update_or_create(
                sigla=sigla,
                defaults={"nome": nome},
            )

            acao = "Criado" if created else "Atualizado"
            self.stdout.write(self.style.SUCCESS(f"{acao}: {sigla} - {nome}"))

        self.stdout.write(self.style.SUCCESS(f"{len(TIMES)} seleções processadas."))

    def criar_partidas_fase_grupos(self):
        self.stdout.write("")
        self.stdout.write(self.style.NOTICE("Criando/atualizando partidas da fase de grupos..."))

        fase_grupos = Fase.objects.get(nome="Fase de Grupos")

        for numero_jogo, item in enumerate(JOGOS_FASE_GRUPOS, start=1):
            ordem_rodada, grupo_nome, data_jogo, sigla_casa, sigla_fora, estadio = item

            grupo = Grupo.objects.get(nome=grupo_nome)
            rodada = Rodada.objects.get(fase=fase_grupos, ordem=ordem_rodada)
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
                    "data_jogo": parse_datetime(data_jogo),
                    "estadio": estadio,
                },
            )

            acao = "Criada" if created else "Atualizada"
            self.stdout.write(
                self.style.SUCCESS(
                    f"{acao} - Jogo {numero_jogo}: {time_casa.nome} x {time_fora.nome}"
                )
            )

        self.stdout.write(self.style.SUCCESS("Partidas da fase de grupos processadas."))

    def criar_partidas_mata_mata(self):
        self.stdout.write("")
        self.stdout.write(self.style.NOTICE("Criando/atualizando partidas do mata-mata..."))

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
                },
            )

            acao = "Criada" if created else "Atualizada"
            self.stdout.write(
                self.style.SUCCESS(
                    f"{acao} - Jogo {numero_jogo} - {fase_nome}: "
                    f"{mandante_ref} x {visitante_ref}"
                )
            )

        self.stdout.write(self.style.SUCCESS("Partidas do mata-mata processadas."))

    def carregar_bandeiras(self):
        self.stdout.write("")
        self.stdout.write(self.style.NOTICE("Carregando bandeiras..."))

        pasta_static = os.path.join(settings.BASE_DIR, "static", "img")
        pasta_media = os.path.join(settings.MEDIA_ROOT, "bandeiras")

        os.makedirs(pasta_media, exist_ok=True)

        atualizados = 0
        nao_encontrados = []

        for time in Time.objects.all().order_by("nome"):
            sigla = time.sigla.strip()

            candidatos = [
                f"{sigla.lower()}.webp",
                f"{sigla.upper()}.webp",
                f"{sigla.lower()}.png",
                f"{sigla.upper()}.png",
                f"{sigla.lower()}.jpg",
                f"{sigla.upper()}.jpg",
                f"{sigla.lower()}.jpeg",
                f"{sigla.upper()}.jpeg",
                f"{sigla.lower()}.svg",
                f"{sigla.upper()}.svg",
            ]

            origem = None
            arquivo_encontrado = None

            for arquivo in candidatos:
                caminho = os.path.join(pasta_static, arquivo)

                if os.path.exists(caminho):
                    origem = caminho
                    arquivo_encontrado = arquivo
                    break

            if not origem:
                nao_encontrados.append(f"{time.nome} ({time.sigla})")
                continue

            destino = os.path.join(pasta_media, arquivo_encontrado)
            shutil.copy2(origem, destino)

            time.bandeira = f"bandeiras/{arquivo_encontrado}"
            time.save(update_fields=["bandeira"])

            atualizados += 1

        self.stdout.write(self.style.SUCCESS(f"Bandeiras atualizadas: {atualizados}"))

        if nao_encontrados:
            self.stdout.write(self.style.WARNING("Bandeiras não encontradas:"))
            for item in nao_encontrados:
                self.stdout.write(self.style.WARNING(f"- {item}"))
