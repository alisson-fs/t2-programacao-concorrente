from time import sleep
from threading import Lock, Semaphore
import simulacao as sim


class Pista:
    '''
        Definição de apenas uma pista.
    '''
    def __init__(self, id = -1):
        self.nome = "Pista " + str(id)

    def overview(self):
        return self.nome

class Portao:
    '''
        Definição de apenas uma portão.
    '''
    def __init__(self, id = -1):
        self.nome = "Portão " + str(id)

    def overview(self):
        return self.nome

class Esteira:
    '''
        Definição de apenas uma esteira.
    '''
    def __init__(self, id = -1):
        self.quant_avioes = 0
        self.nome = "Esteira " + str(id)

    def overview(self):
        return self.nome + " (" + str(self.quant_avioes) + ")"

class Aeroporto:
    '''
        O Aeroporto possui recursos para atender os aviões que trafegarão
        por ele.

        É sua responsabilidade CRIAR esses recursos e CONTROLAR
        a alocação/liberação deles pelos diferentes aviões.

        A criação dos recursos deve seguir as variáveis globais do arquivo
        simulacao.py. Você pode utilizá-las assim: 'sim.quant_pistas'

        Só deve existir uma instância do aeroporto (olhe no final do arquivo)
        que já está criada.

        IMPORTANTE: os recursos devem ser únicos e dois aviões nunca podem
        utilizar o mesmo recurso ao mesmo tempo, tirando casos especiais como
        a esteira que pode atender uma quantidade limitada de aviões ao mesmo
        tempo.
    '''
    def __init__(self):
        self.nome = "Aeroporto"
        # Lista de pistas.
        self.pistas = []
        [self.pistas.append(Pista(i)) for i in range(sim.quant_pistas)]

        # Lista de portoes.
        self.portoes = []
        [self.portoes.append(Portao(j)) for j in range(sim.quant_portoes)]

        # Lista de esteiras.
        self.esteiras = []
        [self.esteiras.append(Esteira(k)) for k in range(sim.quant_esteiras)]
        
        # Listas para pouso.
        self.lista_pouso_decolagem = []
        self.lista_prioridade = []

        # Controle de concorrencia:

        # Semaforo para controle de reserva de pistas.
        self.sem_pistas = Semaphore(sim.quant_pistas)
        
        # Semaforo para controle de reserva de portões.
        self.sem_portoes = Semaphore(sim.quant_portoes)
        
        # Semaforo para controle de reserva de esteiras.
        self.sem_esteiras = Semaphore(sim.quant_esteiras * sim.quant_max_avioes_por_esteira)

    def overview(self):
        n_entrou        = sim.contadores["entrando"]
        n_aproximando   = sim.contadores["aproximando"]
        n_pousando      = sim.contadores["pousando"]
        n_acoplando     = sim.contadores["acoplando"]
        n_descarregando = sim.contadores["descarregando"]
        n_carregando    = sim.contadores["carregando"]
        n_desacoplando  = sim.contadores["desacoplando"]
        n_decolando     = sim.contadores["decolando"]
        n_saindo        = sim.contadores["saindo"]

        descricao = self.nome + " ("
        descricao += str(n_entrou)        + ", "
        descricao += str(n_aproximando)   + ", "
        descricao += str(n_pousando)      + ", "
        descricao += str(n_acoplando)     + ", "
        descricao += str(n_descarregando) + ", "
        descricao += str(n_carregando)    + ", "
        descricao += str(n_desacoplando)  + ", "
        descricao += str(n_decolando)     + ", "
        descricao += str(n_saindo)        + ")"
        return descricao

# Varivável global para armazenar o objeto Aeroporto.
# Utilize essa variável dentro das funções de um avião.
aeroporto = Aeroporto()
