from enum import Enum

class StatusLocacao(Enum):
    ATIVA = "ativa"
    DEVOLVIDA = "devolvida"
    ATRASADA = "atrasada"

class Locacao:
    def __init__(self, id_locacao, data_inicio, data_fim, cliente_id, id_filme, status):
        self.id = id_locacao
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.cliente_id = cliente_id
        self.filme_id = id_filme
        self.status = status