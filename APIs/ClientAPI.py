from AuxiliaryFiles.SGBD import SGBD
from AuxiliaryFiles.Validator import Validator
from AuxiliaryFiles.TablesClasses import Client
from typing import Optional, Tuple


class ClientAPI:
    sgbd: Optional[SGBD] = None
    vd: Optional[Validator] = None

    def __init__(self, sgbd: SGBD, vd: Validator) -> None:
        self.sgbd = sgbd
        self.vd = vd

    def login(self) -> Tuple[bool, int]:
        client_id = self.vd.validate_int(
            "\nInsira o ID do cliente: ",
            "Por favor, insira um ID valido.",
            lambda x: x > 0,
        )

        client_data = self.sgbd.read("cliente", "senha", f"cliente_id = {client_id}")

        if not client_data:
            print("\nO cliente informado nao esta registrado.")
            return (False, -1)

        password = self.vd.validate_str(
            "\nInsira a senha do cliente: ",
            "Por favor, insira uma senha valida, com tamanho entre 3 e 20.\n",
            lambda x: 3 <= len(x) and len(x) <= 20,
        )

        client_password = client_data[0][0]
        if password != client_password:
            print("\nA senha informada esta incorreta.")
            return (False, -1)

        print("\nLog in realizado com sucesso.")
        return (True, client_id)

    def register(self) -> Tuple[bool, int]:
        client = Client()
        client_id = self.sgbd.insert("cliente", client.columns, client.values, ("cliente_id",))[0]
        print("\nCadastro realizado com sucesso.")
        print(f"O ID do cliente cadastrado é: '{client_id}', esse ID será utilizado junto da senha para realizar o login.")

        return (True, client_id)
