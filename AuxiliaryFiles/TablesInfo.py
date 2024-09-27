class TablesInfo:
    TABLES_DEFINITIONS = {
        "produto": {
            "prod_id": "SERIAL PRIMARY KEY",
            "nome": "VARCHAR(100) NOT NULL",
            "preco": "NUMERIC(10, 2) NOT NULL",
            "quantidade": "INTEGER NOT NULL",
            "data_validade": "DATE NOT NULL",
            "data_fabricacao": "DATE NOT NULL",
            "descricao": "TEXT NOT NULL",
            "categoria": "VARCHAR(100) NOT NULL",
            "feito_em_mari": "BOOLEAN NOT NULL",
            "CONSTRAINT check_quantidade CHECK (quantidade >= 0)": ""
        },
        "cliente": {
            "cliente_id": "SERIAL PRIMARY KEY",
            "nome": "VARCHAR(100) NOT NULL",
            "senha": "VARCHAR(20) NOT NULL",
            "torce_flamengo": "BOOLEAN NOT NULL",
            "assiste_one_piece": "BOOLEAN NOT NULL",
            "mora_em_sousa": "BOOLEAN NOT NULL",
        },
        "vendedor": {
            "vendedor_id": "SERIAL PRIMARY KEY",
            "nome": "VARCHAR(100) NOT NULL",
            "senha": "VARCHAR(20) NOT NULL"
        },
        "compra": {
            "compra_id": "SERIAL PRIMARY KEY",
            "cliente_id": "INTEGER NOT NULL",
            "vendedor_id": "INTEGER NOT NULL",
            "tipo_pagamento": "VARCHAR(50) NOT NULL",
            "data": "DATE NOT NULL",
            "FOREIGN KEY (cliente_id) REFERENCES cliente(cliente_id) ON UPDATE CASCADE ON DELETE CASCADE": "",
            "FOREIGN KEY (vendedor_id) REFERENCES vendedor(vendedor_id) ON UPDATE CASCADE ON DELETE CASCADE": "",
        },
        "posse": {
            "compra_id": "INTEGER NOT NULL",
            "prod_id": "INTEGER NOT NULL",
            "quantidade": "INTEGER CHECK (quantidade >= 1) NOT NULL",
            "PRIMARY KEY (compra_id, prod_id)": "",
            "FOREIGN KEY (compra_id) REFERENCES compra(compra_id) ON UPDATE CASCADE ON DELETE CASCADE": "",
            "FOREIGN KEY (prod_id) REFERENCES produto(prod_id) ON UPDATE CASCADE ON DELETE CASCADE": "",
        }
    }
