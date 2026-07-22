import pandas as pd
import streamlit as st

st.set_page_config(page_title="Painel Eleitoral de Pernambuco", layout="wide")

st.title("🦁 Painel Eleitoral de Pernambuco")


@st.cache_data
def carregar_dados():
  caminho_arquivo = "dados_eleitorais_pe_completo_2002_2024.csv"

  # Tentativa 1: Padrão TSE Brasil (separador ';' e codificação latin1)
  try:
    df = pd.read_csv(
        caminho_arquivo,
        sep=";",
        encoding="latin1",
        on_bad_lines="skip",
        low_memory=False,
    )
  except Exception:
    # Tentativa 2: Padrão vírgula e UTF-8
    try:
      df = pd.read_csv(
          caminho_arquivo,
          sep=",",
          encoding="utf-8",
          on_bad_lines="skip",
          low_memory=False,
      )
    except Exception:
      # Tentativa 3: Leitura com motor Python flexível
      df = pd.read_csv(
          caminho_arquivo,
          sep=None,
          engine="python",
          on_bad_lines="skip",
          encoding="latin1",
      )

  # Padroniza os nomes das colunas para evitar incompatibilidade
  df.columns = [str(c).strip().upper() for c in df.columns]
  return df


df = carregar_dados()

# Localiza a coluna de ano de forma garantida
col_ano = "ANO" if "ANO" in df.columns else df.columns[0]

st.sidebar.header("Filtros")
anos = sorted(df[col_ano].dropna().unique(), reverse=True)
ano_sel = st.sidebar.selectbox("Ano Eleitoral", anos)

df_filtrado = df[df[col_ano] == ano_sel]

st.metric(
    "Total de Registros no Ano", f"{len(df_filtrado):,}".replace(",", ".")
)
st.dataframe(df_filtrado, use_container_width=True)