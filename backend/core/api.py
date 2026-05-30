from ninja import Router
from typing import List
from ninja import Schema
from core.models import Partida, Palpite
from core.jwt_utils import obter_usuario_request

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