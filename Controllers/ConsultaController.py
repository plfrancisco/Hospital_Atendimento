# =================================================================
# CONTROLLER: ConsultaController
# Responsabilidade: Gerenciar o agendamento e histórico de consultas médicas.
# =================================================================

import sqlite3
from Services.database import conectaBD

def agendarConsulta(consulta):
    """
    --- BLOCO 1: AGENDAMENTO (CREATE) ---
    Persiste um novo registro de consulta no banco de dados.
    Vincula um Paciente a um Médico em uma data e hora específica.
    """
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
    """
    --- BLOCO 2: VISUALIZAÇÃO DE AGENDA (READ) ---
    Recupera todas as consultas agendadas, trazendo os nomes do paciente 
    e do médico através de JOINs para facilitar a leitura na View.
    """
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
    """
    --- BLOCO 3: REAGENDAMENTO / ATUALIZAÇÃO (UPDATE) ---
    Permite alterar o horário, o status (ex: Realizada, Cancelada) 
    ou adicionar observações clínicas à consulta.
    """
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
    """
    --- BLOCO 4: CANCELAMENTO (DELETE) ---
    Remove definitivamente o registro da consulta do banco de dados.
    """
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
