import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import os # Untuk cek file logo

# ==========================================
# 1. KONFIGURASI HALAMAN & GAYA (ELEGAN BALI)
# ==========================================
st.set_page_config(
    page_title="SiPilah Timpag",
    page_icon="🌴",
    layout="centered"
)

# CSS Custom untuk tampilan yang lebih berkelas
st.markdown("""
    <style>
    /* Mengubah font judul utama menjadi Serif agar lebih elegan */
    .main_title {
        font-family: 'Georgia', serif;
        font-size: 2.8rem;
        color: #2E8B57; /* Hijau tua elegan */
        text-align: center;
        font-weight: bold;
        margin-top: -20px;
    }
    .sub_title {
        font-family: 'Helvetica', sans-serif;
        text-align: center;
        color: #555;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
    
    /* Gaya untuk kotak hasil (Result Box) dengan sentuhan Bali */
    .result_box {
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-top: 25px;
        font-size: 1.1rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        /* Aksen batas bawah seperti warna emas/kayu */
        border-bottom: 5px solid #DAA520; 
    }
    
    /* Menyembunyikan elemen default Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Mengatur agar gambar logo di tengah kolom */
    [data-testid="stImage"] {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. HEADER & LOGO AREA
# ==========================================
# Membuat 3 kolom untuk logo. Menggunakan rasio [1, 2, 1] agar judul di tengah lebih lebar jika logo mau ditaruh di samping judul.
# Tapi untuk request ini, kita taruh logo di atas judul dengan 3 kolom sejajar [1,1,1].
col_uns, col_kkn, col_desa = st.columns(3)

# Fungsi helper untuk menampilkan logo dengan aman
def show_logo(col, path, caption):
    with col:
        if os.path.exists(path):
            st.image(path, use_column_width=True)
        else:
            # Placeholder jika file belum ada agar layout tidak rusak
            st.markdown(f"<div style='text-align:center; color:gray; padding:20px; border:1px dashed gray;'>Logo {caption}</div>", unsafe_allow_html=True)

show_logo(col_uns, "logo_uns.png", "UNS")
show_logo(col_kkn, "logo_kkn.png", "KKN")
show_logo(col_desa, "logo_desa.png", "Desa Timpag")

st.write("") # Spasi sedikit

# Judul Utama
st.markdown('<div class="main_title">🌴 SiPilah Timpag</div>', unsafe_allow_html=True)
st.markdown('<div class="sub_title">Sistem Identifikasi & Pemilahan Sampah Desa Timpag berbasis AI</div>', unsafe_allow_html=True)

# ==========================================
# 3. LOAD MODEL
# ==========================================
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model('model_sampah.h5')
    return model

try:
    model = load_model()
except:
    st.error("⚠️ File 'model_sampah.h5' tidak ditemukan.")
    st.stop()

# Daftar Kelas (Urutan Abjad)
class_names = [
    'Battery', 'Biological', 'Cardboard', 'Clothes', 'Glass',
    'Metal', 'Paper', 'Plastic', 'Shoes', 'Trash'
]

# ==========================================
# 4. PANDUAN PENGGUNAAN (TIPS FOTO)
# ==========================================
# Menggunakan 'st.expander' agar tidak memenuhi layar, tapi mudah diakses.
with st.expander("📜 Panduan & Tips Pengambilan Gambar yang Tepat"):
    st.markdown("""
    Agar Robot AI dapat mengenali sampah dengan akurat, ikuti tips berikut:

    1.  **Cahaya Cukup:** ☀️ Pastikan area tidak terlalu gelap. Cahaya matahari alami paling baik.
    2.  **Satu Objek:** 🍎 Usahakan hanya ada **satu jenis sampah** di dalam foto. Jangan ditumpuk.
    3.  **Fokus & Jelas:** 📷 Pegang HP dengan stabil agar foto tidak buram (blur).
    4.  **Latar Belakang Polos:** ⬜ Jika memungkinkan, taruh sampah di lantai atau tembok yang warnanya tidak ramai.
    5.  **Jarak Pas:** Jangan terlalu jauh, jangan terlalu dekat sampai terpotong.

    *Selamat mencoba!*
    """)

# ==========================================
# 5. KAMERA & LOGIKA UTAMA
# ==========================================
st.write("---")
st.subheader("📸 Mulai Pindai Sampah")
img_file = st.camera_input("Arahkan kamera ke objek sampah, lalu tekan tombol ambil gambar.")

if img_file:
    # Tampilkan foto dengan border tipis agar rapi
    st.markdown('<style>img {border-radius: 10px; border: 3px solid #F5F5DC;}</style>', unsafe_allow_html=True)
    st.image(img_file, caption="Gambar yang diambil", width=300)
    
    # Preprocessing
    img = Image.open(img_file).resize((224, 224))
    x = tf.keras.preprocessing.image.img_to_array(img) / 255.0
    x = np.expand_dims(x, axis=0)

    # Prediksi
    with st.spinner('Menganalisis...'):
        predictions = model.predict(x)
        predicted_index = np.argmax(predictions)
        label = class_names[predicted_index]
        confidence = predictions[0][predicted_index] * 100

    # ==========================================
    # 6. TAMPILKAN HASIL (ELEGAN)
    # ==========================================
    # Kita gunakan warna latar yang lebih lembut (pastel) dan border aksen emas/kayu.

    # --- ORGANIK ---
    if label == 'Biological':
        st.markdown(f"""
        <div class="result_box" style="background-color: #E9F5EC; border-color: #2E8B57; color: #1B4D3E;">
            <h2 style="margin:0; color:#2E8B57;">🌿 ORGANIK (Biological)</h2>
            <p style="margin-top:10px;">Terdeteksi sebagai sisa bahan alam.</p>
            <hr style="border-top: 1px solid #2E8B57;">
            👉 <b>Masukkan ke Tong Kompos / Teba (Hijau)</b><br>
            <small>Akurasi: {confidence:.0f}%</small>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()

    # --- B3 ---
    elif label == 'Battery':
        st.markdown(f"""
        <div class="result_box" style="background-color: #FDEDEE; border-color: #C0392B; color: #922B21;">
            <h2 style="margin:0; color:#C0392B;">⚠️ BERBAHAYA (B3)</h2>
            <p style="margin-top:10px;">Terdeteksi sebagai Baterai/Limbah Berbahaya.</p>
            <hr style="border-top: 1px solid #C0392B;">
            👉 <b>Pisahkan di wadah khusus. Jangan dibuang ke tanah!</b><br>
            <small>Akurasi: {confidence:.0f}%</small>
        </div>
        """, unsafe_allow_html=True)

    # --- ANORGANIK DAUR ULANG ---
    elif label in ['Cardboard', 'Paper', 'Glass', 'Metal', 'Plastic']:
        # Mapping nama Indonesia
        indo_label = label
        if label == 'Cardboard': indo_label = 'Kardus'
        if label == 'Paper': indo_label = 'Kertas'
        if label == 'Glass': indo_label = 'Kaca/Beling'
        if label == 'Metal': indo_label = 'Logam/Kaleng'
        if label == 'Plastic': indo_label = 'Plastik'
        
        st.markdown(f"""
        <div class="result_box" style="background-color: #FFF9E6; border-color: #DAA520; color: #7D6608;">
            <h2 style="margin:0; color:#DAA520;">♻️ ANORGANIK (Daur Ulang)</h2>
            <p style="margin-top:10px;">Terdeteksi sebagai <b>{indo_label}</b>.</p>
            <hr style="border-top: 1px solid #DAA520;">
            👉 <b>Masukkan ke Tong Daur Ulang (Kuning/Biru)</b><br>
            <small>Pastikan dalam keadaan bersih. Akurasi: {confidence:.0f}%</small>
        </div>
        """, unsafe_allow_html=True)

    # --- RESIDU/LAINNYA ---
    else: # Clothes, Shoes, Trash
        indo_label = label
        if label == 'Clothes': indo_label = 'Kain/Baju Bekas'
        if label == 'Shoes': indo_label = 'Sepatu Bekas'
        if label == 'Trash': indo_label = 'Sampah Campuran (Residu)'

        st.markdown(f"""
        <div class="result_box" style="background-color: #F4F6F7; border-color: #7F8C8D; color: #515A5A;">
            <h2 style="margin:0; color:#7F8C8D;">🗑️ ANORGANIK (Residu)</h2>
            <p style="margin-top:10px;">Terdeteksi sebagai <b>{indo_label}</b>.</p>
            <hr style="border-top: 1px solid #7F8C8D;">
            👉 <b>Masukkan ke Tong Residu (Abu-abu/Merah)</b><br>
            <small>Akurasi: {confidence:.0f}%</small>
        </div>
        """, unsafe_allow_html=True)