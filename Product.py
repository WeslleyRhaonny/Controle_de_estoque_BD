from TablesInfo import TablesInfo
from Validator import Validator
from typing import Optional, Tuple, List


class Product:
    columns: Optional[Tuple[str]] = None
    values: Optional[List[str]] = None

    def __init__(self, values: Optional[List[str]] = None) -> None:
        """
        Inicializa um objeto Product com valores opcionais.

        :param values: Lista contendo os valores para as colunas do produto.
        """
        ti = TablesInfo.TABLES_DEFINITIONS["produtos"]
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
        self.changeName(vd)
        self.changePrice(vd)
        self.changeQuantity(vd)
        self.changeExpDate(vd)
        self.changeFabDate(vd)
        self.changeDescription(vd)

    def changeName(self, vd: Validator):
        self.values[0] = vd.validate_str(
            "\nInsira o nome do produto (Com ate 100 caracteres): ",
            "Por favor, insira um nome valido.\n",
            lambda x: len(x) <= 100,
        )
    
    def changePrice(self, vd: Validator):
        self.values[1] = str(vd.validate_float(
            "Insira o preco do produto: R$",
            "Por favor, insira um preco valido.\n",
            lambda x: x >= 0.01 and x <= 99999999.99,
        ))
    
    def changeQuantity(self, vd: Validator):
        self.values[2] = str(vd.validate_int(
            "Insira a quantidade do produto: ",
            "Por favor, insira uma quantidade valida.\n",
            lambda x: x >= 0,
        ))
    
    def changeExpDate(self, vd: Validator):
        self.values[3] = vd.validate_date(
            "Insira a data de validade do produto (Ano-Mes-Dia): ",
            "Por favor, insira uma data de validade válida.\n",
            lambda x: True,
        ).strftime("%Y-%m-%d")
        
    def changeFabDate(self, vd: Validator):
        self.values[4] = vd.validate_date(
            "Insira a data de fabricacao do produto (Ano-Mes-Dia): ",
            "Por favor, insira uma data de fabricacao válida.\n",
            lambda x: True,
        ).strftime("%Y-%m-%d")
    
    def changeDescription(self, vd: Validator):
        self.values[5] = vd.validate_str(
            "Insira a descricao do produto: ",
            "Por favor, insira uma descricao valida.\n",
            lambda x: True,
        )
