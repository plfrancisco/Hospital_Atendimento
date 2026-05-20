import streamlit as st
import Controllers.AtendimentoController as AtendimentoController
import Controllers.MedicoController as MedicoController
import Controllers.EnfermeiraController as EnfermeiraController

def exibir_pagina():
    st.markdown("<h1 style='color: #0f172a;'>Triagem Clínica</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 14px; margin-bottom: 24px;'>Avaliação do paciente e controle de encaminhamento médico.</p>", unsafe_allow_html=True)

    # 1. Obter pacientes aguardando triagem
    fila = AtendimentoController.consultarFila(status_filtro="Aguardando Triagem")
    
    if not fila:
        st.info("Nenhum paciente aguardando triagem no momento.")
        return

    # 2. Seleção de Paciente
    col_p, _ = st.columns([1, 1])
    with col_p:
        pacientes_nomes = {f"{p['Paciente']} (Ref: {p['ID']})": p for p in fila}
        selecao = st.selectbox("Selecionar Paciente para Avaliação:", list(pacientes_nomes.keys()))
        p_selecionado = pacientes_nomes[selecao]

    st.divider()

    # 3. Formulário de Triagem
    with st.form("form_triagem", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<p style='font-weight: 600; color: #1e293b;'>Observações Clínicas</p>", unsafe_allow_html=True)
            sintomas = st.text_area("Sintomas Relatados:", placeholder="ex: Cefaleia, febre, náusea...")
            sinais_vitais = st.text_area("Sinais Vitais:", placeholder="ex: PA: 120/80 mmHg, FC: 80 bpm, Temp: 36.5°C")

        with col2:
            st.markdown("<p style='font-weight: 600; color: #1e293b;'>Encaminhamento Médico</p>", unsafe_allow_html=True)
            
            # Rodízio Automático de Enfermagem
            enf_id_auto = AtendimentoController.obterProximaEnfermeiraRodizio()
            enfermeiras = EnfermeiraController.consultarEnfermeiras()
            enf_nome_auto = next((e['Nome'] for e in enfermeiras if e['ID'] == enf_id_auto), "Nenhum profissional disponível")
            
            st.markdown(f"""
                <div style='background-color: #f8fafc; padding: 12px; border-radius: 6px; border: 1px solid #e2e8f0; margin-bottom: 16px;'>
                    <span style='color: #64748b; font-size: 12px; font-weight: 600;'>ENFERMEIRA ATRIBUÍDA</span><br>
                    <span style='color: #1e40af; font-weight: 700;'>{enf_nome_auto}</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Seleção de Especialidade/Médico
            medicos = MedicoController.consultarMedicos()
            if medicos:
                esp_medicos = {}
                for m in medicos:
                    esp = m['Especialidade']
                    if esp not in esp_medicos: esp_medicos[esp] = []
                    esp_medicos[esp].append(m)
                
                especialidade = st.selectbox("Especialidade Necessária:", list(esp_medicos.keys()))
                medicos_da_esp = {m['Nome']: m['ID'] for m in esp_medicos[especialidade]}
                medico_nome = st.selectbox("Médico Atribuído:", list(medicos_da_esp.keys()))
                medico_id = medicos_da_esp[medico_nome]
            else:
                st.error("Nenhum médico encontrado no sistema.")
                st.stop()

        if st.form_submit_button("FINALIZAR AVALIAÇÃO E ENCAMINHAR", use_container_width=True, type="primary"):
            if enf_id_auto:
                AtendimentoController.finalizarTriagem(
                    p_selecionado['ID'], 
                    enf_id_auto, 
                    sintomas, 
                    sinais_vitais, 
                    medico_id
                )
                st.toast(f"Triagem concluída para {p_selecionado['Paciente']}", icon="✅")
                st.rerun()
            else:
                st.error("Erro: O sistema falhou ao atribuir um profissional de enfermagem.")
