from django.contrib import admin
from .models import Grupo, Fase, Rodada, Time, Partida, Palpite


admin.site.register(Grupo)
admin.site.register(Fase)
admin.site.register(Rodada)


@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "sigla", "bandeira")
    search_fields = ("nome", "sigla")


@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "numero_jogo",
        "fase",
        "rodada",
        "grupo",
        "time_casa",
        "time_fora",
        "data_jogo",
        "estadio",
        "gols_casa",
        "gols_fora",
    )

    list_filter = (
        "fase",
        "grupo",
        "rodada",
        "data_jogo",
    )

    search_fields = (
        "numero_jogo",
        "time_casa__nome",
        "time_fora__nome",
        "estadio",
    )

    ordering = (
        "numero_jogo",
        "data_jogo",
    )

    list_per_page = 25


@admin.register(Palpite)
class PalpiteAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "partida", "gols_casa", "gols_fora", "pontos")

