import sys
import os

from model import cliente

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from model.cliente import Cliente
from dao.db_config import DatabaseConfig
from dao.generic_dao import GenericDAO
from dao.cliente_dao import ClienteDAO

class ClienteDAO(GenericDAO):
    
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()
        
    def salvar(self, cliente: cliente.Cliente):
        if not self.conexao:
            raise Exception("Sem conexão com o BD")
        
        try:
            cursor = self.conexao.cursor()
            query = """
            INSERT INTO tb_clientes
            (id_cliente, nome, cpf, telefone)
            VALUES (%s, %s, %s, %s)
            """
            
            cursor.execute(query, (
                cliente.id_cliente,
                cliente.nome,
                cliente.cpf,
                cliente.telefone
            ))
            
            self.conexao.commit()
            return True, "Cliente cadastrado com sucesso"
                                
                                
        except Exception as e:
            print(f"Erro ao inserir cliente: {e}")
            self.conexao.rollback()
            return False, f"Erro ao inserir cliente: {e}"
        
        finally:
            if cursor:
                cursor.close()


    def listar_todos(self):
        if not self.conexao:
            return []
        
        try:
            cursor = self.conexao.cursor()
            query = """
            SELECT id_cliente,
                nome,
                cpf,
                telefone
            FROM tb_clientes
            """
            cursor.execute(query)
            linhas = cursor.fetchall()
            
            clientes = []
            
            for linha in linhas:

                cli = cliente.Cliente(
                    id_cliente=linha[0],
                    nome=linha[1],
                    cpf=linha[2],
                    telefone=linha[3]
                )

                clientes.append(cli)
            
            return clientes
                                
        except Exception as e:
            print(f"Erro ao buscar clientes: {e}")
            return []
        
        finally:
            if cursor:
                cursor.close()


    def atualizar(self, cliente: cliente.Cliente, id_cliente: int):
        if not self.conexao:
            return False, "Sem conexão com o BD"
        
        try:
            cursor = self.conexao.cursor()
            query = """UPDATE tb_clientes SET nome = %s,
                           cpf = %s, 
                           telefone = %s
                       WHERE id_cliente = %s"""
            
            cursor.execute(query, (
                cliente.nome,
                cliente.cpf,
                cliente.telefone,
                id_cliente
            ))
            
            self.conexao.commit()
            return True, "Cliente atualizado com sucesso"
        
            
        except Exception as e:
            print(f"Erro ao atualizar cliente: {e}")
            self.conexao.rollback()
            return False, f"Erro ao atualizar cliente: {e}"
        
        finally:
            if cursor:
                cursor.close()


    def remover(self, id_cliente: int):
        if not self.conexao:
            return False, "Sem conexão com o BD"
        
        try:
            cursor = self.conexao.cursor()
            query = "DELETE FROM tb_clientes WHERE id_cliente = %s"
            cursor.execute(query, (id_cliente,))
            
            self.conexao.commit()
            return True, "Cliente removido com sucesso"
            
        except Exception as e:
            print(f"Erro ao remover cliente: {e}")
            self.conexao.rollback()
            return False, f"Erro ao remover cliente: {e}"
        
        finally:
            if cursor:
                cursor.close()


    def buscar_por_id(self, id_cliente: int):
        if not self.conexao:
            return None
        
        try:
            cursor = self.conexao.cursor()
            query = """
            SELECT id_cliente,
                nome,
                cpf,
                telefone
            FROM tb_clientes
            WHERE id_cliente = %s
            """
            
            cursor.execute(query, (id_cliente,))
            linha = cursor.fetchone()
            
            if linha:
                
                cli = Cliente(
                    id_cliente=linha[0],
                    nome=linha[1],
                    cpf=linha[2],
                    telefone=linha[3]
                )
                
                
                return cli
            
            return None
            
        except Exception as e:
            print(f"Erro ao buscar cliente: {e}")
        
        finally:
            if cursor:
                cursor.close()
