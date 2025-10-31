import streamlit as st
from PIL import Image
from transformers import pipeline
import numpy as np
import io

st.set_page_config(page_title="Removedor de Fundo (Hugging Face)", page_icon="🧠", layout="centered")

st.title("🧠 Removedor de Fundo (Hugging Face Pipeline)")
st.write("Modelo: **BRIAAI/RMBG-1.4** — Background Removal baseado em Vision Transformer")

uploaded_file = st.file_uploader("Envie uma imagem (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])

@st.cache_resource
def load_model():
    return pipeline("image-segmentation", model="briaai/RMBG-1.4", trust_remote_code=True)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="📷 Imagem original", use_container_width=True)

    with st.spinner("Removendo fundo com Transformer..."):
        bg_remover = load_model()
        result = bg_remover(image)

        # O pipeline retorna um dicionário com a máscara (0–1)
        mask = np.array(result[0]['mask']) * 255
        mask = mask.astype(np.uint8)

        rgba = image.copy()
        rgba.putalpha(Image.fromarray(mask))

    st.success("✅ Fundo removido com sucesso!")
    st.image(rgba, caption="🪄 Imagem sem fundo", use_container_width=True)

    buf = io.BytesIO()
    rgba.save(buf, format="PNG")
    st.download_button(
        "⬇️ Baixar imagem sem fundo (PNG)",
        data=buf.getvalue(),
        file_name="imagem_sem_fundo.png",
        mime="image/png"
    )
