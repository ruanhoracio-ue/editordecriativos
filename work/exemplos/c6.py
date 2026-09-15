import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from criativo import rodar_formatos as rodar
CFG = dict(
    id="c6", ref="referencias/criativo-6", saida="saidas/criativo-6-v1.mp4",
    titulo=["Demitiu 7 pessoas", "e aumentou o lucro"],
    t_gancho=3.75, t_titulo=7.05, legenda_desde="Brasil",
    gancho=[
        (0.00, 1.00, "startupi-foto.jpg", 0.5, None),
        (1.00, 1.95, "pag3.png", 0.0, (0, 100, 1080, 1060)),
        (1.95, 2.90, "metropoles-terry.jpg", 0.5, None),
        (2.90, 3.75, "pag2.png", 0.0, (0, 330, 1080, 1290)),
    ],
    cutaways=[],
    repl={51: (1, ["pro"]), 54: (2, ["Não", "é", "orçamento,"]), 90: (2, ["follow-up,"]), 112: (2, ["rodando"]),
          128: (2, ["Quanto", "da"]), 150: (1, ["Dá"]), 180: (5, ["de", "ir", "garimpar"]), 214: (1, ["do"]), 255: (1, ["vendas"])},
    frases="""E o que eu vou te contar | de graça | é o que eu tô aprendendo | aqui dentro, | até trocando ideias | com grandes empresários | do mercado digital. | Sabe qual é a diferença | dessa gente | pro empresário comum? | Não é orçamento, | não é equipe grande, | não é sorte, | é velocidade | de implementação.
Enquanto o mercado | ainda tá discutindo | se a IA funciona, | essas pessoas aqui | já colocaram IA | para gerenciar tráfego, | qualificar lead, | para fazer follow-up, | para cortar a ferramenta cara | e para tirar da equipe | tudo que é repetitivo. | Resultado? | Operação mais barata, | faturando mais | rodando 24 horas por dia. | E eu tô aqui exatamente | para levar isso para você.
Quanto da sua equipe | foi embora? | Você falou? | Demitiu em 1 ano? | 7 pessoas. | Quantos por cento? | Tem a metade da empresa? | Dá uns 80%. | E você aumentou o lucro? | Muito. | E por quê? | Olha só, | porque ele implementou IA | na empresa dele.
Porque eu sei | que você não tem também tempo | de ir garimpar | e ver como funciona, | como eu começo do zero, | galera. | Dentro do novo | Conversão Extrema, | na era | da inteligência artificial, | você recebe isso tudo | pronto para implementar, | mesmo começando do zero. | E eu mostrei aqui para ele, | pirou ou não pirou? | Demais.
E aí, então galera, | clica nesse link, | fala com o meu time, | que eu vou te explicar | tudo em detalhes | para você implementar IA | no seu tráfego, | marketing, vendas | e vender muito mais. | Bora? | Bora.""",
    enquadro=lambda t: (1.0, 0.40),
)
rodar(CFG)
