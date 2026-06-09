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
    initial_sidebar_state="collapsed", # Mengubah default sidebar menjadi tertutup total
)

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* Root Variables */
:root {
    --teal:   #0EB8A4;
    --blue:   #1A6EFC;
    --indigo: #2D3A8C;
    --dark:   #0D1117;
    --card:   #161B25;
    --border: #242C3D;
    --text:   #E8EDF5;
    --muted:  #7A8BA6;
    --good:   #22C55E;
    --warn:   #F59E0B;
    --bad:    #EF4444;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: var(--dark);
    color: var(--text);
}

/* Hide default streamlit branding & sidebar button completely */
#MainMenu, footer, header {visibility: hidden;}
[data-testid="collapsedControl"] {display: none;} /* Menyembunyikan tombol pembuka sidebar */

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
    color: var(--muted);
    font-size: 1rem;
    margin: 0;
    font-weight: 400;
}
.hero-badge {
    display: inline-block;
    background: rgba(14,184,164,0.12);
    border: 1px solid rgba(14,184,164,0.4);
    color: var(--teal);
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
.status-good   { background: rgba(34,197,94,0.15);  color: #22C55E; border: 1px solid rgba(34,197,94,0.35); }
.status-warn   { background: rgba(245,158,11,0.15); color: #F59E0B; border: 1px solid rgba(245,158,11,0.35); }
.status-bad    { background: rgba(239,68,68,0.15);  color: #EF4444; border: 1px solid rgba(239,68,68,0.35); }

/* Reference Table */
.ref-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
}
.ref-table th {
    background: rgba(14,184,164,0.1);
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
.ref-table tr:hover td { background: rgba(255,255,255,0.02); }

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
    background: rgba(14,184,164,0.06);
    border: 1px solid rgba(14,184,164,0.25);
    border-left: 4px solid var(--teal);
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 0.88rem;
    color: var(--text);
    margin: 10px 0;
    line-height: 1.6;
}
.warn-box {
    background: rgba(245,158,11,0.06);
    border: 1px solid rgba(245,158,11,0.25);
    border-left: 4px solid #F59E0B;
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 0.88rem;
    color: var(--text);
    margin: 10px 0;
    line-height: 1.6;
}
.bad-box {
    background: rgba(239,68,68,0.06);
    border: 1px solid rgba(239,68,68,0.25);
    border-left: 4px solid #EF4444;
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 0.88rem;
    color: var(--text);
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
.stSlider > label { color: var(--muted) !important; font-size: 0.85rem !important; }
.stButton > button {
    background: linear-gradient(135deg, var(--teal), var(--blue));
    color: white;
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
# Tambahan session state pelacak mode input aktif halaman utama
if "main_input_mode" not in st.session_state:
    st.session_state.main_input_mode = "📊 Langsung (Nilai)"

# ─────────────────────────────────────────────
#  REFERENCE DATA
# ─────────────────────────────────────────────
PH_REF = [
    {"Kategori": "Sangat Asam / Sangat Basa (Berbahaya)", "Rentang": "< 5.0 atau > 9.0", "Status": "💀 Tercemar Berat", "Kelas": "bad"},
    {"Kategori": "Asam / Basa Ringan (Tercemar Sedang)", "Rentang": "5.0 – 6.0 atau 8.5 – 9.0", "Status": "⚠️ Tercemar Sedang", "Kelas": "warn"},
    {"Kategori": "Mendekati Normal", "Rentang": "6.0 – 6.5 atau 8.0 – 8.5", "Status": "🟡 Tercemar Ringan", "Kelas": "warn"},
    {"Kategori": "Normal / Baku Mutu", "Rentang": "6.5 – 8.0", "Status": "✅ Memenuhi Baku Mutu", "Kelas": "good"},
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
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────
def get_ph_status(v):
    if 6.5 <= v <= 8.0: return "Memenuhi Baku Mutu", "good", 100
    elif (6.0 <= v < 6.5) or (8.0 < v <= 8.5): return "Tercemar Ringan", "warn", 60
    elif (5.0 <= v < 6.0) or (8.5 < v <= 9.0): return "Tercemar Sedang", "warn", 35
    else: return "Tercemar Berat", "bad", 10

def get_bod_status(v):
    if v < 2: return "Tidak Tercemar", "good", 100
    elif v <= 3: return "Memenuhi Baku Mutu", "good", 85
    elif v <= 6: return "Tercemar Sedang", "warn", 50
    elif v <= 12: return "Tercemar Berat", "bad", 25
    else: return "Sangat Tercemar Berat", "bad", 5

def get_cod_status(v):
    if v < 10: return "Tidak Tercemar", "good", 100
    elif v <= 25: return "Memenuhi Baku Mutu", "good", 80
    elif v <= 50: return "Tercemar Sedang", "warn", 45
    elif v <= 100: return "Tercemar Berat", "bad", 20
    else: return "Sangat Tercemar Berat", "bad", 5

def calc_ika(ph_val, bod_val, cod_val):
    """ Indeks Kualitas Air sederhana berdasarkan sub-indeks tiap parameter. Bobot: pH=30%, BOD=35%, COD=35% """
    _, _, ph_score  = get_ph_status(ph_val)
    _, _, bod_score = get_bod_status(bod_val)
    _, _, cod_score = get_cod_status(cod_val)
    ika = 0.30 * ph_score + 0.35 * bod_score + 0.35 * cod_score
    return round(ika, 1), ph_score, bod_score, cod_score

def ika_category(score):
    if score >= 80: return "Baik 🟢", "#22C55E"
    elif score >= 50: return "Tercemar Ringan–Sedang 🟡", "#F59E0B"
    elif score >= 25: return "Tercemar Berat 🔴", "#EF4444"
    else: return "Sangat Tercemar Berat ☠️", "#EF4444"

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

# ─────────────────────────────────────────────
#  MAIN — HERO
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
<div class="hero-badge">INDEKS KUALITAS AIR</div>
<h1 class="hero-title">{st.session_state.app_name}</h1>
<p class="hero-sub">{st.session_state.web_desc}</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FITUR TOMBOL & PANEL INPUT DI HALAMAN UTAMA
# ─────────────────────────────────────────────
st.markdown('<div class="sec-head">🎛️ Panel Kontrol Mode Input Data</div>', unsafe_allow_html=True)

# Membuat tata letak baris tombol interaktif halaman utama
btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    if st.button("📊 MODE 1: Input Nilai Langsung (PH/BOD/COD Sudah Diketahui)"):
        st.session_state.main_input_mode = "📊 Langsung (Nilai)"
with btn_col2:
    if st.button("🧪 MODE 2: Hitung dari Titrasi (Laboratorium)"):
        st.session_state.main_input_mode = "🧪 Dari Titrasi"

# Menampilkan indikator status mode yang sedang aktif saat ini
st.markdown(f"""
<div style="font-size:0.9rem; margin-bottom:20px; color:var(--muted);">
Mode aktif saat ini: <span style="color:var(--teal); font-weight:bold; font-family:'Space Mono', monospace;">{st.session_state.main_input_mode}</span>
</div>
""", unsafe_allow_html=True)

# Inisialisasi variabel default sebelum kondisional penentuan nilai input
ph_val = 7.0
bod_val = 2.0
cod_val = 15.0

# Wadah penampung form input data lapangan utama
with st.container():
    st.markdown('<div style="background:var(--card); border:1px solid var(--border); border-radius:14px; padding:24px; margin-bottom:25px;">', unsafe_allow_html=True)
    # Input umum pH (Selalu muncul di kedua mode)
    ph_val = st.number_input("Masukkan Nilai pH", min_value=0.0, max_value=14.0, value=7.0, step=0.1, help="Skala 0–14. Baku mutu: 6.5–8.0", key="main_ph_input")
    
    if st.session_state.main_input_mode == "📊 Langsung (Nilai)":
        st.markdown("<p style='color:var(--teal); font-weight:600; margin-top:10px;'>Masukkan Nilai Parameter Langsung:</p>", unsafe_allow_html=True)
        col_direct1, col_direct2 = st.columns(2)
        with col_direct1:
            bod_val = st.number_input("BOD (mg/L)", min_value=0.0, max_value=200.0, value=2.0, step=0.1, help="Biochemical Oxygen Demand. Baku mutu: < 3 mg/L", key="main_bod_direct")
        with col_direct2:
            cod_val = st.number_input("COD (mg/L)", min_value=0.0, max_value=500.0, value=15.0, step=0.1, help="Chemical Oxygen Demand. Baku mutu: < 25 mg/L", key="main_cod_direct")
            
    elif st.session_state.main_input_mode == "🧪 Dari Titrasi":
        # ── BOD dari Titrasi Winkler ──
        st.markdown("""<div style="font-size:0.9rem; color:#0EB8A4; font-family:'Space Mono',monospace; margin:15px 0 6px 0; font-weight:bold;">🔬 Perhitungan Parameter BOD — Titrasi Winkler</div>""", unsafe_allow_html=True)
        st.markdown("""<div style="font-size:0.75rem; color:#7A8BA6; margin-bottom:8px;"> Rumus: BOD = (V_titran_blanko − V_titran_sampel) × N_Na₂S₂O₃ × 8000 / V_sampel </div>""", unsafe_allow_html=True)
        
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
        st.markdown(f"""<div style="background:rgba(14,184,164,0.08); border:1px solid rgba(14,184,164,0.3); border-radius:8px; padding:10px 14px; font-size:0.85rem; margin:6px 0 20px 0;"> Hasil Perhitungan Terhitung BOD: <b style="color:#0EB8A4; font-family:'Space Mono',monospace;"> {bod_val} mg/L</b></div>""", unsafe_allow_html=True)
        
        # ── COD dari Titrasi Permanganometri / Dikromat ──
        st.markdown("""<div style="font-size:0.9rem; color:#8B5CF6; font-family:'Space Mono',monospace; margin:15px 0 6px 0; font-weight:bold;">🔬 Perhitungan Parameter COD — Titrasi Dikromat / Permanganometri</div>""", unsafe_allow_html=True)
        st.markdown("""<div style="font-size:0.75rem; color:#7A8BA6; margin-bottom:8px;"> Rumus: COD = (V_blanko − V_sampel) × N_titran × 8000 / V_sampel </div>""", unsafe_allow_html=True)
        
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
        st.markdown(f"""<div style="background:rgba(139,92,246,0.08); border:1px solid rgba(139,92,246,0.3); border-radius:8px; padding:10px 14px; font-size:0.85rem; margin:6px 0 4px 0;"> Hasil Perhitungan Terhitung COD: <b style="color:#8B5CF6; font-family:'Space Mono',monospace;"> {cod_val} mg/L</b></div>""", unsafe_allow_html=True)
        
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
#  TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Analisis Parameter",
    "📖 Referensi Standar",
    "📈 Visualisasi",
    "ℹ️ Tentang",
])

# ══════════════════════════════════════════════
#  TAB 1 — ANALISIS
# ══════════════════════════════════════════════
with tab1:
    # IKA Score strip
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

    # ── Parameter Detail ──
    st.markdown('<div class="sec-head">Detail Parameter</div>', unsafe_allow_html=True)
    
    # pH
    with st.expander("🔵 pH — Derajat Keasaman Air", expanded=True):
        col_a, col_b = st.columns([1, 1.4])
        with col_a:
            st.markdown("""
            *Apa itu pH?*
            pH mengukur konsentrasi ion hidrogen dalam air dan menunjukkan seberapa asam atau basa suatu larutan. Skala pH berkisar 0–14, di mana 7 bersifat netral.
            
            *Mengapa penting?*
            pH mempengaruhi reaksi kimia dalam air, kelarutan logam berat, dan kemampuan organisme akuatik untuk bertahan hidup. Nilai di luar rentang 6.5–8.0 menunjukkan adanya pencemaran atau gangguan keseimbangan ekosistem perairan.
            """)
        with col_b:
            if ph_cls == "good":
                st.markdown(f'<div class="info-box">✅ <strong>pH {ph_val}</strong> — Nilai ini memenuhi baku mutu air kelas II (6.5–8.0). Air dalam kondisi normal dan aman untuk berbagai pemanfaatan.</div>', unsafe_allow_html=True)
            elif ph_cls == "warn":
                st.markdown(f'<div class="warn-box">⚠️ <strong>pH {ph_val}</strong> — Nilai ini berada di luar baku mutu optimal. Air menunjukkan tanda-tanda asam/basa ringan. Perlu monitoring lebih lanjut.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bad-box">🚨 <strong>pH {ph_val}</strong> — Nilai ekstrem! Air terindikasi sangat asam atau basa. Berbahaya bagi biota air and tidak layak untuk penggunaan langsung.</div>', unsafe_allow_html=True)

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
                <div style="margin-top:10px; font-size:0.83rem; color:#7A8BA6; line-height:1.6;">
                {'✅ <b style="color:#22C55E">Mudah terurai secara biologis</b> — Rasio > 0.5 menandakan limbah organik yang dapat diolah dengan proses biologis (IPAL).' if ratio >= 0.5 else ('⚠️ <b style="color:#F59E0B">Cukup dapat terurai</b> — Perlu kombinasi pengolahan biologis dan kimia.' if ratio >= 0.3 else '🔴 <b style="color:#EF4444">Sulit terurai secara biologis</b> — Rasio < 0.3 mengindikasikan bahan kimia organik rekalcitran. Perlu pengolahan kimia-fisika.')}
                </div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="param-card">
                <div class="param-title">Sub-Indeks Tiap Parameter</div>
                <div class="param-fullname">Kontribusi terhadap IKA</div>
                <div style="margin-top:14px;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                        <span style="color:#7A8BA6; font-size:0.83rem;">Sub-Indeks pH (Bobot 30%)</span>
                        <span style="font-family:\'Space Mono\',monospace; color:#0EB8A4; font-weight:bold;">{ph_si} / 100</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                        <span style="color:#7A8BA6; font-size:0.83rem;">Sub-Indeks BOD (Bobot 35%)</span>
                        <span style="font-family:\'Space Mono\',monospace; color:#22C55E; font-weight:bold;">{bod_si} / 100</span>
                    </div>
                    <div style="display:flex; justify-content:space-between;">
                        <span style="color:#7A8BA6; font-size:0.83rem;">Sub-Indeks COD (Bobot 35%)</span>
                        <span style="font-family:\'Space Mono\',monospace; color:#1A6EFC; font-weight:bold;">{cod_si} / 100</span>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  TAB 2 — REFERENSI
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-head">📋 Tabel Parameter Baku Mutu Air (Kelas II)</div>', unsafe_allow_html=True)
    
    st.markdown("<p style='color:var(--teal); font-weight:bold; margin-top:10px;'>1. Parameter pH (Derajat Keasaman)</p>", unsafe_allow_html=True)
    render_ref_table(PH_REF)
    
    st.markdown("<p style='color:var(--teal); font-weight:bold; margin-top:20px;'>2. Parameter BOD (Biochemical Oxygen Demand)</p>", unsafe_allow_html=True)
    render_ref_table(BOD_REF)
    
    st.markdown("<p style='color:var(--teal); font-weight:bold; margin-top:20px;'>3. Parameter COD (Chemical Oxygen Demand)</p>", unsafe_allow_html=True)
    render_ref_table(COD_REF)

# ══════════════════════════════════════════════
#  TAB 3 — VISUALISASI
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-head">📈 Grafik & Visualisasi Kualitas Air</div>', unsafe_allow_html=True)
    
    # 1. Gauge Chart untuk IKA
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = ika_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Indeks Kualitas Air (Category: {ika_cat})", 'font': {'color': "#E8EDF5", 'size': 16}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#7A8BA6"},
            'bar': {'color': ika_color},
            'bgcolor': "#161B25",
            'borderwidth': 1,
            'bordercolor': "#242C3D",
            'steps': [
                {'range': [0, 25], 'color': 'rgba(239,68,68,0.1)'},
                {'range': [25, 50], 'color': 'rgba(239,68,68,0.2)'},
                {'range': [50, 80], 'color': 'rgba(245,158,11,0.15)'},
                {'range': [80, 100], 'color': 'rgba(34,197,94,0.15)'}
            ],
        }
    ))
    fig_gauge.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#E8EDF5", 'family': "Plus Jakarta Sans"},
        height=280,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    # 2. Bar Chart Perbandingan Sub-Indeks
    st.markdown('<div class="sec-head">Perbandingan Sub-Indeks Kontributor</div>', unsafe_allow_html=True)
    df_si = pd.DataFrame({
        'Parameter': ['pH', 'BOD', 'COD'],
        'Sub-Indeks': [ph_si, bod_si, cod_si],
        'Bobot (%)': [30, 35, 35]
    })
    
    fig_bar = px.bar(
        df_si, 
        x='Parameter', 
        y='Sub-Indeks',
        text='Sub-Indeks',
        color='Parameter',
        color_discrete_map={'pH': '#0EB8A4', 'BOD': '#22C55E', 'COD': '#1A6EFC'},
        hover_data=['Bobot (%)']
    )
    fig_bar.update_traces(textposition='outside', marker_line_color='#242C3D', marker_line_width=1)
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#161B25',
        font={'color': "#E8EDF5"},
        xaxis=dict(showgrid=False, title_font=dict(size=12)),
        yaxis=dict(range=[0, 110], gridcolor="#242C3D", title_font=dict(size=12)),
        showlegend=False,
        height=300,
        margin=dict(l=20, r=20, t=10, b=10)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ══════════════════════════════════════════════
#  TAB 4 — TENTANG
# ══════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec-head">ℹ️ Informasi Sistem & Kelompok</div>', unsafe_allow_html=True)
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown(f"""
        <div class="about-card" style="border-color:rgba(26,110,252,0.3);">
            <div class="about-label">Sistem IPAL & Baku Mutu</div>
            <div class="about-title">🌊 {st.session_state.app_name}</div>
            <div class="about-body">
                Aplikasi ini dirancang untuk melakukan kalkulasi cepat parameter kimia lingkungan air. 
                Acuan klasifikasi didasarkan pada <b>Peraturan Pemerintah (PP) No. 22 Tahun 2021</b> Lampiran VI mengenai Baku Mutu Kualitas Air Nasional Kelas II (diperuntukkan bagi prasarana/sarana rekreasi air, pembudidayaan ikan air tawar, peternakan, air untuk mengairi pertanaman).
                <br><br>
                <b>Nilai Batas Baku Mutu Kelas II:</b><br>
                • <b>pH:</b> Rentang 6.5 – 8.5 (Optimal 6.5–8.0)<br>
                • <b>BOD:</b> Maksimal ≤ 3 mg/L. Kebutuhan bio-oksigen bakteri pengurai.<br>
                • <b>COD:</b> Maksimal ≤ 25 mg/L. Total oksigen untuk mengoksidasi semua bahan organik secara kimiawi.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_t2:
        st.markdown(f"""
        <div class="about-card" style="border-color:rgba(14,184,164,0.3);">
            <div class="about-label">Metodologi IKA</div>
            <div class="about-title">📐 Cara Perhitungan Indeks</div>
            <div class="about-body">
                Indeks Kualitas Air (IKA) dihitung menggunakan sistem sub-indeks berbobot:
                <br><br>
                <code style="background:#0D1117; padding:10px 16px; border-radius:6px; border:1px solid #242C3D; display:block; margin:8px 0; font-family:\'Space Mono\',monospace; color:#0EB8A4; font-size:0.85rem;">
                IKA = (0.30 × SI_pH) + (0.35 × SI_BOD) + (0.35 × SI_COD)
                </code>
                Di mana SI (Sub-Indeks) bernilai 0–100 berdasarkan posisi nilai terhadap baku mutu. 
                Bobot lebih besar pada BOD dan COD karena keduanya langsung mencerminkan beban pencemaran organik yang paling umum di perairan Indonesia.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  BAGIAN BAWAH UTAMA (PENGGANTI SIDEBAR)
# ─────────────────────────────────────────────
st.markdown('<div class="sec-head">⚙️ Panel Admin & Referensi Aplikasi</div>', unsafe_allow_html=True)

# Memindahkan st.expander Pengaturan Aplikasi asli ke bagian bawah halaman utama
with st.expander("⚙️  Pengaturan Aplikasi (Konfigurasi Konten)"):
    new_app = st.text_input("Nama Aplikasi", value=st.session_state.app_name)
    new_grp = st.text_input("Nama Kelompok", value=st.session_state.group_name)
    new_gdesc = st.text_area("Deskripsi Kelompok", value=st.session_state.group_desc, height=80)
    new_wdesc = st.text_area("Deskripsi Website", value=st.session_state.web_desc, height=100)
    if st.button("💾  SIMPAN PENGATURAN"):
        st.session_state.app_name  = new_app
        st.session_state.group_name  = new_grp
        st.session_state.group_desc  = new_gdesc
        st.session_state.web_desc    = new_wdesc
        st.success("Pengaturan tersimpan!")

# Memindahkan Info Box Kelompok & Referensi Legal Hukum ke halaman utama bagian bawah
col_bottom1, col_bottom2 = st.columns(2)
with col_bottom1:
    st.markdown(f"""
    <div style="padding:16px; background:var(--card); border-radius:10px; border:1px solid var(--border); height:100%;">
        <p style="color:var(--teal); font-weight:bold; margin-top:0; font-family:'Space Mono', monospace; font-size:0.85rem;">👥 {st.session_state.group_name}</p>
        <p style="white-space: pre-line; color:var(--text); font-size:0.85rem; line-height:1.6;">{st.session_state.group_desc}</p>
    </div>
    """, unsafe_allow_html=True)

with col_bottom2:
    st.markdown("""
    <div style="padding:16px; background:#0D1117; border-radius:10px; border:1px solid var(--border); font-size:0.8rem; color:#7A8BA6; height:100%; display:flex; flex-direction:column; justify-content:center;">
        <div><b>📋 Dokumen Referensi Regulasi Lingkungan:</b></div>
        <div style="margin-top:6px;">• Peraturan Pemerintah No. 22 Tahun 2021 (Lampiran VI)</div>
        <div>• Baku mutu kualitas air nasional kelas II perairan sungai/sejenis</div>
        <div>• Standardisasi Pengujian Laboratorium Kementerian LHK RI</div>
    </div>
    """, unsafe_allow_html=True)
