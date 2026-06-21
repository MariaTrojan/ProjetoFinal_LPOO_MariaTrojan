class Cliente:
    def __init__(self, nome, cpf, telefone, id_cliente=None):
        self.id_cliente = id_cliente
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        