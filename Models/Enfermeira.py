class Enfermeira:
    """
    Representa a entidade Enfermeira no sistema hospitalar.
    """
    def __init__(self, id, nome, coren):
        self._id = id
        self._nome = nome
        self._coren = coren

    def get_id(self): return self._id
    def get_nome(self): return self._nome
    def get_coren(self): return self._coren
