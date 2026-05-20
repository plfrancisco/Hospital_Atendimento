import sqlite3
from Services.database import conectaBD
from Models.Medico import Medico

def incluirMedico(medico):
    conexao = conectaBD()
    cursor = conexao.cursor()
    medico_id = None
    try:
        cursor.execute("""
            INSERT INTO medico (nome, crm, especialidade)
            VALUES (?, ?, ?)
        """, (medico.get_nome(), medico.get_crm(), medico.get_especialidade()))
        conexao.commit()
        medico_id = cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Erro ao inserir medico: {e}")
    finally:
        conexao.close()
    return medico_id

def consultarMedicos():
    conexao = conectaBD()
    cursor = conexao.cursor()
    dados = []
    try:
        cursor.execute("SELECT * FROM medico")
        rows = cursor.fetchall()
        for row in rows:
            dados.append({
                "ID": row[0],
                "Nome": row[1],
                "CRM": row[2],
                "Especialidade": row[3]
            })
    except sqlite3.Error as e:
        print(f"Erro ao consultar medicos: {e}")
    finally:
        conexao.close()
    return dados

def atualizarMedico(medico):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            UPDATE medico 
            SET nome = ?, crm = ?, especialidade = ?
            WHERE id = ?
        """, (medico.get_nome(), medico.get_crm(), medico.get_especialidade(), medico.get_id()))
        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao atualizar medico: {e}")
        return False
    finally:
        conexao.close()

def excluirMedico(id_medico):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM medico WHERE id = ?", (id_medico,))
        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao excluir medico: {e}")
        return False
    finally:
        conexao.close()
