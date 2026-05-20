import Services.tabela_paciente as tabela_paciente
import Services.tabela_atendimento as tabela_atendimento
import Services.tabela_medico as tabela_medico
import Services.tabela_consulta as tabela_consulta
import Services.tabela_leito as tabela_leito
import Services.tabela_internacao as tabela_internacao
import Services.tabela_enfermeira as tabela_enfermeira
import Services.tabela_diario as tabela_diario
import Services.tabela_usuario as tabela_usuario

def inicializar_sistema():
    """
    Orquestra a criação de todas as tabelas necessárias para o sistema.
    Deve ser chamado no início da execução da aplicação.
    """
    print("Iniciando Verificação de Banco de Dados...")
    tabela_usuario.criar_tabela()
    tabela_paciente.criar_tabela()
    tabela_atendimento.criar_tabela()
    tabela_medico.criar_tabela()
    tabela_consulta.criar_tabela()
    tabela_leito.criar_tabela()
    tabela_internacao.criar_tabela()
    tabela_enfermeira.criar_tabela()
    tabela_diario.criar_tabela()
    print("Sistema de Banco de Dados pronto para uso!")

if __name__ == "__main__":
    inicializar_sistema()
