import pandas as pd
import streamlit as st

st.set_page_config(page_title="Painel Eleitoral de Pernambuco", layout="wide")

st.title("Painel Eleitoral de Pernambuco")


@st.cache_data
def carregar_dados():
  df = pd.read_csv("dados_eleitorais_pe_completo_2002_2024.csv")
  return df


df = carregar_dados()

st.sidebar.header("Filtros")
anos = sorted(df["ANO"].unique(), reverse=True)
ano_sel = st.sidebar.selectbox("Ano", anos)

df_filtrado = df[df["ANO"] == ano_sel]

st.metric("Total de Registros", len(df_filtrado))
st.dataframe(df_filtrado)

