import streamlit as st
from dotenv import load_dotenv
from view.streamlit_view import StreamlitView
from controller.simulacao_controller import SimulacaoController

# Carrega as variáveis de ambiente
load_dotenv()

# Configura a página
st.set_page_config(page_title="CodeGenix - Simulador de Evolução de Algoritmos", layout="wide")

def main():
    """Função principal que inicia a aplicação."""
    # Cria a view e o controlador
    view = StreamlitView()
    controller = SimulacaoController()
    
    # Exibe a interface e obtém as configurações
    config = view.exibir_interface()
    
    # Botão para iniciar a simulação
    if st.button("Iniciar Simulação"):
        if not config["codigo_inicial"].strip():
            st.error("Por favor, insira um código inicial.")
        else:
            with st.spinner("Executando simulação..."):
                # Inicia a simulação
                melhor_algoritmo, estatisticas, caminho_historico = controller.iniciar_simulacao(
                    codigo_inicial=config["codigo_inicial"],
                    linguagem=config["linguagem"],
                    tamanho_populacao=config["tamanho_populacao"],
                    geracoes=config["geracoes"],
                )
                
                # Exibe os resultados
                view.exibir_resultados(melhor_algoritmo, estatisticas, caminho_historico)

if __name__ == "__main__":
    main()