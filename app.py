# app.py - Versão MESCLADA (Tamanho correto + Formatação Celular + Adicionar Médico)
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

# ===== FUNÇÃO PARA FORMATAR CELULAR =====
def formatar_celular(numero):
    """Formata número de celular no padrão brasileiro (XX) XXXXX-XXXX"""
    if not numero or numero == '':
        return ''
    
    numeros = ''.join(filter(str.isdigit, str(numero)))
    if not numeros:
        return ''
    
    if len(numeros) > 11:
        numeros = numeros[:11]
    
    if len(numeros) == 10:
        return f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:10]}"
    elif len(numeros) == 11:
        return f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:11]}"
    elif len(numeros) == 8:
        return f"{numeros[:4]}-{numeros[4:8]}"
    elif len(numeros) == 9:
        return f"{numeros[:5]}-{numeros[5:9]}"
    else:
        return numero

# ===== FUNÇÃO PARA CAMPOS DE CELULAR =====
def campo_celular_formatado(label, value="", placeholder="", key=None, help_text="Digite apenas os números (ex: 48999999999)"):
    if value and '(' in str(value):
        value = ''.join(filter(str.isdigit, str(value)))
    
    celular = st.text_input(
        label,
        value=value if value else '',
        placeholder=placeholder,
        key=key,
        help=help_text
    )
    
    if celular and celular != '':
        numeros = ''.join(filter(str.isdigit, str(celular)))
        if numeros:
            return formatar_celular(numeros)
    
    return celular

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
    colunas = []
    if 'Médico' in df.columns:
        colunas.append(('Médico', '👨‍⚕️ Médico'))
    if 'Local' in df.columns:
        colunas.append(('Local', '🏥 Local'))
    if 'Endereço' in df.columns:
        colunas.append(('Endereço', '📍 Endereço'))
    if 'Número' in df.columns:
        colunas.append(('Número', '🔢 Número'))
    if 'Complemento' in df.columns:
        colunas.append(('Complemento', '📝 Complemento'))
    if 'Bairro' in df.columns:
        colunas.append(('Bairro', '🏘️ Bairro'))
    if 'Cidade' in df.columns:
        colunas.append(('Cidade', '📍 Cidade'))
    if 'UF' in df.columns:
        colunas.append(('UF', '📌 UF'))
    if 'CEP' in df.columns:
        colunas.append(('CEP', '📮 CEP'))
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
    return colunas

# ===== FUNÇÃO PARA ADICIONAR MÉDICO =====
def adicionar_medico(df, novo_medico):
    """Adiciona um novo médico ao DataFrame"""
    novo_registro = {
        'Médico': novo_medico['Médico'],
        'Local': novo_medico.get('Local', ''),
        'Endereço': novo_medico.get('Endereço', ''),
        'Número': novo_medico.get('Número', ''),
        'Complemento': novo_medico.get('Complemento', ''),
        'Bairro': novo_medico.get('Bairro', ''),
        'Cidade': novo_medico.get('Cidade', ''),
        'UF': novo_medico.get('UF', ''),
        'CEP': novo_medico.get('CEP', ''),
        'Celular Médico': novo_medico.get('Celular Médico', ''),
        'Fone Clínica': novo_medico.get('Fone Clínica', ''),
        'Email1': novo_medico.get('Email1', ''),
        'UF/CRM': novo_medico.get('UF/CRM', ''),
        'Especialidade': novo_medico.get('Especialidade', ''),
        'Sexo': novo_medico.get('Sexo', ''),
        'Horário de Atendimento': novo_medico.get('Horário de Atendimento', ''),
        'Status': 'A Visitar',
        'Ultima_Visita': '',
        'Proxima_Visita': '',
        'Data_Visita': '',
        'Setor': novo_medico.get('Setor', ''),
        'Sigla2': novo_medico.get('Sigla2', ''),
        'Potencial': novo_medico.get('Potencial', ''),
        'Categoria': novo_medico.get('Categoria', ''),
        'Celular Clínica': novo_medico.get('Celular Clínica', ''),
        'Formatura': novo_medico.get('Formatura', ''),
        'Aniversario': novo_medico.get('Aniversario', ''),
        'Email2': novo_medico.get('Email2', ''),
        'Cargo': novo_medico.get('Cargo', ''),
        'Nome': novo_medico.get('Nome', ''),
        'Visitas': novo_medico.get('Visitas', ''),
        'Freq.Visita': novo_medico.get('Freq.Visita', ''),
    }
    
    novo_df = pd.DataFrame([novo_registro])
    return pd.concat([df, novo_df], ignore_index=True)

# ===== FUNÇÃO PARA OBTER CLÍNICAS ÚNICAS =====
def get_clinicas_unicas(df):
    clinicas = {}
    for idx, row in df.iterrows():
        local = row.get('Local', '')
        if local and local != '':
            if local not in clinicas:
                clinicas[local] = {
                    'Local': local,
                    'Endereço': row.get('Endereço', ''),
                    'Número': row.get('Número', ''),
                    'Complemento': row.get('Complemento', ''),
                    'Bairro': row.get('Bairro', ''),
                    'Cidade': row.get('Cidade', ''),
                    'UF': row.get('UF', ''),
                    'CEP': row.get('CEP', ''),
                    'Fone Clínica': row.get('Fone Clínica', ''),
                    'Email1': row.get('Email1', ''),
                    'Setor': row.get('Setor', ''),
                }
    return clinicas

# ===== FUNÇÃO PARA INICIALIZAR ESTADOS =====
def inicializar_estados():
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
    if 'mostrar_gerenciador_colunas' not in st.session_state:
        st.session_state.mostrar_gerenciador_colunas = False
    if 'medico_busca' not in st.session_state:
        st.session_state.medico_busca = ""
    if 'ordem_coluna' not in st.session_state:
        st.session_state.ordem_coluna = None
    if 'ordem_direcao' not in st.session_state:
        st.session_state.ordem_direcao = None
    if 'pagina_atual' not in st.session_state:
        st.session_state.pagina_atual = 'principal'

# ===== CONFIGURAÇÃO DA PÁGINA =====
st.set_page_config(
    page_title="Sistema de Visitas - Ariana Martins",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== PÁGINA DE ADIÇÃO DE MÉDICOS =====
def pagina_adicionar_medico():
    st.title("➕ Adicionar Novo Médico")
    st.markdown("---")
    
    col_voltar1, col_voltar2, col_voltar3 = st.columns([1, 2, 1])
    with col_voltar2:
        if st.button("⬅️ Voltar para Lista", use_container_width=True, key="btn_voltar_lista"):
            st.session_state.pagina_atual = 'principal'
            st.rerun()
    
    st.markdown("---")
    
    if st.session_state.df is None:
        st.warning("⚠️ Faça o upload de uma planilha primeiro!")
        return
    
    df = st.session_state.df.copy()
    
    st.subheader("🏥 Buscar Clínica Existente")
    
    clinicas = get_clinicas_unicas(df)
    lista_clinicas = [''] + sorted(clinicas.keys())
    
    clinica_selecionada = st.selectbox(
        "Selecione uma clínica existente (ou deixe em branco para criar uma nova):",
        options=lista_clinicas,
        help="Digite parte do nome para buscar"
    )
    
    st.subheader("📋 Dados do Médico")
    
    if clinica_selecionada and clinica_selecionada in clinicas:
        dados_clinica = clinicas[clinica_selecionada]
        st.success(f"✅ Clínica selecionada: **{clinica_selecionada}**")
        
        local_valor = clinica_selecionada
        endereco_valor = dados_clinica.get('Endereço', '')
        numero_valor = dados_clinica.get('Número', '')
        complemento_valor = dados_clinica.get('Complemento', '')
        bairro_valor = dados_clinica.get('Bairro', '')
        cidade_valor = dados_clinica.get('Cidade', '')
        uf_valor = dados_clinica.get('UF', '')
        cep_valor = dados_clinica.get('CEP', '')
        fone_clinica_valor = dados_clinica.get('Fone Clínica', '')
        email_clinica_valor = dados_clinica.get('Email1', '')
        setor_valor = dados_clinica.get('Setor', '')
        
        with st.expander("📋 Dados da Clínica"):
            st.write(f"**Endereço:** {endereco_valor}, {numero_valor}")
            st.write(f"**Complemento:** {complemento_valor}")
            st.write(f"**Bairro:** {bairro_valor}")
            st.write(f"**Cidade:** {cidade_valor} - {uf_valor}")
            st.write(f"**CEP:** {cep_valor}")
            st.write(f"**Telefone:** {fone_clinica_valor}")
            st.write(f"**Email:** {email_clinica_valor}")
    else:
        local_valor = ''
        endereco_valor = ''
        numero_valor = ''
        complemento_valor = ''
        bairro_valor = ''
        cidade_valor = ''
        uf_valor = ''
        cep_valor = ''
        fone_clinica_valor = ''
        email_clinica_valor = ''
        setor_valor = ''
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**👤 Dados Pessoais**")
        novo_medico_nome = st.text_input("👨‍⚕️ Nome do Médico *", placeholder="Ex: Dr. João Silva")
        novo_uf_crm = st.text_input("📋 CRM/UF", placeholder="Ex: SC 12345")
        nova_especialidade = st.text_input("💉 Especialidade", placeholder="Ex: Cardiologista")
        novo_sexo = st.selectbox(
            "⚤ Sexo",
            options=['', 'Masculino', 'Feminino']
        )
        
        novo_celular = campo_celular_formatado(
            "📱 Celular Médico",
            value="",
            placeholder="Digite apenas os números (ex: 48999999999)",
            key="novo_celular",
            help_text="Digite apenas os números. O formato será aplicado automaticamente!"
        )
        
        novo_email = st.text_input("✉️ Email", placeholder="Ex: medico@email.com")
        
    with col2:
        st.markdown("**🏥 Dados da Clínica**")
        novo_local = st.text_input("🏥 Local (Clínica)", value=local_valor, placeholder="Ex: Clínica Saúde")
        novo_endereco = st.text_input("📍 Endereço", value=endereco_valor, placeholder="Ex: Rua das Flores")
        novo_numero = st.text_input("🔢 Número", value=numero_valor, placeholder="Ex: 123")
        novo_complemento = st.text_input("📝 Complemento", value=complemento_valor, placeholder="Ex: Sala 101")
        novo_bairro = st.text_input("🏘️ Bairro", value=bairro_valor, placeholder="Ex: Centro")
        nova_cidade = st.text_input("📍 Cidade", value=cidade_valor, placeholder="Ex: Florianópolis")
        novo_uf = st.text_input("📌 UF", value=uf_valor, placeholder="Ex: SC")
        novo_cep = st.text_input("📮 CEP", value=cep_valor, placeholder="Ex: 88000-000")
        novo_fone_clinica = st.text_input("📞 Telefone da Clínica", value=fone_clinica_valor, placeholder="Ex: (48) 3333-3333")
        novo_email_clinica = st.text_input("✉️ Email da Clínica", value=email_clinica_valor, placeholder="Ex: clinica@email.com")
        novo_setor = st.text_input("📂 Setor", value=setor_valor, placeholder="Ex: 81505 - Ariana Martins")
    
    with st.expander("📋 Informações Adicionais"):
        novo_horario = st.text_area(
            "🕐 Horário de Atendimento",
            placeholder="Ex: Seg (09:00-12:00)  Ter (08:00-10:15)  Qua (08:00-12:15)",
            help="Informe os dias e horários de atendimento"
        )
        novo_frequencia = st.text_input("📅 Frequência de Visitas", placeholder="Ex: 2ª Sem (Qui)  7ª Sem (Qui)")
        novo_categoria = st.text_input("📊 Categoria", placeholder="Ex: 3.0")
        novo_potencial = st.text_input("🎯 Potencial", placeholder="Ex: Foco")
        novo_sigla2 = st.text_input("🔤 Sigla2", placeholder="Ex: CIV/R1")
        novo_visitas = st.text_input("📊 Visitas", placeholder="Ex: 2.0")
    
    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("💾 Adicionar Médico", type="primary", use_container_width=True, key="btn_adicionar_medico"):
            if not novo_medico_nome:
                st.error("❌ O nome do médico é obrigatório!")
            else:
                celular_formatado = novo_celular
                if novo_celular:
                    numeros = ''.join(filter(str.isdigit, str(novo_celular)))
                    if numeros:
                        celular_formatado = formatar_celular(numeros)
                
                novo_medico = {
                    'Médico': novo_medico_nome,
                    'Local': novo_local if novo_local else '',
                    'Endereço': novo_endereco if novo_endereco else '',
                    'Número': novo_numero if novo_numero else '',
                    'Complemento': novo_complemento if novo_complemento else '',
                    'Bairro': novo_bairro if novo_bairro else '',
                    'Cidade': nova_cidade if nova_cidade else '',
                    'UF': novo_uf if novo_uf else '',
                    'CEP': novo_cep if novo_cep else '',
                    'Celular Médico': celular_formatado,
                    'Fone Clínica': novo_fone_clinica if novo_fone_clinica else '',
                    'Email1': novo_email if novo_email else '',
                    'UF/CRM': novo_uf_crm if novo_uf_crm else '',
                    'Especialidade': nova_especialidade if nova_especialidade else '',
                    'Sexo': novo_sexo if novo_sexo else '',
                    'Horário de Atendimento': novo_horario if novo_horario else '',
                    'Freq.Visita': novo_frequencia if novo_frequencia else '',
                    'Categoria': novo_categoria if novo_categoria else '',
                    'Potencial': novo_potencial if novo_potencial else '',
                    'Sigla2': novo_sigla2 if novo_sigla2 else '',
                    'Visitas': novo_visitas if novo_visitas else '',
                    'Setor': novo_setor if novo_setor else '',
                    'Email2': '',
                    'Cargo': '',
                    'Nome': '',
                    'Formatura': '',
                    'Aniversario': '',
                    'Celular Clínica': '',
                }
                
                df_atualizado = adicionar_medico(df, novo_medico)
                st.session_state.df = df_atualizado
                
                st.success(f"✅ Médico **{novo_medico_nome}** adicionado com sucesso!")
                
                col_clear, col_back = st.columns(2)
                with col_clear:
                    if st.button("🔄 Adicionar Outro Médico", use_container_width=True, key="btn_adicionar_outro"):
                        st.rerun()
                with col_back:
                    if st.button("⬅️ Voltar para Lista", use_container_width=True, key="btn_voltar_depois_adicionar"):
                        st.session_state.pagina_atual = 'principal'
                        st.rerun()

# ===== PÁGINA PRINCIPAL =====
def pagina_principal():
    st.title("🎯 Sistema de Gestão de Visitas - Ariana Martins (Te adora!!!)")
    st.markdown("---")
    
    # ===== BOTÃO PARA ADICIONAR MÉDICO =====
    col_add1, col_add2, col_add3 = st.columns([1, 2, 1])
    with col_add2:
        if st.button("➕ Adicionar Novo Médico", type="primary", use_container_width=True, key="btn_adicionar_novo"):
            st.session_state.pagina_atual = 'adicionar'
            st.rerun()
    
    st.markdown("---")
    
    # ===== SIDEBAR COM FILTROS =====
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
                
                if 'Data_Visita' in df.columns:
                    df['Data_Visita'] = df['Data_Visita'].apply(
                        lambda x: formatar_data_br(x) if pd.notna(x) else ''
                    )
                
                for col in df.columns:
                    df[col] = df[col].apply(
                        lambda x: str(x) if pd.notna(x) else ''
                    )
                
                st.session_state.df = df
                st.session_state.uploaded_file_name = uploaded_file.name
                st.session_state.locais_selecionados = []
                st.session_state.colunas_inicializadas = False
                st.session_state.medico_busca = ""
                
                st.session_state.ordem_coluna = None
                st.session_state.ordem_direcao = None
                
                st.sidebar.success(f"✅ {len(df)} médicos carregados!")
            except Exception as e:
                st.sidebar.error(f"❌ Erro ao carregar: {str(e)}")
    
    if st.session_state.df is not None:
        df = st.session_state.df.copy()
        
        st.sidebar.markdown("---")
        st.sidebar.header("🔍 Filtros")
        
        # ===== BUSCA POR MÉDICO =====
        st.sidebar.subheader("👨‍⚕️ Buscar Médico")
        st.sidebar.markdown("**🔍 Digite o nome do médico:**")
        
        medico_busca = st.sidebar.text_input(
            "",
            placeholder="Ex: Silva, Pedro, Maria...",
            value=st.session_state.medico_busca,
            key="medico_busca_input",
            help="Digite parte do nome do médico para filtrar"
        )
        
        st.session_state.medico_busca = medico_busca
        
        if medico_busca:
            df_temp = df.copy()
            mask = df_temp['Médico'].str.contains(medico_busca, case=False, na=False)
            qtd_encontrados = len(df_temp[mask])
            if qtd_encontrados > 0:
                st.sidebar.success(f"✅ {qtd_encontrados} médicos encontrados com '{medico_busca}'")
            else:
                st.sidebar.warning(f"⚠️ Nenhum médico encontrado com '{medico_busca}'")
        
        # Status
        status_filter = st.sidebar.selectbox(
            "Status",
            ['Todos', 'A Visitar', 'Visitado']
        )
        
        st.sidebar.subheader("📍 Localização")
        cidades = ['Todos'] + sorted(df['Cidade'].dropna().unique().tolist())
        cidade_filter = st.sidebar.selectbox("Cidade", cidades, key="cidade_filter")
        
        if cidade_filter != 'Todos':
            bairros_cidade = df[df['Cidade'] == cidade_filter]['Bairro'].dropna().unique().tolist()
            bairros_cidade = sorted(bairros_cidade)
        else:
            bairros_cidade = sorted(df['Bairro'].dropna().unique().tolist())
        
        bairro_filter = st.sidebar.selectbox("Bairro", ['Todos'] + bairros_cidade, key="bairro_filter")
        
        # ===== LOCAL =====
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
        busca_local = st.sidebar.text_input("", placeholder="Digite para buscar (ex: BA, RES...)", key="busca_local_input")
        
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
        
        data_inicio = st.sidebar.date_input("Data Início", value=datetime.now().date() - timedelta(days=30))
        data_fim = st.sidebar.date_input("Data Fim", value=datetime.now().date())
        usar_filtro_data = st.sidebar.checkbox("✅ Filtrar por data de visita")
        
        # ===== SELEÇÃO DE COLUNAS =====
        st.sidebar.markdown("---")
        st.sidebar.subheader("📋 Colunas para Exibir")
        
        colunas_disponiveis = get_colunas_disponiveis(df)
        nomes_colunas = [col for col, _ in colunas_disponiveis]
        
        if not st.session_state.colunas_inicializadas:
            st.session_state.colunas_selecionadas = nomes_colunas.copy()
            st.session_state.colunas_inicializadas = True
        
        opcoes_visuais = {
            "👀 Modo Rápido": ['Médico', 'Horário de Atendimento'],
            "📊 Modo Visitas": ['Médico', 'Status', 'Data_Visita', 'Horário de Atendimento'],
            "📍 Modo Localização": ['Médico', 'Local', 'Endereço', 'Número', 'Bairro', 'Cidade'],
            "📋 Modo Completo": nomes_colunas
        }
        
        modo_visual = st.sidebar.selectbox("🎯 Modo de Visualização:", ['Personalizado'] + list(opcoes_visuais.keys()))
        
        if modo_visual != 'Personalizado':
            colunas_nomes = opcoes_visuais[modo_visual]
            novas_colunas = [col for col in nomes_colunas if col in colunas_nomes]
            if set(novas_colunas) != set(st.session_state.colunas_selecionadas):
                st.session_state.colunas_selecionadas = novas_colunas
                st.rerun()
        
        colunas_selecionadas = st.sidebar.multiselect(
            "Selecione as colunas:",
            options=nomes_colunas,
            default=st.session_state.colunas_selecionadas,
            key="multiselect_colunas_persistente"
        )
        
        st.session_state.colunas_selecionadas = colunas_selecionadas
        st.sidebar.caption(f"📊 {len(colunas_selecionadas)} colunas selecionadas")
        
        # ===== APLICA FILTROS =====
        df_filtrado = df.copy()
        
        if medico_busca:
            mask = df_filtrado['Médico'].str.contains(medico_busca, case=False, na=False)
            df_filtrado = df_filtrado[mask]
        
        if status_filter != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['Status'] == status_filter]
        
        if cidade_filter != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['Cidade'] == cidade_filter]
        
        if bairro_filter != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['Bairro'] == bairro_filter]
        
        if st.session_state.locais_selecionados:
            df_filtrado = df_filtrado[df_filtrado['Local'].isin(st.session_state.locais_selecionados)]
        
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
        
        # ===== APLICA ORDENAÇÃO =====
        df_exibicao_completa = df_filtrado.copy()
        df_exibicao_completa['_idx_original'] = df_exibicao_completa.index
        
        if st.session_state.ordem_coluna is not None and st.session_state.ordem_coluna in df_exibicao_completa.columns:
            coluna_ordenacao = st.session_state.ordem_coluna
            direcao = st.session_state.ordem_direcao
            
            df_exibicao_completa[coluna_ordenacao] = df_exibicao_completa[coluna_ordenacao].astype(str)
            
            if direcao == 'asc':
                df_exibicao_completa = df_exibicao_completa.sort_values(by=coluna_ordenacao, ascending=True)
            elif direcao == 'desc':
                df_exibicao_completa = df_exibicao_completa.sort_values(by=coluna_ordenacao, ascending=False)
            else:
                df_exibicao_completa = df_exibicao_completa.sort_index()
        else:
            df_exibicao_completa = df_exibicao_completa.sort_index()
        
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
        
        # ===== BOTÕES DE ORDENAÇÃO =====
        st.subheader("📊 Ordenação")
        col_ord1, col_ord2, col_ord3, col_ord4 = st.columns(4)
        
        with col_ord1:
            if st.button("🔤 Médico (A→Z)", use_container_width=True):
                if st.session_state.ordem_coluna == 'Médico' and st.session_state.ordem_direcao == 'asc':
                    st.session_state.ordem_direcao = 'desc'
                else:
                    st.session_state.ordem_coluna = 'Médico'
                    st.session_state.ordem_direcao = 'asc'
                st.rerun()
        
        with col_ord2:
            if st.button("🔤 Médico (Z→A)", use_container_width=True):
                if st.session_state.ordem_coluna == 'Médico' and st.session_state.ordem_direcao == 'desc':
                    st.session_state.ordem_coluna = None
                    st.session_state.ordem_direcao = None
                else:
                    st.session_state.ordem_coluna = 'Médico'
                    st.session_state.ordem_direcao = 'desc'
                st.rerun()
        
        with col_ord3:
            if st.button("🏥 Local (A→Z)", use_container_width=True):
                if st.session_state.ordem_coluna == 'Local' and st.session_state.ordem_direcao == 'asc':
                    st.session_state.ordem_direcao = 'desc'
                else:
                    st.session_state.ordem_coluna = 'Local'
                    st.session_state.ordem_direcao = 'asc'
                st.rerun()
        
        with col_ord4:
            if st.button("🔄 Resetar Ordem", use_container_width=True):
                st.session_state.ordem_coluna = None
                st.session_state.ordem_direcao = None
                st.rerun()
        
        st.markdown("---")
        
        # ===== GERENCIADOR DE COLUNAS =====
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("📋 Gerenciar Colunas", type="secondary", use_container_width=True):
                st.session_state.mostrar_gerenciador_colunas = not st.session_state.mostrar_gerenciador_colunas
                st.rerun()
        
        if st.session_state.mostrar_gerenciador_colunas:
            st.markdown("---")
            st.subheader("📋 Selecionar Colunas para Exibir")
            
            cols_check = st.columns(min(len(nomes_colunas), 6))
            for i, col_nome in enumerate(nomes_colunas):
                col_idx = i % len(cols_check)
                with cols_check[col_idx]:
                    is_checked = col_nome in st.session_state.colunas_selecionadas
                    checked = st.checkbox(
                        col_nome,
                        value=is_checked,
                        key=f"col_{col_nome}"
                    )
                    if checked and col_nome not in st.session_state.colunas_selecionadas:
                        st.session_state.colunas_selecionadas.append(col_nome)
                    elif not checked and col_nome in st.session_state.colunas_selecionadas:
                        st.session_state.colunas_selecionadas.remove(col_nome)
            
            col_sel1, col_sel2, col_sel3, col_sel4 = st.columns(4)
            with col_sel1:
                if st.button("✅ Selecionar Todas", use_container_width=True, key="btn_selecionar_todas"):
                    st.session_state.colunas_selecionadas = nomes_colunas.copy()
                    st.rerun()
            with col_sel2:
                if st.button("⬜ Desmarcar Todas", use_container_width=True, key="btn_desmarcar_todas"):
                    st.session_state.colunas_selecionadas = []
                    st.rerun()
            with col_sel3:
                if st.button("👀 Modo Rápido", use_container_width=True, key="btn_modo_rapido"):
                    st.session_state.colunas_selecionadas = ['Médico', 'Horário de Atendimento']
                    st.rerun()
            with col_sel4:
                if st.button("📋 Modo Completo", use_container_width=True, key="btn_modo_completo"):
                    st.session_state.colunas_selecionadas = nomes_colunas.copy()
                    st.rerun()
            
            st.markdown("---")
        
        # ===== TABELA =====
        if medico_busca:
            st.subheader(f"📋 Resultados da busca por '{medico_busca}' ({len(df_exibicao_completa)} encontrados)")
        else:
            st.subheader(f"📋 Lista de Médicos ({len(df_exibicao_completa)} encontrados)")
        
        if st.session_state.ordem_coluna:
            direcao_texto = "crescente" if st.session_state.ordem_direcao == 'asc' else "decrescente"
            st.caption(f"📌 Ordenado por: **{st.session_state.ordem_coluna}** ({direcao_texto})")
        
        colunas_exibir = st.session_state.colunas_selecionadas if st.session_state.colunas_selecionadas else ['Médico', 'Horário de Atendimento']
        colunas_existentes = [col for col in colunas_exibir if col in df_exibicao_completa.columns]
        
        if not colunas_existentes:
            st.warning("⚠️ Nenhuma coluna selecionada. Mostrando colunas padrão.")
            colunas_existentes = ['Médico', 'Horário de Atendimento']
        
        df_exibicao = df_exibicao_completa[colunas_existentes + ['_idx_original']].copy()
        
        for col in df_exibicao.columns:
            if col != '_idx_original':
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
            elif col == 'Endereço':
                column_config[col] = st.column_config.TextColumn("📍 Endereço", width="medium")
            elif col == 'Número':
                column_config[col] = st.column_config.TextColumn("🔢 Número", width="small")
            elif col == 'Complemento':
                column_config[col] = st.column_config.TextColumn("📝 Complemento", width="medium")
            elif col == 'Bairro':
                column_config[col] = st.column_config.TextColumn("🏘️ Bairro", width="small")
            elif col == 'Cidade':
                column_config[col] = st.column_config.TextColumn("📍 Cidade", width="small")
            elif col == 'UF':
                column_config[col] = st.column_config.TextColumn("📌 UF", width="small")
            elif col == 'CEP':
                column_config[col] = st.column_config.TextColumn("📮 CEP", width="medium")
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
            else:
                column_config[col] = st.column_config.TextColumn(col, width="medium")
        
        column_config['_idx_original'] = None
        
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
        
        # ===== SALVAR ALTERAÇÕES =====
        col_salvar1, col_salvar2, col_salvar3 = st.columns([1, 2, 1])
        with col_salvar2:
            if st.button("💾 Salvar Alterações da Tabela", type="primary", use_container_width=True):
                try:
                    for idx, row in edited_df.iterrows():
                        if '_idx_original' in row and pd.notna(row['_idx_original']):
                            id_original = int(row['_idx_original'])
                            if id_original < len(df):
                                for col in colunas_existentes:
                                    if col in row:
                                        valor = row[col]
                                        if pd.isna(valor):
                                            valor = ''
                                        df.loc[id_original, col] = str(valor)
                    
                    st.session_state.df = df
                    st.success("✅ Alterações salvas com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao salvar: {str(e)}")
        
        st.markdown("---")
        
        # ===== SELEÇÃO E AÇÕES =====
        st.subheader("👤 Selecionar Médico para Ações Rápidas")
        
        medicos_lista = [''] + df_exibicao_completa['Médico'].tolist()
        medico_escolhido = st.selectbox("Selecione um médico:", medicos_lista)
        
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
- **CEP:** {get_val('CEP')}

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
        st.caption("📌 A planilha será exportada com **TODAS AS COLUNAS** (mantendo compatibilidade) e na **ORDEM ATUAL** da tabela")
        
        col_exp1, col_exp2, col_exp3, col_exp4, col_exp5 = st.columns(5)
        
        with col_exp1:
            if st.button("📥 Filtrados", type="primary", use_container_width=True):
                if len(df_exibicao_completa) > 0:
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        colunas_originais = [col for col in df.columns if col not in ['_idx_original']]
                        df_para_exportar = df_exibicao_completa[colunas_originais].copy()
                        if '_idx_original' in df_para_exportar.columns:
                            df_para_exportar = df_para_exportar.drop(columns=['_idx_original'])
                        df_para_exportar.to_excel(writer, sheet_name='Ariana Martins - Cadastro_Medic', index=False)
                    
                    st.download_button(
                        label=f"📥 {len(df_exibicao_completa)} médicos",
                        data=output.getvalue(),
                        file_name=f"filtrados_ordenados_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="download_filtrados"
                    )
                else:
                    st.warning("⚠️ Nenhum médico nos filtros")
        
        with col_exp2:
            if st.button("📥 Todos", type="secondary", use_container_width=True):
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    colunas_originais = [col for col in df.columns if col not in ['_idx_original']]
                    df_para_exportar = df[colunas_originais].copy()
                    df_para_exportar.to_excel(writer, sheet_name='Ariana Martins - Cadastro_Medic', index=False)
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
                        colunas_originais = [col for col in df.columns if col not in ['_idx_original']]
                        df_para_exportar = df_visitados[colunas_originais].copy()
                        df_para_exportar.to_excel(writer, sheet_name='Ariana Martins - Cadastro_Medic', index=False)
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
                        colunas_originais = [col for col in df.columns if col not in ['_idx_original']]
                        df_para_exportar = df_a_visitar[colunas_originais].copy()
                        df_para_exportar.to_excel(writer, sheet_name='Ariana Martins - Cadastro_Medic', index=False)
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
                    colunas_originais = [col for col in df.columns if col not in ['_idx_original']]
                    df_para_exportar = df[colunas_originais].copy()
                    df_para_exportar.to_excel(writer, sheet_name='Ariana Martins - Cadastro_Medic', index=False)
                st.download_button(
                    label="📥 Backup completo",
                    data=output.getvalue(),
                    file_name=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_backup"
                )

# ===== INICIALIZAÇÃO =====
inicializar_estados()

if st.session_state.pagina_atual == 'adicionar':
    pagina_adicionar_medico()
else:
    pagina_principal()