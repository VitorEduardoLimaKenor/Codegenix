class Algoritmo:
    def __init__(self, id, linguagem, codigo):
        self.id = id
        self.linguagem = linguagem
        self.codigo = codigo
        self.fitness = None
        self.metricas = {
            "eficiencia": 0,
            "clareza": 0,
            "boas_praticas": 0
        }
