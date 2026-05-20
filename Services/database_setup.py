# =================================================================
# SERVIÇO: Database Setup
# Responsabilidade: Centralizar a criação e configuração de todas as tabelas
# =================================================================

from Services.database import conectaBD

def configurar_tabelas():
    """
    Executa os comandos SQL para criação de todas as tabelas do sistema,
    garantindo a integridade referencial e configurações iniciais.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    print("--- [DATABASE SETUP] Iniciando Configuração de Tabelas ---")

    # 1. TABELA: USUARIO (Acesso ao Sistema)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        nivel_acesso TEXT DEFAULT 'ADMIN'
    );
    """)

    # 2. TABELA: PACIENTE (Dados Cadastrais)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS paciente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL UNIQUE,
        prioridade TEXT NOT NULL
    );
    """)

    # 3. TABELA: MEDICO (Corpo Clínico)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medico (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        crm TEXT NOT NULL UNIQUE,
        especialidade TEXT NOT NULL
    );
    """)

    # 4. TABELA: ENFERMEIRA (Equipe de Triagem e Assistência)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enfermeira (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        coren TEXT NOT NULL UNIQUE
    );
    """)

    # 5. TABELA: LEITO (Recursos de Internação)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leito (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero TEXT NOT NULL UNIQUE,
        tipo TEXT NOT NULL,
        status TEXT NOT NULL
    );
    """)

    # 6. TABELA: ATENDIMENTO (Fluxo de Fila e Prontuário Rápido)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS atendimento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        medico_id INTEGER,
        enfermeira_id INTEGER,
        status TEXT NOT NULL,
        data_chegada DATETIME NOT NULL,
        data_triagem DATETIME,
        data_atendimento DATETIME,
        sintomas TEXT,
        sinais_vitais TEXT,
        FOREIGN KEY (paciente_id) REFERENCES paciente (id),
        FOREIGN KEY (medico_id) REFERENCES medico (id),
        FOREIGN KEY (enfermeira_id) REFERENCES enfermeira (id)
    );
    """)

    # 7. TABELA: CONSULTA (Agendamentos)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consulta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        medico_id INTEGER NOT NULL,
        data_hora DATETIME NOT NULL,
        status TEXT NOT NULL,
        observacoes TEXT,
        FOREIGN KEY (paciente_id) REFERENCES paciente (id),
        FOREIGN KEY (medico_id) REFERENCES medico (id)
    );
    """)

    # 8. TABELA: INTERNACAO (Controle de Estadia)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS internacao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        leito_id INTEGER NOT NULL,
        data_entrada DATETIME NOT NULL,
        data_saida DATETIME,
        motivo TEXT NOT NULL,
        FOREIGN KEY (paciente_id) REFERENCES paciente (id),
        FOREIGN KEY (leito_id) REFERENCES leito (id)
    );
    """)

    # 9. TABELA: DIARIO_ENFERMAGEM (Evolução Diária)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS diario_enfermagem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        internacao_id INTEGER NOT NULL,
        enfermeira_id INTEGER NOT NULL,
        observacao TEXT NOT NULL,
        data_registro DATETIME NOT NULL,
        FOREIGN KEY (internacao_id) REFERENCES internacao (id),
        FOREIGN KEY (enfermeira_id) REFERENCES enfermeira (id)
    );
    """)

    # --- SEED DATA: USUÁRIO ADMINISTRADOR ---
    cursor.execute("SELECT * FROM usuario WHERE login = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO usuario (login, senha, nivel_acesso) VALUES (?, ?, ?)", 
                       ('admin', 'admin', 'ADMIN'))
        print("✅ Usuário Admin padrão gerado com sucesso.")

    conexao.commit()
    cursor.close()
    conexao.close()
    print("✅ Configuração de tabelas finalizada com sucesso!")

if __name__ == "__main__":
    configurar_tabelas()
