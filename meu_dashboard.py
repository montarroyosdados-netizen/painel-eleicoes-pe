import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Painel Eleitoral de Pernambuco", layout="wide")

st.title("🦁 Painel Eleitoral de Pernambuco")


@st.cache_data
def carregar_dados():
  # Procura pelo arquivo CSV independentemente de maiúsculas/minúsculas
  arquivos = os.listdir(".")
  csv_encontrado = None
  for f in arquivos:
    if f.lower().endswith(".csv"):
      csv_encontrado = f
      break

  if csv_encontrado:
    return pd.read_csv(csv_encontrado, low_memory=False)
  return None


df = carregar_dados()

if df is None:
  st.error("Erro: Nenhum arquivo CSV foi encontrado na pasta do projeto.")
else:
  # Identifica automaticamente a coluna de ano
  col_ano = next((c for c in df.columns if "ano" in c.lower()), df.columns[0])

  st.sidebar.header("Filtros")
  anos = sorted(df[col_ano].dropna().unique(), reverse=True)
  ano_sel = st.sidebar.selectbox("Ano", anos)

  df_filtrado = df[df[col_ano] == ano_sel]

  st.metric("Total de Registros", f"{len(df_filtrado):,}".replace(",", "."))
  st.dataframe(df_filtrado, use_container_width=True)