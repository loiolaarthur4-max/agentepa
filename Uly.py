import sys
import os
import requests

# Correção para o erro de codificação UTF-8
sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"

import streamlit as st

st.set_page_config(page_title="Agente IA Gemini")
st.title("Meu Agente de IA com Gemini")

# --- BARRA LATERAL ---
st.sidebar.header("Configuracoes")

api_key_input = st.sidebar.text_input(
    "Insira sua GEMINI_API_KEY:",
    type="password",
    help="Pegue sua chave no Google AI Studio (aistudio.google.com)"
).strip()

st.sidebar.markdown("---")
st.sidebar.markdown("1. Cole sua chave da API acima.")
st.sidebar.markdown("2. Digite sua mensagem no chat abaixo.")

if not api_key_input:
    st.warning("Por favor, insira sua chave de API na barra lateral para começar.")
    st.stop()

# Histórico da conversa
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Entrada do usuário
if user_input := st.chat_input("Digite sua pergunta..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                # Monta o histórico de mensagens para a API REST
                contents = []
                for m in st.session_state.messages:
                    role = "user" if m["role"] == "user" else "model"
                    contents.append({
                        "role": role,
                        "parts": [{"text": m["content"]}]
                    })

                # URL da API REST do Gemini
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key_input}"
                
                payload = {
                    "contents": contents,
                    "systemInstruction": {
                        "parts": [{"text": "Você é um assistente virtual amigável e direto."}]
                    }
                }

                headers = {'Content-Type': 'application/json'}

                # Requisição HTTP direta
                response = requests.post(url, json=payload, headers=headers)
                data = response.json()

                if response.status_code == 200:
                    response_text = data["candidates"][0]["content"]["parts"][0]["text"]
                    st.write(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                else:
                    error_msg = data.get("error", {}).get("message", "Erro desconhecido na API")
                    st.error(f"Erro na API ({response.status_code}): {error_msg}")

            except Exception as e:
                st.error(f"Erro ao processar a requisição: {e}")
