#!/usr/bin/env python3
import os
import subprocess
import sys
import logging

# Configura o logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('codegenix')

def verificar_ambiente():
    """Verifica se o ambiente está corretamente configurado."""
    # Verifica se o arquivo .env existe
    if not os.path.exists('.env'):
        logger.error("Arquivo .env não encontrado!")
        print("⚠️ Arquivo .env não encontrado!")
        print("Por favor, crie um arquivo .env com sua chave API da Groq:")
        print("GROQ_API_KEY=sua_chave_api_aqui")
        return False

    # Verifica se as dependências estão instaladas
    try:
        import streamlit
        import groq
        import dotenv
        import pandas
        import matplotlib
        import seaborn
        return True
    except ImportError as e:
        logger.error(f"Dependência faltando: {e}")
        print("⚠️ Algumas dependências estão faltando!")
        print("Execute: pip install -r requirements.txt")
        return False

def main():
    """Função principal que inicia a aplicação."""
    logger.info("Iniciando CodeGenix - Simulador de Evolução de Algoritmos")
    
    # Verifica o ambiente
    if not verificar_ambiente():
        return

    # Inicia o servidor Streamlit
    try:
        print("🚀 Iniciando o servidor...")
        logger.info("Iniciando servidor Streamlit")
        subprocess.run(["streamlit", "run", "main.py"], check=True)
    except KeyboardInterrupt:
        logger.info("Servidor encerrado pelo usuário")
        print("\n👋 Servidor encerrado!")
    except Exception as e:
        logger.error(f"Erro ao iniciar o servidor: {e}")
        print(f"❌ Erro ao iniciar o servidor: {e}")

if __name__ == "__main__":
    main()
