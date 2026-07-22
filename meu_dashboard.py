import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Painel Eleitoral de Pernambuco",
    page_icon="🦁",
    layout="wide",
)

st.title("🦁 Painel Eleitoral de Pernambuco")


@st.cache_data
def carregar_dados():
  # Procura o arquivo CSV na pasta atual independentemente de maiúsculas/minúsculas
  for f in os.listdir("."):
    if f.lower().endswith(".csv"):
      try:
        return pd.read_csv(f, low_memory=False, on_bad_lines="skip")
      except Exception:
        pass
  return None


df = carregar_dados()

if df is None:
  st.error(
      "Erro crítico: O arquivo CSV de dados não foi encontrado na pasta do"
      " projeto."
  )
else:
  # Normaliza os nomes das colunas para maiúsculo para evitar conflito
  df.columns = [str(c).strip().upper() for c in df.columns]

  # Identifica a coluna de ano
  col_ano = "ANO" if "ANO" in df.columns else df.columns[0]

  st.sidebar.header("Filtros")
  anos_disponiveis = sorted(df[col_ano].dropna().unique(), reverse=True)
  ano_selecionado = st.sidebar.selectbox("Selecione o Ano", anos_disponiveis)

  df_filtrado = df[df[col_ano] == ano_selecionado]

  st.metric(
      "Total de Registros no Ano", f"{len(df_filtrado):,}".replace(",", ".")
  )
  st.dataframe(df_filtrado, use_container_width=True)