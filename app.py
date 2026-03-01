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

# --- LOGO YÜKLEME FONKSİYONU --- 
@st.cache_data 
def load_logo(file_path): 
    if os.path.exists(file_path): return Image.open(file_path) 
    return None 

# --- TÜM DİLLERİ İÇEREN GLOBAL DİL SİSTEMİ --- 
ui_languages = { 
    "English": { 
        "title": f"{BRAND_NAME} | Estate Intelligence", "service_desc": "AI-Powered Visual Property Analysis", "subtitle": "Convert property visuals into marketing masterpieces.",
        "settings": "⚙️ Configuration", "target_lang": "✍️ Write Listing In...", "prop_type": "Property Type", "price": "Market Price", "location": "Location", "tone": "Strategy",
        "tones": ["Ultra-Luxury", "Investment Potential", "Modern Minimalist", "Family Comfort", "Standard Pro"],
        "custom_inst": "📝 Special Notes", "custom_inst_ph": "E.g., High ceilings...", "btn": f"🚀 {BRAND_NAME} GENERATE", "upload_label": "📸 Drop Photos Here",
        "loading": "Architecting your listing...", "empty": "Awaiting visuals.", "download": "📥 Export All", "download_tab": "📥 Download Section",
        "tab_main": "📝 Listing", "tab_social": "📱 Social", "tab_video": "🎬 Video", "tab_tech": "⚙️ Specs", "error": "Error:"
    }, 
    "Türkçe": { 
        "title": f"{BRAND_NAME} | Emlak Zekası", "service_desc": "Yapay Zeka Destekli Görsel Analiz", "subtitle": "Mülk görsellerini pazarlama şaheserlerine dönüştürün.",
        "settings": "⚙️ Yapılandırma", "target_lang": "✍️ İlan Yazım Dili...", "prop_type": "Emlak Tipi", "price": "Pazar Fiyatı", "location": "Konum", "tone": "Strateji",
        "tones": ["Ultra-Lüks", "Yatırım Potansiyeli", "Modern Minimalist", "Aile Konforu", "Standart Profesyonel"],
        "custom_inst": "📝 Özel Notlar", "custom_inst_ph": "Örn: Yüksek tavanlar...", "btn": f"🚀 {BRAND_NAME} OLUŞTUR", "upload_label": "📸 Fotoğrafları Buraya Bırakın",
        "loading": "İlanınız yazılıyor...", "empty": "Görsel bekleniyor.", "download": "📥 Tümünü İndir", "download_tab": "📥 Bölümü İndir",
        "tab_main": "📝 İlan", "tab_social": "📱 Sosyal", "tab_video": "🎬 Video", "tab_tech": "⚙️ Teknik", "error": "Hata:"
    },
    "Español": { 
        "title": f"{BRAND_NAME} | Inteligencia Inmobiliaria", "service_desc": "Análisis Visual de Propiedades con IA", "subtitle": "Convierta visuales en obras maestras de marketing.",
        "settings": "⚙️ Configuración", "target_lang": "✍️ Escribir en...", "prop_type": "Tipo de Propiedad", "price": "Precio", "location": "Ubicación", "tone": "Estrategia",
        "tones": ["Ultra-Lujo", "Potencial de Inversión", "Minimalista", "Confort Familiar", "Profesional"],
        "btn": f"🚀 GENERAR {BRAND_NAME}", "upload_label": "📸 Subir Fotos", "loading": "Generando...", "empty": "Esperando imágenes.",
        "tab_main": "📝 Anuncio", "tab_social": "📱 Redes", "tab_video": "🎬 Video", "tab_tech": "⚙️ Técnico", "download": "📥 Exportar", "download_tab": "📥 Descargar", "error": "Error:"
    },
    "Deutsch": { 
        "title": f"{BRAND_NAME} | Immobilien-KI", "service_desc": "KI-gestützte Immobilienanalyse", "subtitle": "Immobilienfotos in Marketing-Erfolge verwandeln.",
        "settings": "⚙️ Konfiguration", "target_lang": "✍️ Erstellen in...", "prop_type": "Objekttyp", "price": "Preis", "location": "Standort", "tone": "Strategie",
        "tones": ["Ultra-Luxus", "Investition", "Minimalistisch", "Familie", "Profi"],
        "btn": f"🚀 {BRAND_NAME} ERSTELLEN", "upload_label": "📸 Fotos hochladen", "loading": "Erstelle...", "empty": "Warte auf Bilder.",
        "tab_main": "📝 Exposé", "tab_social": "📱 Social Media", "tab_video": "🎬 Video", "tab_tech": "⚙️ Details", "download": "📥 Exportieren", "download_tab": "📥 Herunterladen", "error": "Fehler:"
    },
    "Français": { 
        "title": f"{BRAND_NAME} | Intelligence Immobilière", "service_desc": "Analyse Visuelle Immobilière par IA", "subtitle": "Transformez vos visuels en chefs-d'œuvre.",
        "settings": "⚙️ Configuration", "target_lang": "✍️ Rédiger en...", "prop_type": "Type de Bien", "price": "Prix", "location": "Localisation", "tone": "Stratégie",
        "tones": ["Ultra-Luxe", "Investissement", "Minimaliste", "Famille", "Pro"],
        "btn": f"🚀 GÉNÉRER {BRAND_NAME}", "upload_label": "📸 Déposer les Photos", "loading": "Rédaction...", "empty": "En attente.",
        "tab_main": "📝 Annonce", "tab_social": "📱 Réseaux", "tab_video": "🎬 Vidéo", "tab_tech": "⚙️ Détails", "download": "📥 Tout Exporter", "download_tab": "📥 Télécharger", "error": "Erreur:"
    },
    "Português": { 
        "title": f"{BRAND_NAME} | Inteligência Imobiliária", "service_desc": "Análise Visual de Imóveis com IA", "subtitle": "Converta visuais em obras-primas de marketing.",
        "settings": "⚙️ Configuração", "target_lang": "✍️ Escrever em...", "prop_type": "Tipo de Imóvel", "price": "Preço", "location": "Localização", "tone": "Estratégia",
        "tones": ["Ultra-Luxo", "Investimento", "Minimalista", "Família", "Padrão"],
        "btn": f"🚀 GERAR {BRAND_NAME}", "upload_label": "📸 Enviar Fotos", "loading": "Gerando...", "empty": "Aguardando fotos.",
        "tab_main": "📝 Anúncio", "tab_social": "📱 Redes", "tab_video": "🎬 Vídeo", "tab_tech": "⚙️ Detalhes", "download": "📥 Exportar", "download_tab": "📥 Baixar", "error": "Erro:"
    },
    "日本語": { 
        "title": f"{BRAND_NAME} | 不動産AI", "service_desc": "AIを活用した物件ビジュアル分析", "subtitle": "物件写真をマーケティング傑作に変換します。",
        "settings": "⚙️ 設定", "target_lang": "✍️ 作成言語...", "prop_type": "物件種別", "price": "価格", "location": "所在地", "tone": "戦略",
        "tones": ["ラグジュアリー", "投資用", "ミニマリスト", "ファミリー", "プロ"],
        "btn": f"🚀 {BRAND_NAME} 生成", "upload_label": "📸 写真をアップロード", "loading": "生成中...", "empty": "画像を待機中。",
        "tab_main": "📝 メイン", "tab_social": "📱 SNS", "tab_video": "🎬 動画", "tab_tech": "⚙️ 詳細", "download": "📥 出力", "download_tab": "📥 ダウンロード", "error": "エラー:"
    },
    "中文 (简体)": { 
        "title": f"{BRAND_NAME} | 房地产智能", "service_desc": "AI驱动的房产视觉分析", "subtitle": "将房产图片转化为营销杰作。",
        "settings": "⚙️ 配置", "target_lang": "✍️ 编写语言...", "prop_type": "房产类型", "price": "价格", "location": "地点", "tone": "策略",
        "tones": ["顶奢豪宅", "投资潜力", "现代简约", "家庭舒适", "专业标准"],
        "btn": f"🚀 生成 {BRAND_NAME}", "upload_label": "📸 上传照片", "loading": "正在构思...", "empty": "等待图像。",
        "tab_main": "📝 房源", "tab_social": "📱 社交媒体", "tab_video": "🎬 视频脚本", "tab_tech": "⚙️ 细节", "download": "📥 全部导出", "download_tab": "📥 下载此部分", "error": "错误:"
    },
    "العربية": { 
        "title": f"{BRAND_NAME} | ذكاء العقارات", "service_desc": "تحليل الصور العقارية بالذكاء الاصطناعي", "subtitle": "حول صور العقارات إلى تحف تسويقية.",
        "settings": "⚙️ الإعدادات", "target_lang": "✍️ لغة الكتابة...", "prop_type": "نوع العقار", "price": "السعر", "location": "الموقع", "tone": "الاستراتيجية",
        "tones": ["فخامة فائقة", "إمكانات استثمارية", "عصري بسيط", "راحة عائلية", "احترافي"],
        "btn": f"🚀 إنشاء {BRAND_NAME}", "upload_label": "📸 ضع الصور هنا", "loading": "جاري الصياغة...", "empty": "بانتظار الصور.",
        "tab_main": "📝 الإعلان", "tab_social": "📱 التواصل", "tab_video": "🎬 فيديو", "tab_tech": "⚙️ تفاصيل", "download": "📥 تصدير الكل", "download_tab": "📥 تنزيل القسم", "error": "خطأ:"
    }
} 

# --- SESSION STATE --- 
for key, val in [("uretilen_ilan", ""), ("prop_type", "Luxury Property"), ("price", "Price Upon Request"), ("location", "Global"), ("tone", "Ultra-Luxury"), ("custom_inst", ""), ("target_lang_input", "English")]:
    if key not in st.session_state: st.session_state[key] = val

# --- TASARIM (HATAYI KÖKTEN ÇÖZEN GÜÇLÜ CSS) --- 
st.markdown(f""" 
    <style> 
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap'); 
        html, body, [class*="st-"] {{ font-family: 'Plus Jakarta Sans', sans-serif; }} 
        .stApp {{ background-color: #f8fafc; }} 
        .block-container {{ background: white; padding: 3rem !important; border-radius: 20px; box-shadow: 0 15px 45px rgba(0,0,0,0.04); margin-top: 2rem; border: 1px solid #e2e8f0; }} 
        h1 {{ color: #0f172a !important; font-weight: 800 !important; text-align: center; }} 
        .stButton>button {{ background: #0f172a; color: white !important; border-radius: 10px; width: 100%; height: 3.5rem; font-weight: 600; }}
        
        /* 🎯 KESİN ÇÖZÜM: Hatalı metni gizle ve simgeyi düzelt */
        [data-testid="stSidebarCollapseButton"] {{
            visibility: hidden; /* Butonu gizle ama yerini koru */
        }}
        [data-testid="stSidebarCollapseButton"]::after {{
            content: "▶"; /* Yerine basit bir ok koy */
            visibility: visible;
            display: block;
            font-size: 1.5rem;
            color: #0f172a;
            padding: 5px;
            cursor: pointer;
        }}
        /* Sidebar açıkken oku çevir */
        [data-testid="stSidebar"][aria-expanded="true"] ~ section [data-testid="stSidebarCollapseButton"]::after {{
            content: "◀";
        }}
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
    st.session_state.prop_type = st.text_input(t["prop_type"], value=st.session_state.prop_type) 
    st.session_state.price = st.text_input(t["price"], value=st.session_state.price) 
    st.session_state.location = st.text_input(t["location"], value=st.session_state.location) 
    st.session_state.tone = st.selectbox(t["tone"], t["tones"]) 
    st.session_state.custom_inst = st.text_area(t["custom_inst"], value=st.session_state.custom_inst) 

# --- ANA EKRAN --- 
st.markdown(f"<h1>🏢 {t['title']}</h1>", unsafe_allow_html=True) 
st.markdown(f"<p style='text-align:center; font-weight:600; font-size:1.1rem;'>{t['service_desc']}</p>", unsafe_allow_html=True) 

uploaded_files = st.file_uploader(t["upload_label"], type=["jpg", "png", "webp", "jpeg"], accept_multiple_files=True) 

if uploaded_files: 
    images_for_ai = [Image.open(f) for f in uploaded_files] 
    st.image(images_for_ai, width=150)

    if st.button(t["btn"]): 
        with st.spinner(t["loading"]): 
            expert_prompt = f"Role: Senior Architect & PropTech Copywriter for {BRAND_NAME}. Task: Analyze property photos (materials, lighting, finishes) and create an elite marketing suite. Target Language: {st.session_state.target_lang_input}. Location: {st.session_state.location}. Tone: {st.session_state.tone}. Format: ## SECTION_1 (Narrative), ## SECTION_2 (Social), ## SECTION_3 (Video), ## SECTION_4 (Technical)."
            try: 
                response = model.generate_content([expert_prompt] + images_for_ai) 
                st.session_state.uretilen_ilan = response.text 
            except Exception as e: 
                st.error(f"{t['error']} {e}") 

    if st.session_state.uretilen_ilan: 
        raw_text = st.session_state.uretilen_ilan 
        parts = raw_text.split("##") 
        sec1, sec2, sec3, sec4 = "", "", "", "" 
        for p in parts: 
            if "SECTION_1" in p: sec1 = p.replace("SECTION_1", "").split(":", 1)[-1].strip() 
            elif "SECTION_2" in p: sec2 = p.replace("SECTION_2", "").split(":", 1)[-1].strip() 
            elif "SECTION_3" in p: sec3 = p.replace("SECTION_3", "").split(":", 1)[-1].strip() 
            elif "SECTION_4" in p: sec4 = p.replace("SECTION_4", "").split(":", 1)[-1].strip() 

        tabs = st.tabs([t["tab_main"], t["tab_social"], t["tab_video"], t["tab_tech"]]) 
        content_list = [sec1, sec2, sec3, sec4]
        
        for i, tab in enumerate(tabs):
            with tab:
                area_val = content_list[i] if content_list[i] else raw_text
                st.text_area(f"Edit {i}", value=area_val, height=400, label_visibility="collapsed")
                st.download_button(t["download_tab"], data=area_val, file_name=f"part_{i}.txt", key=f"dl_{i}")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.download_button(t["download"], data=raw_text, file_name=f"{BRAND_NAME.lower()}_complete.txt"):
            st.balloons()
else: 
    st.info(t["empty"])
