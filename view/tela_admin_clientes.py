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
            text="Editar Cliente",
            command=self.editar_cliente
        ).pack(pady=5)

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


    def editar_cliente(self):

        selecionado = self.tree.selection()

        if not selecionado:
            messagebox.showerror("Erro", "Selecione um cliente")
            return

        valores = self.tree.item(selecionado[0])["values"]

        id_cliente = valores[0]
        cliente = self.controller.buscar_por_id(id_cliente)

        if not cliente:
            messagebox.showerror("Erro", "Cliente não encontrado")
            return

        janela_edicao = tk.Toplevel(self)
        janela_edicao.title("Editar Cliente")
        janela_edicao.geometry("350x250")

        tk.Label(janela_edicao, text="Nome").pack(pady=5)
        entry_nome = tk.Entry(janela_edicao)
        entry_nome.pack()
        entry_nome.insert(0, cliente.nome)

        tk.Label(janela_edicao, text="CPF").pack(pady=5)
        entry_cpf = tk.Entry(janela_edicao)
        entry_cpf.pack()
        entry_cpf.insert(0, cliente.cpf)

        tk.Label(janela_edicao, text="Telefone").pack(pady=5)
        entry_telefone = tk.Entry(janela_edicao)
        entry_telefone.pack()
        entry_telefone.insert(0, cliente.telefone)

        def salvar_alteracoes():
            nome = entry_nome.get().strip()
            cpf = entry_cpf.get().strip()
            telefone = entry_telefone.get().strip()

            if not nome or not cpf:
                messagebox.showerror("Erro", "Nome e CPF são obrigatórios")
                return

            cliente.nome = nome
            cliente.cpf = cpf
            cliente.telefone = telefone

            sucesso, msg = self.controller.atualizar_cliente(cliente)

            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                janela_edicao.destroy()
                self.carregar_dados()
            else:
                messagebox.showerror("Erro", msg)

        tk.Button(
            janela_edicao,
            text="Salvar",
            command=salvar_alteracoes
        ).pack(pady=15)


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