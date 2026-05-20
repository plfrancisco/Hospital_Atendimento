# =================================================================
# CONTROLLER: PacienteController
# Responsabilidade: Lógica de Negócio e Persistência da entidade Paciente.
# =================================================================

import sqlite3
from Services.database import conectaBD
from Models.Paciente import Paciente

def incluirPaciente(paciente):
    """
    --- BLOCO 1: INSERÇÃO (CREATE) ---
    Recebe um objeto Paciente e persiste seus dados no SQLite.
    Retorna o ID gerado pelo banco para ser usado em outras tabelas.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    paciente_id = None
    try:
        cursor.execute("""
            INSERT INTO paciente (nome, cpf, prioridade)
            VALUES (?, ?, ?)
        """, (paciente.get_nome(), paciente.get_cpf(), paciente.get_prioridade()))
        conexao.commit()
        paciente_id = cursor.lastrowid # Captura o ID auto-incremental gerado
    except sqlite3.Error as e:
        print(f"Erro ao inserir paciente: {e}")
    finally:
        conexao.close()
    return paciente_id

def consultarPacientes():
    """
    --- BLOCO 2: CONSULTA GERAL (READ) ---
    Retorna uma lista de dicionários com todos os pacientes.
    Utiliza um LEFT JOIN com a tabela de atendimento para mostrar a última chegada.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    dados = []
    try:
        # Busca dados do paciente e sua data de chegada (primeiro atendimento registrado)
        query = """
            SELECT p.id, p.nome, p.cpf, p.prioridade, a.data_chegada
            FROM paciente p
            LEFT JOIN atendimento a ON p.id = a.paciente_id
            GROUP BY p.id
            ORDER BY a.data_chegada DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            id_p, nome, cpf, prioridade, data_chegada = row
            dados.append({
                "ID": id_p,
                "Nome": nome,
                "CPF": cpf,
                "Prioridade": prioridade,
                "Chegada": data_chegada if data_chegada else "Não registrada"
            })
    except sqlite3.Error as e:
        print(f"Erro ao consultar pacientes: {e}")
    finally:
        conexao.close()
    return dados

def buscarPacientePorCPF(cpf):
    """
    --- BLOCO 3: BUSCA ESPECÍFICA ---
    Localiza um paciente pelo CPF para evitar cadastros duplicados
    ou para resgatar dados na recepção.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    paciente = None
    try:
        cursor.execute("SELECT * FROM paciente WHERE cpf = ?", (cpf,))
        row = cursor.fetchone()
        if row:
            # Reconstrói o objeto Paciente (Model) a partir dos dados do banco
            paciente = Paciente(row[0], row[1], row[2], row[3])
    except sqlite3.Error as e:
        print(f"Erro ao buscar paciente: {e}")
    finally:
        conexao.close()
    return paciente

def excluirPaciente(id_paciente):
    """
    --- BLOCO 4: EXCLUSÃO (DELETE) ---
    Remove o paciente do banco. Por segurança e integridade, 
    remove primeiro seus atendimentos vinculados.
    """
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

def atualizarPaciente(paciente):
    """
    --- BLOCO 5: ATUALIZAÇÃO (UPDATE) ---
    Atualiza os dados de um paciente existente no banco de dados.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            UPDATE paciente 
            SET nome = ?, cpf = ?, prioridade = ?
            WHERE id = ?
        """, (paciente.get_nome(), paciente.get_cpf(), paciente.get_prioridade(), paciente.get_id()))
        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao atualizar paciente: {e}")
        return False
    finally:
        conexao.close()
