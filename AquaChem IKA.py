import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AquaChem IKA",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed", # REVISI 1: Diubah dari expanded menjadi collapsed agar sidebar tidak terbuka otomatis
)

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght=400;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* REVISI 2: Modifikasi Root Variables warna kontras tinggi agar terlihat sangat jelas di Mode Terang (Light Mode) */
:root {
    --teal:   #0D9488;
    --blue:   #1A6EFC;
    --indigo: #2D3A8C;
    --dark:   #FFFFFF;          /* Background halaman menjadi putih agar tulisan terlihat jelas */
    --card:   #F8FAFC;          /* Warna background card dibuat abu-abu sangat terang agar kontras */
    --border: #CBD5E1;          /* Border dipertegas */
    --text:   #0F172A;          /* Warna tulisan utama diganti ke hitam/gelap pekat agar terbaca jelas */
    --muted:  #475569;          /* Teks sekunder/keterangan dipergelap agar tidak samar-samar */
    --good:   #16A34A;
    --warn:   #D97706;
    --bad:    #DC2626;
}

/* Otomatis mendeteksi dan menyesuaikan warna jika pengguna menggunakan tema gelap bawaan Streamlit */
@media (prefers-color-scheme: dark) {
    :root {
        --dark:   #0D1117;
        --card:   #161B25;
        --border: #242C3D;
        --text:   #E8EDF5;
        --muted:  #7A8BA6;
        --teal:   #0EB8A4;
    }
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: var(--dark);
    color: var(--text);
}

/* Memastikan elemen-elemen teks standar streamlit mewarisi warna kontras utama */
.stMarkdown p, .stMarkdown li, span, label, div[data-testid="stExpander"] summary p {
    color: var(--text) !important;
}

/* Hide default streamlit branding */
#MainMenu, footer, header {visibility: hidden;}

/* Hero Banner */
.hero {
    background: linear-gradient(135deg, #0D1117 0%, #0a2a40 50%, #0D1117 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 40px 36px 32px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(14,184,164,0.18) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: "";
    position: absolute;
    bottom: -80px; left: 10%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(26,110,252,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(90deg, #0EB8A4, #1A6EFC);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 8px 0;
    line-height: 1.2;
}
.hero-sub {
    color: #94A3B8 !important; /* Diperjelas khusus di dalam banner gelap */
    font-size: 1rem;
    margin: 0;
    font-weight: 400;
}
.hero-badge {
    display: inline-block;
    background: rgba(14,184,164,0.12);
    border: 1px solid rgba(14,184,164,0.4);
    color: #0EB8A4 !important;
    border-radius: 20px;
    padding: 3px 14px;
    font-size: 0.72rem;
    font-family: 'Space Mono', monospace;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

/* Cards */
.param-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 24px 22px;
    height: 100%;
    transition: border-color 0.2s;
}
.param-card:hover { border-color: var(--teal); }
.param-title {
    font-family: 'Space Mono', monospace;
    font-size: 1rem;
    color: var(--teal);
    margin-bottom: 6px;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.param-fullname {
    color: var(--muted);
    font-size: 0.8rem;
    margin-bottom: 16px;
}
.param-value {
    font-size: 2.4rem;
    font-weight: 800;
    color: var(--text);
    line-height: 1;
    margin-bottom: 4px;
}
.param-unit {
    font-size: 0.8rem;
    color: var(--muted);
    margin-bottom: 14px;
}
.status-chip {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.status-good   { background: #DCFCE7; color: #15803D !important; border: 1px solid #BBF7D0; }
.status-warn   { background: #FEF3C7; color: #B45309 !important; border: 1px solid #FDE68A; }
.status-bad    { background: #FEE2E2; color: #B91C1C !important; border: 1px solid #FCA5A5; }

/* Reference Table */
.ref-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
}
.ref-table th {
    background: rgba(14,184,164,0.15);
    color: var(--teal);
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    padding: 10px 14px;
    text-align: left;
    border-bottom: 1px solid var(--border);
}
.ref-table td {
    padding: 10px 14px;
    border-bottom: 1px solid var(--border);
    color: var(--text);
}
.ref-table tr:last-child td { border-bottom: none; }
.ref-table tr:hover td { background: rgba(0,0,0,0.02); }

/* Section Header */
.sec-head {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 2px;
    color: var(--teal);
    text-transform: uppercase;
    margin: 32px 0 16px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.sec-head::after {
    content: "";
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* IKA Score */
.ika-ring {
    text-align: center;
    padding: 16px 0;
}
.ika-score {
    font-family: 'Space Mono', monospace;
    font-size: 3.8rem;
    font-weight: 700;
    line-height: 1;
}
.ika-label {
    font-size: 0.85rem;
    color: var(--muted);
    margin-top: 6px;
}
.ika-cat {
    font-size: 1.1rem;
    font-weight: 700;
    margin-top: 8px;
}

/* Info box */
.info-box {
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-left: 4px solid #16A34A;
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 0.88rem;
    color: #166534 !important;
    margin: 10px 0;
    line-height: 1.6;
}
.warn-box {
    background: #FFFBEB;
    border: 1px solid #FDE68A;
    border-left: 4px solid #D97706;
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 0.88rem;
    color: #92400E !important;
    margin: 10px 0;
    line-height: 1.6;
}
.bad-box {
    background: #FEF2F2;
    border: 1px solid #FCA5A5;
    border-left: 4px solid #DC2626;
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 0.88rem;
    color: #991B1B !important;
    margin: 10px 0;
    line-height: 1.6;
}

/* Divider */
.divider { border: none; border-top: 1px solid var(--border); margin: 24px 0; }

/* About section */
.about-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 28px 26px;
    margin-bottom: 18px;
}
.about-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 2px;
    color: var(--teal);
    text-transform: uppercase;
    margin-bottom: 8px;
}
.about-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 10px;
}
.about-body {
    color: var(--muted);
    font-size: 0.9rem;
    line-height: 1.7;
}

/* Metric strip */
.metric-strip {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 20px;
}
.metric-item {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 20px;
    flex: 1;
    min-width: 120px;
}
.metric-num {
    font-family: 'Space Mono', monospace;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--teal);
}
.metric-desc {
    font-size: 0.78rem;
    color: var(--muted);
    margin-top: 2px;
}

/* Streamlit overrides */
.stSlider > label { color: var(--text) !important; font-size: 0.85rem !important; }
.stButton > button {
    background: linear-gradient(135deg, var(--teal), var(--blue));
    color: white !important;
    border: none;
    border-radius: 8px;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 1px;
    padding: 10px 24px;
    transition: opacity 0.2s;
    width: 100%;
}
.stButton > button:hover { opacity: 0.85; }
div[data-testid="stExpander"] {
    background: var(--card);
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}
div[data-testid="stExpander"] summary { color: var(--text) !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--card);
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border-radius: 7px !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(14,184,164,0.25), rgba(26,110,252,0.25)) !important;
    color: var(--text) !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE — default settings
# ─────────────────────────────────────────────
if "app_name" not in st.session_state:
    st.session_state.app_name = "AquaChem IKA"
if "group_name" not in st.session_state:
    st.session_state.group_name = "Anggota Kelompok 4"
if "group_desc" not in st.session_state:
    st.session_state.group_desc = (
        "Aqiila Rahmania Mumtaza (2560577)\n"
        "Gevan Eirano Yusuf (2560635)\n"
        "Magali Wahyudi (2560663)\n"
        "Naufa Afifah (2560715)\n"
        "Siti Halimah Tusysyadiyah Tsany (2560785)"
    )
if "web_desc" not in st.session_state:
    st.session_state.web_desc = (
        "Aplikasi ini dikembangkan untuk membantu analisis kualitas air "
        "berdasarkan parameter kimia utama yaitu pH, BOD, dan COD. "
        "Gunakan panel input data di bawah banner halaman utama untuk memasukkan data pengukuran."
    )
if "main_input_mode" not in st.session_state:
    st.session_state.main_input_mode = "📊 Langsung (Nilai)"

# ─────────────────────────────────────────────
#  REFERENCE DATA (REVISI 4: pH disesuaikan dengan PP No. 22/2021 Lampiran VI untuk Kelas 2 yaitu 6.0 – 9.0)
# ─────────────────────────────────────────────
PH_REF = [
    {"Kategori": "Sangat Asam / Sangat Basa (Berbahaya)", "Rentang": "< 5.0 atau > 9.5", "Status": "💀 Tercemar Berat", "Kelas": "bad"},
    {"Kategori": "Asam / Basa Ringan", "Rentang": "5.0 – 6.0 atau 9.0 – 9.5", "Status": "⚠️ Tercemar Sedang", "Kelas": "warn"},
    {"Kategori": "Normal / Memenuhi Baku Mutu Kelas II", "Rentang": "6.0 – 9.0", "Status": "✅ Memenuhi Baku Mutu", "Kelas": "good"},
]
BOD_REF = [
    {"Kategori": "Sangat Baik (Air Bersih)", "Rentang": "< 2 mg/L", "Status": "✅ Tidak Tercemar", "Kelas": "good"},
    {"Kategori": "Baik (Air Bersih)", "Rentang": "2 – 3 mg/L", "Status": "✅ Memenuhi Baku Mutu", "Kelas": "good"},
    {"Kategori": "Tercemar Sedang", "Rentang": "3 – 6 mg/L", "Status": "⚠️ Tercemar Sedang", "Kelas": "warn"},
    {"Kategori": "Tercemar Berat", "Rentang": "6 – 12 mg/L", "Status": "🔴 Tercemar Berat", "Kelas": "bad"},
    {"Kategori": "Sangat Tercemar Berat", "Rentang": "> 12 mg/L", "Status": "💀 Sangat Tercemar", "Kelas": "bad"},
]
COD_REF = [
    {"Kategori": "Sangat Baik", "Rentang": "< 10 mg/L", "Status": "✅ Tidak Tercemar", "Kelas": "good"},
    {"Kategori": "Baik (Baku Mutu Kelas I/II)", "Rentang": "10 – 25 mg/L", "Status": "✅ Memenuhi Baku Mutu", "Kelas": "good"},
    {"Kategori": "Tercemar Ringan–Sedang", "Rentang": "25 – 50 mg/L", "Status": "⚠️ Tercemar Sedang", "Kelas": "warn"},
    {"Kategori": "Tercemar Berat", "Rentang": "50 – 100 mg/L", "Status": "🔴 Tercemar Berat", "Kelas": "bad"},
    {"Kategori": "Sangat Tercemar Berat", "Rentang": "> 100 mg/L", "Status": "💀 Sangat Tercemar", "Kelas": "bad"},
]

# ─────────────────────────────────────────────
#  HELPER FUNCTIONS (REVISI 4: Evaluasi pH disesuaikan ke standar baku mutu Kelas 2: 6.0 s.d 9.0)
# ─────────────────────────────────────────────
def get_ph_status(v):
    if 6.0 <= v <= 9.0:
        return "Memenuhi Baku Mutu", "good", 100
    elif (5.0 <= v < 6.0) or (9.0 < v <= 9.5):
        return "Tercemar Sedang", "warn", 50
    else:
        return "Tercemar Berat", "bad", 10

def get_bod_status(v):
    if v < 2:
        return "Tidak Tercemar", "good", 100
    elif v <= 3:
        return "Memenuhi Baku Mutu", "good", 85
    elif v <= 6:
        return "Tercemar Sedang", "warn", 50
    elif v <= 12:
        return "Tercemar Berat", "bad", 25
    else:
        return "Sangat Tercemar Berat", "bad", 5

def get_cod_status(v):
    if v < 10:
        return "Tidak Tercemar", "good", 100
    elif v <= 25:
        return "Memenuhi Baku Mutu", "good", 80
    elif v <= 50:
        return "Tercemar Sedang", "warn", 45
    elif v <= 100:
        return "Tercemar Berat", "bad", 20
    else:
        return "Sangat Tercemar Berat", "bad", 5

def calc_ika(ph_val, bod_val, cod_val):
    """
    Indeks Kualitas Air sederhana berdasarkan sub-indeks tiap parameter.
    Bobot: pH=30%, BOD=35%, COD=35%
    """
    _, _, ph_score  = get_ph_status(ph_val)
    _, _, bod_score = get_bod_status(bod_val)
    _, _, cod_score = get_cod_status(cod_val)
    ika = 0.30 * ph_score + 0.35 * bod_score + 0.35 * cod_score
    return round(ika, 1), ph_score, bod_score, cod_score

def ika_category(score):
    if score >= 80:
        return "Baik 🟢", "#22C55E"
    elif score >= 50:
        return "Tercemar Ringan–Sedang 🟡", "#F59E0B"
    elif score >= 25:
        return "Tercemar Berat 🔴", "#EF4444"
    else:
        return "Sangat Tercemar Berat ☠️", "#EF4444"

def status_chip(label, cls):
    return f'<span class="status-chip status-{cls}">{label}</span>'

def render_ref_table(data):
    rows = ""
    for r in data:
        cls  = r["Kelas"]
        chip = status_chip(r["Status"], cls)
        rows += f"<tr><td>{r['Kategori']}</td><td>{r['Rentang']}</td><td>{chip}</td></tr>"
    html = f"""
    <table class="ref-table">
    <thead><tr><th>Kategori</th><th>Rentang</th><th>Status</th></tr></thead>
    <tbody>{rows}</tbody>
    </table>"""
    st.markdown(html, unsafe_allow_html=True)

# REVISI 1: Porsi Sidebar lama dipindahkan ke dalam container fungsi tab atau di bawah agar halaman bersih dari sidebar.
# Seluruh markup sidebar asli 'with st.sidebar:' telah dihilangkan total dari script ini.

# ─────────────────────────────────────────────
#  MAIN — HERO (REVISI 3: Menambahkan badge informasi Baku Mutu Air Kelas 2 PP No. 22/2021)
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-badge">BAKU MUTU AIR KELAS II — PP NO. 22 TAHUN 2021</div>
    <h1 class="hero-title">{st.session_state.app_name}</h1>
    <p class="hero-sub">{st.session_state.web_desc}</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FITUR TOMBOL & PANEL INPUT DI HALAMAN UTAMA
# ─────────────────────────────────────────────
st.markdown('<div class="sec-head">🎛️ Panel Kontrol Mode Input Data</div>', unsafe_allow_html=True)

btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    if st.button("📊 MODE 1: Input Nilai Langsung (PH/BOD/COD Sudah Diketahui)"):
        st.session_state.main_input_mode = "📊 Langsung (Nilai)"
with btn_col2:
    if st.button("🧪 MODE 2: Hitung dari Titrasi (Laboratorium)"):
        st.session_state.main_input_mode = "🧪 Dari Titrasi"

st.markdown(f"""
<div style="font-size:0.9rem; margin-bottom:20px; color:var(--text);">
    Mode aktif saat ini: <span style="color:var(--teal); font-weight:bold; font-family:'Space Mono', monospace;">{st.session_state.main_input_mode}</span>
</div>
""", unsafe_allow_html=True)

ph_val = 7.0
bod_val = 2.0
cod_val = 15.0

with st.container():
    st.markdown('<div style="background:var(--card); border:1px solid var(--border); border-radius:14px; padding:24px; margin-bottom:25px;">', unsafe_allow_html=True)
    # Input umum pH (REVISI 4: Keterangan helper disesuaikan ke standar 6.0 – 9.0)
    ph_val = st.number_input("Masukkan Nilai pH", min_value=0.0, max_value=14.0, value=7.0, step=0.1, help="Skala 0–14. Baku mutu kelas 2: 6.0–9.0", key="main_ph_input")
    
    if st.session_state.main_input_mode == "📊 Langsung (Nilai)":
        st.markdown("<p style='color:var(--teal); font-weight:600; margin-top:10px;'>Masukkan Nilai Parameter Langsung:</p>", unsafe_allow_html=True)
        col_direct1, col_direct2 = st.columns(2)
        with col_direct1:
            bod_val = st.number_input("BOD (mg/L)", min_value=0.0, max_value=200.0, value=2.0, step=0.1, help="Biochemical Oxygen Demand. Baku mutu Kelas 2: ≤ 3 mg/L", key="main_bod_direct")
        with col_direct2:
            cod_val = st.number_input("COD (mg/L)", min_value=0.0, max_value=500.0, value=15.0, step=0.1, help="Chemical Oxygen Demand. Baku mutu Kelas 2: ≤ 25 mg/L", key="main_cod_direct")
            
    elif st.session_state.main_input_mode == "🧪 Dari Titrasi":
        st.markdown("""<div style="font-size:0.9rem; color:#0EB8A4; font-family:'Space Mono',monospace; margin:15px 0 6px 0; font-weight:bold;">🔬 Perhitungan Parameter BOD — Titrasi Winkler</div>""", unsafe_allow_html=True)
        st.markdown("""<div style="font-size:0.75rem; color:var(--muted); margin-bottom:8px;"> Rumus: BOD = (V_titran_blanko − V_titran_sampel) × N_Na₂S₂O₃ × 8000 / V_sampel </div>""", unsafe_allow_html=True)
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            bod_v_blanko = st.number_input("V Titran Blanko (mL)", min_value=0.0, value=10.0, step=0.01, key="main_bod_vb")
            bod_v_sampel_t = st.number_input("V Titran Sampel (mL)", min_value=0.0, value=8.5, step=0.01, key="main_bod_vs")
        with col_b2:
            bod_n = st.number_input("N Na₂S₂O₃", min_value=0.0, value=0.025, step=0.001, format="%.4f", key="main_bod_n")
            bod_v_sampel = st.number_input("V Sampel (mL)", min_value=0.1, value=100.0, step=1.0, key="main_bod_ml")
        
        if bod_v_sampel > 0:
            bod_val = round((bod_v_blanko - bod_v_sampel_t) * bod_n * 8000 / bod_v_sampel, 3)
        else:
            bod_val = 0.0
        st.markdown(f"""<div style="background:rgba(14,184,164,0.08); border:1px solid rgba(14,184,164,0.3); border-radius:8px; padding:10px 14px; font-size:0.85rem; margin:6px 0 20px 0; color:var(--text);"> Hasil Perhitungan Terhitung BOD: <b style="color:#0EB8A4; font-family:'Space Mono',monospace;"> {bod_val} mg/L</b></div>""", unsafe_allow_html=True)

        st.markdown("""<div style="font-size:0.9rem; color:#8B5CF6; font-family:'Space Mono',monospace; margin:15px 0 6px 0; font-weight:bold;">🔬 Perhitungan Parameter COD — Titrasi Dikromat / Permanganometri</div>""", unsafe_allow_html=True)
        st.markdown("""<div style="font-size:0.75rem; color:var(--muted); margin-bottom:8px;"> Rumus: COD = (V_blanko − V_sampel) × N_titran × 8000 / V_sampel </div>""", unsafe_allow_html=True)
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            cod_v_blanko = st.number_input("V Titran Blanko (mL)", min_value=0.0, value=15.0, step=0.01, key="main_cod_vb")
            cod_v_sampel_t = st.number_input("V Titran Sampel (mL)", min_value=0.0, value=12.0, step=0.01, key="main_cod_vs")
        with col_c2:
            cod_n = st.number_input("N Titran (FAS/KMnO₄)", min_value=0.0, value=0.1, step=0.001, format="%.4f", key="main_cod_n")
            cod_v_sampel = st.number_input("V Sampel (mL)", min_value=0.1, value=20.0, step=1.0, key="main_cod_ml")
        
        if cod_v_sampel > 0:
            cod_val = round((cod_v_blanko - cod_v_sampel_t) * cod_n * 8000 / cod_v_sampel, 3)
        else:
            cod_val = 0.0
        st.markdown(f"""<div style="background:rgba(139,92,246,0.08); border:1px solid rgba(139,92,246,0.3); border-radius:8px; padding:10px 14px; font-size:0.85rem; margin:6px 0 4px 0; color:var(--text);"> Hasil Perhitungan Terhitung COD: <b style="color:#8B5CF6; font-family:'Space Mono',monospace;"> {cod_val} mg/L</b></div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CALCULATE (LOGIKA EVALUASI UTAMA)
# ─────────────────────────────────────────────
ika_score, ph_si, bod_si, cod_si = calc_ika(ph_val, bod_val, cod_val)
ika_cat, ika_color = ika_category(ika_score)

ph_label, ph_cls, _ = get_ph_status(ph_val)
bod_label, bod_cls, _ = get_bod_status(bod_val)
cod_label, cod_cls, _ = get_cod_status(cod_val)

# ─────────────────────────────────────────────
#  TABS (REVISI 1: Menambahkan Tab ke-5 sebagai wadah "Pengaturan Aplikasi" pindahan dari Sidebar)
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Analisis Parameter", 
    "📖 Referensi Standar", 
    "📈 Visualisasi", 
    "ℹ️ Tentang",
    "⚙️ Pengaturan Aplikasi"
])

# ══════════════════════════════════════════════
#  TAB 1 — ANALISIS
# ══════════════════════════════════════════════
with tab1:
    st.markdown('<div class="sec-head">Indeks Kualitas Air (IKA)</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1])
    
    with c1:
        st.markdown(f"""
        <div class="param-card" style="border-color:{ika_color}40;">
            <div class="ika-ring">
                <div class="ika-score" style="color:{ika_color};">{ika_score}</div>
                <div class="ika-label">Skor IKA (0–100)</div>
                <div class="ika-cat" style="color:{ika_color};">{ika_cat}</div>
            </div>
        </div>""", unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
        <div class="param-card">
            <div class="param-title">pH</div>
            <div class="param-fullname">Derajat Keasaman</div>
            <div class="param-value">{ph_val}</div>
            <div class="param-unit">skala</div>
            {status_chip(ph_label, ph_cls)}
        </div>""", unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""
        <div class="param-card">
            <div class="param-title">BOD</div>
            <div class="param-fullname">Biochemical Oxygen Demand</div>
            <div class="param-value">{bod_val}</div>
            <div class="param-unit">mg/L</div>
            {status_chip(bod_label, bod_cls)}
        </div>""", unsafe_allow_html=True)
        
    with c4:
        st.markdown(f"""
        <div class="param-card">
            <div class="param-title">COD</div>
            <div class="param-fullname">Chemical Oxygen Demand</div>
            <div class="param-value">{cod_val}</div>
            <div class="param-unit">mg/L</div>
            {status_chip(cod_label, cod_cls)}
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Detail Parameter</div>', unsafe_allow_html=True)
    
    # pH (REVISI 4: Narasi teks disesuaikan ke rentang baku mutu kelas 2 baru: 6.0 – 9.0)
    with st.expander("🔵 pH — Derajat Keasaman Air", expanded=True):
        col_a, col_b = st.columns([1, 1.4])
        with col_a:
            st.markdown("""
            *Apa itu pH?*
            pH mengukur konsentrasi ion hidrogen dalam air dan menunjukkan seberapa asam atau basa suatu larutan. Skala pH berkisar 0–14, di mana 7 bersifat netral.
            
            *Mengapa penting?*
            pH mempengaruhi reaksi kimia dalam air, kelarutan logam berat, dan kemampuan organisme akuatik untuk bertahan hidup. Nilai di luar rentang standar menunjukkan adanya pencemaran atau gangguan keseimbangan ekosistem perairan.
            """)
        with col_b:
            if ph_cls == "good":
                st.markdown(f'<div class="info-box">✅ <strong>pH {ph_val}</strong> — Nilai ini memenuhi baku mutu air kelas II (6.0–9.0). Air dalam kondisi normal dan aman untuk berbagai pemanfaatan sesuai peruntukannya.</div>', unsafe_allow_html=True)
            elif ph_cls == "warn":
                st.markdown(f'<div class="warn-box">⚠️ <strong>pH {ph_val}</strong> — Nilai ini berada di luar baku mutu optimal kelas II. Air menunjukkan tanda-tanda asam/basa ringan. Perlu monitoring lebih lanjut.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bad-box">🚨 <strong>pH {ph_val}</strong> — Nilai ekstrem! Air terindikasi sangat asam atau basa. Berbahaya bagi biota air dan tidak layak untuk penggunaan langsung.</div>', unsafe_allow_html=True)

    # BOD
    with st.expander("🟢 BOD — Biochemical Oxygen Demand", expanded=True):
        col_a, col_b = st.columns([1, 1.4])
        with col_a:
            st.markdown("""
            *Apa itu BOD?*
            BOD adalah jumlah oksigen yang dibutuhkan oleh mikroorganisme untuk mengurai bahan organik dalam air secara biologis pada kondisi tertentu (biasanya 5 hari, 20°C).
            
            *Mengapa penting?*
            BOD tinggi menandakan banyak bahan organik terlarut, yang menyebabkan deplesi oksigen terlarut (DO), membunuh ikan dan biota akuatik, serta menandakan pencemaran dari limbah domestik/industri.
            """)
        with col_b:
            if bod_cls == "good":
                st.markdown(f'<div class="info-box">✅ <strong>BOD {bod_val} mg/L</strong> — Memenuhi baku mutu. Kandungan bahan organik rendah, oksigen terlarut cukup untuk mendukung ekosistem perairan.</div>', unsafe_allow_html=True)
            elif bod_cls == "warn":
                st.markdown(f'<div class="warn-box">⚠️ <strong>BOD {bod_val} mg/L</strong> — Melewati baku mutu (3 mg/L). Air terindikasi tercemar bahan organik. Dapat mengganggu kehidupan biota air.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bad-box">🚨 <strong>BOD {bod_val} mg/L</strong> — Jauh melampaui baku mutu! Pencemaran organik berat. Air tidak layak pakai tanpa pengolahan intensif.</div>', unsafe_allow_html=True)

    # COD
    with st.expander("🔴 COD — Chemical Oxygen Demand", expanded=True):
        col_a, col_b = st.columns([1, 1.4])
        with col_a:
            st.markdown("""
            *Apa itu COD?*
            COD mengukur total oksigen yang dibutuhkan untuk mengoksidasi seluruh bahan organik (termasuk yang tidak bisa diurai secara biologis) menggunakan oksidator kimia kuat.
            
            *Mengapa penting?*
            COD selalu lebih tinggi dari BOD. Rasio COD/BOD yang besar menandakan adanya senyawa organik sulit terurai (rekalcitran) seperti pestisida, deterjen, atau limbah industri kimia.
            """)
        with col_b:
            if cod_cls == "good":
                st.markdown(f'<div class="info-box">✅ <strong>COD {cod_val} mg/L</strong> — Memenuhi baku mutu. Beban pencemar organik dan kimia masih dalam batas aman.</div>', unsafe_allow_html=True)
            elif cod_cls == "warn":
                st.markdown(f'<div class="warn-box">⚠️ <strong>COD {cod_val} mg/L</strong> — Melampaui baku mutu. Indikasi pencemaran bahan kimia organik. Perlu investigasi sumber pencemar.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bad-box">🚨 <strong>COD {cod_val} mg/L</strong> — Sangat tinggi! Indikasi pencemaran kimia berat. Air memerlukan pengolahan khusus sebelum digunakan.</div>', unsafe_allow_html=True)

    # Rasio BOD/COD
    st.markdown('<div class="sec-head">Analisis Lanjutan</div>', unsafe_allow_html=True)
    if cod_val > 0:
        ratio = round(bod_val / cod_val, 3)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="param-card">
                <div class="param-title">Rasio BOD/COD</div>
                <div class="param-fullname">Biodegradabilitas Limbah</div>
                <div class="param-value">{ratio}</div>
                <div style="margin-top:10px; font-size:0.83rem; color:var(--muted); line-height:1.6;">
                {'✅ <b style="color:#16A34A">Mudah terurai secara biologis</b> — Rasio > 0.5 menandakan limbah organik yang dapat diolah dengan proses biologis (IPAL).' if ratio >= 0.5 else ('⚠️ <b style="color:#D97706">Cukup dapat terurai</b> — Perlu kombinasi pengolahan biologis dan kimia.' if ratio >= 0.3 else '🔴 <b style="color:#DC2626">Sulit terurai secara biologis</b> — Rasio < 0.3 mengindikasikan bahan kimia organik rekalcitran. Perlu pengolahan kimia-fisika.')}
                </div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="param-card">
                <div class="param-title">Sub-Indeks Tiap Parameter</div>
                <div class="param-fullname">Kontribusi terhadap IKA</div>
                <div style="margin-top:14px;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                        <span style="color:var(--muted); font-size:0.83rem;">pH (bobot 30%)</span>
                        <span style="font-family:'Space Mono',monospace; color:var(--teal);">{ph_si} / 100</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                        <span style="color:var(--muted); font-size:0.83rem;">BOD (bobot 35%)</span>
                        <span style="font-family:'Space Mono',monospace; color:var(--teal);">{bod_si} / 100</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                        <span style="color:var(--muted); font-size:0.83rem;">COD (bobot 35%)</span>
                        <span style="font-family:'Space Mono',monospace; color:var(--teal);">{cod_si} / 100</span>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  TAB 2 — REFERENSI
# ══════════════════════════════════════════════
with tab2:
    st.markdown("### Tabel Acuan Baku Mutu Air Kelas II (PP No. 22/2021)")
    st.markdown("**1. Parameter pH**")
    render_ref_table(PH_REF)
    st.markdown("**2. Parameter BOD**")
    render_ref_table(BOD_REF)
    st.markdown("**3. Parameter COD**")
    render_ref_table(COD_REF)

# ══════════════════════════════════════════════
#  TAB 3 — VISUALISASI
# ══════════════════════════════════════════════
with tab3:
    st.markdown("### Grafik Perbandingan Parameter Terhadap Nilai Baku Mutu")
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Nilai Pengukuran', x=['pH', 'BOD', 'COD'], y=[ph_val, bod_val, cod_val], marker_color='#1A6EFC'))
    fig.add_trace(go.Scatter(name='Batas Maks Baku Mutu Kelas II', x=['pH', 'BOD', 'COD'], y=[9.0, 3.0, 25.0], mode='lines+markers', marker=dict(color='red', size=10)))
    fig.update_layout(title="Visualisasi Parameter vs Batas Baku Mutu", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════
#  TAB 4 — TENTANG
# ══════════════════════════════════════════════
with tab4:
    st.markdown(f"### {st.session_state.group_name}")
    st.text(st.session_state.group_desc)
    
    st.markdown("""
    <div class="about-card" style="border-color:rgba(14,184,164,0.3); margin-top:15px;">
      <div class="about-label">Metodologi IKA</div>
      <div class="about-title">📐 Cara Perhitungan Indeks</div>
      <div class="about-body">
        Indeks Kualitas Air (IKA) dihitung menggunakan sistem sub-indeks berbobot:
        <br><br>
        <code style="background:#0D1117; padding:10px 16px; border-radius:6px;
                     border:1px solid #242C3D; display:block; margin:8px 0;
                     font-family:'Space Mono',monospace; color:#0EB8A4; font-size:0.85rem;">
          IKA = (0.30 × SI_pH) + (0.35 × SI_BOD) + (0.35 × SI_COD)
        </code>
        Di mana SI (Sub-Indeks) bernilai 0–100 berdasarkan posisi nilai terhadap baku mutu.
        Bobot lebih besar pada BOD dan COD karena keduanya langsung mencerminkan
        beban pencemaran organik yang paling umum di perairan Indonesia.
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  TAB 5 — PENGATURAN APLIKASI (REVISI 1: Pindahan dari Sidebar)
# ══════════════════════════════════════════════
with tab5:
    st.markdown("### ⚙️ Pengaturan Manajemen Informasi Web")
    new_app = st.text_input("Nama Aplikasi", value=st.session_state.app_name)
    new_grp = st.text_input("Nama Kelompok", value=st.session_state.group_name)
    new_gdesc = st.text_area("Deskripsi Kelompok", value=st.session_state.group_desc, height=100)
    new_wdesc = st.text_area("Deskripsi Website", value=st.session_state.web_desc, height=100)
    if st.button("💾 SIMPAN PENGATURAN"):
        st.session_state.app_name  = new_app
        st.session_state.group_name  = new_grp
        st.session_state.group_desc  = new_gdesc
        st.session_state.web_desc    = new_wdesc
        st.success("Pengaturan tersimpan!")

    st.markdown("""
    <div style="margin-top:24px; padding:12px; background:var(--card); border-radius:8px; border:1px solid var(--border); font-size:0.75rem; color:var(--text);">
        📋 Referensi: PP No. 22/2021 & PermenLHK<br>
        Baku mutu air kelas II
    </div>
    """, unsafe_allow_html=True)
