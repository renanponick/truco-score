#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera e empacota os clipes do narrador de truco (ElevenLabs, modelo Eleven v3).

    export ELEVENLABS_API_KEY="sk_..."
    pip install requests

    python gerar_audios.py --dry-run          # lista o que faria + custo
    python gerar_audios.py                    # gera tudo que falta
    python gerar_audios.py --persona bar      # regera uma persona
    python gerar_audios.py --evento truco     # um evento em todas as personas
    python gerar_audios.py --force            # regera por cima

    python gerar_audios.py --empacotar        # manifest.json + README + .zip

    # so o manifest.json, sobre uma pasta ja pronta (o que o placar web consome)
    python gerar_audios.py --manifesto --out audios

CICLO DE TRABALHO
    1. gerar tudo
    2. ouvir a pasta out/
    3. APAGAR os .mp3 que ficaram ruins
    4. rodar de novo — so os apagados sao refeitos
    5. --empacotar quando estiver satisfeito
"""

import argparse
import datetime as dt
import json
import os
import sys
import time
import zipfile
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("Falta a lib requests.  ->  pip install requests")

from falas import FALAS, EVENTOS, EVENTO_DESCRICAO, PERSONAS_ADULTAS

API = "https://api.elevenlabs.io/v1/text-to-speech"
MODEL = "eleven_v3"
VARIANTE_REGRAS = "paulista"

# ---------------------------------------------------------------------------
# stability: use 0.0 / 0.5 / 1.0 — os tres pontos que a interface do v3 expoe
# como Criativo / Natural / Robusto. Valores intermediarios podem ser
# rejeitados pela API no v3; estes tres sempre funcionam.
#
#   0.0 Criativo -> maxima expressividade e resposta a tags; pode alucinar
#   0.5 Natural  -> mais proximo da gravacao original da voz
#   1.0 Robusto  -> consistencia entre clipes; responde menos a tags
# ---------------------------------------------------------------------------
PERSONAS = {
    "serio": {
        "rotulo": "Sério",
        "voz": "Lucas - Deep & Profound Narrator",
        "voice_id": "GIuLCSVfgJaUuh7hYOY8",
        "stability": 1.0,
        "seed": 101,
    },
    "comico": {
        "rotulo": "Cômico",
        "voz": "Mário - Excited, Constant and Cheerful",
        "voice_id": "YU8EsJtXFMyKMxYtheDk",
        "stability": 0.5,
        "seed": 202,
    },
    "bar": {
        "rotulo": "Bar",
        "voz": "Otto - Intimidating and Aggressive",
        "voice_id": "ycxdm1PRMs962FxyyuJ0",
        "stability": 0.0,
        "seed": 303,
    },
    "bar_leve": {
        "rotulo": "Bar (linguagem livre)",
        "voz": "Otto - Intimidating and Aggressive",
        "voice_id": "ycxdm1PRMs962FxyyuJ0",
        "stability": 0.0,
        "seed": 404,
    },
}

# mp3_22050_32 corta o bundle em ~4x e e indistinguivel num efeito de meio
# segundo saindo do alto-falante de celular. Troque para mp3_44100_128 se for
# usar os audios em video ou material de marketing.
OUTPUT_FORMAT = "mp3_22050_32"

OUT = Path("out")
DIST = Path("dist")


# ---------------------------------------------------------------------------
# geracao
# ---------------------------------------------------------------------------
def gerar(api_key, persona, evento, idx, texto, cfg, force=False):
    destino = OUT / persona / f"{evento}_{idx:02d}.mp3"
    destino.parent.mkdir(parents=True, exist_ok=True)

    if destino.exists() and not force:
        return "pulado", destino, 0

    payload = {
        "text": texto,
        "model_id": MODEL,
        "language_code": "pt",
        "voice_settings": {"stability": cfg["stability"]},
        # seed fixa por persona = mesma pegada entre os clipes dela.
        "seed": cfg["seed"] + idx,
    }

    try:
        r = requests.post(
            f"{API}/{cfg['voice_id']}?output_format={OUTPUT_FORMAT}",
            headers={"xi-api-key": api_key, "Content-Type": "application/json"},
            json=payload,
            timeout=120,
        )
    except requests.RequestException as e:
        return f"ERRO de rede: {e}", destino, 0

    if r.status_code == 401:
        return ("ERRO 401: chave invalida ou sem permissao de Text to Speech. "
                "Confira o escopo da chave em Desenvolvedores > Chaves de API."), destino, 0
    if r.status_code == 404:
        return (f"ERRO 404: voice_id {cfg['voice_id']} nao acessivel nesta conta. "
                "Adicione a voz em Vozes > Explorar > (tres pontinhos) > "
                "Adicionar as minhas vozes."), destino, 0
    if r.status_code != 200:
        return f"ERRO {r.status_code}: {r.text[:200]}", destino, 0

    destino.write_bytes(r.content)
    return "ok", destino, len(texto)


def testar(api_key):
    """Gera um clipe curto por persona antes da rodada completa.

    Custa ~200 creditos e responde as duas perguntas que fazem a rodada de
    7.727 creditos falhar: a chave tem escopo certo, e as quatro vozes estao
    acessiveis nesta conta.
    """
    print("Teste de conexao — 1 clipe por persona\n")
    ok = True
    for persona, cfg in PERSONAS.items():
        texto = FALAS[persona]["truco"][0]
        status, destino, _ = gerar(
            api_key, "_teste", persona, 1, texto, cfg, force=True
        )
        if status == "ok":
            kb = destino.stat().st_size / 1024
            print(f"  ok  {cfg['rotulo']:24s} {kb:5.1f} KB  -> {destino}")
        else:
            ok = False
            print(f"  XX  {cfg['rotulo']:24s} {status}")
        time.sleep(0.4)

    print()
    if ok:
        print("Tudo certo. Ouca os 4 arquivos em out/_teste/ e, se gostou,")
        print("rode:  python gerar_audios.py")
    else:
        print("Corrija os erros acima antes de rodar a geracao completa.")
    return ok


# ---------------------------------------------------------------------------
# empacotamento
# ---------------------------------------------------------------------------
def montar_manifesto():
    """Contrato que o dev consome. Lista so o que existe em disco."""
    manifesto = {
        "pacote": "narrador-truco",
        "versao": "1.0",
        "gerado_em": dt.date.today().isoformat(),
        "variante_regras": VARIANTE_REGRAS,
        "formato_audio": OUTPUT_FORMAT,
        "modelo": MODEL,
        "regras_de_uso": {
            "sorteio": "Cada evento tem varias variacoes. Sorteie uma a cada disparo.",
            "nao_repetir": "Nunca toque a mesma variacao duas vezes seguidas no mesmo evento.",
            "persona_unica_por_sessao": "A persona e escolhida pelo usuario e nao muda no meio da partida.",
            "vocabulario": "Os nomes de evento sao identicos entre personas. Trocar de narrador e trocar de pasta.",
        },
        "personas": {},
        "eventos": {},
    }

    for persona, cfg in PERSONAS.items():
        if not (OUT / persona).exists():
            continue
        manifesto["personas"][persona] = {
            "rotulo": cfg["rotulo"],
            "voz": cfg["voz"],
            "voice_id": cfg["voice_id"],
            "estabilidade": cfg["stability"],
            "linguagem_adulta": persona in PERSONAS_ADULTAS,
        }

    for evento in EVENTOS:
        clipes = {}
        for persona in manifesto["personas"]:
            arquivos = sorted(
                f"{persona}/{p.name}" for p in (OUT / persona).glob(f"{evento}_*.mp3")
            )
            if arquivos:
                clipes[persona] = arquivos
        if clipes:
            manifesto["eventos"][evento] = {
                "descricao": EVENTO_DESCRICAO.get(evento, ""),
                "clipes": clipes,
            }

    return manifesto


README_DEV = """# Pacote de voz — Narrador de Truco

Audio pre-gerado para o marcador. Nada aqui chama API em runtime:
sao arquivos estaticos, tocados localmente. Sem latencia, sem custo por
partida, funciona offline.

## Estrutura

    manifest.json
    serio/       inicio_01.mp3, truco_01.mp3, ...
    comico/      ...
    bar/         ...          <- LINGUAGEM ADULTA
    bar_leve/    ...          <- mesma energia, sem palavrao

## Como integrar

Leia `manifest.json`. Ele mapeia evento -> lista de arquivos por persona:

    manifest.eventos["truco"].clipes["comico"]
      -> ["comico/truco_01.mp3", "comico/truco_02.mp3", "comico/truco_03.mp3"]

No disparo de um evento, **sorteie** uma das variacoes e **nunca repita
a ultima tocada daquele evento**. Isso nao e detalhe de polimento: uma
partida de truco tem dezenas de maos, e um "Truco!" identico toda vez faz
o usuario desligar o som — e ai o pacote inteiro foi perdido.

Sugestao de implementacao:

    ultimo = {}  # evento -> indice tocado por ultimo

    def tocar(evento, persona):
        opcoes = manifest["eventos"][evento]["clipes"][persona]
        if len(opcoes) > 1 and evento in ultimo:
            opcoes = [o for o in opcoes if o != ultimo[evento]]
        escolhido = random.choice(opcoes)
        ultimo[evento] = escolhido
        player.play(escolhido)

## Classificacao etaria — ler antes de embarcar

A pasta `bar/` tem palavrao pesado. Se ela entrar no bundle, o app vai para
**17+ na App Store** e **18 na Google Play**, mesmo vindo desligada por
padrao — as lojas classificam pelo conteudo presente, nao pelo ativado.

Duas opcoes:

- **Publicar so com `bar_leve/`** — classificacao aberta, publico maior.
- **Embarcar as duas** — assumir 17+/18, com a `bar/` atras de um toggle
  "linguagem adulta" desligado por padrao.

A decisao e de negocio. Confirme com o Rafael antes de fechar o bundle.

## Eventos

Os nomes de evento sao iguais nas quatro personas. Trocar de narrador e
trocar a pasta, nada mais. Variante de regras: **truco paulista**
(Truco 3 -> Seis -> Nove -> Doze, sem envido, sem flor).

Se o app passar a suportar truco gaucho, os eventos `seis`/`nove`/`doze`
precisam virar `retruco`/`vale_quatro` e entram `envido` e `flor` — sao
audios novos, nao renomeacao.

## Regerar ou ajustar

Falas em `falas.py`, geracao em `gerar_audios.py`. Para trocar uma fala:
edite o texto, apague o `.mp3` correspondente, rode `python gerar_audios.py`.
So o arquivo apagado e refeito.
"""


def escrever_manifesto():
    """So o manifest.json, sem zip. E o arquivo que o index.html le."""
    if not OUT.exists() or not any(OUT.rglob("*.mp3")):
        sys.exit(f"Nada em {OUT}/. Rode a geracao primeiro.")

    manifesto = montar_manifesto()
    destino = OUT / "manifest.json"
    destino.write_text(
        json.dumps(manifesto, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    n_audio = len(list(OUT.rglob("*.mp3")))
    print(f"  {destino}")
    print(f"  {n_audio} clipes · {len(manifesto['personas'])} personas · "
          f"{len(manifesto['eventos'])} eventos")
    return destino


def empacotar():
    if not OUT.exists() or not any(OUT.rglob("*.mp3")):
        sys.exit("Nada em out/. Rode a geracao primeiro.")

    DIST.mkdir(exist_ok=True)
    manifesto = montar_manifesto()

    (OUT / "manifest.json").write_text(
        json.dumps(manifesto, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / "README_DEV.md").write_text(README_DEV, encoding="utf-8")

    zip_path = DIST / f"narrador-truco-v{manifesto['versao']}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for arq in sorted(OUT.rglob("*")):
            if arq.is_file():
                z.write(arq, arq.relative_to(OUT))

    n_audio = len(list(OUT.rglob("*.mp3")))
    tamanho = zip_path.stat().st_size / 1_048_576

    print(f"\n{'-'*60}")
    print(f"  {zip_path}")
    print(f"  {n_audio} clipes · {len(manifesto['personas'])} personas · "
          f"{len(manifesto['eventos'])} eventos · {tamanho:.1f} MB")
    print(f"\n  Manda esse zip para o dev. O README_DEV.md dentro dele")
    print(f"  explica a integracao e a questao de classificacao etaria.")
    return zip_path


# ---------------------------------------------------------------------------
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--persona", choices=list(PERSONAS))
    p.add_argument("--evento")
    p.add_argument("--force", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--teste", action="store_true")
    p.add_argument("--empacotar", action="store_true")
    p.add_argument("--manifesto", action="store_true")
    p.add_argument("--out", default="out",
                   help="pasta dos clipes (padrao: out). O placar web usa audios/.")
    args = p.parse_args()

    global OUT
    OUT = Path(args.out)

    if args.manifesto:
        escrever_manifesto()
        return

    if args.empacotar:
        empacotar()
        return

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key and not args.dry_run:
        sys.exit(
            "Defina ELEVENLABS_API_KEY no ambiente:\n"
            '  export ELEVENLABS_API_KEY="sk_..."'
        )

    if args.teste:
        sys.exit(0 if testar(api_key) else 1)

    personas = [args.persona] if args.persona else list(PERSONAS)
    total_chars = feitos = erros = 0

    for persona in personas:
        cfg = PERSONAS[persona]
        eventos = FALAS[persona]
        alvos = [args.evento] if args.evento else list(eventos)

        print(f"\n=== {cfg['rotulo'].upper()}  "
              f"(stability={cfg['stability']}, voz={cfg['voz']})")

        for evento in alvos:
            if evento not in eventos:
                print(f"  ! evento '{evento}' nao existe em {persona}")
                continue

            for idx, texto in enumerate(eventos[evento], start=1):
                if args.dry_run:
                    print(f"  [dry] {persona}/{evento}_{idx:02d}.mp3  ({len(texto)} chars)")
                    total_chars += len(texto)
                    continue

                status, destino, n = gerar(
                    api_key, persona, evento, idx, texto, cfg, args.force
                )
                total_chars += n

                if status == "ok":
                    feitos += 1
                    print(f"  ok  {destino}")
                elif status == "pulado":
                    print(f"  --  {destino} (ja existe)")
                else:
                    erros += 1
                    print(f"  XX  {destino}  {status}")

                time.sleep(0.4)

    print(f"\n{'-'*60}")
    if args.dry_run:
        print(f"Geraria {total_chars} caracteres  ~= {total_chars} creditos.")
    else:
        print(f"Gerados: {feitos}   Erros: {erros}   "
              f"Caracteres: {total_chars} (~= mesmo tanto de creditos)")
        print("\nOuca a pasta out/. Apague o que ficou ruim e rode de novo —")
        print("so os apagados sao refeitos. Depois: --empacotar")


if __name__ == "__main__":
    main()
