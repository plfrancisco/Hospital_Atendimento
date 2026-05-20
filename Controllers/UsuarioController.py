import sqlite3
from Services.database import conectaBD
from Models.Usuario import Usuario

def autenticar_usuario(login, senha):
    """
    Verifica as credenciais e retorna o Objeto Usuario se bem-sucedido.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM usuario WHERE login = ? AND senha = ?", (login, senha))
        row = cursor.fetchone()
        if row:
            return Usuario(row[0], row[1], row[2], row[3])
        return None
    except sqlite3.Error as e:
        print(f"Erro de Segurança: {e}")
        return None
    finally:
        conexao.close()
