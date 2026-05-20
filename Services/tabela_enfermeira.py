from Services.database import conectaBD

def criar_tabela():
    conexao = conectaBD()
    cursor = conexao.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enfermeira (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        coren TEXT NOT NULL UNIQUE
    );
    """)
    conexao.commit()
    cursor.close()
    conexao.close()
    print("Tabela 'enfermeira' criada com sucesso!")

if __name__ == "__main__":
    criar_tabela()
