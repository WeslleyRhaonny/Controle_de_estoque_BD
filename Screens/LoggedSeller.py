from AuxiliaryFiles.SGBD import SGBD
from AuxiliaryFiles.Validator import Validator
from APIs.ProductAPI import ProductAPI
from APIs.MonthlyReportAPI import MonthlyReportAPI
from time import sleep
from typing import Optional

class LoggedSeller:
    sgbd: Optional[SGBD] = None
    vd: Optional[Validator] = None
    prod_api: Optional[ProductAPI] = None
    mr_api: Optional[MonthlyReportAPI] = None

    def __init__(self, sgbd: SGBD, vd: Validator) -> None:
        self.sgbd = sgbd
        self.vd = vd
        self.prod_api = ProductAPI(sgbd, vd)
        self.mr_api = MonthlyReportAPI(sgbd)

    @staticmethod
    def print_header() -> None:
        print("\n" + "=" * 60)
        print(f'{"Tela do Vendedor":^60}')
        print("=" * 60)
        print("\nPor favor, selecione uma opcao:")
        print("1. Inserir um produto")
        print("2. Modificar um produto")
        print("3. Remover um produto")
        print("4. Procurar um produto")
        print("5. Listar todos os produtos")
        print("6. Exibir relatorio mensal")
        print("7. Exibir relatorio do estoque")
        print("0. Sair")

    def main(self) -> None:
        while True:
            self.print_header()
            opt: int = self.vd.validate_int(
                "Escolha uma opcao: ",
                "\nPor favor, selecione uma opcao valida, entre 0 e 7.\n",
                lambda x: 0 <= x <= 7,
            )

            if opt == 0:
                return
            elif opt == 1:
                self.prod_api.insert_product()
            elif opt == 2:
                self.prod_api.modify_product()
            elif opt == 3:
                self.prod_api.remove_product()
            elif opt == 4:
                self.search_product()
            elif opt == 5:
                self.prod_api.list_all_products()
            elif opt == 6:
                self.mr_api.monthly_report()
            elif opt == 7:
                self.prod_api.stock_report()
            sleep(3)

    def search_product(self) -> None:
        print("\nPor favor, selecione uma opcao:")
        print("1. Procurar por Nome")
        print("2. Procurar por Preco")
        print("3. Procurar por Categoria")
        print("4. Procurar por produtos feitos em Mari")
        print("5. Procurar por produtos com menos de 5 no estoque")
        print("0. Sair")

        opt: int = self.vd.validate_int(
            "Escolha uma opcao: ",
            "\nPor favor, selecione uma opcao valida, entre 0 e 5.\n",
            lambda x: 0 <= x <= 5
        )

        if opt == 0:
            print("\nRetornando ao menu do vendedor.")
        elif opt == 1:
            self.prod_api.search_product_by_name()
        elif opt == 2:
            self.prod_api.search_product_by_price()
        elif opt == 3:
            self.prod_api.search_product_by_category()
        elif opt == 4:
            self.prod_api.search_product_by_mari()
        elif opt == 5:
            self.prod_api.search_product_by_less_5()

