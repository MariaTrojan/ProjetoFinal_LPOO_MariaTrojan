import tkinter as tk
from tkinter import ttk, messagebox

from control.filme_controller import FilmeController


class TelaAdminFilmes(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master)

        self.title("Gerenciar Filmes")
        self.geometry("850x450")

        self.controller = FilmeController()

        self.criar_widgets()
        self.carregar_dados()


    def criar_widgets(self):

        tk.Label(
            self,
            text="Gerenciar Filmes",
            font=("Arial", 14)
        ).pack(pady=10)

        frame_form = tk.Frame(self)
        frame_form.pack(padx=20, pady=10, fill="x")

        tk.Label(frame_form, text="ID").grid(row=0, column=0, sticky="w")
        self.entry_id = tk.Entry(frame_form)
        self.entry_id.grid(row=0, column=1, sticky="ew", padx=5)

        tk.Label(frame_form, text="Título").grid(row=0, column=2, sticky="w")
        self.entry_titulo = tk.Entry(frame_form)
        self.entry_titulo.grid(row=0, column=3, sticky="ew", padx=5)

        tk.Label(frame_form, text="Gênero").grid(row=1, column=0, sticky="w")
        self.entry_genero = tk.Entry(frame_form)
        self.entry_genero.grid(row=1, column=1, sticky="ew", padx=5)

        tk.Label(frame_form, text="Ano").grid(row=1, column=2, sticky="w")
        self.entry_ano = tk.Entry(frame_form)
        self.entry_ano.grid(row=1, column=3, sticky="ew", padx=5)

        tk.Label(frame_form, text="Estoque").grid(row=2, column=0, sticky="w")
        self.entry_estoque = tk.Entry(frame_form)
        self.entry_estoque.grid(row=2, column=1, sticky="ew", padx=5)

        tk.Label(frame_form, text="Valor Locação").grid(row=2, column=2, sticky="w")
        self.entry_valor_locacao = tk.Entry(frame_form)
        self.entry_valor_locacao.grid(row=2, column=3, sticky="ew", padx=5)

        frame_form.columnconfigure(1, weight=1)
        frame_form.columnconfigure(3, weight=1)

        colunas = ("ID", "Título", "Gênero", "Ano", "Estoque", "Valor")

        self.tree = ttk.Treeview(
            self,
            columns=colunas,
            show="headings"
        )

        for coluna in colunas:
            self.tree.heading(coluna, text=coluna)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Button-1>", self.on_tree_click)
        self.tree.pack(expand=True, fill="both", padx=20, pady=10)

        frame_actions = tk.Frame(self)
        frame_actions.pack(pady=5)

        tk.Button(
            frame_actions,
            text="Cadastrar Filme",
            command=self.cadastrar_filme
        ).pack(side="left", padx=5)

        tk.Button(
            frame_actions,
            text="Editar Filme",
            command=self.editar_filme
        ).pack(side="left", padx=5)

        tk.Button(
            frame_actions,
            text="Remover Filme",
            command=self.remover_filme
        ).pack(side="left", padx=5)


    def carregar_dados(self):

        self.tree.delete(*self.tree.get_children())

        filmes = self.controller.listar_filmes()

        for filme in filmes:
            self.tree.insert("", "end", values=(
                filme.id_filme,
                filme.titulo,
                filme.genero,
                filme.ano,
                filme.estoque,
                filme.valor_locacao
            ))


    def cadastrar_filme(self):

        try:
            id_filme = int(self.entry_id.get().strip())
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser número inteiro")
            return

        titulo = self.entry_titulo.get().strip()
        genero = self.entry_genero.get().strip()

        if not titulo:
            messagebox.showerror("Erro", "Título obrigatório")
            return

        try:
            ano = int(self.entry_ano.get().strip())
        except ValueError:
            messagebox.showerror("Erro", "Ano deve ser número inteiro")
            return

        try:
            estoque = int(self.entry_estoque.get().strip())
        except ValueError:
            messagebox.showerror("Erro", "Estoque deve ser número inteiro")
            return

        try:
            valor_locacao = float(self.entry_valor_locacao.get().strip().replace(',', '.'))
        except ValueError:
            messagebox.showerror("Erro", "Valor de locação deve ser número")
            return

        sucesso, msg = self.controller.cadastrar_filme(
            id_filme,
            titulo,
            genero,
            ano,
            estoque,
            valor_locacao
        )

        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.carregar_dados()
        else:
            messagebox.showerror("Erro", msg)

    def editar_filme(self):

        selecionado = self.tree.selection()

        if not selecionado:
            messagebox.showerror("Erro", "Selecione um filme para editar")
            return

        try:
            id_filme = int(self.entry_id.get().strip())
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser número inteiro")
            return

        titulo = self.entry_titulo.get().strip()
        genero = self.entry_genero.get().strip()

        if not titulo:
            messagebox.showerror("Erro", "Título obrigatório")
            return

        try:
            ano = int(self.entry_ano.get().strip())
        except ValueError:
            messagebox.showerror("Erro", "Ano deve ser número inteiro")
            return

        try:
            estoque = int(self.entry_estoque.get().strip())
        except ValueError:
            messagebox.showerror("Erro", "Estoque deve ser número inteiro")
            return

        try:
            valor_locacao = float(self.entry_valor_locacao.get().strip().replace(',', '.'))
        except ValueError:
            messagebox.showerror("Erro", "Valor de locação deve ser número")
            return

        filme = self.controller.buscar_por_id(id_filme)

        if not filme:
            messagebox.showerror("Erro", "Filme não encontrado")
            return

        filme.titulo = titulo
        filme.genero = genero
        filme.ano = ano
        filme.estoque = estoque
        filme.valor_locacao = valor_locacao

        sucesso, msg = self.controller.atualizar_filme(filme)

        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.carregar_dados()
        else:
            messagebox.showerror("Erro", msg)

    def on_tree_select(self, event):

        selecionado = self.tree.selection()

        if not selecionado:
            return

        valores = self.tree.item(selecionado[0])["values"]

        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, valores[0])

        self.entry_titulo.delete(0, tk.END)
        self.entry_titulo.insert(0, valores[1])

        self.entry_genero.delete(0, tk.END)
        self.entry_genero.insert(0, valores[2])

        self.entry_ano.delete(0, tk.END)
        self.entry_ano.insert(0, valores[3])

        self.entry_estoque.delete(0, tk.END)
        self.entry_estoque.insert(0, valores[4])

        self.entry_valor_locacao.delete(0, tk.END)
        self.entry_valor_locacao.insert(0, valores[5])

    def on_tree_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "nothing":
            self.tree.selection_remove(self.tree.selection())

    def remover_filme(self):

        selecionado = self.tree.selection()

        if not selecionado:
            messagebox.showerror("Erro", "Selecione um filme")
            return

        valores = self.tree.item(selecionado[0])["values"]

        id_filme = valores[0]

        sucesso, msg = self.controller.remover_filme(id_filme)

        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.carregar_dados()

        else:
            messagebox.showerror("Erro", msg)