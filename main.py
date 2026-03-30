import streamlit as st
from streamlit_gsheets import GSheetsConnection 
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Gestão de Gastos", 
    page_icon="👦👧", 
    layout="wide"
)

# 2. INICIALIZAÇÃO DA CONEXÃO
# Mantemos para que a página de 'Inclusão' consiga gravar os dados depois
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Erro na conexão com o Sheets. Verifique o secrets.")

# Para ler os dados (o parâmetro spreadsheet vai aqui, se não estiver no secrets)
df = conn.read()

# 3. LOGIN DIRETO NO CÓDIGO
def verificar_login(usuario, senha):
    # Defina aqui os usuários e senhas desejados
    acesso = {
        "GIUSEPPE": "1234",
        "GIOVANNA": "4321"
    }
    
    user_upper = str(usuario).strip().upper()
    if user_upper in acesso and acesso[user_upper] == str(senha).strip():
        return True
    return False

# --- LÓGICA DE INTERFACE ---
if 'logado' not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.markdown("### 🔐 Acesso ao Sistema")
    
    with st.form("login_form"):
        user_input = st.text_input("Usuário")
        pass_input = st.text_input("Senha", type="password")
        btn_login = st.form_submit_button("Entrar")
        
        if btn_login:
            if verificar_login(user_input, pass_input):
                st.session_state.logado = True
                st.session_state.usuario_atual = user_input.upper()
                st.rerun()
            else:
                st.error("⚠️ Usuário ou senha incorretos.")

else:
    # --- MENU APÓS LOGIN ---
    st.sidebar.success(f"Logado como: {st.session_state.usuario_atual}")
    
    # Define as páginas que estão na sua pasta /pages
    pg = st.navigation([
        st.Page("pages/Gestao.py", title="Dashboard", icon="📊"),
        st.Page("pages/Inclusao.py", title="Lançar Gasto", icon="💰")
    ])
    
    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()

    pg.run()