"""
agent.py — O "cérebro" do nosso agente IA
==========================================
Usando Google Gemini (gratuito, sem cartão de crédito!)
"""

# ── FIX SSL (necessário no Windows com alguns antivírus/proxies) ──────────────
# O Windows às vezes tem conflito de certificados SSL com Python.
# Esta linha diz ao Python para usar as configurações de segurança do próprio Windows.
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# ── IMPORTS ───────────────────────────────────────────────────────────────────
import os
from dotenv import load_dotenv
from google import genai               # biblioteca oficial do Google Gemini
from google.genai import types         # tipos de dados da API

# ── CARREGA O .env ────────────────────────────────────────────────────────────
# Carrega aqui mesmo, garantindo que a chave esteja disponível antes de tudo
_pasta = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_pasta, ".env"))

# ── CONFIGURAÇÃO ──────────────────────────────────────────────────────────────
# Cria o cliente com a chave lida do arquivo .env
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Modelo a usar — testamos e este funciona no plano gratuito
MODELO = "gemini-flash-lite-latest"

# ── PERSONA DO AGENTE ─────────────────────────────────────────────────────────
# Mude este texto para dar qualquer personalidade ao seu agente!
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
    Envia uma mensagem para o Gemini e retorna a resposta.

    Parâmetros:
        mensagem  — o texto que o usuário digitou agora
        historico — lista com todas as mensagens anteriores da conversa
    """

    # Passo 1: Converte o histórico para o formato que a API do Gemini aceita
    # Nosso formato:  {"role": "user"/"assistant", "content": "texto"}
    # Formato Gemini: types.Content(role="user"/"model", parts=[types.Part(text="texto")])
    gemini_history = []

    for msg in historico:
        role = "model" if msg["role"] == "assistant" else "user"
        gemini_history.append(
            types.Content(
                role=role,
                parts=[types.Part(text=msg["content"])]
            )
        )

    # Passo 2: Cria o chat com histórico e persona
    chat = client.chats.create(
        model=MODELO,
        history=gemini_history,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )

    # Passo 3: Envia a mensagem e pega a resposta
    resposta = chat.send_message(mensagem)
    texto_resposta = resposta.text

    # Passo 4: Salva no histórico (formato padrão)
    historico.append({"role": "user",      "content": mensagem})
    historico.append({"role": "assistant", "content": texto_resposta})

    return texto_resposta
