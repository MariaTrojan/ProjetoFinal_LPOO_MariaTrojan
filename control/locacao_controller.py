from dao.cliente_dao import ClienteDAO
from dao.locacao_dao import LocacaoDAO
from dao.filme_dao import FilmeDAO
from model import filme
from model.locacao import Locacao, StatusLocacao
from model.filme import Filme
from datetime import date
from strategy.calculo_padrao import CalculoPadrao

class LocacaoController:
    
    def __init__(self):
        self.locacao_dao = LocacaoDAO()
        self.calculo_strategy = CalculoPadrao()
        self.filme_dao = FilmeDAO()
        self.cliente_dao = ClienteDAO()
        
        
    def criar_locacao(self, id_locacao, id_cliente, id_filme, data_inicio, data_fim=None):
        if not id_filme or not data_inicio:
            return False, "Preencha os campos obrigatórios"
        
        try:
            cliente = self.cliente_dao.buscar_por_id(id_cliente)

            if not cliente:
                return False, "Cliente não encontrado"

            filme = self.filme_dao.buscar_por_id(id_filme)
            
            if not filme:
                return False, "Filme não encontrado"

            if filme.estoque <= 0:
                return False, "Filme indisponível no momento"
            
            locacao = Locacao(
                id_locacao=id_locacao,
                cliente_id=id_cliente,
                id_filme=id_filme,
                data_inicio=data_inicio,
                data_fim=data_fim,
                status=StatusLocacao.RESERVADO
            )
            
            sucesso, msg = self.locacao_dao.salvar(locacao)
            return sucesso, msg
        
        except Exception as e:
            return False, f"Erro ao criar locação: {e}"
    
    
    def listar_locacoes(self):
        try:
            return self.locacao_dao.listar_todos()
        
        except Exception as e:
            print(f"Erro ao listar locações: {e}")
            return None
    
    
    def retirar_filme(self, locacao, id_locacao):
        try:
            # verifica se está reservado
            if locacao.status != StatusLocacao.RESERVADO:
                return False, "Só é possível retirar filmes reservados"

            # busca o filme
            filme = self.filme_dao.buscar_por_id(locacao.filme_id)

            if not filme:
                return False, "Filme não encontrado"

            # estoque
            if filme.estoque < 1:
                return False, "Filme sem estoque disponível"

            # muda status da locação
            locacao.status = StatusLocacao.LOCADO

            filme.estoque -= 1

            # atualiza banco
            self.filme_dao.atualizar(filme, filme.id_filme)
            self.locacao_dao.atualizar(locacao, id_locacao)

            return True, "Filme retirado com sucesso"

        except Exception as e:
            return False, f"Erro ao retirar filme: {e}"
    
    
    def devolver_filme(self, locacao, id_locacao):
        try:
            if locacao.status != StatusLocacao.LOCADO:
                return False, "O filme não está locado"

            filme = self.filme_dao.buscar_por_id(locacao.filme_id)

            if not filme:
                return False, "Filme não encontrado"

            locacao.status = StatusLocacao.DEVOLVIDO
            locacao.data_fim = date.today()

            dias = (locacao.data_fim - locacao.data_inicio).days
            if dias <= 0:
                dias = 1

            estrategia = CalculoPadrao()

            valor = estrategia.calcular(
                filme.valor_locacao,
                dias
            )

            filme.estoque += 1

            self.filme_dao.atualizar(filme, filme.id_filme)
            self.locacao_dao.atualizar(locacao, id_locacao)

            return True, f"Devolução realizada. Valor total: R$ {valor}"

        except Exception as e:
            return False, f"Erro ao devolver: {e}"
    
    def cancelar_reserva(self, locacao, id_locacao):
        try:
            if locacao.status != StatusLocacao.RESERVADO:
                return False, "Só é possível cancelar reservas"

            locacao.status = StatusLocacao.CANCELADO

            return self.locacao_dao.atualizar(locacao, id_locacao)

        except Exception as e:
            return False, f"Erro ao cancelar: {e}"
    
    
    def remover_locacao(self, id_locacao): #admin
        try:
            return self.locacao_dao.remover(id_locacao)
        
        except Exception as e:
            return False, f"Erro ao remover locação: {e}"
        
    def ver_detalhes(self, locacao):
        try:
            filme = self.filme_dao.buscar_por_id(locacao.filme_id)

            if not filme:
                return "Filme não encontrado"

            if locacao.status == StatusLocacao.DEVOLVIDO:

                dias = (locacao.data_fim - locacao.data_inicio).days
                if dias <= 0:
                    dias = 1

                estrategia = CalculoPadrao()

                valor = estrategia.calcular(
                    filme.valor_locacao,
                    dias
                )

                return f"""
        Status: Devolvida
        Início: {locacao.data_inicio}
        Devolução: {locacao.data_fim}
        Diárias: {dias}
        Valor total: R$ {valor:.2f}
        """

            elif locacao.status in [StatusLocacao.RESERVADO, StatusLocacao.LOCADO]:

                dias = (locacao.data_fim - locacao.data_inicio).days
                if dias <= 0:
                    dias = 1

                estrategia = CalculoPadrao()
                valor = estrategia.calcular(
                    filme.valor_locacao,
                    dias
                )

                return f"""
        Status: {locacao.status.value}
        Início: {locacao.data_inicio}
        Previsão: {locacao.data_fim}
        Valor estimado: R$ {valor:.2f}
        """

            elif locacao.status == StatusLocacao.CANCELADO:

                return f"""
        Status: Cancelada
        Início: {locacao.data_inicio}
        (Locação cancelada — sem cobrança)
        """

        except Exception as e:
            return f"Erro ao exibir detalhes: {e}"


        
    def atualizar_locacao_admin(self, locacao):
        try:
            if locacao.data_fim and locacao.data_inicio > locacao.data_fim:
                return False, "Data início deve ser <= data fim"

            return self.locacao_dao.atualizar(locacao, locacao.id)

        except Exception as e:
            return False, str(e)
        
    
    def buscar_por_id(self, id_locacao):
        return self.locacao_dao.buscar_por_id(id_locacao)
    
    def listar_filmes_disponiveis(self):
        filmes = self.filme_dao.listar_todos()

        disponiveis = []

        for filme in filmes:
            if filme.estoque > 0:
                disponiveis.append(filme)

        return disponiveis