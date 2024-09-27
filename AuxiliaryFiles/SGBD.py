import psycopg2
from typing import Optional, Dict, List, Tuple, Union


class SGBD:
    def __init__(self, dbname: str, user: str, password: str, host: str, port: str) -> None:
        self.conn_params: Dict[str, str] = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port,
        }
        self.conn: Optional[psycopg2.extensions.connection] = None
        self.cur: Optional[psycopg2.extensions.cursor] = None

    def connect(self) -> None:
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            self.cur = self.conn.cursor()
        except Exception as e:
            print(f"Erro ao conectar: {e}")

    def close(self) -> None:
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def table_exists(self, table: str) -> bool:
        """
        Verifica se a tabela existe no banco de dados.

        :param table: Nome da tabela (pode incluir o esquema, ex: 'esquema.nome_da_tabela')
        :return: True se a tabela existir, False caso contrário
        """
        try:
            self.cur.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_name = %s
                )
                """,
                (table.split(".")[-1],),
            )
            return self.cur.fetchone()[0]
        except Exception as e:
            print(f"Erro ao verificar existência da tabela: {e}")
            return False

    def create_table(self, table: str, columns: Dict[str, str]) -> bool:
        """
        Cria uma nova tabela no banco de dados.

        :param table: Nome da tabela (pode incluir o esquema, ex: 'esquema.nome_da_tabela')
        :param columns: Dicionário de colunas e tipos (ex: {'col1': 'INTEGER', 'col2': 'VARCHAR(50)'})
        """
        if self.table_exists(table):
            print(f"Tabela {table} já existe.")
            return False

        try:
            col_defs: str = ", ".join(
                [f"{col} {dtype}" for col, dtype in columns.items()]
            )
            query: str = f"CREATE TABLE {table} ({col_defs})"
            self.cur.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao criar tabela: {e}")
            self.conn.rollback()
            return False

    def count_rows(self, table: str) -> Optional[int]:
        """
        Conta o número de registros na tabela especificada.

        :param table: Nome da tabela (pode incluir o esquema, ex: 'esquema.nome_da_tabela')
        :return: Número de registros na tabela ou None se houver um erro.
        """
        if not self.table_exists(table):
            print(f"Tabela {table} não existe.")
            return None

        try:
            query: str = f"SELECT COUNT(*) FROM {table}"
            self.cur.execute(query)
            count: int = self.cur.fetchone()[0]
            return count
        except Exception as e:
            print(f"Erro ao contar registros: {e}")
            return None

    def insert(self, table: str, columns: Tuple[str], values: Tuple, return_columns: Optional[Tuple[str]] = None) -> Optional[Union[str,  Tuple[str]]]:
        """
        Insere dados na tabela especificada.

        :param table: Nome da tabela (pode incluir o esquema, ex: 'esquema.nome_da_tabela')
        :param columns: Lista de colunas (em formato de string, ex: ['col1', 'col2'])
        :param values: Lista de valores a serem inseridos (em formato de tupla, ex: (val1, val2))
        """
        if not self.table_exists(table):
            print(f"Tabela {table} não existe.")
            return None

        try:
            col_str: str = ", ".join(columns)
            val_placeholders: str = ", ".join(["%s"] * len(values))
            if return_columns:
                return_str = ", ".join(return_columns)
                query: str = f"INSERT INTO {table} ({col_str}) VALUES ({val_placeholders}) RETURNING {return_str}"
            else:
                query: str = f"INSERT INTO {table} ({col_str}) VALUES ({val_placeholders})"
            
            self.cur.execute(query, values)
            if return_columns:
                result = self.cur.fetchone()
            self.conn.commit()
            return result if result else None
        except Exception as e:
            print(f"Erro ao inserir dados: {e}")
            self.conn.rollback()

    def read(self, table: str, columns: Union[str, Tuple[str]] = "*", conditions: Optional[str] = None) -> Optional[List[Tuple]]:
        """
        Lê dados da tabela especificada.

        :param table: Nome da tabela (pode incluir o esquema, ex: 'esquema.nome_da_tabela')
        :param columns: Colunas a serem selecionadas (pode ser uma lista de colunas ou uma string '*')
        :param conditions: Condições da consulta (em formato de string SQL, ex: "id = 1")
        :return: Resultado da consulta
        """
        if not self.table_exists(table):
            print(f"Tabela {table} não existe.")
            return None

        try:
            if isinstance(columns, tuple):
                col_str = ", ".join(columns)
            else:
                col_str = columns

            query = f"SELECT {col_str} FROM {table}"
            if conditions:
                query += f" WHERE {conditions}"
            self.cur.execute(query)
            results = self.cur.fetchall()
            return results
        except Exception as e:
            print(f"Erro ao ler dados: {e}")
            return None

    def update(self, table: str, updates: Dict[str, Union[str, int, float]], conditions: str) -> None:
        """
        Atualiza dados na tabela especificada.

        :param table: Nome da tabela (pode incluir o esquema, ex: 'esquema.nome_da_tabela')
        :param updates: Dicionário de colunas e valores para atualização (ex: {'col1': 'novo_valor', 'col2': 123})
        :param conditions: Condições para a atualização (em formato de string SQL, ex: "id = 1")
        """
        if not self.table_exists(table):
            print(f"Tabela {table} não existe.")
            return

        try:
            set_clause: str = ", ".join([f"{col} = %s" for col in updates.keys()])
            values: Tuple = tuple(updates.values())
            query: str = f"UPDATE {table} SET {set_clause} WHERE {conditions}"
            self.cur.execute(query, values)
            self.conn.commit()
        except Exception as e:
            print(f"Erro ao atualizar dados: {e}")
            self.conn.rollback()

    def delete(self, table: str, conditions: str) -> bool:
        """
        Remove dados da tabela especificada.

        :param table: Nome da tabela (pode incluir o esquema, ex: 'esquema.nome_da_tabela')
        :param conditions: Condições para a remoção (em formato de string SQL, ex: "id = 1")
        """
        if not self.table_exists(table):
            print(f"Tabela {table} não existe.")
            return

        try:
            query: str = f"DELETE FROM {table} WHERE {conditions}"
            self.cur.execute(query)
            rows_deleted = self.cur.rowcount > 0
            if rows_deleted:
                self.conn.commit()
            else:
                self.conn.rollback()
            return rows_deleted
        except Exception as e:
            print(f"Erro ao remover dados: {e}")
            self.conn.rollback()
            return False

    def drop_table(self, table: str) -> None:
        """
        Remove a tabela especificada do banco de dados.

        :param table: Nome da tabela (pode incluir o esquema, ex: 'esquema.nome_da_tabela')
        """
        if not self.table_exists(table):
            print(f"Tabela {table} não existe.")
            return

        try:
            query: str = f"DROP TABLE {table}"
            self.cur.execute(query)
            self.conn.commit()
            print(f"Tabela {table} removida com sucesso.")
        except Exception as e:
            print(f"Erro ao remover tabela: {e}")
            self.conn.rollback()







#############################
#
#       EXEMPLO DE USO
#
#############################
"""
from TablesInfo import TablesInfo

# Cria uma instância da classe SGBD
sgbd = SGBD()
sgbd.connect()

# **1. Inserir Dados**
ti = TablesInfo()
table_name = 'produtos'
columns = tuple(ti.TABLES_DEFINITIONS["produtos"].keys())[1:]
values = ('Produto A', 19.99, 100, '2025-12-31', '2024-01-01', 'Descrição do Produto A')

sgbd.insert(table_name, columns, values)

# **2. Ler Dados**

columns_to_read = ['nome', 'preco', 'quantidade']
results = sgbd.read(table_name, columns_to_read)

print("Dados lidos da tabela:")
for row in results:
    print(row)

# **3. Atualizar Dados**

updates = {
    'preco': 24.99
}
conditions = "nome = 'Produto A'"

sgbd.update(table_name, updates, conditions)

# **4. Deletar Dados**

conditions = "nome = 'Produto A'"

sgbd.delete(table_name, conditions)

# Fecha a conexão com o banco de dados
sgbd.close()
"""