import streamlit as st 
from PIL import Image 
import google.generativeai as genai 
import os 
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# --- AI YAPILANDIRMASI --- 
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"] 
genai.configure(api_key=GOOGLE_API_KEY) 
MODEL_NAME = 'gemini-2.5-flash'  
model = genai.GenerativeModel(MODEL_NAME) 

# --- SAYFA AYARLARI --- 
st.set_page_config(page_title="SarSa AI | Global Estate", page_icon="🏢", layout="wide") 

# --- HIZLANDIRICI --- 
@st.cache_data 
def load_logo(file_path): 
    if os.path.exists(file_path): return Image.open(file_path) 
    return None 

# --- PDF FONKSİYONU ---
def create_pdf(text_content):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "SarSa AI - Professional Property Report")
    p.line(100, 740, 500, 740)
    p.setFont("Helvetica", 10)
    y = 710
    for line in text_content.split('\n'):
        if y < 50: p.showPage(); p.setFont("Helvetica", 10); y = 750
        p.drawString(100, y, line[:90]); y -= 15
    p.save(); buffer.seek(0)
    return buffer

# --- GLOBAL DİL SİSTEMİ --- 
ui_languages = { 
    "English": {"title": "SarSa AI | Analysis", "settings": "⚙️ Configuration", "target_lang": "✍️ Write In...", "prop_type": "Type", "price": "Price", "location": "Location", "tone": "Strategy", "tones": ["Standard Pro", "Ultra-Luxury", "Investment", "Modern", "Family"], "btn": "🚀 GENERATE", "upload_label": "📸 Drop Photos", "empty": "Awaiting visuals.", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 Copy", "saved_msg": "✅ Saved!", "tab_main": "📝 Listing", "tab_social": "📱 Social", "tab_video": "🎬 Video", "tab_tech": "⚙️ Tech"}, 
    "Türkçe": {"title": "SarSa AI | Analiz", "settings": "⚙️ Yapılandırma", "target_lang": "✍️ Yazım Dili...", "prop_type": "Tip", "price": "Fiyat", "location": "Konum", "tone": "Strateji", "tones": ["Standart Profesyonel", "Ultra-Lüks", "Yatırım", "Modern", "Aile"], "btn": "🚀 OLUŞTUR", "upload_label": "📸 Fotoğraf Yükle", "empty": "Görsel bekleniyor.", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 Kopyala", "saved_msg": "✅ Kaydedildi!", "tab_main": "📝 İlan", "tab_social": "📱 Sosyal", "tab_video": "🎬 Video", "tab_tech": "⚙️ Teknik"},
    "Español": {"title": "SarSa AI | Análisis", "settings": "⚙️ Configuración", "target_lang": "✍️ Escribir en...", "prop_type": "Tipo", "price": "Precio", "location": "Ubicación", "tone": "Estrategia", "tones": ["Estándar", "Lujo", "Inversión", "Moderno", "Familiar"], "btn": "🚀 GENERAR", "upload_label": "📸 Subir fotos", "empty": "Esperando imágenes.", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 Copiar", "saved_msg": "✅ ¡Guardado!", "tab_main": "📝 Anuncio", "tab_social": "📱 Social", "tab_video": "🎬 Video", "tab_tech": "⚙️ Técnica"},
    "Deutsch": {"title": "SarSa AI | Analyse", "settings": "⚙️ Konfiguration", "target_lang": "✍️ Sprache...", "prop_type": "Typ", "price": "Preis", "location": "Standort", "tone": "Strategie", "tones": ["Standard", "Luxus", "Investition", "Modern", "Familie"], "btn": "🚀 ERSTELLEN", "upload_label": "📸 Fotos hochladen", "empty": "Warte auf Bilder.", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 Kopieren", "saved_msg": "✅ Gespeichert!", "tab_main": "📝 Exposé", "tab_social": "📱 Social", "tab_video": "🎬 Video", "tab_tech": "⚙️ Tech"},
    "Français": {"title": "SarSa AI | Analyse", "settings": "⚙️ Configuration", "target_lang": "✍️ Langue...", "prop_type": "Type", "price": "Prix", "location": "Lieu", "tone": "Stratégie", "tones": ["Standard", "Luxe", "Investissement", "Moderne", "Famille"], "btn": "🚀 GÉNÉRER", "upload_label": "📸 Photos", "empty": "En attente.", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 Copier", "saved_msg": "✅ Enregistré!", "tab_main": "📝 Annonce", "tab_social": "📱 Social", "tab_video": "🎬 Vidéo", "tab_tech": "⚙️ Tech"},
    "日本語": {"title": "SarSa AI | 分析", "settings": "⚙️ 設定", "target_lang": "✍️ 言語...", "prop_type": "種類", "price": "価格", "location": "場所", "tone": "戦略", "tones": ["標準", "高級", "投資", "モダン", "ファミリー"], "btn": "🚀 生成する", "upload_label": "📸 写真をアップロード", "empty": "待機中。", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 コピー", "saved_msg": "✅ 完了", "tab_main": "📝 広告", "tab_social": "📱 SNS", "tab_video": "🎬 動画", "tab_tech": "⚙️ 仕様"},
    "العربية": {"title": "SarSa AI | تحليل", "settings": "⚙️ الإعدادات", "target_lang": "✍️ لغة الكتابة", "prop_type": "النوع", "price": "السعر", "location": "الموقع", "tone": "الاستراتيجية", "tones": ["قياسي", "فخم", "استثمار", "عصري", "عائلي"], "btn": "🚀 إنشاء", "upload_label": "📸 تحميل الصور", "empty": "في الانتظار.", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 نسخ", "saved_msg": "✅ تم الحفظ!", "tab_main": "📝 إعلان", "tab_social": "📱 تواصل", "tab_video": "🎬 فيديو", "tab_tech": "⚙️ تقني"}
}

# --- CSS (MARKAYA ÖZEL STİL VE PARMAK İMLECİ) --- 
st.markdown(""" 
    <style> 
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap'); 
        html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; } 
        
        button, .stButton>button, [role="button"], .stSelectbox, .stTextInput, .stTextArea { 
            cursor: pointer !important; 
        }

        .stButton>button { 
            background: #0f172a !important; 
            color: white !important; 
            border-radius: 12px !important; 
            padding: 10px 24px !important; 
            transition: all 0.3s ease !important;
            border: none !important;
            width: 100%;
        }

        .stButton>button:hover { 
            background: #1e293b !important; 
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        }

        [data-testid="stSidebar"] .stButton>button {
            background: #f1f5f9 !important;
            color: #0f172a !important;
            border: 1px solid #cbd5e1 !important;
        }
    </style> 
""", unsafe_allow_html=True)

# --- SESSION STATE --- 
for key, val in [("uretilen_ilan", ""), ("prop_type", ""), ("price", ""), ("location", ""), ("tone", "Standard Pro"), ("custom_inst", ""), ("target_lang_input", "English")]:
    if key not in st.session_state: st.session_state[key] = val

# --- SIDEBAR --- 
with st.sidebar: 
    logo_img = load_logo("SarSa_Logo_Transparent.png") 
    if logo_img: st.image(logo_img, use_container_width=True) 
    else: st.header("SARSA AI") 
      
    current_ui_lang = st.selectbox("🌐 Interface Language", list(ui_languages.keys()))   
    t = ui_languages[current_ui_lang] 
      
    st.markdown("---") 
    st.header(t["settings"]) 
    st.session_state.target_lang_input = st.text_input(t["target_lang"], value=st.session_state.target_lang_input) 
    st.session_state.prop_type = st.text_input(t["prop_type"], value=st.session_state.prop_type) 
    st.session_state.price = st.text_input(t["price"], value=st.session_state.price) 
    st.session_state.location = st.text_input(t["location"], value=st.session_state.location) 
    st.session_state.tone = st.selectbox(t["tone"], t["tones"]) 
    st.session_state.custom_inst = st.text_area("Notes", value=st.session_state.custom_inst) 

# --- ANA EKRAN --- 
st.markdown(f"<h1 style='text-align:center;'>🏢 {t['title']}</h1>", unsafe_allow_html=True) 
uploaded_files = st.file_uploader(t["upload_label"], type=["jpg", "png", "webp", "jpeg"], accept_multiple_files=True) 

if uploaded_files: 
    cols = st.columns(min(len(uploaded_files), 4)) 
    images_for_ai = [Image.open(f) for f in uploaded_files] 
    for i, img in enumerate(images_for_ai): 
        with cols[i % 4]: st.image(img, use_container_width=True) 

    if st.button(t["btn"]): 
        with st.spinner("Processing..."): 
            prompt = f"Analyze photos. Language: {st.session_state.target_lang_input}. Strategy: {st.session_state.tone}. Sections: ## SECTION_1 (Listing), ## SECTION_2 (Social), ## SECTION_3 (Video), ## SECTION_4 (Tech)."
            try:
                response = model.generate_content([prompt] + images_for_ai) 
                st.session_state.uretilen_ilan = response.text 
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state.uretilen_ilan: 
        raw = st.session_state.uretilen_ilan 
        parts = raw.split("##")
        tabs = st.tabs([t["tab_main"], t["tab_social"], t["tab_video"], t["tab_tech"]]) 
        for i, tab in enumerate(tabs):
            with tab:
                content = parts[i+1] if len(parts) > i+1 else raw
                st.text_area("Content", value=content, height=300, key=f"t_{i}")
                if st.button(t["copy_btn"], key=f"c_{i}"): st.toast(t["saved_msg"])

        c1, c2 = st.columns(2)
        with c1: st.download_button(t["download"], data=raw, file_name="sarsa_ai.txt")
        with c2: st.download_button(t["pdf_btn"], data=create_pdf(raw), file_name="sarsa_ai.pdf")
else: 
    st.info(t["empty"])
