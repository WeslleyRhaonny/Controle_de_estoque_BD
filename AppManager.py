from Screens.StartMenu import StartMenu
from Screens.StockView import StockView 
from Screens.LogIn import LogIn 
from Screens.LoggedClient import LoggedClient 
from Screens.LoggedSeller import LoggedSeller

from AuxiliaryFiles.SGBD import SGBD
from AuxiliaryFiles.Validator import Validator
from AuxiliaryFiles.TablesInfo import TablesInfo
from typing import Optional, Dict, Union


class AppManager:
    sgbd: Optional[SGBD] = None
    vd: Optional[Validator] = None
    ti: Optional[TablesInfo] = None
    valid: bool = False
    screens: Dict[str, Union[StartMenu, StockView, LogIn, LoggedClient, LoggedSeller]]

    def __init__(self) -> None:
        cadastro_lucas = ["postgres", "postgres", "admin", "localhost", "5432"]
        cadastro_eliane = ["postgres", "postgres", "admin@123", "localhost", "5432"]
        cadastro_wesley = ["", "", "", "", ""]
        self.sgbd = SGBD(*cadastro_lucas)
        self.vd = Validator()
        self.ti = TablesInfo()

    def create_tables(self) -> None:
        if not self.valid:
            return

        for table_name, table_columns in self.ti.TABLES_DEFINITIONS.items():
            if not self.sgbd.table_exists(table_name):
                self.sgbd.create_table(table_name, table_columns)

    def start(self) -> None:
        if self.valid:
            return

        self.valid = True
        self.sgbd.connect()
        self.create_tables()

        self.screens = dict()
        self.screens["start_menu"] = StartMenu(self.vd)
        self.screens["stock_view"] = StockView(self.sgbd, self.vd)
        self.screens["login"] = LogIn(self.sgbd, self.vd)
        self.screens["logged_client"] = LoggedClient(self.sgbd, self.vd)
        self.screens["logged_seller"] = LoggedSeller(self.sgbd, self.vd)

    def main(self) -> None:
        next_screen = self.screens["start_menu"].main()

        while True:
            if next_screen == 0:
                return
            elif next_screen == 1:
                next_screen, user_id = self.screens["login"].main()
                break
            elif next_screen == 2:
                next_screen = self.screens["stock_view"].main()

        if next_screen == 0:
            return
        elif next_screen == 1:
            next_screen = next_screen = self.screens["logged_client"].main(user_id)
        elif next_screen == 2:
            next_screen = next_screen = self.screens["logged_seller"].main(user_id)

    def end(self) -> None:
        if self.valid:
            self.sgbd.close()
            self.valid = False