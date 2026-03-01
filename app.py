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
st.set_page_config(page_title="SarSa AI | Real Estate Analysis & Marketing Engine", page_icon="🏢", layout="wide") 

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

# --- GLOBAL DİL SİSTEMİ (TÜM AÇIKLAMALAR VE DİLLER GERİ GELDİ) --- 
ui_languages = { 
    "English": { 
        "title": "SarSa AI | Real Estate Analysis & Marketing Engine", 
        "service_desc": "All-in-One Visual Property Intelligence & Global Sales Automation", 
        "subtitle": "Transform property photos into premium listings, social media kits, cinematic video scripts, and technical data sheets instantly.",
        "settings": "⚙️ Configuration", "target_lang": "✍️ Write Listing In...", "prop_type": "Property Type", "price": "Market Price", "location": "Location", "tone": "Strategy",
        "tones": ["Standard Pro", "Ultra-Luxury", "Investment Potential", "Modern Minimalist", "Family Comfort"],
        "ph_prop": "E.g., 3+1 Apartment...", "ph_price": "E.g., $500,000...", "ph_loc": "E.g., Manhattan, NY...",
        "custom_inst": "📝 Special Notes", "custom_inst_ph": "E.g., High ceilings...", "btn": "🚀 GENERATE COMPLETE MARKETING ASSETS", "upload_label": "📸 Drop Property Photos Here",
        "result": "💎 Executive Preview", "loading": "Crafting your premium marketing ecosystem...", "empty": "Awaiting visuals to start professional analysis.", "download": "📥 Export TXT", "pdf_btn": "📄 PDF Report", "copy_btn": "📋 Copy", "saved_msg": "✅ Copied!", 
        "tab_main": "📝 Prime Listing", "tab_social": "📱 Social Media Kit", "tab_video": "🎬 Video Scripts", "tab_tech": "⚙️ Technical Specs", "tab_invest": "📊 Invest Score", "tab_seo": "🔍 SEO Pro"
    }, 
    "Türkçe": { 
        "title": "SarSa AI | Gayrimenkul Analiz ve Pazarlama Motoru", 
        "service_desc": "Hepsi Bir Arada Görsel Mülk Zekası ve Küresel Satış Otomasyonu", 
        "subtitle": "Mülk fotoğraflarını anında profesyonel ilanlara, sosyal medya kitlerine, sinematik video senaryolarına ve teknik şartnamelere dönüştürün.",
        "settings": "⚙️ Yapılandırma", "target_lang": "✍️ İlan Yazım Dili...", "prop_type": "Emlak Tipi", "price": "Pazar Fiyatı", "location": "Konum", "tone": "Strateji",
        "tones": ["Standart Profesyonel", "Ultra-Lüks", "Yatırım Potansiyeli", "Modern Minimalist", "Aile Konforu"],
        "ph_prop": "Örn: 3+1 Daire...", "ph_price": "Örn: 5.000.000 TL...", "ph_loc": "Örn: Beşiktaş, İstanbul...",
        "custom_inst": "📝 Özel Notlar", "custom_inst_ph": "Örn: Yüksek tavanlar...", "btn": "🚀 TÜM PAZARLAMA VARLIKLARINI OLUŞTUR", "upload_label": "📸 Fotoğrafları Buraya Bırakın",
        "result": "💎 Yönetici Önizlemesi", "loading": "Premium pazarlama ekosisteminiz hazırlanıyor...", "empty": "Profesyonel analiz için görsel bekleniyor.", "download": "📥 TXT İndir", "pdf_btn": "📄 PDF Raporu", "copy_btn": "📋 Kopyala", "saved_msg": "✅ Kopyalandı!", 
        "tab_main": "📝 Ana İlan", "tab_social": "📱 Sosyal Medya Kiti", "tab_video": "🎬 Video Senaryoları", "tab_tech": "⚙️ Teknik Özellikler", "tab_invest": "📊 Yatırım Skoru", "tab_seo": "🔍 SEO Pro"
    },
    "Español": { "title": "SarSa AI | Motor de Marketing Inmobiliario", "service_desc": "Inteligencia Visual y Automatización de Ventas", "subtitle": "Convierta fotos en anuncios premium y kits de redes sociales al instante.", "settings": "⚙️ Configuración", "target_lang": "✍️ Idioma...", "prop_type": "Tipo", "price": "Precio", "location": "Ubicación", "tone": "Estrategia", "tones": ["Estándar", "Lujo", "Inversión"], "btn": "🚀 GENERAR ACTIVOS", "upload_label": "📸 Subir Fotos", "result": "💎 Vista Previa", "loading": "Analizando...", "empty": "Esperando imágenes.", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 Copiar", "saved_msg": "✅ ¡Copiado!", "tab_main": "📝 Anuncio", "tab_social": "📱 Social", "tab_video": "🎬 Video", "tab_tech": "⚙️ Técnica", "tab_invest": "📊 Inversión", "tab_seo": "🔍 SEO"},
    "Deutsch": { "title": "SarSa AI | Immobilien Marketing Plattform", "service_desc": "Visuelle Objektintelligenz", "subtitle": "Fotos sofort in Premium-Exposés verwandeln.", "settings": "⚙️ Konfiguration", "target_lang": "✍️ Sprache...", "prop_type": "Objekttyp", "price": "Preis", "location": "Standort", "tone": "Strategie", "tones": ["Standard", "Luxus", "Invest"], "btn": "🚀 ERSTELLEN", "upload_label": "📸 Fotos hochladen", "result": "💎 Vorschau", "loading": "Wird erstellt...", "empty": "Warte auf Bilder.", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 Kopieren", "saved_msg": "✅ Kopiert!", "tab_main": "📝 Exposé", "tab_social": "📱 Social", "tab_video": "🎬 Video", "tab_tech": "⚙️ Tech", "tab_invest": "📊 Invest", "tab_seo": "🔍 SEO"},
    "Français": { "title": "SarSa AI | Marketing Immobilier", "service_desc": "Intelligence Visuelle Immobilière", "subtitle": "Transformez vos photos en annonces premium.", "settings": "⚙️ Configuration", "target_lang": "✍️ Langue...", "prop_type": "Type", "price": "Prix", "location": "Lieu", "tone": "Stratégie", "tones": ["Standard", "Luxe", "Invest"], "btn": "🚀 GÉNÉRER", "upload_label": "📸 Déposer Photos", "result": "💎 Aperçu", "loading": "Analyse...", "empty": "Attente d'images.", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 Copier", "saved_msg": "✅ Copié!", "tab_main": "📝 Annonce", "tab_social": "📱 Social", "tab_video": "🎬 Vidéo", "tab_tech": "⚙️ Tech", "tab_invest": "📊 Invest", "tab_seo": "🔍 SEO"},
    "Português": { "title": "SarSa AI | Marketing Imobiliário", "service_desc": "Inteligência Visual Imobiliária", "subtitle": "Transforme fotos em anúncios premium.", "settings": "⚙️ Configuração", "target_lang": "✍️ Idioma...", "prop_type": "Tipo", "price": "Preço", "location": "Local", "tone": "Estratégia", "tones": ["Padrão", "Luxo", "Investimento"], "btn": "🚀 GERAR", "upload_label": "📸 Enviar Fotos", "result": "💎 Pré-visualização", "loading": "Analisando...", "empty": "Aguardando imagens.", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 Copiar", "saved_msg": "✅ Copiado!", "tab_main": "📝 Anúncio", "tab_social": "📱 Social", "tab_video": "🎬 Vídeo", "tab_tech": "⚙️ Detalhes", "tab_invest": "📊 Invest", "tab_seo": "🔍 SEO"},
    "日本語": { "title": "SarSa AI | 不動産分析エンジン", "service_desc": "物件インテリジェンス自動化", "subtitle": "写真をプレミアム広告に瞬時に変換。", "settings": "⚙️ 設定", "target_lang": "✍️ 言語...", "prop_type": "物件種別", "price": "価格", "location": "所在地", "tone": "戦略", "tones": ["標準", "高級", "投資"], "btn": "🚀 生成する", "upload_label": "📸 写真アップ", "result": "💎 プレビュー", "loading": "構築中...", "empty": "画像を待機中。", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 コピー", "saved_msg": "✅ 完了", "tab_main": "📝 広告", "tab_social": "📱 SNS", "tab_video": "🎬 台本", "tab_tech": "⚙️ 仕様", "tab_invest": "📊 投資", "tab_seo": "🔍 SEO"},
    "中文": { "title": "SarSa AI | 房地产营销引擎", "service_desc": "房产视觉智能自动化", "subtitle": "立即将房产照片转化为优质房源描述。", "settings": "⚙️ 配置", "target_lang": "✍️ 编写语言...", "prop_type": "房产类型", "price": "市场价格", "location": "地点", "tone": "策略", "tones": ["标准", "豪宅", "投资潜力"], "btn": "🚀 生成", "upload_label": "📸 上传照片", "result": "💎 预览", "loading": "正在打造...", "empty": "等待图像。", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 复制", "saved_msg": "✅ 已复制", "tab_main": "📝 房源", "tab_social": "📱 社交媒体", "tab_video": "🎬 视频脚本", "tab_tech": "⚙️ 技术", "tab_invest": "📊 投资", "tab_seo": "🔍 SEO"},
    "العربية": { "title": "SarSa AI | محرك تسويق العقارات", "service_desc": "ذكاء العقارات البصري المتكامل", "subtitle": "حوّل صور العقارات إلى إعلانات مميزة فوراً.", "settings": "⚙️ الإعدادات", "target_lang": "✍️ لغة الكتابة...", "prop_type": "نوع العقار", "price": "السعر", "location": "الموقع", "tone": "الاستراتيجية", "tones": ["قياسي", "فخامة", "استثمار"], "btn": "🚀 إنشاء", "upload_label": "📸 ضع الصور هنا", "result": "💎 معاينة", "loading": "جاري التجهيز...", "empty": "في انتظار الصور.", "download": "📥 TXT", "pdf_btn": "📄 PDF", "copy_btn": "📋 نسخ", "saved_msg": "✅ تم النسخ!", "tab_main": "📝 إعلان", "tab_social": "📱 باقة التواصل", "tab_video": "🎬 فيديو", "tab_tech": "⚙️ تفاصيل", "tab_invest": "📊 استثمار", "tab_seo": "🔍 SEO"}
}

# --- CSS (İMLEÇ, BUTON VE SIDEBAR STİLİ TAMAMEN KORUNDU) --- 
st.markdown(""" 
    <style> 
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap'); 
        html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; } 
        .stApp { background-color: #f8fafc; } 
        div[data-testid="stInputInstructions"] { display: none !important; }
        .block-container { background: white; padding: 3rem !important; border-radius: 20px; box-shadow: 0 15px 45px rgba(0,0,0,0.04); margin-top: 2rem; border: 1px solid #e2e8f0; } 
        h1 { color: #0f172a !important; font-weight: 800 !important; text-align: center; } 
        
        /* KRİTİK: PARMAK İMLECİ (POINTER) AYARI */
        button, [data-baseweb="tab"], [data-testid="stFileUploader"],  
        div[data-baseweb="select"], div[role="button"], .stSelectbox div { 
            cursor: pointer !important; 
        } 
        .stTextInput input, .stTextArea textarea { cursor: text !important; }
        .stButton>button { background: #0f172a; color: white !important; border-radius: 10px; padding: 14px; font-weight: 600; width: 100%; border: none; transition: 0.3s; }
        .stButton>button:hover { background: #1e293b; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); } 
        .stTabs [aria-selected="true"] { background-color: #0f172a !important; color: white !important; border-radius: 8px 8px 0 0; }
    </style> 
""", unsafe_allow_html=True) 

# --- SESSION STATE --- 
for key, val in [("uretilen_ilan", ""), ("prop_type", ""), ("price", ""), ("location", ""), ("tone", "Standard Pro"), ("custom_inst", ""), ("target_lang_input", "English")]:
    if key not in st.session_state: st.session_state[key] = val

# --- SIDEBAR (DOKUNULMADI) --- 
with st.sidebar: 
    logo_img = load_logo("SarSa_Logo_Transparent.png") 
    if logo_img: st.image(logo_img, use_container_width=True) 
    else: st.markdown("<h2 style='text-align:center; color:#0f172a;'>SARSA AI</h2>", unsafe_allow_html=True) 
    current_ui_lang = st.selectbox("🌐 Interface Language", list(ui_languages.keys()), index=0)   
    t = ui_languages[current_ui_lang] 
    st.markdown("---") 
    st.header(t["settings"]) 
    st.session_state.target_lang_input = st.text_input(t["target_lang"], value=st.session_state.target_lang_input) 
    st.session_state.prop_type = st.text_input(t["prop_type"], value=st.session_state.prop_type, placeholder=t.get("ph_prop", "")) 
    st.session_state.price = st.text_input(t["price"], value=st.session_state.price, placeholder=t.get("ph_price", "")) 
    st.session_state.location = st.text_input(t["location"], value=st.session_state.location, placeholder=t.get("ph_loc", "")) 
    st.session_state.tone = st.selectbox(t["tone"], t["tones"]) 
    st.session_state.custom_inst = st.text_area(t["custom_inst"], value=st.session_state.custom_inst, placeholder=t.get("custom_inst_ph", "")) 

# --- ANA EKRAN (AÇIKLAMALAR GERİ GELDİ) --- 
st.markdown(f"<h1>🏢 {t['title']}</h1>", unsafe_allow_html=True) 
st.markdown(f"<p style='text-align:center; color:#0f172a; font-weight:700; font-size:1.4rem; letter-spacing:0.5px; margin-bottom:5px;'>{t.get('service_desc', '')}</p>", unsafe_allow_html=True) 
st.markdown(f"<div style='text-align:center; color:#64748b; font-size:1.1rem; max-width:850px; margin: 0 auto 2rem auto; line-height:1.5;'>{t.get('subtitle', '')}</div>", unsafe_allow_html=True) 

uploaded_files = st.file_uploader(t["upload_label"], type=["jpg", "png", "webp", "jpeg"], accept_multiple_files=True) 

if uploaded_files: 
    cols = st.columns(4) 
    images_for_ai = [Image.open(f) for f in uploaded_files] 
    for i, img in enumerate(images_for_ai): 
        with cols[i % 4]: st.image(img, use_container_width=True) 

    if st.button(t["btn"]): 
        with st.spinner(t["loading"]): 
            prompt = (f"Analyze as Senior Real Estate Strategist. Lang: {st.session_state.target_lang_input}. Type: {st.session_state.prop_type}. Loc: {st.session_state.location}. Price: {st.session_state.price}. Tone: {st.session_state.tone}. Notes: {st.session_state.custom_inst}. "
                     f"Sections: ## SEC_1 (Listing), ## SEC_2 (Social), ## SEC_3 (Video), ## SEC_4 (Tech), ## SEC_5 (Investment Scorecard Table), ## SEC_6 (SEO Keywords).")
            response = model.generate_content([prompt] + images_for_ai) 
            st.session_state.uretilen_ilan = response.text 

    if st.session_state.uretilen_ilan: 
        st.markdown("---") 
        raw = st.session_state.uretilen_ilan 
        parts = raw.split("##") 
        content_map = {}
        tab_titles = [t["tab_main"], t["tab_social"], t["tab_video"], t["tab_tech"], t["tab_invest"], t["tab_seo"]]
        tabs = st.tabs(tab_titles) 
        
        for i, tab in enumerate(tabs):
            with tab:
                sec_text = parts[i+1].split(":", 1)[-1].strip() if len(parts) > i+1 else raw
                content_map[tab_titles[i]] = sec_text
                st.text_area("Edit", value=sec_text, height=350, key=f"ed_{i}")
                if st.button(t["copy_btn"], key=f"cp_{i}"): st.toast(t["saved_msg"])

        c1, c2 = st.columns(2)
        with c1: st.download_button(t["download"], data=raw, file_name="sarsa_export.txt")
        with c2: st.download_button(t["pdf_btn"], data=create_pdf(content_map, {"loc": st.session_state.location, "price": st.session_state.price}), file_name="SarSa_Report.pdf")
else: st.info(t["empty"])
