import pandas as pd
import streamlit as st

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Painel Eleitoral de Pernambuco",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# DESIGN SYSTEM: CORES DE PERNAMBUCO
# ==========================================
PRIMARY_COLOR = "#002D62"
ACCENT_COLOR = "#FFD700"
BG_COLOR = "#F4F7F6"

st.markdown(
    f"""
    <style>
        .main {{ background-color: {BG_COLOR}; }}
        .stMetric {{
            background-color: #ffffff;
            padding: 18px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            border-left: 5px solid {ACCENT_COLOR};
        }}
        .stMetric label {{ color: #555555 !important; font-weight: 600; }}
        .stMetric [data-testid="stMetricValue"] {{ color: {PRIMARY_COLOR} !important; font-weight: 700; }}
        h1, h2, h3 {{ color: {PRIMARY_COLOR}; font-family: 'Helvetica Neue', sans-serif; }}
        .card-pe {{
            background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, #1A365D 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            margin-bottom: 25px;
        }}
    </style>
""",
    unsafe_allow_html=True,
)


# ==========================================
# CARREGAMENTO BLINDADO DOS DADOS
# ==========================================
@st.cache_data
def carregar_dados():
  try:
    # Leitura otimizada e tolerante a falhas de formatação no CSV grande
    df = pd.read_csv(
        "dados_eleitorais_pe_completo_2002_2024.csv",
        low_memory=False,
        on_bad_lines="skip",
    )
    return df
  except Exception as e:
    st.error(f"Erro ao carregar o CSV: {e}")
    return None


df = carregar_dados()

# ==========================================
# CABEÇALHO
# ==========================================
st.markdown(
    """
    <div class="card-pe">
        <h1 style="color: #FFD700; margin: 0; font-size: 2.5rem;">🦁 Painel Eleitoral de Pernambuco</h1>
        <p style="margin-top: 10px; font-size: 1.1rem; color: #E2E8F0;">
            Análise interativa dos pleitos eleitorais no Estado de Pernambuco de 2002 a 2024.
        </p>
    </div>
""",
    unsafe_allow_html=True,
)

if df is None or df.empty:
  st.warning(
      "O arquivo de dados não pôde ser lido corretamente. Verifique se o"
      " arquivo CSV está na pasta."
  )
else:
  # ==========================================
  # FILTROS DA BARRA LATERAL
  # ==========================================
  st.sidebar.markdown("### ⚙️ Filtros do Painel")
  colunas_disponiveis = df.columns.tolist()

  anos_col = next((c for c in colunas_disponiveis if "ano" in c.lower()), None)
  cargos_col = next(
      (c for c in colunas_disponiveis if "cargo" in c.lower()), None
  )
  municipios_col = next(
      (c for c in colunas_disponiveis if "municipio" in c.lower()), None
  )

  df_filtrado = df.copy()
  st.sidebar.markdown("---")

  if anos_col:
    anos_unicos = sorted(df[anos_col].dropna().unique(), reverse=True)
    ano_selecionado = st.sidebar.selectbox(
        "📅 Selecione o Ano Eleitoral", ["Todos"] + list(anos_unicos)
    )
    if ano_selecionado != "Todos":
      df_filtrado = df_filtrado[df_filtrado[anos_col] == ano_selecionado]

  if cargos_col:
    cargos_unicos = sorted(df[cargos_col].dropna().unique())
    cargo_selecionado = st.sidebar.selectbox(
        "🏛️ Selecione o Cargo", ["Todos"] + list(cargos_unicos)
    )
    if cargo_selecionado != "Todos":
      df_filtrado = df_filtrado[df_filtrado[cargos_col] == cargo_selecionado]

  # ==========================================
  # KPIs (MÉTRICAS)
  # ==========================================
  st.markdown("### 📊 Visão Geral do Pleito")
  kpi1, kpi2, kpi3 = st.columns(3)

  with kpi1:
    st.metric(
        "Registros Filtrados",
        f"{len(df_filtrado):,}".replace(",", "."),
    )

  with kpi2:
    votos_col_nome = next(
        (c for c in df_filtrado.columns if "voto" in c.lower()), None
    )
    if votos_col_nome:
      total_votos = pd.to_numeric(
          df_filtrado[votos_col_nome], errors="coerce"
      ).sum()
      st.metric("Total de Votos", f"{int(total_votos):,}".replace(",", "."))
    else:
      st.metric("Total de Linhas", len(df_filtrado))

  with kpi3:
    if municipios_col:
      st.metric("Municípios", df_filtrado[municipios_col].nunique())
    else:
      st.metric("Status", "Online")

  st.markdown("---")

  # ==========================================
  # GRÁFICOS E TABELA
  # ==========================================
  col_grafico, col_tabela = st.columns([1, 1])

  with col_grafico:
    st.subheader("📈 Análise Gráfica")
    candidato_col = next(
        (c for c in colunas_disponiveis if "candidato" in c.lower()), None
    )
    if candidato_col and votos_col_nome:
      top_cand = (
          df_filtrado.groupby(candidato_col)[votos_col_nome]
          .sum()
          .reset_index()
          .sort_values(by=votos_col_nome, ascending=False)
          .head(10)
      )
      st.bar_chart(top_cand.set_index(candidato_col)[votos_col_nome])
    else:
      st.info("Filtre os dados para exibir o gráfico.")

  with col_tabela:
    st.subheader("📋 Amostra de Dados Detalhada")
    st.dataframe(df_filtrado.head(50), use_container_width=True)

  st.markdown("---")
  st.markdown(
      "<p style='text-align: center; color: #718096; font-size: 0.9rem;'>Painel"
      " Eleitoral de Pernambuco — Python & Streamlit</p>",
      unsafe_allow_html=True,
  )