from groq import Groq
import os
import random
from model.algoritmo import Algoritmo
from controller.interfaces import IOperadorGenetico

class OperadorGenetico(IOperadorGenetico):
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def selecionar(self, algoritmos, quantidade=5):
        """Seleciona os melhores algoritmos para reprodução usando seleção por roleta."""
        print(f"[DEBUG] Selecionando entre {len(algoritmos)} algoritmos...")
        
        # Filtra algoritmos com fitness positivo
        algoritmos_validos = [a for a in algoritmos if a.get_fitness() > 0]
        print(f"[DEBUG] Encontrados {len(algoritmos_validos)} algoritmos válidos")

        if not algoritmos_validos:
            # Se não houver algoritmos válidos, retorna os algoritmos originais
            print("[DEBUG] Nenhum algoritmo válido encontrado, usando todos os algoritmos")
            return algoritmos[:quantidade]

        # Ordena por fitness
        algoritmos_validos.sort(key=lambda x: x.get_fitness(), reverse=True)

        # Ajusta quantidade para não exceder o número de válidos
        quantidade = min(quantidade, len(algoritmos_validos))

        return self._selecao_roleta(algoritmos_validos, quantidade)
        
    def _selecao_roleta(self, algoritmos_validos, quantidade):
        """Método privado que implementa a seleção por roleta."""
        fitness_total = sum(a.get_fitness() for a in algoritmos_validos)

        selecionados = []
        usados = set()

        while len(selecionados) < quantidade:
            r = random.random()
            soma = 0
            for i, a in enumerate(algoritmos_validos):
                if i in usados:
                    continue  # pula algoritmos já usados
                prob = a.get_fitness() / fitness_total
                soma += prob
                if r <= soma:
                    selecionados.append(a)
                    usados.add(i)
                    break

        return selecionados


    def cruzar(self, pai1, pai2):
        """Cruza dois algoritmos para gerar um novo."""
        novo_codigo = self._gerar_codigo_cruzado(pai1.codigo, pai2.codigo)
        return Algoritmo(id=random.randint(1000, 9999), linguagem=pai1.linguagem, codigo=novo_codigo)
        
    def _gerar_codigo_cruzado(self, codigo1, codigo2):
        """Método privado que usa a API para gerar um código cruzado a partir de dois códigos."""
        prompt = f"""
        Você é um otimizador de código.
        Combine os dois algoritmos a seguir, criando uma versão que preserve o objetivo de ambos e que seja eficiente.
        Algoritmo 1:
        {codigo1}
        Algoritmo 2:
        {codigo2}
        ⚠️ Responda apenas com Resultado (código):
        """
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[Erro ao cruzar algoritmos]: {str(e)}")
            # Em caso de erro, retorna uma combinação simples dos códigos
            return f"""# Código combinado (fallback por erro na API)
# Algoritmo 1:
{codigo1}

# Algoritmo 2:
{codigo2}"""

    def mutar(self, algoritmo):
        """Aplica mutação em um algoritmo."""
        novo_codigo = self._gerar_codigo_mutado(algoritmo.codigo)
        return Algoritmo(id=random.randint(1000, 9999), linguagem=algoritmo.linguagem, codigo=novo_codigo)
        
    def _gerar_codigo_mutado(self, codigo):
        """Método privado que usa a API para gerar uma mutação de um código."""
        prompt = f"""
        Você é um otimizador de código.
        Melhore o seguinte código com pequenas alterações que aumentem a eficiência ou simplifiquem a lógica.

        Código:
        {codigo}

        ⚠️ Responda apenas com Resultado (código otimizado apenas):
        """
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=200
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[Erro ao mutar algoritmo]: {str(e)}")
            # Em caso de erro, retorna o código original com um pequeno comentário
            return f"""# Código original (falha na mutação){codigo}"""

    def gerar_variacoes_iniciais(self, codigo_base: str, linguagem: str, quantidade: int = 10):
        """Gera variações iniciais de um código base."""
        try:
            variacoes = self._obter_variacoes_da_api(codigo_base, linguagem, quantidade)
            
            # Se não conseguiu obter variações suficientes da API, cria variações simples
            if len(variacoes) < quantidade:
                variacoes.extend(self._criar_variacoes_simples(codigo_base, linguagem, quantidade - len(variacoes)))
                
            return variacoes[:quantidade]  # Garante que não ultrapasse a quantidade solicitada
            
        except Exception as e:
            print(f"[Erro ao gerar variações]: {str(e)}")
            # Em caso de erro, cria variações simples
            return self._criar_variacoes_simples(codigo_base, linguagem, quantidade)
    
    def _obter_variacoes_da_api(self, codigo_base, linguagem, quantidade):
        """Método privado que usa a API para gerar variações de um código."""
        variacoes = []
        
        # Primeiro, adicione o código base como primeira variação para garantir que tenhamos pelo menos uma
        from model.algoritmo import Algoritmo
        variacoes.append(Algoritmo(id=1000, linguagem=linguagem, codigo=codigo_base))
        
        # Salva o código original como backup para uso futuro
        try:
            with open("./utils/algoritmo_original.py", "w", encoding="utf-8") as f:
                f.write(codigo_base)
        except Exception as e:
            print(f"[AVISO] Não foi possível salvar o código original: {str(e)}")
        
        try:
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
            print("[INFO] Resposta da API recebida com sucesso")
        except Exception as e:
            print(f"[ERRO] Falha ao chamar API para variações: {str(e)}")
            return variacoes  # Retorna apenas o código original

        # Separar versões (ex: separadas por comentários ou blocos)
        blocos = resposta.split("```")
        for i, bloco in enumerate(blocos):
            if linguagem in bloco:
                codigo = bloco.split(linguagem)[-1].strip()
                variacoes.append(Algoritmo(id=1000+i, linguagem=linguagem, codigo=codigo))
                if len(variacoes) >= quantidade:
                    break
                    
        return variacoes
        
    def _criar_variacoes_simples(self, codigo_base, linguagem, quantidade):
        """Método privado que cria variações simples de um código (fallback)."""
        variacoes = []
        
        # Cria uma variação com o código original
        variacoes.append(Algoritmo(id=1000, linguagem=linguagem, codigo=codigo_base))
        
        # Cria variações simples adicionando comentários ou pequenas modificações
        for i in range(1, quantidade):
            codigo_modificado = f"""# Variação {i} do algoritmo original# Gerada automaticamente{codigo_base}"""
            variacoes.append(Algoritmo(id=1000+i, linguagem=linguagem, codigo=codigo_modificado))
            
        return variacoes
