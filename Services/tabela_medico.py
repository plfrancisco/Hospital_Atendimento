from Services.database import conectaBD

def criar_tabela():
    conexao = conectaBD()
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medico (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        crm TEXT NOT NULL UNIQUE,
        especialidade TEXT NOT NULL
    );
    """)

    conexao.commit()
    cursor.close()
    conexao.close()
    print("Tabela 'medico' criada com sucesso!")

if __name__ == "__main__":
    criar_tabela()
