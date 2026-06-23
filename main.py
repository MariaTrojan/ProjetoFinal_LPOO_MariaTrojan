import tkinter as tk
from view.janela_cadastro_locacao import JanelaCadastroLocacao
from view.tela_cadastro_cliente import TelaCadastroCliente
from view.filme_list_view import JanelaListagemFilmes
from view.tela_admin import TelaLoginAdmin


def abrir_locacao():
    nova_janela = tk.Toplevel(root)
    JanelaCadastroLocacao(nova_janela)

def abrir_cliente():
    TelaCadastroCliente(root)

def abrir_filmes():
    JanelaListagemFilmes(root)

def abrir_admin():
    TelaLoginAdmin(root)

def sair():
    root.quit()


root = tk.Tk()
root.title("Locadora de Filmes")
root.geometry("600x400")

# Criar menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Menu Cadastro
menu_cadastro = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Cadastro", menu=menu_cadastro)
menu_cadastro.add_command(label="Nova Reserva", command=abrir_locacao)
menu_cadastro.add_command(label="Novo Cliente", command=abrir_cliente)
menu_cadastro.add_separator()
menu_cadastro.add_command(label="Sair", command=sair)

# Menu Filmes
menu_filmes = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Filmes", menu=menu_filmes)
menu_filmes.add_command(label="Listar Filmes", command=abrir_filmes)

# Menu Admin
menu_admin = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Admin", menu=menu_admin)
menu_admin.add_command(label="Painel Admin", command=abrir_admin)


tk.Label(root, text="Sistema Locadora de Filmes", font=("Arial", 16, "bold")).pack(pady=20)

tk.Label(root, text="Bem-vindo ao sistema!", font=("Arial", 12)).pack(pady=10)

tk.Label(root, text="Use o menu acima para navegar", font=("Arial", 10), fg="gray").pack(pady=5)

root.mainloop()