import sys
import os

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox

# Importações das telas, removendo duplicatas e caminhos incorretos
from LogIn import *  # Importe funções específicas se necessário
from StartMenu import *  # Importe funções específicas se necessário
from StockView import *  # Importe funções específicas se necessário
from LoggedClient import *  # Importe funções específicas se necessário
from LoggedSeller import *  # Importe funções específicas se necessário

from AuxiliaryFiles.SGBD import SGBD
from AuxiliaryFiles.Validator import Validator
from AppManager import AppManager
from APIs.ClientAPI import ClientAPI
# Criação de instâncias necessárias para o ClientAPI funcionar
app_manager = AppManager()
app_manager.start()
sgbd = app_manager.sgbd
vd = app_manager.vd
client_api = ClientAPI(sgbd, vd)
seller_api = SellerAPI(sgbd, vd)

# Função para Tela de Login
def login_screen():
    login = tk.Tk()
    login.title("Login")
    login.geometry("400x300")

    tk.Label(login, text="Login", font=("Arial", 18)).pack(pady=20)

    tk.Label(login, text="Usuário (ID):").pack()
    username_entry = tk.Entry(login)
    username_entry.pack()

    tk.Label(login, text="Senha:").pack()
    password_entry = tk.Entry(login, show="*")
    password_entry.pack()

    def submit_login():
        user_id = username_entry.get()
        password = password_entry.get()

        try:
            user_id = int(user_id)  # Convertendo o ID para inteiro
        except ValueError:
            messagebox.showerror("Erro", "ID do cliente deve ser um número.")
            return

        # Tentativa de login via client_api
        try:
            # Chamando a API de login com o ID e senha do cliente
            result, client_id = client_api.login(user_id, password)

            # Se o login for bem-sucedido
            if result:
                login.destroy()  # Fecha a tela de login
                messagebox.showinfo("Sucesso", f"Login realizado com sucesso! ID: {client_id}")
                view_client(client_id)  # Abre o menu principal
            else:
                messagebox.showerror("Erro", "Usuário ou senha inválidos!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao tentar login: {str(e)}")
    tk.Button(login, text="Entrar", command=submit_login).pack(pady=20)

    login.mainloop()

def login_seller_screen():
    login = tk.Tk()
    login.title("Login")
    login.geometry("400x300")

    tk.Label(login, text="Login", font=("Arial", 18)).pack(pady=20)

    tk.Label(login, text="Usuário (ID):").pack()
    username_entry = tk.Entry(login)
    username_entry.pack()

    tk.Label(login, text="Senha:").pack()
    password_entry = tk.Entry(login, show="*")
    password_entry.pack()

    def submit_login():
        user_id = username_entry.get()
        password = password_entry.get()

        try:
            user_id = int(user_id)  # Convertendo o ID para inteiro
        except ValueError:
            messagebox.showerror("Erro", "ID do vendedor deve ser um número.")
            return

        # Tentativa de login via client_api
        try:
            # Chamando a API de login com o ID e senha do cliente
            result, seller_id = seller_api.login(user_id, password)

            # Se o login for bem-sucedido
            if result:
                login.destroy()  # Fecha a tela de login
                messagebox.showinfo("Sucesso", f"Login realizado com sucesso! ID: {seller_id}")
                view_seller()  # Abre o menu principal
            else:
                messagebox.showerror("Erro", "Usuário ou senha inválidos!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao tentar login: {str(e)}")
    tk.Button(login, text="Entrar", command=submit_login).pack(pady=20)

    login.mainloop()
import tkinter as tk
from tkinter import messagebox

def register_seller_screen():
    register_window = tk.Tk()
    register_window.title("Cadastro Vendedor")
    register_window.geometry("400x400")

    tk.Label(register_window, text="Cadastro Vendedor", font=("Arial", 18)).pack(pady=20)

    # Entrada para o nome de usuário
    tk.Label(register_window, text="Nome de Usuário:").pack()
    username_entry = tk.Entry(register_window)
    username_entry.pack()

    # Entrada para a senha
    tk.Label(register_window, text="Senha:").pack()
    password_entry = tk.Entry(register_window, show="*")
    password_entry.pack()

    # Entrada para o token de autenticação
    tk.Label(register_window, text="Token de Autenticação:").pack()
    token_entry = tk.Entry(register_window, show = "*")
    token_entry.pack()

    def submit_registration():
        username = username_entry.get()
        password = password_entry.get()
        token = token_entry.get()

        # Validações de entrada
        if not username or not password or not token:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        if token != "123":
            messagebox.showerror("Erro", "Token de autenticação incorreto.")
            return

        # Criar um novo vendedor (adapte de acordo com sua estrutura de Seller)
        new_seller = {
            "nome_usuario": username,
            "senha": password,
            "token": token,
        }

        try:
            # Registrar o novo vendedor usando a API
            result, seller_id = seller_api.register(new_seller)
            if result:
                messagebox.showinfo("Sucesso", f"Cadastro realizado com sucesso! ID: {seller_id}")
                register_window.destroy()  # Fecha a tela de cadastro
            else:
                messagebox.showerror("Erro", "Erro ao realizar o cadastro.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao tentar cadastrar: {str(e)}")

    tk.Button(register_window, text="Cadastrar", command=submit_registration).pack(pady=20)

    register_window.mainloop()

# Função para Tela de Cadastro
def register_screen():
    register_window = tk.Tk()
    register_window.title("Cadastro")
    register_window.geometry("400x400")

    tk.Label(register_window, text="Cadastro", font=("Arial", 18)).pack(pady=20)

    # Entrada para o nome
    tk.Label(register_window, text="Nome:").pack()
    name_entry = tk.Entry(register_window)
    name_entry.pack()

    # Entrada para a senha
    tk.Label(register_window, text="Senha:").pack()
    password_entry = tk.Entry(register_window, show="*")
    password_entry.pack()

    # Checkboxes para preferências
    flamengo_var = tk.IntVar()
    onepiece_var = tk.IntVar()
    sousa_var = tk.IntVar()

    tk.Checkbutton(register_window, text="Torce pro Flamengo", variable=flamengo_var).pack()
    tk.Checkbutton(register_window, text="Assiste One Piece", variable=onepiece_var).pack()
    tk.Checkbutton(register_window, text="Mora em Sousa", variable=sousa_var).pack()

    def submit_registration():
        name = name_entry.get()
        password = password_entry.get()

        # Validações de entrada
        if not name or not password:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        # Criar um dicionário com os dados do novo cliente
        new_client = {
            "nome": name,
            "senha": password,
            "torce_flamengo": flamengo_var.get(),
            "assiste_onepiece": onepiece_var.get(),
            "mora_sousa": sousa_var.get(),
        }

        try:
            # Registrar o novo cliente usando a API
            result, client_id = client_api.register(new_client)
            if result:
                messagebox.showinfo("Sucesso", f"Cadastro realizado com sucesso! ID: {client_id}")
                register_window.destroy()  # Fecha a tela de cadastro
            else:
                messagebox.showerror("Erro", "Erro ao realizar o cadastro.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao tentar cadastrar: {str(e)}")


    tk.Button(register_window, text="Cadastrar", command=submit_registration).pack(pady=20)

    register_window.mainloop()


# Função para Tela de Menu Inicial
def start_menu_screen():
    menu = tk.Tk()
    menu.title("Menu Inicial")
    menu.geometry("400x300")
    tk.Label(menu, text="Bem-vindo!", font=("Arial", 18)).pack(pady=20)
    
    tk.Label(menu, text="Menu Inicial", font=("Arial", 18)).pack(pady=20)

    tk.Button(menu, text="Login / Cadastro (Cliente)", command=login_cadastro_client_screen).pack(pady=10)
    tk.Button(menu, text="Login / Cadastro (Vendedor)", command=login_cadastro_seller_screen).pack(pady=10)
    tk.Button(menu, text="Visualizar estoque (Como visitante)", command=view_stock).pack(pady=10)
    
    menu.mainloop()

# Função para Tela de Cliente Logado
def login_cadastro_client_screen():
    client_window = tk.Tk()
    client_window.title("Log In / Cadastro")
    client_window.geometry("400x300")
    
    tk.Label(client_window, text="Bem-vindo!", font=("Arial", 18)).pack(pady=20)
    tk.Button(client_window, text="Log In", command=login_screen).pack(pady=10)
    tk.Button(client_window, text=" Cadastrar-se", command=register_screen).pack(pady=10)
    
    # Adicione elementos específicos para a tela do cliente aqui
    
    tk.Button(client_window, text="Voltar ao Menu Inicial", command=client_window.destroy).pack(pady=10)
    
    client_window.mainloop()

def login_cadastro_seller_screen():
    client_window = tk.Tk()
    client_window.title("Log In / Cadastro")
    client_window.geometry("400x300")
    
    tk.Label(client_window, text="Bem-vindo!", font=("Arial", 18)).pack(pady=20)
    tk.Button(client_window, text="Log In", command=login_seller_screen).pack(pady=10)
    tk.Button(client_window, text=" Cadastrar-se", command=register_seller_screen).pack(pady=10)
    
    # Adicione elementos específicos para a tela do cliente aqui
    
    tk.Button(client_window, text="Voltar ao Menu Inicial", command=client_window.destroy).pack(pady=10)
    
    client_window.mainloop()

def view_stock():
    seller_window = tk.Tk()
    seller_window.title("Visualizar Estoque (Como Visitante)")
    seller_window.geometry("400x300")
    
    tk.Label(seller_window, text="Bem-vindo!", font=("Arial", 18)).pack(pady=20)
    tk.Button(seller_window, text="Procurar um produto", command=view_stock).pack(pady=10)
    tk.Button(seller_window, text="Listar todos os produtos", command=view_stock).pack(pady=10)
    # Adicione elementos específicos para a tela do vendedor aqui
    
    tk.Button(seller_window, text="Voltar", command=seller_window.destroy).pack(pady=10)

    seller_window.mainloop()

# Função para Tela de Visualização de Estoque
def stock_view_screen():
    stock_window = tk.Tk()
    stock_window.title("Visualização de Estoque")
    stock_window.geometry("400x300")
    
    tk.Label(stock_window, text="Estoque", font=("Arial", 18)).pack(pady=20)
    
    # Adicione elementos específicos para a visualização do estoque aqui
    
    tk.Button(stock_window, text="Voltar", command=stock_window.destroy).pack(pady=20)
    
    stock_window.mainloop()

def view_client(client_id):
    logged_client = tk.Tk()
    logged_client.title("Tela do Cliente")
    logged_client.geometry("400x600")
    
    tk.Label(logged_client, text="Tela do Cliente", font=("Arial", 18)).pack(pady=20)
    tk.Button(logged_client, text="Verificar seus dados", command=lambda: view_client_data(client_id)).pack(pady=10)
    tk.Button(logged_client, text="Verificar compras passadas", command=view_stock).pack(pady=10)
    tk.Button(logged_client, text="Adicionar produtos ao carrinho", command=view_stock).pack(pady=10)
    tk.Button(logged_client, text="Remover produtos do carrinho", command=view_stock).pack(pady=10)
    tk.Button(logged_client, text="Realizar compra", command=view_stock).pack(pady=10)
    tk.Button(logged_client, text="Procurar um produto", command=view_stock).pack(pady=10)
    tk.Button(logged_client, text="Listar todos os produtos", command=view_stock).pack(pady=10)

    
    tk.Button(logged_client, text="Voltar", command=logged_client.destroy).pack(pady=10)

    logged_client.mainloop()

def view_seller():
    logged_seller = tk.Tk()
    logged_seller.title("Tela do Vendedor")
    logged_seller.geometry("400x600")
    
    tk.Label(logged_seller, text="Tela do Vendedor", font=("Arial", 18)).pack(pady=20)
    tk.Button(logged_seller, text="Inserir um produto", command=view_stock).pack(pady=10)
    tk.Button(logged_seller, text="Modificar um produto", command=view_stock).pack(pady=10)
    tk.Button(logged_seller, text="Remover um produto", command=view_stock).pack(pady=10)
    tk.Button(logged_seller, text="Procurar um produto", command=view_stock).pack(pady=10)
    tk.Button(logged_seller, text="Listar todos os produtos", command=view_stock).pack(pady=10)
    tk.Button(logged_seller, text="Exibir relatório mensal", command=view_stock).pack(pady=10)
    tk.Button(logged_seller, text="Exibir relatório do estoque", command=view_stock).pack(pady=10)

    
    tk.Button(logged_seller, text="Voltar", command=logged_seller.destroy).pack(pady=10)

    logged_seller.mainloop()

import tkinter.ttk as ttk

def view_client_data(client_id):
    try:
        # Usar a API do cliente para obter os dados do cliente
        client_data = client_api.sgbd.read(
            "cliente", 
            "*", 
            f"cliente_id = {client_id}"
        )[0]

        # Criar uma nova janela para mostrar os dados do cliente
        client_data_window = tk.Toplevel()
        client_data_window.title("Dados do Cliente")
        client_data_window.geometry("800x300")

        # Criar uma Treeview para exibir os dados do cliente
        tree = ttk.Treeview(client_data_window)
        tree["columns"] = ("ID", "Nome", "Senha", "Torce pro Flamengo", "Assiste One Piece", "Mora em Sousa")

        # Definir os cabeçalhos das colunas
        tree.column("#0", width=0, stretch=tk.NO)  # Coluna fantasma para a árvore (não necessária)
        tree.column("ID", anchor=tk.CENTER, width=50)
        tree.column("Nome", anchor=tk.W, width=150)
        tree.column("Senha", anchor=tk.W, width=100)
        tree.column("Torce pro Flamengo", anchor=tk.CENTER, width=150)
        tree.column("Assiste One Piece", anchor=tk.CENTER, width=150)
        tree.column("Mora em Sousa", anchor=tk.CENTER, width=150)

        # Criar os cabeçalhos das colunas
        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("ID", text="ID", anchor=tk.CENTER)
        tree.heading("Nome", text="Nome", anchor=tk.W)
        tree.heading("Senha", text="Senha", anchor=tk.W)
        tree.heading("Torce pro Flamengo", text="Torce pro Flamengo", anchor=tk.CENTER)
        tree.heading("Assiste One Piece", text="Assiste One Piece", anchor=tk.CENTER)
        tree.heading("Mora em Sousa", text="Mora em Sousa", anchor=tk.CENTER)

        # Adicionar os dados do cliente à Treeview
        tree.insert(
            "", 
            tk.END, 
            values=(
                client_data[0], 
                client_data[1], 
                client_data[2], 
                "Sim" if client_data[3] else "Nao", 
                "Sim" if client_data[4] else "Nao", 
                "Sim" if client_data[5] else "Nao"
            )
        )

        tree.pack(pady=20)

        tk.Button(client_data_window, text="Fechar", command=client_data_window.destroy).pack(pady=20)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao tentar visualizar os dados do cliente: {str(e)}")


# Executar a tela de login inicialmente
if __name__ == "__main__":
    start_menu_screen()
#    login_screen()