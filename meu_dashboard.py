import pandas as pd
import streamlit as st

st.set_page_config(page_title="Painel Eleitoral de Pernambuco", layout="wide")

st.title("🦁 Painel Eleitoral de Pernambuco")


@st.cache_data
def carregar_dados():
  # Leitura padrão otimizada para o arquivo local
  df = pd.read_csv(
      "dados_eleitorais_pe_completo_2002_2024.csv",
      low_memory=False,
      on_bad_lines="skip",
  )
  # Padroniza nomes das colunas para maiúsculo
  df.columns = [str(c).strip().upper() for c in df.columns]
  return df


df = carregar_dados()

# Localiza a coluna de ano com segurança absoluta
col_ano = "ANO" if "ANO" in df.columns else df.columns[0]

# Garante que os valores da coluna de ano sejam tratados como números inteiros limpos
df[col_ano] = pd.to_numeric(df[col_ano], errors="coerce")
df = df.dropna(subset=[col_ano])
df[col_ano] = df[col_ano].astype(int)

st.sidebar.header("Filtros")
anos = sorted(df[col_ano].unique(), reverse=True)
ano_sel = st.sidebar.selectbox("Ano Eleitoral", anos)

# Filtro blindado
df_filtrado = df[df[col_ano] == int(ano_sel)]

st.metric(
    "Total de Registros no Ano", f"{len(df_filtrado):,}".replace(",", ".")
)
st.dataframe(df_filtrado, use_container_width=True)