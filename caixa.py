import streamlit as st
import pandas as pd

# Função para salvar dados em um arquivo Excel
def save_to_excel(data, filename='sugestoes.xlsx'):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

# Função para carregar dados de um arquivo Excel
def load_from_excel(filename='sugestoes.xlsx'):
    try:
        df = pd.read_excel(filename)
        return df.to_dict(orient='records')
    except FileNotFoundError:
        return []

# Aplicativo Streamlit
st.title('Sistema de Sugestões')

# Carrega sugestões existentes do arquivo Excel
sugestoes = load_from_excel()

# Inicializa o estado da sessão com as sugestões carregadas
if 'sugestoes' not in st.session_state:
    st.session_state.sugestoes = sugestoes

# Formulário para coletar dados do usuário
with st.form(key='sugestao_form'):
    nome = st.text_input('Nome')
    cargo = st.text_input('Cargo')
    setor = st.text_input('Setor')
    sugestao = st.text_area('Sugestão')
    melhoria = st.text_area('Possível Melhoria')
    custo_estimado = st.number_input('Custo Estimado', min_value=0.0, format="%.2f")
    
    submit_button = st.form_submit_button(label='Enviar')

# Lida com o envio do formulário
if submit_button:
    nova_sugestao = {
        'Nome': nome,
        'Cargo': cargo,
        'Setor': setor,
        'Sugestão': sugestao,
        'Possível Melhoria': melhoria,
        'Custo Estimado': custo_estimado
    }
    
    # Adiciona nova sugestão ao estado da sessão
    st.session_state.sugestoes.append(nova_sugestao)
    
    # Salva sugestões no arquivo Excel
    save_to_excel(st.session_state.sugestoes)
    
    st.success('Sugestão enviada com sucesso!')

# Exibe sugestões existentes (opcional)
if st.session_state.sugestoes:
    st.subheader('Sugestões Recebidas')
    for sugestao in st.session_state.sugestoes:
        st.write(sugestao)
