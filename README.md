
# Sistema Locadora de Filmes

Projeto desenvolvido em Python utilizando Programação Orientada a Objetos (POO), interface gráfica com Tkinter e banco de dados PostgreSQL.

---

## Sobre o projeto

O sistema simula o funcionamento de uma locadora de filmes, permitindo o gerenciamento de clientes, catálogo de filmes e controle das locações.

O projeto possui separação entre área do cliente e área administrativa, aplicando conceitos de arquitetura em camadas.

---

## Diagrama de Classes
<img width="1081" height="1010" alt="Diagrama_Locadora_Filmes drawio" src="https://github.com/user-attachments/assets/f2247c73-af2d-402c-bdfc-6fa2bc2e70a7" />


## Funcionalidades

### Área do Cliente

* Cadastro de clientes
* Visualização do catálogo de filmes
* Reserva de filmes disponíveis

### Área do Administrador

* Login administrativo
* Cadastro de novos filmes
* Atualização de estoque
* Remoção de filmes
* Gerenciamento de clientes
* Aprovação de retirada do filme reservado
* Registro de devolução
* Cancelamento de reservas

---

## Estrutura do Projeto

```bash
Projeto-Locadora/

├── main.py

├── model/
│   ├── cliente.py
│   ├── filme.py
│   └── locacao.py

├── control/
│   ├── cliente_controller.py
│   ├── filme_controller.py
│   └── locacao_controller.py

├── dao/
│   ├── db_config.py
│   ├── generic_dao.py
│   ├── cliente_dao.py
│   ├── filme_dao.py
│   └── locacao_dao.py

└── view/
    ├── tela_cadastro_cliente.py
    ├── janela_listagem_filmes.py
    ├── janela_cadastro_locacao.py
    ├── tela_admin.py
    ├── tela_admin_clientes.py
    ├── tela_admin_filmes.py
    └── tela_admin_locacoes.py
```

## Padrões de Projeto Utilizados
* DAO
* Strategy

O sistema utiliza o padrão DAO (Data Access Object) para a persistência dos dados no PostgreSQL e o padrão Strategy para o cálculo do valor total das locações. 
O Strategy permite encapsular a lógica de cálculo em uma classe específica, facilitando a manutenção e futuras alterações nas regras de negócio.


---

## Tecnologias utilizadas

* Python 3
* Tkinter
* PostgreSQL
* psycopg2
* Programação Orientada a Objetos (POO)

---

## Banco de Dados

O sistema utiliza PostgreSQL com as seguintes tabelas:

### tb_clientes

* id_cliente
* nome
* cpf
* telefone

### tb_filmes

* id_filme
* filme_titulo
* filme_genero
* filme_ano
* filme_estoque
* filme_valor_locacao

### tb_locacoes

* id_locacao
* cliente_id
* filme_id
* data_inicio
* data_fim
* status

---

## Fluxo do sistema

1. Cliente realiza cadastro
2. Cliente visualiza catálogo de filmes
3. Cliente realiza reserva
4. Reserva fica com status **RESERVADO**
5. Administrador confirma retirada
6. Status altera para **LOCADO**
7. Cliente devolve o filme
8. Sistema calcula valor da locação
9. Estoque é atualizado automaticamente

---

## Conceitos aplicados

* Programação Orientada a Objetos
* Arquitetura MVC adaptada
* CRUD completo
* Conexão com banco de dados
* Interface gráfica
* Manipulação de exceções
* Encapsulamento
* Separação de responsabilidades

---

## Declaração de Uso de IA
- [ ] **Nenhuma IA foi utilizada** na elaboração deste código.
- [x] **Utilizei IA** como ferramenta de apoio.

- **Ferramenta(s):** ChatGPT
- **Finalidade:**  



