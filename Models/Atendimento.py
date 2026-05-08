class Atendimento:
    def __init__(self, id, paciente_id, status, data_chegada, data_triagem=None, data_atendimento=None):
        self._id = id
        self._paciente_id = paciente_id
        self._status = status
        self._data_chegada = data_chegada
        self._data_triagem = data_triagem
        self._data_atendimento = data_atendimento

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_paciente_id(self):
        return self._paciente_id

    def set_paciente_id(self, paciente_id):
        self._paciente_id = paciente_id

    def get_status(self):
        return self._status

    def set_status(self, status):
        self._status = status

    def get_data_chegada(self):
        return self._data_chegada

    def set_data_chegada(self, data_chegada):
        self._data_chegada = data_chegada

    def get_data_triagem(self):
        return self._data_triagem

    def set_data_triagem(self, data_triagem):
        self._data_triagem = data_triagem

    def get_data_atendimento(self):
        return self._data_atendimento

    def set_data_atendimento(self, data_atendimento):
        self._data_atendimento = data_atendimento
