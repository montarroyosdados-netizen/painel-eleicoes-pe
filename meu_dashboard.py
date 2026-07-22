import streamlit as st
import pandas as pd

# Configuração da página do site
st.set_page_config(page_title="Eleições PE", layout="wide")
st.title("📊 Painel Eleitoral - Pernambuco (2002-2024)")

# Carrega os dados uma vez só
@st.cache_data
def carregar_dados():
    return pd.read_csv('dados_eleitorais_pe_completo_2002_2024.csv', sep=';', encoding='utf-8-sig')

df = carregar_dados()

# Filtros
col1, col2 = st.columns(2)
with col1:
    ano_selecionado = st.selectbox("Selecione o Ano:", sorted(df['Ano'].dropna().unique(), reverse=True))
with col2:
    candidato_busca = st.text_input("Digite o nome do Candidato:").strip().upper()

# Regra de busca
if candidato_busca:
    filtro = df[(df['Ano'] == ano_selecionado) & (df['Candidato'].str.contains(candidato_busca, na=False))]
    
    if filtro.empty:
        st.warning(f"Nenhum registro encontrado para '{candidato_busca}' em {ano_selecionado}.")
        st.info("💡 Dica: Verifique os acentos. O sistema diferencia 'JOÃO' de 'JOAO'.")
    else:
        # Agrupa os votos garantindo que a coluna Candidato volte a aparecer
        resultado = filtro.groupby(['Candidato', 'Município', 'Cargo', 'Partido'])['Votos'].sum().reset_index()
        resultado = resultado.sort_values(by='Votos', ascending=False)
        
        # Mostra o resumo com o total de votos e o número exato de cidades
        st.success(f"Votação em {ano_selecionado}: {resultado['Votos'].sum():,.0f} votos recebidos em {len(resultado)} cidades.".replace(',', '.'))
        
        # height=600 força o painel a mostrar uma tabela muito maior na tela
        st.dataframe(resultado, use_container_width=True, hide_index=True, height=600)