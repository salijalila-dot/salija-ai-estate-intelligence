import streamlit as st 
from PIL import Image 
import google.generativeai as genai 
import os 

# --- MERKEZİ AYARLAR ---
BRAND_NAME = "SarSa AI"
LOGO_FILE = "SarSa_Logo_Transparent.png" 

# --- AI YAPILANDIRMASI --- 
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"] 
genai.configure(api_key=GOOGLE_API_KEY) 
MODEL_NAME = 'gemini-2.5-flash'  
model = genai.GenerativeModel(MODEL_NAME) 

# --- SAYFA AYARLARI --- 
st.set_page_config(page_title=f"{BRAND_NAME} | Estate Intelligence", page_icon="🏢", layout="wide") 

# --- LOGO YÜKLEME --- 
@st.cache_data 
def load_logo(file_path): 
    if os.path.exists(file_path): return Image.open(file_path) 
    return None 

# --- GLOBAL DİL SİSTEMİ --- 
ui_languages = { 
    "English": { 
        "title": f"{BRAND_NAME} | Estate Intelligence", "service_desc": "AI-Powered Visual Property Analysis", 
        "settings": "⚙️ Configuration", "target_lang": "✍️ Write Listing In...", "prop_type": "Property Type", "price": "Market Price", "location": "Location", "tone": "Strategy",
        "tones": ["Ultra-Luxury", "Investment Potential", "Modern Minimalist", "Family Comfort", "Standard Pro"],
        "custom_inst": "📝 Special Notes", "btn": f"🚀 {BRAND_NAME} GENERATE", "upload_label": "📸 Drop Photos Here",
        "loading": "Architecting...", "empty": "Awaiting visuals.", "download": "📥 Export All", "download_tab": "📥 Download Section",
        "tab_main": "📝 Listing", "tab_social": "📱 Social", "tab_video": "🎬 Video", "tab_tech": "⚙️ Specs", "error": "Error:"
    }, 
    "Türkçe": { 
        "title": f"{BRAND_NAME} | Emlak Zekası", "service_desc": "Yapay Zeka Destekli Görsel Analiz", 
        "settings": "⚙️ Yapılandırma", "target_lang": "✍️ İlan Yazım Dili...", "prop_type": "Emlak Tipi", "price": "Pazar Fiyatı", "location": "Konum", "tone": "Strateji",
        "tones": ["Ultra-Lüks", "Yatırım Potansiyeli", "Modern Minimalist", "Aile Konforu", "Standart Profesyonel"],
        "custom_inst": "📝 Özel Notlar", "btn": f"🚀 {BRAND_NAME} OLUŞTUR", "upload_label": "📸 Fotoğrafları Buraya Bırakın",
        "loading": "İlanınız yazılıyor...", "empty": "Görsel bekleniyor.", "download": "📥 Tümünü İndir", "download_tab": "📥 Bölümü İndir",
        "tab_main": "📝 İlan", "tab_social": "📱 Sosyal", "tab_video": "🎬 Video", "tab_tech": "⚙️ Teknik", "error": "Hata:"
    }
} 

# --- SESSION STATE --- 
for key, val in [("uretilen_ilan", ""), ("target_lang_input", "English")]:
    if key not in st.session_state: st.session_state[key] = val

# --- TASARIM VE İMLEÇ DÜZELTMELERİ (CSS) --- 
st.markdown(f""" 
    <style> 
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap'); 
        html, body, [class*="st-"] {{ font-family: 'Plus Jakarta Sans', sans-serif; }} 
        .stApp {{ background-color: #f8fafc; }} 
        
        /* 🎯 1. SIDEBAR OKU SABİTLEME VE TEMİZLEME */
        [data-testid="stSidebarCollapseButton"] {{
            position: absolute !important;
            top: 10px !important;
            right: 0px !important;
        }}
        span[data-testid="stIconMaterial"] {{
            visibility: hidden !important;
        }}
        span[data-testid="stIconMaterial"]::before {{
            content: "➡️" !important;
            visibility: visible !important;
            font-size: 22px !important;
            display: block !important;
            color: #0f172a !important;
            cursor: pointer !important;
        }}
        [data-testid="stSidebar"][aria-expanded="true"] ~ section span[data-testid="stIconMaterial"]::before {{
            content: "⬅️" !important;
        }}

        /* 🎯 2. İMLEÇ (CURSOR) AYARLARI */
        /* Seçim kutuları (Selectbox) ve Butonlar -> El İşareti */
        .stSelectbox, .stButton, button, [data-testid="stMarkdownContainer"] a, .stDownloadButton {{
            cursor: pointer !important;
        }}
        div[data-baseweb="select"] {{
            cursor: pointer !important;
        }}
        
        /* Yazı alanları (Input/TextArea) -> Yazı İmleci */
        .stTextInput input, .stTextArea textarea {{
            cursor: text !important;
        }}

        /* 🎯 3. GENEL GÖRSEL İYİLEŞTİRME */
        .block-container {{ background: white; padding: 3rem !important; border-radius: 20px; box-shadow: 0 15px 45px rgba(0,0,0,0.04); margin-top: 2rem; border: 1px solid #e2e8f0; }} 
        h1 {{ color: #0f172a !important; font-weight: 800 !important; text-align: center; }} 
        .stButton>button {{ background: #0f172a; color: white !important; border-radius: 10px; width: 100%; height: 3.5rem; font-weight: 600; }}
    </style> 
""", unsafe_allow_html=True) 

# --- SIDEBAR --- 
with st.sidebar: 
    logo_img = load_logo(LOGO_FILE) 
    if logo_img: st.image(logo_img, use_container_width=True) 
    else: st.markdown(f"<h2 style='text-align:center;'>{BRAND_NAME}</h2>", unsafe_allow_html=True) 
     
    current_ui_lang = st.selectbox("🌐 UI Language", list(ui_languages.keys()), index=0)  
    t = ui_languages[current_ui_lang] 
     
    st.markdown("---") 
    st.header(t["settings"]) 
    st.session_state.target_lang_input = st.text_input(t["target_lang"], value=st.session_state.target_lang_input) 
    prop_type = st.text_input(t["prop_type"], value="Luxury Villa") 
    price = st.text_input(t["price"], value="Contact for Price") 
    location = st.text_input(t["location"], value="Global") 
    tone = st.selectbox(t["tone"], t["tones"]) 
    custom_inst = st.text_area(t["custom_inst"]) 

# --- ANA EKRAN --- 
st.markdown(f"<h1>🏢 {t['title']}</h1>", unsafe_allow_html=True) 
st.markdown(f"<p style='text-align:center; font-weight:600; font-size:1.1rem;'>{t['service_desc']}</p>", unsafe_allow_html=True) 

uploaded_files = st.file_uploader(t["upload_label"], type=["jpg", "png", "webp", "jpeg"], accept_multiple_files=True) 

if uploaded_files: 
    images_for_ai = [Image.open(f) for f in uploaded_files] 
    st.image(images_for_ai, width=150)

    if st.button(t["btn"]): 
        with st.spinner(t["loading"]): 
            expert_prompt = f"Role: Senior Architect & PropTech Copywriter for {BRAND_NAME}. Task: Analyze property photos and create marketing suite. Language: {st.session_state.target_lang_input}. Location: {location}. Tone: {tone}. Format: ## SECTION_1 (Narrative), ## SECTION_2 (Social), ## SECTION_3 (Video), ## SECTION_4 (Technical)."
            try: 
                response = model.generate_content([expert_prompt] + images_for_ai) 
                st.session_state.uretilen_ilan = response.text 
            except Exception as e: 
                st.error(f"{t['error']} {e}") 

    if st.session_state.uretilen_ilan: 
        raw_text = st.session_state.uretilen_ilan 
        parts = raw_text.split("##") 
        sec1 = parts[1].replace("SECTION_1", "").strip() if len(parts) > 1 else raw_text 
        sec2 = parts[2].replace("SECTION_2", "").strip() if len(parts) > 2 else "" 
        sec3 = parts[3].replace("SECTION_3", "").strip() if len(parts) > 3 else "" 
        sec4 = parts[4].replace("SECTION_4", "").strip() if len(parts) > 4 else "" 

        tabs = st.tabs([t["tab_main"], t["tab_social"], t["tab_video"], t["tab_tech"]]) 
        contents = [sec1, sec2, sec3, sec4]
        
        for i, tab in enumerate(tabs):
            with tab:
                st.text_area(f"Edit {i}", value=contents[i], height=400, label_visibility="collapsed")
                st.download_button(t["download_tab"], data=contents[i], file_name=f"part_{i}.txt", key=f"dl_{i}")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.download_button(t["download"], data=raw_text, file_name=f"{BRAND_NAME.lower()}_complete.txt"):
            st.balloons()
else: 
    st.info(t["empty"])
