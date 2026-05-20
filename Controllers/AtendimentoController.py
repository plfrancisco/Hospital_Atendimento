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
    --- BLOCO 1: REGISTRO DE CHEGADA ---
    Cria um novo registro na tabela 'atendimento' assim que o paciente é cadastrado na recepção.
    Define o status inicial como 'Aguardando Triagem' e salva o timestamp exato da entrada.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    try:
        # Captura a data e hora atual no formato padrão SQL
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
    --- BLOCO 2: LÓGICA DE RODÍZIO (SMART ASSIGNMENT) ---
    Garante uma distribuição justa de trabalho buscando a lista de enfermeiras 
    e identificando quem foi a última a realizar uma triagem para selecionar a próxima.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    try:
        # Passo A: Obter todas as enfermeiras disponíveis ordenadas
        cursor.execute("SELECT id FROM enfermeira ORDER BY id ASC")
        enfermeiras = [row[0] for row in cursor.fetchall()]
        
        if not enfermeiras:
            return None
            
        # Passo B: Localizar quem fez a triagem mais recente no sistema
        cursor.execute("""
            SELECT enfermeira_id FROM atendimento 
            WHERE enfermeira_id IS NOT NULL 
            ORDER BY data_triagem DESC LIMIT 1
        """)
        last_row = cursor.fetchone()
        
        if not last_row:
            return enfermeiras[0] # Se for o primeiro atendimento do dia, pega a primeira da lista
            
        last_id = last_row[0]
        
        # Passo C: Calcular o próximo índice da lista (Circular Buffer Logic)
        try:
            current_index = enfermeiras.index(last_id)
            next_index = (current_index + 1) % len(enfermeiras)
            return enfermeiras[next_index]
        except ValueError:
            # Caso a enfermeira que fez a última triagem não esteja mais no sistema
            return enfermeiras[0]
            
    except sqlite3.Error as e:
        print(f"Erro no rodízio: {e}")
        return None
    finally:
        conexao.close()

def finalizarTriagem(atendimento_id, enfermeira_id, sintomas, sinais_vitais, medico_id):
    """
    --- BLOCO 3: CONCLUSÃO DA TRIAGEM ---
    Atualiza o registro de atendimento com os dados coletados pela enfermagem.
    Muda o status para 'Aguardando Atendimento' e encaminha para o médico selecionado.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    try:
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
    --- BLOCO 4: CONCLUSÃO MÉDICA ---
    Encerra a jornada do paciente na unidade de atendimento imediato. 
    O status passa para 'Atendido', selando o registro clínico.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    try:
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
    --- BLOCO 5: CONSULTA DA FILA (READ MULTI-TABLE) ---
    Recupera os dados de atendimento unindo (JOIN) informações de múltiplas tabelas
    para apresentar uma visão completa (Paciente, Médico e Enfermeira).
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    dados = []
    
    try:
        # Query unificada que traz nomes em vez de apenas IDs (Foreign Keys)
        query = """
            SELECT a.id, p.nome, p.prioridade, a.status, a.data_chegada, a.data_triagem, a.data_atendimento, 
                   m.nome, e.nome, a.sintomas, a.sinais_vitais
            FROM atendimento a
            JOIN paciente p ON a.paciente_id = p.id
            LEFT JOIN medico m ON a.medico_id = m.id
            LEFT JOIN enfermeira e ON a.enfermeira_id = e.id
        """
        
        if status_filtro:
            query += " WHERE a.status = ?"
            cursor.execute(query, (status_filtro,))
        else:
            cursor.execute(query)
            
        rows = cursor.fetchall()
        
        # Converte o resultado bruto do banco em uma lista de dicionários (Fácil uso no Streamlit)
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
