"""
INTERFACE DE OPERAÇÕES (Status)
Este arquivo gerencia a interação do profissional de saúde com o fluxo do paciente.
Ele utiliza 'Cards' em vez de tabelas para uma visualização mais limpa e intuitiva.
"""

import streamlit as st
import pandas as pd
import Controllers.AtendimentoController as AtendimentoController

def exibir_pagina(operacao):
    st.header("Central de Status - Gestão de Fluxo")
    
    """
    BLOCO DE INDICADOR DE OCUPAÇÃO
    Calcula e exibe uma barra de progresso baseada no volume de pacientes que 
    ainda não foram finalizados (status diferente de 'Atendido').
    """
    dados_totais = AtendimentoController.consultarFila()
    if dados_totais:
        em_espera = len([a for a in dados_totais if a['Status'] != "Atendido"])
        capacidade_maxima = 100 
        percentual = min(em_espera / capacidade_maxima, 1.0)
        
        st.write(f"**Ocupação Atual da Clínica:** {em_espera} pacientes em fluxo")
        st.progress(percentual)
        if percentual > 0.8:
            st.warning("⚠️ Capacidade próxima ao limite!")
    
    tab1, tab2 = st.tabs(["🩺 Realizar Triagem", "👨‍⚕️ Iniciar Atendimento Médico"])
    
    """
    BLOCO DE TRIAGEM (TAB 1)
    Busca pacientes com status 'Aguardando Triagem' e os exibe em Cards.
    Cada card contém as informações do paciente e um botão que, ao ser clicado,
    dispara a lógica do Controller para atualizar o status no banco de dados.
    """
    with tab1:
        st.subheader("Pacientes Aguardando Triagem")
        dados_triagem = AtendimentoController.consultarFila(status_filtro="Aguardando Triagem")
        if dados_triagem:
            for i in range(0, len(dados_triagem), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(dados_triagem):
                        row = dados_triagem[i + j]
                        with cols[j]:
                            cor_prioridade = "#dc3545" if row['Prioridade'] == "Preferencial" else "#007BFF"
                            with st.container(border=True):
                                st.markdown(f"**{row['Paciente']}**")
                                st.caption(f"🆔 Atendimento: {row['Atendimento_ID']} | 🕒 Chegada: {row['Chegada']}")
                                st.markdown(f"<span style='color:{cor_prioridade}; font-weight:bold;'>● {row['Prioridade']}</span>", unsafe_allow_html=True)
                                
                                if st.button(f"Finalizar Triagem", key=f"btn_tri_{row['Atendimento_ID']}", use_container_width=True, type="primary"):
                                    AtendimentoController.finalizarTriagem(row['Atendimento_ID'])
                                    st.toast(f"✅ Triagem finalizada para {row['Paciente']}!", icon="🩺")
                                    st.rerun()
        else:
            st.info("Nenhum paciente aguardando triagem.")

    """
    BLOCO DE ATENDIMENTO MÉDICO (TAB 2)
    Similar ao bloco de triagem, mas focado em pacientes que já passaram pela enfermaria
    e agora aguardam o médico. A finalização aqui move o paciente para o status 'Atendido'.
    """
    with tab2:
        st.subheader("Pacientes Aguardando Médico")
        dados_medico = AtendimentoController.consultarFila(status_filtro="Aguardando Atendimento")
        if dados_medico:
            for i in range(0, len(dados_medico), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(dados_medico):
                        row = dados_medico[i + j]
                        with cols[j]:
                            with st.container(border=True):
                                st.markdown(f"**{row['Paciente']}**")
                                st.caption(f"🆔 Atendimento: {row['Atendimento_ID']} | 🩺 Triado em: {row['Triagem']}")
                                st.markdown(f"<span style='color:#28a745; font-weight:bold;'>● Aguardando Consulta</span>", unsafe_allow_html=True)
                                
                                if st.button(f"Finalizar Consulta", key=f"btn_med_{row['Atendimento_ID']}", use_container_width=True, type="primary"):
                                    AtendimentoController.finalizarAtendimento(row['Atendimento_ID'])
                                    st.toast(f"🎉 Atendimento concluído para {row['Paciente']}!", icon="👨‍⚕️")
                                    st.rerun()
        else:
            st.info("Nenhum paciente aguardando atendimento médico.")
