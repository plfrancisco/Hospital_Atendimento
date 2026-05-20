import sqlite3
from Services.database import conectaBD

def incluirEnfermeira(enfermeira):
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
