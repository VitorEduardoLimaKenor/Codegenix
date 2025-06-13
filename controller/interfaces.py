"""
Interfaces para os controladores do sistema.
Seguindo o princípio de Inversão de Dependência (SOLID).
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

class IAvaliador(ABC):
    """Interface para avaliadores de algoritmos."""
    
    @abstractmethod
    def avaliar(self, algoritmo):
        """Avalia um algoritmo e atualiza seu fitness e métricas."""
        pass
    
    @abstractmethod
    def set_geracao(self, geracao: int):
        """Define a geração atual para as próximas avaliações."""
        pass
    
    @abstractmethod
    def salvar_historico(self, caminho: str = "./utils/historico_avaliacoes.json"):
        """Salva o histórico de avaliações em um arquivo."""
        pass
    
    @abstractmethod
    def carregar_historico(self, caminho: str = "./utils/historico_avaliacoes.json"):
        """Carrega o histórico de avaliações de um arquivo."""
        pass
    
    @abstractmethod
    def get_metricas_geracao(self, geracao: Optional[int] = None) -> Dict[str, Any]:
        """Retorna as métricas médias de uma geração específica."""
        pass


class IOperadorGenetico(ABC):
    """Interface para operadores genéticos."""
    
    @abstractmethod
    def selecionar(self, algoritmos: List, quantidade: int = 5) -> List:
        """Seleciona os melhores algoritmos para reprodução."""
        pass
    
    @abstractmethod
    def cruzar(self, pai1, pai2):
        """Cruza dois algoritmos para gerar um novo."""
        pass
    
    @abstractmethod
    def mutar(self, algoritmo):
        """Aplica mutação em um algoritmo."""
        pass
    
    @abstractmethod
    def gerar_variacoes_iniciais(self, codigo_base: str, linguagem: str, quantidade: int = 10) -> List:
        """Gera variações iniciais de um código base."""
        pass
