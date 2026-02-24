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

"result": "💎 Executive Preview (Listing, Social Media & Video)",

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

"result": "💎 Yönetici Önizlemesi (İlan, Sosyal Medya ve Video)",

"loading": "Pazarlama paketiniz hazırlanıyor...",

"empty": "Analiz için görsel bekleniyor.",

"download": "📥 TXT Olarak İndir",

"save_btn": "💾 Kaydet",

"saved_msg": "✅ Kaydedildi!",

"error": "Hata:"

},

"Español": {

"title": "Salija AI | Inteligencia Inmobiliaria",

"service_desc": "Motor de Redacción y Análisis Visual de Propiedades con IA",

"subtitle": "Convierta visuales de propiedades en obras maestras de marketing.",

"settings": "⚙️ Configuración",

"target_lang": "✍️ Escribir en...",

"prop_type": "Tipo de Propiedad",

"price": "Precio de Mercado",

"location": "Ubicación",

"tone": "Estrategia",

"tones": ["Ultra-Lujo", "Potencial de Inversión", "Minimalista Moderno", "Confort Familiar", "Profesional Estándar"],

"custom_inst": "📝 Notas Especiales",

"custom_inst_ph": "Ej: Techos altos, cerca del metro...",

"btn": "🚀 GENERAR TEXTO ELITE",

"upload_label": "📸 Subir Fotos Aquí",

"result": "💎 Vista Previa Ejecutiva (Anuncio, Redes y Video)",

"loading": "Arquitectando su kit de marketing...",

"empty": "Esperando imágenes para analizar.",

"download": "📥 Exportar TXT",

"save_btn": "💾 Guardar Cambios",

"saved_msg": "✅ ¡Guardado!",

"error": "Error:"

},

"Deutsch": {

"title": "Salija AI | Immobilien-Intelligenz",

"service_desc": "KI-gestützte visuelle Objektanalyse & Copywriting-Engine",

"subtitle": "Verwandeln Sie Immobilienfotos in hochwirksame Marketing-Meisterwerke.",

"settings": "⚙️ Konfiguration",

"target_lang": "✍️ Erstellen in...",

"prop_type": "Objekttyp",

"price": "Marktpreis",

"location": "Standort",

"tone": "Strategie",

"tones": ["Ultra-Luxus", "Investitionspotenzial", "Modern-Minimalistisch", "Familienkomfort", "Standard-Profi"],

"custom_inst": "📝 Notizen",

"custom_inst_ph": "Z.B. Hohe Decken, U-Bahn-Nähe...",

"btn": "🚀 ELITE-TEXT ERSTELLEN",

"upload_label": "📸 Fotos hier hochladen",

"result": "💎 Executive-Vorschau (Exposé, Social Media & Video)",

"loading": "Erstelle Ihr Marketing-Kit...",

"empty": "Warte auf Bilder zur Analyse.",

"download": "📥 TXT Exportieren",

"save_btn": "💾 Speichern",

"saved_msg": "✅ Gespeichert!",

"error": "Fehler:"

},

"Français": {

"title": "Salija AI | Intelligence Immobilière",

"service_desc": "Moteur d'Analyse Visuelle et de Rédaction Immobilière via IA",

"subtitle": "Transformez vos visuels en chefs-d'œuvre marketing à haute conversion.",

"settings": "⚙️ Configuration",

"target_lang": "✍️ Rédiger en...",

"prop_type": "Type de Bien",

"price": "Prix du Marché",

"location": "Localisation",

"tone": "Stratégie",

"tones": ["Ultra-Luxe", "Potentiel d'Investissement", "Minimaliste Moderne", "Confort Familial", "Standard Pro"],

"custom_inst": "📝 Notes Spéciales",

"custom_inst_ph": "Ex: Plafonds hauts, proche métro...",

"btn": "🚀 GÉNÉRER TEXTE ÉLITE",

"upload_label": "📸 Déposer les Photos Ici",

"result": "💎 Aperçu Exécutif (Annonce, Réseaux et Vidéo)",

"loading": "Création de votre kit marketing...",

"empty": "En attente d'images pour analyse.",

"download": "📥 Exporter TXT",

"save_btn": "💾 Enregistrer",

"saved_msg": "✅ Enregistré !",

"error": "Erreur :"

},

"Português": {

"title": "Salija AI | Inteligência Imobiliária",

"service_desc": "Motor de Redação e Análise Visual de Imóveis com IA",

"subtitle": "Converta visuais de imóveis em obras-primas de marketing.",

"settings": "⚙️ Configuração",

"target_lang": "✍️ Escrever em...",

"prop_type": "Tipo de Imóvel",

"price": "Preço de Mercado",

"location": "Localização",

"tone": "Estratégia",

"tones": ["Ultra-Luxo", "Potencial de Investimento", "Minimalista Moderno", "Conforto Familiar", "Profissional Padrão"],

"custom_inst": "📝 Notas Especiais",

"custom_inst_ph": "Ex: Tetos altos, perto do metrô...",

"btn": "🚀 GERAR TEXTO ELITE",

"upload_label": "📸 Enviar Fotos Aqui",

"result": "💎 Pré-visualização (Anúncio, Redes e Vídeo)",

"loading": "Arquitetando seu kit de marketing...",

"empty": "Aguardando imagens para análise.",

"download": "📥 Exportar TXT",

"save_btn": "💾 Salvar Alterações",

"saved_msg": "✅ Salvo!",

"error": "Erro:"

},

"日本語": {

"title": "Salija AI | 不動産インテリジェンス",

"service_desc": "AIを活用した物件ビジュアル分析＆コピーライティングエンジン",

"subtitle": "物件写真を高成約率のマーケティング傑作に変換します。",

"settings": "⚙️ 設定",

"target_lang": "✍️ 作成言語...",

"prop_type": "物件種別",

"price": "市場価格",

"location": "所在地",

"tone": "戦略",

"tones": ["ウルトララグジュアリー", "投資ポテンシャル", "モダンミニマリスト", "ファミリーコンフォート", "スタンダードプロ"],

"custom_inst": "📝 特記事項",

"custom_inst_ph": "例：高い天井、駅近...",

"btn": "🚀 エリートコピーを生成",

"upload_label": "📸 ここに写真をアップロード",

"result": "💎 プレビュー (広告、SNS、動画)",

"loading": "マーケティングキットを作成中...",

"empty": "分析用の画像を待機中。",

"download": "📥 TXT出力",

"save_btn": "💾 変更を保存",

"saved_msg": "✅ 保存完了！",

"error": "エラー:"

},

"中文 (简体)": {

"title": "Salija AI | 房地产智能",

"service_desc": "AI驱动的房产视觉分析与文案引擎",

"subtitle": "将房产图片转化为高转化率的营销杰作。",

"settings": "⚙️ 配置",

"target_lang": "✍️ 编写语言...",

"prop_type": "房产类型",

"price": "市场价格",

"location": "地点",

"tone": "策略",

"tones": ["顶奢豪宅", "投资潜力", "现代简约", "家庭舒适", "标准专业"],

"custom_inst": "📝 特别备注",

"custom_inst_ph": "例如：挑高天花板，靠近地铁...",

"btn": "🚀 生成精英文案",

"upload_label": "📸 在此处上传照片",

"result": "💎 预览 (房源、社交媒体与视频)",

"loading": "正在构思您的营销套件...",

"empty": "等待图像进行分析。",

"download": "📥 导出 TXT",

"save_btn": "💾 保存更改",

"saved_msg": "✅ 已保存！",

"error": "错误:"

},

"العربية": {

"title": "Salija AI | ذكاء العقارات",

"service_desc": "محرك تحليل الصور وكتابة الإعلانات العقارية بالذكاء الاصطناعي",

"subtitle": "حول صور العقارات إلى تحف تسويقية عالية التحويل.",

"settings": "⚙️ الإعدادات",

"target_lang": "✍️ لغة الكتابة...",

"prop_type": "نوع العقار",

"price": "سعر السوق",

"location": "الموقع",

"tone": "الاستراتيجية",

"tones": ["فخامة فائقة", "إمكانات استثمارية", "عصري بسيط", "راحة عائلية", "احترافي قياسي"],

"custom_inst": "📝 ملاحظات خاصة",

"custom_inst_ph": "مثال: أسقف عالية، بالقرب من المترو...",

"btn": "🚀 إنشاء نص احترافي",

"upload_label": "📸 ضع الصور هنا",

"result": "💎 معاينة تنفيذية (إعلان، وسائل التواصل، فيديو)",

"loading": "جاري تجهيز حزمة التسويق الخاصة بك...",

"empty": "في انتظار الصور لبدء التحليل.",

"download": "📥 تصدير TXT",

"save_btn": "💾 حفظ التغييرات",

"saved_msg": "✅ تم الحفظ!",

"error": "خطأ:"

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

