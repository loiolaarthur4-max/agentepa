import os
import streamlit as st
from google import genai
from google.genai import types

# Configuração da página Streamlit
st.set_page_config(page_title="Agente IA Gemini", page_icon="🤖")
st.title("🤖 Meu Agente de IA com Gemini")

# Obter a API Key das variáveis de ambiente (Secrets)
api_key = os.environ.get("AQ.Ab8RN6LZE3z5PKdu5aZ9Ejw3OULjTUSJx7D8ESUPmVA40_N-9A")

if not api_key:
    st.error("Chave de API do Gemini não encontrada! Configure a variável GEMINI_API_KEY.")
    st.stop()

# Inicializa o cliente do Gemini usando a SDK google-genai
client = genai.Client(api_key=api_key)

# Instrui o comportamento/personalidade do agente
SYSTEM_INSTRUCTION = "Você é um assistente virtual amigável, criativo e focado em resolver problemas com explicações diretas e claras."

# Inicializa o histórico de mensagens na sessão do Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico de mensagens salvas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Entrada do usuário
if user_input := st.chat_input("Digite sua pergunta..."):
    # Exibe a mensagem do usuário na tela
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Prepara e envia o contexto para a API do Gemini
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                # Converte o histórico no formato esperado pela API
                formatted_contents = [
                    types.Content(
                        role="user" if m["role"] == "user" else "model",
                        parts=[types.Part.from_text(text=m["content"])]
                    )
                    for m in st.session_state.messages
                ]

                # Executa a chamada do modelo
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

                # Salva a resposta do assistente no histórico
                st.session_state.messages.append({"role": "assistant", "content": response_text})

            except Exception as e:
                st.error(f"Erro ao gerar resposta: {e}")
