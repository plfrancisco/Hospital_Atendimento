from Services.database import conectaBD

"""
Módulo de Gerenciamento da Tabela de Pacientes.
Este serviço lida com a infraestrutura da tabela 'paciente' no banco de dados.
"""

def criar_tabela():
    """
    Cria a tabela 'paciente' caso ela ainda não exista.

    A tabela armazena os dados básicos e a classificação de risco (prioridade):
    - id: Identificador único.
    - nome: Nome completo do paciente.
    - cpf: CPF (único).
    - prioridade: Classificação (ex: Verde, Amarelo, Vermelho).
    """
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

