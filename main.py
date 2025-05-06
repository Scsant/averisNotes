import streamlit as st
import pandas as pd
from io import BytesIO

from src.loader import load_averis_file, load_fazendas_files
from src.processor import tratar_dados

st.set_page_config(page_title="NF-e Averis", layout="wide")

st.title("🚚 Tratamento de NF-e para Averis")

# Passo 1: Upload do arquivo Averis
st.markdown("### 1. Envie o arquivo `averis.xlsx`")
averis_file = st.file_uploader("Arquivo Averis", type=["xlsx"])

# Passo 2: Upload dos arquivos das fazendas
st.markdown("### 2. Envie os arquivos de emissão das fazendas")
fazenda_files = st.file_uploader("Arquivos das Fazendas", type=["xlsx"], accept_multiple_files=True)

# Passo 3: Seleção do mês
meses = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]
mes_nome = st.selectbox("Escolha o mês de emissão para filtrar os dados (somente 2025):", meses)
mes_numero = meses.index(mes_nome) + 1

# Processamento
if averis_file and fazenda_files:
    with st.spinner("Carregando arquivos..."):
        df_averis = load_averis_file(averis_file)
        df_fazendas = load_fazendas_files(fazenda_files)

    with st.spinner("Processando dados..."):
        df_resultado = tratar_dados(df_averis, df_fazendas, mes=mes_numero)

    st.success("✅ Dados processados com sucesso!")
    st.dataframe(df_resultado)

    # Função de conversão para Excel
    def convert_df_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()

    # Botão para download do Excel
    st.markdown("### 3. Baixe o resultado")
    excel_bytes = convert_df_to_excel(df_resultado)
    st.download_button(
        label="📥 Baixar planilha com situação",
        data=excel_bytes,
        file_name="averis_tratado.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("⚠️ Envie os dois tipos de arquivos acima para iniciar o processamento.")
