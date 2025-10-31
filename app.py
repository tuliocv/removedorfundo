import streamlit as st
from PIL import Image
import torch
from transformers import AutoProcessor, AutoModelForImageSegmentation
import numpy as np
import io

st.set_page_config(page_title="Removedor de Fundo com Transformer", page_icon="🤖", layout="centered")

st.title("🤖 Removedor de Fundo (Transformer – Hugging Face)")
st.write("Modelo: **BRIAAI/RMBG-1.4** — Segmentação precisa com Vision Transformer")

uploaded_file = st.file_uploader("Escolha uma imagem...", type=["png", "jpg", "jpeg"])

@st.cache_resource
def load_model():
    processor = AutoProcessor.from_pretrained("briaai/RMBG-1.4", trust_remote_code=True)
    model = AutoModelForImageSegmentation.from_pretrained("briaai/RMBG-1.4", trust_remote_code=True)
    return processor, model

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Imagem Original", use_container_width=True)

    with st.spinner("Removendo fundo usando transformer..."):
        processor, model = load_model()
        inputs = processor(images=image, return_tensors="pt")
        with torch.no_grad():
            preds = model(**inputs).logits
        mask = torch.sigmoid(preds)[0][0].numpy()
        mask = (mask * 255).astype(np.uint8)
        rgba = image.copy()
        rgba.putalpha(Image.fromarray(mask))

        st.success("✅ Fundo removido com sucesso!")
        st.image(rgba, caption="Imagem sem fundo (Transformer)", use_container_width=True)

        buf = io.BytesIO()
        rgba.save(buf, format="PNG")
        st.download_button(
            label="⬇️ Baixar imagem sem fundo (PNG)",
            data=buf.getvalue(),
            file_name="sem_fundo_transformer.png",
            mime="image/png"
        )
