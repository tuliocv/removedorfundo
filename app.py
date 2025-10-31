import streamlit as st
from PIL import Image
import requests
import io

# ===============================
# ⚙️ CONFIGURAÇÕES DO APLICATIVO
# ===============================
st.set_page_config(page_title="Removedor de Fundo (Hugging Face API)", page_icon="🪄", layout="centered")

st.title("🪄 Removedor de Fundo (Hugging Face API)")
st.write("Modelo usado: **BRIAAI/RMBG-1.4** — Segmentação precisa baseada em Vision Transformer.")

# ===============================
# 🔐 AUTENTICAÇÃO
# ===============================
with st.expander("🔑 Configuração do Token (necessário apenas 1 vez)"):
    st.markdown(
        """
        Você precisa de um token gratuito do Hugging Face para usar a API.  
        1. Crie uma conta em [huggingface.co](https://huggingface.co/join)  
        2. Vá em [Tokens de Acesso](https://huggingface.co/settings/tokens)  
        3. Copie seu token (ex: `hf_xxxxxxxxxxxxxxxxxxx`)  
        4. Cole abaixo:
        """
    )
    token_input = st.text_input("Cole seu token do Hugging Face aqui:", type="password")
    if token_input:
        st.session_state["hf_token"] = token_input
        st.success("✅ Token salvo na sessão com sucesso!")

# ===============================
# 📤 UPLOAD DA IMAGEM
# ===============================
uploaded_file = st.file_uploader("Envie uma imagem (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])

# ===============================
# 🚀 PROCESSAMENTO VIA API
# ===============================
if uploaded_file is not None:
    if "hf_token" not in st.session_state:
        st.warning("⚠️ Insira seu token do Hugging Face antes de continuar.")
    else:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="📷 Imagem Original", use_container_width=True)

        API_URL = "https://api-inference.huggingface.co/models/briaai/RMBG-1.4"
        headers = {"Authorization": f"Bearer {st.session_state['hf_token']}"}

        with st.spinner("Removendo fundo via Hugging Face API..."):
            response = requests.post(API_URL, headers=headers, data=uploaded_file.getvalue())

            if response.status_code == 200:
                result = Image.open(io.BytesIO(response.content)).convert("RGBA")
                st.success("✅ Fundo removido com sucesso!")
                st.image(result, caption="🪄 Imagem sem fundo", use_container_width=True)

                buf = io.BytesIO()
                result.save(buf, format="PNG")
                st.download_button(
                    "⬇️ Baixar imagem sem fundo (PNG)",
                    data=buf.getvalue(),
                    file_name="imagem_sem_fundo.png",
                    mime="image/png",
                )
            else:
                st.error(f"❌ Erro na API ({response.status_code}): {response.text}")
