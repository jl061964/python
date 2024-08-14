import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Função para carregar e ajustar os dados
def carregar_dados():
    # Defina o caminho do OneDrive
    caminho_onedrive = r"C:\Users\braga\OneDrive - Rodenstock Brasil Industria Optica Ltda"

    # Carregue os arquivos usando o caminho completo
    clientes_df = pd.read_excel(f"{caminho_onedrive}\\estatistica_clientes.xlsx", engine='openpyxl')
    vendas_credito_df = pd.read_excel(f"{caminho_onedrive}\\Vendas_Credito.xlsx", engine='openpyxl')


    # Corrigir os nomes das colunas
    clientes_df.columns = [
        "Inativo", "Não.", "Empresa", "Cliente ", "Fantasia", "Referência", "Vencimento",
        "Vl.liquido", "TD", "Nr.docto", "Dt.pagto", "Vl.pagamento", "TP", "Nr.pagamento",
        "Conta", "Dt.Emissão", "Cobrança", "Modelo", "Negociação", "Duplicata", "Razão Social",
        "CNPJ/CPF", "PDD"
    ]

    vendas_credito_df.columns = [
        "Não.", "Empresa", "Cliente1", "Fantasia1", "Referência", "Vencimento1", "Vl.liquido1",
        "TD", "Nr.docto", "Dt.pagto", "Vl.pagamento", "TP", "Nr.pagamento", "Conta", "Dt.Emissão1",
        "Cobrança", "Negociação", "Razão Social", "CNPJ/CPF", "PDD"
    ]

    # Cria uma nova coluna combinando "Cliente" e "Fantasia"
    clientes_df["Cliente_Fantasia"] = clientes_df.apply(lambda row: f"{row['Cliente ']} - {row['Fantasia']}", axis=1)

    return clientes_df, vendas_credito_df

def main():
    st.title("Análise de Clientes")
    st.sidebar.title("Filtros")

    # Carregar os dados
    clientes_df, vendas_credito_df = carregar_dados()

    # Exibe a lista suspensa com as opções de cliente + fantasia
    opcoes = clientes_df["Cliente_Fantasia"].unique().tolist()
    escolha = st.sidebar.selectbox("Escolha um Cliente_Fantasia:", ["Selecione um cliente"] + opcoes)

    if escolha == "Selecione um cliente":
        st.warning("Por favor, selecione um cliente.")
        return

    # Filtra os dados com base na escolha do usuário
    clientes_filtrados = clientes_df[clientes_df["Cliente_Fantasia"] == escolha].copy()

    # Converte as colunas de data
    for coluna in ["Vencimento", "Dt.Emissão"]:
        clientes_filtrados[coluna] = pd.to_datetime(clientes_filtrados[coluna], errors='coerce')

    # Filtra os dados de vendas a crédito para o cliente selecionado
    cliente_nome = clientes_filtrados["Cliente "].iloc[0]
    vendas_cliente = vendas_credito_df[vendas_credito_df["Cliente1"] == cliente_nome].copy()

    # Converte as colunas de data em vendas a crédito
    for coluna in ["Dt.Emissão1"]:
        vendas_cliente[coluna] = pd.to_datetime(vendas_cliente[coluna], errors='coerce')

    hoje = pd.Timestamp.today()

    # Filtra valores vencidos e a vencer
    valores_vencidos = clientes_filtrados[clientes_filtrados["Vencimento"] < hoje]
    valores_a_vencer = clientes_filtrados[clientes_filtrados["Vencimento"] >= hoje]

    # Cálculo dos totais
    total_vencidos = valores_vencidos["Vl.liquido"].sum()
    total_a_vencer = valores_a_vencer["Vl.liquido"].sum()
    total_geral = total_vencidos + total_a_vencer

    # Exibe os totais
    st.write(f"**Total de registros vencidos:** {len(valores_vencidos)}")
    st.write(f"**Total de registros a vencer:** {len(valores_a_vencer)}")
    st.write(f"**Total Vencidos:** R$ {total_vencidos:,.2f}")
    st.write(f"**Total A Vencer:** R$ {total_a_vencer:,.2f}")
    st.write(f"**Total Geral:** R$ {total_geral:,.2f}")

    # Alertas baseados nos totais
    if total_vencidos > total_a_vencer:
        st.error("Atenção: Títulos vencidos são maiores que títulos a vencer!")
    elif total_vencidos < total_a_vencer:
        st.success("Títulos a vencer são maiores que títulos vencidos.")
    else:
        st.info("Títulos vencidos e títulos a vencer são iguais.")

    # Cálculo dos percentuais
    percentual_vencidos = (total_vencidos / total_geral * 100) if total_geral > 0 else 0
    percentual_a_vencer = (total_a_vencer / total_geral * 100) if total_geral > 0 else 0

    st.write(f"**Montante de Vencidos:** R$ {total_vencidos:,.2f} ({percentual_vencidos:.2f}% do total)")
    st.write(f"**Montante de A Vencer:** R$ {total_a_vencer:,.2f} ({percentual_a_vencer:.2f}% do total)")

    # Cálculo do prazo médio de faturamento ponderado
    clientes_filtrados["Prazo"] = (clientes_filtrados["Vencimento"] - clientes_filtrados["Dt.Emissão"]).dt.days
    prazo_medio_ponderado = (clientes_filtrados["Prazo"] * clientes_filtrados["Vl.liquido"]).sum() / clientes_filtrados["Vl.liquido"].sum()
    st.write(f"**Prazo Médio de Faturamento (ponderado):** {prazo_medio_ponderado:.2f} dias")

    # Cálculo do faturamento diário médio (ADP)
    dias_no_periodo = (vendas_cliente["Dt.Emissão1"].max() - vendas_cliente["Dt.Emissão1"].min()).days
    if dias_no_periodo > 0:
        faturamento_diario_medio = vendas_cliente["Vl.liquido1"].sum() / dias_no_periodo
    else:
        faturamento_diario_medio = 0

    # Cálculo do DSO
    contas_receber_total = clientes_filtrados["Vl.liquido"].sum()
    if faturamento_diario_medio > 0:
        DSO = contas_receber_total / faturamento_diario_medio
    else:
        DSO = 0

    st.write(f"**DSO (Days Sales Outstanding) para o cliente selecionado:** {DSO:.2f} dias")

    # Cálculo do CEI (Collection Effectiveness Index)
    total_vendas_credito = vendas_cliente["Vl.liquido1"].sum()
    total_pagamentos_recebidos = vendas_cliente["Vl.pagamento"].sum()
    if total_vendas_credito > 0:
        CEI = (total_pagamentos_recebidos / total_vendas_credito) * 100
    else:
        CEI = 0

    st.write(f"**CEI (Collection Effectiveness Index) para o cliente selecionado:** {CEI:.2f}%")

    # Gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(["Vencidos", "A Vencer"], [total_vencidos, total_a_vencer])
    ax.set_ylabel("Valor Total")
    ax.set_title(f"Valores Vencidos vs. Valores a Vencer para {escolha}")

    st.pyplot(fig)

if __name__ == "__main__":
    main()
