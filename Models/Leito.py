class Leito:
    """
    Representa a infraestrutura de Leitos no hospital.
    """
    def __init__(self, id, numero, tipo, status):
        self._id = id
        self._numero = numero
        self._tipo = tipo
        self._status = status

    def get_id(self): return self._id
    def set_id(self, id): self._id = id

    def get_numero(self): return self._numero
    def set_numero(self, numero): self._numero = numero

    def get_tipo(self): return self._tipo
    def set_tipo(self, tipo): self._tipo = tipo

    def get_status(self): return self._status
    def set_status(self, status): self._status = status
