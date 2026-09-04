import os
import streamlit as st
from google import genai
from google.genai import types

# Configuração da página
st.set_page_config(page_title="Agente IA Gemini", page_icon="🤖")
st.title("🤖 Meu Agente de IA com Gemini")

# --- BARRA LATERAL PARA CONFIGURAÇÃO DA API KEY ---
st.sidebar.header("⚙️ Configurações")

# Verifica se já existe uma chave nas variáveis de ambiente ou nos segredos
env_api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")

# Cria o campo de texto na barra lateral para digitar a chave
api_key_input = st.sidebar.text_input(
    "Insira sua GEMINI_API_KEY:",
    value=env_api_key,
    type="password",
    help="Pegue sua chave no Google AI Studio (aistudio.google.com)"
)

# Instruções rápidas na barra lateral
st.sidebar.markdown("---")
st.sidebar.markdown("👉 **Instruções:**")
st.sidebar.markdown("1. Cole sua chave da API acima.")
st.sidebar.markdown("2. Digite sua mensagem no chat abaixo.")

# --- LÓGICA DO AGENTE ---

# Se a chave não for informada, exibe um aviso e para o aplicativo
if not api_key_input:
    st.warning("👈 Por favor, insira sua chave de API na barra lateral para começar a usar o agente.")
    st.stop()

# Inicializa o cliente do Gemini usando a chave informada na interface
try:
    client = genai.Client(api_key=api_key_input)
except Exception as e:
    st.error(f"Erro ao inicializar o cliente da API: {e}")
    st.stop()

# Personalidade / Instruções do agente
SYSTEM_INSTRUCTION = "Você é um assistente virtual amigável, criativo e focado em resolver problemas com explicações diretas e claras."

# Inicializa o histórico de mensagens na sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens anteriores do chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Campo de entrada de texto do chat
if user_input := st.chat_input("Digite sua pergunta..."):
    # Salva e exibe a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Envia as mensagens acumuladas para o modelo
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                # Converte o histórico para o formato da biblioteca google-genai
                formatted_contents = [
                    types.Content(
                        role="user" if m["role"] == "user" else "model",
                        parts=[types.Part.from_text(text=m["content"])]
                    )
                    for m in st.session_state.messages
                ]

                # Chamada do modelo Gemini
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
                st.error(f"Erro ao gerar resposta. Verifique sua chave de API e tente novamente. Detalhes: {e}")
