from controller.operador_genetico import OperadorGenetico
from controller.avaliador_service import AvaliadorService

class Populacao:
    def __init__(self, linguagem: str, tamanho: int = 5):
        self.algoritmos = []
        self.linguagem = linguagem
        self.geracao = 0
        self.tamanho = tamanho
        self.avaliador = AvaliadorService()
        self.operador = OperadorGenetico()

    def gerar_populacao_inicial(self, codigo_base: str, tamanho: int = None):
        # Permite sobrescrever o tamanho na chamada, se necessário
        if tamanho is not None:
            self.tamanho = tamanho

        variacoes = self.operador.gerar_variacoes_iniciais(
            codigo_base=codigo_base,
            linguagem=self.linguagem,
            quantidade=self.tamanho
        )
        self.algoritmos = variacoes

        # Avalia cada algoritmo já na geração inicial
        for algoritmo in self.algoritmos:
            self.avaliador.avaliar(algoritmo)

    def evoluir(self, num_geracoes: int = 5):
        for _ in range(num_geracoes):
            # Avalia todos os algoritmos da geração atual
            for alg in self.algoritmos:
                self.avaliador.avaliar(alg)

            # Seleciona os melhores para cruzar
            selecionados = self.operador.selecionar(self.algoritmos, quantidade=self.tamanho)

            nova_geracao = []
            for i in range(0, len(selecionados), 2):
                if i + 1 < len(selecionados):
                    filho = self.operador.cruzar(selecionados[i], selecionados[i + 1])
                    filho = self.operador.mutar(filho)
                    self.avaliador.avaliar(filho)
                    nova_geracao.append(filho)

            self.algoritmos = nova_geracao
            self.geracao += 1

    def melhor_individuo(self):
        """Retorna o melhor indivíduo da população atual."""
        if not self.algoritmos:
            return None
        return max(self.algoritmos, key=lambda a: a.fitness or 0)

    def salvar_melhor_algoritmo(self, caminho="melhor_algoritmo.py"):
        if not self.algoritmos:
            print("Nenhum algoritmo na população.")
            return

        melhor = self.melhor_individuo()

        with open(caminho, "w", encoding="utf-8") as f:
            f.write(f"# Algoritmo mais eficiente - Fitness: {melhor.fitness}\n")
            f.write(melhor.codigo)

