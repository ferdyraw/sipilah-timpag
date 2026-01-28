import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# ==========================================
# 1. KONFIGURASI HALAMAN (BRANDING TIMPAG)
# ==========================================
st.set_page_config(
    page_title="SiPilah Timpag",
    page_icon="assets/tapaktimpag.jpg",
    layout="centered"
)

NAVY = "#071D3E"

# CSS font + palette (navy) biar lebih modern
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Poppins', system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
    }}

    .main_title {{
        font-size: 2.6rem;
        color: {NAVY};
        text-align: center;
        font-weight: 700;
        letter-spacing: 0.2px;
        line-height: 1.15;
        margin-top: 0.25rem;
    }}
    .sub_title {{
        text-align: center;
        color: rgba(7, 29, 62, 0.78);
        font-size: 1.05rem;
        margin-bottom: 16px;
    }}
    .result_box {{
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        margin-top: 20px;
        font-size: 1.05rem;
        box-shadow: 0 10px 24px rgba(7, 29, 62, 0.12);
        border: 1px solid rgba(7, 29, 62, 0.10);
        background: rgba(255,255,255,0.90);
        backdrop-filter: blur(6px);
    }}

    /* Button style (lebih "navy") */
    .stButton > button {{
        background: {NAVY};
        color: #ffffff;
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 12px;
        padding: 0.65rem 1rem;
        font-weight: 600;
    }}
    .stButton > button:hover {{
        background: #0B2A5C;
        border-color: rgba(255,255,255,0.18);
    }}
    .stButton > button:focus {{
        outline: none;
        box-shadow: 0 0 0 0.2rem rgba(7, 29, 62, 0.25);
    }}

    /* Progress bar */
    [data-testid="stProgressBar"] > div > div {{
        background-color: {NAVY};
    }}

    /* Sembunyikan menu developer Streamlit biar bersih */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# Judul Utama
st.markdown('<div class="main_title">🌴 SiPilah Timpag 🕵️‍♂️</div>', unsafe_allow_html=True)
st.markdown('<div class="sub_title">Si Pintar Memilah dari Desa Timpag</div>', unsafe_allow_html=True)
st.markdown('<div class="sub_title">Om Swastiastu! Adik-adik Desa Timpag, ayo cek sampahmu!</div>', unsafe_allow_html=True)

# ==========================================
# 2. LOAD MODEL (HANYA SEKALI SAAT START)
# ==========================================
@st.cache_resource
def load_model():
    # Pastikan nama file ini SAMA PERSIS dengan file di foldermu
    model = tf.keras.models.load_model('modelo_desechos.h5')
    return model

# Loading state biar kelihatan canggih
with st.spinner('Sedang menyiapkan Robot Pintar... 🤖'):
    try:
        model = load_model()
    except Exception as e:
        st.error("⚠️ File 'modelo_desechos.h5' tidak ditemukan / gagal dibuka!")
        st.caption(f"Detail: {e}")
        st.stop()

# Daftar Kelas (Harus urut Abjad A-Z sesuai training dataset)
class_names = [
    'Battery', 'Biological', 'Cardboard', 'Clothes', 'Glass',
    'Metal', 'Paper', 'Plastic', 'Shoes', 'Trash'
]

# ==========================================
# 3. KAMERA & LOGIKA UTAMA
# ==========================================
img_file = st.camera_input("📸 Tekan tombol ini untuk memotret sampah")

if img_file:
    # Tampilkan foto user
    st.image(img_file, caption="Foto Sampahmu", width=300)
    
    # Preprocessing (Menyesuaikan gambar agar bisa dibaca AI)
    img = Image.open(img_file)
    img = img.resize((128, 128))
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0  # Normalisasi

    # Prediksi
    predictions = model.predict(x)
    predicted_index = np.argmax(predictions)
    label = class_names[predicted_index]
    confidence = predictions[0][predicted_index] * 100

    # ==========================================
    # 4. HASIL & EDUKASI
    # ==========================================
    st.write("---")
    st.caption(f"Tingkat Keyakinan Robot: {confidence:.0f}%")
    st.progress(int(confidence))

    # LOGIKA PENGELOMPOKAN (MAPPING)
    
    # --- ORGANIK ---
    if label == 'Biological':
        st.balloons()
        st.markdown(f"""
        <div class="result_box" style="background-color: #d4edda; color: #155724; border: 2px solid #c3e6cb;">
            <h1>🌿 ORGANIK</h1>
            <p>Ini adalah <b>{label}</b> (Sisa Makanan/Daun).</p>
            <hr>
            👉 <b>Buang ke Tong Warna HIJAU (Teba/Kompos)</b><br>
            <i>"Sampah ini bisa jadi pupuk buat tanaman lho!"</i>
        </div>
        """, unsafe_allow_html=True)

    # --- ANORGANIK (B3 - BERBAHAYA) ---
    elif label == 'Battery':
        st.markdown("""
        <div class="result_box" style="background-color: #f8d7da; color: #721c24; border: 2px solid #f5c6cb;">
            <h1>⚠️ BERBAHAYA (B3)</h1>
            <p>Ini adalah <b>Baterai Bekas</b>.</p>
            <hr>
            👉 <b>JANGAN buang sembarangan!</b><br>
            <i>"Serahkan ke Kakak Pendamping atau pisahkan di wadah khusus ya."</i>
        </div>
        """, unsafe_allow_html=True)

    # --- ANORGANIK (DAUR ULANG - KERTAS) ---
    elif label in ['Cardboard', 'Paper']:
        st.markdown(f"""
        <div class="result_box" style="background-color: #fff3cd; color: #856404; border: 2px solid #ffeeba;">
            <h1>♻️ KERTAS/KARDUS</h1>
            <p>Ini adalah <b>{label}</b>.</p>
            <hr>
            👉 <b>Buang ke Tong Warna BIRU/KUNING</b><br>
            <i>"Kalau bersih dan kering, ini bisa dijual atau didaur ulang!"</i>
        </div>
        """, unsafe_allow_html=True)

    # --- ANORGANIK (RESIDU/LAINNYA) ---
    else:
        # Plastic, Metal, Glass, Shoes, Clothes, Trash
        display_name = label
        if label == 'Glass':
            display_name = "Kaca/Beling (Hati-hati!)"
        if label == 'Metal':
            display_name = "Logam/Kaleng"
        
        st.markdown(f"""
        <div class="result_box" style="background-color: #fff3cd; color: #856404; border: 2px solid #ffeeba;">
            <h1>♻️ ANORGANIK</h1>
            <p>Terdeteksi sebagai: <b>{display_name}</b></p>
            <hr>
            👉 <b>Buang ke Tong Warna KUNING</b><br>
            <i>"Jangan dibakar ya, nanti udaranya jadi kotor."</i>
        </div>
        """, unsafe_allow_html=True)