import sqlite3
from Services.database import conectaBD
from Models.Paciente import Paciente

def incluirPaciente(paciente):
    conexao = conectaBD()
    cursor = conexao.cursor()
    paciente_id = None
    try:
        cursor.execute("""
            INSERT INTO paciente (nome, cpf, prioridade)
            VALUES (?, ?, ?)
        """, (paciente.get_nome(), paciente.get_cpf(), paciente.get_prioridade()))
        conexao.commit()
        paciente_id = cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Erro ao inserir paciente: {e}")
    finally:
        conexao.close()
    return paciente_id

def consultarPacientes():
    conexao = conectaBD()
    cursor = conexao.cursor()
    dados = []
    try:
        cursor.execute("SELECT * FROM paciente")
        rows = cursor.fetchall()
        for row in rows:
            id_p, nome, cpf, prioridade = row
            dados.append({
                "ID": id_p,
                "Nome": nome,
                "CPF": cpf,
                "Prioridade": prioridade
            })
    except sqlite3.Error as e:
        print(f"Erro ao consultar pacientes: {e}")
    finally:
        conexao.close()
    return dados

def buscarPacientePorCPF(cpf):
    conexao = conectaBD()
    cursor = conectaBD().cursor() # Usando conectaBD direto para garantir nova conexão
    paciente = None
    try:
        cursor.execute("SELECT * FROM paciente WHERE cpf = ?", (cpf,))
        row = cursor.fetchone()
        if row:
            paciente = Paciente(row[0], row[1], row[2], row[3])
    except sqlite3.Error as e:
        print(f"Erro ao buscar paciente: {e}")
    finally:
        cursor.close()
    return paciente

def excluirPaciente(id_paciente):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        # Primeiro excluir atendimentos vinculados (Integridade Referencial)
        cursor.execute("DELETE FROM atendimento WHERE paciente_id = ?", (id_paciente,))
        # Depois excluir o paciente
        cursor.execute("DELETE FROM paciente WHERE id = ?", (id_paciente,))
        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao excluir paciente: {e}")
        return False
    finally:
        conexao.close()
