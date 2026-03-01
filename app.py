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
st.set_page_config(page_title="SarSa AI | Real Estate Analysis & Marketing Engine", page_icon="🏢", layout="wide") 

# --- HIZLANDIRICI --- 
@st.cache_data 
def load_logo(file_path): 
    if os.path.exists(file_path): return Image.open(file_path) 
    return None 

# --- PDF OLUŞTURMA FONKSİYONU ---
def create_pdf(text_content):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "SarSa AI - Professional Property Report")
    p.line(100, 740, 500, 740)
    p.setFont("Helvetica", 10)
    y = 710
    for line in text_content.split('\n'):
        if y < 50:
            p.showPage()
            p.setFont("Helvetica", 10)
            y = 750
        p.drawString(100, y, line[:90])
        y -= 15
    p.save()
    buffer.seek(0)
    return buffer

# --- GLOBAL DİL SİSTEMİ (TÜM DİLLER VE YENİ ÖZELLİKLER) --- 
ui_languages = { 
    "English": { 
        "title": "SarSa AI | Real Estate Analysis & Marketing Engine", 
        "service_desc": "All-in-One Visual Property Intelligence & Global Sales Automation", 
        "subtitle": "Transform property photos into premium listings, social media kits, cinematic video scripts, and technical data sheets instantly.",
        "settings": "⚙️ Configuration", "target_lang": "✍️ Write Listing In...", "prop_type": "Property Type", "price": "Market Price", "location": "Location", "tone": "Strategy",
        "tones": ["Standard Pro", "Ultra-Luxury", "Investment Potential", "Modern Minimalist", "Family Comfort"],
        "ph_prop": "E.g., 3+1 Apartment, Luxury Villa...", "ph_price": "E.g., $500,000 or £2,000/mo...", "ph_loc": "E.g., Manhattan, NY or London, UK...",
        "custom_inst": "📝 Special Notes", "custom_inst_ph": "E.g., High ceilings, near metro...", "btn": "🚀 GENERATE COMPLETE MARKETING ASSETS", "upload_label": "📸 Drop Property Photos Here",
        "result": "💎 Executive Preview", "loading": "Crafting your premium marketing ecosystem...", "empty": "Awaiting visuals to start professional analysis.", "download": "📥 Export TXT", "save_btn": "💾 Save Changes", "saved_msg": "✅ Saved!", "error": "Error:",
        "tab_main": "📝 Prime Listing", "tab_social": "📱 Social Media Kit", "tab_video": "🎬 Video Scripts", "tab_tech": "⚙️ Technical Specs", "label_main": "Sales Copy", "label_social": "Social Media Content", "label_video": "Video Script", "label_tech": "Technical Specifications",
        "copy_btn": "📋 Copy to Clipboard", "pdf_btn": "📄 Download PDF Report"
    }, 
    "Türkçe": { 
        "title": "SarSa AI | Gayrimenkul Analiz ve Pazarlama Motoru", 
        "service_desc": "Hepsi Bir Arada Görsel Mülk Zekası ve Küresel Satış Otomasyonu", 
        "subtitle": "Mülk fotoğraflarını anında profesyonel ilanlara, sosyal medya kitlerine, sinematik video senaryolarına ve teknik şartnamelere dönüştürün.",
        "settings": "⚙️ Yapılandırma", "target_lang": "✍️ İlan Yazım Dili...", "prop_type": "Emlak Tipi", "price": "Pazar Fiyatı", "location": "Konum", "tone": "Strateji",
        "tones": ["Standart Profesyonel", "Ultra-Lüks", "Yatırım Potansiyeli", "Modern Minimalist", "Aile Konforu"],
        "ph_prop": "Örn: 3+1 Daire, Müstakil Villa...", "ph_price": "Örn: 5.000.000 TL veya $2.500/ay...", "ph_loc": "Örn: Beşiktaş, İstanbul...",
        "custom_inst": "📝 Özel Notlar", "custom_inst_ph": "Örn: Yüksek tavanlar, metroya yakın...", "btn": "🚀 TÜM PAZARLAMA VARLIKLARINI OLUŞTUR", "upload_label": "📸 Fotoğrafları Buraya Bırakın",
        "result": "💎 Yönetici Önizlemesi", "loading": "Premium pazarlama ekosisteminiz hazırlanıyor...", "empty": "Profesyonel analiz için görsel bekleniyor.", "download": "📥 TXT Olarak İndir", "save_btn": "💾 Kaydet", "saved_msg": "✅ Kaydedildi!", "error": "Hata:",
        "tab_main": "📝 Ana İlan", "tab_social": "📱 Sosyal Medya Kiti", "tab_video": "🎬 Video Senaryoları", "tab_tech": "⚙️ Teknik Özellikler", "label_main": "Satış Metni", "label_social": "Sosyal Medya", "label_video": "Video Script", "label_tech": "Teknik Detaylar",
        "copy_btn": "📋 Panoya Kopyala", "pdf_btn": "📄 PDF Raporu İndir"
    },
    "Español": { 
        "title": "SarSa AI | Motor de Marketing y Análisis Inmobiliario", 
        "service_desc": "Inteligencia Visual de Propiedades y Automatización de Ventas Globales", 
        "subtitle": "Convierta fotos en anuncios premium, kits de redes sociales, guiones de video y fichas técnicas al instante.",
        "settings": "⚙️ Configuración", "target_lang": "✍️ Escribir en...", "prop_type": "Tipo de Propiedad", "price": "Precio de Mercado", "location": "Ubicación", "tone": "Estrategia",
        "tones": ["Profesional Estándar", "Ultra-Lujo", "Potencial de Inversión", "Minimalista Moderno", "Confort Familiar"],
        "ph_prop": "Ej: Apartamento 3+1, Villa de Lujo...", "ph_price": "Ej: $500.000 o €1.500/mes...", "ph_loc": "Ej: Madrid, España...",
        "custom_inst": "📝 Notas Especiales", "custom_inst_ph": "Ej: Techos altos, cerca del metro...", "btn": "🚀 GENERAR ACTIVOS DE MARKETING COMPLETOS", "upload_label": "📸 Subir Fotos Aquí",
        "result": "💎 Vista Previa Ejecutiva", "loading": "Creando su ecosistema de marketing...", "empty": "Esperando imágenes para análisis profesional.", "download": "📥 Exportar TXT", "save_btn": "💾 Guardar Cambios", "saved_msg": "✅ ¡Guardado!", "error": "Error:",
        "tab_main": "📝 Anuncio Premium", "tab_social": "📱 Kit de Redes", "tab_video": "🎬 Guiones de Video", "tab_tech": "⚙️ Especificaciones", "label_main": "Texto de Ventas", "label_social": "Contenido Social", "label_video": "Guion de Video", "label_tech": "Ficha Técnica",
        "copy_btn": "📋 Copiar", "pdf_btn": "📄 Descargar PDF"
    },
    "Deutsch": { 
        "title": "SarSa AI | Immobilienanalyse & Marketing-Plattform", 
        "service_desc": "All-in-One Visuelle Objektintelligenz & Globale Verkaufsautomatisierung", 
        "subtitle": "Verwandeln Sie Fotos sofort in Premium-Exposés, Social-Media-Kits, Videoskripte und Datenblätter.",
        "settings": "⚙️ Konfiguration", "target_lang": "✍️ Erstellen in...", "prop_type": "Objekttyp", "price": "Marktpreis", "location": "Standort", "tone": "Strategie",
        "tones": ["Standard-Profi", "Ultra-Luxus", "Investitionspotenzial", "Modern-Minimalistisch", "Familienkomfort"],
        "ph_prop": "Z.B. 3-Zimmer-Wohnung, Luxusvilla...", "ph_price": "Z.B. 500.000€...", "ph_loc": "Z.B. Berlin, Deutschland...",
        "custom_inst": "📝 Notizen", "custom_inst_ph": "Z.B. Hohe Decken...", "btn": "🚀 MARKETING-ASSETS ERSTELLEN", "upload_label": "📸 Fotos hier hochladen",
        "result": "💎 Executive-Vorschau", "loading": "Wird erstellt...", "empty": "Warte auf Bilder.", "download": "📥 TXT Export", "save_btn": "💾 Speichern", "saved_msg": "✅ Gespeichert!", "error": "Fehler:",
        "tab_main": "📝 Exposé", "tab_social": "📱 Social Kit", "tab_video": "🎬 Videoskripte", "tab_tech": "⚙️ Tech-Details", "label_main": "Verkaufstext", "label_social": "Social Media", "label_video": "Video", "label_tech": "Technische Daten",
        "copy_btn": "📋 Kopieren", "pdf_btn": "📄 PDF Herunterladen"
    },
    "Français": { 
        "title": "SarSa AI | Moteur d'Analyse Immobilier", 
        "service_desc": "Intelligence Visuelle Immobilière et Ventes Globales", 
        "subtitle": "Transformez vos photos en annonces premium et outils marketing.",
        "settings": "⚙️ Configuration", "target_lang": "✍️ Rédiger en...", "prop_type": "Type de Bien", "price": "Prix", "location": "Localisation", "tone": "Stratégie",
        "tones": ["Standard Pro", "Ultra-Luxe", "Investissement", "Moderne", "Famille"],
        "ph_prop": "Ex: Appartement T4...", "ph_price": "Ex: 500.000€...", "ph_loc": "Ex: Paris, France...",
        "custom_inst": "📝 Notes", "custom_inst_ph": "Ex: Proche métro...", "btn": "🚀 GÉNÉRER LES ACTIFS", "upload_label": "📸 Déposer les Photos",
        "result": "💎 Aperçu", "loading": "Préparation...", "empty": "En attente d'images.", "download": "📥 Exporter TXT", "save_btn": "💾 Enregistrer", "saved_msg": "✅ Enregistré!", "error": "Erreur:",
        "tab_main": "📝 Annonce", "tab_social": "📱 Kit Social", "tab_video": "🎬 Vidéo", "tab_tech": "⚙️ Tech", "label_main": "Texte", "label_social": "Social", "label_video": "Script", "label_tech": "Spécifications",
        "copy_btn": "📋 Copier", "pdf_btn": "📄 Télécharger PDF"
    },
    "Português": { 
        "title": "SarSa AI | Motor de Marketing Imobiliário", 
        "service_desc": "Inteligência Visual e Automação de Vendas", 
        "subtitle": "Converta fotos em anúncios premium e kits de marketing.",
        "settings": "⚙️ Configuração", "target_lang": "✍️ Escrever em...", "prop_type": "Tipo de Imóvel", "price": "Preço", "location": "Localização", "tone": "Estratégia",
        "tones": ["Profissional Padrão", "Ultra-Luxo", "Investimento", "Moderno", "Família"],
        "ph_prop": "Ex: Apartamento T3...", "ph_price": "Ex: 500.000€...", "ph_loc": "Ex: Lisboa, Portugal...",
        "custom_inst": "📝 Notas", "custom_inst_ph": "Ex: Perto do metrô...", "btn": "🚀 GERAR ATIVOS", "upload_label": "📸 Enviar Fotos",
        "result": "💎 Pré-visualização", "loading": "Preparando...", "empty": "Aguardando imagens.", "download": "📥 Exportar TXT", "save_btn": "💾 Salvar", "saved_msg": "✅ Salvo!", "error": "Erro:",
        "tab_main": "📝 Anúncio", "tab_social": "📱 Redes Sociais", "tab_video": "🎬 Vídeo", "tab_tech": "⚙️ Detalhes", "label_main": "Vendas", "label_social": "Social", "label_video": "Roteiro", "label_tech": "Técnico",
        "copy_btn": "📋 Copiar", "pdf_btn": "📄 Baixar PDF"
    },
    "日本語": { 
        "title": "SarSa AI | 不動産分析＆マーケティング", 
        "service_desc": "物件インテリジェンス＆グローバル販売自動化", 
        "subtitle": "物件写真をプレミアム広告、SNSキットに瞬時に変換。",
        "settings": "⚙️ 設定", "target_lang": "✍️ 作成言語...", "prop_type": "物件種別", "price": "価格", "location": "所在地", "tone": "戦略",
        "tones": ["スタンダードプロ", "ウルトララグジュアリー", "投資", "モダン", "ファミリー"],
        "ph_prop": "例：3LDKマンション...", "ph_price": "例：5000万円...", "ph_loc": "例：東京都港区...",
        "custom_inst": "📝 特記事項", "custom_inst_ph": "例：駅近...", "btn": "🚀 生成する", "upload_label": "📸 写真をアップロード",
        "result": "💎 プレビュー", "loading": "構築中...", "empty": "画像を待機中。", "download": "📥 TXT出力", "save_btn": "💾 保存", "saved_msg": "✅ 保存完了！", "error": "エラー:",
        "tab_main": "📝 広告", "tab_social": "📱 SNS", "tab_video": "🎬 動画", "tab_tech": "⚙️ 技術仕様", "label_main": "コピー", "label_social": "SNS用", "label_video": "台本", "label_tech": "仕様書",
        "copy_btn": "📋 コピー", "pdf_btn": "📄 PDFダウンロード"
    },
    "中文 (简体)": { 
        "title": "SarSa AI | 房地产分析与营销", 
        "service_desc": "房产视觉智能与全球销售自动化", 
        "subtitle": "将照片转化为优质房源描述和营销工具。",
        "settings": "⚙️ 配置", "target_lang": "✍️ 编写语言...", "prop_type": "房产类型", "price": "价格", "location": "地点", "tone": "策略",
        "tones": ["标准专业", "顶奢豪宅", "投资潜力", "现代简约", "家庭舒适"],
        "ph_prop": "例如：3居室公寓...", "ph_price": "例如：$500,000...", "ph_loc": "例如：上海...",
        "custom_inst": "📝 特别备注", "custom_inst_ph": "例如：靠近地铁...", "btn": "🚀 生成营销资产", "upload_label": "📸 上传照片",
        "result": "💎 预览", "loading": "正在打造...", "empty": "等待分析。", "download": "📥 导出 TXT", "save_btn": "💾 保存更改", "saved_msg": "✅ 已保存！", "error": "错误:",
        "tab_main": "📝 房源", "tab_social": "📱 社交媒体", "tab_video": "🎬 视频脚本", "tab_tech": "⚙️ 技术细节", "label_main": "文案", "label_social": "社媒", "label_video": "脚本", "label_tech": "规格",
        "copy_btn": "📋 复制", "pdf_btn": "📄 下载 PDF"
    },
    "العربية": { 
        "title": "SarSa AI | محرك تسويق العقارات", 
        "service_desc": "ذكاء العقارات البصري وأتمتة المبيعات", 
        "subtitle": "حوّل صور العقارات إلى إعلانات مميزة وأدوات تسويقية.",
        "settings": "⚙️ الإعدادات", "target_lang": "✍️ لغة الكتابة...", "prop_type": "نوع العقار", "price": "السعر", "location": "الموقع", "tone": "الاستراتيجية",
        "tones": ["احترافي قياسي", "فخامة فائقة", "استثمار", "عصري", "عائلي"],
        "ph_prop": "مثال: شقة 3+1...", "ph_price": "مثال: $500,000...", "ph_loc": "مثال: دبي...",
        "custom_inst": "📝 ملاحظات", "custom_inst_ph": "مثال: قريب من المترو...", "btn": "🚀 إنشاء الأصول", "upload_label": "📸 ضع الصور هنا",
        "result": "💎 معاينة", "loading": "جاري التجهيز...", "empty": "في انتظار الصور.", "download": "📥 تصدير TXT", "save_btn": "💾 حفظ", "saved_msg": "✅ تم الحفظ!", "error": "خطأ:",
        "tab_main": "📝 إعلان", "tab_social": "📱 تواصل", "tab_video": "🎬 فيديو", "tab_tech": "⚙️ تفاصيل", "label_main": "نص البيع", "label_social": "محتوى", "label_video": "سيناريو", "label_tech": "فني",
        "copy_btn": "📋 نسخ", "pdf_btn": "📄 تحميل PDF"
    }
} 

# --- SESSION STATE --- 
for key, val in [("uretilen_ilan", ""), ("prop_type", ""), ("price", ""), ("location", ""), ("tone", ""), ("custom_inst", ""), ("target_lang_input", "English")]:
    if key not in st.session_state: st.session_state[key] = val

# --- CSS (MARKAYA ÖZEL STİL) --- 
st.markdown(""" 
    <style> 
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap'); 
        html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; } 
        .stApp { background-color: #f8fafc; } 
        div[data-testid="stInputInstructions"] { display: none !important; }
        .block-container { background: white; padding: 3rem !important; border-radius: 20px; box-shadow: 0 15px 45px rgba(0,0,0,0.04); border: 1px solid #e2e8f0; } 
        h1 { color: #0f172a !important; font-weight: 800 !important; text-align: center; } 
        .stButton>button { background: #0f172a; color: white !important; border-radius: 10px; padding: 12px; font-weight: 600; width: 100%; border: none; cursor: pointer; }
        .stButton>button:hover { background: #1e293b; } 
    </style> 
""", unsafe_allow_html=True) 

# --- SIDEBAR --- 
with st.sidebar: 
    logo_img = load_logo("SarSa_Logo_Transparent.png") 
    if logo_img: st.image(logo_img, use_container_width=True) 
    else: st.markdown("<h2 style='text-align:center; color:#0f172a;'>SARSA AI</h2>", unsafe_allow_html=True) 
      
    current_ui_lang = st.selectbox("🌐 Interface Language", list(ui_languages.keys()), index=0)   
    t = ui_languages[current_ui_lang] 
      
    st.markdown("---") 
    st.header(t["settings"]) 
    st.session_state.target_lang_input = st.text_input(t["target_lang"], value=st.session_state.target_lang_input) 
    st.session_state.prop_type = st.text_input(t["prop_type"], value=st.session_state.prop_type, placeholder=t["ph_prop"]) 
    st.session_state.price = st.text_input(t["price"], value=st.session_state.price, placeholder=t["ph_price"]) 
    st.session_state.location = st.text_input(t["location"], value=st.session_state.location, placeholder=t["ph_loc"]) 
    
    current_tone_idx = t["tones"].index(st.session_state.tone) if st.session_state.tone in t["tones"] else 0
    st.session_state.tone = st.selectbox(t["tone"], t["tones"], index=current_tone_idx) 
    st.session_state.custom_inst = st.text_area(t["custom_inst"], value=st.session_state.custom_inst, placeholder=t["custom_inst_ph"]) 

# --- ANA EKRAN --- 
st.markdown(f"<h1>🏢 {t['title']}</h1>", unsafe_allow_html=True) 
st.markdown(f"<p style='text-align:center; color:#0f172a; font-weight:700; font-size:1.4rem;'>{t['service_desc']}</p>", unsafe_allow_html=True) 
st.markdown(f"<div style='text-align:center; color:#64748b; margin-bottom:2rem;'>{t['subtitle']}</div>", unsafe_allow_html=True) 

uploaded_files = st.file_uploader(t["upload_label"], type=["jpg", "png", "webp", "jpeg"], accept_multiple_files=True) 

if uploaded_files: 
    cols = st.columns(4) 
    images_for_ai = [Image.open(f) for f in uploaded_files] 
    for i, img in enumerate(images_for_ai): 
        with cols[i % 4]: st.image(img, use_container_width=True) 

    if st.button(t["btn"]): 
        with st.spinner(t["loading"]): 
            p_type = st.session_state.prop_type if st.session_state.prop_type else "Property"
            p_loc = st.session_state.location if st.session_state.location else "undisclosed location"
            expert_prompt = (f"Role: Real Estate Strategist. Language: {st.session_state.target_lang_input}. "
                             f"Property: {p_type} at {p_loc}. Strategy: {st.session_state.tone}. "
                             f"Instructions: Split into ## SECTION_1 (Listing), ## SECTION_2 (Social), ## SECTION_3 (Video), ## SECTION_4 (Tech).")
            try: 
                response = model.generate_content([expert_prompt] + images_for_ai) 
                st.session_state.uretilen_ilan = response.text 
            except Exception as e: st.error(f"{t['error']} {e}") 

    if st.session_state.uretilen_ilan: 
        st.markdown("---") 
        raw_text = st.session_state.uretilen_ilan 
        parts = raw_text.split("##") 
        sections = {f"SECTION_{i}": "" for i in range(1, 5)}
        for p in parts:
            for s_key in sections.keys():
                if s_key in p: sections[s_key] = p.split(":", 1)[-1].strip()

        tabs = st.tabs([t["tab_main"], t["tab_social"], t["tab_video"], t["tab_tech"]]) 
        
        for i, tab in enumerate(tabs):
            s_key = f"SECTION_{i+1}"
            content = sections[s_key] if sections[s_key] else raw_text if i==0 else ""
            with tab:
                st.text_area("Content", value=content, height=350, key=f"area_{i}")
                # Panoya kopyalama hatırlatıcısı
                if st.button(t["copy_btn"], key=f"copy_{i}"):
                    st.toast(f"{t['saved_msg']}")

        st.markdown("---")
        c1, c2, c3 = st.columns(3) 
        with c1: 
            if st.button(t["save_btn"]): st.success(t["saved_msg"]) 
        with c2: 
            st.download_button(t["download"], data=raw_text, file_name="sarsa_ai_export.txt") 
        with c3:
            pdf_data = create_pdf(raw_text)
            st.download_button(t["pdf_btn"], data=pdf_data, file_name="SarSa_AI_Report.pdf", mime="application/pdf")
else: 
    st.info(t["empty"])
