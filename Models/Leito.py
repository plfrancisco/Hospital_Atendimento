# =================================================================
# MODELO: Leito
# Responsabilidade: Representa a infraestrutura de Leitos no hospital.
# =================================================================

class Leito:
    """
    Representa a infraestrutura de Leitos no hospital.
    Controla o tipo de leito e sua disponibilidade atual.
    """
    def __init__(self, id, numero, tipo, status):
        """Inicializa os atributos do leito."""
        # --- BLOCO: ATRIBUTOS BÁSICOS ---
        self._id = id
        self._numero = numero
        self._tipo = tipo
        self._status = status

    # --- BLOCO: MÉTODOS DE ACESSO (GETTERS/SETTERS) ---

    def get_id(self):
        """Retorna o ID do leito."""
        return self._id

    def set_id(self, id):
        """Define o ID do leito."""
        self._id = id

    def get_numero(self):
        """Retorna o número do leito."""
        return self._numero

    def set_numero(self, numero):
        """Define o número do leito."""
        self._numero = numero

    def get_tipo(self):
        """Retorna o tipo do leito."""
        return self._tipo

    def set_tipo(self, tipo):
        """Define o tipo do leito."""
        self._tipo = tipo

    def get_status(self):
        """Retorna o status do leito."""
        return self._status

    def set_status(self, status):
        """Define o status do leito."""
        self._status = status
