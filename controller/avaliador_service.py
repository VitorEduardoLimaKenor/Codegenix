import os
from groq import Groq

class AvaliadorService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.1-8b-instant"

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

            import json
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

            print(f"[DEBUG] Fitness calculado: {algoritmo.fitness}")

        except Exception as e:
            print(f"[Erro ao avaliar algoritmo]: {str(e)}")
            print(f"[DEBUG] Código que causou erro: {algoritmo.codigo}")
            # Define um fitness mínimo para evitar o erro de seleção
           
            algoritmo.metricas = {
                "eficiencia": 1,
                "clareza": 1,
                "boas_praticas": 1
            }
