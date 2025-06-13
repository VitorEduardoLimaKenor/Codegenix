# CodeGenix - Simulador de Evolução de Algoritmos

## Sobre o Projeto

O CodeGenix é um simulador de evolução de códigos baseado em algoritmos genéticos. Ele permite que usuários submetam algoritmos para otimização automática através de princípios de evolução genética (seleção, mutação e cruzamento). A aplicação utiliza a API da Groq para avaliar e gerar variações de código.

## Integrantes do grupo

- Pedro Chastalo
- Vitor Eduardo
- Mayara Rodruigues
- Winicius dos passos
- Marcus Nunes

## Arquitetura MVC e Princípios SOLID

O projeto foi estruturado seguindo o padrão de arquitetura MVC (Model-View-Controller) e os princípios SOLID de design de software, proporcionando uma base sólida para manutenção e extensão.

### Estrutura do Projeto

```
codegenix/
├── model/                  # Camada de modelo
│   ├── algoritmo.py        # Classe que representa um algoritmo
│   └── populacao.py        # Classe que gerencia a população de algoritmos
├── controller/             # Camada de controlador
│   ├── interfaces.py       # Interfaces para inversão de dependência
│   ├── avaliador_service.py # Serviço de avaliação de algoritmos
│   ├── operador_genetico.py # Implementa operações genéticas
│   └── simulacao_controller.py # Controlador principal da simulação
├── view/                   # Camada de visualização
│   ├── visualizador.py     # Visualização gráfica da evolução
│   └── streamlit_view.py   # Interface de usuário com Streamlit
├── main.py                 # Ponto de entrada da aplicação web
├── run.py                  # Script para iniciar a aplicação
├── requirements.txt        # Dependências do projeto
└── .env                    # Arquivo de configuração (não versionado)
```

### Princípios SOLID Aplicados

1. **S - Princípio da Responsabilidade Única**
   - Cada classe tem uma única responsabilidade:
     - `Algoritmo`: Representa um algoritmo e suas propriedades
     - `Populacao`: Gerencia a população de algoritmos
     - `AvaliadorService`: Avalia algoritmos usando a API Groq
     - `OperadorGenetico`: Implementa operações genéticas (seleção, cruzamento, mutação)
     - `VisualizadorEvolucao`: Visualiza a evolução dos algoritmos
     - `StreamlitView`: Gerencia a interface do usuário

2. **O - Princípio Aberto/Fechado**
   - As classes são abertas para extensão, mas fechadas para modificação:
     - Novas implementações de avaliadores podem ser criadas implementando a interface `IAvaliador`
     - Novos operadores genéticos podem ser criados implementando a interface `IOperadorGenetico`
     - Novas visualizações podem ser criadas implementando a interface `IVisualizador`

3. **L - Princípio da Substituição de Liskov**
   - As implementações das interfaces podem ser substituídas sem afetar o funcionamento do sistema:
     - Qualquer implementação de `IAvaliador` pode ser usada na classe `Populacao`
     - Qualquer implementação de `IOperadorGenetico` pode ser usada na classe `Populacao`

4. **I - Princípio da Segregação de Interface**
   - Interfaces específicas para cada tipo de componente:
     - `IAvaliador`: Define o contrato para avaliadores
     - `IOperadorGenetico`: Define o contrato para operadores genéticos
     - `IVisualizador`: Define o contrato para visualizadores
     - `IView`: Define o contrato para interfaces de usuário

5. **D - Princípio da Inversão de Dependência**
   - As classes dependem de abstrações, não de implementações concretas:
     - `Populacao` depende de `IAvaliador` e `IOperadorGenetico`, não de implementações específicas
     - `SimulacaoController` pode receber qualquer implementação de `IAvaliador` e `IOperadorGenetico`

## Funcionalidades

- **Geração de População Inicial**: Cria uma população inicial de algoritmos a partir de um código base.
- **Avaliação de Algoritmos**: Avalia os algoritmos com base em eficiência, clareza e boas práticas usando a API Groq.
- **Evolução de Algoritmos**: Aplica seleção, cruzamento e mutação para evoluir a população.
- **Visualização da Evolução**: Gera gráficos mostrando a evolução do fitness e métricas ao longo das gerações.
- **Exportação do Melhor Algoritmo**: Permite salvar o melhor algoritmo encontrado.

## Fluxo de Execução

1. O usuário insere um código inicial e configura parâmetros da simulação na interface.
2. O controlador `SimulacaoController` orquestra o processo de evolução:
   - Cria uma população inicial usando o `OperadorGenetico`
   - Avalia os algoritmos usando o `AvaliadorService`
   - Evolui a população por várias gerações
   - Retorna o melhor algoritmo e estatísticas
3. A visualização `StreamlitView` exibe os resultados e gráficos de evolução.

## Requisitos e Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Chave de API da Groq

### Instalação

1. Clone o repositório:
   ```
   git clone [url-do-repositorio]
   cd codegenix
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Configure a chave de API da Groq:
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione sua chave API: `GROQ_API_KEY=sua_chave_api_aqui`

### Execução

Para iniciar a aplicação:

```
python run.py
```

Ou diretamente com Streamlit:

```
streamlit run main.py
```

## Extensibilidade

O projeto foi projetado para ser facilmente extensível:

- **Novos Avaliadores**: Implemente a interface `IAvaliador` para criar novos métodos de avaliação.
- **Novos Operadores Genéticos**: Implemente a interface `IOperadorGenetico` para criar novos operadores.
- **Novas Visualizações**: Implemente a interface `IVisualizador` para criar novas formas de visualização.
- **Novas Interfaces**: Implemente a interface `IView` para criar novas interfaces de usuário.

## Tratamento de Erros

O sistema implementa tratamento robusto de erros em vários níveis:

- **Validação de Entrada**: Verifica se o código inicial e parâmetros são válidos.
- **Tratamento de Exceções da API**: Lida com falhas na comunicação com a API Groq.
- **Fallbacks**: Implementa alternativas quando operações principais falham.
- **Logging**: Registra informações e erros para facilitar a depuração.

## Conclusão

O CodeGenix demonstra como princípios de design de software como MVC e SOLID podem ser aplicados para criar uma aplicação robusta, extensível e fácil de manter. A arquitetura modular permite que novas funcionalidades sejam adicionadas com mínimo impacto no código existente.
