# =================================================================
# MODELO: Enfermeira
# Responsabilidade: Representa a entidade Enfermeira no sistema hospitalar.
# =================================================================

class Enfermeira:
    """
    Representa a entidade Enfermeira no sistema hospitalar.
    Armazena dados de identificação profissional (COREN).
    """
    def __init__(self, id, nome, coren):
        """Inicializa os atributos da enfermeira."""
        # --- BLOCO: ATRIBUTOS BÁSICOS ---
        self._id = id
        self._nome = nome
        self._coren = coren

    # --- BLOCO: MÉTODOS DE ACESSO (GETTERS) ---

    def get_id(self):
        """Retorna o ID da enfermeira."""
        return self._id

    def get_nome(self):
        """Retorna o nome da enfermeira."""
        return self._nome

    def get_coren(self):
        """Retorna o COREN da enfermeira."""
        return self._coren
