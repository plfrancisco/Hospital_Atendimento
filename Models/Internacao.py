class Internacao:
    """
    Representa o registro de internação de um paciente em um leito.
    """
    def __init__(self, id, paciente_id, leito_id, data_entrada, data_saida, motivo):
        self._id = id
        self._paciente_id = paciente_id
        self._leito_id = leito_id
        self._data_entrada = data_entrada
        self._data_saida = data_saida
        self._motivo = motivo

    def get_id(self): return self._id
    def set_id(self, id): self._id = id

    def get_paciente_id(self): return self._paciente_id
    def set_paciente_id(self, paciente_id): self._paciente_id = paciente_id

    def get_leito_id(self): return self._leito_id
    def set_leito_id(self, leito_id): self._leito_id = leito_id

    def get_data_entrada(self): return self._data_entrada
    def set_data_entrada(self, data_entrada): self._data_entrada = data_entrada

    def get_data_saida(self): return self._data_saida
    def set_data_saida(self, data_saida): self._data_saida = data_saida

    def get_motivo(self): return self._motivo
    def set_motivo(self, motivo): self._motivo = motivo
