from Services.database import conectaBD

def criar_tabela():
    conexao = conectaBD()
    cursor = conexao.cursor()

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

    conexao.commit()
    cursor.close()
    conexao.close()
    print("Tabela 'consulta' criada com sucesso!")

if __name__ == "__main__":
    criar_tabela()
