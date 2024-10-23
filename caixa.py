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

# Função para baixar o arquivo Excel com senha
def download_excel_with_password(filename='sugestoes.xlsx'):
    password = st.text_input('Digite a senha para baixar o arquivo Excel', type='password')
    if password == 'RBR2024':  # Senha definida como "RBR2024"
        with open(filename, 'rb') as f:
            st.download_button('Baixar arquivo Excel', f, file_name=filename)
        return True
    elif password:
        st.error('Senha incorreta. Por favor, tente novamente.')
    return False

# Função para limpar o arquivo de sugestões
def clear_excel_file(filename='sugestoes.xlsx'):
    df = pd.DataFrame(columns=['Nome', 'função', 'Setor', 'Sugestão', 'Possível Melhoria', 'Custo Estimado', 'Economia Prevista(Se não for quantificavel, descrever beneficios para a empresa.)'])
    df.to_excel(filename, index=False)
    st.write(f'Arquivo {filename} limpo com sucesso!')

# Aplicativo Streamlit
st.title('Sistema de Sugestões   "RODENSTOCK"')

# Carrega sugestões existentes do arquivo Excel
sugestoes = load_from_excel()

# Inicializa o estado da sessão com as sugestões carregadas
if 'sugestoes' not in st.session_state:
    st.session_state.sugestoes = sugestoes

# Formulário para coletar dados do usuário
with st.form(key='sugestao_form'):
    nome = st.text_input('Nome')
    funcao = st.text_input('Função')
    setor = st.text_input('Setor')
    sugestao = st.text_area('Sugestão')
    melhoria = st.text_area('Possível Melhoria')
    custo_estimado = st.number_input('Custo Estimado', min_value=0.0, format="%.2f")
    economia_prevista = st.text_area('Economia Prevista(Se não for quantificavel, descrever beneficios para a empresa.)')  # Novo campo de texto
    
    submit_button = st.form_submit_button(label='Enviar')

# Lida com o envio do formulário
if submit_button:
    nova_sugestao = {
        'Nome': nome,
        'Função': funcao,
        'Setor': setor,
        'Sugestão': sugestao,
        'Possível Melhoria': melhoria,
        'Custo Estimado': custo_estimado,
        'Economia Prevista(Se não for quantificavel, descrever beneficios para a empresa.)': economia_prevista  # Novo campo de texto
    }
    
    st.session_state.sugestoes.append(nova_sugestao)
    
    save_to_excel(st.session_state.sugestoes)
    
    st.success('Sugestão enviada com sucesso!')

# Adiciona botão para baixar o arquivo Excel com senha e limpar o arquivo de sugestões
st.subheader('Baixar ou Limpar Arquivo Excel')
if download_excel_with_password():
    if st.button('Limpar Arquivo de Sugestões'):
        clear_excel_file()
