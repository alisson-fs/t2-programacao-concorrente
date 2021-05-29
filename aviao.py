from threading import Thread
from time import sleep

import simulacao as sim
from aeroporto import *

class Aviao(Thread):
    '''
        Aviões devem ser criados periodicamente e realizar as seguintes ações:
        - Se aproximar do aeroporto e esperar a sua vez de pousar.
          Verifique no enunciado a ordem de pouso.
        - O avião deve pousar (por um determinado tempo) na pista reservada
          para ele.
        - O avião que acabou de pousar deve tentar ir para um portão livre.
        - O avião deve alocar uma esteira para descarregar as bagagens dos
          passageiros.
        - O avião deve carregar as bagagens do próximo vôo.
        - O avião deve desacoplar do portão e tentar decolar.
        - O avião deve sair do portão para uma pista livre e decolar.

        A sua responsabilidade é desenvolver os comportamentos dentro das
        funções do avião e proteger os contadores globais.
    '''

    def __init__(self, id, combustivel):
        # Atributos default
        self.id          = id
        self.combustivel = combustivel

        # Atributos nulos, não altere essas variáveis. Elas devem ser alteradas
        # apenas durante alocação e liberação de recursos. Ou seja, ao liberar
        # um recurso, sobreescreva o valor antigo com um recurso nulo
        # (construtor vázio).
        self.pista   = Pista()
        self.portao  = Portao()
        self.esteira = Esteira()
        super().__init__(name=("Avião " + str(id)))

    def overview(self):
        descricao = self.name + " ("
        descricao += "Combustível " + str(self.combustivel) + "%, "
        descricao += self.pista.overview()                  + ", "
        descricao += self.portao.overview()                 + ", "
        descricao += self.esteira.overview()                + ")"
        return descricao

    def log(self, frase, espacos = 0):
        print('[', self.overview(), '] ', frase,
            " " * espacos, ' | ', aeroporto.overview(), sep = ''
        )

    def run(self):
        '''
            NÃO ALTERE A ORDEM DAS CHAMADAS A BAIXO.

            Você deve implementar os comportamentos dentro das funções aqui
            invocadas. Lembre-se de usar a variável global "aeroporto" para ter
            acesso a funções e recursos.
            Observação: Comente no código qual o objetivo de uma dada
            operação, ou conjunto de operações, para facilitar a correção do
            trabalho.
        '''
        sim.contadores["entrando"] += 1

        self.log("Entrou no espaço aéreo", 17)

        self.aproximar()
        self.pousar()
        self.acoplar()
        self.descarregar_bagagens()
        self.carregar_bagagens()
        self.desacoplar()
        self.decolar()

        sim.contadores["saindo"] += 1

        self.log("Saindo do espaço aéreo", 17)

    def atualiza_contador(contador):
        def decorador(operacao):
            def envelope(self):
                sim.contadores[contador] += 1
                operacao(self)
                sim.contadores[contador] -= 1
            return envelope
        return decorador

    @atualiza_contador("aproximando")
    def aproximar(self):
        self.log("Aproxima-se", 28)
        '''
            O avião deve tentar reservar uma pista, respeitando a ordem de
            prioridade definida no enunciado. Se não houver pistas livres,
            o avião deve aguardar até que seja a sua vez de alocar a próxima
            pista liberada.
        '''

        # Adiciona o avião a fila de utilização da pista, se necessário, será 
        # adicionado a uma lista prioritária.
        if self.combustivel < 10:
            aeroporto.lista_prioridade.append(self)
        else:
            aeroporto.lista_pouso_decolagem.append(self)

        # Quando for sua vez, aguarda uma pista liberar.
        while (len(aeroporto.lista_pouso_decolagem) != 0 or
               len(aeroporto.lista_prioridade) != 0):
            if len(aeroporto.lista_prioridade) != 0:
                if self == aeroporto.lista_prioridade[0]:
                    aeroporto.sem_pistas.acquire()
                    self.pista = aeroporto.pistas.pop(0)
                    aeroporto.lista_prioridade.pop(0)
            elif len(aeroporto.lista_pouso_decolagem) != 0:
                if self == aeroporto.lista_pouso_decolagem[0]:
                    aeroporto.sem_pistas.acquire()
                    self.pista = aeroporto.pistas.pop(0)
                    aeroporto.lista_pouso_decolagem.pop(0)
            

    @atualiza_contador("pousando")
    def pousar(self):
        '''
            Avião só chega aqui quando tiver reservado uma pista.
        '''
        self.log("Pousa na " + self.pista.overview(), 22)
        '''
            O avião deve "pousar" por um período de tempo e taxiar até um
            portão livre. Após o pouso, a pista pode ser liberada para outro
            avião enquanto o avião atual aguarda um portão liberar.
        '''

        # Aguarda o tempo de pouso.
        sleep(sim.tempo_pouso_decolagem/1000)
        
        # Libera a pista utilizada.
        aeroporto.pistas.append(self.pista)
        self.pista = Pista()
        aeroporto.sem_pistas.release()

    @atualiza_contador("acoplando")
    def acoplar(self):
        '''
            O avião que acabou de sair da pista após sua aterrisagem deve
            aguardar um portão liberar. A ordem de reserva dos portões deve
            respeitar a ordem de requisição.
        '''

        # Caso necessário, aguarda a liberação de um portão.
        aeroporto.sem_portoes.acquire()
        self.portao = aeroporto.portoes.pop(0)

        '''
            Avião só chega aqui quando tiver reservado um portão.
        '''
        self.log("Acopla no " + self.portao.overview(), 20)

    @atualiza_contador("descarregando")
    def descarregar_bagagens(self):
        '''
            O avião deve buscar uma esteira que possua espaço livre para
            descarregar as bagagens dos passageiros. Lembre que uma esteira
            suporta uma quantidade definida de aviões ao mesmo tempo.
        '''

        # Caso necessário, aguarda a liberação de uma esteira.
        aeroporto.sem_esteiras.acquire()
        
        # Pega uma esteira e atualiza a quantidade de aviões na esteira.
        self.esteira = aeroporto.esteiras[0]
        aeroporto.esteiras[0].quant_avioes += 1
        
        # Caso a quantidade de aviões por esteira chegar ao máximo, a esteira
        # sai da lista de esteiras disponíveis.
        if self.esteira.quant_avioes == sim.quant_max_avioes_por_esteira:
            aeroporto.esteiras.pop(0)
            
        '''
            Avião só chega aqui quando tiver reservado uma esteira.
        '''
        self.log("Descarrega bagagens pela " + self.esteira.overview(), 0)
        '''
            O avião deve descarregar as bagagens dos passageiros.
        '''

        # Aguarda o tempo de descarregamento das bagagens.
        sleep(sim.tempo_descarregar_bagagens/1000)
        sleep(sim.tempo_bagagens_esteira/1000)

    @atualiza_contador("carregando")
    def carregar_bagagens(self):
        '''
            Avião só chega aqui quando tiver descarregado as bagagens.
        '''
        self.log("Carrega bagagens pela " + self.esteira.overview(), 3)
        '''
            O avião deve carregar as bagagens dos novos passageiros. Após
            o embarque das bagagens e dos passageiros, o avião pode liberar
            a esteira e desacoplar.
        '''
        
        # Aguarda o tempo de carregamento das bagagens.
        sleep(sim.tempo_carregar_bagagens/1000)
        
        # Libera esteira e adiciona na lista de esteiras disponíveis.
        self.esteira.quant_avioes -= 1
        if self.esteira.quant_avioes == sim.quant_max_avioes_por_esteira - 1:
            aeroporto.esteiras.append(self.esteira)
        self.esteira = Esteira()
        aeroporto.sem_esteiras.release()

    @atualiza_contador("desacoplando")
    def desacoplar(self):
        '''
            Avião só chega aqui quando tiver carregado as bagagens.
        '''
        self.log("Desacoplando do " + self.portao.overview(), 14)
        '''
            O avião deve liberar o portão e taxiar até a pista. Caso não haja
            uma pista disponível, o avião deve aguardar seguindo a ordem de
            prioridade definida no enunciado do trabalho.
        '''

        # IMPLEMENTE A LIBERAÇÃO DO PORTÃO E RESERVA DA PISTA.

        aeroporto.portoes.append(self.portao)
        self.portao = Portao()
        aeroporto.sem_portoes.release()

        # Adiciona o avião a fila de utilização da pista.
        aeroporto.lista_pouso_decolagem.append(self)

        # Quando for sua vez, aguarda uma pista liberar.
        while (len(aeroporto.lista_pouso_decolagem) != 0 or
               len(aeroporto.lista_prioridade) != 0):
            if len(aeroporto.lista_prioridade) != 0:
                if self == aeroporto.lista_prioridade[0]:
                    aeroporto.sem_pistas.acquire()
                    self.pista = aeroporto.pistas.pop(0)
                    aeroporto.lista_prioridade.pop(0)
            elif len(aeroporto.lista_pouso_decolagem) != 0:
                if self == aeroporto.lista_pouso_decolagem[0]:
                    aeroporto.sem_pistas.acquire()
                    self.pista = aeroporto.pistas.pop(0)
                    aeroporto.lista_pouso_decolagem.pop(0)

    @atualiza_contador("decolando")
    def decolar(self):
        '''
            Avião só chega aqui quando tiver reservado uma pista.
        '''
        self.log("Decolando pela " + self.pista.overview(), 16)
        '''
            O avião deve decolar e liberar a pista.
        '''

        # Libera a pista utilizada.
        aeroporto.pistas.append(self.pista)
        self.pista = Pista()
        aeroporto.sem_pistas.release()
