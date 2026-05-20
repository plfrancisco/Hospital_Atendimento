from Services.database import conectaBD

def criar_tabela():
    conexao = conectaBD()
    cursor = conexao.cursor()

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

    conexao.commit()
    cursor.close()
    conexao.close()
    print("Tabela 'diario_enfermagem' criada com sucesso!")

if __name__ == "__main__":
    criar_tabela()
