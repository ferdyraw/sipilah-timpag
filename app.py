import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import os

# ==========================================
# 1. KONFIGURASI & GAYA TAMPILAN (CSS)
# ==========================================
st.set_page_config(
    page_title="SiPilah Timpag",
    page_icon="🌴",
    layout="centered"
)

# Menyuntikkan CSS untuk kustomisasi tingkat lanjut
st.markdown("""
    <style>
    /* Mengubah font judul utama menjadi lebih berkelas */
    h1 {
        font-family: 'Merriweather', 'Georgia', serif !important;
        color: #2E8B57 !important;
        font-weight: 700 !important;
        text-align: center;
    }
    
    /* Gaya untuk Sub-judul */
    .sub_header {
        text-align: center;
        color: #666;
        font-style: italic;
        margin-top: -15px;
        margin-bottom: 30px;
    }

    /* Gaya KARTU HASIL (Result Card) yang elegan */
    .result-card {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-top: 20px;
        border-left: 8px solid #ccc; /* Default border color */
    }
    
    /* Warna spesifik untuk Organik */
    .card-organic {
        border-left-color: #2E8B57 !important; /* Hijau */
    }
    h2.organic-title { color: #2E8B57; margin: 0; }
    
    /* Warna spesifik untuk Anorganik */
    .card-anorganic {
        border-left-color: #DAA520 !important; /* Emas/Kuning Tua */
    }
    h2.anorganic-title { color: #DAA520; margin: 0; }

    /* Membersihkan tampilan default Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Mengatur posisi logo agar rata tengah di kolomnya */
    [data-testid="stImage"] > img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        max-height: 80px; /* Batasi tinggi logo biar rapi */
        object-fit: contain;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. AREA LOGO & JUDUL
# ==========================================
# Membuat 3 kolom untuk logo
col1, col2, col3 = st.columns(3)

# Fungsi helper untuk menampilkan logo/placeholder
def display_logo(col, path, label):
    with col:
        if os.path.exists(path):
            st.image(path)
        else:
            # Tampilan placeholder yang rapi jika logo belum ada
            st.markdown(f"""
                <div style="text-align:center; padding: 15px; border: 1px dashed #ccc; color: #999; font-size: 0.8em; border-radius: 8px;">
                    Logo {label}
                </div>
            """, unsafe_allow_html=True)

display_logo(col1, "logo_uns.png", "UNS")
display_logo(col2, "logo_kkn.png", "KKN")
display_logo(col3, "logo_desa.png", "Desa Timpag")

st.write("") # Spasi

# Judul Aplikasi
st.title("🌴 SiPilah Timpag")
st.markdown('<div class="sub_header">Sistem Cerdas Pemilahan Sampah Desa Timpag</div>', unsafe_allow_html=True)

# ==========================================
# 3. LOGIKA AI & PEMETAAN KATEGORI
# ==========================================
@st.cache_resource
def load_model():
    # Ganti nama file jika berbeda
    model = tf.keras.models.load_model('modelo_desechos.h5')
    return model

try:
    model = load_model()
except:
    st.error("⚠️ File model tidak ditemukan. Mohon hubungi administrator.")
    st.stop()

# 10 Kelas Asli dari Dataset
RAW_CLASSES = [
    'Battery', 'Biological', 'Cardboard', 'Clothes', 'Glass',
    'Metal', 'Paper', 'Plastic', 'Shoes', 'Trash'
]

# PEMETAAN PENTING: Menyederhanakan 10 kelas menjadi 2 Kategori Utama
# Kita anggap biological sebagai satu-satunya organik basah. Sisanya anorganik/residu.
CATEGORY_MAP = {
    'Biological': 'ORGANIK',
    'Battery':    'ANORGANIK',
    'Cardboard':  'ANORGANIK',
    'Clothes':    'ANORGANIK',
    'Glass':      'ANORGANIK',
    'Metal':      'ANORGANIK',
    'Paper':      'ANORGANIK',
    'Plastic':    'ANORGANIK',
    'Shoes':      'ANORGANIK',
    'Trash':      'ANORGANIK'
}

# ==========================================
# 4. PANDUAN & INPUT KAMERA
# ==========================================
with st.expander("📋 Panduan & Tips Pengambilan Gambar"):
    st.markdown("""
    **Agar hasil deteksi akurat, mohon perhatikan:**
    1.  **Pencahayaan:** Pastikan objek sampah terlihat jelas dan terang.
    2.  **Fokus Tunggal:** Usahakan hanya ada satu jenis sampah utama dalam foto.
    3.  **Jarak:** Ambil foto dari jarak yang pas, tidak terlalu jauh atau terlalu dekat.
    4.  **Latar Belakang:** Latar belakang yang bersih (misal: lantai/tembok polos) lebih baik.
    """)

st.write("---")
st.write("**Silakan ambil foto sampah:**")
img_file = st.camera_input("Arahkan kamera", label_visibility='collapsed')

if img_file:
    # Proses Gambar
    img = Image.open(img_file).resize((224, 224))
    x = tf.keras.preprocessing.image.img_to_array(img) / 255.0
    x = np.expand_dims(x, axis=0)

    # Prediksi AI
    with st.spinner('Menganalisis citra...'):
        predictions = model.predict(x)
        predicted_index = np.argmax(predictions)
        
        # Mendapatkan label spesifik (misal: 'Plastic')
        specific_label = RAW_CLASSES[predicted_index]
        
        # Mendapatkan kategori utama (misal: 'ANORGANIK') berdasarkan peta di atas
        main_category = CATEGORY_MAP[specific_label]
        
        confidence = predictions[0][predicted_index]

    # ==========================================
    # 5. TAMPILAN HASIL (KARTU ELEGAN)
    # ==========================================
    st.write("") # Spasi

    # --- KARTU HASIL ORGANIK ---
    if main_category == 'ORGANIK':
        st.markdown(f"""
        <div class="result-card card-organic">
            <h2 class="organic-title">🌿 Sampah Organik</h2>
            <p style="color: #666; margin-top: 5px;">Terdeteksi sebagai: <b>{specific_label}</b> (Sisa Alam)</p>
            <hr style="border-top: 1px solid #eee;">
            <p><b>Rekomendasi Penanganan:</b><br>
            Dapat diolah menjadi pupuk kompos atau dimasukkan ke lubang biopori/teba di halaman rumah.</p>
        </div>
        """, unsafe_allow_html=True)

    # --- KARTU HASIL ANORGANIK ---
    else:
        # Sedikit penyesuaian teks untuk B3 (Baterai) agar tetap ada warning
        tindakan = "Sebaiknya dikumpulkan untuk didaur ulang atau dibuang ke tempat sampah anorganik."
        if specific_label == 'Battery':
            tindakan = "⚠️ <b>Ini termasuk Limbah B3 (Berbahaya).</b> Jangan dibuang sembarangan ke tanah. Pisahkan khusus."

        st.markdown(f"""
        <div class="result-card card-anorganic">
            <h2 class="anorganic-title">♻️ Sampah Anorganik</h2>
            <p style="color: #666; margin-top: 5px;">Terdeteksi sebagai: <b>{specific_label}</b></p>
            <hr style="border-top: 1px solid #eee;">
            <p><b>Rekomendasi Penanganan:</b><br>
            {tindakan}</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.caption(f"Tingkat Keyakinan Sistem: {confidence:.2%}")