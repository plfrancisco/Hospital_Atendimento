import sqlite3
from Services.database import conectaBD
from datetime import datetime

def registrarInternacao(internacao):
    conexao = conectaBD()
    cursor = conexao.cursor()
    internacao_id = None
    try:
        cursor.execute("""
            INSERT INTO internacao (paciente_id, leito_id, data_entrada, motivo)
            VALUES (?, ?, ?, ?)
        """, (internacao.get_paciente_id(), internacao.get_leito_id(), internacao.get_data_entrada(), internacao.get_motivo()))
        
        # Atualiza status do leito para 'Ocupado'
        cursor.execute("UPDATE leito SET status = 'Ocupado' WHERE id = ?", (internacao.get_leito_id(),))
        
        conexao.commit()
        internacao_id = cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Erro ao registrar internacao: {e}")
    finally:
        conexao.close()
    return internacao_id

def consultarInternacoes():
    conexao = conectaBD()
    cursor = conexao.cursor()
    dados = []
    try:
        query = """
            SELECT i.id, p.nome, l.numero, i.data_entrada, i.data_saida, i.motivo
            FROM internacao i
            JOIN paciente p ON i.paciente_id = p.id
            JOIN leito l ON i.leito_id = l.id
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            dados.append({
                "ID": row[0],
                "Paciente": row[1],
                "Leito": row[2],
                "Entrada": row[3],
                "Saida": row[4],
                "Motivo": row[5]
            })
    except sqlite3.Error as e:
        print(f"Erro ao consultar internacoes: {e}")
    finally:
        conexao.close()
    return dados

def registrarAlta(id_internacao, id_leito):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        data_saida = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            UPDATE internacao 
            SET data_saida = ?
            WHERE id = ?
        """, (data_saida, id_internacao))
        
        # Atualiza status do leito para 'Livre'
        cursor.execute("UPDATE leito SET status = 'Livre' WHERE id = ?", (id_leito,))
        
        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao registrar alta: {e}")
        return False
    finally:
        conexao.close()
