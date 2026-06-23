import tkinter as tk
from tkinter import ttk, messagebox

from control.locacao_controller import LocacaoController
from strategy.calculo_padrao import CalculoPadrao


class TelaAdminLocacoes(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master)

        self.title("Gerenciar Locações")
        self.geometry("900x450")

        self.controller = LocacaoController()
        self.calculo_strategy = CalculoPadrao()

        self.criar_widgets()
        self.carregar_dados()


    def criar_widgets(self):

        tk.Label(
            self,
            text="Locações",
            font=("Arial", 14)
        ).pack(pady=10)

        colunas = ("ID", "Cliente", "Filme", "Data Início", "Data Fim", "Status", "Valor Total")

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
            text="Confirmar Retirada",
            command=self.retirar
        ).pack(pady=5)

        tk.Button(
            self,
            text="Registrar Devolução",
            command=self.devolver
        ).pack(pady=5)

        tk.Button(
            self,
            text="Cancelar Reserva",
            command=self.cancelar
        ).pack(pady=5)


    def carregar_dados(self):

        self.tree.delete(*self.tree.get_children())

        locacoes = self.controller.listar_locacoes()

        if locacoes is None:
            locacoes = []

        for locacao in locacoes:
            filme = self.controller.filme_dao.buscar_por_id(locacao.id_filme)
            nome_filme = filme.titulo if filme else "N/A"
            valor_filme = filme.valor_locacao if filme else 0
            
            cliente = self.controller.cliente_dao.buscar_por_id(locacao.id_cliente)
            nome_cliente = cliente.nome if cliente else "N/A"
            
            # calcular valor total usando a strategy
            try:
                from datetime import datetime
                data_inicio = locacao.data_inicio
                data_fim = locacao.data_fim
                
                if isinstance(data_inicio, str):
                    data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
                if isinstance(data_fim, str):
                    data_fim = datetime.strptime(data_fim, "%Y-%m-%d").date()
                
                dias = (data_fim - data_inicio).days
                if dias <= 0:
                    dias = 1
                
                # usar strategy para calcular
                valor_total = self.calculo_strategy.calcular(valor_filme, dias)
            except:
                valor_total = 0
            
            self.tree.insert("", "end", values=(
                locacao.id,
                nome_cliente,
                nome_filme,
                locacao.data_inicio,
                locacao.data_fim,
                locacao.status.value,
                f"R$ {valor_total:.2f}"
            ))


    def retirar(self):

        selecionado = self.tree.selection()

        if not selecionado:
            return

        valores = self.tree.item(selecionado[0])["values"]

        id_locacao = valores[0]

        locacao = self.controller.buscar_por_id(id_locacao)

        sucesso, msg = self.controller.retirar_filme(
            locacao,
            id_locacao
        )

        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.carregar_dados()

        else:
            messagebox.showerror("Erro", msg)


    def devolver(self):

        selecionado = self.tree.selection()

        if not selecionado:
            return

        valores = self.tree.item(selecionado[0])["values"]

        id_locacao = valores[0]

        locacao = self.controller.buscar_por_id(id_locacao)

        sucesso, msg = self.controller.devolver_filme(
            locacao,
            id_locacao
        )

        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.carregar_dados()

        else:
            messagebox.showerror("Erro", msg)

    def cancelar(self):

        selecionado = self.tree.selection()

        if not selecionado:
            messagebox.showerror("Erro", "Selecione uma locação")
            return

        valores = self.tree.item(selecionado[0])["values"]

        id_locacao = valores[0]

        locacao = self.controller.buscar_por_id(id_locacao)

        sucesso, msg = self.controller.cancelar_reserva(
            locacao,
            id_locacao
        )

        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.carregar_dados()

        else:
            messagebox.showerror("Erro", msg)