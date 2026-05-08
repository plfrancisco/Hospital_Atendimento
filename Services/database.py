import sqlite3

def conectaBD():
    # Cria a conexão com o banco de dados Hospital.db
    # O arquivo será criado automaticamente se não existir
    conexao = sqlite3.connect("Hospital.db")
    return conexao
