# Inicialização do Projeto CodeGenix

## Pré-requisitos
- Python 3.x
- pip (gerenciador de pacotes Python)

## Passos para Inicialização

1. Clone o repositório:
```bash
git clone <seu-repositorio>
cd codegenix
```

2. Configure o ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure a chave API da Groq:
- Crie um arquivo `.env` na raiz do projeto
- Adicione sua chave API:
```
GROQ_API_KEY=sua_chave_api_aqui
```

## Executando o Projeto

Para iniciar o aplicativo, simplesmente execute:
```bash
python run.py
```

O aplicativo estará disponível em `http://localhost:8501`
