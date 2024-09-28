from AuxiliaryFiles.Validator import Validator
from typing import Optional


class StartMenu:
    vd: Optional[Validator] = None

    def __init__(self, vd: Validator) -> None:
        self.vd = vd

    def main(self) -> int:
        print("\n" + "=" * 60)
        print(f'{"Menu Inicial":^60}')
        print("=" * 60)
        print("\nBem vindo! Por favor, selecione uma opcao:")
        print("1. Login / Cadastro")
        print("2. Visualizar estoque (Como visitante)")
        print("0. Sair")
        opt: int = self.vd.validate_int(
            "Escolha uma opcao: ",
            "\nPor favor, selecione uma opcao valida, entre 0 e 2.\n",
            lambda x: 0 <= x <= 2
        )

        return opt
