import streamlit as st
import requests

st.set_page_config(
    page_title="GenAI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
<style>

/* Main background */
.stApp{
    background:#0F172A;
}

/* Chat messages */
[data-testid="stChatMessage"]{
    border-radius:18px;
    padding:12px;
    margin-bottom:12px;
    border:1px solid #263244;
    background:#1E293B;
}

/* User message */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]){
    background:#1F2937;
}

/* Assistant message */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]){
    background:#162033;
}

/* Chat input */
[data-testid="stChatInput"]{
    border-radius:18px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* Main App */
.stApp{
    background-color:#0f172a;
    color:white;
}

/* Main content container */
.block-container{
    padding-top:2rem;
    max-width:900px;
}

/* Sidebar */
[data-testid="stSidebar"]{
    background-color:#111827;
}

/* Chat input */
[data-testid="stChatInput"]{
    background-color:#1f2937;
    border-radius:12px;
}

/* Buttons */
.stButton>button{
    width:100%;
    border-radius:12px;
    background:#1e293b;
    color:white;
    border:1px solid #374151;
}

.stButton>button:hover{
    background:#2563eb;
    color:white;
}

/* Hide Streamlit footer */
footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)
# ---------------- Sidebar ----------------
with st.sidebar:

    st.markdown("# 🤖 GenAI")

    st.markdown("---")

    st.success("🟢 AI Online")

    st.markdown("### 🤖 Model")
    st.info("Llama 3.2")

    st.markdown("### 👩‍💻 Developer")
    st.write("**Vaishnavi Barve**")

    st.markdown("### ⚙ Technology")
    st.write("• FastAPI")
    st.write("• Streamlit")
    st.write("• Ollama")

    st.markdown("---")

    # ---------------- PDF Upload ----------------

    st.markdown("### 📄 Upload PDF")

    uploaded_pdf = st.file_uploader(
        "Choose a PDF",
        type=["pdf"]
    )

    if uploaded_pdf is not None:

        files = {
            "file": (
                uploaded_pdf.name,
                uploaded_pdf.getvalue(),
                "application/pdf"
            )
        }

        try:
            response = requests.post(
                "http://127.0.0.1:8000/upload-pdf",
                files=files
            )

            if response.status_code == 200:
                st.success("✅ PDF uploaded successfully!")
            else:
                st.error("❌ Upload failed.")

        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown("---")

    # ---------------- Image Upload ----------------

    st.markdown("### 🖼 Upload Image")

    uploaded_image = st.file_uploader(
        "Choose an image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_image is not None:
        st.image(
            uploaded_image,
            caption="Uploaded Image",
            use_container_width=True
        )

    st.markdown("---")

    # ---------------- Clear Chat ----------------

    if st.button("🗑 Clear Chat", use_container_width=True):
        requests.post("http://127.0.0.1:8000/clear")
        st.session_state.messages = []
        st.rerun()

# ---------------- Main ----------------

st.title("🤖 GenAI Chatbot")
st.caption("Ask me anything!")

# Chat History

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- Welcome Screen ----------------
if len(st.session_state.messages) == 0:

    st.markdown("""
<div style="text-align:center; margin-top:-20px; margin-bottom:25px;">
    <h1 style="font-size:58px; margin-bottom:5px;">🤖 GenAI Chatbot</h1>
    <h3 style="color:#A1A1AA; margin-bottom:10px;">
        Your Personal AI Assistant
    </h3>
    <p style="color:#6B7280;">
        Powered by Llama 3.2 • FastAPI • Streamlit • Ollama
    </p>
</div>
""", unsafe_allow_html=True)

  
st.markdown("### 💡 Try asking")

col1, col2 = st.columns(2)

with col1:
    if st.button("💻 Explain Python", use_container_width=True):
        st.session_state["quick_prompt"] = "Explain Python in simple words."

    if st.button("📚 Machine Learning", use_container_width=True):
        st.session_state["quick_prompt"] = "What is Machine Learning?"

with col2:
    if st.button("🧠 Generative AI", use_container_width=True):
        st.session_state["quick_prompt"] = "Explain Generative AI."

    if st.button("📝 Write Resume", use_container_width=True):
        st.session_state["quick_prompt"] = "Write a professional resume."

# ---------------- Display Chat ----------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- Chat Input ----------------

user_input = st.chat_input("Type your message...")

if "quick_prompt" in st.session_state:
    user_input = st.session_state.pop("quick_prompt")

if user_input:

    # Show user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant Response

    with st.chat_message("assistant"):

        with st.spinner("🤖 Thinking..."):

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/chat",
                    json={"message": user_input},
                    timeout=180
                
                )

                response.raise_for_status()

                bot_reply = response.json()["reply"]

            except requests.exceptions.ConnectionError:

                bot_reply = "⚠ Cannot connect to the FastAPI backend.\n\nStart the backend server."

            except requests.exceptions.Timeout:

                bot_reply = "⏳ AI is taking too long to respond."

            except requests.exceptions.HTTPError:

                bot_reply = "❌ Server returned an error."

            except Exception as e:

                bot_reply = f"❌ Unexpected Error:\n\n{e}"

            st.markdown(bot_reply)

    # Save assistant message

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": bot_reply
        }
    )

    st.session_state.last_response = bot_reply

    st.divider()

if "last_response" in st.session_state:

    st.markdown("### 📋 Copy Last Response")

    st.code(
        st.session_state.last_response,
        language=None
    )

    st.caption("Select the text above and press Ctrl + C to copy it.")

# ---------------- Footer ----------------

st.caption(
    "🚀 GenAI Chatbot | Developed by Vaishnavi Barve | FastAPI • Streamlit • Ollama • Llama 3.2"
)