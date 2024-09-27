from AuxiliaryFiles.SGBD import SGBD
from AuxiliaryFiles.Validator import Validator
from APIs.ClientAPI import ClientAPI
from APIs.SellerAPI import SellerAPI
from typing import Optional

class LoggedClient:
    sgbd: Optional[SGBD] = None
    vd: Optional[Validator] = None
    client_api: Optional[ClientAPI] = None
    seller_api: Optional[SellerAPI] = None

    def __init__(self, sgbd: SGBD, vd: Validator) -> None:
        self.sgbd = sgbd
        self.vd = vd
        self.client_api = ClientAPI(sgbd, vd)
        self.seller_api = SellerAPI(sgbd, vd)
