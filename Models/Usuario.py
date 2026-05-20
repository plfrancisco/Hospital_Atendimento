# =================================================================
# MODELO: Usuario
# Responsabilidade: Representação de um Usuário do Sistema Hospitalar.
# =================================================================

class Usuario:
    """
    Representação de um Usuário do Sistema Hospitalar.
    Controla as credenciais de acesso e o nível de permissão.
    """
    def __init__(self, id, login, senha, nivel_acesso="ADMIN"):
        """Inicializa os atributos do usuário."""
        # --- BLOCO: CREDENCIAIS E ACESSO ---
        self._id = id
        self._login = login
        self._senha = senha
        self._nivel_acesso = nivel_acesso

    # --- BLOCO: MÉTODOS DE ACESSO (GETTERS) ---

    def get_id(self):
        """Retorna o ID do usuário."""
        return self._id

    def get_login(self):
        """Retorna o login do usuário."""
        return self._login

    def get_senha(self):
        """Retorna a senha do usuário."""
        return self._senha

    def get_nivel_acesso(self):
        """Retorna o nível de acesso do usuário."""
        return self._nivel_acesso
