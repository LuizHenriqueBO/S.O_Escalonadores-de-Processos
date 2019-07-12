
class BCP():
    def __init__(self): #, id, prioridade, estado, tempo_chegada, tempo_inicio,tempo_CPU
        self.id = 0
        self.prioridade = 0
        self.tempo_chegada = 0
        self.tempo_inicio = 0
        self.tempo_CPU = 0
        self.tempo_executado = 0

        self.fila_IO = []
        self.tempo_IO = 0
        self.tempo_fim = 0

        self.tempo_espera = 0
        self.tempo_restante = 0

        self.lista_execucao = list()
        self.lista_bloqueado = list()
        self.lista_espera = list()
        

    def set_tempo_execucao_inicio(self, tempo):
        self.lista_execucao.append(tempo)
    def set_tempo_execucao_fim(self, tempo):
        self.lista_execucao.append(tempo+1)


    def set_tempo_bloqueio_inicio(self, tempo):
        self.lista_bloqueado.append(tempo)
    def set_tempo_bloqueio_fim(self, tempo):
        self.lista_bloqueado.append(tempo)



    def set_tempo_espera_inicio(self, tempo):
        if tempo in self.lista_espera:
            self.lista_espera.pop(-1)
        else:
            self.lista_espera.append(tempo)
    def set_tempo_espera_fim(self, tempo):
        if tempo in self.lista_espera:
            self.lista_espera.pop(-1)
        else:
            self.lista_espera.append(tempo)
    


    def get_id(self):
        return self.id
    
    def get_prioridade(self):
        return self.prioridade
    
    def get_tempo_chegada(self):
        return self.tempo_chegada
    
    def get_tempo_inicio(self):
        return self.tempo_inicio
    
    def get_tempo_CPU(self):
        return self.tempo_CPU

    def get_fila_io(self):
        return self.fila_IO

    def get_tempo_executado(self):
        return self.tempo_executado

    def get_tempo_IO(self):
        return self.tempo_IO

    def get_tempo_fim(self):
        return self.tempo_fim

    def get_tempo_execucao(self):     # Com finalidade para análise
        return (self.tempo_fim - self.tempo_inicio)

    def get_tempo_restante(self):
        return self.tempo_restante


 ################# setters ############################

    
    def set_id(self, id):
        self.id = int(id)
    
    def set_prioridade(self, prioridade):
        self.prioridade = int(prioridade)
    
    def set_tempo_chegada(self, chegada):
        self.tempo_chegada = int(chegada)
    
    def set_tempo_inicio(self, tempo_inicio):
        if(self.tempo_inicio <= 0):                 # se não foi setado o tempo de inicio ainda, então coloca
            self.tempo_inicio = int(tempo_inicio)   # caso ao contrário não coloca um novo tempo!
    
    def set_tempo_CPU(self, tempo_cpu):
        self.tempo_CPU = int(tempo_cpu)

    def set_fila_io(self, fila):
        #print(fila)
        self.fila_IO = list(map(int,fila)) if fila and fila[-1] else []

    def set_tempo_fim(self, clock):
        self.tempo_fim =  clock

    
    def set_tempo_restante(self,tempo_restante):
        self.tempo_restante = int(tempo_restante)




 ################# setters ############################
    
    def set_tempo_CPU(self, tempo_cpu):
        self.tempo_CPU = int(tempo_cpu)

    def set_fila_io(self, fila):
        print(fila)
        self.fila_IO = list(map(int,fila)) if fila and fila[-1] else []

    def set_tempo_fim(self, clock):
        self.tempo_fim =  clock

    ######################################



    ###################### metodos #############


    ##############
    
    def add_tempo_IO(self):
        self.tempo_IO = 5
    
    def decrem_tempo_IO(self):
        if(self.tempo_IO >= 0):
            self.tempo_IO -=1
            return True
        return False

    #################




    def executar(self):
        self.tempo_executado += 1        # atualixa o tempo de execução
        self.tempo_restante  -= 1        # atualixa o tempo restante



    def remove_fila_io(self):
        self.fila_IO.remove(self.fila_IO[0])
    

    # def decrementar_tempo_cpu(self):
    #     if(self.tempo_CPU  <= 0):
    #         return False
    #     else:
    #         self.tempo_CPU -=1
    #         return True


    def finalizado(self):
        if(self.tempo_executado == self.tempo_CPU):
            return True
        else:
            return False

    def solicita_io(self):
        #print("Solicita io %d" % self.tempo_executado)
        if(self.tempo_executado in self.fila_IO):
            print("processo: ",self.id,"entrou em IO no tempo: ",self.tempo_executado)
            self.fila_IO.remove(self.fila_IO[0])
            #print("QQQ")
            return True
        else:
            return False

    def imprimedados(self):
        print(self.id, self.tempo_CPU, self.prioridade, self.tempo_chegada, self.fila_IO, self.tempo_executado, self.tempo_inicio, self.tempo_IO)