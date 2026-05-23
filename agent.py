"""
agent.py — O "cérebro" do nosso agente IA
==========================================
Usando Anthropic Claude API
"""

# ── FIX SSL (necessário no Windows com alguns antivírus/proxies) ──────────────
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# ── IMPORTS ───────────────────────────────────────────────────────────────────
import os
from dotenv import load_dotenv
import anthropic

# ── CARREGA O .env (só funciona localmente) ───────────────────────────────────
_pasta = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_pasta, ".env"))

# ── CONFIGURAÇÃO ──────────────────────────────────────────────────────────────
# Cliente criado na primeira chamada (lazy) para garantir que os secrets
# do Streamlit Cloud já estejam carregados quando for lido
_client = None

def _get_client():
    global _client
    if _client is None:
        try:
            import streamlit as st
            key = st.secrets["ANTHROPIC_API_KEY"]
        except Exception:
            key = os.getenv("ANTHROPIC_API_KEY")
        _client = anthropic.Anthropic(api_key=key)
    return _client

# Modelo a usar
MODELO = "claude-haiku-4-5"

# ── PERSONA DO AGENTE ─────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
Você é o assistente pessoal de Inteligência Artificial da Gabriela Michelotto.
Responda sempre em português do Brasil, de forma clara, direta e amigável.

Você pode ajudar com:
- Vendas: estratégias, abordagem de clientes, metas e técnicas de negociação
- Produtividade: organização, foco, planejamento de tarefas e rotinas
- Carreira: dicas profissionais, currículo, portfólio e desenvolvimento pessoal
- Qualquer outra dúvida do dia a dia

Seja objetivo mas acolhedor. Quando não souber algo, diga honestamente.
Nunca invente informações. Trate a Gabriela pelo primeiro nome quando fizer sentido.
"""

# ── FUNÇÃO PRINCIPAL ──────────────────────────────────────────────────────────

def perguntar_ao_agente(mensagem: str, historico: list) -> str:
    """
    Envia uma mensagem para o Claude e retorna a resposta.

    Parâmetros:
        mensagem  — o texto que o usuário digitou agora
        historico — lista com todas as mensagens anteriores da conversa
    """

    # Passo 1: Converte o histórico para o formato da API Anthropic
    messages = []
    for msg in historico:
        role = "user" if msg["role"] == "user" else "assistant"
        messages.append({"role": role, "content": msg["content"]})

    # Passo 2: Adiciona a mensagem atual
    messages.append({"role": "user", "content": mensagem})

    # Passo 3: Chama a API e pega a resposta
    response = _get_client().messages.create(
        model=MODELO,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages
    )

    texto_resposta = response.content[0].text

    # Passo 4: Salva no histórico (formato padrão)
    historico.append({"role": "user",      "content": mensagem})
    historico.append({"role": "assistant", "content": texto_resposta})

    return texto_resposta
