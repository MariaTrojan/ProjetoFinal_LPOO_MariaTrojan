import tkinter as tk
from tkinter import messagebox

from control.locacao_controller import LocacaoController
from control.filme_controller import FilmeController
from control.cliente_controller import ClienteController
from strategy.calculo_padrao import CalculoPadrao
from datetime import datetime

class JanelaCadastroLocacao:

    def __init__(self, root):
        self.root = root
        self.root.title("Reservar Filme")
        self.root.geometry("400x450")

        self.controller = LocacaoController()
        self.filme_controller = FilmeController()
        self.cliente_controller = ClienteController()
        self.calculo_strategy = CalculoPadrao()

        # guarda o filme escolhido
        self.id_filme_selecionado = None
        self.filme_selecionado = None

        # CLIENTE
        tk.Label(root, text="Nome Cliente").grid(row=1, column=0, padx=10, pady=5)

        self.entry_nome = tk.Entry(root)
        self.entry_nome.grid(row=1, column=1)

        # BUSCAR FILME
        tk.Label(root, text="Buscar Filme").grid(row=2, column=0, padx=10, pady=5)

        self.entry_filme = tk.Entry(root)
        self.entry_filme.grid(row=2, column=1)

        # enquanto digita
        self.entry_filme.bind("<KeyRelease>", self.filtrar_filmes)

        self.lista_filmes = tk.Listbox(root, height=4)
        self.lista_filmes.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=10,
            sticky="ew"
        )

        self.lista_filmes.bind(
            "<<ListboxSelect>>",
            self.selecionar_filme
        )

        # DATA INÍCIO
        tk.Label(root, text="Data Início (DD-MM-AAAA)").grid(
            row=4, column=0, padx=10, pady=5
        )

        self.entry_data_inicio = tk.Entry(root)
        self.entry_data_inicio.grid(row=4, column=1)
        self.entry_data_inicio.bind("<KeyRelease>", lambda e: self.calcular_valor())

        # DATA FIM
        tk.Label(root, text="Data Fim (DD-MM-AAAA)").grid(
            row=5, column=0, padx=10, pady=5
        )

        self.entry_data_fim = tk.Entry(root)
        self.entry_data_fim.grid(row=5, column=1)
        self.entry_data_fim.bind("<KeyRelease>", lambda e: self.calcular_valor())

        # VALOR TOTAL
        tk.Label(root, text="Valor Total").grid(row=6, column=0, padx=10, pady=5)
        self.lbl_valor = tk.Label(root, text="R$ 0.00", font=("Arial", 12, "bold"), fg="green")
        self.lbl_valor.grid(row=6, column=1, padx=10, pady=5)

        # BOTÃO
        tk.Button(
            root,
            text="Reservar Filme",
            command=self.reservar_filme
        ).grid(row=7, column=0, columnspan=2, pady=20)

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
            f"{filme.id_filme} - {filme.titulo} ({filme.estoque} disponíveis)"
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
        
        # busca o filme para armazenar
        self.filme_selecionado = self.filme_controller.buscar_por_id(self.id_filme_selecionado)

        # coloca nome no entry
        self.entry_filme.delete(0, tk.END)
        self.entry_filme.insert(0, self.filme_selecionado.titulo)

        # limpa sugestões
        self.lista_filmes.delete(0, tk.END)
        
        # calcula valor
        self.calcular_valor()

    # =========================
    # RESERVAR
    # =========================
    def reservar_filme(self):
        try:
            nome_cliente = self.entry_nome.get().strip()
            data_inicio = datetime.strptime(
                self.entry_data_inicio.get().strip(),
                "%d-%m-%Y"
            ).date()

            data_fim = datetime.strptime(
                self.entry_data_fim.get().strip(),
                "%d-%m-%Y"
            ).date()

            if not nome_cliente:
                messagebox.showerror("Erro", "Informe o nome do cliente")
                return

            if self.id_filme_selecionado is None:
                messagebox.showerror("Erro", "Selecione um filme")
                return

            # busca cliente pelo nome (pega o primeiro resultado)
            clientes = self.cliente_controller.buscar_por_nome(nome_cliente)
            if not clientes:
                messagebox.showerror("Erro", "Cliente não encontrado. Cadastre o cliente primeiro.")
                return

            cliente = clientes[0]

            sucesso, msg = self.controller.criar_locacao(
                cliente.id_cliente,
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
    
    # =========================
    # CALCULAR VALOR
    # =========================
    def calcular_valor(self):
        if self.filme_selecionado is None:
            self.lbl_valor.config(text="R$ 0.00")
            return
        
        try:
            from datetime import datetime
            data_inicio_str = self.entry_data_inicio.get().strip()
            data_fim_str = self.entry_data_fim.get().strip()
            
            if not data_inicio_str or not data_fim_str:
                self.lbl_valor.config(text="R$ 0.00")
                return
            
            # converter strings para date
            data_inicio = datetime.strptime(data_inicio_str, "%d-%m-%Y").date()
            data_fim = datetime.strptime(data_fim_str, "%d-%m-%Y").date()
            
            # calcular dias
            dias = (data_fim - data_inicio).days
            if dias <= 0:
                dias = 1
            
            # usar strategy para calcular valor total
            valor_total = self.calculo_strategy.calcular(self.filme_selecionado.valor_locacao, dias)
            self.lbl_valor.config(text=f"R$ {valor_total:.2f}")
        except Exception as e:
            print(e)
            self.lbl_valor.config(text="R$ 0.00")


if __name__ == "__main__":
    root = tk.Tk()
    app = JanelaCadastroLocacao(root)
    root.mainloop()