from Services.database import conectaBD

def criar_tabela():
    conexao = conectaBD()
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS paciente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL UNIQUE,
        prioridade TEXT NOT NULL
    );
    """)

    conexao.commit()
    cursor.close()
    conexao.close()
    print("Tabela 'paciente' criada com sucesso!")

if __name__ == "__main__":
    criar_tabela()
