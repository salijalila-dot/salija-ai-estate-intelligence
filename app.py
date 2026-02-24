import streamlit as st
from PIL import Image
import google.generativeai as genai
import os

# --- AI YAPILANDIRMASI ---
# API Anahtarını sistemden gizli olarak alıyoruz
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
MODEL_NAME = 'gemini-1.5-flash' 
model = genai.GenerativeModel(MODEL_NAME)

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Salija AI | Estate Intelligence", page_icon="🏢", layout="wide")

# --- HIZLANDIRICI ---
@st.cache_data
def load_logo(file_path):
    if os.path.exists(file_path): return Image.open(file_path)
    return None

# --- GLOBAL DİL SİSTEMİ ---
ui_languages = {
    "English": {
        "title": "Salija AI | Estate Intelligence",
        "service_desc": "AI-Powered Visual Property Analysis & Copywriting Engine",
        "subtitle": "Convert property visuals into high-conversion marketing masterpieces.",
        "settings": "⚙️ Configuration",
        "target_lang": "✍️ Write Listing In...",
        "prop_type": "Property Type",
        "price": "Market Price",
        "location": "Location",
        "tone": "Strategy",
        "tones": ["Ultra-Luxury", "Investment Potential", "Modern Minimalist", "Family Comfort", "Standard Pro"],
        "custom_inst": "📝 Special Notes",
        "custom_inst_ph": "E.g., High ceilings, near metro...",
        "btn": "🚀 GENERATE ELITE COPY",
        "upload_label": "📸 Drop Property Photos Here",
        "result": "💎 Executive Preview",
        "loading": "Architecting your listing...",
        "empty": "Awaiting visuals to start analysis.",
        "download": "📥 Export TXT",
        "save_btn": "💾 Save Changes",
        "saved_msg": "✅ Saved!",
        "error": "Error:"
    },
    "Türkçe": {
        "title": "Salija AI | Emlak Zekası",
        "service_desc": "Yapay Zeka Destekli Görsel Mülk Analizi ve İlan Yazım Motoru",
        "subtitle": "Mülk görsellerini yüksek dönüşümlü pazarlama şaheserlerine dönüştürün.",
        "settings": "⚙️ Yapılandırma",
        "target_lang": "✍️ İlan Yazım Dili...",
        "prop_type": "Emlak Tipi",
        "price": "Pazar Fiyatı",
        "location": "Konum",
        "tone": "Strateji",
        "tones": ["Ultra-Lüks", "Yatırım Potansiyeli", "Modern Minimalist", "Aile Konforu", "Standart Profesyonel"],
        "custom_inst": "📝 Özel Notlar",
        "custom_inst_ph": "Örn: Yüksek tavanlar, metroya yakın...",
        "btn": "🚀 ELİT METİN OLUŞTUR",
        "upload_label": "📸 Fotoğrafları Buraya Bırakın",
        "result": "💎 Yönetici Önizlemesi",
        "loading": "İlanınız yazılıyor...",
        "empty": "Analiz için görsel bekleniyor.",
        "download": "📥 TXT Olarak İndir",
        "save_btn": "💾 Kaydet",
        "saved_msg": "✅ Kaydedildi!",
        "error": "Hata:"
    }
}

# --- SESSION STATE ---
if "uretilen_ilan" not in st.session_state: st.session_state.uretilen_ilan = ""
if "prop_type" not in st.session_state: st.session_state.prop_type = "Luxury Apartment"
if "price" not in st.session_state: st.session_state.price = "Price Upon Request"
if "location" not in st.session_state: st.session_state.location = "City Center"
if "tone" not in st.session_state: st.session_state.tone = "Ultra-Luxury"
if "custom_inst" not in st.session_state: st.session_state.custom_inst = ""
if "target_lang_input" not in st.session_state: st.session_state.target_lang_input = "English"

# --- CSS (PRO UI & CLEAN LOGO) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
        @import url('https://fonts.googleapis.com/icon?family=Material+Icons');

        html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; }

        .stApp { 
            background-color: #f8fafc;
            background-image: radial-gradient(#cbd5e1 0.5px, transparent 0.5px);
            background-size: 24px 24px;
        }

        .block-container {
            background: white;
            padding: 3rem !important;
            border-radius: 20px;
            box-shadow: 0 15px 45px rgba(0,0,0,0.04);
            margin-top: 2rem;
            border: 1px solid #e2e8f0;
        }

        /* LOGO FULLSCREEN BUTONUNU KALDIRMA */
        button[title="View fullscreen"] {
            display: none !important;
        }
        
        /* Akıllı İmleç */
        button, [data-testid="stFileUploadDropzone"], select, label, 
        .stSelectbox div, .stDownloadButton, div[role="button"] {
            cursor: pointer !important;
        }
        input, textarea, .stTextInput div input, .stTextArea div textarea {
            cursor: text !important;
        }

        /* İkon Fix */
        span[data-testid="stIconMaterial"] {
            font-family: 'Material Icons' !important;
        }

        /* Başlıklar */
        h1 { color: #0f172a !important; font-weight: 800 !important; text-align: center; margin-bottom: 5px; }
        .service-text { text-align: center; color: #1e293b; font-weight: 600; font-size: 1.2rem; margin-bottom: 5px; }
        .subtitle-text { text-align: center; color: #64748b; font-size: 1rem; margin-bottom: 2rem; }

        [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }

        .stButton>button { 
            background: #0f172a; color: white !important; border: none; border-radius: 10px;
            padding: 14px; font-weight: 600; width: 100%; transition: 0.3s;
        }
        .stButton>button:hover { background: #334155; transform: translateY(-1px); }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    logo_img = load_logo("Salija_AI_Transparent_Logo.png")
    if logo_img: st.image(logo_img, use_container_width=True)
    else: st.markdown("<h2 style='text-align:center; color:#0f172a;'>SALIJA AI</h2>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    current_ui_lang = st.selectbox("🌐 Interface", list(ui_languages.keys()), index=0)
    t = ui_languages[current_ui_lang]
    
    st.markdown("---")
    st.header(t["settings"])
    
    st.session_state.target_lang_input = st.text_input(t["target_lang"], value=st.session_state.target_lang_input)
    st.session_state.prop_type = st.text_input(t["prop_type"], value=st.session_state.prop_type)
    st.session_state.price = st.text_input(t["price"], value=st.session_state.price)
    st.session_state.location = st.text_input(t["location"], value=st.session_state.location)
    
    current_tone_idx = t["tones"].index(st.session_state.tone) if st.session_state.tone in t["tones"] else 0
    st.session_state.tone = st.selectbox(t["tone"], t["tones"], index=current_tone_idx)
    st.session_state.custom_inst = st.text_area(t["custom_inst"], value=st.session_state.custom_inst, placeholder=t["custom_inst_ph"])

# --- ANA EKRAN ---
st.markdown(f"<h1>🏢 {t['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='service-text'>{t['service_desc']}</p>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle-text'>{t['subtitle']}</p>", unsafe_allow_html=True)

uploaded_files = st.file_uploader(t["upload_label"], type=["jpg", "png", "webp", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    cols = st.columns(4)
    images_for_ai = []
    for i, file in enumerate(uploaded_files):
        img = Image.open(file)
        images_for_ai.append(img)
        with cols[i % 4]: st.image(img, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(t["btn"]):
        with st.spinner(t["loading"]):
            expert_prompt = f"""
            System: Elite Real Estate Marketer.
            Task: Write a high-conversion listing in {st.session_state.target_lang_input}.
            Strategy: {st.session_state.tone}.
            Details: {st.session_state.prop_type}, {st.session_state.location}, Price: {st.session_state.price}.
            Notes: {st.session_state.custom_inst}
            Requirements: headline, lifestyle story, features, CTA.
            """
            try:
                response = model.generate_content([expert_prompt] + images_for_ai)
                st.session_state.uretilen_ilan = response.text
            except Exception as e:
                st.error(f"{t['error']} {e}")

    if st.session_state.uretilen_ilan:
        st.markdown("---")
        st.subheader(t["result"])
        final_edit = st.text_area("Editor", st.session_state.uretilen_ilan, height=450, label_visibility="collapsed")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button(t["save_btn"]):
                st.session_state.uretilen_ilan = final_edit
                st.success(t["saved_msg"])
        with c2:
            st.download_button(t["download"], data=st.session_state.uretilen_ilan, file_name="salija_ai_listing.txt")
else:

    st.info(t["empty"])

