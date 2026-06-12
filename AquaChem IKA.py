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
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* Root Variables dengan penyesuaian kontras tinggi */
:root {
    --teal:   #0D9488;
    --blue:   #1D4ED8;
    --indigo: #2D3A8C;
    --dark:   #0D1117;
    --card:   #1F2937;
    --border: #4B5563;
    --text:   #111827;
    --muted:  #4B5563;
    --good:   #15803D;
    --warn:   #B45309;
    --bad:    #B91C1C;
}

/* Fallback deteksi tema otomatis Streamlit */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Memastikan teks kontras tinggi di semua komponen kustom */
.hero {
    background: linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 100%);
    border: 2px solid #9CA3AF;
    border-radius: 16px;
    padding: 40px 36px 32px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
@media (prefers-color-scheme: dark) {
    .hero {
        background: linear-gradient(135deg, #111827 0%, #1F2937 100%);
        border: 2px solid #4B5563;
    }
    .hero-title {
        background: linear-gradient(90deg, #2DD4BF, #60A5FA) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    .hero-sub { color: #E5E7EB !important; }
    .param-card { background: #1F2937 !important; border: 2px solid #4B5563 !important; }
    .param-value { color: #FFFFFF !important; }
    .param-fullname, .param-unit { color: #9CA3AF !important; }
    .ref-table td { color: #FFFFFF !important; border-bottom: 1px solid #4B5563 !important; }
    .ref-table th { background: rgba(45, 212, 191, 0.2) !important; color: #2DD4BF !important; }
    .info-box { background: rgba(21, 128, 61, 0.15) !important; color: #86EFAC !important; border: 1px solid #15803D !important; }
    .warn-box { background: rgba(180, 83, 9, 0.15) !important; color: #FDE047 !important; border: 1px solid #B45309 !important; }
    .bad-box { background: rgba(185, 28, 28, 0.15) !important; color: #FCA5A5 !important; border: 1px solid #B91C1C !important; }
    .about-card { background: #1F2937 !important; border: 2px solid #4B5563 !important; }
    .about-body { color: #E5E7EB !important; }
    .about-title { color: #FFFFFF !important; }
}

.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    color: #111827;
    margin: 0 0 8px 0;
    line-height: 1.2;
}
.hero-sub {
    color: #374151;
    font-size: 1.1rem;
    margin: 0;
    font-weight: 500;
}
.hero-badge {
    display: inline-block;
    background: #0D9488;
    color: white;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.75rem;
    font-family: 'Space Mono', monospace;
    letter-spacing: 1px;
    margin-bottom: 12px;
    font-weight: bold;
}

/* Cards */
.param-card {
    background: #FFFFFF;
    border: 2px solid #D1D5DB;
    border-radius: 14px;
    padding: 24px 22px;
    height: 100%;
}
.param-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.1rem;
    color: #0D9488;
    margin-bottom: 6px;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.param-fullname {
    color: #4B5563;
    font-size: 0.85rem;
    margin-bottom: 16px;
    font-weight: 500;
}
.param-value {
    font-size: 2.4rem;
    font-weight: 800;
    color: #111827;
    line-height: 1;
    margin-bottom: 4px;
}
.param-unit {
    font-size: 0.85rem;
    color: #4B5563;
    margin-bottom: 14px;
}
.status-chip {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.status-good   { background: #DCFCE7;  color: #15803D; border: 2px solid #22C55E; }
.status-warn   { background: #FEF3C7;  color: #B45309; border: 2px solid #F59E0B; }
.status-bad    { background: #FEE2E2;  color: #B91C1C; border: 2px solid #EF4444; }

/* Reference Table */
.ref-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
}
.ref-table th {
    background: #E5E7EB;
    color: #0F766E;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    padding: 12px 14px;
    text-align: left;
    border-bottom: 2px solid #9CA3AF;
}
.ref-table td {
    padding: 12px 14px;
    border-bottom: 1px solid #D1D5DB;
    color: #111827;
    font-weight: 500;
}

/* Section Header */
.sec-head {
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    letter-spacing: 2px;
    color: #0D9488;
    text-transform: uppercase;
    margin: 32px 0 16px 0;
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: bold;
}
.sec-head::after {
    content: "";
    flex: 1;
    height: 2px;
    background: #9CA3AF;
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
    font-size: 0.9rem;
    color: #374151;
    font-weight: 600;
    margin-top: 6px;
}
.ika-cat {
    font-size: 1.2rem;
    font-weight: 800;
    margin-top: 8px;
}

/* Info box dengan tingkat keterbacaan tinggi */
.info-box { background: #DCFCE7; border-left: 5px solid #15803D; border-radius: 8px; padding: 14px 18px; font-size: 0.95rem; color: #14532D; margin: 10px 0; line-height: 1.6; }
.warn-box { background: #FEF3C7; border-left: 5px solid #B45309; border-radius: 8px; padding: 14px 18px; font-size: 0.95rem; color: #78350F; margin: 10px 0; line-height: 1.6; }
.bad-box  { background: #FEE2E2; border-left: 5px solid #B91C1C; border-radius: 8px; padding: 14px 18px; font-size: 0.95rem; color: #7F1D1D; margin: 10px 0; line-height: 1.6; }

/* About section */
.about-card {
    background: #FFFFFF;
    border: 2px solid #D1D5DB;
    border-radius: 14px;
    padding: 28px 26px;
    margin-bottom: 18px;
}
.about-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 2px;
    color: #0D9488;
    text-transform: uppercase;
    margin-bottom: 8px;
    font-weight: bold;
}
.about-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 10px;
}
.about-body {
    color: #374151;
    font-size: 0.95rem;
    line-height: 1.7;
    font-weight: 500;
}

/* Hide default streamlit branding */
#MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE — default settings
# ─────────────────────────────────────────────
if "app_name" not in st.session_state:
    st.session_state.app_name = "AquaChem IKA"
if "web_desc" not in st.session_state:
    st.session_state.web_desc = (
        "Aplikasi ini dikembangkan untuk membantu analisis kualitas air "
        "berdasarkan parameter kimia utama yaitu pH, BOD, dan COD. "
        "Gunakan panel input data di bawah banner halaman utama untuk memasukkan data pengukuran."
    )
if "main_input_mode" not in st.session_state:
    st.session_state.main_input_mode = "📊 Langsung (Nilai)"

# ─────────────────────────────────────────────
#  REFERENCE DATA
# ─────────────────────────────────────────────
PH_REF = [
    {"Kategori": "Sangat Asam / Sangat Basa (Berbahaya)", "Rentang": "< 6.0 atau > 9.0", "Status": "💀 Tidak Sesuai", "Kelas": "bad"},
    {"Kategori": "Asam / Basa Ringan", "Rentang": "6.0 – 6.5 atau 8.5 – 9.0", "Status": "⚠️ Tidak Sesuai", "Kelas": "warn"},
    {"Kategori": "Sesuai Ketentuan PP No. 22/2021", "Rentang": "6.5 – 8.5", "Status": "✅ Sesuai Baku Mutu", "Kelas": "good"},
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
    if 6.5 <= v <= 8.5:
        return "Sesuai Baku Mutu", "good", 100
    elif (6.0 <= v < 6.5) or (8.5 < v <= 9.0):
        return "Tidak Sesuai", "warn", 50
    else:
        return "Tidak Sesuai", "bad", 10

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
    _, _, ph_score  = get_ph_status(ph_val)
    _, _, bod_score = get_bod_status(bod_val)
    _, _, cod_score = get_cod_status(cod_val)
    ika = 0.30 * ph_score + 0.35 * bod_score + 0.35 * cod_score
    return round(ika, 1), ph_score, bod_score, cod_score

def ika_category(score):
    if score >= 80:
        return "Baik 🟢", "#15803D"
    elif score >= 50:
        return "Tercemar Ringan–Sedang 🟡", "#B45309"
    elif score >= 25:
        return "Tercemar Berat 🔴", "#B91C1C"
    else:
        return "Sangat Tercemar Berat ☠️", "#B91C1C"

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
    <div class="hero-badge">BAKU MUTU AIR KELAS II (PP NO. 22 TAHUN 2021)</div>
    <h1 class="hero-title">{st.session_state.app_name}</h1>
    <p class="hero-sub">{st.session_state.web_desc}</p>
    <div style="margin-top:15px; padding:8px 12px; background:rgba(13, 148, 136, 0.1); border-radius:6px; font-size:0.9rem; color:#0D9488; font-weight:bold; border:1px solid rgba(13, 148, 136, 0.3);">
        📢 INFORMASI UTAMA: Website aplikasi ini dikonfigurasi secara khusus sebagai sistem monitoring dan evaluasi kualitas air berdasarkan Standar Baku Mutu Air Kelas II menurut PP Nomor 22 Tahun 2021.
    </div>
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
<div style="font-size:0.95rem; margin-bottom:20px; color:#374151; font-weight: 600;">
    Mode aktif saat ini: <span style="color:#0D9488; font-weight:bold; font-family:'Space Mono', monospace;">{st.session_state.main_input_mode}</span>
</div>
""", unsafe_allow_html=True)

ph_val = 7.0
bod_val = 2.0
cod_val = 15.0

with st.container():
    st.markdown('<div style="background:rgba(243,244,246,0.5); border:2px solid #D1D5DB; border-radius:14px; padding:24px; margin-bottom:25px;">', unsafe_allow_html=True)
    
    ph_val = st.number_input("Masukkan Nilai pH", min_value=0.0, max_value=14.0, value=7.0, step=0.1, help="Skala 0–14. Baku mutu Kelas II: 6.5–8.5", key="main_ph_input")
    
    if st.session_state.main_input_mode == "📊 Langsung (Nilai)":
        st.markdown("<p style='color:#0D9488; font-weight:700; margin-top:10px;'>Masukkan Nilai Parameter Langsung:</p>", unsafe_allow_html=True)
        col_direct1, col_direct2 = st.columns(2)
        with col_direct1:
            bod_val = st.number_input("BOD (mg/L)", min_value=0.0, max_value=200.0, value=2.0, step=0.1, help="Biochemical Oxygen Demand. Baku mutu: ≤ 3 mg/L", key="main_bod_direct")
        with col_direct2:
            cod_val = st.number_input("COD (mg/L)", min_value=0.0, max_value=500.0, value=15.0, step=0.1, help="Chemical Oxygen Demand. Baku mutu: ≤ 25 mg/L", key="main_cod_direct")
            
    elif st.session_state.main_input_mode == "🧪 Dari Titrasi":
        st.markdown("""<div style="font-size:1rem; color:#0D9488; font-family:'Space Mono',monospace; margin:15px 0 6px 0; font-weight:bold;">🔬 Perhitungan Parameter BOD — Titrasi Winkler</div>""", unsafe_allow_html=True)
        st.markdown("""<div style="font-size:0.85rem; color:#4B5563; margin-bottom:8px; font-weight:500;"> Rumus: BOD = (V_titran_blanko − V_titran_sampel) × N_Na₂S₂O₃ × 8000 / V_sampel </div>""", unsafe_allow_html=True)
        
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
        st.markdown(f"""<div style="background:rgba(13, 148, 136, 0.1); border:2px solid #0D9488; border-radius:8px; padding:10px 14px; font-size:0.9rem; margin:6px 0 20px 0; color:#111827; font-weight:600;"> Hasil Perhitungan Terhitung BOD: <b style="color:#0D9488; font-family:'Space Mono',monospace;"> {bod_val} mg/L</b></div>""", unsafe_allow_html=True)
        
        st.markdown("""<div style="font-size:1rem; color:#1D4ED8; font-family:'Space Mono',monospace; margin:15px 0 6px 0; font-weight:bold;">🔬 Perhitungan Parameter COD — Titrasi Dikromat / Permanganometri</div>""", unsafe_allow_html=True)
        st.markdown("""<div style="font-size:0.85rem; color:#4B5563; margin-bottom:8px; font-weight:500;"> Rumus: COD = (V_blanko − V_sampel) × N_titran × 8000 / V_sampel </div>""", unsafe_allow_html=True)
        
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
        st.markdown(f"""<div style="background:rgba(29, 78, 216, 0.1); border:2px solid #1D4ED8; border-radius:8px; padding:10px 14px; font-size:0.9rem; margin:6px 0 4px 0; color:#111827; font-weight:600;"> Hasil Perhitungan Terhitung COD: <b style="color:#1D4ED8; font-family:'Space Mono',monospace;"> {cod_val} mg/L</b></div>""", unsafe_allow_html=True)
        
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
    st.markdown('<div class="sec-head">Indeks Kualitas Air (IKA)</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1])
    
    with c1:
        st.markdown(f"""
        <div class="param-card" style="border-color:{ika_color};">
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
    
    # pH
    with st.expander("🔵 pH — Derajat Keasaman Air", expanded=True):
        col_a, col_b = st.columns([1, 1.4])
        with col_a:
            st.markdown("""
            *Apa itu pH?*
            pH mengukur konsentrasi ion hidrogen dalam air dan menunjukkan seberapa asam atau basa suatu larutan. Skala pH berkisar 0–14, di mana 7 bersifat netral.
            
            *Mengapa penting?*
            pH mempengaruhi reaksi kimia dalam air, kelarutan logam berat, dan kehidupan biota. Berdasarkan ketentuan **PP No. 22 Tahun 2021 Lampiran VI**, standar baku mutu pH untuk **Air Kelas II** berada pada rentang **6.5 – 8.5**.
            """)
        with col_b:
            if ph_cls == "good":
                st.markdown(f'<div class="info-box">✅ <strong>pH {ph_val}</strong> — Nilai ini memenuhi ketentuan standar baku mutu Air Kelas II sesuai PP No. 22 Tahun 2021 (Rentang 6.5 – 8.5). Air berada dalam rentang normal yang dipersyaratkan.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bad-box">🚨 <strong>pH {ph_val}</strong> — Nilai ini tidak sesuai dengan ketentuan standar baku mutu Air Kelas II menurut PP No. 22 Tahun 2021 yang mewajibkan rentang berada antara 6.5 – 8.5.</div>', unsafe_allow_html=True)

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
                st.markdown(f'<div class="info-box">✅ <strong>BOD {bod_val} mg/L</strong> — Memenuhi baku mutu air kelas II (≤ 3 mg/L). Kandungan bahan organik rendah, oksigen terlarut cukup untuk mendukung ekosistem perairan.</div>', unsafe_allow_html=True)
            elif bod_cls == "warn":
                st.markdown(f'<div class="warn-box">⚠️ <strong>BOD {bod_val} mg/L</strong> — Melewati baku mutu air kelas II (3 mg/L). Air terindikasi tercemar bahan organik. Dapat mengganggu kehidupan biota air.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bad-box">🚨 <strong>BOD {bod_val} mg/L</strong> — Jauh melampaui baku mutu air kelas II! Pencemaran organik berat. Air tidak layak pakai tanpa pengolahan intensif.</div>', unsafe_allow_html=True)

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
                st.markdown(f'<div class="info-box">✅ <strong>COD {cod_val} mg/L</strong> — Memenuhi baku mutu air kelas II (≤ 25 mg/L). Beban pencemar organik dan kimia masih dalam batas aman.</div>', unsafe_allow_html=True)
            elif cod_cls == "warn":
                st.markdown(f'<div class="warn-box">⚠️ <strong>COD {cod_val} mg/L</strong> — Melampaui baku mutu air kelas II. Indikasi pencemaran bahan kimia organik. Perlu investigasi sumber pencemar.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bad-box">🚨 <strong>COD {cod_val} mg/L</strong> — Sangat tinggi! Indikasi pencemaran kimia berat. Air memerlukan pengolahan khusus sebelum digunakan.</div>', unsafe_allow_html=True)

    # Rasio BOD/COD
    st.markdown('<div class="sec-head">Analisis Lanjutan</div>', unsafe_allow_html=True)
    if cod_val > 0:
        ratio = round(bod_val / cod_val, 3)
        col1, col2 = st.columns(2)
        with col1:
            status_text = (
                '✅ <b style="color:#15803D">Mudah terurai secara biologis</b> — Rasio ≥ 0.5 menandakan limbah organik yang dapat diolah dengan proses biologis (IPAL).'
                if ratio >= 0.5 else 
                ('⚠️ <b style="color:#B45309">Cukup dapat terurai</b> — Perlu kombinasi pengolahan biologis dan kimia.' if ratio >= 0.2 else 
                 '🚨 <b style="color:#B91C1C">Sulit terurai (Kurang Biodegradable)</b> — Didominasi zat kimia sintetis beracun/toksik, memerlukan pengolahan kimiawi khusus (AOPs).')
            )
            st.markdown(f"""
            <div class="param-card">
                <div class="param-title">Rasio BOD/COD</div>
                <div class="param-fullname">Biodegradabilitas Limbah</div>
                <div class="param-value">{ratio}</div>
                <div style="margin-top:10px; font-size:0.95rem; color:#111827; font-weight:500; line-height:1.6;">
                    {status_text}
                </div>
            </div>""", unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="param-card">
                <div class="param-title">💡 Interpretasi Singkat</div>
                <div class="about-body" style="font-size:0.95rem; line-height:1.6;">
                    Nilai rasio <b>{ratio}</b> memberikan gambaran mengenai karakteristik beban cemaran di perairan. Semakin rendah rasio mendekati 0, menandakan bahwa polutan air didominasi oleh zat kimia industri non-biodegradable yang tidak sanggup dirombak oleh bakteri alami perairan.
                </div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  TAB 2 — REFERENSI STANDAR
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-head">Tabel Acuan Standar Baku Mutu Air Kelas II</div>', unsafe_allow_html=True)
    
    st.markdown("### 🔵 Parameter pH (Berdasarkan PP No. 22 Tahun 2021)")
    render_ref_table(PH_REF)
    
    st.markdown("### 🟢 Parameter BOD (Biochemical Oxygen Demand)")
    render_ref_table(BOD_REF)
    
    st.markdown("### 🔴 Parameter COD (Chemical Oxygen Demand)")
    render_ref_table(COD_REF)

# ══════════════════════════════════════════════
#  TAB 3 — VISUALISASI
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-head">Grafik Analisis Kualitas Air</div>', unsafe_allow_html=True)
    
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("Kondisi pH", "Kandungan BOD (mg/L)", "Kandungan COD (mg/L)"),
        specs=[[{"type": "indicator"}, {"type": "bar"}, {"type": "bar"}]]
    )
    
    # Gauge pH
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=ph_val,
            domain={'x': [0, 0.28], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 14], 'tickwidth': 1},
                'bar': {'color': "#0D9488"},
                'steps': [
                    {'range': [0, 6.5], 'color': "#FEE2E2"},
                    {'range': [6.5, 8.5], 'color': "#DCFCE7"},
                    {'range': [8.5, 14], 'color': "#FEE2E2"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 3},
                    'thickness': 0.75,
                    'value': ph_val
                }
            }
        ),
        row=1, col=1
    )
    
    # Bar BOD
    fig.add_trace(
        go.Bar(
            x=["Sampel Air", "Baku Mutu Kelas II"],
            y=[bod_val, 3],
            marker_color=["#22C55E" if bod_val <= 3 else "#EF4444", "#4B5563"],
            text=[f"{bod_val} mg/L", "3 mg/L"],
            textposition='auto',
            showlegend=False
        ),
        row=1, col=2
    )
    
    # Bar COD
    fig.add_trace(
        go.Bar(
            x=["Sampel Air", "Baku Mutu Kelas II"],
            y=[cod_val, 25],
            marker_color=["#22C55E" if cod_val <= 25 else "#EF4444", "#4B5563"],
            text=[f"{cod_val} mg/L", "25 mg/L"],
            textposition='auto',
            showlegend=False
        ),
        row=1, col=3
    )
    
    fig.update_layout(
        height=450,
        margin=dict(l=20, r=20, t=60, b=20),
        font=dict(family="Plus Jakarta Sans", size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════
#  TAB 4 — TENTANG
# ══════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec-head">Informasi Metodologi Perhitungan</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="about-card">
        <div class="about-label">Parameter pH</div>
        <div class="about-title">📐 Standar pH Air Kelas II</div>
        <div class="about-body">
            Sesuai ketentuan <b>PP No. 22 Tahun 2021 Lampiran VI</b>, syarat kelayakan pH untuk kategori Air Kelas II ditetapkan berada dalam rentang nilai <b>6.5 hingga 8.5</b>. Rentang baku mutu ini diperbarui dari regulasi lama demi menjaga keseimbangan ekosistem dan biota akuatik serta peruntukan prasarana rekreasi air, pembudidayaan ikan air tawar, peternakan, dan mengairi pertamanan.
        </div>
    </div>
    
    <div class="about-card">
        <div class="about-label">Metodologi IKA</div>
        <div class="about-title">📐 Cara Perhitungan Indeks</div>
        <div class="about-body">
            Indeks Kualitas Air (IKA) dihitung menggunakan sistem sub-indeks berbobot dengan skema formulasi sebagai berikut:
            <br><br>
            <code style="background:#111827; padding:10px 16px; border-radius:6px;
                         border:1px solid #4B5563; display:block; margin:8px 0;
                         font-family:'Space Mono',monospace; color:#2DD4BF; font-size:0.95rem;">
                IKA = (0.30 × SI_pH) + (0.35 × SI_BOD) + (0.35 × SI_COD)
            </code>
            Di mana nilai masing-masing SI (Sub-Indeks) bergradasi antara 0–100 berdasarkan letak posisi nilai riil sampel di lapangan terhadap batasan baku mutu nasional. Bobot alokasi lebih tinggi difokuskan pada BOD dan COD karena kedua nilai tersebut secara akumulatif mencerminkan realitas beban pencemaran organik struktural yang paling krusial ditemukan di perairan Indonesia.
        </div>
    </div>
    """, unsafe_allow_html=True)
