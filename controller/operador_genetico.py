from groq import Groq
import os
import random
from model.algoritmo import Algoritmo

class OperadorGenetico:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def selecionar(self, algoritmos, quantidade=5):
        print(f"[DEBUG] Selecionando entre {len(algoritmos)} algoritmos...")
        # Filtra algoritmos com fitness positivo
        algoritmos_validos = [a for a in algoritmos if a.fitness is not None and a.fitness > 0]
        print(f"[DEBUG] Encontrados {len(algoritmos_validos)} algoritmos válidos")

        if not algoritmos_validos:
            # Se não houver algoritmos válidos, retorna os algoritmos originais
            print("[DEBUG] Nenhum algoritmo válido encontrado, usando todos os algoritmos")
            return algoritmos[:quantidade]

        # Ordena por fitness
        algoritmos_validos.sort(key=lambda x: x.fitness, reverse=True)

        # Ajusta quantidade para não exceder o número de válidos
        quantidade = min(quantidade, len(algoritmos_validos))

        fitness_total = sum(a.fitness for a in algoritmos_validos)

        selecionados = []
        usados = set()

        while len(selecionados) < quantidade:
            r = random.random()
            soma = 0
            for i, a in enumerate(algoritmos_validos):
                if i in usados:
                    continue  # pula algoritmos já usados
                prob = a.fitness / fitness_total
                soma += prob
                if r <= soma:
                    selecionados.append(a)
                    usados.add(i)
                    break

        return selecionados


    def cruzar(self, pai1, pai2):
        prompt = f"""
        Você é um otimizador de código.
        Combine os dois algoritmos a seguir, criando uma versão que preserve o objetivo de ambos e que seja eficiente.
        Algoritmo 1:
        {pai1.codigo}
        Algoritmo 2:
        {pai2.codigo}
        ⚠️ Responda apenas com Resultado (código):
        """
        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        novo_codigo = response.choices[0].message.content.strip()
        return pai1.__class__(id=random.randint(1000, 9999), linguagem=pai1.linguagem, codigo=novo_codigo)

    def mutar(self, algoritmo):
        prompt = f"""
        Você é um otimizador de código.
        Melhore o seguinte código com pequenas alterações que aumentem a eficiência ou simplifiquem a lógica.

        Código:
        {algoritmo.codigo}

        ⚠️ Responda apenas com Resultado (código otimizado apenas):
        """
        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=200
        )
        novo_codigo = response.choices[0].message.content.strip()
        return algoritmo.__class__(id=random.randint(1000, 9999), linguagem=algoritmo.linguagem, codigo=novo_codigo)

    def gerar_variacoes_iniciais(self, codigo_base: str, linguagem: str, quantidade: int = 10):
        variacoes = []

        prompt = f"""
        Você é um gerador de variações de código.
        Receba um algoritmo em {linguagem} e crie {quantidade} variações ligeiramente diferentes dele.
        Cada variação deve manter o comportamento original, mas pode ser mais legível, organizada.

        Código base:
        {codigo_base}

        ⚠️ Responda apenas com Resultado (código):
        """
        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=3000,
        )
        resposta = response.choices[0].message.content.strip()

        # Separar versões (ex: separadas por comentários ou blocos)
        blocos = resposta.split("```")
        for i, bloco in enumerate(blocos):
            if linguagem in bloco:
                codigo = bloco.split(linguagem)[-1].strip()
                variacoes.append(Algoritmo(id=1000+i, linguagem=linguagem, codigo=codigo))
                if len(variacoes) >= quantidade:
                    break

        return variacoes
