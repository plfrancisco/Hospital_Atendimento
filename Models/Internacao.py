# =================================================================
# MODELO: Internacao
# Responsabilidade: Representa o registro de internação de um paciente em um leito.
# =================================================================

class Internacao:
    """
    Representa o registro de internação de um paciente em um leito.
    Controla o tempo de permanência e o motivo clínico.
    """
    def __init__(self, id, paciente_id, leito_id, data_entrada, data_saida, motivo):
        """Inicializa os atributos da internação."""
        # --- BLOCO: VÍNCULOS ---
        self._id = id
        self._paciente_id = paciente_id
        self._leito_id = leito_id
        
        # --- BLOCO: DADOS DA ESTADIA ---
        self._data_entrada = data_entrada
        self._data_saida = data_saida
        self._motivo = motivo

    # --- BLOCO: MÉTODOS DE ACESSO (GETTERS/SETTERS) ---

    def get_id(self):
        """Retorna o ID da internação."""
        return self._id

    def set_id(self, id):
        """Define o ID da internação."""
        self._id = id

    def get_paciente_id(self):
        """Retorna o ID do paciente."""
        return self._paciente_id

    def set_paciente_id(self, paciente_id):
        """Define o ID do paciente."""
        self._paciente_id = paciente_id

    def get_leito_id(self):
        """Retorna o ID do leito."""
        return self._leito_id

    def set_leito_id(self, leito_id):
        """Define o ID do leito."""
        self._leito_id = leito_id

    def get_data_entrada(self):
        """Retorna a data de entrada."""
        return self._data_entrada

    def set_data_entrada(self, data_entrada):
        """Define a data de entrada."""
        self._data_entrada = data_entrada

    def get_data_saida(self):
        """Retorna a data de saída."""
        return self._data_saida

    def set_data_saida(self, data_saida):
        """Define a data de saída."""
        self._data_saida = data_saida

    def get_motivo(self):
        """Retorna o motivo da internação."""
        return self._motivo

    def set_motivo(self, motivo):
        """Define o motivo da internação."""
        self._motivo = motivo
