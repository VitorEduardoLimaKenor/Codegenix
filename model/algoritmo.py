class Algoritmo:
    """Classe que representa um algoritmo a ser evoluído.
    
    Responsabilidades:
    - Armazenar o código do algoritmo
    - Manter informações sobre sua avaliação (fitness e métricas)
    """
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
    
    def set_fitness(self, valor):
        """Define o valor de fitness do algoritmo."""
        self.fitness = valor
        
    def set_metricas(self, metricas):
        """Define as métricas de avaliação do algoritmo."""
        self.metricas = metricas
        
    def get_fitness(self):
        """Retorna o valor de fitness do algoritmo."""
        return self.fitness or 0
        
    def get_metricas(self):
        """Retorna as métricas de avaliação do algoritmo."""
        return self.metricas
    
    def clone(self, novo_codigo=None, novo_id=None):
        """Cria uma cópia do algoritmo, opcionalmente com novo código."""
        from copy import deepcopy
        id_clone = novo_id if novo_id is not None else self.id
        codigo_clone = novo_codigo if novo_codigo is not None else self.codigo
        clone = Algoritmo(id_clone, self.linguagem, codigo_clone)
        clone.fitness = self.fitness
        clone.metricas = deepcopy(self.metricas)
        return clone
