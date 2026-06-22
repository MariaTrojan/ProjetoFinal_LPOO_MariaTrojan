from abc import ABC, abstractmethod

class CalculoLocacaoStrategy(ABC):

    @abstractmethod
    def calcular(self, valor_diaria, quantidade_dias):
        pass