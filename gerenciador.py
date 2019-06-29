class Gerenciador():
    def __init__(self):
        self.fila_processos = []
        self.fila_pronto = []
        self.fila_bloqueado = []
        self.fila_finalizados = []

        self.fila_io = []
        self.fila_quantum = []
        

    def get_fila_io(self):
        return self.fila_io

    def get_fila_quantum(self):
        return self.fila_quantum
    
    
    ##### getters
    def get_fila_pronto(self):
        return self.fila_pronto
    
    def get_fila_bloqueado(self):
        return self.fila_bloqueado

    def get_fila_processos(self):
        return self.fila_processos

    def get_fila_finalizados(self):
        return self.fila_finalizados


    #### add
    def add_fila_finalizados(self, processo):
        self.fila_finalizados.append(processo)

    def add_fila_pronto(self, processo):
        self.fila_pronto.append(processo)
    
    def add_fila_bloqueio(self, processo):
        self.fila_bloqueado.append(processo)

    def add_fila_processos(self, processo):
        self.fila_processos.append(processo)

    def add_fila_io(self, processo):
        self.fila_io.append(processo)
    
    def add_fila_quantum(self, processo):
        self.fila_quantum.append(processo)
    
    