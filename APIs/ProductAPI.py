from AuxiliaryFiles.SGBD import SGBD
from AuxiliaryFiles.Validator import Validator
from time import sleep
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
            datav_centralizada = str(product[4]).center(16)
            dataf_centralizada = str(product[5]).center(18)
            print(f"| {product[0]:^5} | {product[1]:^20} | {product[2]:>10.2f} | {product[3]:>10} | {datav_centralizada} | {dataf_centralizada} | {product[7]:^20} |")
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
            print(f"\nNao ha produtos registrados com o nome informado.\n")
        else:
            self.show_products(products)
        sleep(3)

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
            print(f"\nNao ha produtos registrados com os precos desejados.\n")
        else:
            self.show_products(products)
        sleep(3)

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
            print(f"\nNao ha produtos registrados com a categoria informada.\n")
        else:
            self.show_products(products)
        sleep(3)

    def search_product_by_mari(self) -> None:
        products = self.sgbd.read(
            "produto", 
            "*", 
            "feito_em_mari = TRUE"
        )

        if not products:
            print(f"\nNao ha produtos registrados que foram feitos em Mari.\n")
        else:
            self.show_products(products)
        sleep(3)

    def list_all_products(self) -> None:
        products: Optional[List[Tuple]] = self.sgbd.read("produto", ("prod_id", "nome"))
        if not products:
            print("\nNao ha produtos disponiveis no momento.\n")
        else:
            print()
            print(f"\n+{'-' * 30}+")
            print(f"| {'ID':^5} | {'Nome':^20} |")
            print(f"+{'-' * 30}+")
            for product in products:
                print(f"| {product[0]:^5} | {product[1]:^20} |")
                sleep(0.1)
            print(f"+{'-' * 30}+")
        sleep(3)
