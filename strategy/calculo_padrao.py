from strategy.calculo_locacao_strategy import CalculoLocacaoStrategy

class CalculoPadrao(CalculoLocacaoStrategy):

    def calcular(self, valor_diaria, quantidade_dias):
        return valor_diaria * quantidade_dias