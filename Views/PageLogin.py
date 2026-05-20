# =================================================================
# VIEW: PageLogin
# Responsabilidade: Interface de Autenticação (Hospital Sofia Edition)
# =================================================================

import streamlit as st
import Controllers.UsuarioController as UsuarioController

def exibir_pagina():
    # 1. INJEÇÃO DE CSS REFINADO (Estética Sofia Edition - Baseada no Estoque)
    st.markdown("""
        <style>
        /* Ocultar elementos padrão do Streamlit no Login */
        [data-testid="stHeader"], [data-testid="stFooter"] {
            display: none !important;
        }

        /* Fundo Harmonizado com o Sistema */
        .stApp {
            background-color: #f1f5f9 !important;
        }

        /* Container do Formulário (Glassmorphism para Fundo Claro) */
        [data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.8) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-radius: 30px !important;
            border: 1px solid rgba(226, 232, 240, 0.8) !important;
            padding: 50px !important;
            box-shadow: 
                0 10px 25px -5px rgba(0, 0, 0, 0.05),
                0 8px 10px -6px rgba(0, 0, 0, 0.05) !important;
            max-width: 450px !important;
            margin: 100px auto !important;
            animation: card-entrance 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        @keyframes card-entrance {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Cabeçalho do Card */
        .login-title {
            color: #1e40af;
            font-weight: 800;
            font-size: 2.2rem;
            letter-spacing: -1.5px;
            margin-bottom: 5px;
            text-align: center;
        }
        .login-subtitle {
            color: #64748b;
            font-size: 0.95rem;
            font-weight: 500;
            margin-bottom: 40px;
            text-align: center;
        }

        /* Inputs Customizados */
        div[data-testid="stForm"] .stTextInput input {
            border-radius: 12px !important;
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            padding: 14px 18px !important;
            color: #0f172a !important;
            transition: all 0.3s ease !important;
        }
        div[data-testid="stForm"] .stTextInput input:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        }

        /* Botão de Entrada (Azul Corporativo do Sistema) */
        div[data-testid="stForm"] .stButton button {
            border-radius: 12px !important;
            padding: 14px 24px !important;
            font-weight: 600 !important;
            background-color: #1e40af !important;
            border: none !important;
            color: white !important;
            margin-top: 20px !important;
            transition: all 0.2s ease !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 0.8rem;
        }
        div[data-testid="stForm"] .stButton button:hover {
            background-color: #1e3a8a !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(30, 64, 175, 0.2) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. ESTRUTURA DE CONTEÚDO
    with st.form("login_portal"):
        st.markdown("<div class='login-title'>NÚCLEO.</div>", unsafe_allow_html=True)
        st.markdown("<div class='login-subtitle'>Terminal de Gestão Hospitalar</div>", unsafe_allow_html=True)
        
        st.markdown("<p style='color: #64748b; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;'>Identidade</p>", unsafe_allow_html=True)
        user = st.text_input("Usuário", placeholder="ID do Profissional", label_visibility="collapsed")
        
        st.write("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        
        st.markdown("<p style='color: #64748b; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;'>Segurança</p>", unsafe_allow_html=True)
        pwd = st.text_input("Senha", type="password", placeholder="••••••••", label_visibility="collapsed")
        
        st.write("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        
        if st.form_submit_button("AUTENTICAR ACESSO", use_container_width=True):
            usuario_validado = UsuarioController.autenticar_usuario(user, pwd)
            if usuario_validado:
                st.session_state.autenticado = True
                st.session_state.usuario_nome = usuario_validado.get_login()
                st.rerun()
            else:
                st.error("Credenciais inválidas ou acesso negado.")

    # Footer
    st.markdown("""
        <div style='text-align: center; margin-top: 30px; opacity: 0.5;'>
            <p style='color: #475569; font-size: 0.7rem; font-weight: 500; letter-spacing: 1px;'>
                HEALTH SECURE GATEWAY &middot; V3.5.0 CORPORATE
            </p>
        </div>
    """, unsafe_allow_html=True)
