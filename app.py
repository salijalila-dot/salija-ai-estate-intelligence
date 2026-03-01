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

# --- GLOBAL DİL SİSTEMİ (TÜM DİLLER + SARSA AI GÜNCELLEMESİ) --- 
ui_languages = { 
    "English": { 
        "title": "SarSa AI | Estate Intelligence", 
        "service_desc": "AI-Powered Visual Property Analysis & Copywriting Engine", 
        "subtitle": "Convert property visuals into high-conversion marketing masterpieces.", 
        "settings": "⚙️ Configuration", "target_lang": "✍️ Write Listing In...", "prop_type": "Property Type", "price": "Market Price", "location": "Location", "tone": "Strategy", 
        "tones": ["Ultra-Luxury", "Investment Potential", "Modern Minimalist", "Family Comfort", "Standard Pro"], 
        "custom_inst": "📝 Special Notes", "custom_inst_ph": "E.g., High ceilings, near metro...", "btn": "🚀 GENERATE ELITE COPY", "upload_label": "📸 Drop Property Photos Here", 
        "result": "💎 Executive Preview", "loading": "Architecting your listing...", "empty": "Awaiting visuals to start analysis.", "download": "📥 Export All as TXT", "download_tab": "📥 Download Section",
        "save_btn": "💾 Save Changes", "saved_msg": "✅ Saved!", "error": "Error:", "tab_main": "📝 Main Listing", "tab_social": "📱 Social Media", "tab_video": "🎬 Video", "tab_tech": "⚙️ Technical Details", 
        "label_main": "Marketing Copy", "label_social": "Social Media Content", "label_video": "Video Script", "label_tech": "Technical Specs" 
    }, 
    "Türkçe": { 
        "title": "SarSa AI | Emlak Zekası", 
        "service_desc": "Yapay Zeka Destekli Görsel Mülk Analizi ve İlan Yazım Motoru", 
        "subtitle": "Mülk görsellerini yüksek dönüşümlü pazarlama şaheserlerine dönüştürün.", 
        "settings": "⚙️ Yapılandırma", "target_lang": "✍️ İlan Yazım Dili...", "prop_type": "Emlak Tipi", "price": "Pazar Fiyatı", "location": "Konum", "tone": "Strateji", 
        "tones": ["Ultra-Lüks", "Yatırım Potansiyeli", "Modern Minimalist", "Aile Konforu", "Standart Profesyonel"], 
        "custom_inst": "📝 Özel Notlar", "custom_inst_ph": "Örn: Yüksek tavanlar, metroya yakın...", "btn": "🚀 ELİT METİN OLUŞTUR", "upload_label": "📸 Fotoğrafları Buraya Bırakın", 
        "result": "💎 Yönetici Önizlemesi", "loading": "İlanınız yazılıyor...", "empty": "Analiz için görsel bekleniyor.", "download": "📥 Tümünü TXT İndir", "download_tab": "📥 Sadece Bu Bölümü İndir",
        "save_btn": "💾 Kaydet", "saved_msg": "✅ Kaydedildi!", "error": "Hata:", "tab_main": "📝 Ana İlan", "tab_social": "📱 Sosyal Medya", "tab_video": "🎬 Video", "tab_tech": "⚙️ Teknik Detay", 
        "label_main": "Pazarlama Metni", "label_social": "Sosyal Medya", "label_video": "Video Script", "label_tech": "Teknik Özellikler" 
    },
    "Español": { 
        "title": "SarSa AI | Inteligencia Inmobiliaria", "service_desc": "Motor de Redacción y Análisis Visual de Propiedades con IA", "subtitle": "Convierta visuales de propiedades en obras maestras de marketing.", 
        "settings": "⚙️ Configuración", "target_lang": "✍️ Escribir en...", "prop_type": "Tipo de Propiedad", "price": "Precio de Mercado", "location": "Ubicación", "tone": "Estrategia", 
        "tones": ["Ultra-Lujo", "Potencial de Inversión", "Minimalista Moderno", "Confort Familiar", "Profesional Estándar"], 
        "custom_inst": "📝 Notas Especiales", "custom_inst_ph": "Ej: Techos altos, cerca del metro...", "btn": "🚀 GENERAR TEXTO ELITE", "upload_label": "📸 Subir Fotos Aquí", 
        "result": "💎 Vista Previa Ejecutiva", "loading": "Arquitectando su anuncio...", "empty": "Esperando imágenes.", "download": "📥 Exportar Todo", "download_tab": "📥 Descargar Sección",
        "save_btn": "💾 Guardar", "saved_msg": "✅ ¡Guardado!", "error": "Error:", "tab_main": "📝 Anuncio", "tab_social": "📱 Redes", "tab_video": "🎬 Video", "tab_tech": "⚙️ Técnico", 
        "label_main": "Texto Marketing", "label_social": "Contenido Social", "label_video": "Guion Video", "label_tech": "Especificaciones" 
    },
    "Deutsch": { 
        "title": "SarSa AI | Immobilien-Intelligenz", "service_desc": "KI-gestützte visuelle Objektanalyse & Copywriting-Engine", "subtitle": "Verwandeln Sie Immobilienfotos in Marketing-Meisterwerke.", 
        "settings": "⚙️ Konfiguration", "target_lang": "✍️ Erstellen in...", "prop_type": "Objekttyp", "price": "Marktpreis", "location": "Standort", "tone": "Strategie", 
        "tones": ["Ultra-Luxus", "Investitionspotenzial", "Modern-Minimalistisch", "Familienkomfort", "Standard-Profi"], 
        "custom_inst": "📝 Notizen", "custom_inst_ph": "Z.B. Hohe Decken...", "btn": "🚀 ELITE-TEXT ERSTELLEN", "upload_label": "📸 Fotos hochladen", 
        "result": "💎 Executive-Vorschau", "loading": "Erstelle Exposé...", "empty": "Warte auf Bilder.", "download": "📥 Alles Exportieren", "download_tab": "📥 Bereich Herunterladen",
        "save_btn": "💾 Speichern", "saved_msg": "✅ Gespeichert!", "error": "Fehler:", "tab_main": "📝 Exposé", "tab_social": "📱 Social Media", "tab_video": "🎬 Video", "tab_tech": "⚙️ Details", 
        "label_main": "Marketing-Text", "label_social": "Social Media Content", "label_video": "Video-Skript", "label_tech": "Technische Daten" 
    },
    "Français": { 
        "title": "SarSa AI | Intelligence Immobilière", "service_desc": "Moteur d'Analyse Visuelle et de Rédaction Immobilière via IA", "subtitle": "Transformez vos visuels en chefs-d'œuvre marketing.", 
        "settings": "⚙️ Configuration", "target_lang": "✍️ Rédiger en...", "prop_type": "Type de Bien", "price": "Prix du Marché", "location": "Localisation", "tone": "Stratégie", 
        "tones": ["Ultra-Luxe", "Potentiel d'Investissement", "Minimaliste Moderne", "Confort Familial", "Standard Pro"], 
        "custom_inst": "📝 Notes Spéciales", "custom_inst_ph": "Ex: Plafonds hauts...", "btn": "🚀 GÉNÉRER TEXTE ÉLITE", "upload_label": "📸 Déposer les Photos", 
        "result": "💎 Aperçu Exécutif", "loading": "Rédaction...", "empty": "En attente d'images.", "download": "📥 Tout Exporter", "download_tab": "📥 Télécharger la Section",
        "save_btn": "💾 Enregistrer", "saved_msg": "✅ Enregistré!", "error": "Erreur:", "tab_main": "📝 Annonce", "tab_social": "📱 Réseaux Sociaux", "tab_video": "🎬 Vidéo", "tab_tech": "⚙️ Détails", 
        "label_main": "Texte Marketing", "label_social": "Contenido Social", "label_video": "Script Vidéo", "label_tech": "Spécifications" 
    },
    "Português": { 
        "title": "SarSa AI | Inteligência Imobiliária", "service_desc": "Motor de Redação e Análise Visual de Imóveis com IA", "subtitle": "Converta visuais de imóveis em obras-primas.", 
        "settings": "⚙️ Configuração", "target_lang": "✍️ Escrever em...", "prop_type": "Tipo de Imóvel", "price": "Preço de Mercado", "location": "Localização", "tone": "Estratégia", 
        "tones": ["Ultra-Luxo", "Potencial de Investimento", "Minimalista Moderno", "Conforto Familiar", "Profissional Padrão"], 
        "custom_inst": "📝 Notas Especiais", "custom_inst_ph": "Ex: Tetos altos...", "btn": "🚀 GERAR TEXTO ELITE", "upload_label": "📸 Enviar Fotos", 
        "result": "💎 Pré-visualização", "loading": "Arquitetando...", "empty": "Aguardando imagens.", "download": "📥 Exportar Tudo", "download_tab": "📥 Baixar Seção",
        "save_btn": "💾 Salvar", "saved_msg": "✅ Salvo!", "error": "Erro:", "tab_main": "📝 Anúncio", "tab_social": "📱 Redes Sociais", "tab_video": "🎬 Vídeo", "tab_tech": "⚙️ Detalhes", 
        "label_main": "Texto Marketing", "label_social": "Conteúdo Social", "label_video": "Script de Vídeo", "label_tech": "Especificações" 
    },
    "日本語": { 
        "title": "SarSa AI | 不動産インテリジェンス", "service_desc": "AIを活用した物件ビジュアル分析＆コピーライティングエンジン", "subtitle": "物件写真を高成約率のマーケティング傑作に変換します。", 
        "settings": "⚙️ 設定", "target_lang": "✍️ 作成言語...", "prop_type": "物件種別", "price": "市場価格", "location": "所在地", "tone": "戦略", 
        "tones": ["ウルトララグジュアリー", "投資ポテンシャル", "モダンミニマリスト", "ファミリーコンフォート", "スタンダードプロ"], 
        "custom_inst": "📝 特記事項", "custom_inst_ph": "例：高い天井...", "btn": "🚀 エリートコピーを生成", "upload_label": "📸 アップロード", 
        "result": "💎 プレビュー", "loading": "作成中...", "empty": "画像を待機中。", "download": "📥 すべて出力", "download_tab": "📥 この部分をダウンロード",
        "save_btn": "💾 保存", "saved_msg": "✅ 保存完了！", "error": "エラー:", "tab_main": "📝 メイン広告", "tab_social": "📱 SNS投稿", "tab_video": "🎬 動画", "tab_tech": "⚙️ 詳細", 
        "label_main": "コピー", "label_social": "SNSコンテンツ", "label_video": "動画台本", "label_tech": "技術仕様" 
    },
    "中文 (简体)": { 
        "title": "SarSa AI | 房地产智能", "service_desc": "AI驱动的房产视觉分析与文案引擎", "subtitle": "将房产图片转化为高转化率的营销杰作。", 
        "settings": "⚙️ 配置", "target_lang": "✍️ 编写语言...", "prop_type": "房产类型", "price": "市场价格", "location": "地点", "tone": "策略", 
        "tones": ["顶奢豪宅", "投资潜力", "现代简约", "家庭舒适", "标准专业"], 
        "custom_inst": "📝 特别备注", "custom_inst_ph": "例如：挑高天花板...", "btn": "🚀 生成精英文案", "upload_label": "📸 上传照片", 
        "result": "💎 高管预览", "loading": "正在构思...", "empty": "等待图像。", "download": "📥 全部导出", "download_tab": "📥 下载此部分",
        "save_btn": "💾 保存更改", "saved_msg": "✅ 已保存！", "error": "错误:", "tab_main": "📝 房源描述", "tab_social": "📱 社交媒体", "tab_video": "🎬 视频脚本", "tab_tech": "⚙️ 技术细节", 
        "label_main": "营销文案", "label_social": "社媒内容", "label_video": "视频脚本", "label_tech": "技术规格" 
    },
    "العربية": { 
        "title": "SarSa AI | ذكاء العقارات", "service_desc": "محرك تحليل الصور وكتابة الإعلانات العقارية بالذكاء الاصطناعي", "subtitle": "حول صور العقارات إلى تحف تسويقية.", 
        "settings": "⚙️ الإعدادات", "target_lang": "✍️ لغة الكتابة...", "prop_type": "نوع العقار", "price": "سعر السوق", "location": "الموقع", "tone": "الاستراتيجية", 
        "tones": ["فخامة فائقة", "إمكانات استثمارية", "عصري بسيط", "راحة عائلية", "احترافي قياسي"], 
        "custom_inst": "📝 ملاحظات خاصة", "custom_inst_ph": "مثال: أسقف عالية...", "btn": "🚀 إنشاء نص احترافي", "upload_label": "📸 ضع الصور هنا", 
        "result": "💎 معاينة", "loading": "جاري الصياغة...", "empty": "في انتظار الصور.", "download": "📥 تصدير الكل", "download_tab": "📥 تنزيل القسم",
        "save_btn": "💾 حفظ", "saved_msg": "✅ تم الحفظ!", "error": "خطأ:", "tab_main": "📝 الإعلان", "tab_social": "📱 وسائل التواصل", "tab_video": "🎬 فيديو", "tab_tech": "⚙️ تفاصيل", 
        "label_main": "نص التسويق", "label_social": "محتوى التواصل", "label_video": "سيناريو الفيديو", "label_tech": "المواصفات" 
    }
} 

# --- SESSION STATE & CSS --- 
for key, val in [("uretilen_ilan", ""), ("prop_type", "Ultra-Luxury Apartment"), ("price", "£14,500,000"), ("location", "Mayfair, London"), ("tone", "Ultra-Luxury"), ("custom_inst", ""), ("target_lang_input", "English")]:
    if key not in st.session_state: st.session_state[key] = val

st.markdown(""" 
    <style> 
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap'); 
        html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; } 
        .stApp { background-color: #f8fafc; } 
        div[data-testid="stInputInstructions"] { display: none !important; }
        .block-container { background: white; padding: 3rem !important; border-radius: 20px; box-shadow: 0 15px 45px rgba(0,0,0,0.04); margin-top: 2rem; border: 1px solid #e2e8f0; } 
        h1 { color: #0f172a !important; font-weight: 800 !important; text-align: center; } 
        .stButton>button { background: #0f172a; color: white !important; border-radius: 10px; padding: 14px; font-weight: 600; width: 100%; transition: all 0.3s ease; cursor: pointer !important; } 
        .stButton>button:hover { background: #1e293b; border-color: #0f172a; } 
        .stTabs [data-baseweb="tab"] { height: 45px; background-color: #f1f5f9; border-radius: 8px 8px 0 0; padding: 8px 16px; cursor: pointer !important; } 
        .stTabs [aria-selected="true"] { background-color: #0f172a !important; color: white !important; } 
    </style> 
""", unsafe_allow_html=True) 

# --- SIDEBAR --- 
with st.sidebar: 
    logo_img = load_logo("Salija_AI_Transparent_Logo.png") 
    if logo_img: st.image(logo_img, use_container_width=True) 
    else: st.markdown("<h2 style='text-align:center; color:#0f172a;'>SARSA AI</h2>", unsafe_allow_html=True) 
     
    current_ui_lang = st.selectbox("🌐 Interface Language", list(ui_languages.keys()), index=0)  
    t = ui_languages[current_ui_lang] 
     
    st.markdown("---") 
    st.header(t["settings"]) 
    st.session_state.target_lang_input = st.text_input(t["target_lang"], value=st.session_state.target_lang_input) 
    st.session_state.prop_type = st.text_input(t["prop_type"], value=st.session_state.prop_type) 
    st.session_state.price = st.text_input(t["price"], value=st.session_state.price) 
    st.session_state.location = st.text_input(t["location"], value=st.session_state.location) 
    st.session_state.tone = st.selectbox(t["tone"], t["tones"]) 
    st.session_state.custom_inst = st.text_area(t["custom_inst"], value=st.session_state.custom_inst, placeholder=t["custom_inst_ph"]) 

# --- ANA EKRAN --- 
st.markdown(f"<h1>🏢 {t['title']}</h1>", unsafe_allow_html=True) 
st.markdown(f"<p style='text-align:center; color:#1e293b; font-weight:600; font-size:1.2rem;'>{t['service_desc']}</p>", unsafe_allow_html=True) 
st.markdown(f"<p style='text-align:center; color:#64748b; font-size:1rem; margin-bottom:2rem;'>{t['subtitle']}</p>", unsafe_allow_html=True) 

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
            # --- ZEKASI ARTIRILMIŞ PROMPT ---
            expert_prompt = f""" 
            Role: Senior PropTech Analyst & Luxury Copywriter for SarSa AI.
            Context: Create an elite marketing suite in {st.session_state.target_lang_input} for a {st.session_state.prop_type}.
            Location: {st.session_state.location}. Value: {st.session_state.price}.
            Tone Strategy: {st.session_state.tone}.
            
            Visual Intelligence Protocol:
            - Analyze images for premium finishes (hardwood, stone, designer fixtures).
            - Note spatial characteristics (open-plan, high ceilings, terraces).
            - Identify 'hero features' that drive value.
            
            Output strictly follows these headers:
            
            ## SECTION_1
            The Narrative: Write a captivating, high-conversion property story. Use sensory language. Focus on the lifestyle and prestige.
            
            ## SECTION_2
            Social Media: Create a viral-ready post for Instagram/LinkedIn. Include a hook, bulleted features, and 10 luxury hashtags.
            
            ## SECTION_3
            Video Script: Provide a 45-second cinematic storyboard script. Define visual shots and a professional voiceover.
            
            ## SECTION_4
            Technical Specs: A detailed list of architectural and technical features identified from the visuals or notes.
            """ 
            try: 
                response = model.generate_content([expert_prompt] + images_for_ai) 
                st.session_state.uretilen_ilan = response.text 
            except Exception as e: 
                st.error(f"{t['error']} {e}") 

    if st.session_state.uretilen_ilan: 
        st.markdown("---") 
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
        file_names = ["sarsa_listing.txt", "sarsa_social.txt", "sarsa_video.txt", "sarsa_specs.txt"]
        
        for i, tab in enumerate(tabs):
            with tab:
                area_val = content_list[i] if content_list[i] else raw_text
                st.text_area(f"Edit {i}", value=area_val, height=400, label_visibility="collapsed")
                st.download_button(t["download_tab"], data=area_val, file_name=file_names[i], key=f"dl_{i}")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.download_button(t["download"], data=raw_text, file_name="sarsa_complete_kit.txt"):
            st.balloons()
else: 
    st.info(t["empty"])
