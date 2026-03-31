import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Gestão de Gastos", page_icon="📊")

st.title("📊 Gestão e Indicadores")

# 1. CONEXÃO E LEITURA
try:
    url_planilha = st.secrets["connections"]["gsheets"]["url"]
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url_planilha, ttl=0)
    
    # Converter a coluna Data para o formato datetime do Python
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# 2. FILTROS NA LATERAL (SIDEBAR)
st.sidebar.header("Filtros")

# Filtro de Período
data_inicio = st.sidebar.date_input("Data Início", df['Data'].min())
data_fim = st.sidebar.date_input("Data Fim", df['Data'].max())

# Filtro de Pagante e Criança
pagante_filtro = st.sidebar.multiselect("Pagante", options=df['Pagante'].unique(), default=df['Pagante'].unique())
crianca_filtro = st.sidebar.multiselect("Criança", options=df['Crianca'].unique(), default=df['Crianca'].unique())
tipo_filtro = st.sidebar.multiselect("Tipo de Gasto", options=df['TIPO'].unique(), default=df['TIPO'].unique())

# Aplicar Filtros
mask = (
    (df['Data'].dt.date >= data_inicio) & 
    (df['Data'].dt.date <= data_fim) &
    (df['Pagante'].isin(pagante_filtro)) &
    (df['Crianca'].isin(crianca_filtro)) &
    (df['TIPO'].isin(tipo_filtro))
)
df_filtrado = df.loc[mask]

# 3. INDICADORES (CARDS)
total_geral = df_filtrado['Valor'].sum()

c1, c2, c3 = st.columns(3)
c1.metric("Total no Período", f"R$ {total_geral:,.2f}")
c2.metric("Qtd. Lançamentos", len(df_filtrado))
c3.metric("Média por Gasto", f"R$ {df_filtrado['Valor'].mean() if len(df_filtrado) > 0 else 0:,.2f}")

st.markdown("---")

# 4. ANÁLISES VISUAIS
st.markdown("### 📊 Detalhamento dos Gastos")
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Gastos por Criança")
    gastos_crianca = df_filtrado.groupby("Crianca")["Valor"].sum().reset_index()
    # Usando Plotly para Barras
    fig_barra = px.bar(gastos_crianca, x="Crianca", y="Valor", 
                       text_auto='.2s', title="Total por Filho(a)")
    st.plotly_chart(fig_barra, use_container_width=True)

with col_graf2:
    st.subheader("Divisão por Pagante")
    gastos_pagante = df_filtrado.groupby("Pagante")["Valor"].sum().reset_index()
    # Usando Plotly para Pizza (Onde dava o erro)
    fig_pizza = px.pie(gastos_pagante, values="Valor", names="Pagante", 
                       title="Quem desembolsou mais?")
    st.plotly_chart(fig_pizza, use_container_width=True)

st.subheader("Evolução por Tipo de Gasto")
gastos_tipo = df_filtrado.groupby("TIPO")["Valor"].sum().reset_index().sort_values("Valor", ascending=False)
fig_tipo = px.bar(gastos_tipo, x="TIPO", y="Valor", color="TIPO", title="Gastos por Categoria")
st.plotly_chart(fig_tipo, use_container_width=True)

# 5. TABELA DETALHADA
st.subheader("Lista de Gastos Filtrados")
# Formatar a data de volta para exibição amigável
df_display = df_filtrado.copy()
df_display['Data'] = df_display['Data'].dt.strftime('%d/%m/%Y')
st.dataframe(df_display.sort_values("Data", ascending=False), use_container_width=True)