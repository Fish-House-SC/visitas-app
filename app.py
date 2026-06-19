# app.py - Versão com data no formato BRASILEIRO (dd/MM/yyyy)
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

# ===== FUNÇÃO PARA FORMATAR DATA =====
def formatar_data_br(data):
    """Converte data para formato brasileiro dd/MM/yyyy"""
    if pd.isna(data) or data == '':
        return ''
    try:
        if isinstance(data, str):
            # Tenta converter string para datetime
            data_dt = pd.to_datetime(data)
        else:
            data_dt = data
        return data_dt.strftime('%d/%m/%Y')
    except:
        return str(data)

def formatar_data_br_para_filtro(data):
    """Converte data para formato datetime para filtro"""
    if pd.isna(data) or data == '':
        return None
    try:
        if isinstance(data, str):
            return pd.to_datetime(data, format='%d/%m/%Y')
        return data
    except:
        return None

def hoje_br():
    """Retorna a data de hoje no formato brasileiro"""
    return datetime.now().strftime('%d/%m/%Y')

# TÍTULO
st.title("🎯 Sistema de Gestão de Visitas - Ariana Martins")
st.markdown("---")

# ===== INICIALIZA O ESTADO DA SESSÃO =====
if 'df' not in st.session_state:
    st.session_state.df = None
if 'uploaded_file_name' not in st.session_state:
    st.session_state.uploaded_file_name = None
if 'modo_edicao' not in st.session_state:
    st.session_state.modo_edicao = False
if 'medico_editando' not in st.session_state:
    st.session_state.medico_editando = None

# ===== UPLOAD DO ARQUIVO =====
st.sidebar.header("📤 Upload da Planilha")
uploaded_file = st.sidebar.file_uploader(
    "Selecione a planilha",
    type=['xlsx'],
    help="Faça o upload da planilha 'Planilha medicos (1).xlsx'"
)

# ===== FUNÇÃO PARA SALVAR EDIÇÕES =====
def salvar_edicao(dados_editados):
    """Salva as alterações feitas no médico"""
    df = st.session_state.df
    idx = df[df['Médico'] == st.session_state.medico_editando].index
    
    if len(idx) > 0:
        for col, valor in dados_editados.items():
            if col in df.columns:
                df.loc[idx, col] = valor
        
        st.session_state.df = df
        st.session_state.modo_edicao = False
        st.session_state.medico_editando = None
        st.success("✅ Alterações salvas com sucesso!")
        st.rerun()

# ===== FUNÇÃO PARA EXCLUIR MÉDICO =====
def excluir_medico(medico):
    """Exclui um médico da planilha"""
    df = st.session_state.df
    df = df[df['Médico'] != medico]
    st.session_state.df = df
    st.session_state.modo_edicao = False
    st.session_state.medico_editando = None
    st.success(f"🗑️ Médico {medico} excluído com sucesso!")
    st.rerun()

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
    
    # ===== CIDADE =====
    st.sidebar.subheader("📍 Localização")
    cidades = ['Todos'] + sorted(df['Cidade'].dropna().unique().tolist())
    cidade_filter = st.sidebar.selectbox(
        "Cidade",
        cidades,
        key="cidade_filter"
    )
    
    # ===== BAIRRO (DEPENDENTE DA CIDADE) =====
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
    
    # ===== LOCAL (DEPENDENTE DA CIDADE) =====
    st.sidebar.subheader("🏥 Local")
    
    if cidade_filter != 'Todos':
        locais_cidade = df[df['Cidade'] == cidade_filter]['Local'].dropna().unique().tolist()
        locais_cidade = [str(l).strip() for l in locais_cidade if str(l).strip() != '']
        locais_cidade = sorted(locais_cidade)
    else:
        locais_cidade = df['Local'].dropna().unique().tolist()
        locais_cidade = [str(l).strip() for l in locais_cidade if str(l).strip() != '']
        locais_cidade = sorted(locais_cidade)
    
    local_filter = st.sidebar.selectbox(
        "Local de Atendimento",
        ['Todos'] + locais_cidade,
        help="Filtra pelos locais de atendimento. Os locais são filtrados automaticamente pela cidade selecionada!"
    )
    
    # ===== FILTRO POR DATA (FORMATO BRASILEIRO) =====
    st.sidebar.markdown("---")
    st.sidebar.subheader("📅 Filtro por Data")
    
    # Usa date_input do Streamlit (já funciona com datas)
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
            df_filtrado['Cidade'].str.contains(busca, case=False, na=False) |
            df_filtrado['Local'].str.contains(busca, case=False, na=False)
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
    
    # Local
    if local_filter != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Local'] == local_filter]
    
    # ===== FILTRO POR DATA (FORMATO BRASILEIRO) =====
    if usar_filtro_data and 'Data_Visita' in df_filtrado.columns:
        # Converte as datas do formato brasileiro para datetime
        def converter_para_datetime(data_str):
            if pd.isna(data_str) or data_str == '':
                return None
            try:
                return pd.to_datetime(data_str, format='%d/%m/%Y')
            except:
                return None
        
        # Aplica a conversão
        df_filtrado['Data_Visita_DT'] = df_filtrado['Data_Visita'].apply(converter_para_datetime)
        
        # Filtra
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
        # Conta visitas de hoje no formato brasileiro
        hoje = hoje_br()
        visitas_hoje = len(df[df['Data_Visita'] == hoje])
        st.metric("📌 Visitas Hoje", visitas_hoje)
    
    st.markdown("---")
    
    # ===== TABELA PRINCIPAL =====
    st.subheader(f"📋 Lista de Médicos ({len(df_filtrado)} encontrados)")
    
    # Exibe a tabela - formatando as datas
    colunas_exibir = ['Médico', 'Local', 'Bairro', 'Cidade', 'Celular Médico', 'Status', 'Data_Visita']
    df_display = df_filtrado[colunas_exibir].copy()
    
    # Formata as datas para exibição (já estão no formato correto)
    if 'Data_Visita' in df_display.columns:
        df_display['Data_Visita'] = df_display['Data_Visita'].apply(
            lambda x: x if pd.isna(x) or x == '' else str(x)
        )
    
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
            
            # Botão Marcar como Visitado (com data no formato brasileiro)
            if st.button("✅ Marcar como Visitado", type="primary", use_container_width=True):
                idx = df[df['Médico'] == medico_selecionado].index
                if len(idx) > 0:
                    hoje = hoje_br()  # Data no formato dd/MM/yyyy
                    df.loc[idx, 'Status'] = 'Visitado'
                    df.loc[idx, 'Ultima_Visita'] = hoje
                    df.loc[idx, 'Data_Visita'] = hoje
                    # Próxima visita: 7 dias depois (em formato brasileiro)
                    proxima = (datetime.now() + timedelta(days=7)).strftime('%d/%m/%Y')
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
            
            # Botão Editar
            if st.button("✏️ Editar Informações", type="secondary", use_container_width=True):
                st.session_state.modo_edicao = True
                st.session_state.medico_editando = medico_selecionado
                st.rerun()
            
            # Botão Excluir
            if st.button("🗑️ Excluir Médico", type="secondary", use_container_width=True):
                if st.button("⚠️ Confirmar Exclusão", type="primary"):
                    excluir_medico(medico_selecionado)
        
        with col_details:
            if st.session_state.modo_edicao and st.session_state.medico_editando == medico_selecionado:
                # ===== MODO EDIÇÃO =====
                st.subheader("✏️ Editar Informações")
                st.info(f"Editando: **{medico_selecionado}**")
                
                dados = df[df['Médico'] == medico_selecionado]
                if len(dados) > 0:
                    row = dados.iloc[0]
                    
                    with st.form(key="form_edicao"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            novo_medico = st.text_input("Médico", value=row.get('Médico', ''))
                            novo_crm = st.text_input("UF/CRM", value=row.get('UF/CRM', ''))
                            nova_especialidade = st.text_input("Especialidade", value=row.get('Especialidade', ''))
                            novo_sexo = st.selectbox(
                                "Sexo",
                                ['', 'Masculino', 'Feminino'],
                                index=0 if pd.isna(row.get('Sexo')) else (1 if row.get('Sexo') == 'Masculino' else 2)
                            )
                            novo_celular = st.text_input("Celular Médico", value=row.get('Celular Médico', ''))
                            novo_telefone = st.text_input("Fone Clínica", value=row.get('Fone Clínica', ''))
                            novo_email = st.text_input("Email", value=row.get('Email1', ''))
                        
                        with col2:
                            novo_local = st.text_input("Local", value=row.get('Local', ''))
                            novo_endereco = st.text_input("Endereço", value=row.get('Endereço', ''))
                            novo_numero = st.text_input("Número", value=row.get('Número', ''))
                            novo_complemento = st.text_input("Complemento", value=row.get('Complemento', ''))
                            novo_bairro = st.text_input("Bairro", value=row.get('Bairro', ''))
                            nova_cidade = st.text_input("Cidade", value=row.get('Cidade', ''))
                            novo_uf = st.text_input("UF", value=row.get('UF', ''))
                            novo_cep = st.text_input("CEP", value=row.get('CEP', ''))
                        
                        col_bt1, col_bt2 = st.columns(2)
                        with col_bt1:
                            if st.form_submit_button("💾 Salvar Alterações", type="primary"):
                                dados_editados = {
                                    'Médico': novo_medico,
                                    'UF/CRM': novo_crm,
                                    'Especialidade': nova_especialidade,
                                    'Sexo': novo_sexo,
                                    'Celular Médico': novo_celular,
                                    'Fone Clínica': novo_telefone,
                                    'Email1': novo_email,
                                    'Local': novo_local,
                                    'Endereço': novo_endereco,
                                    'Número': novo_numero,
                                    'Complemento': novo_complemento,
                                    'Bairro': novo_bairro,
                                    'Cidade': nova_cidade,
                                    'UF': novo_uf,
                                    'CEP': novo_cep
                                }
                                salvar_edicao(dados_editados)
                        
                        with col_bt2:
                            if st.form_submit_button("❌ Cancelar"):
                                st.session_state.modo_edicao = False
                                st.session_state.medico_editando = None
                                st.rerun()
            else:
                # ===== MODO VISUALIZAÇÃO =====
                st.subheader("📋 Detalhes do Médico")
                dados = df[df['Médico'] == medico_selecionado]
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
    # ===== TELA INICIAL =====
    st.info("👆 Faça o upload da sua planilha no menu lateral para começar")
    
    st.markdown("""
    ### 📋 Como usar:
    
    1. **Clique em "Browse files"** no menu lateral esquerdo
    2. **Selecione a planilha** "Planilha medicos (1).xlsx"
    3. **Use os filtros** para encontrar os médicos:
       - 📍 **Cidade** - Selecione a cidade (Bairros e Locais são filtrados automaticamente!)
       - 🏘️ **Bairro** - Apenas bairros da cidade selecionada
       - 🏥 **Local** - Apenas locais da cidade selecionada
       - 📊 **Status** - Ver apenas visitados ou a visitar
       - 📅 **Data** - Filtrar por período de visitas (formato brasileiro)
    4. **Selecione um médico** e clique em:
       - ✅ **Marcar como Visitado** - Registrar visita com data no formato **dd/MM/yyyy**
       - ✏️ **Editar Informações** - Editar todos os dados
       - 🗑️ **Excluir Médico** - Remover da planilha
    5. **Exporte a planilha** atualizada quando terminar
    
    ### ✨ Funcionalidades:
    
    - ✅ **Datas no formato brasileiro (dd/MM/yyyy)**
    - ✅ **Filtro inteligente:** Bairros e Locais são filtrados automaticamente pela cidade
    - ✅ **Editar todas as informações** dos médicos
    - ✅ **Excluir médicos** da planilha
    - ✅ **Exportar planilha filtrada** (apenas médicos selecionados)
    - ✅ **Exportar planilha completa**
    - ✅ **Exportar por status** (visitados / a visitar)
    - ✅ **Backup** com timestamp
    - ✅ Marcar visitas com data e hora
    - ✅ Estatísticas em tempo real
    """)