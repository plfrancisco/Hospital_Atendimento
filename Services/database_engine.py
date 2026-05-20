# =================================================================
# SERVIÇO: Database Engine
# Responsabilidade: Ponto de entrada para inicialização do banco de dados
# =================================================================

import Services.database_setup as db_setup

def inicializar_sistema():
    """
    Coordena a inicialização do banco de dados, chamando a criação
    de tabelas e configurações fundamentais.
    """
    try:
        print("--- [DATABASE ENGINE] Inicializando Sistema ---")
        db_setup.configurar_tabelas()
        print("--- [DATABASE ENGINE] Sistema Pronto para Operação ---")
    except Exception as e:
        print(f"--- [DATABASE ENGINE] ERRO CRÍTICO NA INICIALIZAÇÃO: {e} ---")

if __name__ == "__main__":
    inicializar_sistema()
