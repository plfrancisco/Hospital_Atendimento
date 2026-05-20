class Medico:
    """
    Representa a entidade Médico no sistema hospitalar.
    """
    def __init__(self, id, nome, crm, especialidade):
        self._id = id
        self._nome = nome
        self._crm = crm
        self._especialidade = especialidade

    def get_id(self): return self._id
    def set_id(self, id): self._id = id

    def get_nome(self): return self._nome
    def set_nome(self, nome): self._nome = nome

    def get_crm(self): return self._crm
    def set_crm(self, crm): self._crm = crm

    def get_especialidade(self): return self._especialidade
    def set_especialidade(self, especialidade): self._especialidade = especialidade
