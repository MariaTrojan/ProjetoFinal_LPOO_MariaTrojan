import tkinter as tk
from tkinter import ttk, messagebox

from control.cliente_controller import ClienteController


class TelaAdminClientes(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master)

        self.title("Gerenciar Clientes")
        self.geometry("700x400")

        self.controller = ClienteController()

        self.criar_widgets()
        self.carregar_dados()


    def criar_widgets(self):

        tk.Label(
            self,
            text="Clientes Cadastrados",
            font=("Arial", 14)
        ).pack(pady=10)

        colunas = ("ID", "Nome", "CPF", "Telefone")

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
            text="Remover Cliente",
            command=self.remover_cliente
        ).pack(pady=5)


    def carregar_dados(self):

        self.tree.delete(*self.tree.get_children())

        clientes = self.controller.listar_clientes()

        for cliente in clientes:
            self.tree.insert("", "end", values=(
                cliente.id_cliente,
                cliente.nome,
                cliente.cpf,
                cliente.telefone
            ))


    def remover_cliente(self):

        selecionado = self.tree.selection()

        if not selecionado:
            messagebox.showerror("Erro", "Selecione um cliente")
            return

        valores = self.tree.item(selecionado[0])["values"]

        id_cliente = valores[0]

        sucesso, msg = self.controller.remover_cliente(id_cliente)

        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.carregar_dados()

        else:
            messagebox.showerror("Erro", msg)