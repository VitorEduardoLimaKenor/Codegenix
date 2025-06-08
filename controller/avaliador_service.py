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
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )

            import json
            resposta = response.choices[0].message.content.strip()

            # Extrai JSON da resposta
            notas = json.loads(resposta)

            algoritmo.fitness = round((notas["eficiencia"] + notas["clareza"] + notas["boas_praticas"]) / 3)
            algoritmo.metricas = {
                "eficiencia": notas["eficiencia"],
                "clareza": notas["clareza"],
                "boas_praticas": notas["boas_praticas"]
            }

        except Exception as e:
            print(f"[Erro ao avaliar algoritmo]: {e}")
            algoritmo.fitness = 0
            algoritmo.metricas = {
                "eficiencia": 0,
                "clareza": 0,
                "boas_praticas": 0
            }
