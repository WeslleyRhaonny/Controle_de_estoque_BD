from AuxiliaryFiles.SGBD import SGBD
from AuxiliaryFiles.Validator import Validator
from AuxiliaryFiles.TablesClasses import Client
from time import sleep
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

    def verify_data(self, client_id):
        client_data = self.sgbd.read(
            "cliente", 
            "*", 
            f"cliente_id = {client_id}"
        )[0]

        print(f"\n+{'-' * 110}+")
        sleep(0.1)
        print(f"| {'ID':^5} | {'Nome':^20} | {'Senha':^20} | Torce pro Flamengo | Assiste One Piece | Mora em Sousa |")
        sleep(0.1)
        print(f"+{'-' * 110}+")
        sleep(0.1)
        print(f"| {client_data[0]:^5} | {client_data[1]:^20} | {client_data[2]:^20} | {'Sim' if client_data[3] else 'Nao':^18} | {'Sim' if client_data[4] else 'Nao':^17} | {'Sim' if client_data[5] else 'Nao':^13} |")
        sleep(0.1)
        print(f"+{'-' * 110}+")
        sleep(0.1)

    def verify_purchases(self, client_id):
        purchases = self.sgbd.read(custom_query=f"""
                                    SELECT 
                                        c.compra_id,
                                        c.data AS "Data da Compra",
                                        v.nome AS "Nome do Vendedor",
                                        c.preco_total AS "Preço Total"
                                    FROM 
                                        compra c
                                    JOIN 
                                        vendedor v ON c.vendedor_id = v.vendedor_id
                                    WHERE 
                                        c.cliente_id = {client_id}
                                    ORDER BY 
                                        c.data ASC;
                                    """
                                )

        if not purchases:
            print("\nNao ha compras registradas.\n")
            return


        print(f"\n+{'-' * 70}+")
        sleep(0.1)
        print(f"| {'ID da Compra':^12} | {'Data da Compra':^15} | {'Vendedor':^20} | {'Preço Total':^12} |")
        sleep(0.1)
        print(f"+{'-' * 70}+")
        sleep(0.1)
        for purchase in purchases:
            print(f"| {purchase[0]:^12} | {purchase[1].strftime('%Y-%m-%d'):^15} | {purchase[2]:^20} | {purchase[3]:>12.2f} |")
            sleep(0.1)
        print(f"+{'-' * 70}+")
        sleep(0.1)
