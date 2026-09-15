import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from criativo import rodar_formatos as rodar
CFG = dict(
    id="c1", ref="referencias/criativo-1", saida="saidas/criativo-1-v1.mp4",
    titulo=["500 empresários pararam", "2 dias pra aprender IA"],
    t_gancho=4.45, t_titulo=10.30, legenda_desde="vivo",
    gancho=[
        (0.00, 1.20, "mdc-site.png", 0.0, (0, 0, 1080, 1180)),
        (1.20, 2.30, "bg-tiago-claro.png", 0.5, (250, 0, 1150, 830)),
        (2.30, 3.40, "exame-tiago-palco.jpg", 0.45, None),
        (3.40, 4.45, "exame.png", 0.0, (0, 430, 1080, 1560)),
    ],
    cutaways=[
        (30.50, 32.75, "mdc-site-longo.png", 0.0, (0, 1900, 1440, 3180)),
        (32.75, 34.95, "mdc-site-longo.png", 0.5, (0, 2200, 1440, 3480)),
    ],
    repl={63: (3, ["vieram", "aprender"]), 163: (1, ["pequena"]), 184: (2, ["agenda"]), 187: (2, ["uma"]), 205: (2, ["tráfego", "e", "comercial"])},
    # blocos já com a quebra por unidade de sentido (v1 RL tinha "e dentro de toda | a operação" e "Se você é | dono de empresa,")
    frases="""E eu olhei | pra essa sala agora | e pensei | em uma coisa | que eu preciso | te falar.
Essas 500 pessoas | tiraram dois dias | da vida delas | pra estudar.
Deixaram a empresa, | o cliente, | a correria | e vieram aprender | a implementar | inteligência artificial | no tráfego pago | e dentro | de toda a operação | da sua empresa.
Em três meses, | a maioria deles aqui | vai estar | num outro patamar.
Não porque são | mais inteligentes | que você, | mas sim porque | eles pararam | pra aprender | e foram implementar.
E aí que mora | a diferença | do mercado hoje.
Quem domina IA | vai fazer mais vendas | gastando menos, | com menos ferramentas | e menos custo fixo.
Quem não domina | vai continuar | pagando caro | pra fazer o mesmo | de sempre | e vendo o concorrente | crescer | sem entender porquê.
Se você é dono de empresa, | pequena ou média, | você ainda tá | em tempo, | mas tempo é | a única coisa | que não volta.
Clica aqui embaixo | e agenda agora | uma reunião comigo | com o meu time, | que eu vou te explicar | como implementar IA | no seu tráfego | e comercial | em detalhes.
Clica aqui | e eu te vejo | na nossa reunião. | Bora!""",
    enquadro=lambda t: (1.32, 0.30 if t < 10.30 else 0.33),
)
rodar(CFG)
