import streamlit as st 
from PIL import Image 
import google.generativeai as genai 
import os 
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

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

# --- PROFESYONEL PDF OLUŞTURUCU ---
def create_pdf(content_dict, metadata):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    p.setFont("Helvetica-Bold", 20)
    p.drawString(50, height - 50, "SarSa AI | Property Intelligence Report")
    p.line(50, height - 60, width - 50, height - 60)
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, height - 80, f"Location: {metadata.get('loc', 'N/A')} | Price: {metadata.get('price', 'N/A')}")
    y = height - 110
    for section, text in content_dict.items():
        if not text: continue
        p.setFont("Helvetica-Bold", 12); p.drawString(50, y, section.upper()); y -= 20
        p.setFont("Helvetica", 9)
        for line in text.split('\n'):
            if y < 50: p.showPage(); y = height - 50
            p.drawString(60, y, line[:100]); y -= 12
        y -= 10
    p.save(); buffer.seek(0)
    return buffer

# --- GLOBAL DİL SİSTEMİ (EKSİKSİZ LİSTE) --- 
ui_languages = { 
    "English": {"title": "SarSa AI | Analysis", "settings": "⚙️ Configuration", "target_lang": "✍️ Output Lang", "prop_type": "Type", "price": "Price", "location": "Location", "tone": "Strategy", "tones": ["Standard Pro", "Luxury", "Investment"], "btn": "🚀 GENERATE", "upload_label": "📸 Photos", "empty": "Awaiting visuals.", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 Copy", "saved_msg": "✅ Copied!", "tab_main": "📝 Listing", "tab_social": "📱 Social", "tab_video": "🎬 Video", "tab_tech": "⚙️ Tech", "tab_invest": "📊 Invest", "tab_seo": "🔍 SEO"}, 
    "Türkçe": {"title": "SarSa AI | Analiz", "settings": "⚙️ Yapılandırma", "target_lang": "✍️ Yazım Dili", "prop_type": "Tip", "price": "Fiyat", "location": "Konum", "tone": "Strateji", "tones": ["Standart Pro", "Lüks", "Yatırım"], "btn": "🚀 OLUŞTUR", "upload_label": "📸 Fotoğraf", "empty": "Görsel bekleniyor.", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 Kopyala", "saved_msg": "✅ Kopyalandı!", "tab_main": "📝 İlan", "tab_social": "📱 Sosyal", "tab_video": "🎬 Video", "tab_tech": "⚙️ Teknik", "tab_invest": "📊 Yatırım", "tab_seo": "🔍 SEO"},
    "Español": {"title": "SarSa AI | Análisis", "settings": "⚙️ Configuración", "target_lang": "✍️ Idioma", "prop_type": "Tipo", "price": "Precio", "location": "Ubicación", "tone": "Estrategia", "tones": ["Estándar", "Lujo", "Inversión"], "btn": "🚀 GENERAR", "upload_label": "📸 Fotos", "empty": "Esperando.", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 Copiar", "saved_msg": "✅ ¡Copiado!", "tab_main": "📝 Anuncio", "tab_social": "📱 Social", "tab_video": "🎬 Video", "tab_tech": "⚙️ Técnica", "tab_invest": "📊 Inversión", "tab_seo": "🔍 SEO"},
    "Deutsch": {"title": "SarSa AI | Analyse", "settings": "⚙️ Konfiguration", "target_lang": "✍️ Sprache", "prop_type": "Typ", "price": "Preis", "location": "Standort", "tone": "Strategie", "tones": ["Standard", "Luxus", "Invest"], "btn": "🚀 ERSTELLEN", "upload_label": "📸 Fotos", "empty": "Warten.", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 Kopieren", "saved_msg": "✅ Kopiert!", "tab_main": "📝 Exposé", "tab_social": "📱 Social", "tab_video": "🎬 Video", "tab_tech": "⚙️ Tech", "tab_invest": "📊 Invest", "tab_seo": "🔍 SEO"},
    "Français": {"title": "SarSa AI | Analyse", "settings": "⚙️ Configuration", "target_lang": "✍️ Langue", "prop_type": "Type", "price": "Prix", "location": "Lieu", "tone": "Stratégie", "tones": ["Standard", "Luxe", "Invest"], "btn": "🚀 GÉNÉRER", "upload_label": "📸 Photos", "empty": "En attente.", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 Copier", "saved_msg": "✅ Copié!", "tab_main": "📝 Annonce", "tab_social": "📱 Social", "tab_video": "🎬 Vidéo", "tab_tech": "⚙️ Tech", "tab_invest": "📊 Invest", "tab_seo": "🔍 SEO"},
    "Português": {"title": "SarSa AI | Análise", "settings": "⚙️ Configuração", "target_lang": "✍️ Idioma", "prop_type": "Tipo", "price": "Preço", "location": "Local", "tone": "Estratégia", "tones": ["Padrão", "Luxo", "Investimento"], "btn": "🚀 GERAR", "upload_label": "📸 Fotos", "empty": "Aguardando.", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 Copiar", "saved_msg": "✅ Copiado!", "tab_main": "📝 Anúncio", "tab_social": "📱 Social", "tab_video": "🎬 Vídeo", "tab_tech": "⚙️ Detalhes", "tab_invest": "📊 Invest", "tab_seo": "🔍 SEO"},
    "日本語": {"title": "SarSa AI | 分析", "settings": "⚙️ 設定", "target_lang": "✍️ 言語", "prop_type": "種類", "price": "価格", "location": "場所", "tone": "戦略", "tones": ["標準", "高級", "投資"], "btn": "🚀 生成する", "upload_label": "📸 写真アップ", "empty": "待機中。", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 コピー", "saved_msg": "✅ 完了", "tab_main": "📝 広告", "tab_social": "📱 SNS", "tab_video": "🎬 動画", "tab_tech": "⚙️ 仕様", "tab_invest": "📊 投資", "tab_seo": "🔍 SEO"},
    "中文": {"title": "SarSa AI | 分析", "settings": "⚙️ 配置", "target_lang": "✍️ 语言", "prop_type": "类型", "price": "价格", "location": "地点", "tone": "策略", "tones": ["标准", "豪宅", "投资"], "btn": "🚀 生成", "upload_label": "📸 上传照片", "empty": "等待中。", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 复制", "saved_msg": "✅ 已复制", "tab_main": "📝 房源", "tab_social": "📱 社交", "tab_video": "🎬 视频", "tab_tech": "⚙️ 技术", "tab_invest": "📊 投资", "tab_seo": "🔍 SEO"},
    "العربية": {"title": "SarSa AI | تحليل", "settings": "⚙️ الإعدادات", "target_lang": "✍️ لغة الكتابة", "prop_type": "النوع", "price": "السعر", "location": "الموقع", "tone": "الاستراتيجية", "tones": ["قياسي", "فخم", "استثمار"], "btn": "🚀 إنشاء", "upload_label": "📸 تحميل صور", "empty": "في الانتظار.", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 نسخ", "saved_msg": "✅ تم النسخ!", "tab_main": "📝 إعلان", "tab_social": "📱 تواصل", "tab_video": "🎬 فيديو", "tab_tech": "⚙️ تقني", "tab_invest": "📊 استثمار", "tab_seo": "🔍 SEO"}
}

# --- CSS (POINTER & SIDEBAR KORUMASI) --- 
st.markdown(""" 
    <style> 
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap'); 
        html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; } 
        button, .stButton>button, [role="button"], .stSelectbox, .stTextInput, .stTextArea, .stTabs [data-baseweb="tab"] { cursor: pointer !important; } 
        .stButton>button { background: #0f172a; color: white !important; border-radius: 10px; padding: 12px; font-weight: 600; width: 100%; border: none; transition: 0.3s; }
        .stButton>button:hover { background: #1e293b; transform: translateY(-2px); } 
        .stTabs [aria-selected="true"] { background-color: #0f172a !important; color: white !important; border-radius: 8px 8px 0 0; }
    </style> 
""", unsafe_allow_html=True) 

# --- SESSION STATE --- 
for key, val in [("uretilen_ilan", ""), ("prop_type", ""), ("price", ""), ("location", ""), ("tone", "Standard Pro"), ("target_lang_input", "English")]:
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

# --- ANA EKRAN --- 
st.markdown(f"<h1 style='text-align:center;'>🏢 {t['title']}</h1>", unsafe_allow_html=True) 
uploaded_files = st.file_uploader(t["upload_label"], type=["jpg", "png", "webp", "jpeg"], accept_multiple_files=True) 

if uploaded_files: 
    cols = st.columns(4) 
    images_for_ai = [Image.open(f) for f in uploaded_files] 
    for i, img in enumerate(images_for_ai): 
        with cols[i % 4]: st.image(img, use_container_width=True) 

    if st.button(t["btn"]): 
        with st.spinner(t["loading"]): 
            prompt = (f"Pro Estate Strategist. Lang: {st.session_state.target_lang_input}. Type: {st.session_state.prop_type}. Loc: {st.session_state.location}. Price: {st.session_state.price}. Tone: {st.session_state.tone}. "
                     f"Sections: ## SEC_1 (Listing), ## SEC_2 (Social), ## SEC_3 (Video), ## SEC_4 (Tech), ## SEC_5 (Invest Score), ## SEC_6 (SEO).")
            response = model.generate_content([prompt] + images_for_ai) 
            st.session_state.uretilen_ilan = response.text 

    if st.session_state.uretilen_ilan: 
        raw = st.session_state.uretilen_ilan 
        parts = raw.split("##") 
        content_map = {}
        tab_titles = [t["tab_main"], t["tab_social"], t["tab_video"], t["tab_tech"], t["tab_invest"], t["tab_seo"]]
        tabs = st.tabs(tab_titles) 
        for i, tab in enumerate(tabs):
            with tab:
                sec_text = parts[i+1].split(":", 1)[-1].strip() if len(parts) > i+1 else raw
                content_map[tab_titles[i]] = sec_text
                st.text_area("Edit", value=sec_text, height=300, key=f"ed_{i}")
                if st.button(t["copy_btn"], key=f"cp_{i}"): st.toast(t["saved_msg"])

        c1, c2 = st.columns(2)
        with c1: st.download_button(t["download"], data=raw, file_name="sarsa_export.txt")
        with c2: st.download_button(t["pdf_btn"], data=create_pdf(content_map, {"loc": st.session_state.location, "price": st.session_state.price}), file_name="SarSa_Report.pdf")
else: st.info(t["empty"])
