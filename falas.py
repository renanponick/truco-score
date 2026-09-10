# -*- coding: utf-8 -*-
"""
Banco de falas do narrador de truco — 3 personas x 12 eventos x 3 variacoes.

CONVENCAO DE ARQUIVO:  out/<persona>/<evento>_<NN>.mp3
Ex.: out/serio/truco_01.mp3

REGRA DE OURO: o app deve sortear entre as variacoes de um evento.
Repetir a mesma fala toda mao mata a graca em 10 minutos de jogo.

VARIANTE DE REGRA: este banco assume TRUCO PAULISTA
(Truco 3 -> Seis -> Nove -> Doze, sem envido, sem retruco).
Se o app for truco gaucho/mineiro, troque os eventos 'seis_nove_doze'
por 'retruco' e 'vale_quatro' e acrescente 'envido' / 'flor'.
"""

# Nome canonico de cada evento. As 3 personas usam EXATAMENTE os mesmos nomes
# de evento e a mesma terminologia de jogo — nada de "Mao de Ferro" numa
# persona e "Mao Escura" na outra.
EVENTOS = [
    "inicio",
    "mao_de_onze",
    "mao_escura",
    "truco",
    "seis",
    "nove",
    "doze",
    "correu",
    "cangou",
    "mao_vencida",
    "vitoria",
    "derrota",
    "placar_apertado",
]

# Vai para o manifest.json que o dev consome.
EVENTO_DESCRICAO = {
    "inicio":          "Cartas distribuidas, comeco da partida",
    "mao_de_onze":     "Um dos times chega a 11 pontos",
    "mao_escura":      "Ambos em 11 — mao jogada sem ver as cartas",
    "truco":           "Truco pedido (mao vale 3)",
    "seis":            "Aumento para 6",
    "nove":            "Aumento para 9",
    "doze":            "Aumento para 12 (maximo)",
    "correu":          "Jogador recusou o truco",
    "cangou":          "Mao empatada, ninguem pontua",
    "mao_vencida":     "Mao ganha, pontos computados",
    "vitoria":         "Fim de jogo — o jogador venceu",
    "derrota":         "Fim de jogo — o jogador perdeu",
    "placar_apertado": "Placar empatado ou com 1 ponto de diferenca",
}

# Personas que contem linguagem adulta. O app deve deixar estas atras de um
# toggle desligado por padrao — ver README_DEV.md.
PERSONAS_ADULTAS = {"bar"}

FALAS = {
    # ------------------------------------------------------------------
    # PERSONA 1 — SERIO  (voz: Lucas - Deep & Profound Narrator)
    # Estabilidade: Robusto. Poucas tags: a gravidade vem da voz e da pontuacao.
    # ------------------------------------------------------------------
    "serio": {
        "inicio": [
            "As cartas foram distribuídas. Que comece a partida.",
            "Baralho embaralhado. Cada jogador com sua mão.",
            "Começa mais uma partida. Que vença o melhor.",
        ],
        "mao_de_onze": [
            "[serious] Atenção. Mão de Onze em disputa — um ponto decide tudo.",
            "[serious] Mão de Onze. A partir daqui, não há margem para erro.",
            "[serious] Onze pontos. Uma única mão separa os jogadores do fim.",
        ],
        "mao_escura": [
            "[serious] Mão Escura. Nenhum jogador vê as próprias cartas.",
            "[serious] Mão Escura em vigor. Joga-se às cegas.",
            "Mão Escura. Ninguém conhece o que tem em mãos.",
        ],
        "truco": [
            "Truco pedido. Aceitar, correr ou aumentar?",
            "Truco. A mão passa a valer três.",
            "Truco na mesa. A decisão está com o adversário.",
        ],
        "seis": [
            "Seis. A aposta sobe.",
            "Pedido de seis. A mão dobra de valor.",
            "Seis pontos em jogo agora.",
        ],
        "nove": [
            "Nove. A tensão aumenta consideravelmente.",
            "Pedido de nove. Poucos chegam até aqui.",
            "Nove pontos. O recuo já custa caro.",
        ],
        "doze": [
            "[serious] Doze. O máximo. A partida pode terminar aqui.",
            "[serious] Doze pontos em disputa. Tudo ou nada.",
            "[serious] Doze. Não há mais para onde subir.",
        ],
        "correu": [
            "O jogador recusou o truco. Ponto para o adversário.",
            "Correu. Os pontos ficam com quem pediu.",
            "Recusado. A mão se encerra sem disputa.",
        ],
        "cangou": [
            "Mão empatada. Ninguém pontua.",
            "Empate na mão. O placar permanece.",
            "Cangou. Nenhum dos lados leva vantagem.",
        ],
        "mao_vencida": [
            "Mão vencida. Ponto conquistado.",
            "A mão está definida. Pontos computados.",
            "Vitória na mão. O placar se move.",
        ],
        "vitoria": [
            "[serious] Fim de jogo. Vitória conquistada com méritos.",
            "[serious] Encerrada a partida. A vitória é sua.",
            "Doze pontos alcançados. Partida vencida.",
        ],
        "derrota": [
            "Fim de jogo. A vitória ficou com o adversário desta vez.",
            "Partida encerrada. O adversário chegou primeiro.",
            "Derrota nesta partida. Haverá outras.",
        ],
        "placar_apertado": [
            "Placar empatado. Cada ponto agora é decisivo.",
            "Jogo equilibrado. Nenhum dos lados cede.",
            "Placar apertado. A partida se decide nos detalhes.",
        ],
    },

    # ------------------------------------------------------------------
    # PERSONA 2 — COMICO  (voz: Mário - Excited, Constant and Cheerful)
    # Estabilidade: Natural. Tags de emocao fazem o trabalho pesado.
    # ------------------------------------------------------------------
    "comico": {
        "inicio": [
            "[cheerful] Prontos, guerreiros do baralho? Bora ver quem sabe jogar de verdade!",
            "[cheerful] Baralho na mesa! Vamos descobrir quem veio blefar hoje.",
            "[playful] Começou! Que os melhores blefes vençam.",
        ],
        "mao_de_onze": [
            "[playful] Mão de Onze! Agora não dá pra blefar igual estava fazendo até agora, hein?",
            "[excited] Mão de Onze! Aqui separa o jogador do contador de história.",
            "[playful] Onze! Chegou a hora de mostrar serviço, moço.",
        ],
        "mao_escura": [
            "[laughs] Mão Escura! Ninguém enxerga nada, nem o parceiro... boa sorte adivinhando!",
            "[laughs] Mão Escura! Agora é chute com convicção, e olhe lá.",
            "[playful] Mão Escura! Todo mundo cego e fingindo que tem manilha.",
        ],
        "truco": [
            "[laughs] Truco! Ihh, essa doeu — vai encarar ou vai fugir feito lebre?",
            "[excited] Truco! Cadê a coragem que estava sobrando agora há pouco?",
            "[playful] Truco! Vai dizer que não esperava por essa...",
        ],
        "seis": [
            "[playful] Seis! Alguém aqui não sabe quando parar...",
            "[excited] Seis! Subiu a aposta e subiu a pressão junto.",
            "[laughs] Seis! Olha o dedo tremendo aí, ó.",
        ],
        "nove": [
            "[excited] Nove! Isso aqui já virou coisa séria.",
            "[playful] Nove! Alguém tá com muita fé nessa mão, hein.",
            "[laughs] Nove! Ou tem manilha, ou tem cara de pau.",
        ],
        "doze": [
            "[excited] Doze! Cê tava escondendo isso onde, moço?",
            "[laughs] Doze! Vai tudo ou vai nada, não tem meio termo.",
            "[excited] Doze! Agora só sai daqui com a partida decidida.",
        ],
        "correu": [
            "[laughs] Correu do truco! Foi rapidinho, hein, quase nem vi o rastro.",
            "[laughs] Correu! Sabedoria ou covardia? Fica a dúvida.",
            "[playful] Fugiu! Melhor perder um ponto que o orgulho, né...",
        ],
        "cangou": [
            "[playful] Cangou geral! Ninguém levou nada, todo mundo perdendo tempo.",
            "[laughs] Empatou! Tanto barulho pra dar em nada.",
            "[playful] Cangou! Os dois jogaram igual de bem. Ou igual de mal.",
        ],
        "mao_vencida": [
            "[cheerful] Ganhou a mão! Aquele blefe quase não colou, viu...",
            "[excited] Levou a mão! Já pode respirar aliviado.",
            "[playful] Ponto seu! Aproveita que a sorte tá passeando por aqui.",
        ],
        "vitoria": [
            "[excited] E olha quem ganhou! Já pode ir tirando onda por hoje.",
            "[cheerful] Vitória! Guarda esse print, que amanhã ninguém acredita.",
            "[excited] Ganhou! Agora vai lá contar vantagem, você merece.",
        ],
        "derrota": [
            "[playful] Perdeu, perdeu... vai lá chorar no cantinho.",
            "[laughs] Perdeu! Mas foi bonito de assistir, juro.",
            "[playful] Não foi dessa vez. Nem da anterior, aliás.",
        ],
        "placar_apertado": [
            "[playful] Tá osso esse jogo, hein? Ninguém quer ceder nada.",
            "[excited] Olha o placar! Isso aqui vai até o último ponto.",
            "[playful] Empatado! Agora é quem tiver o estômago mais forte.",
        ],
    },

    # ------------------------------------------------------------------
    # PERSONA 3 — BAR  (voz: Otto - Intimidating and Aggressive)
    # Estabilidade: Criativo. Linguagem adulta -> ver nota de classificacao
    # etaria no guia. Mantenha uma versao "leve" se for publicar livre.
    # ------------------------------------------------------------------
    "bar": {
        "inicio": [
            "[shouts] BORA, PORRA! EMBARALHA E JOGA LOGO, CARALHO!",
            "[shouts] SENTA A BUNDA NA CADEIRA E JOGA, VAMBORA!",
            "[shouts] TÁ ESPERANDO O QUÊ?! DISTRIBUI ESSA PORRA!",
        ],
        "mao_de_onze": [
            "[shouts] MÃO DE ONZE, SEUS FRANGOS! AGORA É NA CARA OU NA CORAGEM!",
            "[shouts] ONZE, CARALHO! AQUI NÃO TEM CHORO, TEM DECISÃO!",
            "[shouts] MÃO DE ONZE! QUEM TREMER AGORA VAI OUVIR DE MIM!",
        ],
        "mao_escura": [
            "[shouts] MÃO ESCURA, PORRA! CEGO NEM SABE SE TEM MANILHA, VAI FUNDO!",
            "[shouts] ESCURA! JOGA NO FEELING E REZA, DESGRAÇADO!",
            "[shouts] MÃO ESCURA! NINGUÉM VÊ NADA E TODO MUNDO ACHA QUE GANHA!",
        ],
        "truco": [
            "[shouts] TRUCOOOO! ACEITA OU CORRE LOGO DAÍ, PORRA!",
            "[shouts] TRUCO NA TUA CARA! E AGORA, CAMPEÃO?!",
            "[shouts] TRUCOOO, CARALHO! DECIDE ESSA PORRA!",
        ],
        "seis": [
            "[shouts] SEIS, DESGRAÇADO! TÁ ACHANDO QUE É BRINCADEIRA?!",
            "[shouts] SEIS NA CARA DURA! AGUENTA AGORA!",
            "[shouts] SUBIU PRA SEIS, PORRA! NÃO TEM VOLTA!",
        ],
        "nove": [
            "[shouts] NOVE, CARALHO! ISSO AQUI TÁ PEGANDO FOGO!",
            "[shouts] NOVE! QUEM PISCAR AGORA TÁ MORTO!",
            "[shouts] NOVE, PORRA! COMEÇOU A GUERRA DE VERDADE!",
        ],
        "doze": [
            "[shouts] DOZE, PORRA! TAVA GUARDANDO ESSA PRA QUÊ, CACETA?!",
            "[shouts] DOOOZE! É TUDO OU NADA AGORA, DESGRAÇADO!",
            "[shouts] DOZE NA MESA! ACABOU A PALHAÇADA!",
        ],
        "correu": [
            "[angry] CORREU FEITO GALINHA MOLHADA, SEU FRANGÃO!",
            "[angry] FUGIU, PORRA! NEM ESQUENTOU A CADEIRA!",
            "[angry] CORREU! VAI JOGAR DAMA, VAI!",
        ],
        "cangou": [
            "[shouts] CANGOU, PORRA! NEM UM NEM OUTRO PRESTOU PRA NADA!",
            "[shouts] EMPATOU! DOIS RUINS JOGANDO IGUAL!",
            "[shouts] CANGOU, CARALHO! QUE JOGO MAIS SEM GRAÇA!",
        ],
        "mao_vencida": [
            "[shouts] GANHOU, PORRA! TOMA NA CARA!",
            "[shouts] LEVOU A MÃO, DESGRAÇADO! É ASSIM QUE SE JOGA!",
            "[shouts] PEGOU, CARALHO! MANDOU BEM!",
        ],
        "vitoria": [
            "[triumphant] GANHOOOU, CARALHO! CHORA AGORA!",
            "[triumphant] ACABOU! VITÓRIA, PORRA! TÁ ESCRITO!",
            "[shouts] GANHOU A PARTIDA, DESGRAÇADO! VAI COMEMORAR!",
        ],
        "derrota": [
            "[angry] PERDEU FEIO, HEIN?! VAI TREINAR, CARALHO!",
            "[angry] TOMOU DE LAVADA, PORRA! QUE VERGONHA!",
            "[angry] PERDEU! NEM DEU TRABALHO, DESGRAÇADO!",
        ],
        "placar_apertado": [
            "[shouts] TÁ PEGANDO FOGO, PORRA! NINGUÉM DÁ MOLE AGORA!",
            "[shouts] EMPATADO, CARALHO! AGORA É QUEM TEM MAIS SANGUE!",
            "[shouts] OLHA O PLACAR! ISSO VAI ACABAR EM BRIGA!",
        ],
    },

    # ------------------------------------------------------------------
    # PERSONA 4 — BAR LEVE  (mesma voz e mesma energia do Otto, sem palavrao)
    #
    # Existe por um motivo comercial, nao editorial: com a persona 'bar' no
    # bundle o app vai para 17+ na App Store e 18 na Google Play, mesmo que
    # ela venha desligada. Publicando so com esta, a classificacao abre.
    # A decisao de embarcar as duas ou so esta e de negocio, nao de audio.
    # ------------------------------------------------------------------
    "bar_leve": {
        "inicio": [
            "[shouts] BORA, RAPAZIADA! EMBARALHA E JOGA LOGO!",
            "[shouts] SENTA A BUNDA NA CADEIRA E VAMBORA!",
            "[shouts] TÁ ESPERANDO O QUÊ?! DISTRIBUI ESSAS CARTAS!",
        ],
        "mao_de_onze": [
            "[shouts] MÃO DE ONZE, SEUS FRANGOS! AGORA É NA CARA OU NA CORAGEM!",
            "[shouts] ONZE! AQUI NÃO TEM CHORO, TEM DECISÃO!",
            "[shouts] MÃO DE ONZE! QUEM TREMER AGORA VAI OUVIR DE MIM!",
        ],
        "mao_escura": [
            "[shouts] MÃO ESCURA! CEGO NEM SABE SE TEM MANILHA, VAI FUNDO!",
            "[shouts] ESCURA! JOGA NO FEELING E REZA, RAPAZ!",
            "[shouts] MÃO ESCURA! NINGUÉM VÊ NADA E TODO MUNDO ACHA QUE GANHA!",
        ],
        "truco": [
            "[shouts] TRUCOOOO! ACEITA OU CORRE LOGO DAÍ!",
            "[shouts] TRUCO NA TUA CARA! E AGORA, CAMPEÃO?!",
            "[shouts] TRUCOOO! DECIDE ESSA PARADA!",
        ],
        "seis": [
            "[shouts] SEIS! TÁ ACHANDO QUE É BRINCADEIRA?!",
            "[shouts] SEIS NA CARA DURA! AGUENTA AGORA!",
            "[shouts] SUBIU PRA SEIS! NÃO TEM VOLTA!",
        ],
        "nove": [
            "[shouts] NOVE! ISSO AQUI TÁ PEGANDO FOGO!",
            "[shouts] NOVE! QUEM PISCAR AGORA TÁ FRITO!",
            "[shouts] NOVE! COMEÇOU A GUERRA DE VERDADE!",
        ],
        "doze": [
            "[shouts] DOZE! TAVA GUARDANDO ESSA PRA QUÊ, CARAMBA?!",
            "[shouts] DOOOZE! É TUDO OU NADA AGORA!",
            "[shouts] DOZE NA MESA! ACABOU A PALHAÇADA!",
        ],
        "correu": [
            "[angry] CORREU FEITO GALINHA MOLHADA, SEU FRANGÃO!",
            "[angry] FUGIU! NEM ESQUENTOU A CADEIRA!",
            "[angry] CORREU! VAI JOGAR DAMA, VAI!",
        ],
        "cangou": [
            "[shouts] CANGOU! NEM UM NEM OUTRO PRESTOU PRA NADA!",
            "[shouts] EMPATOU! DOIS RUINS JOGANDO IGUAL!",
            "[shouts] CANGOU! QUE JOGO MAIS SEM GRAÇA!",
        ],
        "mao_vencida": [
            "[shouts] GANHOU! TOMA NA CARA!",
            "[shouts] LEVOU A MÃO! É ASSIM QUE SE JOGA!",
            "[shouts] PEGOU! MANDOU BEM DEMAIS!",
        ],
        "vitoria": [
            "[triumphant] GANHOOOU! CHORA AGORA!",
            "[triumphant] ACABOU! VITÓRIA! TÁ ESCRITO!",
            "[shouts] GANHOU A PARTIDA! VAI COMEMORAR!",
        ],
        "derrota": [
            "[angry] PERDEU FEIO, HEIN?! VAI TREINAR!",
            "[angry] TOMOU DE LAVADA! QUE VERGONHA!",
            "[angry] PERDEU! NEM DEU TRABALHO!",
        ],
        "placar_apertado": [
            "[shouts] TÁ PEGANDO FOGO! NINGUÉM DÁ MOLE AGORA!",
            "[shouts] EMPATADO! AGORA É QUEM TEM MAIS SANGUE!",
            "[shouts] OLHA O PLACAR! ISSO VAI ACABAR EM BRIGA!",
        ],
    },
}
