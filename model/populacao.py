class Populacao:
    """Classe que representa uma população de algoritmos.
    
    Responsabilidades:
    - Gerenciar um conjunto de algoritmos
    - Controlar o processo de evolução através de gerações
    """
    def __init__(self, linguagem: str, tamanho: int = 5):
        self.algoritmos = []
        self.linguagem = linguagem
        self.geracao = 0
        self.tamanho = tamanho
        self.avaliador = None  
        self.operador = None   

    def set_avaliador(self, avaliador):
        """Define o avaliador a ser utilizado."""
        self.avaliador = avaliador
        
    def set_operador(self, operador):
        """Define o operador genético a ser utilizado."""
        self.operador = operador
        
    def gerar_populacao_inicial(self, codigo_base: str, tamanho: int = None):
        """Gera a população inicial de algoritmos a partir de um código base."""
        from model.algoritmo import Algoritmo
        
        if self.avaliador is None or self.operador is None:
            raise ValueError("Avaliador e Operador devem ser definidos antes de gerar a população inicial")
            
        # Permite sobrescrever o tamanho na chamada, se necessário
        if tamanho is not None:
            self.tamanho = tamanho

        # Atualiza a geração atual no avaliador (geração inicial = 0)
        self.avaliador.set_geracao(self.geracao)

        # Salva o código base como backup
        try:
            with open("./utils/algoritmo_original.py", "w", encoding="utf-8") as f:
                f.write(codigo_base)
        except Exception as e:
            print(f"[AVISO] Não foi possível salvar o código original: {str(e)}")

        try:
            # Tenta gerar variações com o operador genético
            variacoes = self.operador.gerar_variacoes_iniciais(
                codigo_base=codigo_base,
                linguagem=self.linguagem,
                quantidade=self.tamanho
            )
            
            # Verifica se temos variações suficientes
            if len(variacoes) < 1:
                print("[AVISO] Nenhuma variação foi gerada pelo operador genético")
                # Cria pelo menos um algoritmo com o código original
                algoritmo_original = Algoritmo(id=999, linguagem=self.linguagem, codigo=codigo_base)
                variacoes = [algoritmo_original]
                
            self.algoritmos = variacoes

            # Avalia cada algoritmo da geração inicial
            for algoritmo in self.algoritmos:
                try:
                    self.avaliador.avaliar(algoritmo)
                except Exception as e:
                    print(f"[ERRO] Falha ao avaliar algoritmo: {str(e)}")
                    # Define um fitness padrão para evitar problemas
                    algoritmo.set_fitness(50)
            
            # Salva o histórico da geração inicial
            try:
                self.avaliador.salvar_historico()
            except Exception as e:
                print(f"[ERRO] Falha ao salvar histórico: {str(e)}")
                
        except Exception as e:
            print(f"[ERRO] Falha ao gerar população inicial: {str(e)}")
            # Cria uma população mínima com o código original
            algoritmo_original = Algoritmo(id=999, linguagem=self.linguagem, codigo=codigo_base)
            algoritmo_original.set_fitness(50)  # Define um fitness padrão
            self.algoritmos = [algoritmo_original]
            print("[INFO] Criada população mínima com o código original")

    def evoluir(self, num_geracoes: int = 3):
        """Evolui a população por um número específico de gerações."""
        if self.avaliador is None or self.operador is None:
            raise ValueError("Avaliador e Operador devem ser definidos antes de evoluir a população")
            
        if not self.algoritmos:
            raise ValueError("A população inicial deve ser gerada antes de evoluir")
            
        # Guarda o algoritmo original com melhor fitness como backup
        algoritmo_original = self.melhor_individuo()
            
        for _ in range(num_geracoes):
            # Incrementa a geração antes de começar
            self.geracao += 1
            self.avaliador.set_geracao(self.geracao)

            # Seleciona os melhores para cruzar
            selecionados = self.operador.selecionar(self.algoritmos, quantidade=self.tamanho)

            nova_geracao = []
            for i in range(0, len(selecionados), 2):
                if i + 1 < len(selecionados):
                    try:
                        filho = self.operador.cruzar(selecionados[i], selecionados[i + 1])
                        filho = self.operador.mutar(filho)
                        self.avaliador.avaliar(filho)
                        nova_geracao.append(filho)
                    except Exception as e:
                        print(f"[ERRO] Falha ao processar algoritmo: {str(e)}")
                        # Em caso de erro, adiciona um dos algoritmos originais
                        nova_geracao.append(selecionados[i])

            # Se a nova geração estiver vazia, mantém a geração anterior
            if not nova_geracao:
                print("[AVISO] Nova geração vazia, mantendo algoritmos anteriores")
            else:
                self.algoritmos = nova_geracao

            # Salva o histórico da geração atual
            self.avaliador.salvar_historico()
            
        # Se no final da evolução não houver algoritmos, restaura o original
        if not self.algoritmos and algoritmo_original:
            self.algoritmos = [algoritmo_original]

    def melhor_individuo(self):
        """Retorna o melhor indivíduo da população atual."""
        if not self.algoritmos:
            return None
        return max(self.algoritmos, key=lambda a: a.get_fitness())

    def salvar_melhor_algoritmo(self, caminho="melhor_algoritmo.py"):
        """Salva o melhor algoritmo da população em um arquivo."""
        from model.algoritmo import Algoritmo
        
        if not self.algoritmos:
            print("[AVISO] Nenhum algoritmo na população para salvar.")
            # Verifica se existe um arquivo de backup com o algoritmo original
            try:
                with open("./utils/algoritmo_original.py", "r", encoding="utf-8") as f:
                    codigo_original = f.read()
                    print("[INFO] Usando algoritmo original como fallback")
                    
                    # Cria um novo algoritmo com o código original
                    algoritmo = Algoritmo(id=999, linguagem=self.linguagem, codigo=codigo_original)
                    algoritmo.set_fitness(50)  # Fitness padrão
                    
                    # Salva o algoritmo original
                    with open(caminho, "w", encoding="utf-8") as f:
                        f.write(f"# Algoritmo original (não otimizado)\n")
                        f.write(codigo_original)
                    return True
            except FileNotFoundError:
                print("[ERRO] Não foi possível encontrar o algoritmo original")
                return False

        melhor = self.melhor_individuo()
        if melhor is None:
            print("[ERRO] Não foi possível determinar o melhor algoritmo")
            return False
            
        try:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(f"# Algoritmo mais eficiente - Fitness: {melhor.get_fitness()}\n")
                f.write(melhor.codigo)
                
            # Salva uma cópia do melhor algoritmo como backup
            with open("./utils/melhor_algoritmo_backup.py", "w", encoding="utf-8") as f:
                f.write(f"# Backup do melhor algoritmo - Fitness: {melhor.get_fitness()}\n")
                f.write(melhor.codigo)
                
            return True
        except Exception as e:
            print(f"[ERRO] Erro ao salvar algoritmo: {str(e)}")
            return False

    def get_estatisticas(self):
        """Retorna estatísticas sobre a população atual."""
        if not self.algoritmos:
            return None
            
        melhor = self.melhor_individuo()
        pior = min(self.algoritmos, key=lambda a: a.get_fitness()) if self.algoritmos else None
        
        return {
            "geracao": self.geracao,
            "tamanho": len(self.algoritmos),
            "melhor_fitness": melhor.get_fitness() if melhor else 0,
            "pior_fitness": pior.get_fitness() if pior else 0
        }
