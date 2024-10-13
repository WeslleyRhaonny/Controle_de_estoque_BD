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


# Função para Tela de Menu Inicial
def start_menu_screen():
    menu = tk.Tk()
    menu.title("Menu Inicial")
    menu.geometry("400x300")
    tk.Label(menu, text="Bem-vindo!", font=("Arial", 18)).pack(pady=20)
    
    tk.Label(menu, text="Menu Inicial", font=("Arial", 18)).pack(pady=20)

    tk.Button(menu, text="Login / Cadastro", command=login_cadastro_client_screen).pack(pady=10)
    tk.Button(menu, text="Visualizar estoque (Como visitante)", command=view_stock).pack(pady=10)
    
    menu.mainloop()

# Função para Tela de Cliente Logado
def login_cadastro_client_screen():
    client_window = tk.Tk()
    client_window.title("Log In / Cadastro")
    client_window.geometry("400x300")
    
    tk.Label(client_window, text="Bem-vindo!", font=("Arial", 18)).pack(pady=20)
    tk.Button(client_window, text="Log In", command=login_screen).pack(pady=10)
    tk.Button(client_window, text=" Cadastrar-se", command=login_cadastro_client_screen).pack(pady=10)
    
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