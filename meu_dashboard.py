import pandas as pd
import streamlit as st

st.set_page_config(page_title="Painel Eleitoral de Pernambuco", layout="wide")

st.title("🦁 Painel Eleitoral de Pernambuco")


@st.cache_data
def carregar_dados():
  df = pd.read_csv("dados_eleitorais_pe_completo_2002_2024.csv")
  return df


df = carregar_dados()

# Identifica automaticamente o nome correto da coluna de ano (maiúscula ou minúscula)
col_ano = next((c for c in df.columns if "ano" in c.lower()), "ANO")

st.sidebar.header("Filtros")
anos = sorted(df[col_ano].dropna().unique(), reverse=True)
ano_sel = st.sidebar.selectbox("Ano", anos)

df_filtrado = df[df[col_ano] == ano_sel]

st.metric("Total de Registros", f"{len(df_filtrado):,}".replace(",", "."))
st.dataframe(df_filtrado, use_container_width=True)