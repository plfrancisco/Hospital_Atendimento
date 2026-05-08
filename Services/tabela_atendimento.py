from Services.database import conectaBD

def criar_tabela():
    conexao = conectaBD()
    cursor = conexao.cursor()

    # status: "Aguardando Triagem", "Aguardando Atendimento", "Atendido"
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS atendimento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        status TEXT NOT NULL,
        data_chegada DATETIME NOT NULL,
        data_triagem DATETIME,
        data_atendimento DATETIME,
        FOREIGN KEY (paciente_id) REFERENCES paciente (id)
    );
    """)

    conexao.commit()
    cursor.close()
    conexao.close()
    print("Tabela 'atendimento' criada com sucesso!")

if __name__ == "__main__":
    criar_tabela()
