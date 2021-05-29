#!/usr/bin/python3

import sys
import getopt


# Parâmetros sobre o avião
novo_aviao_min               = 30
novo_aviao_max               = 120
combustivel_min              = 1
combustivel_max              = 25
tempo_pouso_decolagem        = 40

# Quantidades dos elementos de um aeroporto
quant_pistas                 = 4
quant_portoes                = 8
quant_esteiras               = 2
quant_max_avioes_por_esteira = 3

# Tempos das bagagens
tempo_descarregar_bagagens   = 90
tempo_carregar_bagagens      = 110
tempo_bagagens_esteira       = 200

# Tempo total da simulação
tempo_total                  = 10000

# Contadores globais
# Estes contadores globais guardam a quantidade de aviões que estão realizando
# aproximação, pousando, acoplando, etc. Eles devem ser alterados nos respectivos
# métodos que realizam as operações para aproximar, pousar, acoplar, etc.
# Apenas os contadores "entrando" e "saindo" são sempre incrementados. Os demais,
# serão incrementados/decrementados ao longo do ciclo de vida dos aviões.
contadores = {
    "entrando"      : 0,
    "aproximando"   : 0,
    "pousando"      : 0,
    "acoplando"     : 0,
    "descarregando" : 0,
    "carregando"    : 0,
    "desacoplando"  : 0,
    "decolando"     : 0,
    "saindo"        : 0
}

def ler_argumentos(argv):
    global novo_aviao_min
    global novo_aviao_max
    global combustivel_min
    global combustivel_max
    global tempo_pouso_decolagem
    global quant_pistas
    global quant_portoes
    global quant_esteiras
    global quant_max_avioes_por_esteira
    global tempo_descarregar_bagagens
    global tempo_carregar_bagagens
    global tempo_bagagens_esteira
    global tempo_total

    try:
        opts, args = getopt.getopt(argv, "", [
            "aviao-min=", "aviao-max=", "comb-min=", "comb-max=", "pouso=",
            "pistas=", "portoes=", "esteiras=", "max-avioes-esteiras=",
            "descarregar=", "carregar=", "bagagens=", "total=", "help"
        ])
    except getopt.GetoptError:
        print('Erro ao ler os argumentos.')
        sys.exit(2)

    # Configura simulação
    for opt, arg in opts:
        if opt == '--help':
            print("Possíveis configurações:")
            print ("""python3 main.py --aviao-min novo_aviao_min
                --aviao-max novo_aviao_max
                --comb-min combustivel_min
                --comb-max combustivel_max
                --pouso tempo_pouso_decolagem
                --pistas quant_pistas
                --portoes quant_portoes
                --esteiras quant_esteiras
                --max-avioes-esteiras quant_max_avioes_por_esteira
                --descarregar tempo_descarregar_bagagens
                --carregar tempo_carregar_bagagens
                --bagagens tempo_bagagens_esteira
                --total tempo_total
                --help Imprime essa ajuda
                """
            )
            sys.exit()
        elif opt == "--aviao-min":
            novo_aviao_min = int(arg)
        elif opt == "--aviao-max":
            novo_aviao_max = int(arg)
        elif opt == "--comb-min":
            combustivel_min = int(arg)
        elif opt == "--comb-max":
            combustivel_max = int(arg)
        elif opt == "--pouso":
            tempo_pouso_decolagem = int(arg)
        elif opt == "--pistas":
            quant_pistas = int(arg)
        elif opt == "--portoes":
            quant_portoes = int(arg)
        elif opt == "--esteiras":
            quant_esteiras = int(arg)
        elif opt == "--max-avioes-esteiras":
            quant_esteiras = int(arg)
        elif opt == "--descarregar":
            tempo_descarregar_bagagens = int(arg)
        elif opt == "--carregar":
            tempo_carregar_bagagens = int(arg)
        elif opt == "--bagagens":
            tempo_bagagens_esteira = int(arg)
        elif opt == "--total":
            tempo_total = int(arg)

    print('===================================================================')
    print('[sim] Parâmetros da simulação:')
    print('[sim] - Avião -----------------------------------------------------')
    print('[sim] Intervalo para novos aviões:             [',
        novo_aviao_min, ', ',
        novo_aviao_max, ')',
        sep = ''
    )
    print('[sim] Quantidade de combustível:               [',
        combustivel_min, ', ',
        combustivel_max, ')',
        sep = ''
    )
    print('[sim] Tempo para pousar/decolar um avião:     ',
        tempo_pouso_decolagem, 'ms'
    )
    print('[sim] - Aeroporto -------------------------------------------------')
    print('[sim] Quantidade de pistas:                   ', quant_pistas)
    print('[sim] Quantidade de portões:                  ', quant_portoes)
    print('[sim] Quantidade de esteiras:                 ', quant_esteiras)
    print('[sim] Quantidade máxima de aviões por esteira:',
        quant_max_avioes_por_esteira
    )
    print('[sim] - Bagagens --------------------------------------------------')
    print('[sim] Tempo para descarregar as bagagens:     ',
        tempo_descarregar_bagagens, 'ms'
    )
    print('[sim] Tempo para carregar as bagagens:        ',
        tempo_carregar_bagagens, 'ms'
    )
    print('[sim] Tempo das bagagens na esteira:          ',
        tempo_bagagens_esteira, 'ms'
    )
    print('[sim] - Simulação -------------------------------------------------')
    print('[sim] Tempo total da simulação:               ', tempo_total, 'ms')
    print('===================================================================')

