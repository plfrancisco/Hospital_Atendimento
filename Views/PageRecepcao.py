"""
INTERFACE DE RECEPÇÃO
Gerencia a porta de entrada do hospital: cadastro de novos pacientes,
listagem geral e remoção de registros.
"""

import streamlit as st
import pandas as pd
from Models.Paciente import Paciente
import Controllers.PacienteController as PacienteController
import Controllers.AtendimentoController as AtendimentoController

def exibir_pagina(operacao):
    st.header(f"Módulo: Recepção | Operação: {operacao}")
    
    if operacao == "Cadastrar Paciente":
        aba_cadastrar()
    elif operacao == "Consultar Pacientes":
        aba_consultar()
    elif operacao == "Excluir Paciente":
        aba_excluir()

def aba_cadastrar():
    """
    BLOCO DE CADASTRO
    Coleta dados via formulário Streamlit. Ao salvar, ele realiza duas ações:
    1. Salva o Paciente (dados fixos como nome/CPF).
    2. Registra um novo Atendimento (dados de fluxo) vinculado a esse paciente.
    """
    st.subheader("Cadastro de Novo Paciente")
    nome = st.text_input("Nome Completo:")
    cpf = st.text_input("CPF (Somente números):")
    prioridade = st.selectbox("Prioridade:", ["Normal", "Preferencial"])
    
    if st.button("Cadastrar e Registrar Entrada"):
        if nome and cpf:
            novo_paciente = Paciente(None, nome, cpf, prioridade)
            paciente_id = PacienteController.incluirPaciente(novo_paciente)
            if paciente_id:
                AtendimentoController.registrarChegada(paciente_id)
                st.success(f"Paciente {nome} cadastrado e adicionado à fila de Triagem!")
            else:
                st.error("Erro ao cadastrar paciente. Verifique se o CPF já existe.")
        else:
            st.warning("Preencha todos os campos obrigatórios.")

def aba_consultar():
    """
    BLOCO DE CONSULTA
    Recupera a lista de todos os pacientes do banco de dados e exibe
    formatada em uma tabela usando um DataFrame do Pandas.
    """
    st.subheader("Lista de Pacientes Cadastrados")
    if st.button("Atualizar Lista"):
        dados = PacienteController.consultarPacientes()
        if dados:
            st.table(pd.DataFrame(dados))
        else:
            st.info("Nenhum paciente cadastrado.")

def aba_excluir():
    """
    BLOCO DE EXCLUSÃO (SEGURANÇA)
    Implementa um fluxo de busca seguido de confirmação.
    Usa o 'session_state' para lembrar qual paciente foi encontrado entre
    uma interação e outra da página.
    """
    st.subheader("Excluir Cadastro de Paciente")
    cpf_busca = st.text_input("Digite o CPF do paciente para excluir:")
    
    if st.button("Buscar Paciente"):
        paciente = PacienteController.buscarPacientePorCPF(cpf_busca)
        if paciente:
            st.session_state['paciente_excluir'] = paciente
        else:
            st.error("Paciente não encontrado.")
            st.session_state['paciente_excluir'] = None

    if 'paciente_excluir' in st.session_state and st.session_state['paciente_excluir']:
        p = st.session_state['paciente_excluir']
        st.warning(f"Confirma a exclusão do paciente: **{p.get_nome()}** (CPF: {p.get_cpf()})?")
        st.info("Nota: Isso removerá todo o histórico de atendimentos deste paciente.")
        
        if st.button("Confirmar Exclusão Definitiva"):
            if PacienteController.excluirPaciente(p.get_id()):
                st.success("Paciente e atendimentos removidos com sucesso!")
                st.session_state['paciente_excluir'] = None
                st.rerun()
            else:
                st.error("Erro ao realizar a exclusão no banco de dados.")
