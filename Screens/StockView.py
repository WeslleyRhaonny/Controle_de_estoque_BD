from AuxiliaryFiles.SGBD import SGBD
from AuxiliaryFiles.Validator import Validator
from APIs.ProductAPI import ProductAPI
from time import sleep
from typing import Optional


class StockView:
    sgbd: Optional[SGBD] = None
    vd: Optional[Validator] = None
    prod_api: Optional[ProductAPI] = None

    def __init__(self, sgbd: SGBD, vd: Validator) -> None:
        self.sgbd = sgbd
        self.vd = vd
        self.prod_api = ProductAPI(sgbd, vd)

    @staticmethod
    def print_header() -> None:
        print("\n" + "=" * 60)
        print(f'{"Visualizar Estoque (Como Visitante)":^60}')
        print("=" * 60)
        print("\nPor favor, selecione uma opcao:")
        print("1. Login / Cadastro")
        print("2. Procurar um produto")
        print("3. Listar todos os produtos")
        print("0. Sair")

    def main(self) -> int:
        while True:
            self.print_header()
            opt: int = self.vd.validate_int(
                "Escolha uma opcao: ",
                "\nPor favor, selecione uma opcao valida, entre 0 e 3.\n",
                lambda x: 0 <= x <= 3
            )

            if opt in (0, 1):
                return opt
            elif opt == 2:
                self.search_product()
            elif opt == 3:
                self.prod_api.list_all_products()
            sleep(3)

    def search_product(self) -> None:
        print("\nPor favor, selecione uma opcao:")
        print("1. Procurar por Nome")
        print("2. Procurar por Preco")
        print("3. Procurar por Categoria")
        print("4. Procurar por produtos feitos em Mari")
        print("0. Sair")

        opt: int = self.vd.validate_int(
            "Escolha uma opcao: ",
            "\nPor favor, selecione uma opcao valida, entre 0 e 4.\n",
            lambda x: 0 <= x <= 4
        )

        if opt == 0:
            print("\nRetornando ao menu de visualizacao do estoque.")
        elif opt == 1:
            self.prod_api.search_product_by_name()
        elif opt == 2:
            self.prod_api.search_product_by_price()
        elif opt == 3:
            self.prod_api.search_product_by_category()
        elif opt == 4:
            self.prod_api.search_product_by_mari()
