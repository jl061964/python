import streamlit as st
import pandas as pd
import os

# Função para salvar dados em um arquivo Excel
def save_to_excel(data, filename='sugestoes.xlsx'):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    st.write(f'Arquivo {filename} salvo com sucesso no diretório: {os.getcwd()}')

# Função para carregar dados de um arquivo Excel
def load_from_excel(filename='sugestoes.xlsx'):
    try:
        df = pd.read_excel(filename)
        return df.to_dict(orient='records')
    except FileNotFoundError:
        return []

# Função para baixar o arquivo Excel
def download_excel(filename='sugestoes.xlsx'):
    with open(filename, 'rb') as f:
        st.download_button('Baixar arquivo Excel', f, file_name=filename)

# Aplicativo Streamlit
st.title('Sistema de Sugestões')

# Solicita senha para acessar o arquivo Excel
password = st.text_input('Digite a senha para acessar o arquivo Excel', type='password')

# Verifica a senha
if password == 'sua_senha_segura':  # Substitua 'sua_senha_segura' pela senha desejada
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
        
        st.session_state.sugestoes.append(nova_sugestao)
        
        save_to_excel(st.session_state.sugestoes)
        
        st.success('Sugestão enviada com sucesso!')

    # Adiciona botão para baixar o arquivo Excel
    download_excel()
else:
    st.error('Senha incorreta. Por favor, tente novamente.')
