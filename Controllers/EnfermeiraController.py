# =================================================================
# CONTROLLER: EnfermeiraController
# Responsabilidade: Gerenciar o cadastro e a equipe de enfermagem.
# =================================================================

import sqlite3
from Services.database import conectaBD

def incluirEnfermeira(enfermeira):
    """
    --- BLOCO 1: REGISTRO DE PROFISSIONAL (CREATE) ---
    Insere uma nova enfermeira no banco de dados.
    O COREN (Conselho Regional de Enfermagem) atua como identificador profissional.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    enf_id = None
    try:
        cursor.execute("INSERT INTO enfermeira (nome, coren) VALUES (?, ?)", (enfermeira.get_nome(), enfermeira.get_coren()))
        conexao.commit()
        enf_id = cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Erro ao inserir enfermeira: {e}")
    finally:
        conexao.close()
    return enf_id

def consultarEnfermeiras():
    """
    --- BLOCO 2: LISTAGEM DA EQUIPE (READ) ---
    Retorna a lista completa de profissionais de enfermagem cadastrados.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    dados = []
    try:
        cursor.execute("SELECT * FROM enfermeira")
        rows = cursor.fetchall()
        for row in rows:
            dados.append({"ID": row[0], "Nome": row[1], "COREN": row[2]})
    except sqlite3.Error as e:
        print(f"Erro ao consultar enfermeiras: {e}")
    finally:
        conexao.close()
    return dados

def excluirEnfermeira(id_enf):
    """
    --- BLOCO 3: REMOÇÃO DE REGISTRO (DELETE) ---
    Remove o registro da enfermeira do sistema.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM enfermeira WHERE id = ?", (id_enf,))
        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao excluir enfermeira: {e}")
        return False
    finally:
        conexao.close()
