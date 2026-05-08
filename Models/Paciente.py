class Paciente:
    def __init__(self, id, nome, cpf, prioridade):
        self._id = id
        self._nome = nome
        self._cpf = cpf
        self._prioridade = prioridade

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_nome(self):
        return self._nome

    def set_nome(self, nome):
        self._nome = nome

    def get_cpf(self):
        return self._cpf

    def set_cpf(self, cpf):
        self._cpf = cpf

    def get_prioridade(self):
        return self._prioridade

    def set_prioridade(self, prioridade):
        self._prioridade = prioridade
