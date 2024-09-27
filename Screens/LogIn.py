from AuxiliaryFiles.SGBD import SGBD
from AuxiliaryFiles.Validator import Validator
from APIs.ClientAPI import ClientAPI
from APIs.SellerAPI import SellerAPI
from typing import Optional, Union


class LogIn:
    sgbd: Optional[SGBD] = None
    vd: Optional[Validator] = None
    client_api: Optional[ClientAPI] = None
    seller_api: Optional[SellerAPI] = None

    def __init__(self, sgbd: SGBD, vd: Validator) -> None:
        self.sgbd = sgbd
        self.vd = vd
        self.client_api = ClientAPI(sgbd, vd)
        self.seller_api = SellerAPI(sgbd, vd)

    def main(self) -> None:
        while True:
            print("\n" + "=" * 60)
            print(f'{"Log In / Cadastro":^60}')
            print("=" * 60)
            print("\nPor favor, selecione uma opcao:")
            print("1. Log In")
            print("2. Cadastrar-se")
            print("0. Sair")
            opt: int = self.vd.validate_int(
                "Escolha uma opcao: ",
                "\nPor favor, selecione uma opcao valida, entre 0 e 2.\n",
                lambda x: 0 <= x <= 2
            )

            if opt == 0:
                return opt
            elif opt == 1:
                result = self.login()
                if result != False:
                    return result
            elif opt == 2:
                return self.register()

    def login(self) -> Union[int, bool]:
        print("\n" + "=" * 60)
        print(f'{"Log In":^60}')
        print("=" * 60)
        print("\nPor favor, selecione uma opcao:")
        print("1. Log In como Cliente")
        print("2. Log In como Vendedor")
        print("0. Sair")
        opt: int = self.vd.validate_int(
            "Escolha uma opcao: ",
            "\nPor favor, selecione uma opcao valida, entre 0 e 2.\n",
            lambda x: 0 <= x <= 2
        )

        if opt == 0:
            return opt
        elif opt == 1:
            return self.client_api.login()
        elif opt == 2:
            return self.seller_api.login()

    def register(self) -> int:
        while True:
            print("\n" + "=" * 60)
            print(f'{"Cadastro":^60}')
            print("=" * 60)
            print("\nPor favor, selecione uma opcao:")
            print("1. Cadastrar-se como Cliente")
            print("2. Cadastrar-se como Vendedor")
            print("0. Sair")
            opt: int = self.vd.validate_int(
                "Escolha uma opcao: ",
                "\nPor favor, selecione uma opcao valida, entre 0 e 2.\n",
                lambda x: 0 <= x <= 2
            )

            if opt == 0:
                return opt
            elif opt == 1:
                self.client_api.register_client()
                return opt
            elif opt == 2:
                if self.seller_api.register_seller():
                    return opt
