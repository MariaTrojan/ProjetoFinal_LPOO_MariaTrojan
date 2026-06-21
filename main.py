import tkinter as tk
from view.janela_cadastro_locacao import JanelaCadastroLocacao
from view.tela_cadastro_cliente import TelaCadastroCliente
from view.filme_list_view import JanelaListagemFilmes
from view.tela_admin import TelaAdmin


def abrir_locacao():
    nova_janela = tk.Toplevel(root)
    JanelaCadastroLocacao(nova_janela)

def abrir_cliente():
    nova_janela = tk.Toplevel(root)
    TelaCadastroCliente(nova_janela)

def abrir_filmes():
    nova_janela = tk.Toplevel(root)
    JanelaListagemFilmes(nova_janela)

def abrir_admin():
    TelaAdmin(root)


root = tk.Tk()
root.title("Locadora de Filmes")
root.geometry("600x400")

tk.Label(root, text="Sistema Locadora de Filmes", font=("Arial", 14)).pack(pady=20)

tk.Button(root, text="Cadastro Reserva", command=abrir_locacao).pack(pady=10)

tk.Button(root, text="Cadastro Cliente", command=abrir_cliente).pack(pady=10)

tk.Button(root, text="Filmes", command=abrir_filmes).pack(pady=10)

tk.Button(root, text="Login Admin", command=abrir_admin).pack(pady=10)

root.mainloop()