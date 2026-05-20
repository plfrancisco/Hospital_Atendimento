class Atendimento:
    """
    Representa o registro de um atendimento hospitalar.
    Controla o vínculo com o paciente, o status atual e os registros de horários.
    """
    def __init__(self, id, paciente_id, status, data_chegada, data_triagem=None, data_atendimento=None, sintomas=None, sinais_vitais=None):
        self._id = id                    # Identificador único do atendimento
        self._paciente_id = paciente_id  # ID do paciente vinculado (chave estrangeira)
        self._status = status            # Status atual (ex: Aguardando, Triagem, Atendido)
        self._data_chegada = data_chegada # Data/Hora da recepção
        self._data_triagem = data_triagem # Data/Hora que passou pela triagem
        self._data_atendimento = data_atendimento # Data/Hora do início do atendimento médico
        self._sintomas = sintomas
        self._sinais_vitais = sinais_vitais

    def get_id(self):
    ...
    def set_data_atendimento(self, data_atendimento):
        self._data_atendimento = data_atendimento

    def get_sintomas(self):
        return self._sintomas

    def set_sintomas(self, sintomas):
        self._sintomas = sintomas

    def get_sinais_vitais(self):
        return self._sinais_vitais

    def set_sinais_vitais(self, sinais_vitais):
        self._sinais_vitais = sinais_vitais
    def set_id(self, id):
        """Define o ID do atendimento."""
        self._id = id

    def get_paciente_id(self):
        """Retorna o ID do paciente associado a este atendimento."""
        return self._paciente_id

    def set_paciente_id(self, paciente_id):
        """Vincula um paciente ao atendimento via ID."""
        self._paciente_id = paciente_id

    def get_status(self):
        """Retorna o status atual do processo."""
        return self._status

    def set_status(self, status):
        """Atualiza o status do atendimento."""
        self._status = status

    def get_data_chegada(self):
        """Retorna a data/hora de chegada."""
        return self._data_chegada

    def set_data_chegada(self, data_chegada):
        self._data_chegada = data_chegada

    def get_data_triagem(self):
        """Retorna a data/hora em que a triagem foi realizada."""
        return self._data_triagem

    def set_data_triagem(self, data_triagem):
        self._data_triagem = data_triagem

    def get_data_atendimento(self):
        """Retorna a data/hora em que o atendimento médico iniciou."""
        return self._data_atendimento

    def set_data_atendimento(self, data_atendimento):
        self._data_atendimento = data_atendimento
