# ARQUIVO PRINCIPAL (main.py)
import streamlit as st
from streamlit_option_menu import option_menu
import Views.PageRecepcao as PageRecepcao
import Views.PageTriagem as PageTriagem
import Views.PageFluxo as PageFluxo
import Views.PageLeitos as PageLeitos
import Views.PageDashboard as PageDashboard
import Views.PageLogin as PageLogin
import Services.database_engine as db_engine

# Inicializa o banco de dados e as tabelas
db_engine.inicializar_sistema()

# Configura o título da aba do navegador e o layout da página
st.set_page_config(page_title="Sistema de Gestão Hospitalar", layout="wide")

# --- CONTROLE DE SESSÃO E LOGIN ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

# --- GLOBAL CORPORATE UI ---
st.markdown("""
    <style>
    .main { background-color: #f1f5f9; font-family: 'Inter', sans-serif; }
    
    /* Logout Button - Fixed in Sidebar */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:last-child {
        margin-top: auto;
        padding-top: 100px;
    }
    
    .stButton>button { border-radius: 6px !important; }
    </style>
""", unsafe_allow_html=True)

if not st.session_state['autenticado']:
    PageLogin.exibir_pagina()
    st.stop()

# --- SIDEBAR CORPORATIVA ---
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
    
    # Empurrar o botão de logout para o final da sidebar
    st.markdown("<div style='height: 40vh;'></div>", unsafe_allow_html=True)
    
    if st.button("ENCERRAR SESSÃO", type="primary", use_container_width=True, key="btn_logout_hospital"):
        st.session_state['autenticado'] = False
        st.rerun()

    st.sidebar.divider()
    st.sidebar.markdown("""
        <div style='color: #94a3b8; font-size: 11px;'>
            VERSÃO DO SISTEMA: 3.5.0-SECURE<br>
            ESTAÇÃO: CORE-01
        </div>
    """, unsafe_allow_html=True)

# ROTEAMENTO
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
