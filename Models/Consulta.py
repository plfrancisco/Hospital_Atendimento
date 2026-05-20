class Consulta:
    """
    Representa a entidade Consulta (Agendamento) no sistema hospitalar.
    """
    def __init__(self, id, paciente_id, medico_id, data_hora, status, observacoes=""):
        self._id = id
        self._paciente_id = paciente_id
        self._medico_id = medico_id
        self._data_hora = data_hora
        self._status = status
        self._observacoes = observacoes

    def get_id(self): return self._id
    def set_id(self, id): self._id = id

    def get_paciente_id(self): return self._paciente_id
    def set_paciente_id(self, paciente_id): self._paciente_id = paciente_id

    def get_medico_id(self): return self._medico_id
    def set_medico_id(self, medico_id): self._medico_id = medico_id

    def get_data_hora(self): return self._data_hora
    def set_data_hora(self, data_hora): self._data_hora = data_hora

    def get_status(self): return self._status
    def set_status(self, status): self._status = status

    def get_observacoes(self): return self._observacoes
    def set_observacoes(self, observacoes): self._observacoes = observacoes
