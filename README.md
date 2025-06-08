# 🧬 CodeGenix

**CodeGenix** é um simulador de evolução de algoritmos que utiliza **algoritmos genéticos** aliados ao poder de uma **LLM (Large Language Model)** para gerar, avaliar e aprimorar automaticamente soluções em código-fonte com base em critérios de qualidade como eficiência, clareza e boas práticas.

---

## 📌 Visão Geral

> A ideia é iniciar com um código base e, por meio de **mutações**, **cruzamentos** e **seleções inteligentes**, gerar códigos cada vez melhores — tudo isso de forma automatizada.

---

## 🗂️ Estrutura do Projeto

<pre lang="markdown"> ``` codegenix/ │ ├── main.py # Ponto de entrada principal │ ├── model/ │ └── populacao.py # Classe que gerencia a população de algoritmos │ ├── controller/ │ ├── operador_genetico.py # Operações genéticas: seleção, cruzamento e mutação │ └── avaliador_service.py # Avaliação dos algoritmos via LLM │ ├── utils/ │ └── # Utilitários (adicionar descrição ou arquivos) │ ├── view/ │ └── # Interface ou apresentação (adicionar descrição ou arquivos) │ ├── .env # Variáveis de ambiente │ ├── requirements.txt # Requisitos do projeto │ └── README.md # Este arquivo ``` </pre>

---

## ⚙️ Componentes Principais

### `Populacao` (`model/populacao.py`)
Gerencia a população de algoritmos:

- Geração inicial usando uma LLM.
- Evolução por cruzamento e mutação.
- Avaliação de algoritmos por métrica.
- Salvamento do melhor código.

### `OperadorGenetico` (`controller/operador_genetico.py`)
Executa as operações genéticas:

- **Seleção:** roleta baseada no fitness.
- **Cruzamento:** combinação de dois algoritmos.
- **Mutação:** alteração leve do código.

### `AvaliadorService` (`controller/avaliador_service.py`)
Avalia cada algoritmo com base em:

- ✔️ Eficiência
- ✔️ Clareza
- ✔️ Boas práticas

Essas métricas são pontuadas de 0 a 100. A média delas determina o **fitness** do código.

---

## 📈 Métricas Avaliadas

| Métrica         | Descrição                                               |
|-----------------|---------------------------------------------------------|
| **Eficiência**  | Desempenho e uso otimizado de recursos                  |
| **Clareza**     | Legibilidade e simplicidade do código                   |
| **Boas práticas** | Uso de padrões, nomenclatura, estrutura e modularidade |

As métricas são armazenadas por geração, permitindo a criação de gráficos de evolução.

---

## ▶️ Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/codegenix.git
   cd codegenix

2. Instale os requisitos: 
    pip install -r requirements.txt
