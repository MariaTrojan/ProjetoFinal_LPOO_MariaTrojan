from dao.filme_dao import FilmeDAO
from model.filme import Filme



class FilmeController:
    def __init__(self):
        self.filme_dao = FilmeDAO()

    def cadastrar_filme(self, id_filme, titulo, genero, ano, estoque, valor_locacao): #admin
        if not titulo:
            return False, "Título obrigatório"
    
        filme = Filme(
            id_filme=id_filme,
            titulo=titulo,
            genero=genero,
            ano=ano,
            estoque=estoque,
            valor_locacao=valor_locacao
        )

        return self.filme_dao.salvar(filme)
    
    def listar_filmes(self): 
        return self.filme_dao.listar_todos()
    
    def buscar_por_id(self, id_filme):
        return self.filme_dao.buscar_por_id(id_filme)
    
    def atualizar_filme(self, filme): #Admin
        return self.filme_dao.atualizar(filme, filme.id_filme)
    
    def remover_filme(self, id_filme): #Admin
        return self.filme_dao.remover(id_filme)
    
    def listar_filmes_disponiveis(self):
    
        filmes = self.filme_dao.listar_todos()

        disponiveis = []

        for filme in filmes:
            if filme.estoque > 0:
                disponiveis.append(filme)

        return disponiveis
    
    def buscar_por_nome(self, titulo):
        filmes = self.filme_dao.listar_todos()

        encontrados = []

        for filme in filmes:
            if titulo.lower() in filme.titulo.lower():
                encontrados.append(filme)

        return encontrados
        
    
    def atualizar_estoque(self, id_filme, quantidade):

        filme = self.filme_dao.buscar_por_id(id_filme)

        if not filme:
            return False, "Filme não encontrado"
        
        novo_estoque = filme.estoque + quantidade

        if novo_estoque < 0:
            return False, "Estoque insuficiente"

        filme.estoque = novo_estoque

        return self.filme_dao.atualizar(filme, id_filme)
    
    def buscar_por_genero(self, genero):
        return self.filme_dao.buscar_por_genero(genero)
    