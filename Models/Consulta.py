# =================================================================
# MODELO: Consulta
# Responsabilidade: Representa a entidade Consulta (Agendamento) no sistema hospitalar.
# =================================================================

class Consulta:
    """
    Representa a entidade Consulta (Agendamento) no sistema hospitalar.
    Controla o vínculo entre paciente, médico e o horário agendado.
    """
    def __init__(self, id, paciente_id, medico_id, data_hora, status, observacoes=""):
        """Inicializa os atributos da consulta."""
        # --- BLOCO: IDENTIFICAÇÃO E VÍNCULOS ---
        self._id = id
        self._paciente_id = paciente_id
        self._medico_id = medico_id
        
        # --- BLOCO: DADOS DO AGENDAMENTO ---
        self._data_hora = data_hora
        self._status = status
        self._observacoes = observacoes

    # --- BLOCO: MÉTODOS DE ACESSO (GETTERS/SETTERS) ---

    def get_id(self):
        """Retorna o ID da consulta."""
        return self._id

    def set_id(self, id):
        """Define o ID da consulta."""
        self._id = id

    def get_paciente_id(self):
        """Retorna o ID do paciente."""
        return self._paciente_id

    def set_paciente_id(self, paciente_id):
        """Define o ID do paciente."""
        self._paciente_id = paciente_id

    def get_medico_id(self):
        """Retorna o ID do médico."""
        return self._medico_id

    def set_medico_id(self, medico_id):
        """Define o ID do médico."""
        self._medico_id = medico_id

    def get_data_hora(self):
        """Retorna a data e hora da consulta."""
        return self._data_hora

    def set_data_hora(self, data_hora):
        """Define a data e hora da consulta."""
        self._data_hora = data_hora

    def get_status(self):
        """Retorna o status da consulta."""
        return self._status

    def set_status(self, status):
        """Define o status da consulta."""
        self._status = status

    def get_observacoes(self):
        """Retorna as observações da consulta."""
        return self._observacoes

    def set_observacoes(self, observacoes):
        """Define as observações da consulta."""
        self._observacoes = observacoes
