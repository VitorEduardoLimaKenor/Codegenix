import os
import json
import re
import time
from groq import Groq
from datetime import datetime
from controller.interfaces import IAvaliador

class AvaliadorService(IAvaliador):
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        self.model = "llama-3.1-8b-instant"
        self.historico_avaliacoes = []
        self.geracao_atual = 0
        self.modo_offline = self.api_key is None
        self.max_retries = 3
        self.retry_delay = 2

    def avaliar(self, algoritmo):
        """Avalia um algoritmo e atualiza seu fitness e métricas."""
        try:
            # Obtém as notas do algoritmo usando a API
            notas = self._obter_notas_algoritmo(algoritmo.codigo)
            
            # Calcula o fitness como média das notas
            fitness = round((notas["eficiencia"] + notas["clareza"] + notas["boas_praticas"]) / 3)
            
            # Atualiza o algoritmo com as notas obtidas
            algoritmo.set_fitness(fitness)
            algoritmo.set_metricas({
                "eficiencia": notas["eficiencia"],
                "clareza": notas["clareza"],
                "boas_praticas": notas["boas_praticas"]
            })

            # Salva a avaliação no histórico
            self._registrar_avaliacao(algoritmo)

            print(f"[DEBUG] Fitness calculado: {algoritmo.get_fitness()}")

        except Exception as e:
            print(f"[Erro ao avaliar algoritmo]: {str(e)}")
            print(f"[DEBUG] Código que causou erro: {algoritmo.codigo}")
            # Define um fitness mínimo para evitar o erro de seleção
            algoritmo.set_fitness(1)
            algoritmo.set_metricas({
                "eficiencia": 1,
                "clareza": 1,
                "boas_praticas": 1
            })
            
    def _obter_notas_algoritmo(self, codigo):
        """Método privado para obter as notas de um algoritmo usando a API."""
        if self.modo_offline:
            return self._gerar_notas_offline(codigo)
            
        prompt = f"""
        Avalie o código abaixo em três critérios: eficiência, clareza e boas práticas. Para cada critério, atribua uma nota de 0 a 100.

        ⚠️ Responda apenas no seguinte formato JSON e **sem explicações**:

        {{
        "eficiencia": <nota>,
        "clareza": <nota>,
        "boas_praticas": <nota>
        }}

        Código:
        {codigo}
        """

        # Implementação com retry
        for tentativa in range(self.max_retries):
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
                json_match = re.search(r'\{[^}]+\}', resposta)
                if json_match:
                    resposta = json_match.group(0)

                # Extrai JSON da resposta
                notas = json.loads(resposta)

                # Garante que todas as notas são números
                return {
                    k: float(v) if isinstance(v, (int, float, str)) else 0
                    for k, v in notas.items()
                }
                
            except Exception as e:
                print(f"[AVISO] Tentativa {tentativa+1}/{self.max_retries} falhou: {str(e)}")
                if tentativa < self.max_retries - 1:
                    time.sleep(self.retry_delay)  # Espera antes de tentar novamente
                else:
                    print("[AVISO] Todas as tentativas falharam, usando modo offline")
                    return self._gerar_notas_offline(codigo)
        
        # Fallback final (não deveria chegar aqui, mas por segurança)
        return self._gerar_notas_offline(codigo)
        
    def _gerar_notas_offline(self, codigo):
        """Gera notas localmente quando a API não está disponível."""
        print("[INFO] Usando avaliação offline (simulada)")
        
        # Análise básica do código para gerar notas simuladas
        linhas = codigo.strip().split('\n')
        linhas_codigo = [l for l in linhas if l.strip() and not l.strip().startswith('#')]
        
        # Métricas básicas
        num_linhas = len(linhas_codigo)
        tem_docstring = '"""' in codigo or "'''" in codigo
        tem_comentarios = any(l.strip().startswith('#') for l in linhas)
        
        # Heurísticas simples para avaliar o código
        eficiencia = min(80, 100 - (num_linhas * 2)) if num_linhas > 0 else 40
        clareza = 80 if tem_docstring else (60 if tem_comentarios else 40)
        boas_praticas = 60 if tem_docstring else (40 if tem_comentarios else 20)
        
        # Adiciona alguma variação aleatória
        import random
        eficiencia = max(20, min(100, eficiencia + random.randint(-10, 10)))
        clareza = max(20, min(100, clareza + random.randint(-10, 10)))
        boas_praticas = max(10, min(100, boas_praticas + random.randint(-10, 10)))
        
        notas = {
            "eficiencia": eficiencia,
            "clareza": clareza,
            "boas_praticas": boas_praticas
        }
        
        print(f"[DEBUG] Avaliação offline: {notas}")
        return notas
        
    def _registrar_avaliacao(self, algoritmo):
        """Método privado para registrar a avaliação no histórico."""
        avaliacao = {
            "geracao": self.geracao_atual,
            "fitness": algoritmo.get_fitness(),
            "metricas": algoritmo.metricas,
            "timestamp": datetime.now().isoformat()
        }
        self.historico_avaliacoes.append(avaliacao)

    def salvar_historico(self, caminho="./utils/historico_avaliacoes.json"):
        """Salva o histórico de avaliações em um arquivo JSON."""
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(self.historico_avaliacoes, f, indent=2, ensure_ascii=False)

    def carregar_historico(self, caminho="./utils/historico_avaliacoes.json"):
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
