# =================================================================
# SERVIÇO: Database Engine
# Responsabilidade: Ponto de entrada para inicialização da persistência.
# =================================================================

import Services.database_setup as db_setup

def inicializar_sistema():
    """
    --- BLOCO 1: ORQUESTRAÇÃO DE INFRAESTRUTURA ---
    Esta função é chamada uma única vez no início da execução (no main.py).
    Ela coordena a criação de tabelas e configurações fundamentais para que
    o sistema não falhe por falta de estrutura de dados.
    """
    try:
        # Log de console para depuração rápida durante o desenvolvimento
        print("--- [DATABASE ENGINE] Inicializando Sistema ---")
        
        # Chama o serviço de setup que contém os comandos SQL de criação
        db_setup.configurar_tabelas()
        
        print("--- [DATABASE ENGINE] Sistema Pronto para Operação ---")
    except Exception as e:
        # Tratamento de erro centralizado para falhas de conexão ou permissão
        print(f"--- [DATABASE ENGINE] ERRO CRÍTICO NA INICIALIZAÇÃO: {e} ---")

# Permite rodar este script isoladamente para testar a criação do banco
if __name__ == "__main__":
    inicializar_sistema()
