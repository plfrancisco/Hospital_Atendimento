import streamlit as st
import pandas as pd
from Models.Leito import Leito
from Models.Internacao import Internacao
import Controllers.LeitoController as LeitoController
import Controllers.InternacaoController as InternacaoController
import Controllers.PacienteController as PacienteController
import Controllers.EnfermeiraController as EnfermeiraController
import Controllers.DiarioController as DiarioController
from datetime import datetime

def exibir_pagina():
    st.markdown("<h1 style='color: #0f172a;'>Gestão de Internação</h1>", unsafe_allow_html=True)
    
    # CSS para Cards de Leitos Profissionais
    st.markdown("""
        <style>
        .leito-card {
            background-color: white;
            padding: 16px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            border-top: 4px solid #94a3b8;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            margin-bottom: 16px;
            min-height: 160px;
        }
        .leito-disponível { border-top-color: #10b981; }
        .leito-ocupado { border-top-color: #ef4444; }
        .leito-manutenção { border-top-color: #f59e0b; }
        
        .leito-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        .leito-id { font-size: 18px; font-weight: 700; color: #1e293b; }
        .leito-tag { font-size: 10px; font-weight: 700; color: #64748b; background: #f8fafc; padding: 2px 6px; border-radius: 4px; border: 1px solid #e2e8f0; }
        .p-name { font-size: 14px; font-weight: 600; color: #334155; margin-top: 4px; }
        .p-meta { font-size: 11px; color: #94a3b8; }
        </style>
    """, unsafe_allow_html=True)

    tab_visão, tab_internar, tab_admin = st.tabs([
        "Mapa de Unidades", 
        "Admissão",
        "Configurações"
    ])
    
    with tab_visão:
        render_painel_cards()
        
    with tab_internar:
        render_fluxo_internacao()
        
    with tab_admin:
        render_admin_leitos()

def render_painel_cards():
    leitos = LeitoController.consultarLeitos()
    internacoes = InternacaoController.consultarInternacoes()
    internados_ativos = {i['Leito']: i for i in internacoes if i['Saida'] is None}
    
    if not leitos:
        st.info("Nenhuma unidade cadastrada.")
        return

    # --- MODAIS DE AÇÃO ---
    if 'view_diario' in st.session_state:
        int_sel = st.session_state['view_diario']
        with st.container(border=True):
            st.markdown(f"<h3 style='font-size: 18px;'>Diário Clínico: {int_sel['Paciente']}</h3>", unsafe_allow_html=True)
            col_d1, col_d2 = st.columns([1.2, 1])
            with col_d1:
                st.markdown("<p style='font-size: 12px; font-weight: 600; color: #64748b;'>HISTÓRICO DE ENTRADAS</p>", unsafe_allow_html=True)
                registros = DiarioController.consultarDiario(int_sel['ID'])
                if registros:
                    for r in registros:
                        st.markdown(f"""
                            <div style='background: #f8fafc; padding: 10px; border-radius: 6px; margin-bottom: 8px; border-left: 2px solid #1e40af;'>
                                <span style='font-size: 11px; color: #94a3b8;'>{r['Data']} | {r['Enfermeira']}</span><br>
                                <span style='font-size: 13px; color: #334155;'>{r['Observacao']}</span>
                            </div>
                        """, unsafe_allow_html=True)
                else: st.write("Nenhum registro encontrado.")
            
            with col_d2:
                st.markdown("<p style='font-size: 12px; font-weight: 600; color: #64748b;'>NOVA EVOLUÇÃO CLÍNICA</p>", unsafe_allow_html=True)
                enfermeiras = EnfermeiraController.consultarEnfermeiras()
                if enfermeiras:
                    enf_opcoes = {e['Nome']: e['ID'] for e in enfermeiras}
                    sel_enf = st.selectbox("Equipe de Enfermagem:", list(enf_opcoes.keys()), key="enf_diario")
                    obs = st.text_area("Notas Clínicas:", key="obs_diario")
                    if st.button("SALVAR REGISTRO", use_container_width=True, type="primary"):
                        if obs:
                            if DiarioController.registrarObservacao(int_sel['ID'], enf_opcoes[sel_enf], obs):
                                st.rerun()
                else: st.warning("Registro de enfermagem necessário.")
            
            if st.button("FECHAR DIÁRIO", use_container_width=True):
                del st.session_state['view_diario']
                st.rerun()
        st.divider()

    if 'confirm_alta' in st.session_state:
        int_sel = st.session_state['confirm_alta']
        with st.status(f"Confirmando Alta: {int_sel['Paciente']}", expanded=True):
            st.markdown(f"<p style='font-size: 13px;'>Finalizando estadia no Leito {int_sel['Leito']}. O recurso será marcado como disponível.</p>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            if c1.button("CONFIRMAR ALTA HOSPITALAR", type="primary", use_container_width=True):
                leitos_all = LeitoController.consultarLeitos()
                l_id = next((l['ID'] for l in leitos_all if l['Numero'] == int_sel['Leito']), None)
                if InternacaoController.registrarAlta(int_sel['ID'], l_id):
                    del st.session_state['confirm_alta']
                    st.rerun()
            if c2.button("CANCELAR", use_container_width=True):
                del st.session_state['confirm_alta']
                st.rerun()
        st.divider()

    # --- FILTROS E GRID ---
    cols_filtros = st.columns(4)
    status_filtro = cols_filtros[0].multiselect("Filtrar por Status:", ["Livre", "Ocupado", "Manutenção"], default=["Livre", "Ocupado", "Manutenção"])
    
    leitos_filtrados = [l for l in leitos if l['Status'] in status_filtro]
    
    cols = st.columns(4)
    for idx, l in enumerate(leitos_filtrados):
        col_idx = idx % 4
        with cols[col_idx]:
            # Mapeamento para CSS sem acentos nas classes
            status_map_css = {"Livre": "disponível", "Ocupado": "ocupado", "Manutenção": "manutenção"}
            status_class = f"leito-{status_map_css.get(l['Status'], 'disponível')}"
            int_data = internados_ativos.get(l['Numero'])
            
            entrada_html = f"<div class='p-meta'>ENTRADA: {int_data['Entrada']}</div>" if int_data else ""
            
            st.markdown(f"""
                <div class="leito-card {status_class}">
                    <div class="leito-header">
                        <span class="leito-id">L-{l['Numero']}</span>
                        <span class="leito-tag">{l['Tipo']}</span>
                    </div>
                    <div style="font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; margin-bottom: 8px;">
                        {l['Status']}
                    </div>
                    <div class="p-name">
                        {int_data['Paciente'] if int_data else "VAGO"}
                    </div>
                    {entrada_html}
                </div>
            """, unsafe_allow_html=True)
            
            if l['Status'] == 'Ocupado' and int_data:
                c1, c2 = st.columns(2)
                if c1.button("DIÁRIO", key=f"btn_diario_{l['ID']}", use_container_width=True):
                    st.session_state['view_diario'] = int_data
                    st.rerun()
                if c2.button("ALTA", key=f"btn_alta_{l['ID']}", use_container_width=True):
                    st.session_state['confirm_alta'] = int_data
                    st.rerun()

def render_fluxo_internacao():
    st.markdown("<h3 style='color: #334155;'>Protocolo de Admissão</h3>", unsafe_allow_html=True)
    with st.container(border=True):
        pacientes = PacienteController.consultarPacientes()
        leitos_livres = [l for l in LeitoController.consultarLeitos() if l['Status'] == 'Livre']
        
        if pacientes and leitos_livres:
            with st.form("form_interna_nova", clear_on_submit=True):
                p_opcoes = {p['Nome']: p['ID'] for p in pacientes}
                l_opcoes = {f"LEITO {l['Numero']} - {l['Tipo']}": l['ID'] for l in leitos_livres}
                col1, col2 = st.columns(2)
                sel_p = col1.selectbox("Paciente:", list(p_opcoes.keys()))
                sel_l = col2.selectbox("Recurso Disponível:", list(l_opcoes.keys()))
                motivo = st.text_area("Contexto da Internação:")
                if st.form_submit_button("AUTORIZAR ADMISSÃO", use_container_width=True, type="primary"):
                    i = Internacao(None, p_opcoes[sel_p], l_opcoes[sel_l], datetime.now().strftime("%Y-%m-%d %H:%M:%S"), None, motivo)
                    if InternacaoController.registrarInternacao(i):
                        st.rerun()
        else:
            st.warning("Recursos insuficientes: Nenhum leito livre ou paciente cadastrado.")

def render_admin_leitos():
    st.markdown("<h3 style='color: #334155;'>Configurações da Unidade</h3>", unsafe_allow_html=True)
    col_cad, col_edit = st.columns([1, 1])
    
    with col_cad:
        with st.container(border=True):
            st.markdown("<p style='font-weight: 600;'>Novo Recurso</p>", unsafe_allow_html=True)
            with st.form("form_leito_novo", clear_on_submit=True):
                num = st.text_input("ID/Número do Leito:")
                tipo = st.selectbox("Tipo de Recurso:", ["Enfermaria", "UTI", "Pediatria", "Isolamento"])
                if st.form_submit_button("ADICIONAR AO INVENTÁRIO", use_container_width=True):
                    if num:
                        if LeitoController.incluirLeito(Leito(None, num, tipo, "Livre")):
                            st.rerun()
    with col_edit:
        with st.container(border=True):
            st.markdown("<p style='font-weight: 600;'>Parâmetros do Recurso</p>", unsafe_allow_html=True)
            leitos = LeitoController.consultarLeitos()
            if leitos:
                l_opcoes = {f"LEITO {l['Numero']}": l for l in leitos}
                sel_l_nome = st.selectbox("Selecionar Leito:", list(l_opcoes.keys()))
                l_dados = l_opcoes[sel_l_nome]
                
                with st.expander("Atualizar Parâmetros", expanded=True):
                    enum = st.text_input("Número:", value=l_dados['Numero'])
                    estatus = st.selectbox("Status Operacional:", ["Livre", "Ocupado", "Manutenção"],
                                        index=["Livre", "Ocupado", "Manutenção"].index(l_dados['Status']))
                    if st.button("ATUALIZAR CONFIGURAÇÕES", use_container_width=True):
                        if LeitoController.atualizarLeito(Leito(l_dados['ID'], enum, l_dados['Tipo'], estatus)):
                            st.rerun()
            else: st.info("Nenhum registro encontrado.")
