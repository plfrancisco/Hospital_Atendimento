import streamlit as st
import pandas as pd
import Controllers.AtendimentoController as AtendimentoController
import Controllers.LeitoController as LeitoController
from datetime import datetime

def exibir_pagina():
    st.title("📊 Painel de Indicadores e Performance")
    
    # 1. FILTROS GLOBAIS (Barra Lateral ou Topo)
    with st.expander("🔍 Filtros de Período", expanded=False):
        col_f1, col_f2 = st.columns(2)
        data_inicio = col_f1.date_input("Data Início:", value=datetime(datetime.now().year, 1, 1))
        data_fim = col_f2.date_input("Data Fim:", value=datetime.now())

    # Busca dados base
    atendimentos_raw = AtendimentoController.consultarFila()
    leitos_raw = LeitoController.consultarLeitos()
    
    if not atendimentos_raw:
        st.info("Nenhum dado de atendimento disponível para análise.")
        return

    # Transformação de Dados com Pandas para facilidade de KPI
    df = pd.DataFrame(atendimentos_raw)
    
    # Converter colunas de data para datetime
    df['Chegada_DT'] = pd.to_datetime(df['Chegada'], errors='coerce')
    
    # Aplicar Filtro de Data
    df_filtrado = df[(df['Chegada_DT'].dt.date >= data_inicio) & (df['Chegada_DT'].dt.date <= data_fim)]

    # --- SEÇÃO 1: MÉTRICAS OPERACIONAIS ---
    st.subheader("Métricas Operacionais")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.metric("Total Admissões", len(df_filtrado))
    with c2:
        st.metric("Aguardando Triagem", len(df_filtrado[df_filtrado['Status'] == 'Aguardando Triagem']))
    with c3:
        st.metric("Em Atendimento", len(df_filtrado[df_filtrado['Status'] == 'Aguardando Atendimento']))
    with c4:
        st.metric("Altas Concluídas", len(df_filtrado[df_filtrado['Status'] == 'Atendido']))

    st.divider()

    # --- SEÇÃO 2: PERFORMANCE CLÍNICA (MÉDICOS E ENFERMEIRAS) ---
    st.subheader("Performance da Equipe Clínica")
    col_med, col_enf = st.columns(2)
    
    with col_med:
        st.markdown("**Pacientes Atendidos por Médico**")
        # Filtrar apenas atendimentos finalizados para contar produtividade real
        df_med = df_filtrado[df_filtrado['Médico'] != 'Pendente']
        if not df_med.empty:
            med_counts = df_med['Médico'].value_counts().reset_index()
            med_counts.columns = ['Médico', 'Atendimentos']
            st.bar_chart(med_counts.set_index('Médico'), color="#1e40af")
        else:
            st.caption("Nenhum atendimento médico finalizado no período.")

    with col_enf:
        st.markdown("**Triagens Realizadas por Enfermeira**")
        # Filtrar apenas quem passou pela triagem
        df_enf = df_filtrado[df_filtrado['Enfermeira'] != 'Pendente']
        if not df_enf.empty:
            enf_counts = df_enf['Enfermeira'].value_counts().reset_index()
            enf_counts.columns = ['Enfermeira', 'Triagens']
            st.bar_chart(enf_counts.set_index('Enfermeira'), color="#28a745")
        else:
            st.caption("Nenhuma triagem realizada no período.")

    st.divider()

    # --- SEÇÃO 3: OCUPAÇÃO DE LEITOS ---
    st.subheader("Gestão de Recursos (Leitos)")
    if leitos_raw:
        df_leitos = pd.DataFrame(leitos_raw)
        total_leitos = len(df_leitos)
        ocupados = len(df_leitos[df_leitos['Status'] == 'Ocupado'])
        livres = len(df_leitos[df_leitos['Status'] == 'Livre'])
        manutencao = len(df_leitos[df_leitos['Status'] == 'Manutenção'])
        
        taxa_ocupacao = (ocupados / total_leitos) * 100 if total_leitos > 0 else 0
        
        c_l1, c_l2, c_l3, c_l4 = st.columns(4)
        c_l1.metric("Capacidade Total", total_leitos)
        c_l2.metric("Ocupados", ocupados, delta=f"{taxa_ocupacao:.1f}% Taxa", delta_color="inverse" if taxa_ocupacao > 80 else "normal")
        c_l3.metric("Disponíveis", livres)
        c_l4.metric("Em Manutenção", manutencao)
        
        # Gráfico de Rosca para Ocupação
        st.markdown("**Distribuição de Ocupação**")
        leito_status_dist = df_leitos['Status'].value_counts()
        st.bar_chart(leito_status_dist, color="#ffc107") # Usando bar_chart por simplicidade visual
    else:
        st.info("Nenhum leito cadastrado.")

    st.divider()

    # --- SEÇÃO 4: DETALHAMENTO ---
    if st.checkbox("Exibir Log Operacional Detalhado"):
        st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
