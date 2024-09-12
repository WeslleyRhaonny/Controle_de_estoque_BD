from SGBD import SGBD
from Validator import Validator
from TablesInfo import TablesInfo
from Product import Product
from time import sleep
from datetime import datetime, timedelta
from typing import Optional, List, Tuple


class Menu:
    sgbd: Optional[SGBD] = None
    vd: Optional[Validator] = None
    ti: Optional[TablesInfo] = None
    valid: bool = False

    def __init__(self) -> None:
        self.sgbd = SGBD()
        self.vd = Validator()
        self.ti = TablesInfo()

    def create_tables(self) -> None:
        if not self.valid:
            return

        for table_name, table_columns in self.ti.TABLES_DEFINITIONS.items():
            if not self.sgbd.table_exists(table_name):
                self.sgbd.create_table(table_name, table_columns)

    def delete_table(self, table: str) -> None:
        if not self.valid:
            return
        if self.sgbd.table_exists(table):
            self.sgbd.drop_table(table)

    def start(self) -> None:
        if self.valid:
            return

        self.valid = True
        self.sgbd.connect()
        self.create_tables()
        self.main_loop()

    def end(self) -> None:
        if self.valid:
            self.sgbd.close()
            self.valid = False

    @staticmethod
    def print_header() -> None:
        print("\n" + "=" * 60)
        print(f'{"Lojinha do Iury":^60}')
        print("=" * 60)
        print("\nBem vindo a Lojinha do Iury! Por favor, selecione uma opcao:")
        print("1. Inserir um produto")
        print("2. Modificar as informacoes de um produto")
        print("3. Procurar um produto pelo nome")
        print("4. Remover um produto")
        print("5. Listar todos os produtos")
        print("6. Mostrar um produto")
        print("7. Exibir relatorio de estoque:")
        print("8. Sair")

    def main_loop(self) -> None:
        while True:
            self.print_header()
            opt: int = self.vd.validate_int(
                "Escolha uma opcao: ",
                "\nPor favor, selecione uma opcao valida, entre 1 e 8.\n",
                lambda x: 1 <= x <= 8,
            )
            if opt == 1:
                self.insert_product()
            elif opt == 2:
                self.modify_product()
            elif opt == 3:
                self.search_product_by_name()
            elif opt == 4:
                self.remove_product()
            elif opt == 5:
                self.list_all_products()
            elif opt == 6:
                self.display_product()
            elif opt == 7:
                self.stock_report()
            elif opt == 8:
                break
            sleep(3)
        self.stock_report()
        self.end()

    def insert_product(self) -> None:
        product = Product()
        self.sgbd.insert("produtos", product.columns, product.values)
        print("\nProduto inserido com sucesso.")

    def modify_product(self) -> None:
        # Solicitar ao usuário o ID do produto que deseja modificar
        prod_id = self.vd.validate_int(
            "\nInsira o ID do produto: ",
            "Por favor, insira um ID valido.",
            lambda x: x > 0,
        )
        
        # Buscar o produto pelo ID na tabela 'produtos'
        product_data = self.sgbd.read("produtos", "*", f"prod_id = {prod_id}")
        if not product_data:
            print("O produto informado nao esta registrado.")
            return

        # Inicializar um dicionário para manter as alterações
        updates = {}

        while True:
            print("\nEscolha uma informação para alterar:")
            print("1. Nome")
            print("2. Preco")
            print("3. Quantidade")
            print("4. Data de validade")
            print("5. Data de fabricacao")
            print("6. Descricao")
            print("7. Finalizar alteracoes")
            opt: int = self.vd.validate_int(
                "Escolha uma opcao: ",
                "Por favor, selecione uma opcao valida, entre 1 e 7.\n",
                lambda x: 1 <= x <= 7,
            )

            if opt == 1:
                updates["nome"] = self.vd.validate_str(
                    "Insira o nome do produto (Com ate 100 caracteres): ",
                    "Por favor, insira um nome valido.\n",
                    lambda x: len(x) <= 100,
                )
            elif opt == 2:
                updates["preco"] = self.vd.validate_float(
                    "Insira o preco do produto: R$",
                    "Por favor, insira um valor valido.\n",
                    lambda x: x > 0,
                )
            elif opt == 3:
                updates["quantidade"] = self.vd.validate_int(
                    "Insira a quantidade do produto: ",
                    "Por favor, insira uma quantidade valida.\n",
                    lambda x: x >= 0,
                )
            elif opt == 4:
                updates["data_validade"] = self.vd.validate_date(
                    "Insira a data de validade do produto (Ano-Mes-Dia): ",
                    "Por favor, insira uma data de validade válida.\n",
                    lambda x: len(x) == 10,
                )
            elif opt == 5:
                updates["data_fabricacao"] = self.vd.validate_date(
                    "Insira a data de fabricacao do produto (Ano-Mes-Dia): ",
                    "Por favor, insira uma data de fabricacao válida.\n",
                    lambda x: len(x) == 10,
                )
            elif opt == 6:
                updates["descricao"] = self.vd.validate_str(
                    "Insira a descricao do produto: ",
                    "Por favor, insira uma descricao valida.\n",
                    lambda x: len(x) <= 200
                )
            elif opt == 7:
                break


        if updates:
            self.sgbd.update("produtos", updates, f"prod_id = {prod_id}")
            print("Produto alterado com sucesso.")
        else:
            print("Nenhuma alteracao foi realizada.")

    def search_product_by_name(self) -> None:
        # Solicitar ao usuário o nome do produto que deseja visualizar
        name = self.vd.validate_str(
            "Insira o nome do produto: ",
            "Por favor, insira um nome valido.\n",
            lambda x: len(x) <= 100,
        )

        # Convertendo o nome para minúsculas e adicionando aspas
        name = f"'{name.lower()}'"

        # Buscar o produto pelo nome na tabela 'produtos' com comparação case-insensitive
        products = self.sgbd.read(
            "produtos", 
            "*", 
            f"LOWER(nome) = LOWER({name})"
        )

        if not products:
            print(f"Nao ha produtos registrados com o nome informado.\n")
        else:
            print(f"+{'-' * 96}+")
            print(f"| {'ID':^5} | {'Nome':^20} | {'Preco':^10} | Quantidade | Data de Validade | Data de Fabricacao |")
            print(f"+{'-' * 96}+")
            for product in products:
                datav_centralizada = str(product[4]).center(16)
                dataf_centralizada = str(product[5]).center(18)
                
                print(f"| {product[0]:^5} | {product[1]:^20} | {product[2]:>10.2f} | {product[3]:>10} | {datav_centralizada} | {dataf_centralizada} |")
            print(f"+{'-' * 96}+")
            print("\n")   

    def remove_product(self) -> None:
        # Solicitar ao usuário o ID do produto que deseja remover
        prod_id = self.vd.validate_int(
            "Insira o ID do produto: ",
            "Por favor, insira um ID valido.\n",
            lambda x: x > 0,
        )

        # Tenta realizar a remoção do item escolhido
        rows_deleted = self.sgbd.delete("produtos", f"prod_id = {prod_id}")
        if rows_deleted:
            print("Produto removido com sucesso.")
        else:
            print("O produto informado nao esta registrado.")

    def list_all_products(self) -> None:
        products: Optional[List[Tuple]] = self.sgbd.read("produtos", ("prod_id", "nome"))
        if not products:
            print("Não há produtos disponíveis no momento.\n")
        else:
            print()
            for product in products:
                print(", ".join(str(item) for item in product))
                sleep(0.1)

    def display_product(self) -> None:
        # Solicitar ao usuário o ID do produto que deseja visualizar
        prod_id = self.vd.validate_int(
            "Insira o ID do produto: ",
            "Por favor, insira um ID valido.\n",
            lambda x: x > 0,
        )
        # Buscar o produto pelo ID na tabela 'produtos'
        product = self.sgbd.read("produtos", "*", f"prod_id = {prod_id}")

        if not product:
            print(f"O produto com o ID {prod_id} nao esta registrado.\n")
        else:
            print("\nInformacoes do produto:")
            print(f"ID: {product[0][0]}")
            print(f"Nome: {product[0][1]}")
            print(f"Preco: R${product[0][2]:.2f}")
            print(f"Quantidade: {product[0][3]}")
            print(f"Data de validade: {product[0][4]}")
            print(f"Data de fabricacao: {product[0][5]}")
            print(f"Descricao: {product[0][6]}")
            print("\n")    

    def stock_report(self) -> None:
        print(f"\n+{'-'*30}+")
        print(f"{'Relatorio de Estoque':^32}")
        print(f"+{'-'*30}+")

        print(f"\nNumero de produtos registrados: {self.sgbd.count_rows('produtos')}")

        out_of_stock_products = "\n".join([", ".join([str(y) for y in x]) for x in self.sgbd.read("produtos", ("prod_id", "nome",), "quantidade = 0")])
        if out_of_stock_products != "":
            print(f"Produtos faltando no estoque: {out_of_stock_products}")
        else:
            print("Nao ha produtos faltando no estoque.")

        today_date = datetime.now().strftime('%Y-%m-%d')
        expired_products = "\n".join([", ".join([str(y) for y in x]) for x in self.sgbd.read("produtos", ("prod_id", "nome",), f"data_validade < '{today_date}'")])
        if expired_products != "":
            print(f"Produtos estragados no estoque: {expired_products}")
        else:
            print("Nao ha produtos estragados no estoque.")

        expiration_date = (datetime.now() + timedelta(10)).strftime('%Y-%m-%d') 
        close_to_expiration_products = "\n".join([", ".join([str(y) for y in x]) for x in self.sgbd.read("produtos", ("prod_id", "nome",), f"data_validade > '{today_date}' AND data_validade < '{expiration_date}'")])
        if close_to_expiration_products != "":
            print(f"Produtos próximos da data de validade: {close_to_expiration_products}")
        else:
            print("Nao ha produtos proximos da data de validade.")
        
