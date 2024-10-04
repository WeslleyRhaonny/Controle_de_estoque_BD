import json
from AuxiliaryFiles.SGBD import SGBD
from typing import Optional


class ProceduresAPI:
    sgbd: Optional[SGBD] = None

    def __init__(self, sgbd: SGBD) -> None:
        self.sgbd = sgbd

    def validate_purchase(self, client_id: int, cart: dict[int, int]) -> tuple[bool, int, float]:
        cart_json = json.dumps(cart)
        return self.sgbd.read(custom_query=f"SELECT * FROM verificar_compra({client_id}, '{cart_json}')")[0]

    def save_purchase(self, client_id: int, seller_id: int, payment_type: str, cart: dict[int, int], total_price: float) -> None:
        cart_json = json.dumps(cart)

        self.sgbd.execute_command(F"SELECT * FROM salvar_compra({client_id}, {seller_id}, '{payment_type}', '{cart_json}', {total_price})")
