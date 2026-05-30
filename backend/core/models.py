from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Grupo(models.Model):
    nome = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Fase(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    ordem = models.PositiveIntegerField(unique=True)

    class Meta:
        ordering = ["ordem"]

    def __str__(self):
        return self.nome


class Rodada(models.Model):
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE, related_name="rodadas")
    nome = models.CharField(max_length=50)
    ordem = models.PositiveIntegerField()

    class Meta:
        ordering = ["fase__ordem", "ordem"]
        unique_together = ("fase", "ordem")

    def __str__(self):
        return f"{self.fase} - {self.nome}"


class Time(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    sigla = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.nome


class Partida(models.Model):
    fase = models.ForeignKey(Fase, on_delete=models.PROTECT, related_name="partidas")
    rodada = models.ForeignKey(
        Rodada,
        on_delete=models.PROTECT,
        related_name="partidas",
        null=True,
        blank=True
    )
    grupo = models.ForeignKey(
        Grupo,
        on_delete=models.CASCADE,
        related_name="partidas",
        null=True,
        blank=True
    )

    numero_jogo = models.PositiveIntegerField(null=True, blank=True)
    time_casa = models.ForeignKey(Time, on_delete=models.CASCADE, related_name="partidas_casa")
    time_fora = models.ForeignKey(Time, on_delete=models.CASCADE, related_name="partidas_fora")
    data_jogo = models.DateTimeField()
    estadio = models.CharField(max_length=150, blank=True)

    gols_casa = models.IntegerField(null=True, blank=True)
    gols_fora = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["data_jogo"]
        unique_together = ("time_casa", "time_fora", "data_jogo")

    def __str__(self):
        return f"{self.time_casa} x {self.time_fora}"


class Palpite(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="palpites")
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, related_name="palpites")
    gols_casa = models.IntegerField()
    gols_fora = models.IntegerField()
    pontos = models.IntegerField(default=0)

    placar_exato = models.BooleanField(default=False)
    vencedor_correto = models.BooleanField(default=False)

    class Meta:
        unique_together = ("usuario", "partida")

    def __str__(self):
        return f"{self.usuario.username} - {self.partida}"

    def calcular_pontos(self):
        partida = self.partida

        self.placar_exato = False
        self.vencedor_correto = False

        if partida.gols_casa is None or partida.gols_fora is None:
            return 0

        if self.gols_casa == partida.gols_casa and self.gols_fora == partida.gols_fora:
            self.placar_exato = True
            self.vencedor_correto = True
            return 5

        resultado_real = partida.gols_casa - partida.gols_fora
        resultado_palpite = self.gols_casa - self.gols_fora

        if resultado_real == 0 and resultado_palpite == 0:
            self.vencedor_correto = True
            return 3

        if resultado_real > 0 and resultado_palpite > 0:
            self.vencedor_correto = True
            return 3

        if resultado_real < 0 and resultado_palpite < 0:
            self.vencedor_correto = True
            return 3

        return 0