import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

# =========================
# CONFIGURACIÓN DE PÁGINA
# =========================
st.set_page_config(
    page_title="VisionScan OCR",
    page_icon="📸",
    layout="wide"
)

# =========================
# ESTILOS VISUALES
# =========================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #ede9fe, #d8b4fe, #c4b5fd);
    background-attachment: fixed;
}

h1, h2, h3 {
    color: #2d1b4e;
}

[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(12px);
}

.stButton>button {
    background-color: #7b2cbf;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 0.6rem 1rem;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #9d4edd;
    color: white;
}

textarea, input {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("📸 VisionScan OCR")
st.markdown("### Escanea imágenes y extrae texto automáticamente usando OCR")

st.markdown("---")

# =========================
# SIDEBAR
# =========================
with st.sidebar:

    st.title("⚙️ Opciones de Escaneo")

    filtro = st.radio(
        "🪄 Aplicar filtro visual",
        ('Con Filtro', 'Sin Filtro')
    )

    st.markdown("---")

    st.info("""
📌 Esta herramienta utiliza OCR para detectar texto desde imágenes capturadas en tiempo real.
""")

# =========================
# CÁMARA
# =========================
st.subheader("📷 Captura una imagen")

img_file_buffer = st.camera_input("Tomar fotografía")

# =========================
# PROCESAMIENTO
# =========================
if img_file_buffer is not None:

    st.success("✅ Imagen capturada correctamente")

    # Convertir buffer en imagen OpenCV
    bytes_data = img_file_buffer.getvalue()

    cv2_img = cv2.imdecode(
        np.frombuffer(bytes_data, np.uint8),
        cv2.IMREAD_COLOR
    )

    # Aplicar filtro
    if filtro == 'Con Filtro':

        cv2_img = cv2.bitwise_not(cv2_img)

        st.warning("🎨 Filtro invertido aplicado")

    # Convertir a RGB
    img_rgb = cv2.cvtColor(
        cv2_img,
        cv2.COLOR_BGR2RGB
    )

    # Mostrar imagen procesada
    st.markdown("### 🖼️ Vista previa")

    st.image(
        img_rgb,
        use_container_width=True
    )

    # OCR
    text = pytesseract.image_to_string(img_rgb)

    st.markdown("---")

    st.markdown("## ✨ Texto Detectado")

    if text.strip() != "":

        st.info(text)

    else:

        st.error("❌ No se detectó texto en la imagen")

# =========================
# FOOTER
# =========================
st.markdown("---")

st.markdown(
    "<center>🧠 Desarrollado con OpenCV + OCR + Streamlit</center>",
    unsafe_allow_html=True
)
