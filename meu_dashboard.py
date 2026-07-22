import pandas as pd
import streamlit as st

st.set_page_config(page_title="Painel Eleitoral de Pernambuco", layout="wide")

st.title("🦁 Painel Eleitoral de Pernambuco")


@st.cache_data
def carregar_dados():
  df = pd.read_csv("dados_eleitorais_pe_completo_2002_2024.csv")
  # Padroniza todas as colunas para maiúsculo para evitar qualquer erro de digitação
  df.columns = [str(c).strip().upper() for c in df.columns]
  return df


df = carregar_dados()

# Garante que a coluna ANO existe de forma exata
col_ano = "ANO" if "ANO" in df.columns else df.columns[0]

st.sidebar.header("Filtros")
anos = sorted(df[col_ano].dropna().unique(), reverse=True)
ano_sel = st.sidebar.selectbox("Ano", anos)

df_filtrado = df[df[col_ano] == ano_sel]

st.metric("Total de Registros", f"{len(df_filtrado):,}".replace(",", "."))
st.dataframe(df_filtrado, use_container_width=True)