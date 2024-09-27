from AuxiliaryFiles.SGBD import SGBD
from AuxiliaryFiles.Validator import Validator
from AuxiliaryFiles.TablesClasses import Seller
from typing import Optional, Tuple


class SellerAPI:
    sgbd: Optional[SGBD] = None
    vd: Optional[Validator] = None

    def __init__(self, sgbd: SGBD, vd: Validator) -> None:
        self.sgbd = sgbd
        self.vd = vd

    def login(self) -> Tuple[bool, int]:
        seller_id = self.vd.validate_int(
            "\nInsira o ID do vendedor: ",
            "Por favor, insira um ID valido.",
            lambda x: x > 0,
        )

        seller_data = self.sgbd.read("vendedor", "senha", f"vendedor_id = {seller_id}")

        if not seller_data:
            print("\nO vendedor informado nao esta registrado.")
            return (False, -1)

        password = self.vd.validate_str(
            "\nInsira a senha do vendedor: ",
            "Por favor, insira uma senha valida, com tamanho entre 3 e 20.\n",
            lambda x: 3 <= len(x) and len(x) <= 20,
        )

        seller_password = seller_data[0][0]
        if password != seller_password:
            print("\nA senha informada esta incorreta.")
            return (False, -1)

        print("\nLog in realizado com sucesso.")
        return (True, seller_id)

    def register(self) -> Tuple[bool, int]:
        password = self.vd.validate_str(
            "Informe a senha do administrador para realizar o cadastro de um novo funcionário: ",
            "\nPor favor, informe uma senha válida.\n",
            lambda x: 0 < len(x) and len(x) < 20
        )
        if password != "123":
            print("\nSenha incorreta. Cancelando o registro de novo vendedor.")
            return (False, -1)

        seller = Seller()
        seller_id = self.sgbd.insert("vendedor", seller.columns, seller.values, ("vendedor_id",))[0]
        print("\nCadastro realizado com sucesso.")
        print(f"O ID do vendedor cadastrado é: '{seller_id}', esse ID será utilizado junto da senha para realizar o login.")

        return (True, seller_id)
