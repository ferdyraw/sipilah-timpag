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

# CSS biar tombol dan judulnya menarik buat anak-anak
st.markdown("""
    <style>
    .main_title {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        font-weight: bold;
        font-family: 'Comic Sans MS', sans-serif;
    }
    .sub_title {
        text-align: center;
        color: #555;
        font-size: 1.2rem;
        margin-bottom: 20px;
    }
    .result_box {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-top: 20px;
        font-size: 1.1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    /* Sembunyikan menu developer Streamlit biar bersih */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Judul Utama
st.markdown('<div class="main_title">🌴 SiPilah Timpag 🕵️‍♂️</div>', unsafe_allow_html=True)
st.markdown('<div class="sub_title">Rahajeng Semeng! Adik-adik Desa Timpag, ayo cek sampahmu!</div>', unsafe_allow_html=True)

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
    except:
        st.error("⚠️ File 'model_sampah.h5' tidak ditemukan di folder ini!")
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
        st.markdown(f"""
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
        if label == 'Glass': display_name = "Kaca/Beling (Hati-hati!)"
        if label == 'Metal': display_name = "Logam/Kaleng"
        
        st.markdown(f"""
        <div class="result_box" style="background-color: #fff3cd; color: #856404; border: 2px solid #ffeeba;">
            <h1>♻️ ANORGANIK</h1>
            <p>Terdeteksi sebagai: <b>{display_name}</b></p>
            <hr>
            👉 <b>Buang ke Tong Warna KUNING</b><br>
            <i>"Jangan dibakar ya, nanti udaranya jadi kotor."</i>
        </div>
        """, unsafe_allow_html=True)