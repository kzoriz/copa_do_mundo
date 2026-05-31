from django.core.management.base import BaseCommand
from core.models import Time


TIMES = [
    ("México", "MEX"),
    ("África do Sul", "RSA"),
    ("Coreia do Sul", "KOR"),
    ("Chéquia", "CZE"),

    ("Canadá", "CAN"),
    ("Bósnia e Herzegovina", "BIH"),
    ("Catar", "QAT"),
    ("Suíça", "SUI"),

    ("Brasil", "BRA"),
    ("Marrocos", "MAR"),
    ("Haiti", "HAI"),
    ("Escócia", "SCO"),

    ("Estados Unidos", "USA"),
    ("Paraguai", "PAR"),
    ("Austrália", "AUS"),
    ("Turquia", "TUR"),

    ("Alemanha", "GER"),
    ("Curaçau", "CUW"),
    ("Costa do Marfim", "CIV"),
    ("Equador", "ECU"),

    ("Países Baixos", "NED"),
    ("Japão", "JPN"),
    ("Suécia", "SWE"),
    ("Tunísia", "TUN"),

    ("Bélgica", "BEL"),
    ("Egito", "EGY"),
    ("Irã", "IRN"),
    ("Nova Zelândia", "NZL"),

    ("Espanha", "ESP"),
    ("Cabo Verde", "CPV"),
    ("Arábia Saudita", "KSA"),
    ("Uruguai", "URU"),

    ("França", "FRA"),
    ("Senegal", "SEN"),
    ("Iraque", "IRQ"),
    ("Noruega", "NOR"),

    ("Argentina", "ARG"),
    ("Argélia", "ALG"),
    ("Áustria", "AUT"),
    ("Jordânia", "JOR"),

    ("Portugal", "POR"),
    ("República Democrática do Congo", "COD"),
    ("Uzbequistão", "UZB"),
    ("Colômbia", "COL"),

    ("Inglaterra", "ENG"),
    ("Croácia", "CRO"),
    ("Gana", "GHA"),
    ("Panamá", "PAN"),
]


class Command(BaseCommand):
    help = "Popula todas as seleções da Copa com siglas FIFA"

    def handle(self, *args, **options):

        for nome, sigla in TIMES:

            time, created = Time.objects.update_or_create(
                sigla=sigla,
                defaults={
                    "nome": nome
                }
            )

            acao = "Criado" if created else "Atualizado"

            self.stdout.write(
                self.style.SUCCESS(
                    f"{acao}: {sigla} - {nome}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"{len(TIMES)} seleções processadas com sucesso."
            )
        )