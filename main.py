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
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Aqui dizemos explicitamente para usar a 'url' que você criou no secrets
    df = conn.read(spreadsheet=st.secrets["connections"]["gsheets"]["url"])
    
    st.success("Conectado com sucesso!")
    #st.write("Dados da planilha:")
    #st.dataframe(df.head()) # Mostra as primeiras linhas para confirmar
    
except Exception as e:
    st.error(f"Erro ao ler planilha: {e}")

# 3. LOGIN DIRETO NO CÓDIGO
def verificar_login(usuario, senha):
    # Defina aqui os usuários e senhas desejados
    acesso = {
        "GIUSEPPE": "ZEPPE",
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