import sys
import os

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox

# Importações dos módulos das outras pastas
# Certifique-se de que o caminho relativo esteja correto a partir do `FrontEnd.py`
try:
    # Tente importar o módulo `SGBD` a partir da pasta `AuxiliaryFiles`
    from AuxiliaryFiles.SGBD import SGBD
except ModuleNotFoundError:
    # Se falhar, exibe uma mensagem de erro
    print("Erro ao importar SGBD. Verifique o caminho do módulo e a estrutura do projeto.")

# Importações das telas, removendo duplicatas e caminhos incorretos
from LogIn import *  # Importe funções específicas se necessário
from StartMenu import *  # Importe funções específicas se necessário
from StockView import *  # Importe funções específicas se necessário
from LoggedClient import *  # Importe funções específicas se necessário
from LoggedSeller import *  # Importe funções específicas se necessário

# Função para Tela de Login
def login_screen():
    login = tk.Tk()
    login.title("Login")
    login.geometry("400x300")
    
    tk.Label(login, text="Login", font=("Arial", 18)).pack(pady=20)
    
    tk.Label(login, text="Usuário:").pack()
    username_entry = tk.Entry(login)
    username_entry.pack()
    
    tk.Label(login, text="Senha:").pack()
    password_entry = tk.Entry(login, show="*")
    password_entry.pack()
    
    def verify_login():
        username = username_entry.get()
        password = password_entry.get()
        # Aqui você pode adicionar lógica de verificação com o backend
        if username == "admin" and password == "admin":  # Substitua pela lógica do seu backend
            login.destroy()
            start_menu_screen()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")
    
    tk.Button(login, text="Entrar", command=verify_login).pack(pady=20)
    
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

# Função para Tela de Vendedor Logado
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

# Executar a tela de login inicialmente
if __name__ == "__main__":
    start_menu_screen()
#    login_screen()