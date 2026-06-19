# app.py - Versão FINAL com persistência REAL
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

# ===== FUNÇÃO PARA FORMATAR DATA =====
def formatar_data_br(data):
    if pd.isna(data) or data == '':
        return ''
    try:
        if isinstance(data, str):
            data_dt = pd.to_datetime(data)
        else:
            data_dt = data
        return data_dt.strftime('%d/%m/%Y')
    except:
        return str(data)

def hoje_br():
    return datetime.now().strftime('%d/%m/%Y')

# ===== FUNÇÃO PARA OBTER COLUNAS DISPONÍVEIS =====
def get_colunas_disponiveis(df):
    """Retorna lista de colunas disponíveis com seus nomes amigáveis"""
    colunas = []
    if 'Médico' in df.columns:
        colunas.append(('Médico', '👨‍⚕️ Médico'))
    if 'Local' in df.columns:
        colunas.append(('Local', '🏥 Local'))
    if 'Bairro' in df.columns:
        colunas.append(('Bairro', '🏘️ Bairro'))
    if 'Cidade' in df.columns:
        colunas.append(('Cidade', '📍 Cidade'))
    if 'Celular Médico' in df.columns:
        colunas.append(('Celular Médico', '📱 Celular'))
    if 'Status' in df.columns:
        colunas.append(('Status', '📊 Status'))
    if 'Data_Visita' in df.columns:
        colunas.append(('Data_Visita', '📅 Data Visita'))
    if 'Horário de Atendimento' in df.columns:
        colunas.append(('Horário de Atendimento', '🕐 Horário'))
    if 'UF/CRM' in df.columns:
        colunas.append(('UF/CRM', '📋 CRM/UF'))
    if 'Especialidade' in df.columns:
        colunas.append(('Especialidade', '💉 Especialidade'))
    if 'Fone Clínica' in df.columns:
        colunas.append(('Fone Clínica', '📞 Clínica'))
    if 'Email1' in df.columns:
        colunas.append(('Email1', '✉️ Email'))
    if 'CEP' in df.columns:
        colunas.append(('CEP', '📮 CEP'))
    if 'Número' in df.columns:
        colunas.append(('Número', '🔢 Número'))
    if 'Complemento' in df.columns:
        colunas.append(('Complemento', '📝 Complemento'))
    return colunas

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Sistema de Visitas - Ariana Martins",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎯 Sistema de Gestão de Visitas - Ariana Martins")
st.markdown("---")

# ===== INICIALIZA O ESTADO DA SESSÃO =====
if 'df' not in st.session_state:
    st.session_state.df = None
if 'uploaded_file_name' not in st.session_state:
    st.session_state.uploaded_file_name = None
if 'locais_selecionados' not in st.session_state:
    st.session_state.locais_selecionados = []
if 'colunas_selecionadas' not in st.session_state:
    st.session_state.colunas_selecionadas = []
if 'colunas_inicializadas' not in st.session_state:
    st.session_state.colunas_inicializadas = False

# ===== UPLOAD DO ARQUIVO =====
st.sidebar.header("📤 Upload da Planilha")
uploaded_file = st.sidebar.file_uploader(
    "Selecione a planilha",
    type=['xlsx'],
    help="Faça o upload da planilha 'Planilha medicos (1).xlsx'"
)

# ===== CARREGAR DADOS =====
if uploaded_file is not None:
    if st.session_state.uploaded_file_name != uploaded_file.name:
        try:
            df = pd.read_excel(uploaded_file, sheet_name='Ariana Martins - Cadastro_Medic')
            df = df.dropna(subset=['Médico'])
            
            if 'Status' not in df.columns:
                df['Status'] = 'A Visitar'
            if 'Ultima_Visita' not in df.columns:
                df['Ultima_Visita'] = ''
            if 'Proxima_Visita' not in df.columns:
                df['Proxima_Visita'] = ''
            if 'Data_Visita' not in df.columns:
                df['Data_Visita'] = ''
            
            # Converte datas para string
            if 'Data_Visita' in df.columns:
                df['Data_Visita'] = df['Data_Visita'].apply(
                    lambda x: formatar_data_br(x) if pd.notna(x) else ''
                )
            
            st.session_state.df = df
            st.session_state.uploaded_file_name = uploaded_file.name
            st.session_state.locais_selecionados = []
            st.session_state.colunas_inicializadas = False
            
            st.sidebar.success(f"✅ {len(df)} médicos carregados!")
        except Exception as e:
            st.sidebar.error(f"❌ Erro ao carregar: {str(e)}")
    
    df = st.session_state.df.copy()
    
    # ===== SIDEBAR COM FILTROS =====
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Filtros")
    
    # Status
    status_filter = st.sidebar.selectbox(
        "Status",
        ['Todos', 'A Visitar', 'Visitado']
    )
    
    # ===== CIDADE =====
    st.sidebar.subheader("📍 Localização")
    cidades = ['Todos'] + sorted(df['Cidade'].dropna().unique().tolist())
    cidade_filter = st.sidebar.selectbox(
        "Cidade",
        cidades,
        key="cidade_filter"
    )
    
    # ===== BAIRRO =====
    if cidade_filter != 'Todos':
        bairros_cidade = df[df['Cidade'] == cidade_filter]['Bairro'].dropna().unique().tolist()
        bairros_cidade = sorted(bairros_cidade)
    else:
        bairros_cidade = sorted(df['Bairro'].dropna().unique().tolist())
    
    bairro_filter = st.sidebar.selectbox(
        "Bairro",
        ['Todos'] + bairros_cidade,
        key="bairro_filter"
    )
    
    # ===== LOCAL - SELEÇÃO PERMANENTE =====
    st.sidebar.subheader("🏥 Selecionar Locais")
    
    if cidade_filter != 'Todos':
        locais_cidade = df[df['Cidade'] == cidade_filter]['Local'].dropna().unique().tolist()
        locais_cidade = [str(l).strip() for l in locais_cidade if str(l).strip() != '']
        locais_cidade = sorted(locais_cidade)
    else:
        locais_cidade = df['Local'].dropna().unique().tolist()
        locais_cidade = [str(l).strip() for l in locais_cidade if str(l).strip() != '']
        locais_cidade = sorted(locais_cidade)
    
    st.sidebar.markdown("**🔍 Buscar local:**")
    busca_local = st.sidebar.text_input(
        "",
        placeholder="Digite para buscar (ex: BA, RES, HOSPITAL...)",
        key="busca_local_input"
    )
    
    if busca_local:
        busca_local_upper = busca_local.upper().strip()
        locais_encontrados = [l for l in locais_cidade if busca_local_upper in l.upper()]
    else:
        locais_encontrados = locais_cidade
    
    if locais_encontrados:
        st.sidebar.markdown(f"**📋 {len(locais_encontrados)} locais encontrados:**")
        locais_para_adicionar = st.sidebar.multiselect(
            "Selecione os locais para adicionar:",
            options=locais_encontrados,
            default=[],
            key="locais_para_adicionar"
        )
        
        if st.sidebar.button("➕ Adicionar Locais Selecionados", type="primary", use_container_width=True):
            if locais_para_adicionar:
                for local in locais_para_adicionar:
                    if local not in st.session_state.locais_selecionados:
                        st.session_state.locais_selecionados.append(local)
                st.sidebar.success(f"✅ {len(locais_para_adicionar)} locais adicionados!")
                st.rerun()
            else:
                st.sidebar.warning("⚠️ Selecione pelo menos um local")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📌 Locais Selecionados")
    
    if st.session_state.locais_selecionados:
        for i, local in enumerate(st.session_state.locais_selecionados):
            col1, col2 = st.sidebar.columns([4, 1])
            with col1:
                st.sidebar.caption(f"📍 {local}")
            with col2:
                if st.sidebar.button("✕", key=f"remove_{i}"):
                    st.session_state.locais_selecionados.remove(local)
                    st.rerun()
        
        st.sidebar.info(f"✅ {len(st.session_state.locais_selecionados)} locais selecionados")
        if st.sidebar.button("🗑️ Limpar Todos os Locais", use_container_width=True):
            st.session_state.locais_selecionados = []
            st.rerun()
    else:
        st.sidebar.info("📍 Nenhum local selecionado (mostra todos)")
    
    # ===== FILTRO POR DATA =====
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
    
    # Busca geral
    busca = st.sidebar.text_input(
        "🔍 Buscar médico",
        placeholder="Nome, bairro ou cidade..."
    )
    
    # ===== SELEÇÃO DE COLUNAS (PERSISTENTE) =====
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Colunas para Exibir")
    
    colunas_disponiveis = get_colunas_disponiveis(df)
    nomes_colunas = [col for col, _ in colunas_disponiveis]
    
    # Inicializa as colunas selecionadas se ainda não foram
    if not st.session_state.colunas_inicializadas:
        st.session_state.colunas_selecionadas = nomes_colunas.copy()
        st.session_state.colunas_inicializadas = True
    
    # Opções de visualização rápida
    opcoes_visuais = {
        "👀 Modo Rápido": ['Médico', 'Horário de Atendimento'],
        "📊 Modo Visitas": ['Médico', 'Status', 'Data_Visita', 'Horário de Atendimento'],
        "📍 Modo Localização": ['Médico', 'Local', 'Bairro', 'Cidade', 'Horário de Atendimento'],
        "📋 Modo Completo": nomes_colunas
    }
    
    # Dropdown para selecionar modo rápido
    modo_visual = st.sidebar.selectbox(
        "🎯 Modo de Visualização:",
        ['Personalizado'] + list(opcoes_visuais.keys())
    )
    
    # Aplica o modo rápido se selecionado
    if modo_visual != 'Personalizado':
        colunas_nomes = opcoes_visuais[modo_visual]
        novas_colunas = [col for col in nomes_colunas if col in colunas_nomes]
        if set(novas_colunas) != set(st.session_state.colunas_selecionadas):
            st.session_state.colunas_selecionadas = novas_colunas
            st.rerun()
    
    # ===== MULTISELECT =====
    # IMPORTANTE: USAR O VALOR DO ESTADO COMO DEFAULT
    colunas_selecionadas = st.sidebar.multiselect(
        "Selecione as colunas:",
        options=nomes_colunas,
        default=st.session_state.colunas_selecionadas,
        key="multiselect_colunas_persistente"
    )
    
    # Atualiza o estado com o valor atual (NÃO usar rerun aqui!)
    st.session_state.colunas_selecionadas = colunas_selecionadas
    
    # Mostra quantas colunas estão selecionadas
    st.sidebar.caption(f"📊 {len(colunas_selecionadas)} colunas selecionadas")
    
    # ===== APLICA FILTROS =====
    df_filtrado = df.copy()
    
    if busca:
        mask = (
            df_filtrado['Médico'].str.contains(busca, case=False, na=False) |
            df_filtrado['Bairro'].str.contains(busca, case=False, na=False) |
            df_filtrado['Cidade'].str.contains(busca, case=False, na=False) |
            df_filtrado['Local'].str.contains(busca, case=False, na=False)
        )
        df_filtrado = df_filtrado[mask]
    
    if status_filter != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Status'] == status_filter]
    
    if cidade_filter != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Cidade'] == cidade_filter]
    
    if bairro_filter != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Bairro'] == bairro_filter]
    
    if st.session_state.locais_selecionados:
        df_filtrado = df_filtrado[df_filtrado['Local'].isin(st.session_state.locais_selecionados)]
    
    # Filtro por data
    if usar_filtro_data and 'Data_Visita' in df_filtrado.columns:
        def converter_para_datetime(data_str):
            if pd.isna(data_str) or data_str == '':
                return None
            try:
                return pd.to_datetime(data_str, format='%d/%m/%Y')
            except:
                try:
                    return pd.to_datetime(data_str)
                except:
                    return None
        
        df_filtrado['Data_Visita_DT'] = df_filtrado['Data_Visita'].apply(converter_para_datetime)
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
        st.metric("📅 Hoje", hoje_br())
    with col5:
        hoje = hoje_br()
        visitas_hoje = len(df[df['Data_Visita'] == hoje])
        st.metric("📌 Visitas Hoje", visitas_hoje)
    
    st.markdown("---")
    
    # ===== TABELA COM SELEÇÃO DE COLUNAS =====
    st.subheader(f"📋 Lista de Médicos ({len(df_filtrado)} encontrados)")
    
    # Usa as colunas selecionadas do estado
    colunas_exibir = st.session_state.colunas_selecionadas if st.session_state.colunas_selecionadas else ['Médico', 'Horário de Atendimento']
    
    # Filtra apenas colunas que existem
    colunas_existentes = [col for col in colunas_exibir if col in df_filtrado.columns]
    
    if not colunas_existentes:
        st.warning("⚠️ Nenhuma coluna selecionada. Mostrando colunas padrão.")
        colunas_existentes = ['Médico', 'Horário de Atendimento']
    
    # Cria o DataFrame de exibição
    df_exibicao = df_filtrado[colunas_existentes].copy()
    
    # Garante que todas as colunas sejam string para evitar erros
    for col in df_exibicao.columns:
        if col != 'Status':
            df_exibicao[col] = df_exibicao[col].apply(
                lambda x: str(x) if pd.notna(x) else ''
            )
    
    # ===== CONFIGURAÇÃO DE COLUNAS =====
    column_config = {}
    for col in colunas_existentes:
        if col == 'Médico':
            column_config[col] = st.column_config.TextColumn("👨‍⚕️ Médico", width="medium")
        elif col == 'Local':
            column_config[col] = st.column_config.TextColumn("🏥 Local", width="medium")
        elif col == 'Bairro':
            column_config[col] = st.column_config.TextColumn("🏘️ Bairro", width="small")
        elif col == 'Cidade':
            column_config[col] = st.column_config.TextColumn("📍 Cidade", width="small")
        elif col == 'Celular Médico':
            column_config[col] = st.column_config.TextColumn("📱 Celular", width="medium")
        elif col == 'Status':
            column_config[col] = st.column_config.SelectboxColumn(
                "📊 Status",
                options=["A Visitar", "Visitado"],
                width="small"
            )
        elif col == 'Data_Visita':
            column_config[col] = st.column_config.TextColumn("📅 Data Visita", width="medium")
        elif col == 'Horário de Atendimento':
            column_config[col] = st.column_config.TextColumn("🕐 Horário", width="large")
        elif col == 'UF/CRM':
            column_config[col] = st.column_config.TextColumn("📋 CRM/UF", width="medium")
        elif col == 'Especialidade':
            column_config[col] = st.column_config.TextColumn("💉 Especialidade", width="medium")
        elif col == 'Fone Clínica':
            column_config[col] = st.column_config.TextColumn("📞 Clínica", width="medium")
        elif col == 'Email1':
            column_config[col] = st.column_config.TextColumn("✉️ Email", width="medium")
        elif col == 'CEP':
            column_config[col] = st.column_config.TextColumn("📮 CEP", width="medium")
        else:
            column_config[col] = st.column_config.TextColumn(col, width="medium")
    
    # ===== DATA_EDITOR =====
    st.info(f"💡 Editando {len(colunas_existentes)} colunas. Dê duplo clique para editar e Enter para salvar!")
    
    try:
        edited_df = st.data_editor(
            df_exibicao,
            use_container_width=True,
            height=500,
            num_rows="dynamic",
            column_config=column_config,
            hide_index=True,
            key="data_editor_visitas"
        )
    except Exception as e:
        st.error(f"❌ Erro ao carregar editor: {str(e)}")
        st.dataframe(df_exibicao, use_container_width=True)
        edited_df = df_exibicao
    
    # ===== BOTÃO PARA SALVAR ALTERAÇÕES =====
    col_salvar1, col_salvar2, col_salvar3 = st.columns([1, 2, 1])
    with col_salvar2:
        if st.button("💾 Salvar Alterações da Tabela", type="primary", use_container_width=True):
            try:
                df_editado = edited_df
                
                # Atualiza o DataFrame principal com as edições
                for idx, row in df_editado.iterrows():
                    medico = row['Médico']
                    idx_original = df[df['Médico'] == medico].index
                    if len(idx_original) > 0:
                        for col in colunas_existentes:
                            if col in row:
                                df.loc[idx_original[0], col] = row[col]
                
                st.session_state.df = df
                st.success("✅ Alterações salvas com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro ao salvar: {str(e)}")
    
    st.markdown("---")
    
    # ===== SELEÇÃO E AÇÕES =====
    st.subheader("👤 Selecionar Médico para Ações Rápidas")
    
    medicos_lista = [''] + df_filtrado['Médico'].tolist()
    medico_escolhido = st.selectbox(
        "Selecione um médico:",
        medicos_lista
    )
    
    if medico_escolhido:
        col_actions, col_details = st.columns([1, 2])
        
        with col_actions:
            st.subheader("⚡ Ações Rápidas")
            
            if st.button("✅ Marcar como Visitado", type="primary", use_container_width=True):
                idx = df[df['Médico'] == medico_escolhido].index
                if len(idx) > 0:
                    hoje = hoje_br()
                    df.loc[idx, 'Status'] = 'Visitado'
                    df.loc[idx, 'Ultima_Visita'] = hoje
                    df.loc[idx, 'Data_Visita'] = hoje
                    proxima = (datetime.now() + timedelta(days=7)).strftime('%d/%m/%Y')
                    df.loc[idx, 'Proxima_Visita'] = proxima
                    
                    st.session_state.df = df
                    st.success(f"✅ Visita registrada para {medico_escolhido} em {hoje}!")
                    st.rerun()
            
            if st.button("🔄 Resetar Status", type="secondary", use_container_width=True):
                idx = df[df['Médico'] == medico_escolhido].index
                if len(idx) > 0:
                    df.loc[idx, 'Status'] = 'A Visitar'
                    df.loc[idx, 'Ultima_Visita'] = ''
                    df.loc[idx, 'Proxima_Visita'] = ''
                    df.loc[idx, 'Data_Visita'] = ''
                    
                    st.session_state.df = df
                    st.warning(f"🔄 Status resetado para {medico_escolhido}!")
                    st.rerun()
            
            if st.button("🗑️ Excluir Médico", type="secondary", use_container_width=True):
                if st.button("⚠️ Confirmar Exclusão", type="primary"):
                    df = df[df['Médico'] != medico_escolhido]
                    st.session_state.df = df
                    st.success(f"🗑️ Médico {medico_escolhido} excluído!")
                    st.rerun()
        
        with col_details:
            st.subheader("📋 Detalhes do Médico")
            dados = df[df['Médico'] == medico_escolhido]
            if len(dados) > 0:
                row = dados.iloc[0]
                
                def get_val(col_name, default='N/A'):
                    try:
                        val = row[col_name]
                        if pd.notna(val) and str(val).strip() != '':
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
- **Local:** {get_val('Local')}
- **Endereço:** {get_val('Endereço')}, {get_val('Número')}
- **Complemento:** {get_val('Complemento')}
- **Bairro:** {get_val('Bairro')}
- **Cidade:** {get_val('Cidade')} - {get_val('UF')}

**🕐 ATENDIMENTO**
- **Horário:** {get_val('Horário de Atendimento')}

**📊 STATUS**
- **Situação:** {get_val('Status')}
- **Última Visita:** {get_val('Ultima_Visita') if get_val('Ultima_Visita') != 'N/A' else 'Nunca'}
- **Data da Visita:** {get_val('Data_Visita') if get_val('Data_Visita') != 'N/A' else 'Não visitado'}
                """)
    
    # ===== EXPORTAR =====
    st.markdown("---")
    st.subheader("💾 Exportar Planilha")
    
    col_exp1, col_exp2, col_exp3, col_exp4, col_exp5 = st.columns(5)
    
    with col_exp1:
        if st.button("📥 Filtrados", type="primary", use_container_width=True):
            if len(df_filtrado) > 0:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_filtrado.to_excel(writer, sheet_name='Ariana Martins - Cadastro_Medic', index=False)
                st.download_button(
                    label=f"📥 {len(df_filtrado)} médicos",
                    data=output.getvalue(),
                    file_name=f"filtrados_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_filtrados"
                )
            else:
                st.warning("⚠️ Nenhum médico nos filtros")
    
    with col_exp2:
        if st.button("📥 Todos", type="secondary", use_container_width=True):
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
        if st.button("📥 Visitados", type="secondary", use_container_width=True):
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
        if st.button("📥 A Visitar", type="secondary", use_container_width=True):
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
    
    with col_exp5:
        if st.button("📥 Backup", type="secondary", use_container_width=True):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Ariana Martins - Cadastro_Medic', index=False)
            st.download_button(
                label="📥 Backup completo",
                data=output.getvalue(),
                file_name=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_backup"
            )

else:
    st.info("👆 Faça o upload da sua planilha no menu lateral para começar")
    
    st.markdown("""
    ### 📋 Como usar:
    
    1. **Clique em "Browse files"** no menu lateral esquerdo
    2. **Selecione a planilha** "Planilha medicos (1).xlsx"
    
    ### 📋 SELEÇÃO DE COLUNAS (PERSISTENTE!):
    
    - **Todas as colunas** são mostradas por padrão
    - Use o multiselect para **esconder** as colunas que não quer ver
    - A seleção **NÃO muda** quando você troca de filtro!
    - Use os **Modos de Visualização** para alternar rapidamente:
      - 👀 **Modo Rápido:** só nome + horário
      - 📊 **Modo Visitas:** foco em status e datas
      - 📋 **Modo Completo:** todas as colunas
    
    ### 🖱️ EDIÇÃO DIRETA:
    
    - **Duplo clique** em qualquer célula para editar
    - **Pressione Enter** para salvar a alteração
    - **Clique em "Salvar Alterações"** para confirmar todas as mudanças
    """)