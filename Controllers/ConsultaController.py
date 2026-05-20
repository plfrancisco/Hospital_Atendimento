import sqlite3
from Services.database import conectaBD

def agendarConsulta(consulta):
    conexao = conectaBD()
    cursor = conexao.cursor()
    consulta_id = None
    try:
        cursor.execute("""
            INSERT INTO consulta (paciente_id, medico_id, data_hora, status, observacoes)
            VALUES (?, ?, ?, ?, ?)
        """, (consulta.get_paciente_id(), consulta.get_medico_id(), consulta.get_data_hora(), consulta.get_status(), consulta.get_observacoes()))
        conexao.commit()
        consulta_id = cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Erro ao agendar consulta: {e}")
    finally:
        conexao.close()
    return consulta_id

def consultarConsultas():
    conexao = conectaBD()
    cursor = conexao.cursor()
    dados = []
    try:
        query = """
            SELECT c.id, p.nome, m.nome, c.data_hora, c.status, c.observacoes
            FROM consulta c
            JOIN paciente p ON c.paciente_id = p.id
            JOIN medico m ON c.medico_id = m.id
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            dados.append({
                "ID": row[0],
                "Paciente": row[1],
                "Medico": row[2],
                "Data/Hora": row[3],
                "Status": row[4],
                "Observacoes": row[5]
            })
    except sqlite3.Error as e:
        print(f"Erro ao consultar consultas: {e}")
    finally:
        conexao.close()
    return dados

def atualizarConsulta(consulta):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            UPDATE consulta 
            SET data_hora = ?, status = ?, observacoes = ?
            WHERE id = ?
        """, (consulta.get_data_hora(), consulta.get_status(), consulta.get_observacoes(), consulta.get_id()))
        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao atualizar consulta: {e}")
        return False
    finally:
        conexao.close()

def cancelarConsulta(id_consulta):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM consulta WHERE id = ?", (id_consulta,))
        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao cancelar consulta: {e}")
        return False
    finally:
        conexao.close()
