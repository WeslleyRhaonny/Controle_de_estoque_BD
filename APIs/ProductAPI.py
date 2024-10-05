from AuxiliaryFiles.SGBD import SGBD
from AuxiliaryFiles.Validator import Validator
from AuxiliaryFiles.TablesClasses import Product
from time import sleep
from datetime import datetime, timedelta
from typing import Optional, List, Tuple


class ProductAPI:
    sgbd: Optional[SGBD] = None
    vd: Optional[Validator] = None

    def __init__(self, sgbd: SGBD, vd: Validator) -> None:
        self.sgbd = sgbd
        self.vd = vd

    def show_products(self, products: List[Tuple]):
        print(f"\n+{'-' * 119}+")
        print(f"| {'ID':^5} | {'Nome':^20} | {'Preco':^10} | Quantidade | Data de Validade | Data de Fabricacao | {'Categoria':^20} |")
        print(f"+{'-' * 119}+")
        for product in products:
            preco = f"{product[2]:.2f}"
            preco = f"R${preco}"
            preco = f"{preco:^10}"
            datav_centralizada = str(product[4]).center(16)
            dataf_centralizada = str(product[5]).center(18)
            print(f"| {product[0]:^5} | {product[1]:^20} | {preco} | {product[3]:^10} | {datav_centralizada} | {dataf_centralizada} | {product[7]:^20} |")
            sleep(0.1)
        print(f"+{'-' * 119}+")

    def search_product_by_name(self) -> None:
        name = self.vd.validate_str(
            "Insira o nome do produto: ",
            "Por favor, insira um nome valido.\n",
            lambda x: len(x) <= 100,
        )

        name = f"'{name.lower()}'"

        products = self.sgbd.read(
            "produto", 
            "*", 
            f"LOWER(nome) = LOWER({name})"
        )

        if not products:
            print("\nNao ha produtos registrados com o nome informado.\n")
        else:
            self.show_products(products)

    def search_product_by_price(self) -> None:
        print("\nPor favor, selecione uma opcao:")
        print("1. Preço minimo")
        print("2. Preço maximo")
        print("3. Faixa de preco")
        print("0. Sair")

        opt: int = self.vd.validate_int(
            "Escolha uma opcao: ",
            "\nPor favor, selecione uma opcao valida, entre 0 e 4.\n",
            lambda x: 0 <= x <= 3
        )

        min_price = -1
        max_price = -1
        if opt == 0:
            print("\nRetornando ao menu de visualizacao do estoque.")
            return
        if opt in (1, 3):
            min_price = self.vd.validate_float(
                "Informe o preço minimo: ",
                "\nPor favor, informe um preco valido (>= 0 e <= 100M).\n",
                lambda x: 0 <= x <= 99999999.99
            )
        if opt in (2, 3):
            max_price = self.vd.validate_float(
                "Informe o preco maximo: ",
                "\nPor favor, informe um preco valido (>= 0 e <= 100M).\n",
                lambda x: 0 <= x <= 99999999.99
            )

        products = []
        if opt == 1:
            products = self.sgbd.read(
                "produto",
                "*",
                f"{min_price} <= preco"
            )
        elif opt == 2:
            products = self.sgbd.read(
                "produto",
                "*",
                f"preco <= {max_price}"
            )
        elif opt == 3:
            products = self.sgbd.read(
                "produto",
                "*",
                f"{min_price} <= preco AND preco <= {max_price}"
            )

        if not products:
            print("\nNao ha produtos registrados com os precos desejados.\n")
        else:
            self.show_products(products)

    def search_product_by_category(self) -> None:
        category = self.vd.validate_str(
            "Insira a categoria do produto: ",
            "Por favor, insira uma categoria valida.\n",
            lambda x: len(x) <= 100,
        )

        category = f"'{category.lower()}'"

        products = self.sgbd.read(
            "produto", 
            "*", 
            f"LOWER(categoria) = LOWER({category})"
        )

        if not products:
            print("\nNao ha produtos registrados com a categoria informada.\n")
        else:
            self.show_products(products)

    def search_product_by_mari(self) -> None:
        products = self.sgbd.read(
            "produto", 
            "*", 
            "feito_em_mari = TRUE"
        )

        if not products:
            print("\nNao ha produtos registrados que foram feitos em Mari.\n")
        else:
            self.show_products(products)

    def search_product_by_less_5(self) -> None:
        products = self.sgbd.read(
            "produto", 
            "*", 
            "quantidade < 5"
        )

        if not products:
            print("\nNao ha produtos registrados com menos de 5 unidades no estoque.\n")
        else:
            self.show_products(products)

    def get_product_by_id(self, prod_id):
        product = self.sgbd.read(
            "produto",
            "*",
            f"prod_id = {prod_id}"
        )

        return product

    def list_all_products(self) -> None:
        products: Optional[List[Tuple]] = self.sgbd.read("produto", ("prod_id", "nome", "quantidade"))
        if not products:
            print("\nNao ha produtos disponiveis no momento.\n")
        else:
            print()
            print(f"\n+{'-' * 43}+")
            print(f"| {'ID':^5} | {'Nome':^20} | {'Quantidade':^10} |")
            print(f"+{'-' * 43}+")
            for product in products:
                print(f"| {product[0]:^5} | {product[1]:^20} | {product[2]:^10} |")
                sleep(0.1)
            print(f"+{'-' * 43}+")

    def insert_product(self) -> None:
        product = Product()
        self.sgbd.insert("produto", product.columns, product.values)
        print("\nProduto inserido com sucesso.")

    def modify_product(self) -> None:
        prod_id = self.vd.validate_int(
            "\nInsira o ID do produto: ",
            "Por favor, insira um ID valido.",
            lambda x: x > 0,
        )

        product_data = self.sgbd.read("produto", "*", f"prod_id = {prod_id}")
        if not product_data:
            print("\nO produto informado nao esta registrado.")
            return

        product_data = [str(x) for x in product_data[0]][1:]
        product = Product(product_data)

        wasAlterated = False
        while True:
            print("\nEscolha uma informação para alterar:")
            print("1. Nome")
            print("2. Preco")
            print("3. Quantidade")
            print("4. Data de validade")
            print("5. Data de fabricacao")
            print("6. Descricao")
            print("7. Categoria")
            print("8. Produzido em Mari")
            print("9. Finalizar alteracoes")
            opt: int = self.vd.validate_int(
                "Escolha uma opcao: ",
                "Por favor, selecione uma opcao valida, entre 1 e 9.\n",
                lambda x: 1 <= x <= 9,
            )

            if opt == 1:
                product.change_name(self.vd)
                wasAlterated = True
            elif opt == 2:
                product.change_price(self.vd)
                wasAlterated = True
            elif opt == 3:
                product.change_quantity(self.vd)
                wasAlterated = True
            elif opt == 4:
                product.change_exp_date(self.vd)
                wasAlterated = True
            elif opt == 5:
                product.change_fab_date(self.vd)
                wasAlterated = True
            elif opt == 6:
                product.change_description(self.vd)
                wasAlterated = True
            elif opt == 7:
                product.change_category(self.vd)
                wasAlterated = True
            elif opt == 8:
                product.change_mari(self.vd)
                wasAlterated = True
            elif opt == 9:
                break


        if wasAlterated:
            self.sgbd.update("produto", dict(zip(product.columns, product.values)), f"prod_id = {prod_id}")
            print("\nProduto alterado com sucesso.")
        else:
            print("\nNenhuma alteracao foi realizada.")

    def remove_product(self) -> None:
        prod_id = self.vd.validate_int(
            "Insira o ID do produto: ",
            "Por favor, insira um ID valido.\n",
            lambda x: x > 0,
        )

        rows_deleted = self.sgbd.delete("produto", f"prod_id = {prod_id}")
        if rows_deleted:
            print("\nProduto removido com sucesso.")
        else:
            print("\nO produto informado nao esta registrado.")

    def stock_report(self) -> None:
        out_of_stock_products = [" - ".join([str(y) for y in x]) for x in self.sgbd.read("produto", ("prod_id", "nome",), "quantidade = 0")]

        today_date = datetime.now().strftime('%Y-%m-%d')
        expired_products = [" - ".join([str(y) for y in x]) for x in self.sgbd.read("produto", ("prod_id", "nome",), f"data_validade < '{today_date}'")]

        expiration_date = (datetime.now() + timedelta(10)).strftime('%Y-%m-%d') 
        close_to_expiration_products = [" - ".join([str(y) for y in x]) for x in self.sgbd.read("produto", ("prod_id", "nome",), f"data_validade > '{today_date}' AND data_validade < '{expiration_date}'")]

        print(f"\n+{'-' * 60}+")
        sleep(0.1)
        print(f"| {'Relatorio de Estoque':^58} |")
        sleep(0.1)
        print(f"+{'-' * 60}+")
        sleep(0.1)
        print(f"| {'Numero de produtos registrados:':<38}{self.sgbd.count_rows('produto'):>20} |")
        sleep(0.1)
        print(f"+{'-' * 60}+")
        sleep(0.1)

        if out_of_stock_products == []:
            print(f"| {'Nao ha produtos faltando no estoque.':<58} |")
            sleep(0.1)
            print(f"+{'-' * 60}+")
            sleep(0.1)
        if expired_products == []:
            print(f"| {'Nao ha produtos estragados no estoque.':<58} |")
            sleep(0.1)
            print(f"+{'-' * 60}+")
            sleep(0.1)
        if close_to_expiration_products == []:
            print(f"| {'Nao ha produtos proximos da data de validade.':<58} |")
            sleep(0.1)
            print(f"+{'-' * 60}+")
            sleep(0.1)
        
        if out_of_stock_products != []:
            print(f"\n+{'-' * 60}+")
            sleep(0.1)
            print(f"| {'Produtos faltando no estoque':^58} |")
            sleep(0.1)
            print(f"+{'-' * 60}+")
            sleep(0.1)

            for product in out_of_stock_products:
                print(f"| {product:^58} |")
                sleep(0.1)
                print(f"+{'-' * 60}+")
                sleep(0.1)
        if expired_products != []:
            print(f"\n+{'-' * 60}+")
            sleep(0.1)
            print(f"| {'Produtos estragados no estoque':^58} |")
            sleep(0.1)
            print(f"+{'-' * 60}+")
            sleep(0.1)
            
            for product in expired_products:
                print(f"| {product:^58} |")
                sleep(0.1)
                print(f"+{'-' * 60}+")
                sleep(0.1)
        if close_to_expiration_products != []:
            print(f"\n+{'-' * 60}+")
            sleep(0.1)
            print(f"| {'Produtos próximos da data de validade':^58} |")
            sleep(0.1)
            print(f"+{'-' * 60}+")
            sleep(0.1)
            
            for product in close_to_expiration_products:
                print(f"| {product:^58} |")
                sleep(0.1)
                print(f"+{'-' * 60}+")
                sleep(0.1)

    def product_exists(self) -> int:
        id = self.vd.validate_int(
            "Insira o ID do produto: ",
            "Por favor, insira um ID valido.\n",
            lambda x: x >= 1
        )

        products = self.sgbd.read(
            "produto", 
            "*", 
            f"prod_id = {id}"
        )

        if products:
            return id
        else:
            return 0
