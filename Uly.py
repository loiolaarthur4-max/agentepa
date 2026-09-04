import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Agente IA Gemini", page_icon="🤖")
st.title("🤖 Meu Agente de IA com Gemini")

# --- BARRA LATERAL PARA CONFIGURAÇÃO DA API KEY ---
st.sidebar.header("⚙️ Configurações")

api_key_input = st.sidebar.text_input(
    "Insira sua GEMINI_API_KEY:",
    type="password",
    help="Pegue sua chave no Google AI Studio (aistudio.google.com)"
).strip()  # .strip() remove espaços vazios no começo ou final da chave

st.sidebar.markdown("---")
st.sidebar.markdown("👉 **Instruções:**")
st.sidebar.markdown("1. Cole sua chave da API acima.")
st.sidebar.markdown("2. Digite sua mensagem no chat abaixo.")

# --- LÓGICA DO AGENTE ---

if not api_key_input:
    st.warning("👈 Por favor, insira sua chave de API na barra lateral para começar.")
    st.stop()

# Define a chave na variável de ambiente explicitamente para evitar erro de OAuth/Token
os.environ["GEMINI_API_KEY"] = api_key_input

try:
    # Inicializa o cliente lendo automaticamente a variável de ambiente
    client = genai.Client()
except Exception as e:
    st.error(f"Erro ao inicializar o cliente: {e}")
    st.stop()

SYSTEM_INSTRUCTION = "Você é um assistente virtual amigável, criativo e focado em resolver problemas com explicações diretas e claras."

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_input := st.chat_input("Digite sua pergunta..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                formatted_contents = [
                    types.Content(
                        role="user" if m["role"] == "user" else "model",
                        parts=[types.Part.from_text(text=m["content"])]
                    )
                    for m in st.session_state.messages
                ]

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=formatted_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.7,
                    )
                )

                response_text = response.text
                st.write(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})

            except Exception as e:
                st.error(f"Erro ao gerar resposta: {e}")
