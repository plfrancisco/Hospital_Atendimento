# =================================================================
# CONTROLLER: AtendimentoController.py
# Responsabilidade: Gerenciar o fluxo de atendimento dos pacientes, 
# desde a chegada até a finalização do atendimento médico.
# =================================================================

import sqlite3
from datetime import datetime
from Services.database import conectaBD

def registrarChegada(paciente_id):
    """
    Cria um novo registro na tabela 'atendimento' assim que o paciente é cadastrado.
    Define o status inicial como 'Aguardando Triagem' e salva o momento exato da chegada.
    """
    # --- BLOCO: CONEXÃO COM O BANCO ---
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    try:
        # --- BLOCO: REGISTRO DE DADOS ---
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

def obterProximaEnfermeiraRodizio():
    """
    Busca a lista de enfermeiras e identifica quem foi a última a realizar triagem.
    Retorna o ID da próxima enfermeira na sequência.
    """
    # --- BLOCO: INICIALIZAÇÃO ---
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    try:
        # --- BLOCO: BUSCA DE ENFERMEIRAS ---
        # 1. Obter todas as enfermeiras ordenadas por ID
        cursor.execute("SELECT id FROM enfermeira ORDER BY id ASC")
        enfermeiras = [row[0] for row in cursor.fetchall()]
        
        if not enfermeiras:
            return None
            
        # --- BLOCO: VERIFICAÇÃO DE ÚLTIMA TRIAGEM ---
        # 2. Obter o ID da última enfermeira que realizou uma triagem
        cursor.execute("""
            SELECT enfermeira_id FROM atendimento 
            WHERE enfermeira_id IS NOT NULL 
            ORDER BY data_triagem DESC LIMIT 1
        """)
        last_row = cursor.fetchone()
        
        if not last_row:
            return enfermeiras[0] # Se ninguém fez triagem ainda, pega a primeira
            
        last_id = last_row[0]
        
        # --- BLOCO: LÓGICA DE RODÍZIO ---
        # 3. Lógica de Rodízio: encontrar o próximo ID
        try:
            current_index = enfermeiras.index(last_id)
            next_index = (current_index + 1) % len(enfermeiras)
            return enfermeiras[next_index]
        except ValueError:
            # Caso a enfermeira que fez a última triagem tenha sido deletada
            return enfermeiras[0]
            
    except sqlite3.Error as e:
        print(f"Erro no rodízio: {e}")
        return None
    finally:
        conexao.close()

def finalizarTriagem(atendimento_id, enfermeira_id, sintomas, sinais_vitais, medico_id):
    """
    Atualiza um atendimento existente. Muda o status para 'Aguardando Atendimento',
    vincula a enfermeira responsável, o médico selecionado e registra os dados clínicos.
    """
    # --- BLOCO: CONEXÃO E ATUALIZAÇÃO ---
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    try:
        # --- BLOCO: PERSISTÊNCIA DE DADOS ---
        data_triagem = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            UPDATE atendimento 
            SET status = ?, data_triagem = ?, enfermeira_id = ?, sintomas = ?, sinais_vitais = ?, medico_id = ?
            WHERE id = ?
        """, ("Aguardando Atendimento", data_triagem, enfermeira_id, sintomas, sinais_vitais, medico_id, atendimento_id))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao finalizar triagem: {e}")
    finally:
        conexao.close()

def finalizarAtendimento(atendimento_id, medico_id):
    """
    Conclui a jornada do paciente no sistema. O status passa para 'Atendido',
    vincula o médico responsável e o horário da consulta é salvo.
    """
    # --- BLOCO: CONEXÃO ---
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    try:
        # --- BLOCO: ATUALIZAÇÃO DE STATUS ---
        data_atendimento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            UPDATE atendimento 
            SET status = ?, data_atendimento = ?, medico_id = ?
            WHERE id = ?
        """, ("Atendido", data_atendimento, medico_id, atendimento_id))
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao finalizar atendimento: {e}")
    finally:
        conexao.close()

def consultarFila(status_filtro=None):
    """
    Recupera os dados de atendimento do banco, unindo (JOIN) com as informações do paciente,
    enfermeira e médico.
    """
    # --- BLOCO: PREPARAÇÃO ---
    conexao = conectaBD()
    cursor = conexao.cursor()
    dados = []
    
    try:
        # --- BLOCO: QUERY SQL ---
        query = """
            SELECT a.id, p.nome, p.prioridade, a.status, a.data_chegada, a.data_triagem, a.data_atendimento, 
                   m.nome, e.nome, a.sintomas, a.sinais_vitais
            FROM atendimento a
            JOIN paciente p ON a.paciente_id = p.id
            LEFT JOIN medico m ON a.medico_id = m.id
            LEFT JOIN enfermeira e ON a.enfermeira_id = e.id
        """
        
        # --- BLOCO: EXECUÇÃO E FILTRAGEM ---
        if status_filtro:
            query += " WHERE a.status = ?"
            cursor.execute(query, (status_filtro,))
        else:
            cursor.execute(query)
            
        rows = cursor.fetchall()
        
        # --- BLOCO: ESTRUTURAÇÃO DOS RESULTADOS ---
        for row in rows:
            dados.append({
                "ID": row[0],
                "Paciente": row[1],
                "Prioridade": row[2],
                "Status": row[3],
                "Chegada": row[4],
                "Triagem": row[5],
                "Atendimento": row[6],
                "Médico": row[7] if row[7] else "Pendente",
                "Enfermeira": row[8] if row[8] else "Pendente",
                "Sintomas": row[9],
                "Sinais Vitais": row[10]
            })
    except sqlite3.Error as e:
        print(f"Erro ao consultar fila: {e}")
    finally:
        conexao.close()
    return dados
