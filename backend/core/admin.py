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
    )
    list_filter = ("fase", "rodada", "grupo")
    search_fields = ("time_casa__nome", "time_fora__nome", "estadio")


@admin.register(Palpite)
class PalpiteAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "partida", "gols_casa", "gols_fora", "pontos")

