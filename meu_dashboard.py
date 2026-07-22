import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Painel Eleitoral de Pernambuco",
    page_icon="🦁",
    layout="wide",
)

PRIMARY_COLOR = "#002D62"
ACCENT_COLOR = "#FFD700"

st.markdown(
    f"""
    <style>
        .stMetric {{
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid {ACCENT_COLOR};
        }}
        h1, h2, h3 {{ color: {PRIMARY_COLOR}; }}
    </style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def carregar_dados():
  try:
    # on_bad_lines='skip' pula qualquer linha defeituosa do CSV gigantesco sem travar o app
    df = pd.read_csv(
        "dados_eleitorais_pe_completo_2002_2024.csv",
        low_memory=False,
        on_bad_lines="skip",
        encoding="utf-8",
    )
    return df
  except Exception:
    try:
      df = pd.read_csv(
          "dados_eleitorais_pe_completo_2002_2024.csv",
          low_memory=False,
          on_bad_lines="skip",
          encoding="latin1",
      )
      return df
    except Exception as e:
      st.error(f"Erro crítico ao ler o arquivo de dados: {e}")
      return None


df = carregar_dados()

st.title("🦁 Painel Eleitoral de Pernambuco")

if df is None:
  st.warning(
      "Aguardando o arquivo de dados ser processado corretamente no repositório."
  )
else:
  st.sidebar.markdown("### ⚙️ Filtros")

  # Identificação dinâmica de colunas
  cols = df.columns.tolist()
  ano_col = next((c for c in cols if "ano" in c.lower()), None)
  cargo_col = next((c for c in cols if "cargo" in c.lower()), None)
  voto_col = next((c for c in cols if "voto" in c.lower()), None)
  cand_col = next((c for c in cols if "candidato" in c.lower()), None)

  df_f = df.copy()

  if ano_col:
    anos = sorted(df[ano_col].dropna().unique(), reverse=True)
    sel_ano = st.sidebar.selectbox("Ano", ["Todos"] + list(anos))
    if sel_ano != "Todos":
      df_f = df_f[df_f[ano_col] == sel_ano]

  if cargo_col:
    cargos = sorted(df[cargo_col].dropna().unique())
    sel_cargo = st.sidebar.selectbox("Cargo", ["Todos"] + list(cargos))
    if sel_cargo != "Todos":
      df_f = df_f[df_f[cargo_col] == sel_cargo]

  # Métricas na tela
  k1, k2 = st.columns(2)
  k1.metric("Registros na Análise", f"{len(df_f):,}".replace(",", "."))

  if voto_col:
    total_v = pd.to_numeric(df_f[voto_col], errors="coerce").sum()
    k2.metric("Total de Votos", f"{int(total_v):,}".replace(",", "."))
  else:
    k2.metric("Colunas Totais", len(df_f.columns))

  st.markdown("---")

  # Exibição de dados limpos
  st.subheader("📋 Amostra dos Dados")
  st.dataframe(df_f.head(100), use_container_width=True)