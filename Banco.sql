


CREATE TABLE tb_clientes (
    id_cliente INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    telefone VARCHAR(20)
);

 

CREATE TABLE tb_filmes (
    id_filme INT PRIMARY KEY,
    filme_titulo VARCHAR(100) NOT NULL,
    filme_genero VARCHAR(50),
    filme_ano INT,
    filme_estoque INT NOT NULL,
    filme_valor_locacao DECIMAL(10,2) NOT NULL
);

CREATE TABLE tb_locacoes (
    loc_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    loc_cliente_id INT NOT NULL,
    loc_filme_id INT NOT NULL,
    loc_data_inicio DATE NOT NULL,
    loc_data_fim DATE,
    loc_status VARCHAR(20) NOT NULL,

    FOREIGN KEY (loc_cliente_id) REFERENCES tb_clientes(id_cliente),
    FOREIGN KEY (loc_filme_id) REFERENCES tb_filmes(id_filme)
);

DROP TABLE tb_clientes, tb_filmes, tb_locacoes CASCADE
SELECT * FROM tb_locacoes;
