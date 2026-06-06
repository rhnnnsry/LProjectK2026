import streamlit as st
import streamlit as st
import pandas as pd

# Konfigurasi halaman
st.set_page_config(
    page_title="Ensiklopedia Unsur Kimia - Kelompok 13",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
&lt;style&gt;
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

    /* KOTAK UNSUR TABEL PERIODIK (Aesthetic &amp; Modern) */
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
        transform: scale(1.08) !important;
        box-shadow: 0 8px 16px rgba(165, 140, 190, 0.2) !important;
        z-index: 10;
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
    }
    
    .element-name {
        font-size: 0.7rem !important;
        font-weight: 500 !important;
        text-overflow: ellipsis;
        white-space: nowrap;
        overflow: hidden;
        width: 100%;
    }
&lt;/style&gt;
""", unsafe_allow_html=True)

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
        st.markdown("&lt;br&gt;&lt;br&gt;", unsafe_allow_html=True)
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
    st.markdown("### 🗂️ Informasi Proyek &amp; Pengembang")
    
    st.markdown(
        """
        &lt;div class="identity-card"&gt;
            &lt;h4 style='margin-top:0;'&gt;✨ Ensiklopedia Unsur Kimia&lt;/h4&gt;
            &lt;p style='font-size: 1.05rem;'&gt;&lt;b&gt;Proyek Kelompok 13 – Politeknik AKA Bogor&lt;/b&gt;&lt;/p&gt;
            &lt;p style='margin-bottom: 8px;'&gt;&lt;b&gt;Nama Editor / Pengembang:&lt;/b&gt;&lt;/p&gt;
            &lt;div&gt;
                &lt;span class="member-name"&gt;🌸 Hayu Raihanun (2560641)&lt;/span&gt;
                &lt;span class="member-name"&gt;🌸 Niken Sri Uttari (2560727)&lt;/span&gt;
                &lt;span class="member-name"&gt;🌸 Nisfy Sabrina Flowerridha Supriyadi (2560728)&lt;/span&gt;
                &lt;span class="member-name"&gt;🍀 Raifan Syahdan Putra Raya (2560742)&lt;/span&gt;
            &lt;/div&gt;
            &lt;p style='margin-top:15px; font-size:0.85rem; opacity:0.8;'&gt;🔬 &lt;i&gt;Dibuat dengan dedikasi penuh untuk praktikum komputasi kimia di Kampus Politeknik AKA Bogor.&lt;/i&gt;&lt;/p&gt;
        &lt;/div&gt;
        """, 
        unsafe_allow_html=True
    )

def show_page_tabel_periodik():
    st.markdown("# 🧪 Tabel Periodik Unsur ✨")
    st.markdown("### *Klik &amp; jelajahi blok unsur pastel kawaii chemistry kamu 💖🔬*")
    st.write("---")
    
    st.markdown("#### 🎨 Petunjuk Kategori Unsur:")
    legend_cols = st.columns(5)
    categories = list(COLOR_MAP.keys())
    
    for idx, cat in enumerate(categories):
        col_idx = idx % 5
        with legend_cols[col_idx]:
            st.markdown(
                f'&lt;div style="background-color:{COLOR_MAP[cat]}; padding:6px; border-radius:8px; text-align:center; '
                f'font-size:0.8rem; font-weight:bold; color:#4A3E56; margin-bottom:5px; border: 1px solid rgba(0,0,0,0.05);"&gt;'
                f'{cat}&lt;/div&gt;', 
                unsafe_allow_html=True
            )
            
    st.write("&lt;br&gt;", unsafe_allow_html=True)
    
    max_period = int(df['Period'].max())
    max_group = 18
    
    for period in range(1, max_period + 1):
        grid_cols = st.columns(max_group)
        
        for group in range(1, max_group + 1):
            match = df[(df['Period'] == period) &amp; (df['Group'] == group)]
            
            with grid_cols[group - 1]:
                if not match.empty:
                    element = match.iloc[0]
                    bg_color = COLOR_MAP.get(element['Category'], '#FFFFFF')
                    
                    box_html = f"""
                    &lt;div class="element-box" style="background-color: {bg_color};"&gt;
                        &lt;div class="atomic-number"&gt;{element['AtomicNumber']}&lt;/div&gt;
                        &lt;div class="element-symbol"&gt;{element['Symbol']}&lt;/div&gt;
                        &lt;div class="element-name"&gt;{element['Name']}&lt;/div&gt;
                    &lt;/div&gt;
                    """
                    # Diganti ke st.markdown agar aman di versi lama
                    st.markdown(box_html, unsafe_allow_html=True)
                else:
                    st.write("")

    st.markdown(
        "&lt;center style='margin-top: 30px; font-size: 1.5rem;'&gt;"
        "✨ ☁️ 💖 🧪 🔬 💖 ☁️ ✨"
        "&lt;/center&gt;", 
        unsafe_allow_html=True
    )

# ==============================================================================
# SISTEM KONTROL NAVIGASI MULTI-HALAMAN &amp; SIDEBAR
# ==============================================================================
st.sidebar.markdown("### 🧭 MENU NAVIGASI")
st.sidebar.markdown("✨ *Kawaii Chem Lab V.2026* ✨")

if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Beranda"

page_selection = st.sidebar.radio(
    "Pilih Halaman:",
    ["🏠 Beranda", "🧪 Tabel Periodik"],
    label_visibility="collapsed"
)

if page_selection != st.session_state.current_page:
    st.session_state.current_page = page_selection
    trigger_loading()

st.sidebar.write("---")
st.sidebar.markdown("#### 🔬 Kelompok 13 - AKA")
st.sidebar.caption("• Hayu Raihanun\n• Niken Sri U.\n• Nisfy Sabrina F.S.\n• Raifan Syahdan P.R.")

if page_selection == "🏠 Beranda":
    show_page_beranda()
elif page_selection == "🧪 Tabel Periodik":
    show_page_tabel_periodik()
</div></div></div></div></div></div><div class="contents print:hidden"><div class="flex flex-col relative max-md:absolute max-md:inset-x-0 max-md:top-0 max-md:hidden md:z-0" inert=""><div class="md:absolute md:right-0 md:top-0 z-20 max-md:w-fit max-md:self-end max-md:pointer-events-auto flex justify-end shrink-0 min-w-0 pr-3 items-center gap-1 !h-12 transition-opacity duration-150 ease-in-out md:opacity-0 md:pointer-events-none" data-testid="wiggle-controls-actions"><button type="button" data-cds="Button" class="cds-reset group/btn relative isolate inline-flex shrink-0 items-center justify-center gap-1.5 whitespace-nowrap select-none border-0 outline-none rounded h-control font-sans text-body font-medium [&amp;:disabled:not([aria-busy])]:opacity-50 disabled:pointer-events-none transition-shadow duration-fast focus-visible:shadow-focus text-primary aria-pressed:text-accent aspect-square w-control px-0" aria-pressed="true" aria-label="Files" data-testid="wiggle-controls-actions-toggle"><span aria-hidden="true" class="absolute -z-[1] rounded-[inherit] transition-colors duration-fast group-focus-visible/btn:shadow-[inset_0_0_0_1px_var(--cds-page-bg)] bg-transparent group-hover/btn:bg-fill-ghost-hover group-aria-expanded/btn:bg-fill-ghost-hover inset-0 group-aria-pressed/btn:bg-accent group-hover/btn:group-aria-pressed/btn:bg-accent cds-btn-squish "></span><span class="inline-flex items-center gap-1 "><span data-cds="Icon" aria-hidden="true" style="font-family: var(--font-anthropicons, Anthropicons-Variable); font-feature-settings: &quot;liga&quot; 0; font-optical-sizing: auto; font-style: normal; font-variation-settings: normal; line-height: 1; width: 1em; height: 1em; display: flex; align-items: center; justify-content: center; flex-shrink: 0; user-select: none; font-size: 20px; font-weight: 433.3;"></span></span></button><button type="button" data-cds="Button" data-size="sm" class="cds-reset group/btn relative isolate inline-flex shrink-0 items-center justify-center gap-1.5 whitespace-nowrap select-none border-0 outline-none rounded h-control font-sans text-body font-medium [&amp;:disabled:not([aria-busy])]:opacity-50 disabled:pointer-events-none transition-shadow duration-fast focus-visible:shadow-focus text-primary aria-pressed:text-accent px-md" data-testid="wiggle-controls-actions-share"><span aria-hidden="true" class="absolute -z-[1] rounded-[inherit] transition-colors duration-fast group-focus-visible/btn:shadow-[inset_0_0_0_1px_var(--cds-page-bg)] bg-fill-secondary group-hover/btn:bg-fill-secondary-hover group-aria-expanded/btn:bg-fill-secondary-hover inset-0 group-aria-pressed/btn:bg-accent group-hover/btn:group-aria-pressed/btn:bg-accent cds-btn-squish shadow-field"></span><span class="inline-flex items-center gap-1 ">Share</span></button></div><div class="overflow-x-hidden overflow-y-auto md:h-[calc(100%-56px)] max-md:h-full max-md:border-t max-md:border-border-300 max-md:bg-bg-100 md:transition-[width] md:duration-300 md:ease-[cubic-bezier(0.4,0,0.2,1)] w-full md:mt-12 md:m-2 md:w-[384px] p-5 border-0.5 border-border-300 md:rounded-2xl max-md:border-0 md:absolute" aria-hidden="false"><div class="md:w-[342px]"><div class="flex flex-col gap-5 md:transition-opacity md:duration-300 md:animate-[fade_0.3s_ease-in-out_0.1s_forwards]"><div class="flex flex-col gap-3"><div class="flex items-center justify-between"><h3 class="font-medium text-sm">Content</h3></div><div class="flex flex-col gap-2"><div class="grid grid-cols-[repeat(auto-fill,minmax(120px,1fr))] gap-3"><div><div class="relative"><div class="group/thumbnail" data-testid="file-thumbnail"><button class="rounded-lg text-left cursor-pointer font-ui transition-all rounded-lg border-0.5 border-[hsl(var(--border-300)/0.25)] flex flex-col justify-between gap-2.5 overflow-hidden px-2.5 py-2 bg-bg-000 hover:border-[hsl(var(--border-200)/0.5)] hover:shadow-always-black/10 shadow-sm shadow-always-black/5" style="width: 100%; height: 120px; min-width: 100%;"><div class="flex flex-col gap-1 min-h-0"><h3 id="_r_8h_" class="text-[12px] break-words text-text-100 line-clamp-4" style="opacity: 1;">streamlit_app (9).py</h3></div><div class=""><div class="relative flex flex-row items-center gap-1 justify-between"><div class="flex flex-row gap-1 shrink min-w-0" style="opacity: 1;"><div data-state="closed" class="min-w-0 h-[18px] flex flex-row items-center justify-center gap-0.5 px-1 border-0.5 border-[hsl(var(--border-300)/0.25)] shadow-sm rounded-[4px] bg-bg-000/70 backdrop-blur-sm font-medium"><p class="uppercase truncate font-ui text-text-300 text-[11px] leading-[13px]">py</p></div></div></div></div></button></div></div></div><div><div class="relative"><div class="group/thumbnail" data-testid="file-thumbnail"><button class="rounded-lg text-left cursor-pointer font-ui transition-all rounded-lg border-0.5 border-[hsl(var(--border-300)/0.25)] flex flex-col justify-between gap-2.5 overflow-hidden px-2.5 py-2 bg-bg-000 hover:border-[hsl(var(--border-200)/0.5)] hover:shadow-always-black/10 shadow-sm shadow-always-black/5" aria-label="Pasted Text, pasted, 334 lines" style="width: 100%; height: 120px; min-width: 100%;"><div class="flex flex-col gap-1 min-h-0"><div class="flex-1 min-h-0 flex flex-row gap-2"><p class=" flex-1 min-w-0 overflow-hidden text-[8px] text-text-500/80 break-all line-clamp-[6]" style="opacity: 1;">
