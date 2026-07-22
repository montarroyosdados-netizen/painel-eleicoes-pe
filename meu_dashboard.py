import pandas as pd
import streamlit as st

# ==========================================
# CONFIGURAÇÃO DA PÁGINA (MODERNO E RESPONSIVO)
# ==========================================
st.set_page_config(
    page_title="Painel Eleitoral de Pernambuco",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# DESIGN SYSTEM: AS CORES DE PERNAMBUCO (MODERNO)
# ==========================================
PRIMARY_COLOR = "#002D62"  # Azul profundo do mar de Pernambuco
ACCENT_COLOR = "#FFD700"  # Amarelo ouro do Leão do Norte
SECONDARY_ACCENT = "#D32F2F"  # Vermelho vibrante
BG_COLOR = "#F4F7F6"

st.markdown(
    f"""
    <style>
        /* Estilização geral inspirada no design corporativo moderno */
        .main {{
            background-color: {BG_COLOR};
        }}
        .stMetric {{
            background-color: #ffffff;
            padding: 18px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            border-left: 5px solid {ACCENT_COLOR};
        }}
        .stMetric label {{
            color: #555555 !important;
            font-weight: 600;
        }}
        .stMetric [data-testid="stMetricValue"] {{
            color: {PRIMARY_COLOR} !important;
            font-weight: 700;
        }}
        h1, h2, h3 {{
            color: {PRIMARY_COLOR};
            font-family: 'Helvetica Neue', sans-serif;
        }}
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
# CARREGAMENTO DOS DADOS COM CACHE
# ==========================================
@st.cache_data
def carregar_dados():
  try:
    df = pd.read_csv("dados_eleitorais_pe_completo_2002_2024.csv")
    return df
  except FileNotFoundError:
    return None


df = carregar_dados()

# ==========================================
# CABEÇALHO MODERNO ESTILO PERNAMBUCO
# ==========================================
st.markdown(
    """
    <div class="card-pe">
        <h1 style="color: #FFD700; margin: 0; font-size: 2.5rem;">🦁 Painel Eleitoral de Pernambuco</h1>
        <p style="margin-top: 10px; font-size: 1.1rem; color: #E2E8F0;">
            Análise interativa dos pleitos eleitorais no Estado de Pernambuco de 2002 a 2024. 
            Desenvolvido com foco em Inteligência de Dados.
        </p>
    </div>
""",
    unsafe_allow_html=True,
)

if df is None:
  st.error(
      "Atenção: O arquivo `dados_eleitorais_pe_completo_2002_2024.csv` não foi"
      " encontrado na mesma pasta do código. Verifique o envio no GitHub."
  )
else:
  # ==========================================
  # BARRA LATERAL (FILTROS INTELIGENTES)
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
    anos_unicos = sorted(df[anos_col].unique(), reverse=True)
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
  # MÉTRICAS PRINCIPAIS (KPIs)
  # ==========================================
  st.markdown("### 📊 Visão Geral do Pleito")
  kpi1, kpi2, kpi3 = st.columns(3)

  with kpi1:
    total_linhas = len(df_filtrado)
    st.metric("Registros Filtrados", f"{total_linhas:,}".replace(",", "."))

  with kpi2:
    if "VOTOS" in [c.upper() for c in df_filtrado.columns]:
      col_votos = [c for c in df_filtrado.columns if c.upper() == "VOTOS"][0]
      total_votos = df_filtrado[col_votos].sum()
      st.metric(
          "Total de Votos Analisados", f"{total_votos:,}".replace(",", ".")
      )
    else:
      st.metric("Total de Registros", len(df_filtrado))

  with kpi3:
    if municipios_col:
      total_mun = df_filtrado[municipios_col].nunique()
      st.metric("Municípios Abrangidos", total_mun)
    else:
      st.metric("Status da Base", "Ativa na Nuvem")

  st.markdown("---")

  # ==========================================
  # EXIBIÇÃO DE DADOS E GRÁFICOS MODERNOS
  # ==========================================
  col_grafico, col_tabela = st.columns([1, 1])

  with col_grafico:
    st.subheader("📈 Análise Gráfica")
    candidato_col = next(
        (c for c in colunas_disponiveis if "candidato" in c.lower()), None
    )
    votos_col = next((c for c in colunas_disponiveis if "voto" in c.lower()), None)

    if candidato_col and votos_col:
      top_candidatos = (
          df_filtrado.groupby(candidato_col)[votos_col]
          .sum()
          .reset_index()
          .sort_values(by=votos_col, ascending=False)
          .head(10)
      )
      st.bar_chart(top_candidatos.set_index(candidato_col)[votos_col])
    else:
      st.info(
          "Selecione os filtros na barra lateral para detalhar o comportamento"
          " gráfico."
      )

  with col_tabela:
    st.subheader("📋 Amostra de Dados Detalhada")
    st.dataframe(df_filtrado.head(50), use_container_width=True)

  # Rodapé elegante
  st.markdown("---")
  st.markdown(
      "<p style='text-align: center; color: #718096; font-size: 0.9rem;'>Painel"
      " Eleitoral de Pernambuco — Desenvolvido em Python & Streamlit Cloud</p>",
      unsafe_allow_html=True,
  )