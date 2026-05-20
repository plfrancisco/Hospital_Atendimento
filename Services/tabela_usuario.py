from Services.database import conectaBD

def criar_tabela():
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    # Criar Tabela
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        nivel_acesso TEXT DEFAULT 'ADMIN'
    );
    """)
    
    # Inserir Usuário Padrão (admin/admin) caso não exista
    cursor.execute("SELECT * FROM usuario WHERE login = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO usuario (login, senha, nivel_acesso) VALUES (?, ?, ?)", 
                       ('admin', 'admin', 'ADMIN'))
    
    conexao.commit()
    cursor.close()
    conexao.close()
    print("Tabela 'usuario' configurada com sucesso!")

if __name__ == "__main__":
    criar_tabela()
