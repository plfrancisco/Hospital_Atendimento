from Services.database import conectaBD

"""
Módulo de Gerenciamento da Tabela de Atendimentos.
Este serviço lida com a infraestrutura da tabela 'atendimento' no banco de dados.
"""

def criar_tabela():
    """
    Cria a tabela 'atendimento' caso ela ainda não exista.
    
    A tabela contém informações sobre o ciclo de vida do atendimento:
    - id: Identificador único.
    - paciente_id: Chave estrangeira para a tabela de pacientes.
    - status: Estado atual (Triagem, Atendimento, Atendido).
    - datas: Registros temporais de cada etapa.
    """
    conexao = conectaBD()
    cursor = conexao.cursor()

    # status: "Aguardando Triagem", "Aguardando Atendimento", "Atendido"
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

    conexao.commit()
    cursor.close()
    conexao.close()
    print("Tabela 'atendimento' criada com sucesso!")

if __name__ == "__main__":
    criar_tabela()
