import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

# Configuración de página
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("🤖 Chatbot - Multi Chat con LangChain + Google")
st.markdown("Este es un *chatbot de ejemplo* con gestión de múltiples chats.")

# ----- Sidebar: Controles generales -----
temperatura = st.sidebar.slider("Temperatura", 0.0, 1.0, 0.7, 0.05)
modelo = st.sidebar.selectbox("Selecciona modelo", ["gemini-2.5-flash", "gemini-3.0", "gemini-2.0"])

# Inicializar chats si no existen
if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1": []}
if "chat_actual" not in st.session_state:
    st.session_state.chat_actual = "Chat 1"

# Selector de chat
st.sidebar.markdown("### 💬 Chats")
chat_actual = st.sidebar.selectbox("Selecciona chat", list(st.session_state.chats.keys()), index=list(st.session_state.chats.keys()).index(st.session_state.chat_actual))
st.session_state.chat_actual = chat_actual

# Botón para crear nuevo chat
if st.sidebar.button("➕ Nuevo chat"):
    nuevo_nombre = f"Chat {len(st.session_state.chats)+1}"
    st.session_state.chats[nuevo_nombre] = []
    st.session_state.chat_actual = nuevo_nombre
    st.rerun()

# ----- Slider de acciones sobre el chat -----
st.sidebar.markdown("### ⚙️ Opciones del chat")
opcion_chat = st.sidebar.selectbox(
    "Acciones",
    ["Ninguna", "📝 Renombrar", "🧹 Vaciar chat", "🗑️ Eliminar chat"]
)

# --- Renombrar chat ---
if opcion_chat == "📝 Renombrar":
    nuevo_nombre = st.sidebar.text_input("Nuevo nombre:", st.session_state.chat_actual)
    if st.sidebar.button("Guardar nombre"):
        if nuevo_nombre.strip() == "":
            st.sidebar.error("El nombre no puede estar vacío.")
        elif nuevo_nombre in st.session_state.chats:
            st.sidebar.error("Ya existe un chat con ese nombre.")
        else:
            st.session_state.chats[nuevo_nombre] = st.session_state.chats.pop(st.session_state.chat_actual)
            st.session_state.chat_actual = nuevo_nombre
            st.sidebar.success("Nombre cambiado correctamente.")
            st.rerun()

# --- Vaciar chat ---
elif opcion_chat == "🧹 Vaciar chat":
    if st.sidebar.button("Vaciar"):
        st.session_state.chats[st.session_state.chat_actual] = []
        st.sidebar.success("Chat vaciado.")
        st.rerun()

# --- Eliminar chat ---
elif opcion_chat == "🗑️ Eliminar chat":
    if st.sidebar.button("Eliminar"):
        if len(st.session_state.chats) == 1:
            st.sidebar.warning("No puedes eliminar el único chat.")
        else:
            del st.session_state.chats[st.session_state.chat_actual]
            st.session_state.chat_actual = list(st.session_state.chats.keys())[0]
            st.sidebar.success("Chat eliminado.")
            st.rerun()

# ----- Crear modelo -----
chat_model = ChatGoogleGenerativeAI(model=modelo, temperature=temperatura)

# ----- Mostrar historial -----
for msg in st.session_state.chats[st.session_state.chat_actual]:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# ----- Input de usuario -----
pregunta = st.chat_input("Escribe tu mensaje:")
if pregunta:
    # Mostrar y almacenar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(pregunta)
    st.session_state.chats[st.session_state.chat_actual].append(HumanMessage(content=pregunta))

    # Generar respuesta
    respuesta = chat_model.invoke(st.session_state.chats[st.session_state.chat_actual])

    # Mostrar respuesta
    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    st.session_state.chats[st.session_state.chat_actual].append(respuesta)
