from Services.database import conectaBD

def criar_tabela():
    conexao = conectaBD()
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leito (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero TEXT NOT NULL UNIQUE,
        tipo TEXT NOT NULL,
        status TEXT NOT NULL
    );
    """)

    conexao.commit()
    cursor.close()
    conexao.close()
    print("Tabela 'leito' criada com sucesso!")

if __name__ == "__main__":
    criar_tabela()
