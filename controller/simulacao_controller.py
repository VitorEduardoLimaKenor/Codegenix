import os
import json
from model.populacao import Populacao
from model.algoritmo import Algoritmo
from controller.avaliador_service import AvaliadorService
from controller.operador_genetico import OperadorGenetico
from controller.interfaces import IAvaliador, IOperadorGenetico

class SimulacaoController:
    """Controlador principal que orquestra a simulação de evolução de algoritmos."""
    
    def __init__(self, avaliador=None, operador_genetico=None):
        """
        Inicializa o controlador com dependências injetadas.
        
        Args:
            avaliador: Implementação de IAvaliador (opcional)
            operador_genetico: Implementação de IOperadorGenetico (opcional)
        """
        self.avaliador = avaliador if avaliador else AvaliadorService()
        self.operador_genetico = operador_genetico if operador_genetico else OperadorGenetico()
        self.populacao = None
        self.historico_caminho = "./utils/historico_avaliacoes.json"
    
    def iniciar_simulacao(self, codigo_inicial, linguagem, tamanho_populacao=5, 
                         geracoes=3, callback_progresso=None):
        """
        Inicia a simulação de evolução de algoritmos.
        
        Args:
            codigo_inicial: Código inicial para gerar a população
            linguagem: Linguagem de programação do código
            tamanho_populacao: Tamanho da população
            geracoes: Número de gerações
            callback_progresso: Função de callback para atualizar o progresso
            
        Returns:
            Tupla contendo (melhor_algoritmo, estatisticas, caminho_historico)
        """
        try:
            print(f"[INFO] Iniciando simulação com {tamanho_populacao} indivíduos e {geracoes} gerações")
            
            # Cria a população
            self.populacao = Populacao(linguagem=linguagem, tamanho=tamanho_populacao)
            
            # Configura as dependências
            self.populacao.set_avaliador(self.avaliador)
            self.populacao.set_operador(self.operador_genetico)
            
            # Gera a população inicial
            self.populacao.gerar_populacao_inicial(codigo_base=codigo_inicial)
            
            # Evolui a população por todas as gerações de uma vez
            print(f"[INFO] Evoluindo população por {geracoes} gerações")
            self.populacao.evoluir(num_geracoes=geracoes)
            
            # Atualiza o progresso se houver callback
            if callback_progresso:
                callback_progresso(geracoes, geracoes)
            
            # Obtém o melhor algoritmo
            melhor_algoritmo = self.populacao.melhor_individuo()
            
            # Salva o melhor algoritmo
            self.populacao.salvar_melhor_algoritmo("./utils/melhor_algoritmo")
            
            # Obtém estatísticas
            estatisticas = self.populacao.get_estatisticas()
            
            return melhor_algoritmo, estatisticas, self.historico_caminho
            
        except Exception as e:
            print(f"[ERRO] Erro na simulação: {str(e)}")
            return None, None, None
    
    def exportar_algoritmo(self, algoritmo, caminho):
        """
        Exporta um algoritmo para um arquivo.
        
        Args:
            algoritmo: Algoritmo a ser exportado
            caminho: Caminho do arquivo
            
        Returns:
            True se o algoritmo foi exportado com sucesso, False caso contrário
        """
        try:
            with open(caminho, "w", encoding="utf-8") as arquivo:
                arquivo.write(algoritmo.codigo)
            return True
        except Exception as e:
            print(f"[ERRO] Erro ao exportar algoritmo: {str(e)}")
            return False
