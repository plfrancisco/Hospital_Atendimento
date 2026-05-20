import streamlit as st
import pandas as pd
import Controllers.AtendimentoController as AtendimentoController
import Controllers.ConsultaController as ConsultaController
import Controllers.PacienteController as PacienteController
import Controllers.MedicoController as MedicoController
from Models.Consulta import Consulta

def exibir_pagina():
    st.markdown("<h1 style='color: #0f172a;'>Operações Clínicas</h1>", unsafe_allow_html=True)
    
    tab_fila, tab_agendas = st.tabs(["Fila Ativa", "Agendamentos"])
    
    with tab_fila:
        render_fila()
        
    with tab_agendas:
        render_agendas()

def render_fila():
    st.markdown("<h3 style='color: #334155; margin-bottom: 20px;'>Gestão da Fila de Espera</h3>", unsafe_allow_html=True)
    
    # CSS para Cards da Fila (Azul Profissional)
    st.markdown("""
        <style>
        .queue-card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #cbd5e1;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 16px;
        }
        .q-prio-high { border-left-color: #e11d48; }
        .q-prio-std { border-left-color: #1e40af; }
        
        .q-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 12px;
        }
        .q-status {
            font-size: 10px;
            font-weight: 700;
            background-color: #f1f5f9;
            color: #475569;
            padding: 2px 8px;
            border-radius: 4px;
            text-transform: uppercase;
        }
        .q-name { font-size: 16px; font-weight: 700; color: #1e293b; }
        .q-meta { font-size: 12px; color: #64748b; }
        </style>
    """, unsafe_allow_html=True)

    dados_all = AtendimentoController.consultarFila()
    dados_fila = [p for p in dados_all if p['Status'] != 'Atendido']
    
    if dados_fila:
        medicos = MedicoController.consultarMedicos()
        med_opcoes = {f"{m['Nome']} ({m['Especialidade']})": m['ID'] for m in medicos}

        for p in dados_fila:
            prio_class = "q-prio-high" if p['Prioridade'] in ["Preferencial", "High Priority"] else "q-prio-std"
            
            with st.container():
                st.markdown(f"""
                    <div class="queue-card {prio_class}">
                        <div class="q-header">
                            <div>
                                <div class="q-name">{p['Paciente']}</div>
                                <div class="q-meta">REF: {p['ID']} | CHEGADA: {p['Chegada']}</div>
                            </div>
                            <div class="q-status">{p['Status']}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                col_info, col_acao = st.columns([1, 1])
                
                with col_info:
                    if p['Status'] == "Aguardando Atendimento":
                        st.markdown(f"**Despacho Clínico**")
                        st.markdown(f"<span style='font-size: 13px; color: #475569;'>Médico Atribuído: Dr(a). {p['Médico']}</span>", unsafe_allow_html=True)
                        with st.expander("Notas de Triagem"):
                            st.markdown(f"<p style='font-size: 12px;'><b>Sintomas:</b> {p['Sintomas']}<br><b>Sinais Vitais:</b> {p['Sinais Vitais']}</p>", unsafe_allow_html=True)

                with col_acao:
                    if p['Status'] == "Aguardando Triagem":
                        st.info("Aguardando avaliação clínica no módulo de Triagem.")
                    
                    elif p['Status'] == "Aguardando Atendimento":
                        if st.button("FINALIZAR CONSULTA", key=f"btn_med_{p['ID']}", use_container_width=True, type="primary"):
                            m_id = None
                            for m in medicos:
                                if m['Nome'] == p['Médico']:
                                    m_id = m['ID']
                                    break
                            
                            if AtendimentoController.finalizarAtendimento(p['ID'], m_id):
                                st.toast("Consulta finalizada", icon="✅")
                                st.rerun()
    else:
        st.info("A fila de espera está vazia no momento.")

def render_agendas():
    st.markdown("<h3 style='color: #334155; margin-bottom: 20px;'>Agendamentos da Clínica</h3>", unsafe_allow_html=True)
    
    col_cad, col_list = st.columns([1, 1.5])
    
    with col_cad:
        with st.container(border=True):
            st.markdown("<p style='font-weight: 600; color: #475569;'>Novo Agendamento</p>", unsafe_allow_html=True)
            pacientes = PacienteController.consultarPacientes()
            medicos = MedicoController.consultarMedicos()
            
            if pacientes and medicos:
                with st.form("form_consulta_nova", clear_on_submit=True):
                    p_opcoes = {p['Nome']: p['ID'] for p in pacientes}
                    m_opcoes = {f"{m['Nome']} ({m['Especialidade']})": m['ID'] for m in medicos}
                    
                    sel_p = st.selectbox("Paciente:", list(p_opcoes.keys()))
                    sel_m = st.selectbox("Profissional:", list(m_opcoes.keys()))
                    
                    c1, c2 = st.columns(2)
                    data = c1.date_input("Data:")
                    hora = c2.time_input("Hora:")
                    
                    obs = st.text_area("Observações Clínicas:", placeholder="Motivo da consulta...")
                    
                    if st.form_submit_button("CONFIRMAR AGENDAMENTO", use_container_width=True):
                        c = Consulta(None, p_opcoes[sel_p], m_opcoes[sel_m], f"{data} {hora}", "Agendado", obs)
                        if ConsultaController.agendarConsulta(c):
                            st.toast("Consulta agendada")
                            st.rerun()
            else:
                st.warning("Pré-requisitos: Pacientes e Médicos devem estar cadastrados.")

    with col_list:
        consultas = ConsultaController.consultarConsultas()
        if consultas:
            df = pd.DataFrame(consultas)
            st.dataframe(df[["ID", "Paciente", "Medico", "Data/Hora", "Status"]], use_container_width=True, hide_index=True)
            
            sel_cancel = st.selectbox("ID do Agendamento para Cancelar:", [c['ID'] for c in consultas], key="cancel_sel")
            if st.button("EXECUTAR CANCELAMENTO", type="primary"):
                if ConsultaController.cancelarConsulta(sel_cancel):
                    st.rerun()
        else:
            st.info("Nenhum agendamento encontrado.")
