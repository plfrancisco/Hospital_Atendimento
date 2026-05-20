# =================================================================
# CONTROLLER: DiarioController
# Responsabilidade: Gerenciar os registros de evolução dos pacientes internados.
# =================================================================

import sqlite3
from datetime import datetime
from Services.database import conectaBD

def registrarObservacao(internacao_id, enfermeira_id, observacao):
    """
    --- BLOCO 1: REGISTRO DE EVOLUÇÃO (CREATE) ---
    Salva uma nova nota no diário de enfermagem vinculada a uma internação ativa.
    Registra automaticamente o timestamp do momento da observação.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        data_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO diario_enfermagem (internacao_id, enfermeira_id, observacao, data_registro)
            VALUES (?, ?, ?, ?)
        """, (internacao_id, enfermeira_id, observacao, data_registro))
        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao registrar observação: {e}")
        return False
    finally:
        conexao.close()

def consultarDiario(internacao_id):
    """
    --- BLOCO 2: HISTÓRICO DE EVOLUÇÃO (READ) ---
    Recupera todas as notas de enfermagem de um paciente específico (via internacao_id).
    Ordena do registro mais recente para o mais antigo para facilitar a leitura clínica.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    dados = []
    try:
        cursor.execute("""
            SELECT d.id, e.nome, d.observacao, d.data_registro
            FROM diario_enfermagem d
            JOIN enfermeira e ON d.enfermeira_id = e.id
            WHERE d.internacao_id = ?
            ORDER BY d.data_registro DESC
        """, (internacao_id,))
        rows = cursor.fetchall()
        for row in rows:
            dados.append({
                "ID": row[0],
                "Enfermeira": row[1],
                "Observacao": row[2],
                "Data": row[3]
            })
    except sqlite3.Error as e:
        print(f"Erro ao consultar diário: {e}")
    finally:
        conexao.close()
    return dados
