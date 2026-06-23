import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox

from control.filme_controller import FilmeController


class JanelaListagemFilmes(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Filmes Cadastrados")
        self.geometry("850x450")
        self.resizable(True, True)
        
        self.controller = FilmeController()
        
        self.criar_widgets()
        self.carregar_dados()

    def criar_widgets(self):
        lbl_titulo = tk.Label(self, text="Filmes Cadastrados", font=("Helvetica", 16, "bold"))
        lbl_titulo.pack(pady=10)

        # Frame para a Treeview e Scrollbar
        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=20, pady=10)

        # Scrollbar vertical
        scrollbar_v = ttk.Scrollbar(frame_tree, orient="vertical")
        scrollbar_v.pack(side="right", fill="y")

        # Scrollbar horizontal
        scrollbar_h = ttk.Scrollbar(frame_tree, orient="horizontal")
        scrollbar_h.pack(side="bottom", fill="x")

        # Filtro por gênero
        tk.Label(self, text="Filtrar por gênero").pack()

        self.combo_genero = ttk.Combobox(
            self,
            values=[
                "Todos",
                "Ação",
                "Comédia",
                "Terror",
                "Drama",
                "Romance",
                "Anime"
            ]
        )

        self.combo_genero.pack(pady=5)

        self.combo_genero.current(0)

        self.combo_genero.bind(
            "<<ComboboxSelected>>",
            self.filtrar_genero
        )

        # Treeview (Tabela)
        colunas = ("ID", "Título", "Gênero", "Ano", "Estoque", "Valor Locação")
        self.tree = ttk.Treeview(
            frame_tree,
            columns=colunas,
            show="headings",
            yscrollcommand=scrollbar_v.set,
            xscrollcommand=scrollbar_h.set
        )
        
        # Configurar cabeçalhos e colunas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Título", text="Título")
        self.tree.heading("Gênero", text="Gênero")
        self.tree.heading("Ano", text="Ano")
        self.tree.heading("Estoque", text="Estoque")
        self.tree.heading("Valor Locação", text="Valor Locação")

        self.tree.column("ID", anchor="center", width=60)
        self.tree.column("Título", anchor="w", width=250)
        self.tree.column("Gênero", anchor="center", width=120)
        self.tree.column("Ano", anchor="center", width=80)
        self.tree.column("Estoque", anchor="center", width=80)
        self.tree.column("Valor Locação", anchor="center", width=130)

        self.tree.pack(expand=True, fill="both")
        scrollbar_v.config(command=self.tree.yview)
        scrollbar_h.config(command=self.tree.xview)

    def carregar_dados(self):

        self.tree.delete(*self.tree.get_children())

        filmes = self.controller.listar_filmes()

        for filme in filmes:

            valor_formatado = f"R$ {filme.valor_locacao:.2f}"

            status = "Disponível" if filme.estoque > 0 else "Indisponível"

            self.tree.insert("", "end", values=(

                filme.id_filme,
                filme.titulo,
                filme.genero,
                filme.ano,
                filme.estoque,
                valor_formatado,
                status 
            ))

    def filtrar_genero(self, event):

        genero = self.combo_genero.get()

        self.tree.delete(*self.tree.get_children())

        if genero == "Todos":
            filmes = self.controller.listar_filmes()
        else:
            filmes = self.controller.buscar_por_genero(genero)

        for filme in filmes:
            self.tree.insert("", "end", values=(
                filme.id_filme,
                filme.titulo,
                filme.genero,
                filme.ano,
                filme.estoque,
                filme.valor_locacao
            ))

        