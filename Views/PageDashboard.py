"""
INTERFACE ANALÍTICA (Dashboard)
Transforma os dados brutos do banco de dados em informações úteis para gestão.
Utiliza Pandas para cálculos estatísticos e Streamlit-Extras para o visual.
"""

import streamlit as st
import pandas as pd
import Controllers.AtendimentoController as AtendimentoController
from datetime import datetime
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.chart_container import chart_container

def exibir_pagina(operacao):
    st.header(f"Módulo: Dashboard | Operação: {operacao}")
    
    if operacao == "Visualizar KPIs":
        aba_visualizar()

def aba_visualizar():
    """
    BLOCO DE PROCESSAMENTO ANALÍTICO
    1. Busca todos os atendimentos do banco.
    2. Converte as strings de data em objetos reais de data (datetime) via Pandas.
    3. Filtra os dados com base no período selecionado pelo usuário.
    """
    st.subheader("Indicadores de Desempenho Hospitalar")
    
    dados = AtendimentoController.consultarFila()
    if not dados:
        st.warning("Ainda não há dados suficientes para gerar indicadores.")
        return
        
    df = pd.DataFrame(dados)
    
    df['Chegada'] = pd.to_datetime(df['Chegada'])
    df['Triagem'] = pd.to_datetime(df['Triagem'])
    df['Atendimento'] = pd.to_datetime(df['Atendimento'])
    
    col1, col2 = st.columns(2)
    with col1:
        data_inicio = st.date_input("Data Início", value=df['Chegada'].min().date())
    with col2:
        data_fim = st.date_input("Data Fim", value=df['Chegada'].max().date())
        
    df_filtrado = df[(df['Chegada'].dt.date >= data_inicio) & (df['Chegada'].dt.date <= data_fim)]
    
    """
    BLOCO DE CÁLCULO DE MÉTRICAS (KPIs)
    Realiza contagens e cálculos de média. O tempo de espera é calculado subtraindo
    o horário de chegada do horário de atendimento médico final.
    """
    total_pacientes = len(df_filtrado)
    atendidos = len(df_filtrado[df_filtrado['Status'] == 'Atendido'])
    na_fila = len(df_filtrado[df_filtrado['Status'] != 'Atendido'])
    
    df_atendidos = df_filtrado[df_filtrado['Status'] == 'Atendido'].copy()
    if not df_atendidos.empty:
        df_atendidos['Tempo_Espera_Total'] = (df_atendidos['Atendimento'] - df_atendidos['Chegada']).dt.total_seconds() / 60
        tempo_medio = df_atendidos['Tempo_Espera_Total'].mean()
    else:
        tempo_medio = 0
        
    """
    BLOCO VISUAL: CARDS E GRÁFICOS
    Exibe as métricas calculadas em cards estilizados e gera um gráfico de barras
    agrupando os atendimentos por dia.
    """
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(label="Total de Pacientes", value=total_pacientes)
    c2.metric(label="Atendidos", value=atendidos)
    c3.metric(label="Aguardando", value=na_fila)
    c4.metric(label="Espera Média (Min)", value=f"{tempo_medio:.1f}")
    
    style_metric_cards(
        background_color="#FFFFFF",
        border_left_color="#1f77b4",
        border_color="#e0e0e0",
        box_shadow=True
    )
    
    st.divider()
    
    with chart_container(df_filtrado):
        st.subheader("Atendimentos por Dia")
        df_filtrado['Data'] = df_filtrado['Chegada'].dt.date
        atendimentos_por_dia = df_filtrado.groupby('Data').size()
        st.bar_chart(atendimentos_por_dia)
    
    st.subheader("Dados Brutos (Filtro Aplicado)")
    st.dataframe(df_filtrado, use_container_width=True)
