import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import Time


class Command(BaseCommand):
    help = "Carrega bandeiras dos times usando a sigla do time"

    def handle(self, *args, **options):
        pasta_static = os.path.join(settings.BASE_DIR, "static", "img")
        pasta_media = os.path.join(settings.MEDIA_ROOT, "bandeiras")

        os.makedirs(pasta_media, exist_ok=True)

        extensoes = ["png", "jpg", "jpeg", "webp", "svg"]

        atualizados = 0
        nao_encontrados = []

        for time in Time.objects.all().order_by("nome"):
            sigla = time.sigla.strip().lower()

            arquivo = f"{sigla}.webp"
            origem = os.path.join(pasta_static, arquivo)

            if not os.path.exists(origem):
                arquivo = f"{time.sigla.upper()}.webp"
                origem = os.path.join(pasta_static, arquivo)

            if not os.path.exists(origem):
                nao_encontrados.append(f"{time.nome} ({time.sigla})")
                continue

            destino = os.path.join(pasta_media, arquivo)

            shutil.copy2(origem, destino)

            time.bandeira = f"bandeiras/{arquivo}"
            time.save(update_fields=["bandeira"])

            atualizados += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Bandeiras atualizadas: {atualizados}"))

        if nao_encontrados:
            self.stdout.write(self.style.WARNING("Bandeiras não encontradas:"))
            for item in nao_encontrados:
                self.stdout.write(self.style.WARNING(f"- {item}"))