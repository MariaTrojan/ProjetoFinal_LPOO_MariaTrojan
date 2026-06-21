from dao.cliente_dao import ClienteDAO
from model.cliente import Cliente


class ClienteController:

    def __init__(self):
        self.cliente_dao = ClienteDAO()

    def cadastrar_cliente(self, nome, cpf, telefone): #admin
        if not nome or not cpf:
            return False, "Nome e CPF são obrigatórios"
        
        cliente = Cliente(
            nome=nome,
            cpf=cpf,
            telefone=telefone
        )

        return self.cliente_dao.salvar(cliente)
    
    def listar_clientes(self): #admin
        return self.cliente_dao.listar_todos()  
    
    def buscar_por_id(self, id_cliente):
        return self.cliente_dao.buscar_por_id(id_cliente)
    
    def atualizar_cliente(self, cliente): #Admin
        return self.cliente_dao.atualizar(cliente, cliente.id_cliente)
    
    def remover_cliente(self, id_cliente): #Admin
        return self.cliente_dao.remover(id_cliente)
    
    def buscar_por_nome(self, nome):
        return self.cliente_dao.buscar_por_nome(nome)
    
    def buscar_por_cpf(self, cpf):
        return self.cliente_dao.buscar_por_cpf(cpf)
    
    