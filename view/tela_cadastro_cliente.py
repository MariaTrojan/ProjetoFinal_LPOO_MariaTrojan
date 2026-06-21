import tkinter as tk
from tkinter import messagebox
from control.cliente_controller import ClienteController


class TelaCadastroCliente(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master)

        self.title("Cadastro Cliente")
        self.geometry("400x300")

        self.controller = ClienteController()

        self.criar_componentes()


    def criar_componentes(self):

        tk.Label(self, text="Nome").pack()
        self.entry_nome = tk.Entry(self)
        self.entry_nome.pack()

        tk.Label(self, text="CPF").pack()
        self.entry_cpf = tk.Entry(self)
        self.entry_cpf.pack()

        tk.Label(self, text="Telefone").pack()
        self.entry_telefone = tk.Entry(self)
        self.entry_telefone.pack()

        tk.Button(
            self,
            text="Cadastrar",
            command=self.cadastrar
        ).pack(pady=15)


    def cadastrar(self):
        try:
            nome = self.entry_nome.get()
            cpf = self.entry_cpf.get()
            telefone = self.entry_telefone.get()

            sucesso, msg = self.controller.cadastrar_cliente(
                nome,
                cpf,
                telefone
            )

            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                self.destroy()

            else:
                messagebox.showerror("Erro", msg)

        except Exception as e:
            messagebox.showerror("Erro", str(e))