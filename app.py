import streamlit as st
from PIL import Image
import google.generativeai as genai
import os

# --- AI YAPILANDIRMASI ---
# API Anahtarını sistemden gizli olarak alıyoruz
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
MODEL_NAME = 'gemini-2.5-flash' 
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
        "loading": "Architecting your marketing kit...",
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
        "loading": "Pazarlama paketiniz hazırlanıyor...",
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
if "price" not in st.session_state: st.session_state.price = "14.000.000 TL"
if "location" not in st.session_state: st.session_state.location = "City Center"
if "tone" not in st.session_state: st.session_state.tone = "Ultra-Luxury"
if "custom_inst" not in st.session_state: st.session_state.custom_inst = ""
if "target_lang_input" not in st.session_state: st.session_state.target_lang_input = "Türkçe"

# --- CSS ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
        html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; }
        .stApp { background-color: #f8fafc; }
        .block-container { background: white; padding: 3rem !important; border-radius: 20px; box-shadow: 0 15px 45px rgba(0,0,0,0.04); margin-top: 2rem; border: 1px solid #e2e8f0; }
        h1 { color: #0f172a !important; font-weight: 800 !important; text-align: center; }
        .service-text { text-align: center; color: #1e293b; font-weight: 600; font-size: 1.2rem; }
        .subtitle-text { text-align: center; color: #64748b; font-size: 1rem; margin-bottom: 2rem; }
        .stButton>button { background: #0f172a; color: white !important; border-radius: 10px; padding: 14px; font-weight: 600; width: 100%; }
        /* Sekme başlıklarını güzelleştirme */
        .stTabs [data-baseweb="tab-list"] { gap: 24px; }
        .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f1f5f9; border-radius: 10px 10px 0 0; padding: 10px 20px; }
        .stTabs [aria-selected="true"] { background-color: #0f172a !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    logo_img = load_logo("Salija_AI_Transparent_Logo.png")
    if logo_img: st.image(logo_img, use_container_width=True)
    else: st.markdown("<h2 style='text-align:center; color:#0f172a;'>SALIJA AI</h2>", unsafe_allow_html=True)
    
    current_ui_lang = st.selectbox("🌐 Interface", list(ui_languages.keys()), index=1)
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

    if st.button(t["btn"]):
        with st.spinner(t["loading"]):
            expert_prompt = f"""
            System: Elite Real Estate Marketer.
            Task: Create a COMPLETE marketing kit in {st.session_state.target_lang_input}.
            Strategy: {st.session_state.tone}.
            Details: {st.session_state.prop_type}, {st.session_state.location}, Price: {st.session_state.price}.
            Notes: {st.session_state.custom_inst}
            
            Strictly provide the output in this format:
            ## SECTION_1
            [Detailed Listing Description]
            ## SECTION_2
            [Social Media Post with hashtags]
            ## SECTION_3
            [Video Script]
            """
            try:
                response = model.generate_content([expert_prompt] + images_for_ai)
                st.session_state.uretilen_ilan = response.text
            except Exception as e:
                st.error(f"{t['error']} {e}")

    if st.session_state.uretilen_ilan:
        st.markdown("---")
        st.subheader(t["result"])
        
        # Parçalara ayırma
        raw_text = st.session_state.uretilen_ilan
        parts = raw_text.split("##")
        
        sec1, sec2, sec3 = "", "", ""
        for p in parts:
            if "SECTION_1" in p: sec1 = p.replace("SECTION_1", "").strip()
            elif "SECTION_2" in p: sec2 = p.replace("SECTION_2", "").strip()
            elif "SECTION_3" in p: sec3 = p.replace("SECTION_3", "").strip()

        # Sekmeli Görünüm
        tab1, tab2, tab3 = st.tabs(["📝 Ana İlan", "📱 Sosyal Medya", "🎬 Video Senaryosu"])
        
        with tab1:
            res_ana = st.text_area("İlan Metni", value=sec1 if sec1 else raw_text, height=400)
        with tab2:
            res_sosyal = st.text_area("Sosyal Medya", value=sec2, height=400)
        with tab3:
            res_video = st.text_area("Video Script", value=sec3, height=400)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button(t["save_btn"]):
                st.session_state.uretilen_ilan = f"## SECTION_1\n{res_ana}\n\n## SECTION_2\n{res_sosyal}\n\n## SECTION_3\n{res_video}"
                st.success(t["saved_msg"])
        with c2:
            st.download_button(t["download"], data=st.session_state.uretilen_ilan, file_name="salija_ai_kit.txt")
else:
    st.info(t["empty"])
