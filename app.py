"""
app.py — Agente da Gabriela Michelotto
Visual: diário — fundo branco, cursiva elegante, ícone rosa
"""

import os as _os
import datetime
import streamlit as st
from dotenv import load_dotenv
from agent import perguntar_ao_agente

load_dotenv(_os.path.join(_os.path.dirname(__file__), ".env"))

st.set_page_config(page_title="Gabriela Michelotto", page_icon="🌸", layout="centered")

# ── SAUDAÇÃO ──────────────────────────────────────────────────────────────────
def saudacao():
    h = datetime.datetime.now().hour
    if 5 <= h < 12:  return "Bom dia"
    elif 12 <= h < 18: return "Boa tarde"
    else: return "Boa noite"

# ── DATA EM PORTUGUÊS ─────────────────────────────────────────────────────────
def data_pt():
    hoje = datetime.datetime.now()
    dias   = ["segunda-feira","terça-feira","quarta-feira","quinta-feira","sexta-feira","sábado","domingo"]
    meses  = ["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"]
    return f"{dias[hoje.weekday()]}, {hoje.day} de {meses[hoje.month-1]} de {hoje.year}"

# ── ESTILO ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pinyon+Script&family=Inter:wght@300;400&display=swap');

/* Força fundo branco em tudo */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"], .main, section.main,
[data-testid="stHeader"] {
    background-color: #f5f0eb !important;
}

.block-container {
    max-width: 660px;
    padding-top: 3rem;
    background-color: #f5f0eb !important;
    text-align: center;
}

/* Data */
.date-line {
    font-family: 'Pinyon Script', cursive;
    font-size: 1.3rem;
    color: #999;
    text-align: center;
    margin-bottom: 0.1rem;
}

/* Saudação cursiva */
.greeting {
    font-family: 'Pinyon Script', cursive;
    font-size: 4.5rem;
    color: #1a1a1a;
    margin: 0;
    line-height: 1.1;
    text-align: center;
}

/* Divisória */
.divider {
    border: none;
    border-top: 1px solid #f0f0f0;
    margin: 1rem 0 1.8rem 0;
}

/* Chat — volta para esquerda */
[data-testid="stChatMessage"] {
    font-family: 'Inter', sans-serif;
    font-weight: 300;
    font-size: 0.9rem;
    background: transparent !important;
    text-align: left;
}

/* Esconde avatares padrão */
[data-testid="chatAvatarIcon-user"],
[data-testid="chatAvatarIcon-assistant"] { display: none; }

/* Balão usuário */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: #ede8e2 !important;
    border-radius: 10px;
    padding: 0.5rem 1rem;
}

/* Input */
[data-testid="stChatInput"] textarea {
    font-family: 'Inter', sans-serif;
    font-weight: 400;
    font-size: 0.92rem;
    color: #1a1a1a !important;
    border-radius: 10px;
    background: #fdf8f5 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #c4959e !important;
    opacity: 1 !important;
}

[data-testid="stChatInput"] > div {
    border: 1.5px solid #e8a0b4 !important;
    border-radius: 14px !important;
    background: #fdf8f5 !important;
}

[data-testid="stChatInput"] > div:focus-within {
    border-color: #d4607e !important;
    box-shadow: 0 0 0 2px rgba(212, 96, 126, 0.12) !important;
}

/* Botão */
div.stButton > button {
    font-family: 'Inter', sans-serif;
    font-weight: 300;
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    border: 1px solid #f0d0d8;
    color: #c9819a;
    background: #f5f0eb;
    border-radius: 20px;
    padding: 0.25rem 1.2rem;
}
div.stButton > button:hover {
    background: #ede8e2;
    border-color: #e8a0b4;
}

/* Rodapé */
.footer {
    text-align: center;
    font-family: 'Inter', sans-serif;
    font-size: 0.65rem;
    font-weight: 300;
    color: #ddd;
    letter-spacing: 0.12em;
    margin-top: 3rem;
}
</style>
""", unsafe_allow_html=True)

# ── CABEÇALHO ─────────────────────────────────────────────────────────────────
st.markdown(f'<p class="date-line">{data_pt()}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="greeting">{saudacao()}, Gabriela.</p>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── SESSÃO ────────────────────────────────────────────────────────────────────
if "historico" not in st.session_state:
    st.session_state.historico = []

if not st.session_state.historico:
    st.markdown("""
    <p style="
        font-family: 'Pinyon Script', cursive;
        font-size: 2rem;
        color: #a07080;
        text-align: center;
        margin: 2rem 0 0.5rem 0;
        line-height: 1.4;
    ">Como posso te ajudar hoje?</p>
    """, unsafe_allow_html=True)

for msg in st.session_state.historico:
    avatar = "🌸" if msg["role"] == "assistant" else "🤍"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# ── INPUT ─────────────────────────────────────────────────────────────────────
if pergunta := st.chat_input("escreva aqui..."):
    with st.chat_message("user", avatar="🤍"):
        st.write(pergunta)
    with st.chat_message("assistant", avatar="🌸"):
        with st.spinner(""):
            resposta = perguntar_ao_agente(pergunta, st.session_state.historico)
        st.write(resposta)

# ── RODAPÉ ────────────────────────────────────────────────────────────────────
if st.session_state.historico:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        if st.button("limpar"):
            st.session_state.historico = []
            st.rerun()

st.markdown('<p class="footer">Python · Streamlit · Google Gemini</p>', unsafe_allow_html=True)
