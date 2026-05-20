# =================================================================
# CONTROLLER: LeitoController
# Responsabilidade: Gerenciar a infraestrutura física (Leitos) do hospital.
# =================================================================

import sqlite3
from Services.database import conectaBD
from Models.Leito import Leito

def incluirLeito(leito):
    """
    --- BLOCO 1: CADASTRO DE INFRAESTRUTURA (CREATE) ---
    Adiciona um novo leito ao inventário hospitalar.
    Define o número da acomodação, o tipo (Enfermaria, UTI, etc) e o status inicial.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    leito_id = None
    try:
        cursor.execute("""
            INSERT INTO leito (numero, tipo, status)
            VALUES (?, ?, ?)
        """, (leito.get_numero(), leito.get_tipo(), leito.get_status()))
        conexao.commit()
        leito_id = cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Erro ao inserir leito: {e}")
    finally:
        conexao.close()
    return leito_id

def consultarLeitos():
    """
    --- BLOCO 2: MONITORAMENTO DE DISPONIBILIDADE (READ) ---
    Retorna a lista de todos os leitos e seus respectivos estados atuais 
    (Livre, Ocupado, Manutenção).
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    dados = []
    try:
        cursor.execute("SELECT * FROM leito")
        rows = cursor.fetchall()
        for row in rows:
            dados.append({
                "ID": row[0],
                "Numero": row[1],
                "Tipo": row[2],
                "Status": row[3]
            })
    except sqlite3.Error as e:
        print(f"Erro ao consultar leitos: {e}")
    finally:
        conexao.close()
    return dados

def atualizarLeito(leito):
    """
    --- BLOCO 3: MANUTENÇÃO DE DADOS (UPDATE) ---
    Permite alterar as características ou o status de um leito específico.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            UPDATE leito 
            SET numero = ?, tipo = ?, status = ?
            WHERE id = ?
        """, (leito.get_numero(), leito.get_tipo(), leito.get_status(), leito.get_id()))
        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao atualizar leito: {e}")
        return False
    finally:
        conexao.close()

def excluirLeito(id_leito):
    """
    --- BLOCO 4: REMOÇÃO DE INFRAESTRUTURA (DELETE) ---
    Exclui o registro de um leito do sistema.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM leito WHERE id = ?", (id_leito,))
        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao excluir leito: {e}")
        return False
    finally:
        conexao.close()
