from Services.database import conectaBD

def criar_tabela():
    conexao = conectaBD()
    cursor = conectaBD().cursor()

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

    conexao.commit()
    cursor.close()
    conexao.close()
    print("Tabela 'internacao' criada com sucesso!")

if __name__ == "__main__":
    criar_tabela()
