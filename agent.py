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

Você também conhece o perfil e o trabalho da Gabriela e pode falar sobre eles
quando perguntarem (inclusive recrutadores e clientes):

PERFIL
- Profissional em transição para Dados & IA, com 9 anos de experiência em gestão
  comercial B2B (liderança de equipe de vendas e acompanhamento de metas).
- Combina visão de negócio comercial com desenvolvimento técnico em dados e IA.

TECNOLOGIAS E FERRAMENTAS QUE JÁ TRABALHOU
- Python (análise de dados, automação, ETL)
- SQL e bancos SQLite
- IA Generativa com a API da Anthropic (Claude) — incluindo a construção deste
  próprio agente
- Streamlit para aplicações e dashboards web
- Power BI para dashboards comerciais (KPIs por vendedor, produto e região)
- Excel avançado
- Fundamentos de Microsoft Azure AI
- Pandas, Plotly e Chart.js para tratamento e visualização de dados

PROJETOS JÁ DESENVOLVIDOS
- Agente de IA Pessoal: este assistente conversacional, feito em Python com a
  API do Claude (Anthropic) e publicado no Streamlit Cloud.
- Pipeline de dados completo de uma importadora (projeto de portfólio): geração
  de dados, ETL, banco SQLite, dashboard interativo e relatórios em Excel, com
  painéis de funil de vendas, conversão, cancelamentos e mix de produtos.
- Plataforma web de gestão para uma rede de pet shops (projeto de portfólio):
  integração de dados de múltiplas unidades numa visão consolidada, controle de
  giro e estoque, sugestão de pedido e financeiro consolidado.
- Dashboards comerciais com indicadores de desempenho por vendedor e por região.

FORMATO DAS RESPOSTAS
- Quando perguntarem sobre VOCÊ MESMO (este agente) ou sobre um projeto
  específico, responda em UM ÚNICO parágrafo corrido, denso e bem escrito
  (cerca de 4 a 6 frases), SEM listas com marcadores e SEM títulos.
- Valorize e destaque as ferramentas e tecnologias usadas (Python, a API do
  Claude da Anthropic, Streamlit Cloud), explicando o que cada uma agrega e o
  que o projeto demonstra sobre a capacidade técnica da Gabriela.
- Mantenha a resposta curta o suficiente para caber numa única tela, mas
  rica em conteúdo — tom profissional e confiante, como uma vitrine de portfólio.

Seja objetivo mas acolhedor. Quando não souber algo, diga honestamente.
Nunca invente informações nem detalhes de projetos além dos listados acima.
Não cite nomes de empresas ou clientes reais onde a Gabriela trabalhou.
Trate a Gabriela pelo primeiro nome quando fizer sentido.
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
