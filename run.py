#!/usr/bin/env python3
import os
import subprocess
import sys

def main():
    # Verifica se o arquivo .env existe
    if not os.path.exists('.env'):
        print("⚠️ Arquivo .env não encontrado!")
        print("Por favor, crie um arquivo .env com sua chave API da Groq:")
        print("GROQ_API_KEY=sua_chave_api_aqui")
        return

    # Verifica se as dependências estão instaladas
    try:
        import streamlit
        import groq
        import dotenv
        import pandas
    except ImportError as e:
        print("⚠️ Algumas dependências estão faltando!")
        print("Execute: pip install -r requirements.txt")
        return

    # Inicia o servidor Streamlit
    try:
        print("🚀 Iniciando o servidor...")
        subprocess.run(["streamlit", "run", "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Servidor encerrado!")
    except Exception as e:
        print(f"❌ Erro ao iniciar o servidor: {e}")

if __name__ == "__main__":
    main()
