class TablesInfo:
    TABLES_DEFINITIONS = {
        "produtos": {
            "prod_id": "SERIAL PRIMARY KEY",
            "nome": "VARCHAR(100) NOT NULL",
            "preco": "NUMERIC(10, 2) NOT NULL",
            "quantidade": "INTEGER NOT NULL",
            "data_validade": "DATE NOT NULL",
            "data_fabricacao": "DATE NOT NULL",
            "descricao": "TEXT NOT NULL",
        },
    }
