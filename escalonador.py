
from grafico import *

class Escalonador(object):


    def __init__(self):
	    self.timer = 0
    

    def geradorGrafico(self, titulo='', labelx='', labely=''):
        import matplotlib.pyplot as plt
        import seaborn as sns
        import pandas as pd
        sns.set()
        x = self.fila_dados[0]
        y = self.fila_dados[1]
        colors = ['#2300A8', '#00A658']
        plt.xticks(range(len(x)), x)
        plt.bar(range(len(y)), y, align='center', color=colors)
        plt.title(titulo)
        plt.xlabel(labelx) # 'Processo (ID)'
        plt.ylabel(labely) # 'Tempo (ciclo de clock)'
        plt.show()
        

    def gerarGraficoExecucao(self, gp, titulo=''):
        # Para criar um gráfico de execução, primeiro criamos um array que conterá as informações
        self.fila_dados = []
        # preenchemos o array fila_execução
        for processo in gp.get_fila_finalizados():
            #self.fila_dados.append((processo.get_id(), processo.get_tempo_execucao()))
            self.fila_dados.append((processo.get_id(), processo.lista_execucao[-1]))
        print(self.fila_dados)
        # formatamos os dados, para que fiquem em subvetores separados
        # chamamos a função que montará o gráfico e passamos um título
        self.fila_dados = list(zip(*self.fila_dados))
        print(self.fila_dados)
        self.geradorGrafico(titulo, 'Processo (ID)', 'Tempo de vida da CPU')


    def removeProcesso(self, processo, fila_origem):
        for i in range(len(fila_origem)):
            if(fila_origem[i] == processo):
                del(fila_origem[i])
                return True
        return False

   
    def escalonar(self, processo, fila_origem, fila_destino):
        # escalona o processo de fila de saida pra fila atual, e faz verificação
        # do tempo atual e tempo de chegada do processo ao cpu
        # pois só posso escalonar um processo que tenha passado pelo processador!
        if(processo in fila_origem):
            if(self.timer >= processo.tempo_chegada): 
                fila_destino.append(processo)
                self.removeProcesso(processo, fila_origem)
                # for i in range(len(fila_origem)):
                #     if(fila_origem[i] == processo):
                #         del(fila_origem[i])
                #         return True
            return False


    def verificaFilaBloqueio(self, gp, fila_destino):
        # verifica se tem alguém na fila de bloqueio, caso tenha, decrementa o tempo de I/O e não escalona,
        # caso for decrementar e não possível, a função decrem_tempo_IO() retorna FALSE, negando essa
        # condição ela se torna verdadeira, portando devemos escalonar para a fila de pronto 
        # pois o tempo de I/O já esgotou.
        gp.get_fila_bloqueado().sort(key = lambda x: x.get_tempo_IO())
        if(len(gp.get_fila_bloqueado()) > 0):
            for processo in gp.get_fila_bloqueado():
                processo.decrem_tempo_IO()
            for processo in gp.get_fila_bloqueado():
                processo = gp.get_fila_bloqueado()[0]
                if(processo.get_tempo_IO() == -1):
                    processo.set_tempo_bloqueio_fim(self.timer)
                    processo.set_tempo_espera_inicio(self.timer)
                    self.escalonar(processo, gp.get_fila_bloqueado(), fila_destino)


    def verificaFilaProcessos(self, gp, fila_destino):
        # todo processo que está na fila de processo deve ser escalonado para a fila de pronto de acordo
        # com o tempo de chegada e cada processo tem seu tempo diferente de chegada.
        # Sendo assim verificamos se tem processo na fila de processos
        # Caso tenha, lembramos que os processos foram ordenados por tempo de chegada,
        # Assim verificamos na fila de processos se o timer (clock) é maior ou igual o 
        # tempo de chegada do processo.
        # Se essas condições foram satisfeitas, escalonamos o processo para a fila de pronto.
        if((len(gp.get_fila_processos()) > 0) and (self.timer >= gp.get_fila_processos()[0].get_tempo_chegada())):
            processo = gp.get_fila_processos()[0]
            processo.set_tempo_espera_inicio(self.timer)
            self.escalonar(processo, gp.get_fila_processos(), fila_destino)
            return True
        return False
    

    def verificarProcessos(self, gp, fila_destino):
        self.timer +=1
        self.verificaFilaProcessos(gp,fila_destino)
        self.verificaFilaBloqueio(gp, fila_destino)
        

    ###################--------RoundRobin------##################
    def RoundRobin(self, gp):
        # tempo que ficará no processador
        self.quantum = 4
        # tempo de ciclo
        self.timer = 0
        # Ordeno a fila de processos por ordem de chegada
        gp.get_fila_processos().sort(key=lambda x: x.get_tempo_chegada())
        self.verificaFilaProcessos(gp, gp.get_fila_pronto())
        while((len(gp.get_fila_pronto()) > 0) or (len(gp.get_fila_bloqueado()) > 0) or (len(gp.get_fila_processos()) > 0)):
            # caso ainda tenha processo na fila de pronto, bloqueado e processos
            # continua executando o programa
            if(len(gp.get_fila_pronto()) > 0):
                # tem alguem na fila de pronto ? se TRUE executa, se FALSE processador fica ocioso
                # executa cada processo da fila de prontos
                for processo in gp.get_fila_pronto()[1:]:
                    processo.tempo_espera +=1
                processo = gp.get_fila_pronto()[0]
                # seta o tempo de início de cada processo
                processo.set_tempo_inicio(self.timer)
                # inicializa o tempo de execução para comparar com Quantum
                self.tempo = 0
                # execute até que alguém impessa
                while(1):
                    if(processo.get_tempo_restante() <= 0):
                        # Como o processo acabou de ser executado, devemos verificar novamente
                        # se o tempo de CPU expirou, se isso acontecer, devemos movê-lo pra
                        # fila de finalizados!
                        # como no momento ele será o último processo da fila, adicionamos um
                        # timer no atributo, que ajudará nas análises e geração de gráficos
                        processo.set_tempo_fim(self.timer)
                        self.escalonar(processo, gp.get_fila_pronto(), gp.get_fila_finalizados())
                        # self.verificarProcessos(gp, gp.get_fila_pronto())
                        break
                    if(len(gp.get_fila_pronto()) > 0):
                        # verifica se tem tempo restante de CPU, caso tenha, continua na fila de pronto
                        if(processo.get_tempo_restante() > 0):
                            # Executa o processo atual e incrementa o timer
                            processo.executar()
                            self.tempo +=1
                            if(processo.get_tempo_restante() <= 0):
                                # Como o processo acabou de ser executado, devemos verificar novamente
                                # se o tempo de CPU expirou, se isso acontecer, devemos movê-lo pra
                                # fila de finalizados!
                                # como no momento ele será o último processo da fila, adicionamos um
                                # timer no atributo, que ajudará nas análises e geração de gráficos
                                processo.set_tempo_fim(self.timer)
                                self.escalonar(processo, gp.get_fila_pronto(), gp.get_fila_finalizados())
                                self.verificarProcessos(gp, gp.get_fila_pronto())
                                break
                            if processo.solicita_io():
                                # Caso o processo não foi para a fila de finalizado, verificamos se
                                # o mesmo solicita I/O, caso isso aconteça, movamos-o para
                                # fila de bloqueado e adicionamos um tempo de I/O (padrão para todos os
                                # processos).
                                processo.add_tempo_IO(self.timer)
                                self.escalonar(processo, gp.get_fila_pronto(), gp.get_fila_bloqueado())
                                self.verificarProcessos(gp, gp.get_fila_pronto())
                                break
                            if(self.tempo >= self.quantum):
                                processo.set_tempo_execucao_fim(self.timer)
                                self.escalonar(processo, gp.get_fila_pronto(), gp.get_fila_pronto())
                                self.tempo = 0
                                self.verificarProcessos(gp, gp.get_fila_pronto())
                                processo.set_tempo_espera_inicio(self.timer)
                                break
                            self.verificarProcessos(gp, gp.get_fila_pronto())
                    else:
                        self.verificarProcessos(gp, gp.get_fila_pronto())
            else:
                # caso não tiver nenhum processo a ser executado, o processador ficará ocioso e
                # o timer (tempo de ciclo) será incrementado.
                self.verificarProcessos(gp, gp.get_fila_pronto())
        # função para gerar o gráfico de execução
        add_dados_diagrama_gantt(gp, self.timer, 'Round Robin')                 # gerando o diagrama de gantt
        self.gerarGraficoExecucao(gp,'Escalonador de processos RoundRobin')     # gerando gráfico de estatistica




    ###################--------Shortest Remaining Time First (SRTF)------##################
    
    def srtf(self, gp):
        # tempo de ciclo
        self.timer = 0
        # Ordeno a fila de processos por ordem de chegada
        gp.get_fila_processos().sort(key=lambda x: x.get_tempo_chegada())
        self.verificaFilaProcessos(gp,gp.get_fila_pronto())
        while((len(gp.get_fila_pronto()) > 0) or (len(gp.get_fila_bloqueado()) > 0) or (len(gp.get_fila_processos()) > 0)):
            # caso ainda tenha processo na fila de pronto, bloqueado e processos
            # continua executando o programa
            if(len(gp.get_fila_pronto()) > 0):
                gp.get_fila_pronto().sort(key = lambda x: x.get_tempo_restante())
                # tem alguem na fila de pronto ? se TRUE executa, se FALSE processador fica ocioso
                # executa cada processo da fila de prontos
                for processo in gp.get_fila_pronto()[1:]:
                    processo.tempo_espera +=1
                processo = gp.get_fila_pronto()[0]
                # seta o tempo de início de cada processo
                processo.set_tempo_inicio(self.timer)
                # execute os processos
                while(1):
                    if(processo.get_tempo_restante() <= 0):
                        # Como o processo acabou de ser executado, devemos verificar novamente
                        # se o tempo de CPU expirou, se isso acontecer, devemos movê-lo pra
                        # fila de finalizados!
                        # como no momento ele será o último processo da fila, adicionamos um
                        # timer no atributo, que ajudará nas análises e geração de gráficos
                        processo.set_tempo_fim(self.timer)
                        self.escalonar(processo, gp.get_fila_pronto(), gp.get_fila_finalizados())
                        # self.verificarProcessos(gp, gp.get_fila_pronto())                        
                        break
                    if(len(gp.get_fila_pronto()) > 0):
                        gp.get_fila_pronto().sort(key = lambda x: x.get_tempo_restante())
                        if(processo.get_tempo_restante() <= gp.get_fila_pronto()[0].get_tempo_restante()):
                        # se tiver alguém na fila de pronto com o tempo restante menor, manda o processo pro fim da fila de pronto e
                        # executa o que tem menor tempo restante.
                            # verifica se tem tempo de CPU, caso tenha, continua na fila de pronto
                            if(processo.get_tempo_restante() > 0):
                                # Executa o processo atual e incrementa o timer
                                processo.executar()
                                if(processo.get_tempo_restante() <= 0):
                                    # Como o processo acabou de ser executado, devemos verificar novamente
                                    # se o tempo de CPU expirou, se isso acontecer, devemos movê-lo pra
                                    # fila de finalizados!
                                    # como no momento ele será o último processo da fila, adicionamos um
                                    # timer no atributo, que ajudará nas análises e geração de gráficos
                                    processo.set_tempo_fim(self.timer)
                                    self.escalonar(processo, gp.get_fila_pronto(), gp.get_fila_finalizados())
                                    self.verificarProcessos(gp, gp.get_fila_pronto())
                                    break
                                if processo.solicita_io():
                                    # Caso o processo não foi para a fila de finalizado, verificamos se
                                    # o mesmo solicita I/O, caso isso aconteça, movamos-o para
                                    # fila de bloqueado e adicionamos um tempo de I/O (padrão para todos os
                                    # processos).
                                    # processo.set_tempo_execucao_fim(self.timer)
                                    # processo.set_tempo_bloqueio_inicio(self.timer)
                                    processo.add_tempo_IO(self.timer)
                                    self.escalonar(processo, gp.get_fila_pronto(), gp.get_fila_bloqueado())
                                    self.verificarProcessos(gp, gp.get_fila_pronto())
                                    break
                                self.verificarProcessos(gp, gp.get_fila_pronto())
                        else:
                            # caso o tenha algum processo com o tempo restante menor que o processo executando,
                            # movamos o processo para o fim da fila de pronto
                            # e o próximo processo será executado
                            processo.set_tempo_execucao_fim(self.timer-1)
                            processo.set_tempo_espera_inicio(self.timer)
                            self.escalonar(processo, gp.get_fila_pronto(), gp.get_fila_pronto())                      
                            break
                    else:    
                        self.verificarProcessos(gp, gp.get_fila_pronto())
            else:
                # caso não tiver nenhum processo a ser executado, o processador ficará ocioso e
                # o timer (tempo de ciclo) será incrementado.
                self.verificarProcessos(gp, gp.get_fila_pronto())
        add_dados_diagrama_gantt(gp, self.timer, 'Shortest Remaining Time First (SRTF)')
        self.gerarGraficoExecucao(gp,'Escalonador de processos Shortest Remaining Time First (SRTF)')


    ###################--------PRIORIDADE DINÂMICA COM DUPLA FILA------##################
    def Prioridade_Dinamica_fila_dupla(self, gp):
        self.prioridade_quantim = 7
        self.prioridade_io      = 3
        # tempo que ficará no processador
        #self.quantum = 4
        # tempo de ciclo
        self.timer = 0
        # Ordeno a fila de processos por ordem de chegada
        gp.get_fila_processos().sort(key=lambda x: x.get_tempo_chegada())
        self.verificaFilaProcessos(gp, gp.get_fila_quantum())
        while( (len(gp.get_fila_io()) > 0) or (len(gp.get_fila_quantum()) > 0) or (len(gp.get_fila_bloqueado()) > 0) or (len(gp.get_fila_processos()) > 0)):
            # caso ainda tenha processo na fila de pronto, bloqueado e processos
            # continua executando o programa
            if((len(gp.get_fila_quantum()) > 0) or (len(gp.get_fila_io()) > 0)):
                contador_quantum = self.prioridade_quantim
                contador_io      = self.prioridade_io
                while((contador_quantum > 0) and len(gp.get_fila_quantum()) > 0):
                    contador_quantum -= 1
                    self.execucao(gp, gp.get_fila_quantum())
                while((contador_io > 0)and(len(gp.get_fila_io()) > 0)):
                    contador_io -=1
                    self.execucao(gp, gp.get_fila_io())
            else:
                # caso não tiver nenhum processo a ser executado, o processador ficará ocioso e
                # o timer (tempo de ciclo) será incrementado.
                self.timer +=1
                self.verificaFilaProcessos(gp,gp.get_fila_quantum())
                self.verificaFilaBloqueio(gp, gp.get_fila_io())
        # função para gerar o gráfico de execução
        add_dados_diagrama_gantt(gp, self.timer, 'Prioridade Dinâmica com Fila Dupla')
        self.gerarGraficoExecucao(gp,'Escalonador de processos Prioridade Dinâmica com Fila Dupla')
        #self.gerarGraficoExecucao(gp,'PRIORIDADE DINÂMICA COM DUPLA FILA')


    def execucao(self, gp, fila_executar):
        self.quantum = 4
        # tem alguem na fila de pronto ? se TRUE executa, se FALSE processador fica ocioso
        # executa cada processo da fila de prontos
        for processo in fila_executar:
            processo.tempo_espera +=1
        processo = fila_executar[0]
        processo.tempo_espera -=1
        # seta o tempo de início de cada processo
        processo.set_tempo_inicio(self.timer)
        # inicializa o tempo de execução para comparar com Quantum
        self.tempo = 0
        # execute até que alguém impessa
        while(1):
            if(processo.get_tempo_restante() <= 0):
                # Como o processo acabou de ser executado, devemos verificar novamente
                # se o tempo de CPU expirou, se isso acontecer, devemos movê-lo pra
                # fila de finalizados!
                # como no momento ele será o último processo da fila, adicionamos um
                # timer no atributo, que ajudará nas análises e geração de gráficos
                processo.set_tempo_fim(self.timer)
                self.escalonar(processo, fila_executar, gp.get_fila_finalizados())
                # self.timer +=1
                # self.verificaFilaProcessos(gp, gp.get_fila_quantum())
                # self.verificaFilaBloqueio(gp, gp.get_fila_io())
                break
            if(len(fila_executar) > 0):
                # verifica se tem tempo restante de CPU, caso tenha, continua na fila de pronto
                if(processo.get_tempo_restante() > 0):
                    # Executa o processo atual e incrementa o timer
                    processo.executar()
                    self.tempo +=1
                    if(processo.get_tempo_restante() <= 0):
                        # Como o processo acabou de ser executado, devemos verificar novamente
                        # se o tempo de CPU expirou, se isso acontecer, devemos movê-lo pra
                        # fila de finalizados!
                        # como no momento ele será o último processo da fila, adicionamos um
                        # timer no atributo, que ajudará nas análises e geração de gráficos
                        processo.set_tempo_fim(self.timer)
                        self.escalonar(processo, fila_executar, gp.get_fila_finalizados())
                        self.timer +=1
                        self.verificaFilaProcessos(gp,gp.get_fila_quantum())
                        self.verificaFilaBloqueio(gp, gp.get_fila_io())
                        break
                    if processo.solicita_io():
                        # Caso o processo não foi para a fila de finalizado, verificamos se
                        # o mesmo solicita I/O, caso isso aconteça, movamos-o para
                        # fila de bloqueado e adicionamos um tempo de I/O (padrão para todos os
                        # processos).
                        processo.add_tempo_IO(self.timer)
                        self.escalonar(processo, fila_executar, gp.get_fila_bloqueado())
                        self.timer +=1
                        self.verificaFilaProcessos(gp,gp.get_fila_quantum())
                        self.verificaFilaBloqueio(gp, gp.get_fila_io())
                        break
                    if(self.tempo >= self.quantum):
                        processo.set_tempo_execucao_fim(self.timer)
                        self.escalonar(processo, fila_executar, gp.get_fila_quantum())
                        self.tempo = 0
                        self.timer +=1
                        self.verificaFilaProcessos(gp,gp.get_fila_quantum())
                        self.verificaFilaBloqueio(gp, gp.get_fila_io())
                        processo.set_tempo_espera_inicio(self.timer)
                        break
                    self.timer +=1
                    self.verificaFilaProcessos(gp,gp.get_fila_quantum())
                    self.verificaFilaBloqueio(gp, gp.get_fila_io())
            else:
                self.timer +=1
                self.verificaFilaProcessos(gp,gp.get_fila_quantum())
                self.verificaFilaBloqueio(gp, gp.get_fila_io())