# =================================================================
# MODELO: Paciente
# Responsabilidade: Representa a entidade Paciente no sistema hospitalar.
# =================================================================

class Paciente:
    """
    Representa a entidade Paciente no sistema hospitalar.
    Armazena dados básicos de identificação e classificação de prioridade.
    """
    def __init__(self, id, nome, cpf, prioridade):
        """
        --- BLOCO 1: CONSTRUTOR ---
        Inicializa os atributos do paciente no momento da criação do objeto.
        """
        # Uso do prefixo _ para incentivar o uso de getters e setters (Encapsulamento)
        self._id = id
        self._nome = nome
        self._cpf = cpf
        self._prioridade = prioridade

    # --- BLOCO 2: MÉTODOS DE ACESSO (ENCAPSULAMENTO) ---
    # Estes métodos (getters e setters) permitem que o resto do sistema
    # interaja com os dados de forma controlada e segura.

    def get_id(self):
        """Retorna o identificador único gerado pelo Banco de Dados."""
        return self._id

    def set_id(self, id):
        """Atualiza o ID (geralmente usado durante a persistência)."""
        self._id = id

    def get_nome(self):
        """Retorna o nome completo do cidadão/paciente."""
        return self._nome

    def set_nome(self, nome):
        """Permite corrigir ou atualizar o nome do paciente."""
        self._nome = nome

    def get_cpf(self):
        """Retorna o CPF (identificador fiscal/social único)."""
        return self._cpf

    def set_cpf(self, cpf):
        """Define o CPF do paciente."""
        self._cpf = cpf

    def get_prioridade(self):
        """Retorna o nível de prioridade (ex: Normal, Preferencial, Emergência)."""
        return self._prioridade

    def set_prioridade(self, prioridade):
        """Atualiza o status de prioridade conforme a triagem."""
        self._prioridade = prioridade
