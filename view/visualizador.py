import seaborn as sns
import json
import pandas as pd
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

class IVisualizador(ABC):
    """Interface para visualizadores de dados."""
    
    @abstractmethod
    def carregar_dados(self, caminho_arquivo):
        """Carrega os dados de um arquivo."""
        pass
    
    @abstractmethod
    def visualizar(self):
        """Visualiza os dados."""
        pass

class VisualizadorEvolucao(IVisualizador):
    """Visualizador de evolução de algoritmos genéticos."""
    
    def __init__(self):
        self.df = None
        
    def carregar_dados(self, caminho_arquivo="./utils/historico_avaliacoes.json"):
        """Carrega os dados de um arquivo JSON."""
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                historico_avaliacoes = json.load(arquivo)
                self.df = pd.json_normalize(historico_avaliacoes)
                
                self.df.rename(columns={
                    'metricas.eficiencia': 'Eficiencia',
                    'metricas.clareza': 'Clareza',
                    'metricas.boas_praticas': 'BoasPraticas'
                }, inplace=True)
                
                return True
        except Exception as e:
            print(f"Erro ao carregar dados: {str(e)}")
            return False
    
    def visualizar(self):
        """Visualiza os dados de evolução em gráficos."""
        if self.df is None or self.df.empty:
            print("Não há dados para visualizar.")
            return False
            
        sns.set_theme(style="darkgrid")
        plt.figure(figsize=(12, 8))

        # Gráfico de fitness
        plt.subplot(2, 2, 1)
        sns.lineplot(data=self.df, x='geracao', y='fitness', color="black", marker='o')
        plt.title('Evolução do Fitness')
        plt.xlabel('Geração')
        plt.ylabel('Fitness')

        # Gráfico de eficiência
        plt.subplot(2, 2, 2)
        sns.lineplot(data=self.df, x='geracao', y='Eficiencia', color="orange", marker='o')
        plt.title('Evolução da Eficiência')
        plt.xlabel('Geração')
        plt.ylabel('Eficiência')

        # Gráfico de clareza
        plt.subplot(2, 2, 3)
        sns.lineplot(data=self.df, x='geracao', y='Clareza', color="green", marker='o')
        plt.title('Evolução da Clareza')
        plt.xlabel('Geração')
        plt.ylabel('Clareza')

        # Gráfico de boas práticas
        plt.subplot(2, 2, 4)
        sns.lineplot(data=self.df, x='geracao', y='BoasPraticas', color="blue", marker='o')
        plt.title('Evolução das Boas Práticas')
        plt.xlabel('Geração')
        plt.ylabel('Boas Práticas')

        plt.tight_layout()
        plt.show()
        return True
        
    def exportar_grafico(self, caminho_arquivo="evolucao.png"):
        """Exporta o gráfico para um arquivo de imagem."""
        if self.df is None or self.df.empty:
            print("Não há dados para exportar.")
            return False
            
        try:
            sns.set_theme(style="darkgrid")
            plt.figure(figsize=(12, 8))

            # Gráfico de fitness
            plt.subplot(2, 2, 1)
            sns.lineplot(data=self.df, x='geracao', y='fitness', color="black", marker='o')
            plt.title('Evolução do Fitness')
            plt.xlabel('Geração')
            plt.ylabel('Fitness')

            # Gráfico de eficiência
            plt.subplot(2, 2, 2)
            sns.lineplot(data=self.df, x='geracao', y='Eficiencia', color="orange", marker='o')
            plt.title('Evolução da Eficiência')
            plt.xlabel('Geração')
            plt.ylabel('Eficiência')

            # Gráfico de clareza
            plt.subplot(2, 2, 3)
            sns.lineplot(data=self.df, x='geracao', y='Clareza', color="green", marker='o')
            plt.title('Evolução da Clareza')
            plt.xlabel('Geração')
            plt.ylabel('Clareza')

            # Gráfico de boas práticas
            plt.subplot(2, 2, 4)
            sns.lineplot(data=self.df, x='geracao', y='BoasPraticas', color="blue", marker='o')
            plt.title('Evolução das Boas Práticas')
            plt.xlabel('Geração')
            plt.ylabel('Boas Práticas')

            plt.tight_layout()
            plt.savefig(caminho_arquivo)
            plt.close()
            return True
        except Exception as e:
            print(f"Erro ao exportar gráfico: {str(e)}")
            return False

# Exemplo de uso
if __name__ == "__main__":
    visualizador = VisualizadorEvolucao()
    if visualizador.carregar_dados():
        visualizador.visualizar()