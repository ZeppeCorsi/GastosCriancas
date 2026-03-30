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
    conn = st.connection("gsheets", type=GSheetsConnection, spreadsheet=URL_PLANILHA)
except Exception as e:
    st.error(f"Erro ao conectar com o Google: {e}")
    st.stop()

# 2. FORMULÁRIO
with st.form("form_inclusao", clear_on_submit=True):
    # Escolha de quem é o gasto
    filho = st.radio("Para quem é?", ["Pedro", "Bella", "Ambos"], horizontal=True)
    
    col1, col2 = st.columns(2)
    with col1:
        pagador = st.radio("Quem pagou?", ["Pai", "Mãe"], horizontal=True)
        data = st.date_input("Data", datetime.now())
    with col2:
        tipo = st.selectbox("Tipo de Gasto", ["Alimentação", "Lazer", "Educação", "Saúde", "Outros"])
        valor = st.number_input("Valor (R$)", min_value=0.0, step=0.01)

    descricao = st.text_input("Descrição (Ex: Farmácia, Tênis...)")
    
    btn = st.form_submit_button("💾 SALVAR NA PLANILHA")

# 3. LOGICA DE SALVAR
if btn:
    if valor > 0:
        try:
            # Lê a aba Gastos
            df_atual = conn.read(worksheet="Gastos", ttl=0)
            
            # Cria a linha nova
            nova_linha = pd.DataFrame([{
                "DATA": data.strftime('%d/%m/%Y'),
                "FILHO": filho,
                "PAGADOR": pagador,
                "TIPO": tipo,
                "VALOR": valor,
                "DESCRICAO": descricao,
                "REGISTRADO_POR": st.session_state.get('usuario_atual', 'GIUSEPPE')
            }])
            
            # Salva tudo
            df_final = pd.concat([df_atual, nova_linha], ignore_index=True)
            conn.update(worksheet="Gastos", data=df_final)
            st.success(f"✅ Sucesso! R$ {valor:.2f} lançado para {filho}.")
        except Exception as e:
            st.error(f"Erro ao salvar na planilha: {e}")
    else:
        st.warning("⚠️ Insira um valor maior que zero.")