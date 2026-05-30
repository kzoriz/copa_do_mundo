from ninja import Router
from typing import List
from ninja import Schema
from core.models import Partida, Palpite
from core.jwt_utils import obter_usuario_request
from django.db.models import Sum, Count
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

router = Router()




class PalpiteSchema(Schema):
    partida_id: int
    gols_casa: int
    gols_fora: int


@router.post("/palpites")
def criar_palpite(request, data: PalpiteSchema):
    usuario = obter_usuario_request(request)

    if usuario is None:
        return {
            "success": False,
            "message": "Você precisa estar logado."
        }

    partida = Partida.objects.get(id=data.partida_id)

    if Palpite.objects.filter(usuario=usuario, partida=partida).exists():
        return {
            "success": False,
            "message": "Você já fez um palpite para este jogo e não pode editar."
        }

    palpite = Palpite.objects.create(
        usuario=usuario,
        partida=partida,
        gols_casa=data.gols_casa,
        gols_fora=data.gols_fora,
    )

    return {
        "success": True,
        "message": "Palpite salvo com sucesso.",
        "palpite": {
            "id": palpite.id,
            "partida_id": partida.id,
            "gols_casa": palpite.gols_casa,
            "gols_fora": palpite.gols_fora,
        }
    }


@router.get("/partidas")
def listar_partidas(request):
    partidas = Partida.objects.select_related(
        "fase", "rodada", "grupo", "time_casa", "time_fora"
    ).all()

    return [
        {
            "id": p.id,
            "numero_jogo": p.numero_jogo,
            "fase": p.fase.nome,
            "rodada": p.rodada.nome if p.rodada else None,
            "grupo": p.grupo.nome if p.grupo else None,
            "time_casa": p.time_casa.nome,
            "time_fora": p.time_fora.nome,
            "data_jogo": p.data_jogo,
            "estadio": p.estadio,
            "gols_casa": p.gols_casa,
            "gols_fora": p.gols_fora,
        }
        for p in partidas
    ]

@router.get("/meus-palpites")
def meus_palpites(request):
    usuario = obter_usuario_request(request)

    if usuario is None:
        return {
            "success": False,
            "message": "Você precisa estar logado."
        }

    palpites = Palpite.objects.select_related(
        "partida",
        "partida__fase",
        "partida__rodada",
        "partida__grupo",
        "partida__time_casa",
        "partida__time_fora",
    ).filter(usuario=usuario).order_by("partida__data_jogo")

    return {
        "success": True,
        "palpites": [
            {
                "id": p.id,
                "partida_id": p.partida.id,
                "numero_jogo": p.partida.numero_jogo,
                "fase": p.partida.fase.nome if p.partida.fase else None,
                "rodada": p.partida.rodada.nome if p.partida.rodada else None,
                "grupo": p.partida.grupo.nome if p.partida.grupo else None,
                "time_casa": p.partida.time_casa.nome,
                "time_fora": p.partida.time_fora.nome,
                "data_jogo": p.partida.data_jogo,
                "estadio": p.partida.estadio,
                "gols_casa": p.gols_casa,
                "gols_fora": p.gols_fora,
                "pontos": p.pontos,
            }
            for p in palpites
        ]
    }

@router.get("/ranking")
def ranking(request):
    usuarios = User.objects.annotate(
        total_pontos=Sum("palpites__pontos"),
        total_palpites=Count("palpites"),
        total_placares_exatos=Count(
            "palpites",
            filter=models.Q(palpites__placar_exato=True)
        ),
        total_vencedores_corretos=Count(
            "palpites",
            filter=models.Q(palpites__vencedor_correto=True)
        ),
    ).filter(
        total_palpites__gt=0
    ).order_by(
        "-total_pontos",
        "-total_placares_exatos",
        "-total_vencedores_corretos",
        "date_joined",
    )

    return {
        "success": True,
        "ranking": [
            {
                "posicao": index + 1,
                "usuario": user.email or user.username,
                "pontos": user.total_pontos or 0,
                "palpites": user.total_palpites,
                "placares_exatos": user.total_placares_exatos,
                "vencedores_corretos": user.total_vencedores_corretos,
            }
            for index, user in enumerate(usuarios)
        ]
    }

class ResultadoOficialSchema(Schema):
    partida_id: int
    gols_casa: int
    gols_fora: int


@router.post("/resultado-oficial")
def salvar_resultado_oficial(request, data: ResultadoOficialSchema):
    usuario = obter_usuario_request(request)

    if usuario is None:
        return {
            "success": False,
            "message": "Você precisa estar logado."
        }

    if not usuario.is_staff and not usuario.is_superuser:
        return {
            "success": False,
            "message": "Você não tem permissão para cadastrar resultados."
        }

    partida = Partida.objects.get(id=data.partida_id)
    partida.gols_casa = data.gols_casa
    partida.gols_fora = data.gols_fora
    partida.save(update_fields=["gols_casa", "gols_fora"])

    for palpite in partida.palpites.all():
        palpite.pontos = palpite.calcular_pontos()
        palpite.save(update_fields=["pontos", "placar_exato", "vencedor_correto"])

    return {
        "success": True,
        "message": "Resultado oficial salvo com sucesso."
    }