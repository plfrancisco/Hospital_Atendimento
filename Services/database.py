# =================================================================
# SERVIÇO: Conector Database
# Responsabilidade: Gerenciar a conexão física com o SQLite
# =================================================================

import sqlite3

def conectaBD():
    """
    Estabelece a conexão com o banco de dados 'Hospital.db'.
    Configura o row_factory para permitir acesso aos dados por nome da coluna.
    """
    try:
        conexao = sqlite3.connect("Hospital.db")
        conexao.row_factory = sqlite3.Row
        return conexao
    except sqlite3.Error as e:
        print(f"--- [DATABASE ERROR] Falha na conexão: {e} ---")
        return None
