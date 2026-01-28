import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="SiPilah Timpag",
    page_icon="♻️",
    layout="centered"
)

# ==========================================
# 2. CUSTOM CSS (LIGHT + BIRU)
# ==========================================
st.markdown("""
<style>
body {
    background-color: #F8FBFF;
}

.main_title {
    font-size: 2.6rem;
    color: #1E88E5;
    text-align: center;
    font-weight: 800;
}

.sub_title {
    text-align: center;
    color: #444;
    font-size: 1.2rem;
}

.tagline {
    text-align: center;
    font-size: 1rem;
    color: #666;
    margin-bottom: 25px;
}

.result_box {
    padding: 22px;
    border-radius: 18px;
    text-align: center;
    margin-top: 20px;
    font-size: 1.05rem;
    box-shadow: 0 6px 15px rgba(0,0,0,0.08);
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. LOGO SECTION
# ==========================================
col1, col2, col3 = st.columns(3)
with col1:
    st.image("assets/logo_tapaktimpag.png", use_container_width=True)
with col2:
    st.image("assets/logo_uns.png", use_container_width=True)
with col3:
    st.image("assets/logo_desa_timpag.png", use_container_width=True)

# ==========================================
# 4. JUDUL
# ==========================================
st.markdown('<div class="main_title">♻️ SiPilah Timpag</div>', unsafe_allow_html=True)
st.markdown('<div class="sub_title">Aplikasi Pintar Pilah Sampah</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Rahajeng semeng adik-adik! Yuk kenali jenis sampahmu 🌏</div>', unsafe_allow_html=True)

# ==========================================
# 5. PANDUAN PENGGUNAAN
# ==========================================
st.markdown("## 🧭 Cara Menggunakan")

colA, colB = st.columns(2)

with colA:
    st.markdown("""
    <div class="result_box" style="background:#E3F2FD; border:2px solid #90CAF9;">
        <h3>👣 Langkah Mudah</h3>
        <ol style="text-align:left;">
            <li>📸 Foto sampah</li>
            <li>🤖 Tunggu robot berpikir</li>
            <li>♻️ Lihat hasilnya</li>
            <li>🗑️ Buang ke tempatnya</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

with colB:
    st.markdown("""
    <div class="result_box" style="background:#E3F2FD; border:2px solid #64B5F6;">
        <h3>🎯 Tujuan</h3>
        <p>
        Aplikasi ini membantu adik-adik
        mengenali jenis sampah:
        </p>
        <ul style="text-align:left;">
            <li>🌿 Organik</li>
            <li>♻️ Anorganik</li>
            <li>⚠️ Berbahaya</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 6. TIPS FOTO
# ==========================================
st.markdown("## 📸 Tips Mengambil Foto")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="result_box" style="background:#F1F8FF; border:2px solid #BBDEFB;">
        <h3>☀️ Terang</h3>
        <p>Foto di tempat<br>yang cukup cahaya</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="result_box" style="background:#F1F8FF; border:2px solid #BBDEFB;">
        <h3>📦 Satu Sampah</h3>
        <p>Jangan campur<br>dengan sampah lain</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="result_box" style="background:#F1F8FF; border:2px solid #BBDEFB;">
        <h3>🎯 Jelas</h3>
        <p>Foto dekat dan<br>tidak blur</p>
    </div>
    """, unsafe_allow_html=True)

st.info("💡 Jika hasil belum tepat, coba foto ulang dengan cahaya lebih terang ya!")

# ==========================================
# 7. LOAD MODEL
# ==========================================
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("modelo_desechos.h5")

with st.spinner("Menyiapkan Robot Pintar... 🤖"):
    try:
        model = load_model()
    except:
        st.error("⚠️ Model AI tidak ditemukan!")
        st.stop()

class_names = [
    'Battery', 'Biological', 'Cardboard', 'Clothes', 'Glass',
    'Metal', 'Paper', 'Plastic', 'Shoes', 'Trash'
]

# ==========================================
# 8. INPUT KAMERA
# ==========================================
st.markdown("## 📷 Ambil Foto Sampah")
img_file = st.camera_input("Klik tombol kamera di bawah 👇")

if img_file:
    st.image(img_file, caption="Foto Sampahmu", width=300)

    img = Image.open(img_file).convert("RGB")
    img = img.resize((128, 128))
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0

    predictions = model.predict(x)
    idx = np.argmax(predictions)
    label = class_names[idx]
    confidence = predictions[0][idx] * 100

    st.caption(f"🔍 Keyakinan AI: {confidence:.0f}%")
    st.progress(int(confidence))

    # ==========================================
    # 9. HASIL KLASIFIKASI
    # ==========================================
    if label == "Biological":
        st.balloons()
        st.markdown("""
        <div class="result_box" style="background:#E3F2FD; border:2px solid #81D4FA;">
            <h1>🌿 ORGANIK</h1>
            <p>Sisa makanan atau daun</p>
            👉 <b>Buang ke Tong HIJAU</b>
        </div>
        """, unsafe_allow_html=True)

    elif label == "Battery":
        st.markdown("""
        <div class="result_box" style="background:#FFEBEE; border:2px solid #EF9A9A;">
            <h1>⚠️ BERBAHAYA</h1>
            <p>Baterai bekas</p>
            👉 <b>Serahkan ke kakak pendamping</b>
        </div>
        """, unsafe_allow_html=True)

    elif label in ["Cardboard", "Paper"]:
        st.markdown("""
        <div class="result_box" style="background:#E3F2FD; border:2px solid #64B5F6;">
            <h1>📦 KERTAS</h1>
            <p>Bisa didaur ulang</p>
            👉 <b>Buang ke Tong BIRU</b>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="result_box" style="background:#E3F2FD; border:2px solid #64B5F6;">
            <h1>♻️ ANORGANIK</h1>
            <p>Plastik, logam, kaca, dll</p>
            👉 <b>Buang ke Tong KUNING</b>
        </div>
        """, unsafe_allow_html=True)
