from ninja import Router
from typing import List
from ninja import Schema
from core.models import Partida, Palpite

router = Router()




class PalpiteSchema(Schema):
    partida_id: int
    gols_casa: int
    gols_fora: int


@router.post("/palpites")
def criar_palpite(request, data: PalpiteSchema):
    if not request.user.is_authenticated:
        return {
            "success": False,
            "message": "Você precisa estar logado."
        }

    partida = Partida.objects.get(id=data.partida_id)

    palpite, created = Palpite.objects.update_or_create(
        usuario=request.user,
        partida=partida,
        defaults={
            "gols_casa": data.gols_casa,
            "gols_fora": data.gols_fora,
        }
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