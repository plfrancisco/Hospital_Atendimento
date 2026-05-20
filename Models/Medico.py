# =================================================================
# MODELO: Medico
# Responsabilidade: Representa a entidade Médico no sistema hospitalar.
# =================================================================

class Medico:
    """
    Representa a entidade Médico no sistema hospitalar.
    Armazena dados profissionais e especialidade.
    """
    def __init__(self, id, nome, crm, especialidade):
        """Inicializa os atributos do médico."""
        # --- BLOCO: ATRIBUTOS BÁSICOS ---
        self._id = id
        self._nome = nome
        self._crm = crm
        self._especialidade = especialidade

    # --- BLOCO: MÉTODOS DE ACESSO (GETTERS/SETTERS) ---

    def get_id(self): 
        """Retorna o ID do médico."""
        return self._id
    
    def set_id(self, id): 
        """Define o ID do médico."""
        self._id = id

    def get_nome(self): 
        """Retorna o nome do médico."""
        return self._nome
    
    def set_nome(self, nome): 
        """Define o nome do médico."""
        self._nome = nome

    def get_crm(self): 
        """Retorna o CRM do médico."""
        return self._crm
    
    def set_crm(self, crm): 
        """Define o CRM do médico."""
        self._crm = crm

    def get_especialidade(self): 
        """Retorna a especialidade do médico."""
        return self._especialidade
    
    def set_especialidade(self, especialidade): 
        """Define a especialidade do médico."""
        self._especialidade = especialidade
