from AuxiliaryFiles.TablesInfo import TablesInfo
from AuxiliaryFiles.SGBD import SGBD
from AuxiliaryFiles.Validator import Validator
from typing import Optional, Tuple, List


class Product:
    columns: Optional[Tuple[str]] = None
    values: Optional[List[str]] = None

    def __init__(self, values: Optional[List[str]] = None) -> None:
        """
        Inicializa um objeto Product com valores opcionais.

        :param values: Lista contendo os valores para as colunas do produto.
        """
        ti = TablesInfo.TABLES_DEFINITIONS["produto"]
        self.columns = tuple(ti.keys())[1:]
        if values:
            self.values = values
        else:
            self.initiate_values()

    def initiate_values(self) -> None:
        """
        Inicializa os valores para as colunas do produto.
        """
        vd = Validator()
        self.values = [None] * len(self.columns)
        self.change_name(vd)
        self.change_price(vd)
        self.change_quantity(vd)
        self.change_exp_date(vd)
        self.change_fab_date(vd)
        self.change_description(vd)
        self.change_category(vd)
        self.change_mari(vd)

    def change_name(self, vd: Validator):
        self.values[0] = vd.validate_str(
            "\nInsira o nome do produto (Com ate 100 caracteres): ",
            "Por favor, insira um nome valido.\n",
            lambda x: len(x) <= 100,
        )

    def change_price(self, vd: Validator):
        self.values[1] = str(vd.validate_float(
            "\nInsira o preco do produto: R$",
            "Por favor, insira um preco valido.\n",
            lambda x: x >= 0.01 and x <= 99999999.99,
        ))

    def change_quantity(self, vd: Validator):
        self.values[2] = str(vd.validate_int(
            "\nInsira a quantidade do produto: ",
            "Por favor, insira uma quantidade valida.\n",
            lambda x: x >= 0,
        ))

    def change_exp_date(self, vd: Validator):
        self.values[3] = vd.validate_date(
            "\nInsira a data de validade do produto (Ano-Mes-Dia): ",
            "Por favor, insira uma data de validade válida.\n",
            lambda x: True,
        ).strftime("%Y-%m-%d")

    def change_fab_date(self, vd: Validator):
        self.values[4] = vd.validate_date(
            "\nInsira a data de fabricacao do produto (Ano-Mes-Dia): ",
            "Por favor, insira uma data de fabricacao válida.\n",
            lambda x: True,
        ).strftime("%Y-%m-%d")

    def change_description(self, vd: Validator):
        self.values[5] = vd.validate_str(
            "\nInsira a descricao do produto: ",
            "Por favor, insira uma descricao valida.\n",
            lambda x: True,
        )

    def change_category(self, vd: Validator):
        self.values[6] = vd.validate_str(
            "\nInsira a categoria do produto (Com ate 100 caracteres): ",
            "Por favor, insira uma categoria valida.\n",
            lambda x: len(x) <= 100,
        )

    def change_mari(self, vd: Validator):
        opt = vd.validate_str(
            "\nInforme se o produto foi feito em Mari [S/N]: ",
            "Por favor, responda apenas com 'Sim' ou 'Não'.\n",
            lambda x: x[0].lower() in "sn"
        )
        self.values[7] = "TRUE" if opt in ['s', 'S'] else "FALSE"


# class Client:
#     columns: Optional[Tuple[str]] = None
#     values: Optional[List[str]] = None

#     def __init__(self, values: Optional[List[str]] = None) -> None:
#         """
#         Inicializa um objeto Client com valores opcionais.

#         :param values: Lista contendo os valores para as colunas do cliente.
#         """
#         ti = TablesInfo.TABLES_DEFINITIONS["cliente"]
#         self.columns = tuple(ti.keys())[1:]
#         if values:
#             self.values = values
#         else:
#             self.initiate_values()

#     def initiate_values(self) -> None:
#         """
#         Inicializa os valores para as colunas do cliente.
#         """
#         vd = Validator()
#         self.values = [None] * len(self.columns)
#         self.change_name(vd)
#         self.change_password(vd)
#         self.change_flamengo(vd)
#         self.change_one_piece(vd)
#         self.change_sousa(vd)

#     def change_name(self, vd: Validator):
#         self.values[0] = vd.validate_str(
#             "\nInsira o nome do cliente (Com ate 100 caracteres): ",
#             "Por favor, insira um nome valido.\n",
#             lambda x: len(x) <= 100,
#         )

#     def change_password(self, vd: Validator):
#         self.values[1] = vd.validate_str(
#             "Insira a senha do cliente (Com ate 20 caracteres): ",
#             "Por favor, insira uma senha valida, com tamanho entre 3 e 20.\n",
#             lambda x: 3 <= len(x) and len(x) <= 20,
#         )

#     def change_flamengo(self, vd: Validator):
#         opt = vd.validate_str(
#             "Informe se o cliente torce para o Flamengo [S/N]: ",
#             "Por favor, responda apenas com 'Sim' ou 'Não'.\n",
#             lambda x: x[0].lower() in "sn"
#         )
#         self.values[2] = "TRUE" if opt in ['s', 'S'] else "FALSE"

#     def change_one_piece(self, vd: Validator):
#         opt = vd.validate_str(
#             "Informe se o cliente assiste One Piece [S/N]: ",
#             "Por favor, responda apenas com 'Sim' ou 'Não'.\n",
#             lambda x: x[0].lower() in "sn"
#         )
#         self.values[3] = "TRUE" if opt in ['s', 'S'] else "FALSE"

#     def change_sousa(self, vd: Validator):
#         opt = vd.validate_str(
#             "Informe se o cliente mora em Sousa [S/N]: ",
#             "Por favor, responda apenas com 'Sim' ou 'Não'.\n",
#             lambda x: x[0].lower() in "sn"
#         )
#         self.values[4] = "TRUE" if opt in ['s', 'S'] else "FALSE"

class Client:
    columns: Optional[Tuple[str]] = None
    values: Optional[List[str]] = None

    def __init__(self, name: str, password: str, flamengo: int, one_piece: int, sousa: int) -> None:
        """
        Inicializa um objeto Client com valores fornecidos da interface de cadastro.

        :param name: Nome do cliente.
        :param password: Senha do cliente.
        :param flamengo: Indica se o cliente torce para o Flamengo (1 para sim, 0 para não).
        :param one_piece: Indica se o cliente assiste One Piece (1 para sim, 0 para não).
        :param sousa: Indica se o cliente mora em Sousa (1 para sim, 0 para não).
        """
        ti = TablesInfo.TABLES_DEFINITIONS["cliente"]
        self.columns = tuple(ti.keys())[1:]  # Define as colunas da tabela
        self.values = [
            name,  # Nome
            password,  # Senha
            "TRUE" if flamengo else "FALSE",  # Torce Flamengo
            "TRUE" if one_piece else "FALSE",  # Assiste One Piece
            "TRUE" if sousa else "FALSE"  # Mora em Sousa
        ]


class Seller:
    columns: Optional[Tuple[str]] = None
    values: Optional[List[str]] = None

    def __init__(self, values: Optional[List[str]] = None) -> None:
        """
        Inicializa um objeto Seller com valores opcionais.

        :param values: Lista contendo os valores para as colunas do vendedor.
        """
        ti = TablesInfo.TABLES_DEFINITIONS["vendedor"]
        self.columns = tuple(ti.keys())[1:]
        if values:
            self.values = values
        else:
            self.initiate_values()

    def initiate_values(self) -> None:
        """
        Inicializa os valores para as colunas do vendedor.
        """
        vd = Validator()
        self.values = [None] * len(self.columns)
        self.change_name(vd)
        self.change_password(vd)

    def change_name(self, vd: Validator):
        self.values[0] = vd.validate_str(
            "\nInsira o nome do vendedor (Com ate 100 caracteres): ",
            "Por favor, insira um nome valido.\n",
            lambda x: len(x) <= 100,
        )

    def change_password(self, vd: Validator):
        self.values[1] = vd.validate_str(
            "Insira a senha do vendedor (Com ate 20 caracteres): ",
            "Por favor, insira uma senha valida, com tamanho entre 3 e 20.\n",
            lambda x: 3 <= len(x) and len(x) <= 20,
        )


class Purchase:
    columns: Optional[Tuple[str]] = None
    values: Optional[List[str]] = None

    def __init__(self, values: List[str], sgbd: SGBD) -> bool:
        """
        Inicializa um objeto Purchase.

        :param values: Lista contendo os valores para as colunas da compra.
        :param sgbd: Gerenciador de banco de dados para verificar as referências.
        :return: Valor booleano informando se a compra possui referências válidas.
        """
        ti = TablesInfo.TABLES_DEFINITIONS["compra"]
        self.columns = tuple(ti.keys())[1:]
        self.values = values

        client = sgbd.read("cliente", "*", f"cliente_id = {values[0]}")
        seller = sgbd.read("vendedor", "*", f"vendedor_id = {values[1]}")

        if not client or not seller:
            return False

        return True


class Possess:
    columns: Optional[Tuple[str]] = None
    values: Optional[List[str]] = None

    def __init__(self, values: List[str], sgbd: SGBD) -> None:
        """
        Inicializa um objeto Possess.

        :param values: Lista contendo os valores para as colunas do produto.
        :param sgbd: Gerenciador de banco de dados para verificar as referências.
        :return: Valor booleano informando se a posse tem referências válidas. 
        """
        ti = TablesInfo.TABLES_DEFINITIONS["posse"]
        self.columns = tuple(ti.keys())[1:]
        self.values = values

        purchase = sgbd.read("compra", "*", f"compra_id = {values[0]}")
        product = sgbd.read("produto", "*", f"prod_id = {values[1]}")

        if not purchase or not product:
            return False

        return True
