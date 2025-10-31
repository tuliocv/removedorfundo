import warnings
warnings.filterwarnings("ignore", category=UserWarning)  # silencia avisos do PyTorch

import streamlit as st
from PIL import Image
import numpy as np
import torch
from transformers import DetrImageProcessor, DetrForSegmentation
import io

# ===============================
# ⚙️ CONFIGURAÇÕES INICIAIS
# ===============================
st.set_page_config(page_title="Removedor de Fundo (DETR público)", page_icon="🪄", layout="centered")
st.title("🪄 Removedor de Fundo com Transformer Público (DETR)")
st.write("Modelo: **facebook/detr-resnet-50-panoptic** — Segmentação panóptica local, sem API nem token.")

# ===============================
# 📦 CACHE DO MODELO
# ===============================
@st.cache_resource
def load_model():
    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50-panoptic")
    model = DetrForSegmentation.from_pretrained("facebook/detr-resnet-50-panoptic")
    return processor, model

processor, model = load_model()

# ===============================
# 📤 UPLOAD DA IMAGEM
# ===============================
uploaded_file = st.file_uploader("Envie uma imagem (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="📷 Imagem Original", width="stretch")

    with st.spinner("Processando imagem... ⏳"):
        inputs = processor(images=image, return_tensors="pt")
        outputs = model(**inputs)
        result = processor.post_process_panoptic_segmentation(outputs, target_sizes=[image.size[::-1]])[0]

        # Máscara do fundo
        panoptic_seg = result["segmentation"].numpy()
        unique_ids = np.unique(panoptic_seg)
        counts = [(uid, np.sum(panoptic_seg == uid)) for uid in unique_ids]
        background_id = max(counts, key=lambda x: x[1])[0]
        mask = np.where(panoptic_seg != background_id, 255, 0).astype(np.uint8)

        # Cria imagem com transparência
        rgba = image.copy()
        rgba.putalpha(Image.fromarray(mask))

    st.success("✅ Fundo removido com sucesso!")
    st.image(rgba, caption="🪄 Imagem sem fundo", width="stretch")

    buf = io.BytesIO()
    rgba.save(buf, format="PNG")
    st.download_button(
        "⬇️ Baixar imagem sem fundo (PNG)",
        data=buf.getvalue(),
        file_name="imagem_sem_fundo.png",
        mime="image/png"
    )
