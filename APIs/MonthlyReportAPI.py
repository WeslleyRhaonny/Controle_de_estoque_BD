from AuxiliaryFiles.SGBD import SGBD
from time import sleep
from typing import Optional


class MonthlyReportAPI:
    sgbd: Optional[SGBD] = None

    def __init__(self, sgbd: SGBD) -> None:
        self.sgbd = sgbd

    def monthly_report(self) -> None:
        rows = self.sgbd.read("relatorio_mensal")
            
        print(f"\n+{'-' * 60}+")
        sleep(0.1)
        print(f"| {'Relatorio Mensal dos Vendedores':^58} |")
        sleep(0.1)
        print(f"+{'-' * 60}+")
        sleep(0.1)
        print(f"| {'ID':^5} | {'Nome':^20} | {'Mes':^10} | Total de Produtos Vendidos | Total de Dinheiro | Media dos Precos dos Produtos |")
        sleep(0.1)
        print(f"+{'-' * 60}+")
        sleep(0.1)

        for row in rows:
            print(f"| {row[0]:^5} | {row[1]:^20} | {row[2]:^10} | {row[3]:^10} | {row[4]:^10.2f} | {row[5]:^10.2f} |")
            sleep(0.1)
        print(f"+{'-' * 119}+")
