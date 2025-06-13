import streamlit as st
import pandas as pd
import os
from abc import ABC, abstractmethod
from view.visualizador import VisualizadorEvolucao

class IView(ABC):
    """Interface para views da aplicação."""
    
    @abstractmethod
    def exibir_interface(self):
        """Exibe a interface principal da aplicação."""
        pass
    
    @abstractmethod
    def exibir_resultados(self, melhor_algoritmo, estatisticas, caminho_historico):
        """Exibe os resultados da simulação."""
        pass

class StreamlitView(IView):
    """Implementação da interface de visualização usando Streamlit."""
    
    def __init__(self):
        """Inicializa a view."""
        self.visualizador = VisualizadorEvolucao()
        
    def exibir_interface(self):
        """Exibe a interface principal da aplicação."""
        st.title("CodeGenix - Simulador de Evolução de Algoritmos")
        
        st.sidebar.header("Configurações")
        
        # Configurações de entrada
        linguagem = st.sidebar.selectbox(
            "Linguagem de programação",
            ["Python", "JavaScript"]
        )
        
        tamanho_populacao = st.sidebar.slider(
            "Tamanho da população",
            min_value=1,
            max_value=10,
            value=1,
            step=1
        )
        
        geracoes = st.sidebar.slider(
            "Número de gerações",
            min_value=1,
            max_value=5,
            value=1
        )
        
       
        
        st.header("Insira o código inicial")
        codigo_exemplo = '''

def maior_valor(lista):
    """Encontra o maior valor em uma lista."""
    if not lista:
        return None
    maior = lista[0]
    for valor in lista:
        if valor > maior:
            maior = valor
    return maior

'''
        codigo_inicial = st.text_area(
            "Código inicial",
            value=codigo_exemplo,
            height=300,
            help="Insira o código que será usado como base para a evolução"
        )
        
        # Retorna as configurações para o controlador
        return {
            "linguagem": linguagem,
            "tamanho_populacao": tamanho_populacao,
            "geracoes": geracoes,
            "codigo_inicial": codigo_inicial
        }
    
    def exibir_resultados(self, melhor_algoritmo, estatisticas, caminho_historico):
        """Exibe os resultados da simulação."""
        if melhor_algoritmo is None:
            st.error("Não foi possível obter resultados. Verifique os logs para mais detalhes.")
            return
            
        st.header("Resultados da Simulação")
        
        # Exibe estatísticas
        st.subheader("Estatísticas")
        if estatisticas:
            col1, col2, col3 = st.columns(3)
            col2.metric("Melhor Fitness", f"{estatisticas.get('melhor_fitness', 0):.2f}")
            col3.metric("Gerações", estatisticas.get('geracoes', 0))
        
        # Exibe o melhor algoritmo
        st.subheader("Melhor Algoritmo")
        st.code(melhor_algoritmo.codigo, language=melhor_algoritmo.linguagem.lower())
        
        # Exibe métricas do melhor algoritmo
        st.subheader("Métricas do Melhor Algoritmo")
        metricas = melhor_algoritmo.get_metricas()
        if metricas:
            col1, col2, col3 = st.columns(3)
            col1.metric("Eficiência", f"{metricas.get('eficiencia', 0):.2f}")
            col2.metric("Clareza", f"{metricas.get('clareza', 0):.2f}")
            col3.metric("Boas Práticas", f"{metricas.get('boas_praticas', 0):.2f}")
        
        # Exibe gráficos de evolução
        st.subheader("Gráficos de Evolução")
        if os.path.exists(caminho_historico):
            # Carrega os dados para visualização
            if self.visualizador.carregar_dados(caminho_historico):
                # Exporta o gráfico para um arquivo temporário
                grafico_path = "evolucao_temp.png"
                if self.visualizador.exportar_grafico(grafico_path):
                    # Exibe o gráfico
                    st.image(grafico_path)
                    # Remove o arquivo temporário
                    if os.path.exists(grafico_path):
                        os.remove(grafico_path)
                else:
                    st.warning("Não foi possível gerar o gráfico de evolução.")
            else:
                st.warning("Não foi possível carregar os dados de evolução.")
        else:
            st.warning(f"Arquivo de histórico não encontrado: {caminho_historico}")
        
        # Opção para exportar o melhor algoritmo
        st.subheader("Exportar Melhor Algoritmo")
        nome_arquivo = st.text_input("Nome do arquivo", f"melhor_algoritmo.{melhor_algoritmo.linguagem.lower()}")
        
        if st.button("Exportar"):
            try:
                with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
                    arquivo.write(melhor_algoritmo.codigo)
                st.success(f"Algoritmo exportado com sucesso para {nome_arquivo}")
            except Exception as e:
                st.error(f"Erro ao exportar algoritmo: {str(e)}")