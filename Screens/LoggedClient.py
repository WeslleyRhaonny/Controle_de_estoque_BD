from AuxiliaryFiles.SGBD import SGBD
from AuxiliaryFiles.Validator import Validator
from APIs.ProductAPI import ProductAPI
from APIs.ClientAPI import ClientAPI
from APIs.SellerAPI import SellerAPI
from APIs.ProceduresAPI import ProceduresAPI
from time import sleep
from typing import Optional


class LoggedClient:
    sgbd: Optional[SGBD] = None
    vd: Optional[Validator] = None
    prod_api: Optional[ProductAPI] = None
    client_api: Optional[ClientAPI] = None
    seller_api: Optional[SellerAPI] = None
    procedures_api: Optional[ProceduresAPI] = None
    cart: dict[int, int]

    def __init__(self, sgbd: SGBD, vd: Validator) -> None:
        self.sgbd = sgbd
        self.vd = vd
        self.prod_api = ProductAPI(sgbd, vd)
        self.client_api = ClientAPI(sgbd, vd)
        self.seller_api = SellerAPI(sgbd, vd)
        self.procedures_api = ProceduresAPI(sgbd)
        self.cart = {}

    @staticmethod
    def print_header() -> None:
        print("\n" + "=" * 60)
        print(f'{"Tela do Cliente":^60}')
        print("=" * 60)
        print("\nPor favor, selecione uma opcao:")
        print("1. Verificar seus dados")
        print("2. Verificar compras passadas")
        print("3. Adicionar produtos ao carrinho")
        print("4. Remover produtos do carrinho")
        print("5. Realizar compra")
        print("6. Procurar um produto")
        print("7. Listar todos os produtos")
        print("0. Sair")

    def main(self, client_id: int) -> None:
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
                self.client_api.verify_data(client_id)
            elif opt == 2:
                self.client_api.verify_purchases(client_id)
            elif opt == 3:
                self.add_product_to_cart()
            elif opt == 4:
                self.remove_product_from_cart()
            elif opt == 5:
                self.confirm_purchase(client_id)
            elif opt == 6:
                self.search_product()
            elif opt == 7:
                self.prod_api.list_all_products()
            sleep(3)

    def add_product_to_cart(self):
        id = self.prod_api.product_exists()
        if id == 0:
            print("\nNao ha produtos registrados com o ID informado.\n")
            return

        quantity = self.vd.validate_int(
            "Insira a quantidade desejada de tal produto: ",
            "\nPor favor, selecione uma quantidade valida.\n",
            lambda x: x >= 1
        )

        self.cart[id] = quantity
        print("\nProduto adicionado com sucesso.\n")

    def remove_product_from_cart(self):
        id = self.prod_api.product_exists()
        if id == 0:
            print("\nNao ha produtos registrados com o ID informado.\n")
            return
        elif id not in self.cart:
            print("\nNao ha produtos no carrinho com o ID informado.\n")
            return

        del self.cart[id]
        print("\nProduto removido com sucesso.\n")

    def confirm_purchase(self, client_id):
        if self.cart == {}:
            print("\nNao ha produtos no carrinho atualmente.\n")
            return

        seller_id = self.seller_api.select_seller()
        if seller_id == 0:
            return

        discount, invalid_product, total_price = self.procedures_api.validate_purchase(client_id, self.cart)
        total_price = float(total_price)

        if invalid_product != 0:
            product = self.prod_api.get_product_by_id(invalid_product)[0]
            print(f"\nNao ha em estoque a quantia desejada do produto '{product[1]}' com ID '{product[0]}', removendo-o do carrinho.\n")
            del self.cart[invalid_product]
            return

        payment_types = ["Cartao", "Boleto", "Pix", "Berries"]
        print(f"\nO total da compra foi de R${total_price:.2f}")
        if discount:
            print(f"Com um desconto de 10% aplicado ao cliente, o novo valor foi: R${total_price * 0.9:.2f}")
        print("Por favor, selecione uma forma de pagamento:")
        print(f"1. {payment_types[0]}")
        print(f"2. {payment_types[1]}")
        print(f"3. {payment_types[2]}")
        print(f"4. {payment_types[3]}")

        opt: int = self.vd.validate_int(
            "Escolha uma opcao: ",
            "\nPor favor, selecione uma opcao valida, entre 1 e 4.\n",
            lambda x: 1 <= x <= 4,
        )

        print(f"Forma de pagamento escolhida: {payment_types[opt - 1]}")

        while True:
            password = self.vd.validate_str(
                "Insira a senha do vendedor escolhido para validar a compra: ",
                "Por favor, insira uma senha valida, com tamanho entre 3 e 20.\n",
                lambda x: 3 <= len(x) and len(x) <= 20,
            )

            if password in self.seller_api.get_seller_by_id(seller_id)[0][2]:
                break

            print("\nSenha inserida incorreta, tente novamente.\n")

        if discount:
            total_price = total_price * (0.9)
        self.procedures_api.save_purchase(client_id, seller_id, payment_types[opt - 1], self.cart, total_price)
        print("\nCompra finalizada com sucesso.\n")

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
            print("\nRetornando ao menu do cliente.")
        elif opt == 1:
            self.prod_api.search_product_by_name()
        elif opt == 2:
            self.prod_api.search_product_by_price()
        elif opt == 3:
            self.prod_api.search_product_by_category()
        elif opt == 4:
            self.prod_api.search_product_by_mari()
