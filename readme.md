 🪄 Removedor de Fundo

Aplicação web desenvolvida em **Streamlit** para remoção automática de fundo em imagens, utilizando o modelo **U²-Net** através da biblioteca [`rembg`](https://github.com/danielgatis/rembg).  
O app permite o upload de imagens nos formatos **PNG**, **JPG** ou **JPEG**, remove o fundo de forma local e disponibiliza o resultado com **transparência** para download.

---

## ⚙️ Instalação e Execução

### 1. Clone o repositório
```
git clone https://github.com/tuliocv/removedorfundo.git
cd removedor-de-fundo
```

### 2. Instale as dependências
```
pip install -r requirements.txt
```
### 3. Execute o app
```
streamlit run app.py
```
ou ainda em:
👉 https://removedorfundoimagem.streamlit.app/

### 4. Depenências
```
streamlit
pillow
rembg
onnxruntime
```

### 5. Funcionalidades
✅ Upload de imagens (PNG, JPG, JPEG)
✅ Remoção automática de fundo com IA (U²-Net)
✅ Visualização da imagem original e do resultado
✅ Download do arquivo final em formato PNG com transparência

### 6. Desenvolvido por
Desenvolvido por Túlio
Aplicação simples, leve e eficiente para manipulação de imagens com inteligência artificial.
