import sqlite3

"""
Módulo de Conexão com o Banco de Dados.
Este serviço é responsável por estabelecer a comunicação com o banco de dados SQLite.
"""

def conectaBD():
    """
    Estabelece uma conexão com o banco de dados local 'Hospital.db'.
    
    Retorna:
        sqlite3.Connection: Objeto de conexão com o banco de dados.
    """
    # Cria a conexão com o banco de dados Hospital.db
    # O arquivo será criado automaticamente se não existir
    conexao = sqlite3.connect("Hospital.db")
    return conexao
