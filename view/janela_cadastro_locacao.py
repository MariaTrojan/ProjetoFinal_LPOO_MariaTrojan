import tkinter as tk
from tkinter import messagebox

from control.locacao_controller import LocacaoController
from control.filme_controller import FilmeController


class JanelaCadastroLocacao:

    def __init__(self, root):
        self.root = root
        self.root.title("Reservar Filme")
        self.root.geometry("400x350")

        self.controller = LocacaoController()
        self.filme_controller = FilmeController()

        # guarda o filme escolhido
        self.id_filme_selecionado = None

        # ID LOCAÇÃO
        tk.Label(root, text="ID Locação").grid(row=0, column=0, padx=10, pady=5)

        self.entry_id_locacao = tk.Entry(root)
        self.entry_id_locacao.grid(row=0, column=1)

        # CLIENTE
        tk.Label(root, text="Nome Cliente").grid(row=1, column=0, padx=10, pady=5)

        self.entry_nome = tk.Entry(root)
        self.entry_nome.grid(row=1, column=1)

        # BUSCAR FILME
        tk.Label(root, text="Buscar Filme").grid(row=2, column=0, padx=10, pady=5)

        self.entry_filme = tk.Entry(root)
        self.entry_filme.grid(row=2, column=1)

        # evento enquanto digita
        self.entry_filme.bind("<KeyRelease>", self.filtrar_filmes)

        # lista sugestões
        self.lista_filmes = tk.Listbox(root, height=4)
        self.lista_filmes.grid(row=3, column=0, columnspan=2, padx=10, sticky="ew")

        # clique na lista
        self.lista_filmes.bind("<<ListboxSelect>>", self.selecionar_filme)

        # DATA INÍCIO
        tk.Label(root, text="Data Início (DD-MM-AAAA)").grid(
            row=4, column=0, padx=10, pady=5
        )

        self.entry_data_inicio = tk.Entry(root)
        self.entry_data_inicio.grid(row=4, column=1)

        # DATA FIM
        tk.Label(root, text="Data Fim (DD-MM-AAAA)").grid(
            row=5, column=0, padx=10, pady=5
        )

        self.entry_data_fim = tk.Entry(root)
        self.entry_data_fim.grid(row=5, column=1)

        # BOTÃO
        tk.Button(
            root,
            text="Reservar Filme",
            command=self.reservar_filme
        ).grid(row=6, column=0, columnspan=2, pady=20)

    # =========================
    # FILTRAR FILMES
    # =========================
    def filtrar_filmes(self, event):

        texto = self.entry_filme.get().strip()

        # limpa lista
        self.lista_filmes.delete(0, tk.END)

        if texto == "":
            return

        filmes = self.filme_controller.buscar_por_nome(texto)

        for filme in filmes:
            self.lista_filmes.insert(
                tk.END,
                f"{filme.id_filme} - {filme.titulo}"
            )

    # =========================
    # ESCOLHER FILME
    # =========================
    def selecionar_filme(self, event):

        selecionado = self.lista_filmes.curselection()

        if not selecionado:
            return

        valor = self.lista_filmes.get(selecionado[0])

        partes = valor.split(" - ")

        self.id_filme_selecionado = int(partes[0])

        # coloca nome no entry
        self.entry_filme.delete(0, tk.END)
        self.entry_filme.insert(0, partes[1])

        # limpa sugestões
        self.lista_filmes.delete(0, tk.END)

    # =========================
    # RESERVAR
    # =========================
    def reservar_filme(self):

        try:
            id_locacao = int(self.entry_id_locacao.get())
            nome_cliente = self.entry_nome.get()
            data_inicio = self.entry_data_inicio.get()
            data_fim = self.entry_data_fim.get()

            if self.id_filme_selecionado is None:
                messagebox.showerror("Erro", "Selecione um filme")
                return

            sucesso, msg = self.controller.criar_locacao(
                id_locacao,
                nome_cliente,
                self.id_filme_selecionado,
                data_inicio,
                data_fim
            )

            if sucesso:
                messagebox.showinfo("Sucesso", msg)
            else:
                messagebox.showerror("Erro", msg)

        except Exception as e:
            messagebox.showerror("Erro", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = JanelaCadastroLocacao(root)
    root.mainloop()