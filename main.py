# =================================================================
# NÚCLEO HOSPITALAR: Arquivo Principal (main.py)
# Responsabilidade: Orquestração Global, Roteamento e Sessão
# =================================================================

import streamlit as st
from streamlit_option_menu import option_menu
import Views.PageRecepcao as PageRecepcao
import Views.PageTriagem as PageTriagem
import Views.PageFluxo as PageFluxo
import Views.PageLeitos as PageLeitos
import Views.PageDashboard as PageDashboard
import Views.PageLogin as PageLogin
import Services.database_engine as db_engine

# --- BLOCO 1: INICIALIZAÇÃO DO MOTOR ---
# Este bloco invoca o motor de banco de dados para garantir que a infraestrutura (SQLite)
# e as 8 tabelas do sistema estejam prontas antes de qualquer interação do usuário.
db_engine.inicializar_sistema()

# Configuração global da página (Título na aba do navegador e layout expandido)
st.set_page_config(page_title="Sistema de Gestão Hospitalar", layout="wide")

# --- BLOCO 2: GESTÃO DE ESTADO (SESSION STATE) ---
# Inicializa a variável de controle de acesso no estado da sessão do Streamlit.
# Isso impede que o usuário acesse as páginas internas sem passar pelo login.
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

# --- BLOCO 3: IDENTIDADE VISUAL (CSS CUSTOMIZADO) ---
# Injeta CSS diretamente no HTML do Streamlit para aplicar o estilo "Sofia Edition".
# Define cores de fundo, fontes corporativas e o posicionamento do botão de logout.
st.markdown("""
    <style>
    .main { background-color: #f1f5f9; font-family: 'Inter', sans-serif; }
    
    /* Ajuste para o rodapé da Sidebar */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:last-child {
        margin-top: auto;
        padding-top: 100px;
    }
    
    .stButton>button { border-radius: 6px !important; }
    </style>
""", unsafe_allow_html=True)

# --- BLOCO 4: GATEKEEPER (BARREIRA DE LOGIN) ---
# Se o usuário não estiver autenticado, a execução do script é interrompida (st.stop())
# após renderizar apenas a página de login.
if not st.session_state['autenticado']:
    PageLogin.exibir_pagina()
    st.stop()

# --- BLOCO 5: NAVEGAÇÃO LATERAL (SIDEBAR) ---
# Cria o menu de navegação corporativo utilizando o componente 'option_menu'.
# Cada opção no menu corresponde a um módulo funcional do hospital.
with st.sidebar:
    st.markdown("<h2 style='color: #0f172a; margin-bottom: 20px;'>NÚCLEO HOSPITALAR</h2>", unsafe_allow_html=True)
    modulo = option_menu(
        menu_title=None,
        options=["Recepção", "Triagem", "Operações", "Internação", "Indicadores"],
        icons=["person-vcard", "clipboard2-pulse", "layout-text-sidebar", "hospital", "bar-chart-line"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0px!important", "background-color": "#ffffff", "border-radius": "0px"},
            "icon": {"color": "#64748b", "font-size": "18px"}, 
            "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#f1f5f9", "color": "#475569"},
            "nav-link-selected": {"background-color": "#eff6ff", "color": "#1e40af", "border-left": "4px solid #1e40af", "font-weight": "700"},
        }
    )
    
    # Espaçamento para empurrar os controles de sistema para o final da barra
    st.markdown("<div style='height: 40vh;'></div>", unsafe_allow_html=True)
    
    # Lógica de Logout: Limpa o estado de autenticação e reinicia o script.
    if st.button("ENCERRAR SESSÃO", type="primary", use_container_width=True, key="btn_logout_hospital"):
        st.session_state['autenticado'] = False
        st.rerun()

    # Informações de Versão e Controle de Estação
    st.sidebar.divider()
    st.sidebar.markdown("""
        <div style='color: #94a3b8; font-size: 11px;'>
            VERSÃO DO SISTEMA: 3.5.0-SECURE<br>
            ESTAÇÃO: CORE-01
        </div>
    """, unsafe_allow_html=True)

# --- BLOCO 6: DISPATCHER (ROTEADOR DE MÓDULOS) ---
# De acordo com a seleção feita no menu lateral, este bloco chama a função
# de exibição da respectiva página (View).
if modulo == "Recepção":
    PageRecepcao.exibir_pagina()
elif modulo == "Triagem":
    PageTriagem.exibir_pagina()
elif modulo == "Operações":
    PageFluxo.exibir_pagina()
elif modulo == "Internação":
    PageLeitos.exibir_pagina()
elif modulo == "Indicadores":
    PageDashboard.exibir_pagina()
