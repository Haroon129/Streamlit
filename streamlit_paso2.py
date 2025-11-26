import streamlit as st
import random
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

# Configuración de página
import streamlit as st

st.set_page_config(
    page_title="AutistBot",
    page_icon="🤖",
    layout="centered"  # opcional: "wide"
)

mensajes = [
    "¡Hola! 👋",
    "Mondongo",
    "Unos Loletes?",
    "Que la fuerza te acompañe ✨",
    "Cuando empecemos la invasión global te tendré en cuenta 😉",
    "Mañana no vengas a clase 😈"
]
st.title("🤖 AutistBot - Tu amigo de confianza")
st.markdown(random.choice(mensajes))



# Inicializar chats
if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1": []}
if "chat_actual" not in st.session_state:
    st.session_state.chat_actual = "Chat 1"

# Selector de chat
st.sidebar.markdown("### 💬 Chats")
chat_actual = st.sidebar.selectbox(
    "Selecciona chat",
    list(st.session_state.chats.keys()),
    index=list(st.session_state.chats.keys()).index(st.session_state.chat_actual)
)
st.session_state.chat_actual = chat_actual

# Nuevo chat
if st.sidebar.button("➕ Nuevo chat"):
    nuevo_nombre = f"Chat {len(st.session_state.chats) + 1}"
    st.session_state.chats[nuevo_nombre] = []
    st.session_state.chat_actual = nuevo_nombre
    st.rerun()

# Acciones sobre el chat
with st.sidebar.expander("⚙️ Opciones del chat"):
    opcion_chat = st.selectbox(
        "Acciones",
        ["Ninguna", "📝 Renombrar", "🧹 Vaciar chat", "🗑️ Eliminar chat"]
    )

    # Renombrar
    if opcion_chat == "📝 Renombrar":
        nuevo_nombre = st.text_input("Nuevo nombre:", st.session_state.chat_actual)
        if st.button("Guardar nombre"):
            if nuevo_nombre.strip() and nuevo_nombre not in st.session_state.chats:
                st.session_state.chats[nuevo_nombre] = st.session_state.chats.pop(st.session_state.chat_actual)
                st.session_state.chat_actual = nuevo_nombre
                st.rerun()

    # Vaciar
    if opcion_chat == "🧹 Vaciar chat":
        if st.button("Vaciar"):
            st.session_state.chats[st.session_state.chat_actual] = []
            st.rerun()

    # Eliminar
    if opcion_chat == "🗑️ Eliminar chat":
        if st.button("Eliminar"):
            if len(st.session_state.chats) > 1:
                del st.session_state.chats[st.session_state.chat_actual]
                st.session_state.chat_actual = list(st.session_state.chats.keys())[0]
                st.rerun()

# ----- Sidebar: Controles generales -----

# Sección principal de controles
st.sidebar.markdown("## ⚙️ Configuración")

modelo = st.sidebar.selectbox(
    "Selecciona modelo",
    [
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
        "gemini-2.5-flash", 
        "gemini-2.5-flash-lite",
        "gemini-2.5-pro"
        
        ]
)

# --- EXPANDER (el “slider dentro de slider” que querías) ---
with st.sidebar.expander("🔧 Ajustes avanzados"):
    temperatura = st.slider("Temperatura", 0.0, 1.0, 0.7, 0.05)
    top_p = st.slider("Creatividad", 0.0, 1.0, 0.9, 0.05)
    max_tokens = st.slider("Carácteres máximos", 50, 500, 200)

# Si no abres el expander, usa valores por defecto
if "temperatura" not in locals():
    temperatura = 0.7
if "top_p" not in locals():
    top_p = 0.9
if "max_tokens" not in locals():
    max_tokens = 200


# Crear modelo
chat_model = ChatGoogleGenerativeAI(
    model=modelo,
    temperature=temperatura,
    top_p=top_p,
    max_output_tokens=max_tokens
)

# Mostrar historial
for msg in st.session_state.chats[st.session_state.chat_actual]:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

# Input de usuario
pregunta = st.chat_input("Escribe tu mensaje:")
if pregunta:
    with st.chat_message("user"):
        st.markdown(pregunta)
    st.session_state.chats[st.session_state.chat_actual].append(HumanMessage(content=pregunta))

    respuesta = chat_model.invoke(st.session_state.chats[st.session_state.chat_actual])
    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    st.session_state.chats[st.session_state.chat_actual].append(respuesta)
