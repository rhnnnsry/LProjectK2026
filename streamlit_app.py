import streamlit as st
import pandas as pd
import time

# Konfigurasi halaman
st.set_page_config(
    page_title="Ensiklopedia Unsur Kimia - Kelompok 13",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# SISTEM DETEKSI KLIK (Menangkap Simbol Unsur dari URL)
# ==============================================================================
if "element" in st.query_params:
    st.session_state.active_element = st.query_params["element"]
    # KUNCI PERBAIKAN 1: Paksa memori aplikasi untuk tetap di halaman Tabel Periodik!
    st.session_state.current_page = "🧪 Tabel Periodik"
    # Bersihkan URL secara instan agar pop-up tidak muncul berulang kali saat refresh
    st.query_params.clear()

# Custom CSS
st.markdown('''
<style>
    /* Latar Belakang Utama Aplikasi */
    .stApp {
        background: linear-gradient(135deg, #FFF6FB, #F3EEFF, #EAF8FF) !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Latar Belakang Sidebar */
    [data-testid="stSidebar"] {
        background-color: #F4ECFF !important;
        border-right: 2px dashed #DCC6FF;
    }
    
    /* Gaya Teks Umum */
    h1, h2, h3, p, span, label {
        color: #4A3E56 !important;
    }
    
    /* Tombol Navigasi Kustom di Sidebar */
    .stSidebar nav li a {
        border-radius: 10px;
        margin: 4px 0;
        transition: all 0.3s ease;
    }
    .stSidebar nav li a:hover {
        background-color: #EAD9FF !important;
        transform: scale(1.02);
    }
    
    /* Wadah Identitas Kelompok di Beranda */
    .identity-card {
        background: rgba(255, 255, 255, 0.7);
        border: 2px solid #F4C2E7;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(244, 194, 231, 0.3);
        margin-top: 20px;
    }
    
    .member-name {
        font-weight: 600;
        color: #5D4A70;
        background: #FFF0FA;
        padding: 6px 12px;
        border-radius: 20px;
        display: inline-block;
        margin: 4px;
        border: 1px solid #F4C2E7;
    }

    /* KOTAK UNSUR TABEL PERIODIK (BERWARNA & BISA DIKLIK) */
    .element-box {
        border-radius: 12px !important;
        padding: 10px !important;
        text-align: center !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05) !important;
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease !important;
        cursor: pointer;
        border: 1px solid rgba(0,0,0,0.03);
        margin-bottom: 12px;
        min-height: 105px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    /* Efek Hover Membesar Sedikit */
    .element-box:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 8px 16px rgba(165, 140, 190, 0.2) !important;
        z-index: 10;
        border: 2px solid #F4C2E7;
    }
    
    .atomic-number {
        font-size: 0.75rem !important;
        font-weight: bold !important;
        align-self: flex-start;
        opacity: 0.7;
    }
    
    .element-symbol {
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        margin: -2px 0 !important;
        color: #4A3E56 !important;
    }
    
    .element-name {
        font-size: 0.7rem !important;
        font-weight: 500 !important;
        text-overflow: ellipsis;
        white-space: nowrap;
        overflow: hidden;
        width: 100%;
        color: #4A3E56 !important;
    }
</style>
''', unsafe_allow_html=True)

# DATA KATEGORI WARNA PASTEL
COLOR_MAP = {
    "Logam Alkali": "#FFB6C1",
    "Logam Alkali Tanah": "#FFD6A5",
    "Logam Transisi": "#FFF3B0",
    "Logam Lainnya": "#CDEAC0",
    "Metaloid": "#B5EAEA",
    "Nonlogam": "#BDE0FE",
    "Halogen": "#D8B4FE",
    "Gas Mulia": "#F8C8DC",
    "Lantanida": "#DCC6FF",
    "Aktinida": "#F4C2E7"
}

# DATA MENTAH UNSUR
elements_data = [
    {"Symbol": "H", "Name": "Hydrogen", "AtomicNumber": 1, "Period": 1, "Group": 1, "Category": "Nonlogam"},
    {"Symbol": "He", "Name": "Helium", "AtomicNumber": 2, "Period": 1, "Group": 18, "Category": "Gas Mulia"},
    {"Symbol": "Li", "Name": "Lithium", "AtomicNumber": 3, "Period": 2, "Group": 1, "Category": "Logam Alkali"},
    {"Symbol": "Be", "Name": "Beryllium", "AtomicNumber": 4, "Period": 2, "Group": 2, "Category": "Logam Alkali Tanah"},
    {"Symbol": "B", "Name": "Boron", "AtomicNumber": 5, "Period": 2, "Group": 13, "Category": "Metaloid"},
    {"Symbol": "C", "Name": "Carbon", "AtomicNumber": 6, "Period": 2, "Group": 14, "Category": "Nonlogam"},
    {"Symbol": "N", "Name": "Nitrogen", "AtomicNumber": 7, "Period": 2, "Group": 15, "Category": "Nonlogam"},
    {"Symbol": "O", "Name": "Oxygen", "AtomicNumber": 8, "Period": 2, "Group": 16, "Category": "Nonlogam"},
    {"Symbol": "F", "Name": "Fluorine", "AtomicNumber": 9, "Period": 2, "Group": 17, "Category": "Halogen"},
    {"Symbol": "Ne", "Name": "Neon", "AtomicNumber": 10, "Period": 2, "Group": 18, "Category": "Gas Mulia"},
    {"Symbol": "Na", "Name": "Sodium", "AtomicNumber": 11, "Period": 3, "Group": 1, "Category": "Logam Alkali"},
    {"Symbol": "Mg", "Name": "Magnesium", "AtomicNumber": 12, "Period": 3, "Group": 2, "Category": "Logam Alkali Tanah"},
    {"Symbol": "Al", "Name": "Aluminum", "AtomicNumber": 13, "Period": 3, "Group": 13, "Category": "Logam Lainnya"},
    {"Symbol": "Si", "Name": "Silicon", "AtomicNumber": 14, "Period": 3, "Group": 14, "Category": "Metaloid"},
    {"Symbol": "P", "Name": "Phosphorus", "AtomicNumber": 15, "Period": 3, "Group": 15, "Category": "Nonlogam"},
    {"Symbol": "S", "Name": "Sulfur", "AtomicNumber": 16, "Period": 3, "Group": 16, "Category": "Nonlogam"},
    {"Symbol": "Cl", "Name": "Chlorine", "AtomicNumber": 17, "Period": 3, "Group": 17, "Category": "Halogen"},
    {"Symbol": "Ar", "Name": "Argon", "AtomicNumber": 18, "Period": 3, "Group": 18, "Category": "Gas Mulia"},
    {"Symbol": "K", "Name": "Potassium", "AtomicNumber": 19, "Period": 4, "Group": 1, "Category": "Logam Alkali"},
    {"Symbol": "Ca", "Name": "Calcium", "AtomicNumber": 20, "Period": 4, "Group": 2, "Category": "Logam Alkali Tanah"},
    {"Symbol": "Sc", "Name": "Scandium", "AtomicNumber": 21, "Period": 4, "Group": 3, "Category": "Logam Transisi"},
    {"Symbol": "Ti", "Name": "Titanium", "AtomicNumber": 22, "Period": 4, "Group": 4, "Category": "Logam Transisi"},
    {"Symbol": "V", "Name": "Vanadium", "AtomicNumber": 23, "Period": 4, "Group": 5, "Category": "Logam Transisi"},
    {"Symbol": "Cr", "Name": "Chromium", "AtomicNumber": 24, "Period": 4, "Group": 6, "Category": "Logam Transisi"},
    {"Symbol": "Mn", "Name": "Manganese", "AtomicNumber": 25, "Period": 4, "Group": 7, "Category": "Logam Transisi"},
    {"Symbol": "Fe", "Name": "Iron", "AtomicNumber": 26, "Period": 4, "Group": 8, "Category": "Logam Transisi"},
    {"Symbol": "Co", "Name": "Cobalt", "AtomicNumber": 27, "Period": 4, "Group": 9, "Category": "Logam Transisi"},
    {"Symbol": "Ni", "Name": "Nickel", "AtomicNumber": 28, "Period": 4, "Group": 10, "Category": "Logam Transisi"},
    {"Symbol": "Cu", "Name": "Copper", "AtomicNumber": 29, "Period": 4, "Group": 11, "Category": "Logam Transisi"},
    {"Symbol": "Zn", "Name": "Zinc", "AtomicNumber": 30, "Period": 4, "Group": 12, "Category": "Logam Transisi"},
    {"Symbol": "Ga", "Name": "Gallium", "AtomicNumber": 31, "Period": 4, "Group": 13, "Category": "Logam Lainnya"},
    {"Symbol": "Ge", "Name": "Germanium", "AtomicNumber": 32, "Period": 4, "Group": 14, "Category": "Metaloid"},
    {"Symbol": "As", "Name": "Arsenic", "AtomicNumber": 33, "Period": 4, "Group": 15, "Category": "Metaloid"},
    {"Symbol": "Se", "Name": "Selenium", "AtomicNumber": 34, "Period": 4, "Group": 16, "Category": "Nonlogam"},
    {"Symbol": "Br", "Name": "Bromine", "AtomicNumber": 35, "Period": 4, "Group": 17, "Category": "Halogen"},
    {"Symbol": "Kr", "Name": "Krypton", "AtomicNumber": 36, "Period": 4, "Group": 18, "Category": "Gas Mulia"},
]
df = pd.DataFrame(elements_data)

# ==============================================================================
# FUNGSI EFEK LOADING SCREEN
# ==============================================================================
def trigger_loading():
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        st.markdown("<br><br>", unsafe_allow_html=True)
        cols = st.columns([1, 2, 1])
        with cols[1]:
            st.image(
                "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExeHFsNXM0aHF5bGhlNjgzYm14eW05dzUwOXMwdWp4ZXF6ZXUybW0wZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/BZyYk1m8x1B3GMH1V1/giphy.gif",
                caption="Mempersiapkan Ramuan Data... 🧪✨",
                use_container_width=True
            )
        time.sleep(1.2)
    loading_placeholder.empty()

# ==============================================================================
# DEFINISI HALAMAN-HALAMAN APLIKASI
# ==============================================================================
def show_page_beranda():
    st.markdown("# 🏠 Selamat Datang di Ensiklopedia Unsur Kimia ✨")
    st.markdown("### *Sains itu Seru, Indah, dan Berwarna! ☁️💖🧪*")
    st.write("---")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("#### 🌟 Deskripsi Aplikasi")
        st.write(
            "Ensiklopedia Unsur Kimia adalah platform edukasi interaktif berbasis web yang didesain "
            "khusus untuk mempermudah visualisasi dan pemahaman mengenai tabel periodik unsur-unsur kimia. "
            "Dikemas dengan desain bertema *Pastel Kawaii Chemistry*, aplikasi ini membuat aktivitas belajar sains terasa menyenangkan."
        )
        
        st.markdown("#### 🎯 Tujuan Aplikasi")
        st.write(
            "Menyediakan media pembelajaran kimia digital yang modern, interaktif, serta mudah diakses "
            "oleh mahasiswa, pelajar, maupun dosen untuk menganalisis data periodisitas unsur secara cepat."
        )
        
        st.markdown("#### 💡 Manfaat Aplikasi")
        st.markdown(
            "- **Visualisasi Interaktif:** Memudahkan klasifikasi golongan unsur lewat visualisasi kode warna kustom.\n"
            "- **Aksesibilitas Informasi:** Membantu mengecek nomor atom, simbol, dan kategori unsur secara instan.\n"
            "- **Pengalaman Belajar Menyenangkan:** Mengurangi kesan kaku pada pelajaran kimia dengan visualisasi estetik."
        )
        
        st.markdown("#### 🛠️ Fitur yang Tersedia")
        st.markdown(
            "- 🧭 **Navigasi Multi-Halaman:** Pemisahan dashboard utama dengan ruang lab data.\n"
            "- 📊 **Interactive Periodic Layout:** Tata letak grid dinamis sesuai susunan asli sistem periodik unsur.\n"
            "- 🎨 **Pastel Category Highlights:** Pembedaan blok warna pastel yang responsif dan memanjakan mata."
        )
        
    with col2:
        st.image(
            "https://i.pinimg.com/736x/2a/60/ad/2a60ade401e17068a8f7db4798312793.jpg", 
            caption="Aesthetic Chemistry Circle 🔬✨",
            use_container_width=True
        )
    
    st.write("---")
    st.markdown("### 🗂️ Informasi Proyek & Pengembang")
    
    st.markdown('''
        <div class="identity-card">
            <h4 style='margin-top:0;'>✨ Ensiklopedia Unsur Kimia</h4>
            <p style='font-size: 1.05rem;'><b>Proyek Kelompok 13 – Politeknik AKA Bogor</b></p>
            <p style='margin-bottom: 8px;'><b>Nama Editor / Pengembang:</b></p>
            <div>
                <span class="member-name">🌸 Hayu Raihanun (2560641)</span>
                <span class="member-name">🌸 Niken Sri Uttari (2560727)</span>
                <span class="member-name">🌸 Nisfy Sabrina Flowerridha Supriyadi (2560728)</span>
                <span class="member-name">🍀 Raifan Syahdan Putra Raya (2560742)</span>
            </div>
            <p style='margin-top:15px; font-size:0.85rem; opacity:0.8;'>🔬 <i>Dibuat dengan dedikasi penuh untuk praktikum komputasi kimia di Kampus Politeknik AKA Bogor.</i></p>
        </div>
    ''', unsafe_allow_html=True)

# ==============================================================================
# FUNGSI POP-UP (MODAL) DETAIL UNSUR
# ==============================================================================
@st.dialog("✨ Informasi Detail Unsur")
def show_element_details(element):
    # Ambil warna dari COLOR_MAP
    bg_color = COLOR_MAP.get(element['Category'], '#FFFFFF')
    
    # Header Pop-up dengan warna pastel kategori
    st.markdown(
        f"""
        <div style="background-color: {bg_color}; padding: 20px; border-radius: 15px; text-align: center; border: 2px dashed #DCC6FF; margin-bottom: 20px;">
            <h1 style="font-size: 4rem; margin: 0; color: #4A3E56 !important;">{element['Symbol']}</h1>
            <h3 style="margin: 0; color: #4A3E56 !important;">{element['Name']}</h3>
        </div>
        """, unsafe_allow_html=True
    )
    
    # Layout Data
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**🧬 Nomor Atom:** {element['AtomicNumber']}")
        st.write(f"**🏷️ Kategori:** {element['Category']}")
    with col2:
        st.write(f"**📏 Golongan:** {element['Group']}")
        st.write(f"**📅 Periode:** {element['Period']}")
        
    st.info(
        f"**{element['Name']}** ({element['Symbol']}) adalah unsur kimia dengan nomor atom **{element['AtomicNumber']}** "
        f"yang terletak pada periode {element['Period']} dan golongan {element['Group']}. "
        f"Unsur ini diklasifikasikan ke dalam kelompok **{element['Category']}**."
    )


# ==============================================================================
# HALAMAN TABEL PERIODIK
# ==============================================================================
def show_page_tabel_periodik():
    st.markdown("# 🧪 Tabel Periodik Unsur ✨")
    st.markdown("### *Klik simbol unsur untuk melihat penjelasan lengkapnya 💖🔬*")
    st.write("---")
    
    st.markdown("#### 🎨 Petunjuk Kategori Unsur:")
    legend_cols = st.columns(5)
    categories = list(COLOR_MAP.keys())
    
    for idx, cat in enumerate(categories):
        col_idx = idx % 5
        with legend_cols[col_idx]:
            st.markdown(
                f'<div style="background-color:{COLOR_MAP[cat]}; padding:6px; border-radius:8px; text-align:center; '
                f'font-size:0.8rem; font-weight:bold; color:#4A3E56; margin-bottom:5px; border: 1px solid rgba(0,0,0,0.05);">'
                f'{cat}</div>', 
                unsafe_allow_html=True
            )
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    max_period = int(df['Period'].max())
    max_group = 18
    
    for period in range(1, max_period + 1):
        grid_cols = st.columns(max_group)
        
        for group in range(1, max_group + 1):
            match = df[(df['Period'] == period) & (df['Group'] == group)]
            
            with grid_cols[group - 1]:
                if not match.empty:
                    element = match.iloc[0]
                    
                    # Ambil warna latar belakang yang sesuai dari COLOR_MAP
                    bg_color = COLOR_MAP.get(element['Category'], '#FFFFFF')
                    
                    # HTML Card Interaktif (Membungkus card dengan tag link <a>)
                    box_html = f"""
                    <a href="?element={element['Symbol']}" target="_self" style="text-decoration: none;">
                        <div class="element-box" style="background-color: {bg_color};">
                            <div class="atomic-number">{element['AtomicNumber']}</div>
                            <div class="element-symbol">{element['Symbol']}</div>
                            <div class="element-name">{element['Name']}</div>
                        </div>
                    </a>
                    """
                    st.markdown(box_html, unsafe_allow_html=True)
                else:
                    st.write("")

    st.markdown(
        "<center style='margin-top: 30px; font-size: 1.5rem;'>"
        "✨ ☁️ 💖 🧪 🔬 💖 ☁️ ✨"
        "</center>", 
        unsafe_allow_html=True
    )

# ==============================================================================
# SISTEM KONTROL NAVIGASI SIDEBAR
# =============================================================================='''''''''''''''
st.sidebar.markdown("### 🧭 MENU NAVIGASI")
st.sidebar.markdown("✨ *Kawaii Chem Lab V.2026* ✨")

# Daftar halaman
pages = ["🏠 Beranda", "🧪 Tabel Periodik"]

if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Beranda"

try:
    default_index = pages.index(st.session_state.current_page)
except ValueError:
    default_index = 0

page_selection = st.sidebar.radio(
    "Pilih Halaman:",
    pages,
    index=default_index,
    label_visibility="collapsed"
)

if page_selection != st.session_state.current_page:
    st.session_state.current_page = page_selection
    trigger_loading()

st.sidebar.write("---")
st.sidebar.markdown("#### 🔬 Kelompok 13 - AKA")
st.sidebar.caption("• Hayu Raihanun\n• Niken Sri U.\n• Nisfy Sabrina F.S.\n• Raifan Syahdan P.R.")

if st.session_state.current_page == "🏠 Beranda":
    show_page_beranda()
elif st.session_state.current_page == "🧪 Tabel Periodik":
    show_page_tabel_periodik()
    
# ==============================================================================
# POP-UP
# ==============================================================================
if "active_element" in st.session_state and st.session_state.active_element:
    selected_symbol = st.session_state.active_element
    match_element = df[df['Symbol'] == selected_symbol]
    if not match_element.empty:
        show_element_details(match_element.iloc[0])
    
    # Hapus state setelah dialog ditampilkan supaya tidak tersangkut
    st.session_state.active_element = None
