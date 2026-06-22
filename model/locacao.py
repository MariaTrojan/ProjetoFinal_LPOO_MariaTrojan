from datetime import date
from enum import Enum

class StatusLocacao(Enum):
    RESERVADO = "reservado"
    LOCADO = "locado"
    DEVOLVIDO = "devolvido"
    CANCELADO = "cancelado"

class Locacao:
    def __init__(self, data_inicio, data_fim, id_cliente, id_filme, status, id_locacao=None):
        self.id = id_locacao
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.id_cliente = id_cliente
        self.id_filme = id_filme
        self.status = status


    def calcular_valor_locacao(self, valor_filme):

            if self.data_fim is None:
                self.data_fim = date.today()

            dias = (self.data_fim - self.data_inicio).days

            if dias <= 0:
                dias = 1

            valor_total = dias * valor_filme

            return float(valor_total)