import sys
import os

# Correção para o erro de codificação ASCII / UTF-8 no terminal
sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"

import streamlit as st
import google.generativeai as genai

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

# Configuração da API Key
try:
    genai.configure(api_key=api_key_input)
    
    # Define as instruções do sistema e o modelo
    system_instruction = "Você é um assistente virtual amigável, criativo e focado em resolver problemas com explicações diretas e claras."
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction
    )
except Exception as e:
    st.error(f"Erro ao inicializar o modelo: {e}")
    st.stop()

# Histórico da conversa
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens antigas na tela
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Entrada do usuário
if user_input := st.chat_input("Digite sua pergunta..."):
    # Exibe a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Gera a resposta do modelo
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                # Prepara o histórico no formato aceito pela biblioteca
                history = [
                    {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                    for m in st.session_state.messages[:-1]
                ]
                
                # Inicia a conversa com o histórico e envia a nova mensagem
                chat = model.start_chat(history=history)
                response = chat.send_message(user_input)

                response_text = response.text
                st.write(response_text)
                
                # Salva a resposta no histórico
                st.session_state.messages.append({"role": "assistant", "content": response_text})

            except Exception as e:
                st.error(f"Erro ao gerar resposta: {e}")
