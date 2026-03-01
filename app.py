import streamlit as st 
from PIL import Image 
import google.generativeai as genai 
import os 

# --- AI YAPILANDIRMASI --- 
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"] 
genai.configure(api_key=GOOGLE_API_KEY) 
MODEL_NAME = 'gemini-2.5-flash'  
model = genai.GenerativeModel(MODEL_NAME) 

# --- SAYFA AYARLARI --- 
st.set_page_config(page_title="SarSa AI | Estate Intelligence", page_icon="🏢", layout="wide") 

# --- HIZLANDIRICI --- 
@st.cache_data 
def load_logo(file_path): 
    if os.path.exists(file_path): return Image.open(file_path) 
    return None 

# --- GLOBAL DİL SİSTEMİ (SARSA AI GÜNCEL) --- 
ui_languages = { 
    "English": { 
        "title": "SarSa AI | Estate Intelligence", "service_desc": "AI-Powered Visual Property Analysis & Copywriting Engine", "subtitle": "Convert property visuals into high-conversion marketing masterpieces.",
        "settings": "⚙️ Configuration", "target_lang": "✍️ Write Listing In...", "prop_type": "Property Type", "price": "Market Price", "location": "Location", "tone": "Strategy",
        "tones": ["Ultra-Luxury", "Investment Potential", "Modern Minimalist", "Family Comfort", "Standard Pro"],
        "custom_inst": "📝 Special Notes", "custom_inst_ph": "E.g., High ceilings, near metro...", "btn": "🚀 GENERATE ELITE COPY", "upload_label": "📸 Drop Property Photos Here",
        "result": "💎 Executive Preview", "loading": "Architecting your listing...", "empty": "Awaiting visuals to start analysis.", "download": "📥 Export TXT", "save_btn": "💾 Save Changes", "saved_msg": "✅ Saved!", "error": "Error:",
        "tab_main": "📝 Main Listing", "tab_social": "📱 Social Media", "tab_video": "🎬 Video", "tab_tech": "⚙️ Technical Details", "label_main": "Marketing Copy", "label_social": "Social Media Content", "label_video": "Video Script", "label_tech": "Technical Specs"
    }, 
    "Türkçe": { 
        "title": "SarSa AI | Emlak Zekası", "service_desc": "Yapay Zeka Destekli Görsel Mülk Analizi ve İlan Yazım Motoru", "subtitle": "Mülk görsellerini yüksek dönüşümlü pazarlama şaheserlerine dönüştürün.",
        "settings": "⚙️ Yapılandırma", "target_lang": "✍️ İlan Yazım Dili...", "prop_type": "Emlak Tipi", "price": "Pazar Fiyatı", "location": "Konum", "tone": "Strateji",
        "tones": ["Ultra-Lüks", "Yatırım Potansiyeli", "Modern Minimalist", "Aile Konforu", "Standart Profesyonel"],
        "custom_inst": "📝 Özel Notlar", "custom_inst_ph": "Örn: Yüksek tavanlar, metroya yakın...", "btn": "🚀 ELİT METİN OLUŞTUR", "upload_label": "📸 Fotoğrafları Buraya Bırakın",
        "result": "💎 Yönetici Önizlemesi", "loading": "İlanınız yazılıyor...", "empty": "Analiz için görsel bekleniyor.", "download": "📥 TXT Olarak İndir", "save_btn": "💾 Kaydet", "saved_msg": "✅ Kaydedildi!", "error": "Hata:",
        "tab_main": "📝 Ana İlan", "tab_social": "📱 Sosyal Medya", "tab_video": "🎬 Video", "tab_tech": "⚙️ Teknik Detay", "label_main": "Pazarlama Metni", "label_social": "Sosyal Medya", "label_video": "Video Script", "label_tech": "Teknik Özellikler"
    }
} 

# --- SESSION STATE --- 
for key, val in [("uretilen_ilan", ""), ("prop_type", "Luxury Villa"), ("price", "Contact for Price"), ("location", "Global"), ("tone", "Ultra-Luxury"), ("custom_inst", ""), ("target_lang_input", "English")]:
    if key not in st.session_state: st.session_state[key] = val

# --- CSS (ÖZEL İKON VE İMLEÇ AYARLARI) --- 
st.markdown(""" 
    <style> 
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap'); 
        html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; } 
        .stApp { background-color: #f8fafc; } 
        
        div[data-testid="stInputInstructions"] { display: none !important; }

        .block-container { background: white; padding: 3rem !important; border-radius: 20px; box-shadow: 0 15px 45px rgba(0,0,0,0.04); margin-top: 2rem; border: 1px solid #e2e8f0; } 
        h1 { color: #0f172a !important; font-weight: 800 !important; text-align: center; } 
         
        /* İMLEÇ AYARLARI */
        div[data-baseweb="select"], div[data-baseweb="select"] > div, button, [data-baseweb="tab"], [data-testid="stFileUploader"] { cursor: pointer !important; }
        [data-testid="stSidebar"] input, [data-testid="stSidebar"] textarea, .stTextArea textarea { cursor: text !important; }

        /* SIDEBAR OKU */
        span[data-testid="stIconMaterial"] { font-size: 0px !important; color: transparent !important; }
        span[data-testid="stIconMaterial"]::before { content: "⬅️" !important; font-size: 18px !important; color: #0f172a !important; visibility: visible !important; display: block !important; cursor: pointer !important; }

        [data-testid="stSidebarCollapseButton"] { background-color: #f1f5f9 !important; border-radius: 8px !important; cursor: pointer !important; }
        .stButton>button { background: #0f172a; color: white !important; border-radius: 10px; padding: 14px; font-weight: 600; width: 100%; }
        
        .stTabs [aria-selected="true"] { background-color: #0f172a !important; color: white !important; }
    </style> 
""", unsafe_allow_html=True) 

# --- SIDEBAR --- 
with st.sidebar: 
    logo_img = load_logo("SarSa_Logo_Transparent.png") 
    if logo_img: st.image(logo_img, use_container_width=True) 
    else: st.markdown("<h2 style='text-align:center; color:#0f172a;'>SARSA AI</h2>", unsafe_allow_html=True) 
     
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
st.markdown(f"<p style='text-align:center; color:#1e293b; font-weight:600; font-size:1.2rem;'>{t['service_desc']}</p>", unsafe_allow_html=True) 
st.markdown(f"<p style='text-align:center; color:#64748b; font-size:1rem; margin-bottom:2rem;'>{t['subtitle']}</p>", unsafe_allow_html=True) 

uploaded_files = st.file_uploader(t["upload_label"], type=["jpg", "png", "webp", "jpeg"], accept_multiple_files=True) 

if uploaded_files: 
    cols = st.columns(4) 
    images_for_ai = [Image.open(f) for f in uploaded_files] 
    for i, img in enumerate(images_for_ai): 
        with cols[i % 4]: st.image(img, use_container_width=True) 

    if st.button(t["btn"]): 
        with st.spinner(t["loading"]): 
            expert_prompt = f"Role: Senior Architect & PropTech Copywriter for SarSa AI. Lang: {st.session_state.target_lang_input}. Context: {st.session_state.prop_type} at {st.session_state.location}. Tone: {st.session_state.tone}. Format: ## SECTION_1, ## SECTION_2, ## SECTION_3, ## SECTION_4."
            try: 
                response = model.generate_content([expert_prompt] + images_for_ai) 
                st.session_state.uretilen_ilan = response.text 
            except Exception as e: 
                st.error(f"{t['error']} {e}") 

    if st.session_state.uretilen_ilan: 
        st.markdown("---") 
        st.subheader(t["result"]) 
        raw_text = st.session_state.uretilen_ilan 
        parts = raw_text.split("##") 
        sec1, sec2, sec3, sec4 = "", "", "", "" 
        for p in parts: 
            if "SECTION_1" in p: sec1 = p.replace("SECTION_1", "").split(":", 1)[-1].strip() 
            elif "SECTION_2" in p: sec2 = p.replace("SECTION_2", "").split(":", 1)[-1].strip() 
            elif "SECTION_3" in p: sec3 = p.replace("SECTION_3", "").split(":", 1)[-1].strip() 
            elif "SECTION_4" in p: sec4 = p.replace("SECTION_4", "").split(":", 1)[-1].strip() 

        tab1, tab2, tab3, tab4 = st.tabs([t["tab_main"], t["tab_social"], t["tab_video"], t["tab_tech"]]) 
        
        with tab1: res_ana = st.text_area(t["label_main"], value=sec1 if sec1 else raw_text, height=400, key="txt_ana") 
        with tab2: res_sosyal = st.text_area(t["label_social"], value=sec2, height=400, key="txt_sosyal") 
        with tab3: res_video = st.text_area(t["label_video"], value=sec3, height=400, key="txt_video") 
        with tab4: res_teknik = st.text_area(t["label_tech"], value=sec4, height=400, key="txt_teknik") 
         
        c1, c2 = st.columns(2) 
        with c1: 
            if st.button(t["save_btn"]): 
                st.session_state.uretilen_ilan = f"## SECTION_1\n{res_ana}\n\n## SECTION_2\n{res_sosyal}\n\n## SECTION_3\n{res_video}\n\n## SECTION_4\n{res_teknik}"
                st.success(t["saved_msg"]) 
        with c2: 
            st.download_button(t["download"], data=st.session_state.uretilen_ilan, file_name="sarsa_ai_kit.txt") 
else: 
    st.info(t["empty"])
