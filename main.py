"""
ARQUIVO PRINCIPAL (main.py)
Este é o ponto de entrada da nossa aplicação. Ele gerencia a configuração da página,
o menu lateral (Sidebar) e decide qual página (View) deve ser exibida ao usuário.
"""

import streamlit as st
from streamlit_option_menu import option_menu
import Views.PageRecepcao as PageRecepcao
import Views.PageStatus as PageStatus
import Views.PageDashboard as PageDashboard

# Configura o título da aba do navegador e o layout da página para ocupar toda a largura
st.set_page_config(page_title="Sistema Hospitalar", layout="wide")

"""
BLOCO DE NAVEGAÇÃO: SIDEBAR
Aqui configuramos o menu lateral moderno. O componente 'option_menu' captura a escolha do usuário
e armazena na variável 'modulo'. Também definimos uma área de 'Operações' que muda
dependendo de qual módulo está selecionado no momento.
"""
with st.sidebar:
    st.title("🏥 Menu")
    modulo = option_menu(
        menu_title=None,
        options=["Recepção", "Status", "Dashboard"],
        icons=["person-plus", "activity", "graph-up"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#f8fafc"},
            "icon": {"color": "#007BFF", "font-size": "18px"}, 
            "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#e2e8f0"},
            "nav-link-selected": {"background-color": "#007BFF"},
        }
    )

st.sidebar.divider()
st.sidebar.title("Operações")
if modulo == "Recepção":
    operacao = st.sidebar.selectbox("Ação rápida:", ["Cadastrar Paciente", "Consultar Pacientes", "Excluir Paciente"])
elif modulo == "Dashboard":
    operacao = st.sidebar.selectbox("Ação rápida:", ["Visualizar KPIs"])
else:
    operacao = "Gestão de Fluxo"

st.title("Sistema Hospitalar - Gestão de Atendimento")

"""
BLOCO DE ROTEAMENTO (ROUTING)
Este trecho de código funciona como um 'guarda de trânsito'. Ele verifica qual módulo foi
selecionado no menu e chama a função 'exibir_pagina' da View correspondente, 
passando também qual operação o usuário deseja realizar.
"""
if modulo == "Recepção":
    PageRecepcao.exibir_pagina(operacao)
elif modulo == "Status":
    PageStatus.exibir_pagina(operacao)
elif modulo == "Dashboard":
    PageDashboard.exibir_pagina(operacao)
