class TablesInfo:
    TABLES_DEFINITIONS = {
        "produto": {
            "prod_id": "SERIAL PRIMARY KEY",
            "nome": "VARCHAR(100) NOT NULL",
            "preco": "NUMERIC(10, 2) NOT NULL",
            "quantidade": "INTEGER NOT NULL CHECK (quantidade >= 0)",
            "data_validade": "DATE NOT NULL",
            "data_fabricacao": "DATE NOT NULL",
            "descricao": "TEXT NOT NULL",
            "categoria": "VARCHAR(100) NOT NULL",
            "feito_em_mari": "BOOLEAN NOT NULL",
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
            "cliente_id": "INTEGER NOT NULL REFERENCES cliente(cliente_id) ON UPDATE CASCADE ON DELETE CASCADE",
            "vendedor_id": "INTEGER NOT NULL REFERENCES vendedor(vendedor_id) ON UPDATE CASCADE ON DELETE CASCADE",
            "tipo_pagamento": "VARCHAR(50) NOT NULL",
            "data": "DATE NOT NULL"
        },
        "posse": {
            "compra_id": "INTEGER NOT NULL REFERENCES compra(compra_id) ON UPDATE CASCADE ON DELETE CASCADE",
            "prod_id": "INTEGER NOT NULL REFERENCES produto(prod_id) ON UPDATE CASCADE ON DELETE CASCADE",
            "quantidade": "INTEGER CHECK (quantidade >= 1) NOT NULL",
            "PRIMARY KEY (compra_id, prod_id)": ""
        }
    }
