from datetime import datetime
from typing import Callable


class Validator:
    def validate_int(self, msg: str, err: str, test: Callable[[int], bool]) -> int:
        while True:
            try:
                aux = input(msg).strip()
                if not aux:
                    raise Exception

                aux = int(aux)

                if test(aux):
                    return aux
                raise Exception
            except Exception:
                print(err)

    def validate_float(self, msg: str, err: str, test: Callable[[float], bool]) -> float:
        while True:
            try:
                aux = input(msg).strip().replace(",", ".")
                if not aux:
                    raise Exception

                aux = float(aux)

                if test(aux):
                    return aux
                raise Exception
            except Exception:
                print(err)

    def validate_str(self, msg: str, err: str, test: Callable[[str], bool]) -> str:
        while True:
            try:
                aux = input(msg).strip()
                if not aux:
                    raise Exception

                if test(aux):
                    return aux
                raise Exception
            except Exception:
                print(err)

    def validate_date(self, msg: str, err: str, test: Callable[[str], bool]) -> datetime:
        while True:
            try:
                aux = input(msg).strip().replace("/", "-")
                if not aux:
                    raise Exception

                if not test(aux):
                    raise Exception

                aux = datetime.strptime(aux, "%Y-%m-%d")
                return aux
            
            except Exception:
                print(err)
