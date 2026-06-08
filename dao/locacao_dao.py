import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from model import locacao
from model.locacao import Locacao, StatusLocacao
from dao.db_config import DatabaseConfig
from dao.generic_dao import GenericDAO
from dao.filme_dao import FilmeDAO

class LocacaoDAO(GenericDAO):
    
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()
        self.filme_dao = FilmeDAO()
        
    def salvar(self, locacao: Locacao):
        if not self.conexao:
            raise Exception("Sem conexão com o BD")
        
        try:
            cursor = self.conexao.cursor()
            query = """
            INSERT INTO tb_locacoes
            (loc_id, loc_cliente_id, loc_id_filme, loc_data_inicio, loc_data_fim, loc_status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(query, (
                locacao.id_locacao,
                locacao.cliente_id,
                locacao.id_filme,
                locacao.data_inicio,
                locacao.data_fim,
                locacao.status.value
             ))
            
            self.conexao.commit()
            return True, "Locação cadastrada com sucesso"
                                
        except Exception as e:
            print(f"Erro ao inserir locação: {e}")
            self.conexao.rollback()
            return False, f"Erro ao inserir locação: {e}"
        
        finally:
            if cursor:
                cursor.close()


    def listar_todos(self):
        if not self.conexao:
            return []
        
        try:
            cursor = self.conexao.cursor()
            query = """
            SELECT loc_id,
                loc_cliente_id,
                loc_id_filme,
                loc_data_inicio,
                loc_data_fim,
                loc_status
            FROM tb_locacoes
            """
            cursor.execute(query)
            linhas = cursor.fetchall()
            
            locacoes = []
            
            for linha in linhas:

                loc = Locacao(
                    id_locacao=linha[0],
                    cliente_id=linha[1],
                    id_filme=linha[2],
                    data_inicio=linha[3],
                    data_fim=linha[4],
                    status=StatusLocacao(linha[5])
                )

            locacoes.append(loc)
            
            return locacoes
                                
        except Exception as e:
            print(f"Erro ao buscar locações: {e}")
            return []
        
        finally:
            if cursor:
                cursor.close()


    def atualizar(self, locacao: Locacao, id_locacao: int):
        if not self.conexao:
            return False, "Sem conexão com o BD"
        
        try:
            cursor = self.conexao.cursor()
            query = """UPDATE tb_locacoes 
                       SET loc_data_inicio = %s,
                           loc_data_fim = %s,
                           loc_status = %s
                       WHERE loc_id = %s"""
            
            cursor.execute(query, (
                locacao.data_inicio,
                locacao.data_fim,
                locacao.status.value,
                id_locacao
            ))
            
            self.conexao.commit()
            return True, "Locação atualizada com sucesso"
            
        except Exception as e:
            print(f"Erro ao atualizar locação: {e}")
            self.conexao.rollback()
            return False, f"Erro ao atualizar locação: {e}"
        
        finally:
            if cursor:
                cursor.close()


    def remover(self, id_locacao: int):
        if not self.conexao:
            return False, "Sem conexão com o BD"
        
        try:
            cursor = self.conexao.cursor()
            query = "DELETE FROM tb_locacoes WHERE loc_id = %s"
            cursor.execute(query, (id_locacao,))
            
            self.conexao.commit()
            return True, "Locação removida com sucesso"
            
        except Exception as e:
            print(f"Erro ao remover locação: {e}")
            self.conexao.rollback()
            return False, f"Erro ao remover locação: {e}"
        
        finally:
            if cursor:
                cursor.close()


    def buscar_por_id(self, id_locacao: int):
        if not self.conexao:
            return None
        
        try:
            cursor = self.conexao.cursor()
            query = """
            SELECT loc_id,
                loc_cliente_id,
                loc_id_filme,
                loc_data_inicio,
                loc_data_fim,
                loc_status
            FROM tb_locacoes
            WHERE loc_id = %s
            """
            
            cursor.execute(query, (id_locacao,))
            linha = cursor.fetchone()
            
            if linha:
                
                loc = Locacao(
                    id_locacao=linha[0],
                    cliente_id=linha[1],
                    id_filme=linha[2],
                    data_inicio=linha[3],
                    data_fim=linha[4],
                    status=StatusLocacao(linha[5])
                )
                
                
                return loc
            
            return None
            
        except Exception as e:
            print(f"Erro ao buscar locação: {e}")
        
        finally:
            if cursor:
                cursor.close()
