import streamlit as st
import pandas as pd
from Models.Paciente import Paciente
from Models.Medico import Medico
from Models.Enfermeira import Enfermeira
import Controllers.PacienteController as PacienteController
import Controllers.MedicoController as MedicoController
import Controllers.EnfermeiraController as EnfermeiraController
import Controllers.AtendimentoController as AtendimentoController
import re

def exibir_pagina():
    st.markdown("<h1 style='color: #0f172a;'>Recepção de Pacientes</h1>", unsafe_allow_html=True)
    
    tab_pacientes, tab_medicos, tab_admin = st.tabs([
        "Cadastro", 
        "Corpo Clínico", 
        "Administração"
    ])
    
    with tab_pacientes:
        render_cadastro_paciente()
        
    with tab_medicos:
        render_cadastro_medico()
        
    with tab_admin:
        render_gestao_administrativa()

def render_cadastro_paciente():
    st.markdown("<h3 style='color: #334155; margin-bottom: 20px;'>Entrada de Pacientes</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        with st.container(border=True):
            st.markdown("<p style='font-weight: 600; color: #475569;'>Novo Registro</p>", unsafe_allow_html=True)
            with st.form("form_paciente_cad", clear_on_submit=True):
                nome = st.text_input("Nome Completo:")
                cpf = st.text_input("CPF (Apenas números):", max_chars=11)
                prioridade = st.selectbox("Nível de Prioridade:", ["Normal", "Preferencial"])
                
                if st.form_submit_button("CADASTRAR E INICIAR FLUXO", use_container_width=True):
                    cpf_limpo = re.sub(r'\D', '', cpf)
                    if nome and len(cpf_limpo) == 11:
                        p_id = PacienteController.incluirPaciente(Paciente(None, nome, cpf_limpo, prioridade))
                        if p_id:
                            AtendimentoController.registrarChegada(p_id)
                            st.toast("Paciente cadastrado", icon="✅")
                            st.rerun()
                        else: st.error("Erro: CPF já existe.")
                    else: st.warning("Dados inválidos fornecidos.")

    with col2:
        st.markdown("<p style='font-weight: 600; color: #475569;'>Admissões Recentes</p>", unsafe_allow_html=True)
        dados = PacienteController.consultarPacientes()
        if dados:
            df = pd.DataFrame(dados).head(10)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum registro encontrado.")

def render_cadastro_medico():
    st.markdown("<h3 style='color: #334155; margin-bottom: 20px;'>Registro de Médicos</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        with st.container(border=True):
            st.markdown("<p style='font-weight: 600; color: #475569;'>Novo Profissional Médico</p>", unsafe_allow_html=True)
            with st.form("form_medico_cad", clear_on_submit=True):
                nome_m = st.text_input("Nome:")
                crm = st.text_input("Número do CRM:")
                esp = st.text_input("Especialidade:")
                if st.form_submit_button("SALVAR REGISTRO", use_container_width=True):
                    if nome_m and crm and esp:
                        if MedicoController.incluirMedico(Medico(None, nome_m, crm, esp)):
                            st.toast("Médico registrado", icon="✅")
                            st.rerun()
                        else: st.error("Erro no banco de dados.")
                    else: st.warning("Todos os campos são obrigatórios.")

    with col2:
        st.markdown("<p style='font-weight: 600; color: #475569;'>Corpo Clínico Ativo</p>", unsafe_allow_html=True)
        dados_m = MedicoController.consultarMedicos()
        if dados_m:
            st.dataframe(pd.DataFrame(dados_m).head(10), use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum profissional registrado.")

def render_gestao_administrativa():
    st.markdown("<h3 style='color: #334155; margin-bottom: 20px;'>Console Administrativo</h3>", unsafe_allow_html=True)
    
    col_p, col_m, col_e = st.columns(3)
    
    with col_p:
        st.markdown("<p style='font-weight: 600; color: #1e293b;'>Gestão de Pacientes</p>", unsafe_allow_html=True)
        with st.container(border=True):
            cpf_busca = st.text_input("Buscar por CPF:", max_chars=11, key="admin_p_cpf")
            if st.button("EXECUTAR BUSCA", use_container_width=True):
                p = PacienteController.buscarPacientePorCPF(re.sub(r'\D', '', cpf_busca))
                if p: st.session_state['admin_edit_p'] = p
                else: st.error("Registro não encontrado.")

            if 'admin_edit_p' in st.session_state:
                p = st.session_state['admin_edit_p']
                with st.expander(f"Editar: {p.get_nome()}", expanded=True):
                    enome = st.text_input("Nome:", value=p.get_nome(), key="edit_p_nome")
                    eprio = st.selectbox("Prioridade:", ["Normal", "Preferencial"], 
                                        index=0 if p.get_prioridade() == "Normal" else 1, key="edit_p_prio")
                    
                    if st.button("ATUALIZAR REGISTRO", use_container_width=True, key="save_p"):
                        p.set_nome(enome)
                        p.set_prioridade(eprio)
                        if PacienteController.atualizarPaciente(p):
                            st.success("Registro atualizado")
                            del st.session_state['admin_edit_p']
                            st.rerun()
                    
                    if st.button("EXCLUIR REGISTRO", type="primary", use_container_width=True, key="del_p"):
                        if PacienteController.excluirPaciente(p.get_id()):
                            st.success("Registro removido")
                            del st.session_state['admin_edit_p']
                            st.rerun()

    with col_m:
        st.markdown("<p style='font-weight: 600; color: #1e293b;'>Gestão de Médicos</p>", unsafe_allow_html=True)
        with st.container(border=True):
            medicos = MedicoController.consultarMedicos()
            if medicos:
                m_opcoes = {f"{m['Nome']} (CRM: {m['CRM']})": m for m in medicos}
                sel_m_nome = st.selectbox("Selecionar Profissional:", list(m_opcoes.keys()), key="admin_m_sel")
                m_dados = m_opcoes[sel_m_nome]
                
                with st.expander(f"Editar: {m_dados['Nome']}", expanded=True):
                    enome_m = st.text_input("Nome:", value=m_dados['Nome'], key="edit_m_nome")
                    ecrm = st.text_input("CRM:", value=m_dados['CRM'], key="edit_m_crm")
                    eesp = st.text_input("Especialidade:", value=m_dados['Especialidade'], key="edit_m_esp")
                    
                    if st.button("ATUALIZAR MÉDICO", use_container_width=True, key="btn_save_m"):
                        med_obj = Medico(m_dados['ID'], enome_m, ecrm, eesp)
                        if MedicoController.atualizarMedico(med_obj):
                            st.success("Médico atualizado")
                            st.rerun()
                    
                    if st.button("EXCLUIR MÉDICO", type="primary", use_container_width=True, key="btn_del_m"):
                        if MedicoController.excluirMedico(m_dados['ID']):
                            st.success("Médico removido")
                            st.rerun()
            else: st.info("Sem registros médicos.")

    with col_e:
        st.markdown("<p style='font-weight: 600; color: #1e293b;'>Gestão de Enfermagem</p>", unsafe_allow_html=True)
        with st.container(border=True):
            with st.form("form_enf_cad", clear_on_submit=True):
                ne = st.text_input("Nome:")
                ce = st.text_input("Registro (COREN):")
                if st.form_submit_button("CADASTRAR ENFERMEIRA", use_container_width=True):
                    if ne and ce:
                        if EnfermeiraController.incluirEnfermeira(Enfermeira(None, ne, ce)):
                            st.toast("Enfermeira registrada")
                            st.rerun()
            
            st.divider()
            enfs = EnfermeiraController.consultarEnfermeiras()
            if enfs:
                st.dataframe(pd.DataFrame(enfs), use_container_width=True, hide_index=True)
                id_del_e = st.number_input("ID para remover:", min_value=1, step=1, key="del_enf_id")
                if st.button("REMOVER ENFERMEIRA", type="primary", use_container_width=True):
                    if EnfermeiraController.excluirEnfermeira(id_del_e):
                        st.rerun()
            else: st.info("Sem equipe de enfermagem.")
