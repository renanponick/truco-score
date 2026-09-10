# truco-score

Placar de truco paulista com narrador. Uma página só (`index.html`), sem build
e sem dependência: abre no celular, guarda tudo no `localStorage` e funciona
offline.

## Rodar

Os clipes do narrador são carregados de `audios/`. Abrir o `index.html` direto
do disco funciona (há um mapa de clipes embutido como fallback), mas o jeito
recomendado é servir a pasta, porque aí o `audios/manifest.json` é lido de
verdade e o navegador cacheia os áudios:

    python3 -m http.server 8000
    # http://localhost:8000

## Narrador

Quatro estilos, trocáveis a qualquer momento na barra abaixo do placar —
inclusive no meio da partida:

| chip      | pasta       | voz                                    |
|-----------|-------------|----------------------------------------|
| Sério     | `serio/`    | Lucas — narrador grave                 |
| Cômico    | `comico/`   | Mário — animado, deboche leve          |
| Bar       | `bar_leve/` | Otto — gritado, sem palavrão           |
| Bar 18+   | `bar/`      | Otto — gritado, **linguagem adulta**   |

O Bar 18+ pede confirmação na primeira vez. O 🔊 à esquerda muda o narrador
sem perder o estilo escolhido. Volume e "qual é o seu time" (define de quem é
a `vitoria` e de quem é a `derrota`) ficam em ⚙ → Narrador.

### Quando cada fala dispara

| evento            | gatilho na tela                                         |
|-------------------|---------------------------------------------------------|
| `inicio`          | "Nova partida"                                          |
| `truco`/`seis`/`nove`/`doze` | chip de valor da mão                         |
| `mao_vencida`     | "Ganhou a mão"                                          |
| `correu`          | "Correu · <time>" — quem correu é o time apontado       |
| `cangou`          | "Cangou"                                                |
| `mao_de_onze`     | um time chega a 11 (uma vez por partida, por time)      |
| `mao_escura`      | os dois em 11                                           |
| `placar_apertado` | diferença ≤ 1 com alguém em 6+, de vez em quando        |
| `vitoria`/`derrota` | alguém fecha em 12                                    |

Cada evento tem 3 variações e o app sorteia sem repetir a última — um "Truco!"
idêntico toda mão faz o usuário desligar o som na primeira meia hora.

Falas situacionais entram na fila depois do resultado da mão (no máximo duas
enfileiradas). Um aumento de aposta corta o que estiver tocando: o momento é o
pedido, não o comentário anterior.

## Regerar os áudios

Falas em `falas.py`, geração (ElevenLabs) em `gerar_audios.py`:

    export ELEVENLABS_API_KEY="sk_..."
    python3 gerar_audios.py --teste          # 1 clipe por persona, ~200 créditos
    python3 gerar_audios.py                  # gera o que falta em out/
    python3 gerar_audios.py --dry-run        # só o custo

Para trocar uma fala: edite o texto, apague o `.mp3` correspondente e rode de
novo — só o apagado é refeito. Depois de copiar os clipes bons para `audios/`,
atualize o manifesto que a página consome:

    python3 gerar_audios.py --manifesto --out audios

## Classificação etária

A pasta `bar/` tem palavrão pesado. Se ela for junto num app de loja, a
classificação vai para 17+ (App Store) e 18 (Google Play) mesmo vindo desligada
— as lojas classificam pelo conteúdo presente, não pelo ativado. Publicando só
com `bar_leve/`, a classificação abre. Como web app isso não se aplica.
