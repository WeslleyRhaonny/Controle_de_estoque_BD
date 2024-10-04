from AuxiliaryFiles.SGBD import SGBD
from time import sleep
from typing import Optional


class ViewsAPI:
    sgbd: Optional[SGBD] = None

    def __init__(self, sgbd: SGBD) -> None:
        self.sgbd = sgbd

    def monthly_report(self) -> None:
        rows = self.sgbd.read("relatorio_mensal")
        
        if rows == []:
            print("\nNao ha compras cadastradas no momento.\n")
            return

        print(f"\n+{'-' * 124}+")
        sleep(0.1)
        print(f"| {'Relatorio Mensal dos Vendedores':^122} |")
        sleep(0.1)
        print(f"+{'-' * 124}+")
        sleep(0.1)
        print(f"| {'ID':^5} | {'Nome':^20} | {'Mes':^10} | Total de Produtos Vendidos | Total de Dinheiro | Media dos Precos dos Produtos |")
        sleep(0.1)
        print(f"+{'-' * 124}+")
        sleep(0.1)

        for row in rows:
            row_date = row[2].strftime("%Y-%m")
            print(f"| {row[0]:^5} | {row[1]:^20} | {str(row_date):^10} | {row[3]:^26} | {row[4]:^17.2f} | {row[5]:^29.2f} |")
            sleep(0.1)
        print(f"+{'-' * 124}+")
