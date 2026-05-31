from ninja import Router
from typing import List
from ninja import Schema
from core.models import Partida, Palpite, Grupo, Fase, Time
from core.jwt_utils import obter_usuario_request
from django.db.models import Sum, Count
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

router = Router()


def vencedor_partida(partida):
    if partida.gols_casa is None or partida.gols_fora is None:
        return None

    if partida.gols_casa > partida.gols_fora:
        return partida.time_casa

    if partida.gols_fora > partida.gols_casa:
        return partida.time_fora

    return None  # empate no mata-mata precisa de pênaltis futuramente

CHAVEAMENTO_MATA_MATA = {
    # Oitavas
    89: (73, 74),
    90: (75, 76),
    91: (77, 78),
    92: (79, 80),
    93: (81, 82),
    94: (83, 84),
    95: (85, 86),
    96: (87, 88),

    # Quartas
    97: (89, 90),
    98: (91, 92),
    99: (93, 94),
    100: (95, 96),

    # Semifinais
    101: (97, 98),
    102: (99, 100),

    # Final e terceiro lugar
    103: (101, 102),  # perdedores
    104: (101, 102),  # vencedores
}

def atualizar_chaveamento_mata_mata():
    for numero_destino, (jogo_origem_1, jogo_origem_2) in CHAVEAMENTO_MATA_MATA.items():
        try:
            partida_destino = Partida.objects.get(numero_jogo=numero_destino)
            origem_1 = Partida.objects.get(numero_jogo=jogo_origem_1)
            origem_2 = Partida.objects.get(numero_jogo=jogo_origem_2)
        except Partida.DoesNotExist:
            continue

        vencedor_1 = vencedor_partida(origem_1)
        vencedor_2 = vencedor_partida(origem_2)

        if numero_destino == 103:
            # Disputa do 3º lugar ainda será tratada depois com perdedores
            continue

        partida_destino.time_casa = vencedor_1 if vencedor_1 else partida_destino.time_casa
        partida_destino.time_fora = vencedor_2 if vencedor_2 else partida_destino.time_fora

        partida_destino.save(update_fields=["time_casa", "time_fora"])

class PalpiteSchema(Schema):
    partida_id: int
    gols_casa: int
    gols_fora: int


class ClassificadoManualSchema(Schema):
    numero_jogo: int
    lado: str  # "casa" ou "fora"
    time_id: int

class DefinirClassificadoManualSchema(Schema):
    numero_jogo: int
    lado: str
    time_id: int

@router.post("/classificado-manual")
def definir_classificado_manual(request, data: ClassificadoManualSchema):
    usuario = obter_usuario_request(request)

    if usuario is None:
        return {
            "success": False,
            "message": "Você precisa estar logado."
        }

    if not usuario.is_staff and not usuario.is_superuser:
        return {
            "success": False,
            "message": "Você não tem permissão para definir classificados."
        }

    partida = Partida.objects.get(numero_jogo=data.numero_jogo)
    time = Time.objects.get(id=data.time_id)

    if data.lado == "casa":
        partida.time_casa = time
    elif data.lado == "fora":
        partida.time_fora = time
    else:
        return {
            "success": False,
            "message": "Lado inválido. Use 'casa' ou 'fora'."
        }

    partida.save(update_fields=["time_casa", "time_fora"])

    return {
        "success": True,
        "message": f"{time.nome} definido manualmente no jogo {partida.numero_jogo}."
    }

def estatisticas_confronto_direto(grupo, times_ids):
    partidas = Partida.objects.filter(
        grupo=grupo,
        time_casa_id__in=times_ids,
        time_fora_id__in=times_ids,
        gols_casa__isnull=False,
        gols_fora__isnull=False,
    )

    tabela = {
        time_id: {
            "pontos": 0,
            "saldo": 0,
            "gols_pro": 0,
        }
        for time_id in times_ids
    }

    for partida in partidas:
        casa = tabela[partida.time_casa_id]
        fora = tabela[partida.time_fora_id]

        casa["gols_pro"] += partida.gols_casa
        fora["gols_pro"] += partida.gols_fora

        casa["saldo"] += partida.gols_casa - partida.gols_fora
        fora["saldo"] += partida.gols_fora - partida.gols_casa

        if partida.gols_casa > partida.gols_fora:
            casa["pontos"] += 3
        elif partida.gols_fora > partida.gols_casa:
            fora["pontos"] += 3
        else:
            casa["pontos"] += 1
            fora["pontos"] += 1

    return tabela

def ordenar_classificacao_fifa(grupo, tabela):
    classificacao = list(tabela.values())

    classificacao.sort(
        key=lambda x: (
            -x["pontos"],
            -x["saldo"],
            -x["gols_pro"],
            x["time"],
        )
    )

    resultado = []
    i = 0

    while i < len(classificacao):
        atual = classificacao[i]

        empatados = [atual]
        j = i + 1

        while j < len(classificacao):
            proximo = classificacao[j]

            mesmo_empate = (
                proximo["pontos"] == atual["pontos"]
                and proximo["saldo"] == atual["saldo"]
                and proximo["gols_pro"] == atual["gols_pro"]
            )

            if not mesmo_empate:
                break

            empatados.append(proximo)
            j += 1

        if len(empatados) == 1:
            resultado.extend(empatados)
        else:
            ids = [time["time_obj"].id for time in empatados]
            confronto = estatisticas_confronto_direto(grupo, ids)

            empatados.sort(
                key=lambda x: (
                    -confronto[x["time_obj"].id]["pontos"],
                    -confronto[x["time_obj"].id]["saldo"],
                    -confronto[x["time_obj"].id]["gols_pro"],
                    x["time"],
                )
            )

            resultado.extend(empatados)

        i = j

    return resultado

def calcular_classificacao_grupo_obj(grupo):
    partidas = Partida.objects.select_related(
        "time_casa",
        "time_fora"
    ).filter(grupo=grupo)

    tabela = {}

    def garantir_time(time):
        if time and time.id not in tabela:
            tabela[time.id] = {
                "time_obj": time,
                "time": time.nome,
                "pontos": 0,
                "jogos": 0,
                "vitorias": 0,
                "empates": 0,
                "derrotas": 0,
                "gols_pro": 0,
                "gols_contra": 0,
                "saldo": 0,
            }

    for partida in partidas:
        garantir_time(partida.time_casa)
        garantir_time(partida.time_fora)

        if partida.gols_casa is None or partida.gols_fora is None:
            continue

        casa = tabela[partida.time_casa.id]
        fora = tabela[partida.time_fora.id]

        casa["jogos"] += 1
        fora["jogos"] += 1

        casa["gols_pro"] += partida.gols_casa
        casa["gols_contra"] += partida.gols_fora
        fora["gols_pro"] += partida.gols_fora
        fora["gols_contra"] += partida.gols_casa

        if partida.gols_casa > partida.gols_fora:
            casa["pontos"] += 3
            casa["vitorias"] += 1
            fora["derrotas"] += 1
        elif partida.gols_casa < partida.gols_fora:
            fora["pontos"] += 3
            fora["vitorias"] += 1
            casa["derrotas"] += 1
        else:
            casa["pontos"] += 1
            fora["pontos"] += 1
            casa["empates"] += 1
            fora["empates"] += 1

    for item in tabela.values():
        item["saldo"] = item["gols_pro"] - item["gols_contra"]

    classificacao = list(tabela.values())

    grupos_empatados = {}

    for item in classificacao:
        chave = (
            item["pontos"],
            item["saldo"],
            item["gols_pro"],
        )

        grupos_empatados.setdefault(chave, []).append(item)

    resultado = []

    for grupo_empate in grupos_empatados.values():

        if len(grupo_empate) == 1:
            resultado.extend(grupo_empate)
            continue

        ids = [x["time_obj"].id for x in grupo_empate]

        confronto = estatisticas_confronto_direto(grupo, ids)

        grupo_empate.sort(
            key=lambda x: (
                -confronto[x["time_obj"].id]["pontos"],
                -confronto[x["time_obj"].id]["saldo"],
                -confronto[x["time_obj"].id]["gols_pro"],
                x["time"],
            )
        )

        resultado.extend(grupo_empate)

    return ordenar_classificacao_fifa(grupo, tabela)


def chave_classificacao(item):
    return (
        item["pontos"],
        item["saldo"],
        item["gols_pro"],
    )


def posicao_sem_empate(classificacao, indice):
    if indice >= len(classificacao):
        return None

    atual = classificacao[indice]

    if atual["jogos"] == 0:
        return None

    if indice > 0 and chave_classificacao(atual) == chave_classificacao(classificacao[indice - 1]):
        return None

    if indice < len(classificacao) - 1 and chave_classificacao(atual) == chave_classificacao(classificacao[indice + 1]):
        return None

    return atual

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
    if partida.time_casa is None or partida.time_fora is None:
        return {
            "success": False,
            "message": "Esta partida ainda não possui times definidos."
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
            "time_casa": p.time_casa.nome if p.time_casa else "A definir",
            "time_fora": p.time_fora.nome if p.time_fora else "A definir",
            "time_casa_bandeira": request.build_absolute_uri(
                p.time_casa.bandeira.url) if p.time_casa and p.time_casa.bandeira else None,
            "time_fora_bandeira": request.build_absolute_uri(
                p.time_fora.bandeira.url) if p.time_fora and p.time_fora.bandeira else None,
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

    atualizar_chaveamento_mata_mata()

    return {
        "success": True,
        "message": "Resultado oficial salvo, pontos recalculados e chaveamento atualizado."
    }

@router.get("/perfil")
def perfil(request):
    usuario = obter_usuario_request(request)

    if usuario is None:
        return {
            "success": False,
            "message": "Você precisa estar logado."
        }

    palpites = Palpite.objects.filter(usuario=usuario)

    total_palpites = palpites.count()
    total_pontos = sum(p.pontos for p in palpites)
    placares_exatos = palpites.filter(placar_exato=True).count()
    vencedores_corretos = palpites.filter(vencedor_correto=True).count()

    taxa_acerto = 0
    if total_palpites > 0:
        taxa_acerto = round((vencedores_corretos / total_palpites) * 100, 1)

    return {
        "success": True,
        "perfil": {
            "email": usuario.email,
            "pontos": total_pontos,
            "palpites": total_palpites,
            "placares_exatos": placares_exatos,
            "vencedores_corretos": vencedores_corretos,
            "taxa_acerto": taxa_acerto,
        }
    }

@router.get("/classificacao-grupo/{grupo_nome}")
def classificacao_grupo(request, grupo_nome: str):
    grupo_obj = Grupo.objects.get(nome=grupo_nome)
    partidas = Partida.objects.select_related(
        "grupo", "time_casa", "time_fora"
    ).filter(
        grupo=grupo_obj
    )

    tabela = {}

    def garantir_time(time):
        if time.id not in tabela:
            tabela[time.id] = {
                "time_obj": time,
                "time": time.nome,
                "pontos": 0,
                "jogos": 0,
                "vitorias": 0,
                "empates": 0,
                "derrotas": 0,
                "gols_pro": 0,
                "gols_contra": 0,
                "saldo": 0,
            }

    for partida in partidas:
        garantir_time(partida.time_casa)
        garantir_time(partida.time_fora)

        if partida.gols_casa is None or partida.gols_fora is None:
            continue

        casa = tabela[partida.time_casa.id]
        fora = tabela[partida.time_fora.id]

        casa["jogos"] += 1
        fora["jogos"] += 1

        casa["gols_pro"] += partida.gols_casa
        casa["gols_contra"] += partida.gols_fora

        fora["gols_pro"] += partida.gols_fora
        fora["gols_contra"] += partida.gols_casa

        if partida.gols_casa > partida.gols_fora:
            casa["pontos"] += 3
            casa["vitorias"] += 1
            fora["derrotas"] += 1
        elif partida.gols_casa < partida.gols_fora:
            fora["pontos"] += 3
            fora["vitorias"] += 1
            casa["derrotas"] += 1
        else:
            casa["pontos"] += 1
            fora["pontos"] += 1
            casa["empates"] += 1
            fora["empates"] += 1

    for item in tabela.values():
        item["saldo"] = item["gols_pro"] - item["gols_contra"]

    classificacao = ordenar_classificacao_fifa(grupo=grupo_obj, tabela=tabela)

    return {
        "success": True,
        "grupo": grupo_nome,
        "classificacao": [
            {
                "posicao": index + 1,
                "time": item["time"],
                "pontos": item["pontos"],
                "jogos": item["jogos"],
                "vitorias": item["vitorias"],
                "empates": item["empates"],
                "derrotas": item["derrotas"],
                "gols_pro": item["gols_pro"],
                "gols_contra": item["gols_contra"],
                "saldo": item["saldo"],
            }
            for index, item in enumerate(classificacao)
        ]
    }

@router.post("/gerar-16-avos")
def gerar_16_avos(request):
    usuario = obter_usuario_request(request)

    if usuario is None:
        return {
            "success": False,
            "message": "Você precisa estar logado."
        }

    if not usuario.is_staff and not usuario.is_superuser:
        return {
            "success": False,
            "message": "Você não tem permissão para gerar o mata-mata."
        }

    fase_16 = Fase.objects.get(nome="16 Avos de Final")

    posicoes = {}
    terceiros = []

    grupos = Grupo.objects.all().order_by("nome")

    for grupo in grupos:
        letra = grupo.nome.replace("Grupo ", "").strip()
        classificacao = calcular_classificacao_grupo_obj(grupo)

        primeiro = posicao_sem_empate(classificacao, 0)
        segundo = posicao_sem_empate(classificacao, 1)
        terceiro = posicao_sem_empate(classificacao, 2)

        if primeiro:
            posicoes[f"1{letra}"] = primeiro

        if segundo:
            posicoes[f"2{letra}"] = segundo

        if terceiro:
            terceiro["grupo_letra"] = letra
            terceiros.append(terceiro)

    terceiros = sorted(
        terceiros,
        key=lambda x: (
            -x["pontos"],
            -x["saldo"],
            -x["gols_pro"],
            x["time"],
        )
    )[:8]

    jogos_16_avos = [
        (73, "2A", "2B"),
        (74, "1E", "3:A/B/C/D/F"),
        (75, "1F", "2C"),
        (76, "1C", "2F"),
        (77, "1I", "3:C/D/F/G/H"),
        (78, "2E", "2I"),
        (79, "1A", "3:C/E/F/H/I"),
        (80, "1L", "3:E/H/I/J/K"),
        (81, "1D", "3:B/E/F/I/J"),
        (82, "1G", "3:A/E/H/I/J"),
        (83, "2K", "2L"),
        (84, "1H", "2J"),
        (85, "1B", "3:E/F/G/I/J"),
        (86, "1J", "2H"),
        (87, "1K", "3:D/E/I/J/L"),
        (88, "2D", "2G"),
    ]

    terceiros_usados = set()
    jogos_atualizados = []
    jogos_pendentes = []

    def resolver_vaga(vaga):
        if vaga.startswith("1") or vaga.startswith("2"):
            return posicoes.get(vaga)

        if vaga.startswith("3:"):
            grupos_permitidos = vaga.replace("3:", "").split("/")

            for terceiro in terceiros:
                if (
                    terceiro["grupo_letra"] in grupos_permitidos
                    and terceiro["time_obj"].id not in terceiros_usados
                ):
                    terceiros_usados.add(terceiro["time_obj"].id)
                    return terceiro

        return None

    for numero_jogo, vaga_casa, vaga_fora in jogos_16_avos:
        time_casa_info = resolver_vaga(vaga_casa)
        time_fora_info = resolver_vaga(vaga_fora)

        partida = Partida.objects.get(
            fase=fase_16,
            numero_jogo=numero_jogo
        )

        partida.time_casa = time_casa_info["time_obj"] if time_casa_info else None
        partida.time_fora = time_fora_info["time_obj"] if time_fora_info else None
        partida.save(update_fields=["time_casa", "time_fora"])

        item_retorno = {
            "numero_jogo": numero_jogo,
            "vaga_casa": vaga_casa,
            "vaga_fora": vaga_fora,
            "time_casa": partida.time_casa.nome if partida.time_casa else "A definir",
            "time_fora": partida.time_fora.nome if partida.time_fora else "A definir",
        }

        if time_casa_info and time_fora_info:
            jogos_atualizados.append(item_retorno)
        else:
            jogos_pendentes.append(item_retorno)

    return {
        "success": True,
        "message": (
            f"Simulação dos 16 Avos atualizada. "
            f"{len(jogos_atualizados)} jogos completos e "
            f"{len(jogos_pendentes)} jogos aguardando adversário."
        ),
        "jogos_atualizados": jogos_atualizados,
        "jogos_pendentes": jogos_pendentes,
    }

@router.get("/times")
def listar_times(request):

    times = Time.objects.order_by("nome")

    return {
        "success": True,
        "times": [
            {
                "id": t.id,
                "nome": t.nome,
                "sigla": t.sigla,
                "bandeira": (
                    request.build_absolute_uri(t.bandeira.url)
                    if t.bandeira else None
                ),
            }
            for t in times
        ]
    }

@router.post("/classificado-manual")
def classificado_manual(
    request,
    data: DefinirClassificadoManualSchema
):
    usuario = obter_usuario_request(request)

    if not usuario.is_staff and not usuario.is_superuser:
        return {
            "success": False,
            "message": "Sem permissão."
        }

    try:
        partida = Partida.objects.get(
            numero_jogo=data.numero_jogo
        )

        time = Time.objects.get(
            id=data.time_id
        )

        if data.lado == "casa":
            partida.time_casa = time

        elif data.lado == "fora":
            partida.time_fora = time

        else:
            return {
                "success": False,
                "message": "Lado inválido."
            }

        partida.save()

        return {
            "success": True,
            "message": "Classificado definido."
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }