import os
import json
from groq import Groq
from datetime import datetime

class AvaliadorService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.1-8b-instant"
        self.historico_avaliacoes = []
        self.geracao_atual = 0

    def avaliar(self, algoritmo):
        prompt = f"""
        Avalie o código abaixo em três critérios: eficiência, clareza e boas práticas. Para cada critério, atribua uma nota de 0 a 100.

        ⚠️ Responda apenas no seguinte formato JSON e **sem explicações**:

        {{
        "eficiencia": <nota>,
        "clareza": <nota>,
        "boas_praticas": <nota>
        }}

        Código:
        {algoritmo.codigo}
        """

        try:
            print("[DEBUG] Enviando requisição para a API da Groq...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )

            resposta = response.choices[0].message.content.strip()
            print(f"[DEBUG] Resposta da API: {resposta}")

            # Tenta extrair o JSON da resposta, mesmo se houver texto adicional
            import re
            json_match = re.search(r'\{[^}]+\}', resposta)
            if json_match:
                resposta = json_match.group(0)

            # Extrai JSON da resposta
            notas = json.loads(resposta)

            # Garante que todas as notas são números
            notas = {
                k: float(v) if isinstance(v, (int, float, str)) else 0
                for k, v in notas.items()
            }

            algoritmo.fitness = round((notas["eficiencia"] + notas["clareza"] + notas["boas_praticas"]) / 3)
            algoritmo.metricas = {
                "eficiencia": notas["eficiencia"],
                "clareza": notas["clareza"],
                "boas_praticas": notas["boas_praticas"]
            }

            # Salva a avaliação no histórico
            avaliacao = {
                "geracao": self.geracao_atual,
                "fitness": algoritmo.fitness,
                "metricas": algoritmo.metricas,
            }
            self.historico_avaliacoes.append(avaliacao)

            print(f"[DEBUG] Fitness calculado: {algoritmo.fitness}")

        except Exception as e:
            print(f"[Erro ao avaliar algoritmo]: {str(e)}")
            print(f"[DEBUG] Código que causou erro: {algoritmo.codigo}")
            # Define um fitness mínimo para evitar o erro de seleção
            algoritmo.fitness = 1
            algoritmo.metricas = {
                "eficiencia": 1,
                "clareza": 1,
                "boas_praticas": 1
            }

    def salvar_historico(self, caminho="historico_avaliacoes.json"):
        """Salva o histórico de avaliações em um arquivo JSON."""
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(self.historico_avaliacoes, f, indent=2, ensure_ascii=False)

    def carregar_historico(self, caminho="historico_avaliacoes.json"):
        """Carrega o histórico de avaliações de um arquivo JSON."""
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                self.historico_avaliacoes = json.load(f)
        except FileNotFoundError:
            print(f"[AVISO] Arquivo de histórico não encontrado: {caminho}")

    def set_geracao(self, geracao):
        """Define a geração atual para as próximas avaliações."""
        self.geracao_atual = geracao

    def get_metricas_geracao(self, geracao=None):
        """Retorna as métricas médias de uma geração específica."""
        if geracao is None:
            geracao = self.geracao_atual

        avaliacoes_geracao = [a for a in self.historico_avaliacoes if a['geracao'] == geracao]
        
        if not avaliacoes_geracao:
            return None

        num_avaliacoes = len(avaliacoes_geracao)
        soma_metricas = {
            'fitness': 0,
            'eficiencia': 0,
            'clareza': 0,
            'boas_praticas': 0
        }

        melhor_fitness = float('-inf')
        melhor_codigo = None

        for av in avaliacoes_geracao:
            soma_metricas['fitness'] += av['fitness']
            soma_metricas['eficiencia'] += av['metricas']['eficiencia']
            soma_metricas['clareza'] += av['metricas']['clareza']
            soma_metricas['boas_praticas'] += av['metricas']['boas_praticas']

            if av['fitness'] > melhor_fitness:
                melhor_fitness = av['fitness']
                melhor_codigo = av['codigo']

        return {
            'geracao': geracao,
            'num_avaliacoes': num_avaliacoes,
            'media_fitness': round(soma_metricas['fitness'] / num_avaliacoes, 2),
            'media_eficiencia': round(soma_metricas['eficiencia'] / num_avaliacoes, 2),
            'media_clareza': round(soma_metricas['clareza'] / num_avaliacoes, 2),
            'media_boas_praticas': round(soma_metricas['boas_praticas'] / num_avaliacoes, 2),
            'melhor_fitness': melhor_fitness,
            'melhor_codigo': melhor_codigo
        }
