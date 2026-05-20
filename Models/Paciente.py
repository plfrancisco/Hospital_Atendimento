# =================================================================
# MODELO: Paciente
# Responsabilidade: Representa a entidade Paciente no sistema hospitalar.
# =================================================================

class Paciente:
    """
    Representa a entidade Paciente no sistema hospitalar.
    Armazena dados básicos de identificação e classificação de prioridade.
    """
    def __init__(self, id, nome, cpf, prioridade):
        """Inicializa os atributos do paciente."""
        # --- BLOCO: ATRIBUTOS PROTEGIDOS ---
        # Uso do prefixo _ para incentivar o uso de getters e setters
        self._id = id
        self._nome = nome
        self._cpf = cpf
        self._prioridade = prioridade

    # --- BLOCO: MÉTODOS DE ACESSO (GETTERS/SETTERS) ---

    def get_id(self):
        """Retorna o ID único do paciente."""
        return self._id

    def set_id(self, id):
        """Define ou atualiza o ID do paciente."""
        self._id = id

    def get_nome(self):
        """Retorna o nome completo do paciente."""
        return self._nome

    def set_nome(self, nome):
        """Define ou atualiza o nome do paciente."""
        self._nome = nome

    def get_cpf(self):
        """Retorna o CPF do paciente."""
        return self._cpf

    def set_cpf(self, cpf):
        """Define ou atualiza o CPF do paciente."""
        self._cpf = cpf

    def get_prioridade(self):
        """Retorna o nível de prioridade (ex: Normal, Preferencial)."""
        return self._prioridade

    def set_prioridade(self, prioridade):
        """Define ou atualiza a prioridade do paciente."""
        self._prioridade = prioridade
