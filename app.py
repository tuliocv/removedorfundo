import streamlit as st
from rembg import remove
from PIL import Image
import io

st.set_page_config(page_title="Removedor de Fundo", page_icon="🪄")
st.title("🪄 Removedor de Fundo — Simples e Rápido")

uploaded_file = st.file_uploader("Envie uma imagem (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGBA")
    st.image(image, caption="📷 Imagem Original", width="stretch")

    with st.spinner("Removendo fundo... ⏳"):
        output = remove(image)

    st.success("✅ Fundo removido com sucesso!")
    st.image(output, caption="🪄 Imagem sem fundo", width="stretch")

    buf = io.BytesIO()
    output.save(buf, format="PNG")
    st.download_button(
        "⬇️ Baixar imagem sem fundo (PNG)",
        data=buf.getvalue(),
        file_name="imagem_sem_fundo.png",
        mime="image/png"
    )
