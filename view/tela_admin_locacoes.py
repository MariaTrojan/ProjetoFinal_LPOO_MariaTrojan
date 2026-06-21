import tkinter as tk
from tkinter import ttk, messagebox

from control.locacao_controller import LocacaoController


class TelaAdminLocacoes(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master)

        self.title("Gerenciar Locações")
        self.geometry("900x450")

        self.controller = LocacaoController()

        self.criar_widgets()
        self.carregar_dados()


    def criar_widgets(self):

        tk.Label(
            self,
            text="Locações",
            font=("Arial", 14)
        ).pack(pady=10)

        colunas = ("ID", "Cliente", "Filme", "Data Início", "Data Fim", "Status")

        self.tree = ttk.Treeview(
            self,
            columns=colunas,
            show="headings"
        )

        for coluna in colunas:
            self.tree.heading(coluna, text=coluna)

        self.tree.pack(expand=True, fill="both", padx=20, pady=10)

        tk.Button(
            self,
            text="Confirmar Retirada",
            command=self.retirar
        ).pack(pady=5)

        tk.Button(
            self,
            text="Registrar Devolução",
            command=self.devolver
        ).pack(pady=5)


    def carregar_dados(self):

        self.tree.delete(*self.tree.get_children())

        locacoes = self.controller.listar_locacoes()

        for locacao in locacoes:
            self.tree.insert("", "end", values=(
                locacao.id,
                locacao.cliente_id,
                locacao.filme_id,
                locacao.data_inicio,
                locacao.data_fim,
                locacao.status.value
            ))


    def retirar(self):

        selecionado = self.tree.selection()

        if not selecionado:
            return

        valores = self.tree.item(selecionado[0])["values"]

        id_locacao = valores[0]

        locacao = self.controller.buscar_por_id(id_locacao)

        sucesso, msg = self.controller.retirar_filme(
            locacao,
            id_locacao
        )

        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.carregar_dados()

        else:
            messagebox.showerror("Erro", msg)


    def devolver(self):

        selecionado = self.tree.selection()

        if not selecionado:
            return

        valores = self.tree.item(selecionado[0])["values"]

        id_locacao = valores[0]

        locacao = self.controller.buscar_por_id(id_locacao)

        sucesso, msg = self.controller.devolver_filme(
            locacao,
            id_locacao
        )

        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.carregar_dados()

        else:
            messagebox.showerror("Erro", msg)