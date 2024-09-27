from time import sleep
from datetime import datetime, timedelta

from AuxiliaryFiles.TablesClasses import Product, Client, Seller, Purchase, Possess

class Menu:
    def main_loop(self) -> None:
        while True:
            self.print_header()
            opt: int = self.vd.validate_int(
                "Escolha uma opcao: ",
                "\nPor favor, selecione uma opcao valida, entre 1 e 8.\n",
                lambda x: 1 <= x <= 8,
            )
            if opt == 1:
                self.insert_product()
            elif opt == 2:
                self.modify_product()
            elif opt == 3:
                self.search_product_by_name()
            elif opt == 4:
                self.remove_product()
            elif opt == 5:
                self.list_all_products()
            elif opt == 6:
                self.display_product()
            elif opt == 7:
                self.stock_report()
            elif opt == 8:
                break
            sleep(3)
        self.stock_report()
        self.end()

    def insert_product(self) -> None:
        product = Product()
        self.sgbd.insert("produto", product.columns, product.values)
        print("\nProduto inserido com sucesso.")

    def modify_product(self) -> None:
        # Solicitar ao usuário o ID do produto que deseja modificar
        prod_id = self.vd.validate_int(
            "\nInsira o ID do produto: ",
            "Por favor, insira um ID valido.",
            lambda x: x > 0,
        )
        
        # Buscar o produto pelo ID na tabela 'produtos'
        product_data = self.sgbd.read("produto", "*", f"prod_id = {prod_id}")
        if not product_data:
            print("O produto informado nao esta registrado.")
            return

        product_data = [str(x) for x in product_data[0]]
        product = Product(product_data)

        wasAlterated = False
        while True:
            print("\nEscolha uma informação para alterar:")
            print("1. Nome")
            print("2. Preco")
            print("3. Quantidade")
            print("4. Data de validade")
            print("5. Data de fabricacao")
            print("6. Descricao")
            print("7. Categoria")
            print("8. Produzido em Mari")
            print("9. Finalizar alteracoes")
            opt: int = self.vd.validate_int(
                "Escolha uma opcao: ",
                "Por favor, selecione uma opcao valida, entre 1 e 9.\n",
                lambda x: 1 <= x <= 9,
            )

            if opt == 1:
                product.change_name(self.vd)
                wasAlterated = True
            elif opt == 2:
                product.change_price(self.vd)
                wasAlterated = True
            elif opt == 3:
                product.change_quantity(self.vd)
                wasAlterated = True
            elif opt == 4:
                product.change_exp_date(self.vd)
                wasAlterated = True
            elif opt == 5:
                product.change_fab_date(self.vd)
                wasAlterated = True
            elif opt == 6:
                product.change_description(self.vd)
                wasAlterated = True
            elif opt == 7:
                product.change_category(self.vd)
                wasAlterated = True
            elif opt == 8:
                product.change_mari(self.vd)
                wasAlterated = True
            elif opt == 9:
                break


        if wasAlterated:
            self.sgbd.update("produtos", dict(zip(product.columns, product.values)), f"prod_id = {prod_id}")
            print("Produto alterado com sucesso.")
        else:
            print("Nenhuma alteracao foi realizada.")

    def remove_product(self) -> None:
        # Solicitar ao usuário o ID do produto que deseja remover
        prod_id = self.vd.validate_int(
            "Insira o ID do produto: ",
            "Por favor, insira um ID valido.\n",
            lambda x: x > 0,
        )

        # Tenta realizar a remoção do item escolhido
        rows_deleted = self.sgbd.delete("produto", f"prod_id = {prod_id}")
        if rows_deleted:
            print("Produto removido com sucesso.")
        else:
            print("O produto informado nao esta registrado.")

    def display_product(self) -> None:
        # Solicitar ao usuário o ID do produto que deseja visualizar
        prod_id = self.vd.validate_int(
            "Insira o ID do produto: ",
            "Por favor, insira um ID valido.\n",
            lambda x: x > 0,
        )
        # Buscar o produto pelo ID na tabela 'produtos'
        product = self.sgbd.read("produto", "*", f"prod_id = {prod_id}")

        if not product:
            print(f"O produto com o ID {prod_id} nao esta registrado.\n")
        else:
            print("\nInformacoes do produto:")
            print(f"ID: {product[0][0]}")
            print(f"Nome: {product[0][1]}")
            print(f"Preco: R${product[0][2]:.2f}")
            print(f"Quantidade: {product[0][3]}")
            print(f"Data de validade: {product[0][4]}")
            print(f"Data de fabricacao: {product[0][5]}")
            print(f"Descricao: {product[0][6]}")
            print("\n")    

    def stock_report(self) -> None:
        print(f"\n+{'-'*30}+")
        print(f"{'Relatorio de Estoque':^32}")
        print(f"+{'-'*30}+")

        print(f"\nNumero de produtos registrados: {self.sgbd.count_rows('produto')}")

        out_of_stock_products = "\n".join([", ".join([str(y) for y in x]) for x in self.sgbd.read("produto", ("prod_id", "nome",), "quantidade = 0")])
        if out_of_stock_products != "":
            print(f"Produtos faltando no estoque: {out_of_stock_products}")
        else:
            print("Nao ha produtos faltando no estoque.")

        today_date = datetime.now().strftime('%Y-%m-%d')
        expired_products = "\n".join([", ".join([str(y) for y in x]) for x in self.sgbd.read("produto", ("prod_id", "nome",), f"data_validade < '{today_date}'")])
        if expired_products != "":
            print(f"Produtos estragados no estoque: {expired_products}")
        else:
            print("Nao ha produtos estragados no estoque.")

        expiration_date = (datetime.now() + timedelta(10)).strftime('%Y-%m-%d') 
        close_to_expiration_products = "\n".join([", ".join([str(y) for y in x]) for x in self.sgbd.read("produto", ("prod_id", "nome",), f"data_validade > '{today_date}' AND data_validade < '{expiration_date}'")])
        if close_to_expiration_products != "":
            print(f"Produtos próximos da data de validade: {close_to_expiration_products}")
        else:
            print("Nao ha produtos proximos da data de validade.")

