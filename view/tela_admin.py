import tkinter as tk
from view.tela_admin_filmes import TelaAdminFilmes
from view.tela_admin_clientes import TelaAdminClientes
from view.tela_admin_locacoes import TelaAdminLocacoes


class TelaAdmin(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master)

        self.title("Painel Admin")
        self.geometry("400x300")

        self.criar_componentes()

    def criar_componentes(self):

        tk.Label(
            self,
            text="Painel do Administrador",
            font=("Arial", 14)
        ).pack(pady=20)

        tk.Button(
            self,
            text="Gerenciar Filmes",
            command=self.abrir_filmes
        ).pack(pady=10)

        tk.Button(
            self,
            text="Gerenciar Clientes",
            command=self.abrir_clientes
        ).pack(pady=10)

        tk.Button(
            self,
            text="Gerenciar Locações",
            command=self.abrir_locacoes
        ).pack(pady=10)


    def abrir_filmes(self):
        TelaAdminFilmes(self)


    def abrir_clientes(self):
        TelaAdminClientes(self)


    def abrir_locacoes(self):
        TelaAdminLocacoes(self)