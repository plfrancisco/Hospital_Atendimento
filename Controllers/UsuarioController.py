# =================================================================
# CONTROLLER: UsuarioController
# Responsabilidade: Autenticação e Segurança de Acesso.
# =================================================================

import sqlite3
from Services.database import conectaBD
from Models.Usuario import Usuario

def autenticar_usuario(login, senha):
    """
    --- BLOCO 1: GATEKEEPER DE SEGURANÇA ---
    Verifica as credenciais fornecidas na tela de login contra a tabela 'usuario'.
    Retorna um objeto Usuario se o acesso for autorizado, caso contrário, retorna None.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        # Busca exata por login e senha (Em sistemas reais, usar Hash de Senha)
        cursor.execute("SELECT * FROM usuario WHERE login = ? AND senha = ?", (login, senha))
        row = cursor.fetchone()
        
        if row:
            # Reconstrói o objeto de sessão do usuário (Model)
            return Usuario(row[0], row[1], row[2], row[3])
        return None
    except sqlite3.Error as e:
        print(f"Erro de Segurança: {e}")
        return None
    finally:
        conexao.close()
