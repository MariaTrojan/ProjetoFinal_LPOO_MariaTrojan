class Locacao:
    def __init__(self, id, data_locacao, data_devolucao, cliente_id, filme_id):
        self.id = id
        self.data_locacao = data_locacao
        self.data_devolucao = data_devolucao
        self.cliente_id = cliente_id
        self.filme_id = filme_id