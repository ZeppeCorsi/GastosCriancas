import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Título da página
st.title("💰 Lançar Gasto das Crianças")

# URL da sua planilha
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1w8I1unID-rBc8ks1CwFd5whSonyiFZUrGflpeCeujbI/edit#gid=0"

# 1. CONEXÃO
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=st.secrets["connections"]["gsheets"]["url"])
except Exception as e:
    st.error(f"Erro ao conectar com o Google: {e}")
    st.stop()

# 2. FORMULÁRIO
with st.form("form_inclusao", clear_on_submit=True):
    filho = st.radio("Para quem é?", ["Pedro", "Bella", "Ambos"], horizontal=True)
    
    col1, col2 = st.columns(2)
    with col1:
        pagador = st.radio("Quem pagou?", ["Pai", "Mãe"], horizontal=True)
        data_input = st.date_input("Data") # Mudei o nome para evitar conflito com a biblioteca
    with col2:
        tipo = st.selectbox("Tipo de Gasto", ["Alimentação", "Lazer", "Educação", "Saúde", "Irene", "Dentista", "Roupa", "Farmacia", "Outros", ])
        valor_input = st.number_input("Valor (R$)", min_value=0.0, step=0.01)

    descricao = st.text_input("Descrição (Ex: Farmácia, Tênis...)")
    
    # O botão de salvar DEVE estar dentro do form
    btn_salvar = st.form_submit_button("💾 SALVAR NA PLANILHA")

# 3. LÓGICA DE SALVAR
if btn_salvar:
    # 1. Prepara os dados exatamente com as colunas da sua planilha (imagem f82354)
    novos_dados = {
        "TIPO": [tipo.upper()],
        "Data": [data_input.strftime('%d/%m/%Y')],
        "Pagante": [pagador.upper()],
        "Crianca": [filho.upper()],
        "Descrição": [descricao],
        "Valor": [valor_input]
    }
    novo_df = pd.DataFrame(novos_dados)

    try:
        url_planilha = st.secrets["connections"]["gsheets"]["url"]
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # 2. BUSCA OS DADOS QUE JÁ ESTÃO LÁ (IMPORTANTE)
        # O ttl=0 garante que ele não pegue uma versão antiga do cache
        df_existente = conn.read(spreadsheet=url_planilha, ttl=0)
        
        # 3. EMPILHA O NOVO GASTO NO FINAL (APPEND)
        # O ignore_index=True garante que ele crie a próxima linha (8, 9, 10...)
        df_atualizado = pd.concat([df_existente, novo_df], ignore_index=True)
        
        # 4. SOBRESCREVE A PLANILHA COM A LISTA COMPLETA E ATUALIZADA
        conn.update(
            spreadsheet=url_planilha,
            data=df_atualizado
        )
        
        st.success(f"✅ Gasto de R$ {valor_input:.2f} adicionado na próxima linha!")
        st.balloons()
        
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")