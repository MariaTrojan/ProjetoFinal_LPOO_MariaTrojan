import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from model import filme
from dao.db_config import DatabaseConfig
from dao.generic_dao import GenericDAO


class FilmeDAO(GenericDAO):
    
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()
        
    def salvar(self, filme: filme.Filme):
        if not self.conexao:
            raise Exception("Sem conexão com o BD")
        
        try:
            cursor = self.conexao.cursor()
            query = """
            INSERT INTO tb_filmes
            (id_filme, filme_titulo, filme_genero, filme_ano, filme_estoque, filme_valor_locacao)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(query, (
                filme.id_filme,
                filme.titulo,
                filme.genero,
                filme.ano,
                filme.estoque,
                filme.valor_locacao
            ))
            
            self.conexao.commit()
            return True, "Filme cadastrado com sucesso"
                                
                                
        except Exception as e:
            print(f"Erro ao inserir filme: {e}")
            self.conexao.rollback()
            return False, f"Erro ao inserir filme: {e}"
        
        finally:
            if cursor:
                cursor.close()


    def listar_todos(self):
        if not self.conexao:
            return []
        
        try:
            cursor = self.conexao.cursor()
            query = """
            SELECT id_filme,
                filme_titulo,
                filme_genero,
                filme_ano,
                filme_estoque,
                filme_valor_locacao
            FROM tb_filmes
            """
            cursor.execute(query)
            linhas = cursor.fetchall()
            
            filmes = []
            
            for linha in linhas:

                fil = filme.Filme(
                    id_filme=linha[0],
                    titulo=linha[1],
                    genero=linha[2],
                    ano=linha[3],
                    estoque=linha[4],
                    valor_locacao=linha[5]
                )

                filmes.append(fil)
            
            return filmes
                                
        except Exception as e:
            print(f"Erro ao buscar filmes: {e}")
            return []
        
        finally:
            if cursor:
                cursor.close()


    def atualizar(self, filme: filme.Filme, id_filme: int):
        if not self.conexao:
            return False, "Sem conexão com o BD"
        
        try:
            cursor = self.conexao.cursor()
            query = """UPDATE tb_filmes SET filme_titulo = %s,
                           filme_genero = %s, 
                           filme_ano = %s,
                           filme_estoque = %s,
                           filme_valor_locacao = %s
                       WHERE id_filme = %s"""
            
            cursor.execute(query, (
                filme.titulo,
                filme.genero,
                filme.ano,
                filme.estoque,
                filme.valor_locacao,
                id_filme
            ))
            
            self.conexao.commit()
            return True, "Filme atualizado com sucesso"
            
        except Exception as e:
            print(f"Erro ao atualizar filme: {e}")
            self.conexao.rollback()
            return False, f"Erro ao atualizar filme: {e}"
        
        finally:
            if cursor:
                cursor.close()


    def remover(self, id_filme: int):
        if not self.conexao:
            return False, "Sem conexão com o BD"
        
        try:
            cursor = self.conexao.cursor()
            query = "DELETE FROM tb_filmes WHERE id_filme = %s"
            cursor.execute(query, (id_filme,))
            
            self.conexao.commit()
            return True, "Filme removido com sucesso"
            
        except Exception as e:
            print(f"Erro ao remover filme: {e}")
            self.conexao.rollback()
            return False, f"Erro ao remover filme: {e}"
        
        finally:
            if cursor:
                cursor.close()


    def buscar_por_id(self, id_filme: int):
        if not self.conexao:
            return None
        
        try:
            cursor = self.conexao.cursor()
            query = """
            SELECT id_filme,
                filme_titulo,
                filme_genero,
                filme_ano,
                filme_estoque,
                filme_valor_locacao
            FROM tb_filmes
            WHERE id_filme = %s
            """
            
            cursor.execute(query, (id_filme,))
            linha = cursor.fetchone()
            
            if linha:
                
                fil = filme.Filme(
                    id_filme=linha[0],
                    titulo=linha[1],
                    genero=linha[2],
                    ano=linha[3],
                    estoque=linha[4],
                    valor_locacao=linha[5]
                )
                
                
                return fil
            
            return None
            
        except Exception as e:
            print(f"Erro ao buscar filme: {e}")
        
        finally:
            if cursor:
                cursor.close()

    def buscar_por_nome(self, nome):

        cursor = self.conexao.cursor()

        query = """
        SELECT * FROM tb_filmes
        WHERE LOWER(filme_titulo) LIKE LOWER(%s)
        """

        cursor.execute(query, (f"%{nome}%",))

        linhas = cursor.fetchall()

        filmes = []

        for linha in linhas:
            filmes.append(
                filme.Filme(
                    id_filme=linha[0],
                    titulo=linha[1],
                    genero=linha[2],
                    ano=linha[3],
                    estoque=linha[4],
                    valor_locacao=linha[5]
                )
            )

        return filmes
    
    def buscar_por_genero(self, genero):

        try:
            cursor = self.conexao.cursor()

            query = """
            SELECT *
            FROM tb_filmes
            WHERE filme_genero = %s
            """

            cursor.execute(query, (genero,))

            linhas = cursor.fetchall()

            filmes = []

            for linha in linhas:

                filme = filme.Filme(
                    id_filme=linha[0],
                    titulo=linha[1],
                    genero=linha[2],
                    ano=linha[3],
                    estoque=linha[4],
                    valor_locacao=linha[5]
                )

                filmes.append(filme)

            return filmes

        except Exception as e:
            print(e)
            return []
