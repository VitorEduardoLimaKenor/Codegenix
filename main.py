import streamlit as st
from model.populacao import Populacao
import time
import pandas as pd
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def main():
    st.set_page_config(page_title="Algoritmo Genético", page_icon="🧬", layout="wide")
    
    # Título e descrição
    st.title("🧬 Evolução de Código com Algoritmo Genético")
    st.markdown("""
    Esta aplicação utiliza algoritmos genéticos para evoluir e melhorar automaticamente trechos de código.
    """)
    
    # Sidebar com configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        language = st.selectbox("Linguagem", ["python", "javascript", "java"], index=0)
        pop_size = st.slider("Tamanho da população", 1, 20, 3)
        num_generations = st.slider("Número de gerações", 1, 50, 2)
        mutation_rate = st.slider("Taxa de mutação", 0.0, 1.0, 0.1)
        
    # Área de código base
    st.subheader("📝 Código Base")
    base_code = st.text_area("Insira o código base para evolução:", 
                           """def somar_lista(lista):
    total = 0
    for numero in lista:
        total += numero
    return total""",
                           height=200)
    
    # Espaço para resultados
    result_placeholder = st.empty()
    progress_bar = st.progress(0)
    log_placeholder = st.empty()
    
    # Botão para executar
    if st.button("▶️ Executar Algoritmo Genético"):
        if not base_code.strip():
            st.error("Por favor, insira um código base válido.")
            return
            
        with st.spinner("Executando..."):
            log_messages = []
            
            # Inicialização
            log_messages.append("🔧 Gerando população inicial...")
            log_placeholder.code("\n".join(log_messages))
            progress_bar.progress(5)
            
            pop = Populacao(language)
            pop.gerar_populacao_inicial(base_code, tamanho=pop_size)
            
            # Evolução
            for gen in range(num_generations):
                progress = 5 + int((gen / num_generations) * 90)
                progress_bar.progress(progress)
                
                log_messages.append(f"\n📈 Evoluindo geração {gen + 1}/{num_generations}...")
                log_placeholder.code("\n".join(log_messages))
                
                pop.evoluir()
                
                # Simula um tempo de processamento para visualização
                time.sleep(0.5)
                
                # Atualiza com informações da geração
                log_messages.append(f"✅ Geração {gen + 1} completada!")
                log_placeholder.code("\n".join(log_messages))
            
            # Resultado final
            progress_bar.progress(100)
            log_messages.append("\n🎯 Evolução concluída!")
            log_placeholder.code("\n".join(log_messages))
            
            # Exibe o melhor algoritmo
            st.subheader("🏆 Melhor Algoritmo Encontrado")
            melhor = pop.melhor_individuo()
            if melhor:
                st.code(melhor.codigo, language=language)
                
                # Botão para download
                st.download_button(
                    label="⬇️ Baixar Melhor Algoritmo",
                    data=melhor.codigo,
                    file_name="melhor_algoritmo.py",
                    mime="text/x-python"
                )
            else:
                st.error("Nenhum algoritmo válido foi encontrado na evolução.")
            
            # Estatísticas (simuladas - você pode adaptar com dados reais da sua implementação)
            st.subheader("📊 Estatísticas da Evolução")
            stats_data = {
                "Geração": list(range(1, num_generations+1)),
                "Fitness": [0.8 + (i * 0.05) for i in range(num_generations)],  # Exemplo
                "Diversidade": [0.9 - (i * 0.03) for i in range(num_generations)]  # Exemplo
            }
            stats_df = pd.DataFrame(stats_data)
            st.line_chart(stats_df.set_index("Geração"))

if __name__ == "__main__":
    main()