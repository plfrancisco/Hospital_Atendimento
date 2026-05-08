"""
CONTROLLER DE ATENDIMENTO
Este arquivo contém a 'inteligência' por trás do fluxo de atendimento.
Ele decide como os dados entram e mudam de estado no banco de dados SQLite.
"""

import sqlite3
from datetime import datetime
from Services.database import conectaBD

def registrarChegada(paciente_id):
    """
    BLOCO DE ENTRADA
    Cria um novo registro na tabela 'atendimento' assim que o paciente é cadastrado.
    Define o status inicial como 'Aguardando Triagem' e salva o momento exato da chegada.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        data_chegada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO atendimento (paciente_id, status, data_chegada)
            VALUES (?, ?, ?)
        """, (paciente_id, "Aguardando Triagem", data_chegada))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao registrar chegada: {e}")
    finally:
        conexao.close()

def finalizarTriagem(atendimento_id):
    """
    BLOCO DE TRANSIÇÃO (TRIAGEM -> MÉDICO)
    Atualiza um atendimento existente. Muda o status para 'Aguardando Atendimento'
    e registra o timestamp de quando a triagem foi concluída para fins de auditoria e KPI.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        data_triagem = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            UPDATE atendimento 
            SET status = ?, data_triagem = ?
            WHERE id = ?
        """, ("Aguardando Atendimento", data_triagem, atendimento_id))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao finalizar triagem: {e}")
    finally:
        conexao.close()

def finalizarAtendimento(atendimento_id):
    """
    BLOCO DE FINALIZAÇÃO
    Conclui a jornada do paciente no sistema. O status passa para 'Atendido'
    e o horário da consulta é salvo, permitindo calcular o tempo total de espera.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        data_atendimento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            UPDATE atendimento 
            SET status = ?, data_atendimento = ?
            WHERE id = ?
        """, ("Atendido", data_atendimento, atendimento_id))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao finalizar atendimento: {e}")
    finally:
        conexao.close()

def consultarFila(status_filtro=None):
    """
    BLOCO DE CONSULTA
    Recupera os dados de atendimento do banco, unindo (JOIN) com as informações do paciente.
    Pode retornar a fila completa ou apenas pacientes com um status específico.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    dados = []
    try:
        query = """
            SELECT a.id, p.nome, p.prioridade, a.status, a.data_chegada, a.data_triagem, a.data_atendimento
            FROM atendimento a
            JOIN paciente p ON a.paciente_id = p.id
        """
        if status_filtro:
            query += " WHERE a.status = ?"
            cursor.execute(query, (status_filtro,))
        else:
            cursor.execute(query)
            
        rows = cursor.fetchall()
        for row in rows:
            dados.append({
                "Atendimento_ID": row[0],
                "Paciente": row[1],
                "Prioridade": row[2],
                "Status": row[3],
                "Chegada": row[4],
                "Triagem": row[5],
                "Atendimento": row[6]
            })
    except sqlite3.Error as e:
        print(f"Erro ao consultar fila: {e}")
    finally:
        conexao.close()
    return dados
