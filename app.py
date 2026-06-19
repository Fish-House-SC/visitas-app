# app.py - Versão para Streamlit Cloud
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Sistema de Visitas - Ariana Martins",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# TÍTULO
st.title("🎯 Sistema de Gestão de Visitas - Ariana Martins")
st.markdown("---")

# ===== INICIALIZA O ESTADO DA SESSÃO =====
if 'df' not in st.session_state:
    st.session_state.df = None
if 'uploaded_file_name' not in st.session_state:
    st.session_state.uploaded_file_name = None

# ===== UPLOAD DO ARQUIVO =====
st.sidebar.header("📤 Upload da Planilha")
uploaded_file = st.sidebar.file_uploader(
    "Selecione a planilha",
    type=['xlsx'],
    help="Faça o upload da planilha 'Planilha medicos (1).xlsx'"
)

# ===== CARREGAR DADOS =====
if uploaded_file is not None:
    # Verifica se é um arquivo novo
    if st.session_state.uploaded_file_name != uploaded_file.name:
        try:
            df = pd.read_excel(uploaded_file, sheet_name='Ariana Martins - Cadastro_Medic')
            df = df.dropna(subset=['Médico'])
            
            # Adiciona colunas de controle
            if 'Status' not in df.columns:
                df['Status'] = 'A Visitar'
            if 'Ultima_Visita' not in df.columns:
                df['Ultima_Visita'] = ''
            if 'Proxima_Visita' not in df.columns:
                df['Proxima_Visita'] = ''
            if 'Data_Visita' not in df.columns:
                df['Data_Visita'] = ''
            
            st.session_state.df = df
            st.session_state.uploaded_file_name = uploaded_file.name
            st.sidebar.success(f"✅ {len(df)} médicos carregados!")
        except Exception as e:
            st.sidebar.error(f"❌ Erro ao carregar: {str(e)}")
    
    # Usa o DataFrame do estado
    df = st.session_state.df.copy()
    
    # ===== SIDEBAR COM FILTROS =====
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Filtros")
    
    # Status
    status_filter = st.sidebar.selectbox(
        "Status",
        ['Todos', 'A Visitar', 'Visitado']
    )
    
    # Cidade
    cidades = ['Todos'] + sorted(df['Cidade'].dropna().unique().tolist())
    cidade_filter = st.sidebar.selectbox(
        "Cidade",
        cidades
    )
    
    # Bairro (dependente da cidade)
    if cidade_filter != 'Todos':
        bairros_cidade = df[df['Cidade'] == cidade_filter]['Bairro'].dropna().unique().tolist()
        bairros_cidade = sorted(bairros_cidade)
    else:
        bairros_cidade = sorted(df['Bairro'].dropna().unique().tolist())
    
    bairro_filter = st.sidebar.selectbox(
        "Bairro",
        ['Todos'] + bairros_cidade
    )
    
    # Data
    st.sidebar.markdown("---")
    st.sidebar.subheader("📅 Filtro por Data")
    
    data_inicio = st.sidebar.date_input(
        "Data Início",
        value=datetime.now().date() - timedelta(days=30)
    )
    data_fim = st.sidebar.date_input(
        "Data Fim",
        value=datetime.now().date()
    )
    usar_filtro_data = st.sidebar.checkbox("✅ Filtrar por data de visita")
    
    # Busca
    busca = st.sidebar.text_input(
        "🔍 Buscar",
        placeholder="Nome, bairro ou cidade..."
    )
    
    # ===== APLICA FILTROS =====
    df_filtrado = df.copy()
    
    # Busca
    if busca:
        mask = (
            df_filtrado['Médico'].str.contains(busca, case=False, na=False) |
            df_filtrado['Bairro'].str.contains(busca, case=False, na=False) |
            df_filtrado['Cidade'].str.contains(busca, case=False, na=False)
        )
        df_filtrado = df_filtrado[mask]
    
    # Status
    if status_filter != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Status'] == status_filter]
    
    # Cidade
    if cidade_filter != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Cidade'] == cidade_filter]
    
    # Bairro
    if bairro_filter != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Bairro'] == bairro_filter]
    
    # Data
    if usar_filtro_data and 'Data_Visita' in df_filtrado.columns:
        df_filtrado['Data_Visita_DT'] = pd.to_datetime(df_filtrado['Data_Visita'], errors='coerce')
        mask_data = (df_filtrado['Data_Visita_DT'] >= pd.Timestamp(data_inicio)) & \
                    (df_filtrado['Data_Visita_DT'] <= pd.Timestamp(data_fim) + pd.Timedelta(days=1))
        df_filtrado = df_filtrado[mask_data]
        df_filtrado = df_filtrado.drop('Data_Visita_DT', axis=1)
    
    # ===== ESTATÍSTICAS =====
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("👨‍⚕️ Total", len(df))
    with col2:
        st.metric("⏳ A Visitar", len(df[df['Status'] == 'A Visitar']))
    with col3:
        st.metric("✅ Visitados", len(df[df['Status'] == 'Visitado']))
    with col4:
        st.metric("📅 Hoje", datetime.now().strftime('%d/%m/%Y'))
    with col5:
        visitas_hoje = len(df[df['Data_Visita'] == datetime.now().strftime('%Y-%m-%d')])
        st.metric("📌 Visitas Hoje", visitas_hoje)
    
    st.markdown("---")
    
    # ===== TABELA PRINCIPAL =====
    st.subheader(f"📋 Lista de Médicos ({len(df_filtrado)} encontrados)")
    
    # Exibe a tabela
    colunas_exibir = ['Médico', 'Bairro', 'Cidade', 'Celular Médico', 'Status', 'Data_Visita']
    df_display = df_filtrado[colunas_exibir].copy()
    
    # Função para colorir o status
    def color_status(val):
        if val == 'Visitado':
            return 'background-color: #90EE90'
        return 'background-color: #FFC8C8'
    
    st.dataframe(
        df_display.style.applymap(color_status, subset=['Status']),
        use_container_width=True,
        height=400
    )
    
    # ===== SELEÇÃO E AÇÕES =====
    st.markdown("---")
    
    # Lista de médicos para seleção
    medicos_lista = [''] + df_filtrado['Médico'].tolist()
    medico_selecionado = st.selectbox(
        "👤 Selecione um médico:",
        medicos_lista
    )
    
    # ===== BOTÕES DE AÇÃO =====
    if medico_selecionado:
        col_actions, col_details = st.columns([1, 2])
        
        with col_actions:
            st.subheader("⚡ Ações")
            
            # Botão Marcar como Visitado
            if st.button("✅ Marcar como Visitado", type="primary", use_container_width=True):
                idx = df[df['Médico'] == medico_selecionado].index
                if len(idx) > 0:
                    hoje = datetime.now().strftime('%Y-%m-%d')
                    df.loc[idx, 'Status'] = 'Visitado'
                    df.loc[idx, 'Ultima_Visita'] = hoje
                    df.loc[idx, 'Data_Visita'] = hoje
                    proxima = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
                    df.loc[idx, 'Proxima_Visita'] = proxima
                    
                    st.session_state.df = df
                    st.success(f"✅ Visita registrada para {medico_selecionado} em {hoje}!")
                    st.rerun()
            
            # Botão Resetar Status
            if st.button("🔄 Resetar Status", type="secondary", use_container_width=True):
                idx = df[df['Médico'] == medico_selecionado].index
                if len(idx) > 0:
                    df.loc[idx, 'Status'] = 'A Visitar'
                    df.loc[idx, 'Ultima_Visita'] = ''
                    df.loc[idx, 'Proxima_Visita'] = ''
                    df.loc[idx, 'Data_Visita'] = ''
                    
                    st.session_state.df = df
                    st.warning(f"🔄 Status resetado para {medico_selecionado}!")
                    st.rerun()
            
            # Botão Resetar Todos
            if st.button("🔄 Resetar Todos", type="secondary", use_container_width=True):
                df['Status'] = 'A Visitar'
                df['Ultima_Visita'] = ''
                df['Proxima_Visita'] = ''
                df['Data_Visita'] = ''
                st.session_state.df = df
                st.warning("🔄 Todos os status foram resetados!")
                st.rerun()
        
        with col_details:
            st.subheader("📋 Detalhes do Médico")
            dados = df[df['Médico'] == medico_selecionado]
            if len(dados) > 0:
                row = dados.iloc[0]
                
                def get_val(col_name, default='N/A'):
                    try:
                        val = row[col_name]
                        if pd.notna(val):
                            return str(val)
                        return default
                    except:
                        return default
                
                st.markdown(f"""
**📍 INFORMAÇÕES PESSOAIS**
- **Médico:** {get_val('Médico')}
- **CRM/UF:** {get_val('UF/CRM')}
- **Especialidade:** {get_val('Especialidade')}
- **Sexo:** {get_val('Sexo')}

**📞 CONTATO**
- **Celular:** {get_val('Celular Médico')}
- **Clínica:** {get_val('Fone Clínica')}
- **Email:** {get_val('Email1')}

**🏥 LOCAL**
- **Endereço:** {get_val('Endereço')}, {get_val('Número')}
- **Complemento:** {get_val('Complemento')}
- **Bairro:** {get_val('Bairro')}
- **Cidade:** {get_val('Cidade')} - {get_val('UF')}

**📊 STATUS**
- **Situação:** {get_val('Status')}
- **Última Visita:** {get_val('Ultima_Visita') if get_val('Ultima_Visita') != 'N/A' else 'Nunca'}
- **Data da Visita:** {get_val('Data_Visita') if get_val('Data_Visita') != 'N/A' else 'Não visitado'}
                """)
    
    # ===== EXPORTAR =====
    st.markdown("---")
    st.subheader("💾 Exportar Planilha")
    
    col_exp1, col_exp2, col_exp3, col_exp4 = st.columns(4)
    
    with col_exp1:
        if st.button("📥 Baixar Filtrados", type="primary", use_container_width=True):
            if len(df_filtrado) > 0:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_filtrado.to_excel(writer, sheet_name='Ariana Martins - Cadastro_Medic', index=False)
                st.download_button(
                    label=f"📥 {len(df_filtrado)} médicos",
                    data=output.getvalue(),
                    file_name=f"medicos_filtrados_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_filtrados"
                )
            else:
                st.warning("⚠️ Nenhum médico nos filtros")
    
    with col_exp2:
        if st.button("📥 Baixar Todos", type="secondary", use_container_width=True):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Ariana Martins - Cadastro_Medic', index=False)
            st.download_button(
                label="📥 Todos os médicos",
                data=output.getvalue(),
                file_name=f"todos_medicos_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_todos"
            )
    
    with col_exp3:
        df_visitados = df[df['Status'] == 'Visitado']
        if st.button("📥 Só Visitados", type="secondary", use_container_width=True):
            if len(df_visitados) > 0:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_visitados.to_excel(writer, sheet_name='Ariana Martins - Cadastro_Medic', index=False)
                st.download_button(
                    label=f"📥 {len(df_visitados)} visitados",
                    data=output.getvalue(),
                    file_name=f"visitados_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_visitados"
                )
            else:
                st.warning("⚠️ Nenhum médico visitado")
    
    with col_exp4:
        df_a_visitar = df[df['Status'] == 'A Visitar']
        if st.button("📥 Só A Visitar", type="secondary", use_container_width=True):
            if len(df_a_visitar) > 0:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_a_visitar.to_excel(writer, sheet_name='Ariana Martins - Cadastro_Medic', index=False)
                st.download_button(
                    label=f"📥 {len(df_a_visitar)} a visitar",
                    data=output.getvalue(),
                    file_name=f"a_visitar_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_a_visitar"
                )
            else:
                st.warning("⚠️ Nenhum médico a visitar")

else:
    # ===== TELA INICIAL =====
    st.info("👆 Faça o upload da sua planilha no menu lateral para começar")
    
    st.markdown("""
    ### 📋 Como usar:
    
    1. **Clique em "Browse files"** no menu lateral esquerdo
    2. **Selecione a planilha** "Planilha medicos (1).xlsx"
    3. **Use os filtros** para encontrar os médicos por cidade, bairro ou status
    4. **Selecione um médico** na lista e clique em "Marcar como Visitado"
    5. **Exporte a planilha** atualizada quando terminar
    
    ### ✨ Funcionalidades:
    
    - ✅ Filtrar médicos por cidade, bairro e status
    - ✅ Buscar por nome, bairro ou cidade
    - ✅ Marcar visitas com data e hora
    - ✅ Ver detalhes completos do médico
    - ✅ Exportar planilha filtrada ou completa
    - ✅ Estatísticas em tempo real
    - ✅ Filtro por período de visitas
    """)