import tkinter as tk
from tkinter import messagebox
from view.tela_admin_filmes import TelaAdminFilmes
from view.tela_admin_clientes import TelaAdminClientes
from view.tela_admin_locacoes import TelaAdminLocacoes


class TelaLoginAdmin(tk.Toplevel):
    
    def __init__(self, master=None):
        super().__init__(master)
        
        self.title("Login Admin")
        self.geometry("300x150")
        self.resizable(False, False)
        
        # Senha padrão
        self.senha_correta = "admin123"
        
        self.criar_componentes()
    
    def criar_componentes(self):
        tk.Label(
            self,
            text="Digite a senha:",
            font=("Arial", 12)
        ).pack(pady=15)
        
        self.entry_senha = tk.Entry(self, show="*", font=("Arial", 11))
        self.entry_senha.pack(pady=10, padx=20, fill="x")
        self.entry_senha.bind("<Return>", lambda e: self.verificar_senha())
        
        tk.Button(
            self,
            text="Acessar",
            command=self.verificar_senha
        ).pack(pady=10)
    
    def verificar_senha(self):
        senha_digitada = self.entry_senha.get()
        
        if senha_digitada == self.senha_correta:
            self.destroy()
            TelaAdmin(self.master)
        else:
            messagebox.showerror("Erro", "Senha incorreta!")
            self.entry_senha.delete(0, tk.END)


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