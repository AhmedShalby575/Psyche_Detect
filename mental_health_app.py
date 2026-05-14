"""
PsyEra – Streamlit Mental Health Assessment Application
========================================================
Web app for early detection of mental health disorders with multilingual support
(Arabic, English, French). Includes dynamic questionnaire, AI chat assistant,
statistics, and forecasts.
"""

import streamlit as st
import random
import json
import requests
import math
from datetime import datetime
from data.questions import get_questions, build_flow, score_answers
from data.disorders import disorders


# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PsyEra",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Full CSS (exactly as original) ──────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
* { font-family: 'Cairo', sans-serif !important; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: linear-gradient(135deg, #0F0C29 0%, #302B63 50%, #24243e 100%) !important;
    min-height: 100vh;
}
[data-testid="stSidebar"] { display: none; }
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }
footer { display: none !important; }
#MainMenu { display: none; }
.block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; max-width: 700px !important; }
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        radial-gradient(1px 1px at 10% 20%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 30% 60%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 50% 10%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 70% 80%, rgba(255,255,255,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 40%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 20% 90%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 80% 15%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 45% 50%, rgba(255,255,255,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 60% 30%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 15% 70%, rgba(255,255,255,0.5) 0%, transparent 100%);
    pointer-events: none;
    z-index: 0;
}
.psyera-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 16px;
    color: white;
}
.psyera-card-warning {
    background: rgba(251,191,36,0.1);
    border: 1px solid rgba(251,191,36,0.3);
    border-radius: 14px;
    padding: 16px;
    color: #FCD34D;
    text-align: center;
    font-size: 14px;
    margin-bottom: 16px;
}
.disorder-card {
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 12px;
    border-left-width: 4px;
    border-left-style: solid;
    background: rgba(255,255,255,0.05);
    color: white;
}
.stButton > button {
    width: 100%;
    border-radius: 50px !important;
    font-family: 'Cairo', sans-serif !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    padding: 12px 24px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(102,126,234,0.4) !important;
}
.stTextInput > div > div > input, .stSelectbox > div > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 14px !important;
    color: white !important;
    font-family: 'Cairo', sans-serif !important;
}
.stProgress > div > div {
    background: linear-gradient(90deg, #667eea, #764ba2) !important;
    border-radius: 50px !important;
}
.stRadio > div { gap: 10px; }
.stRadio > div > label { color: rgba(255,255,255,0.8) !important; }
h1, h2, h3, h4, p, span, label, div {
    color: white !important;
}
.footer-text {
    text-align: center;
    color: rgba(255,255,255,0.25) !important;
    font-size: 11px;
    margin-top: 20px;
    padding-bottom: 10px;
}
.ans-btn-yes { background: rgba(16,185,129,0.2) !important; border: 2px solid #10B981 !important; }
.ans-btn-sometimes { background: rgba(245,158,11,0.2) !important; border: 2px solid #F59E0B !important; }
.ans-btn-no { background: rgba(239,68,68,0.2) !important; border: 2px solid #EF4444 !important; }
.chat-bubble-user {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 18px 18px 4px 18px;
    padding: 12px 16px;
    margin: 6px 0;
    max-width: 80%;
    margin-left: auto;
    color: white;
    font-size: 14px;
    line-height: 1.5;
}
.chat-bubble-bot {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 18px 18px 18px 4px;
    padding: 12px 16px;
    margin: 6px 0;
    max-width: 85%;
    color: rgba(255,255,255,0.9);
    font-size: 14px;
    line-height: 1.5;
}
.metric-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 16px;
    text-align: center;
}
.nav-container {
    display: flex;
    gap: 8px;
    justify-content: center;
    margin-bottom: 20px;
    flex-wrap: wrap;
}
.nav-pill {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 50px;
    padding: 8px 20px;
    color: rgba(255,255,255,0.7);
    font-size: 14px;
    cursor: pointer;
}
.nav-pill-active {
    background: rgba(102,126,234,0.3);
    border-color: #667eea;
    color: white;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ─── Session State Initialization ───────────────────────────────────────────
def init_state():
    """Initialize all session state variables with default values."""
    defaults = {
        "page": "home",
        "lang": "ar",   # ar, en, fr
        "age_group": None,
        "name": "",
        "gender": "",
        "national_id": "",
        "nid_age": None,
        "nid_gender": None,
        "governorate": None,
        "answers": {},
        "quiz_pos": 0,
        "duration": None,
        "scores": None,
        "chat_messages": [],
        "chat_count": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─── Helper functions ────────────────────────────────────────────────────────
def t(ar, en, fr):
    """Return text in current language (Arabic, English, French)."""
    if st.session_state.lang == "ar":
        return ar
    elif st.session_state.lang == "fr":
        return fr
    else:
        return en

def go(page):
    """Change current page and rerun the app."""
    st.session_state.page = page
    st.rerun()

# ─── National ID extraction (unchanged) ──────────────────────────────────────
GOVERNORATE_CODES = {
    "01":"القاهرة","02":"الإسكندرية","03":"بورسعيد","04":"السويس",
    "11":"دمياط","12":"الدقهلية","13":"الشرقية","14":"القليوبية",
    "15":"كفر الشيخ","16":"الغربية","17":"المنوفية","18":"البحيرة",
    "19":"الإسماعيلية","21":"الجيزة","22":"بني سويف","23":"الفيوم",
    "24":"المنيا","25":"أسيوط","26":"سوهاج","27":"قنا","28":"أسوان",
    "29":"الأقصر","31":"البحر الأحمر","32":"الوادي الجديد","33":"مطروح",
    "34":"شمال سيناء","35":"جنوب سيناء","88":"خارج الجمهورية",
}

def extract_national_id(nid):
    """
    Parse a 14-digit Egyptian national ID and extract age, gender, governorate.
    Returns None if invalid.
    """
    try:
        nid = nid.strip()
        if len(nid) != 14 or not nid.isdigit():
            return None
        century = int(nid[0])
        year2d = int(nid[1:3])
        month = int(nid[3:5])
        day = int(nid[5:7])
        gov_code = nid[7:9]
        if century not in (2, 3): return None
        if not (1 <= month <= 12): return None
        if not (1 <= day <= 31): return None
        year = 1900 + year2d if century == 2 else 2000 + year2d
        today = datetime.now()
        age = today.year - year - (1 if (today.month, today.day) < (month, day) else 0)
        if not (0 <= age <= 120): return None
        gender_digit = int(nid[12])
        gender = "Male" if gender_digit % 2 != 0 else "Female"
        governorate = GOVERNORATE_CODES.get(gov_code, "غير معروفة")
        return {"age": age, "gender": gender, "governorate": governorate}
    except:
        return None

# ─── Page functions ──────────────────────────────────────────────────────────
def page_home():
    """Render the home screen with logo, title, and main action buttons."""
    lang_label = t("🌐 AR", "🌐 EN", "🌐 FR")
    about_label = t("عن التطبيق", "About", "À propos")
    col_l, col_mid, col_r = st.columns([2, 3, 2])
    with col_l:
        if st.button(lang_label, key="lang_btn"):
            cur = st.session_state.lang
            if cur == "ar":
                st.session_state.lang = "en"
            elif cur == "en":
                st.session_state.lang = "fr"
            else:
                st.session_state.lang = "ar"
            st.rerun()
    with col_r:
        if st.button(about_label, key="about_btn"):
            go("about")

    # Logo + Title + Subtitle in one centered block
    try:
        import base64, pathlib
        logo_bytes = pathlib.Path("assets/psyera_logo_home.png").read_bytes()
        logo_b64 = base64.b64encode(logo_bytes).decode()
        logo_html = f"<img src='data:image/png;base64,{logo_b64}' style='width:110px; height:110px; object-fit:contain; display:block; margin:0 auto 10px auto;'>"
    except:
        logo_html = "<div style='font-size:80px; text-align:center; margin-bottom:8px;'>🧠</div>"

    subtitle = t("الكشف المبكر عن الاضطرابات النفسية", "Early Detection of Mental Health Disorders", "Détection précoce des troubles mentaux")
    st.markdown(f"""
    <div style='text-align:center; padding: 20px 0 10px 0;'>
        {logo_html}
        <div style='font-size:46px; font-weight:900; background: linear-gradient(90deg,#667eea,#f093fb,#764ba2); -webkit-background-clip:text; -webkit-text-fill-color:transparent; line-height:1.1; margin-bottom:6px;'>PsyEra</div>
        <p style='color:rgba(255,255,255,0.65); font-size:15px; margin:0;'>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(t("🧠 ابدأ التقييم", "🧠 Start Assessment", "🧠 Commencer l'évaluation"), key="start_btn", use_container_width=True):
        go("disclaimer")

    st.markdown("<br style='margin:4px'>", unsafe_allow_html=True)

    if st.button(t("🤖 اسأل بصير", "🤖 Ask the Psyer", "🤖 Demander au Psyer"), key="chat_btn", use_container_width=True):
        go("chat")

    st.markdown("<br style='margin:4px'>", unsafe_allow_html=True)

    if st.button(t("👨‍⚕️ كلم الدوك", "👨‍⚕️ Talk to the Doc", "👨‍⚕️ Parler au Doc"), key="doctor_btn", use_container_width=True):
        go("doctor")

    st.markdown("<br style='margin:4px'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button(t("📊 إحصائيات", "📊 Statistics", "📊 Statistiques"), key="stats_btn", use_container_width=True):
            go("stats")
    with col2:
        if st.button(t("📈 توقعات الانتشار", "📈 Forecasts", "📈 Prévisions"), key="forecast_btn", use_container_width=True):
            go("forecast")

    # Reviews — circle star button centered
    st.markdown("<br style='margin:4px'>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    div[data-testid="stButton"] button[kind="secondary"]#reviews_circle_btn,
    div.reviews-circle-wrap > div > button {
        width: 60px !important;
        height: 60px !important;
        border-radius: 50% !important;
        padding: 0 !important;
        font-size: 26px !important;
        border: 2px solid #FFD700 !important;
        background: rgba(255,215,0,0.10) !important;
        display: flex; align-items:center; justify-content:center;
    }
    </style>
    """, unsafe_allow_html=True)
    _, col_mid_rev, _ = st.columns([3, 1, 3])
    with col_mid_rev:
        if st.button("⭐", key="reviews_btn", use_container_width=False):
            go("reviews")

    st.markdown(f"<div class='footer-text'>PsyEra v1.0 | Bioinformatics Graduation Project 2026</div>", unsafe_allow_html=True)


def page_about():
    """Display project information, team members, and supervisors."""
    if st.button(t("‹ رجوع", "‹ Back", "‹ Retour"), key="back_about"):
        go("home")

    st.markdown(f"""
    <div class='psyera-card' style='text-align:center;'>
        <div style='font-size:44px;'>🧠</div>
        <h2 style='margin:8px 0;'>PsyEra v1.0</h2>
        <p style='color:rgba(255,255,255,0.6); font-size:13px;'>Bioinformatics Graduation Project 2026<br>Faculty of Science — Port Said University</p>
    </div>
    """, unsafe_allow_html=True)

    team_ar = ["أحمد السيد شلبي","أحمد أسامة عوض","أحمد محمد سماحة","إياد محمد طه","إسلام حسام الدين","لؤي السيد زكريا"]
    team_en = ["Ahmed Elsayed Shalaby","Ahmed Osama Awad","Ahmed Mohammed Samaha","Eyad Mohammed Taha","Eslam Hossam Eldin","Loay Elsayed Zakaria"]
    team_fr = team_en  # same as English for now
    sup_ar = ["د. محمد الجنيدي","د. هدير عبد الحق راشد"]
    sup_en = ["Dr. Mohammed Elgenedy","Dr. Hadeer Abd Elhak Rashed"]
    sup_fr = sup_en

    if st.session_state.lang == "ar":
        team = team_ar
        supervisors = sup_ar
    elif st.session_state.lang == "fr":
        team = team_fr
        supervisors = sup_fr
    else:
        team = team_en
        supervisors = sup_en

    st.markdown(f"<div class='psyera-card' style='text-align:center;'><b style='color:#667eea; font-size:15px;'>{t('فريق العمل','Team','Équipe')}</b><br><br>" +
                "<br>".join([f"<span style='color:rgba(255,255,255,0.85);'>• {m}</span>" for m in team]) + "</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='psyera-card' style='text-align:center;'><b style='color:#667eea; font-size:15px;'>{t('إشراف','Supervision','Supervision')}</b><br><br>" +
                "<br>".join([f"<span style='color:rgba(255,255,255,0.85);'>• {s}</span>" for s in supervisors]) + "</div>", unsafe_allow_html=True)

    try:
        col = st.columns([1,2,1])[1]
        with col:
            st.image("assets/faculty_logo.png", width=120)
    except:
        pass


def page_disclaimer():
    """Show legal/educational disclaimer and ask for confirmation."""
    if st.button(t("‹ رجوع", "‹ Back", "‹ Retour"), key="back_disc"):
        go("home")

    st.markdown("""
    <div class='psyera-card' style='text-align:center;'>
        <div style='font-size:50px;'>⚠️</div>
        <h2 style='margin:8px 0;'>{title}</h2>
        <div class='psyera-card-warning' style='margin-top:20px;'>
            {body}
        </div>
    </div>
    """.format(
        title=t("تنبيه مهم","Important Notice","Avis important"),
        body=t(
            "هذا التطبيق أُعد لأغراض أكاديمية وتعليمية فقط.<br>لا يُغني عن استشارة طبيب أو متخصص نفسي.",
            "This app was developed for academic and educational purposes only.<br>It does not replace a consultation with a doctor or mental health professional.",
            "Cette application a été développée à des fins académiques et éducatives uniquement.<br>Elle ne remplace pas une consultation avec un médecin ou un professionnel de la santé mentale."
        )
    ), unsafe_allow_html=True)

    if st.button(t("✅ فهمت، متابعة", "✅ Understood, Continue", "✅ Compris, continuer"), key="disc_ok", use_container_width=True):
        go("mode")

def page_mode():
    """Choose assessment type (mental health disorders or substance use placeholder)."""
    if st.button(t("‹ رجوع", "‹ Back", "‹ Retour"), key="back_mode"):
        go("disclaimer")

    st.markdown(f"""
    <div class='psyera-card' style='text-align:center;'>
        <div style='font-size:44px;'>🎯</div>
        <h2>{t('اختر نوع التقييم','Select Assessment Type',"Choisir le type d'évaluation")}</h2>
    </div>
    """, unsafe_allow_html=True)

    if st.button(t("🧠 الاضطرابات النفسية — 11 اضطراباً", "🧠 Mental Health Disorders — 11 Disorders", "🧠 Troubles mentaux — 11 troubles"), key="mode_mental", use_container_width=True):
        go("age_select")

    st.markdown(f"""
    <div class='psyera-card' style='text-align:center; opacity:0.4;'>
        <div style='font-size:40px;'>🔒</div>
        <p>{t('إدمان المواد — قريباً','Substance Use — Coming Soon','Usage de substances — Bientôt')}</p>
    </div>
    """, unsafe_allow_html=True)


def page_age_select():
    """Ask user for age group (15-24, 25-39, 40-54)."""
    if st.button(t("‹ رجوع", "‹ Back", "‹ Retour"), key="back_age"):
        go("mode")

    st.markdown(f"""
    <div class='psyera-card' style='text-align:center;'>
        <div style='font-size:44px;'>👤</div>
        <h2>{t('اختر فئتك العمرية','Select Your Age Group','Choisissez votre groupe d&#39;âge')}</h2>
    </div>
    """, unsafe_allow_html=True)

    ages = [
        ("15-24", t("الشباب — 15 إلى 24 سنة","Youth — 15 to 24 years","Jeunes — 15 à 24 ans")),
        ("25-39", t("البالغون — 25 إلى 39 سنة","Adults — 25 to 39 years","Adultes — 25 à 39 ans")),
        ("40-54", t("منتصف العمر — 40 إلى 54 سنة","Middle Age — 40 to 54 years","Âge mûr — 40 à 54 ans")),
    ]
    for code, label in ages:
        if st.button(label, key=f"age_{code}", use_container_width=True):
            st.session_state.age_group = code
            go("info")


def page_info():
    """Collect optional name, national ID (auto-extracts data), and required gender."""
    if st.button(t("‹ رجوع", "‹ Back", "‹ Retour"), key="back_info"):
        go("age_select")

    st.markdown(f"""
    <div class='psyera-card' style='text-align:center;'>
        <div style='font-size:44px;'>📋</div>
        <h2>{t('بياناتك الشخصية','Your Personal Info','Vos informations personnelles')}</h2>
        <p style='color:rgba(255,255,255,0.5); font-size:13px;'>{t('البيانات اختيارية وتُستخدم لتحسين التقييم','Data is optional and used to improve the assessment','Les données sont facultatives et utilisées pour améliorer l&#39;évaluation')}</p>
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input(t("الاسم (اختياري)", "Name (optional)", "Nom (facultatif)"), value=st.session_state.name, key="info_name",
                         placeholder=t("اكتب اسمك هنا...","Enter your name...","Entrez votre nom..."))
    nid = st.text_input(
        t("الرقم القومي (اختياري)", "National ID (optional)", "Numéro national (facultatif)"),
        value="",
        key="info_nid",
        placeholder=t("الرقم القومي (قريباً)", "National ID (soon)", "Numéro national (bientôt)"),
        max_chars=14,
        disabled=True,
    )
    st.caption(t(
        "ℹ️ أدخل الرقم القومي صحيحاً أو اتركه فارغاً للمتابعة",
        "ℹ️ Enter a valid national ID or leave it empty to continue",
        "ℹ️ Entrez un numéro national valide ou laissez-le vide pour continuer"
    ))

    nid_result = None
    if nid and len(nid) == 14:
        nid_result = extract_national_id(nid)
        if nid_result:
            st.success(f"✅ {t('تم التحقق','Verified','Vérifié')} — {t('العمر','Age','Âge')}: {nid_result['age']} | {t('الجنس','Gender','Genre')}: {t('ذكر','Male','Homme') if nid_result['gender']=='Male' else t('أنثى','Female','Femme')} | {nid_result['governorate']}")
        else:
            st.error(t("❌ رقم قومي غير صحيح","❌ Invalid national ID","❌ Numéro national invalide"))

    gender_options = [t("ذكر","Male","Homme"), t("أنثى","Female","Femme")]
    default_idx = 0
    if nid_result:
        default_idx = 0 if nid_result["gender"] == "Male" else 1
    elif st.session_state.gender:
        default_idx = 0 if st.session_state.gender == "Male" else 1

    gender_label = st.radio(t("الجنس *","Gender *","Genre *"), gender_options, index=default_idx, horizontal=True)
    gender_val = "Male" if gender_label in [t("ذكر","Male","Homme"), "Male"] else "Female"

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(t("متابعة ›","Continue ›","Suivant ›"), key="info_next", use_container_width=True):
        if nid and len(nid) == 14 and not nid_result:
            st.error(t("الرقم القومي غير صحيح — صححه أو اتركه فارغاً","Invalid national ID — correct it or leave empty","Numéro national invalide — corrigez-le ou laissez-le vide"))
        else:
            st.session_state.name = name
            st.session_state.national_id = nid
            st.session_state.gender = gender_val
            if nid_result:
                st.session_state.nid_age = nid_result["age"]
                st.session_state.nid_gender = nid_result["gender"]
                st.session_state.governorate = nid_result["governorate"]
            st.session_state.answers = {}
            st.session_state.quiz_pos = 0
            go("quiz")


def page_quiz():
    """Present dynamic questions, handle answers, and show duration screen when done."""
    questions = get_questions(st.session_state.age_group)
    flow = build_flow(questions, st.session_state.answers, st.session_state.gender)
    pos = st.session_state.quiz_pos
    total = len(flow) + 1

    if pos >= len(flow):
        st.markdown(f"""
        <div class='psyera-card' style='text-align:center;'>
            <div style='font-size:40px;'>⏱️</div>
            <h3>{t('منذ متى تعاني من هذه الأعراض؟','How long have you been experiencing these symptoms?','Depuis combien de temps ressentez-vous ces symptômes ?')}</h3>
        </div>
        """, unsafe_allow_html=True)

        durations = [
            ("dur_week", t("أسبوع أو أقل","A week or less","Une semaine ou moins")),
            ("dur_month", t("شهر تقريباً","About a month","Environ un mois")),
            ("dur_months", t("عدة أشهر","Several months","Plusieurs mois")),
            ("dur_year", t("سنة أو أكثر","A year or more","Un an ou plus")),
        ]

        for code, label in durations:
            with st.columns([9, 1])[0]:
                if st.button(label, key=f"dur_{code}", use_container_width=True):
                    st.session_state.duration = code
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button(t("‹ رجوع","‹ Back","‹ Retour"), key="quiz_back_dur"):
                st.session_state.quiz_pos -= 1
                st.rerun()
        with c2:
            if st.button(t("عرض النتائج ›","Show Results ›","Voir les résultats ›"), key="quiz_submit",
                        use_container_width=True, disabled=not st.session_state.duration):
                scores = score_answers(questions, st.session_state.answers, st.session_state.age_group)
                st.session_state.scores = scores
                try:
                    save_assessment(scores)
                except:
                    pass
                go("result")
        return

    qi = flow[pos]
    q = questions[qi]
    lang = st.session_state.lang
    if lang == "ar":
        q_text = q["textAr"]
    elif lang == "fr":
        q_text = q.get("textFr", q["textEn"])
    else:
        q_text = q["textEn"]
    name = st.session_state.name

    progress_val = pos / total
    st.progress(progress_val)
    st.markdown(f"<p style='color:rgba(255,255,255,0.5); font-size:13px; text-align:center;'>{t('السؤال','Question','Question')} {pos+1} {t('من','of','de')} {total}</p>", unsafe_allow_html=True)

    if q.get("category") == "sub_followup":
        st.markdown(f"""
        <div style='background:rgba(102,126,234,0.15); border-radius:10px; padding:12px; margin-bottom:12px; font-size:13px; color:rgba(255,255,255,0.8);'>
            {t('بما أنك ذكرت استخدام المواد، نود الاستفسار أكثر...','Since you mentioned substance use, we would like to ask more...','Puisque vous avez mentionné l&#39;usage de substances, nous aimerions en savoir plus...')}
        </div>
        """, unsafe_allow_html=True)

    display_text = f"{name}، {q_text}" if name and lang == "ar" else (f"{name}, {q_text}" if name else q_text)
    st.markdown(f"""
    <div class='psyera-card' style='text-align:center; min-height:120px; display:flex; align-items:center; justify-content:center;'>
        <p style='font-size:19px; line-height:1.7; margin:0;'>{display_text}</p>
    </div>
    """, unsafe_allow_html=True)

    cur = st.session_state.answers.get(qi, "")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button(f"✅ {t('نعم','Yes','Oui')}", key=f"ans_yes_{pos}", use_container_width=True):
            st.session_state.answers[qi] = "yes"
            st.session_state.quiz_pos += 1
            st.rerun()
    with c2:
        if st.button(f"🔸 {t('أحياناً','Sometimes','Parfois')}", key=f"ans_some_{pos}", use_container_width=True):
            st.session_state.answers[qi] = "sometimes"
            st.session_state.quiz_pos += 1
            st.rerun()
    with c3:
        if st.button(f"❌ {t('لا','No','Non')}", key=f"ans_no_{pos}", use_container_width=True):
            st.session_state.answers[qi] = "no"
            st.session_state.quiz_pos += 1
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if pos > 0:
        if st.button(t("‹ رجوع","‹ Back","‹ Retour"), key=f"quiz_back_{pos}"):
            st.session_state.quiz_pos -= 1
            st.rerun()


def _generate_pdf_report(scores):
    """Generate and offer a simple PDF report of the assessment results."""
    import io
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        have_reportlab = True
    except ImportError:
        have_reportlab = False

    if not have_reportlab:
        st.error(t(
            "❌ مكتبة reportlab غير مثبّتة — شغّل: pip install reportlab",
            "❌ reportlab not installed — run: pip install reportlab",
            "❌ reportlab non installé — exécutez: pip install reportlab"
        ))
        return

    lang = st.session_state.lang
    name = st.session_state.name or "—"
    gender = st.session_state.gender or "—"
    age_group = st.session_state.age_group or "—"
    duration = st.session_state.duration or "—"
    top = sorted([(k, v) for k, v in scores.items() if v >= 35], key=lambda x: x[1], reverse=True)[:3]

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    style_title  = ParagraphStyle("title",  fontName="Helvetica-Bold", fontSize=22, textColor=colors.HexColor("#667eea"), spaceAfter=6, alignment=1)
    style_sub    = ParagraphStyle("sub",    fontName="Helvetica",      fontSize=11, textColor=colors.HexColor("#aaaacc"), spaceAfter=4, alignment=1)
    style_head   = ParagraphStyle("head",   fontName="Helvetica-Bold", fontSize=13, textColor=colors.HexColor("#667eea"), spaceAfter=4)
    style_body   = ParagraphStyle("body",   fontName="Helvetica",      fontSize=11, textColor=colors.HexColor("#333333"), spaceAfter=4, leading=16)
    style_dis    = ParagraphStyle("dis",    fontName="Helvetica-Bold", fontSize=12, textColor=colors.HexColor("#222222"), spaceAfter=2)
    style_warn   = ParagraphStyle("warn",   fontName="Helvetica-Oblique", fontSize=10, textColor=colors.HexColor("#cc4444"), spaceAfter=2)

    from datetime import datetime
    date_str = datetime.now().strftime("%d/%m/%Y")

    story = []
    story.append(Paragraph("PsyEra", style_title))
    story.append(Paragraph("Bioinformatics Graduation Project 2026 — Port Said University", style_sub))
    story.append(Spacer(1, 0.4*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#667eea")))
    story.append(Spacer(1, 0.4*cm))

    label_name  = "الاسم" if lang=="ar" else ("Nom" if lang=="fr" else "Name")
    label_gen   = "الجنس" if lang=="ar" else ("Genre" if lang=="fr" else "Gender")
    label_age   = "الفئة العمرية" if lang=="ar" else ("Groupe d'âge" if lang=="fr" else "Age Group")
    label_dur   = "مدة الأعراض" if lang=="ar" else ("Durée des symptômes" if lang=="fr" else "Symptom Duration")
    label_date  = "تاريخ التقييم" if lang=="ar" else ("Date d'évaluation" if lang=="fr" else "Assessment Date")
    label_res   = "نتائج التقييم" if lang=="ar" else ("Résultats" if lang=="fr" else "Assessment Results")
    label_match = "تطابق الأعراض" if lang=="ar" else ("Correspondance" if lang=="fr" else "Symptom Match")
    label_warn  = ("⚠️ هذا التقرير لأغراض تعليمية فقط وليس بديلاً عن التشخيص الطبي المتخصص."
                   if lang=="ar" else
                   ("⚠️ Ce rapport est à des fins éducatives uniquement et ne remplace pas un diagnostic médical."
                    if lang=="fr" else
                    "⚠️ This report is for educational purposes only and is not a substitute for medical diagnosis."))

    for lbl, val in [(label_name, name), (label_gen, gender), (label_age, age_group), (label_dur, duration), (label_date, date_str)]:
        story.append(Paragraph(f"<b>{lbl}:</b>  {val}", style_body))

    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(label_res, style_head))
    story.append(Spacer(1, 0.2*cm))

    if not top:
        no_result = ("✅ لم تظهر نتائج واضحة. الأعراض غير كافية للتشخيص."
                     if lang=="ar" else
                     ("✅ Aucun résultat significatif. Les symptômes sont insuffisants pour un diagnostic."
                      if lang=="fr" else
                      "✅ No significant results. Symptoms are not sufficient for diagnosis."))
        story.append(Paragraph(no_result, style_body))
    else:
        for i, (key, pct) in enumerate(top, 1):
            dis = disorders.get(key, {})
            if lang == "ar":
                dis_name = dis.get("nameAr", key)
            elif lang == "fr":
                dis_name = dis.get("nameFr", dis.get("nameEn", key))
            else:
                dis_name = dis.get("nameEn", key)
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            story.append(Paragraph(f"{i}. {dis_name}", style_dis))
            story.append(Paragraph(f"{label_match}: {pct:.0f}%  [{bar}]", style_body))
            story.append(Spacer(1, 0.15*cm))

    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(label_warn, style_warn))

    doc.build(story)
    buf.seek(0)

    file_name = f"PsyEra_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    st.download_button(
        label=t("⬇️ اضغط هنا لتحميل الـ PDF", "⬇️ Click to download PDF", "⬇️ Cliquer pour télécharger le PDF"),
        data=buf,
        file_name=file_name,
        mime="application/pdf",
        use_container_width=True,
        key="pdf_download_btn",
    )


def page_result():
    """Display assessment results: pie chart, disorder cards, encouragement."""
    scores = st.session_state.scores or {}
    name = st.session_state.name
    name_str = f" {name}" if name else ""

    st.markdown(f"""
    <div class='psyera-card' style='text-align:center;'>
        <div style='font-size:44px;'>📊</div>
        <h2>{t('نتائج التقييم','Assessment Results','Résultats de l&#39;évaluation')}{name_str}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='psyera-card-warning'>
        ⚠️ {t('هذا التطبيق للأغراض التعليمية فقط وليس بديلاً عن التشخيص الطبي.','This app is for educational purposes only and is not a substitute for medical diagnosis.','Cette application est à des fins éducatives uniquement et ne remplace pas un diagnostic médical.')}
    </div>
    """, unsafe_allow_html=True)

    top_disorders = [(k, v) for k, v in scores.items() if v >= 35]
    top_disorders.sort(key=lambda x: x[1], reverse=True)
    top_disorders = top_disorders[:3]

    if not top_disorders:
        st.markdown(f"""
        <div class='psyera-card' style='text-align:center;'>
            <div style='font-size:40px;'>✅</div>
            <p style='font-size:16px; line-height:1.8;'>
                {t('الأعراض غير كافية للتشخيص','Symptoms are not sufficient for diagnosis','Les symptômes sont insuffisants pour un diagnostic')}<br>
                <span style='color:rgba(255,255,255,0.6); font-size:14px;'>
                    {t('لم تظهر نتائج واضحة. إذا كنت تشعر بضيق، تحدث مع متخصص.','No significant results. If you feel distressed, speak with a professional.','Aucun résultat significatif. Si vous vous sentez en détresse, parlez à un professionnel.')}
                </span>
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        import plotly.graph_objects as go_plotly
        total_score = sum(v for _, v in top_disorders)
        pie_labels = []
        for k, _ in top_disorders:
            if st.session_state.lang == "ar":
                pie_labels.append(disorders[k]["nameAr"])
            elif st.session_state.lang == "fr":
                pie_labels.append(disorders[k].get("nameFr", disorders[k]["nameEn"]))
            else:
                pie_labels.append(disorders[k]["nameEn"])
        pie_values = [v for _, v in top_disorders]
        pie_colors = [disorders[k]["color"] for k, _ in top_disorders]

        fig = go_plotly.Figure(data=[go_plotly.Pie(
            labels=pie_labels, values=pie_values, hole=0.5,
            marker=dict(colors=pie_colors, line=dict(color='#1a1535', width=2)),
            textfont=dict(color='white', size=12, family='Cairo'), showlegend=True,
        )])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=20, b=20, l=20, r=20), height=280,
            legend=dict(font=dict(color='white', family='Cairo'), bgcolor='rgba(0,0,0,0)'),
        )
        st.plotly_chart(fig, use_container_width=True)

        for key, pct in top_disorders:
            dis = disorders[key]
            if st.session_state.lang == "ar":
                name_dis = dis["nameAr"]
            elif st.session_state.lang == "fr":
                name_dis = dis.get("nameFr", dis["nameEn"])
            else:
                name_dis = dis["nameEn"]
            color = dis["color"]
            exp_key = f"show_{key}"
            if exp_key not in st.session_state:
                st.session_state[exp_key] = False

            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1);
                border-left:4px solid {color}; border-radius:14px; padding:16px 20px; margin-bottom:4px;'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <span style='font-size:16px; font-weight:700; color:white;'>{name_dis}</span>
                    <span style='font-size:15px; color:{color}; font-weight:700;'>{pct:.0f}%</span>
                </div>
                <div style='background:rgba(255,255,255,0.08); border-radius:50px; height:6px; margin-top:10px;'>
                    <div style='background:{color}; height:6px; border-radius:50px; width:{min(pct,100)}%;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            btn_label = t("▲ إخفاء", "▲ Hide", "▲ Masquer") if st.session_state[exp_key] else t("📖 تعرف على المرض", "📖 Learn More", "📖 En savoir plus")
            if st.button(btn_label, key=f"toggle_{key}"):
                st.session_state[exp_key] = not st.session_state[exp_key]
                st.rerun()

            if st.session_state[exp_key]:
                about_text = dis["aboutAr"] if st.session_state.lang == "ar" else (dis.get("aboutFr", dis["aboutEn"]) if st.session_state.lang == "fr" else dis["aboutEn"])
                meds_text = dis["meds"]
                st.markdown(
                    f'<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);'
                    'border-radius:12px;padding:16px 20px;margin-bottom:12px;">'
                    f'<p style="color:#a78bfa;font-size:12px;font-weight:700;text-transform:uppercase;margin:0 0 6px 0">'
                    + t("عن المرض","About","À propos") + '</p>'
                    f'<p style="color:rgba(255,255,255,0.88);font-size:14px;line-height:1.8;margin:0 0 12px 0">{about_text}</p>'
                    f'<p style="color:#a78bfa;font-size:12px;font-weight:700;text-transform:uppercase;margin:0 0 6px 0">'
                    + t("الأدوية الشائعة","Common Medications","Médicaments courants") + '</p>'
                    f'<p style="color:rgba(255,255,255,0.88);font-size:14px;line-height:1.8;white-space:pre-line;margin:0 0 10px 0">{meds_text}</p>'
                    '<div style="background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);'
                    'border-radius:8px;padding:10px 14px;">'
                    '<p style="color:#FCA5A5;font-size:12px;margin:0;">⚕️ '
                    + t("تنبيه: هذه أدوية للإرشاد فقط. يجب استشارة طبيب متخصص.","Warning: These are for guidance only. Always consult a specialist.","Avertissement : Ces médicaments sont à titre indicatif uniquement. Consultez toujours un spécialiste.")
                    + '</p></div></div>',
                    unsafe_allow_html=True
                )

    # Encouragement
    encourage_ar = [
        "تذكّر — طلب المساعدة هو أول خطوة نحو التحسن. أنت لست وحدك. 💙",
        "الاعتراف بما تشعر به يحتاج شجاعة. أنت أقوى مما تظن. 🌟",
        "الصحة النفسية جزء من صحتك العامة — اهتم بنفسك. 🌿",
        "كل يوم تحاول فيه هو انتصار. استمر. ✨",
    ]
    encourage_en = [
        "Remember — seeking help is the first step toward healing. You are not alone. 💙",
        "Acknowledging how you feel takes courage. You are stronger than you think. 🌟",
        "Mental health is part of your overall health — take care of yourself. 🌿",
        "Every day you try is a victory. Keep going. ✨",
    ]
    encourage_fr = [
        "Rappelez-vous — demander de l'aide est le premier pas vers la guérison. Vous n'êtes pas seul(e). 💙",
        "Reconnaître ce que vous ressentez demande du courage. Vous êtes plus fort(e) que vous ne le pensez. 🌟",
        "La santé mentale fait partie de votre santé globale — prenez soin de vous. 🌿",
        "Chaque jour où vous essayez est une victoire. Continuez. ✨",
    ]
    if st.session_state.lang == "ar":
        msg = random.choice(encourage_ar)
    elif st.session_state.lang == "fr":
        msg = random.choice(encourage_fr)
    else:
        msg = random.choice(encourage_en)
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,rgba(102,126,234,0.2),rgba(118,75,162,0.2)); border:1px solid rgba(102,126,234,0.4); border-radius:16px; padding:20px; text-align:center; margin:16px 0;'>
        <p style='font-size:15px; line-height:1.7; margin:0;'>{msg}</p>
    </div>
    """, unsafe_allow_html=True)

    if top_disorders:
        if st.button(t("📄 تحميل التقرير", "📄 Download Report", "📄 Télécharger le rapport"), key="result_pdf", use_container_width=True):
            _generate_pdf_report(scores)

    if st.button(t("🏠 القائمة الرئيسية","🏠 Home","🏠 Accueil"), key="result_home", use_container_width=True):
        for k in ["answers","quiz_pos","duration","scores","name","gender","national_id","nid_age","nid_gender","governorate","age_group"]:
            if k in ["answers"]:
                st.session_state[k] = {}
            elif k == "quiz_pos":
                st.session_state[k] = 0
            else:
                st.session_state[k] = None if k in ["age_group","nid_age","nid_gender","governorate","duration","scores"] else ""
        go("home")

    st.markdown(f"<div class='footer-text'>PsyEra v1.0 | Bioinformatics Graduation Project 2026</div>", unsafe_allow_html=True)


def save_assessment(scores):
    """Send full assessment data to Supabase (matches Flutter version)."""
    top = sorted([(k,v) for k,v in scores.items() if v >= 35], key=lambda x: x[1], reverse=True)[:3]
    data = {
        "name": st.session_state.name,
        "national_id": st.session_state.national_id,
        "gender": st.session_state.gender,
        "age": st.session_state.nid_age,
        "age_group": st.session_state.age_group,
        "governorate": st.session_state.governorate,
        "duration": st.session_state.duration,
        "lang": st.session_state.lang,
        "top_disorder": top[0][0] if len(top) > 0 else None,
        "top_score": top[0][1] if len(top) > 0 else None,
        "disorder_2": top[1][0] if len(top) > 1 else None,
        "score_2": top[1][1] if len(top) > 1 else None,
        "disorder_3": top[2][0] if len(top) > 2 else None,
        "score_3": top[2][1] if len(top) > 2 else None,
    }
    data = {k:v for k,v in data.items() if v is not None}
    SUPABASE_URL = "https://zrsqufwcpfiifchqbhvp.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpyc3F1ZndjcGZpaWZjaHFiaHZwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3NDgxMjgsImV4cCI6MjA5MTMyNDEyOH0.RDXOg_87waYn54jPNqIPK_yf0Czt_HiZRrE19wc1KRE"
    try:
        requests.post(
            f"{SUPABASE_URL}/rest/v1/assessments",
            headers={"Content-Type":"application/json","apikey":SUPABASE_KEY,"Authorization":f"Bearer {SUPABASE_KEY}","Prefer":"return=minimal"},
            json=data,
            timeout=10
        )
    except:
        pass



def page_chat():
    """AI chat assistant (Psyer/بصير) using Groq API, with daily limit and multilingual prompts."""
    import os
    try:
        GROQ_KEY = st.secrets["GROQ_KEY"]
    except Exception:
        GROQ_KEY = os.environ.get("GROQ_KEY", "")
    DAILY_LIMIT = 15
    SYSTEM_PROMPT = (
        'أنت "بصير" (psyer)، المساعد الذكي والودود لتطبيق PsyEra للصحة النفسية.\n\n'
        '# قواعد الرد الأساسية\n'
        '1. الإيجاز: رد بإيجاز وبدون تكرار أو إسهاب. قدم المعلومة الأساسية فقط، إلا إذا طلب المستخدم تفصيلاً.\n'
        '2. اللغة: مهم جدا انك تستخدم نفس لغة المستخدم بالضبط (عربي أو إنجليزي أو فرنسي) بطلاقة ودقة.\n'
        '3. التشجيع الذكي (يُستخدم فقط عند الاقتضاء):\n'
        '   - لا تضع جملة تشجيعية في نهاية كل رد. هذا ممل وغير طبيعي.\n'
        '   - استخدم التشجيع فقط عندما يشارك المستخدم شعوراً صعباً أو يصف أعراضاً أو يطلب دعماً.\n'
        '   - في باقي الأحوال (أسئلة معلوماتية، تعريف بمصطلح، سؤال عن التطبيق) لا حاجة لتشجيع.\n'
        '   - عند الحاجة للتشجيع، اصنع جملة قصيرة وطبيعية متناسبة مع سياق الحديث.\n\n'
        '# نطاق اختصاصك\n'
        '- أنت مخصص للصحة النفسية: التوعية والمعلومات العامة.\n'
        '- لا تقدم تشخيصاً نهائياً، بل معلومات عامة وتوجيهاً.\n'
        '- إذا سُئلت عن شيء خارج الصحة النفسية، اعتذر بلطف: "أنا بصير، ومهمتي الأساسية دعمك في رحلة الصحة النفسية فقط."\n\n'
        '# الأمراض التي يركز عليها التطبيق\n'
        'MDD، Bipolar I، GAD، Schizophrenia، Anorexia Nervosa، SUD، Panic Disorder، Social Anxiety، OCD، PTSD، BPD.\n'
        'إذا سأل: "التطبيق يركز على 11 اضطراباً منها الاكتئاب، ثنائي القطب، القلق، الفصام، وغيرها."\n\n'
        '# التعريف بالمشروع والفريق\n'
        'إذا سُئلت عن التطبيق أو المطورين بشكل عام:\n'
        '- مشروع تخرج 2026، قسم الحوسبة (Bioinformatics)، كلية العلوم، جامعة بورسعيد.\n'
        '- الفريق: أحمد السيد شلبي، أحمد أسامة عوض، أحمد محمد سماحة، إياد محمد طه، إسلام حسام الدين، لؤي السيد زكريا.\n'
        '- المشرفون: الدكتور محمد الجنيدي والدكتورة هدير عبد الحق راشد.\n\n'
        '# الأدوية\n'
        'إذا سُئلت عن دواء: قدم معلومات عامة مختصرة، ثم أضف:\n'
        '"تنبيه: هذه معلومات عامة فقط. لا تتناول أي دواء بدون وصفة طبية."\n\n'
        '# تذكير دوري\n'
        'مرة كل 10-15 رسالة فقط، أضف: "تذكر أنني مساعد وليس طبيباً، والتشخيص الدقيق يكون من متخصص."'
    )

    c1, c2, c3 = st.columns([1, 4, 1])
    with c1:
        if st.button(t("‹", "‹", "‹"), key="back_chat"):
            go("home")
    with c2:
        remaining = DAILY_LIMIT - st.session_state.chat_count
        st.markdown(
            "<div style='text-align:center;'>"
            "<span style='font-size:20px;'>🧠</span><br>"
            f"<b style='font-size:16px;'> {t('اسأل بصير', 'Ask the Psyer', 'Demander au Psyer')}</b><br>"
            f"<span style='color:rgba(255,255,255,0.5); font-size:11px;'>{t('متخصص في الصحة النفسية', 'Mental Health Specialist', 'Spécialiste en santé mentale')}</span>"
            "</div>",
            unsafe_allow_html=True
        )
    with c3:
        color = "#EF4444" if remaining <= 5 else "#667eea"
        st.markdown(f"<div style='text-align:center; color:{color}; font-weight:bold; font-size:13px; padding-top:8px;'>{remaining}/{DAILY_LIMIT}</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08);margin:8px 0;'>", unsafe_allow_html=True)

    if not st.session_state.chat_messages:
        if st.session_state.lang == "ar":
            suggestions = ["ما هو الاكتئاب؟", "أعراض القلق", "ما هو OCD؟", "كيف أساعد نفسي؟"]
            welcome = "مرحباً! أنا بصير 👋<br>أنا هنا لدعمك، تحدث معي براحتك"
        elif st.session_state.lang == "fr":
            suggestions = ["Qu'est-ce que la dépression ?", "Symptômes d'anxiété", "Qu'est-ce que le TOC ?", "Comment m'aider ?"]
            welcome = "salut ! Je suis le Psyer 👋<br>Je suis là pour vous soutenir, parlez-moi librement"
        else:
            suggestions = ["What is MDD?", "Anxiety symptoms", "What is OCD?", "How to cope?"]
            welcome = "Hello! I'm Psyer 👋<br>I'm here to support you, speak freely"

        st.markdown(
            f"<div style='text-align:center; padding:32px;'>"
            f"<div style='font-size:60px;'>🧠</div>"
            f"<p style='color:rgba(255,255,255,0.7); font-size:15px; line-height:1.6;'>{welcome}</p>"
            "</div>",
            unsafe_allow_html=True
        )

        cols = st.columns(2)
        for i, sug in enumerate(suggestions):
            with cols[i % 2]:
                if st.button(sug, key=f"sug_{i}", use_container_width=True):
                    st.session_state.chat_messages.append({"role": "user", "content": sug})
                    st.session_state.chat_count += 1
                    with st.spinner(t("بصير يفكر...", "Psyer is thinking...", "Le Psyer réfléchit...")):
                        reply = call_groq(GROQ_KEY, SYSTEM_PROMPT, st.session_state.chat_messages)
                    st.session_state.chat_messages.append({"role": "assistant", "content": reply})
                    st.rerun()
    else:
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f"<div style='display:flex; justify-content:flex-end; margin:6px 0;'><div class='chat-bubble-user'>{msg['content']}</div></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='display:flex; align-items:flex-end; gap:8px; margin:6px 0;'><span style='font-size:20px;'>🧠</span><div class='chat-bubble-bot'>{msg['content']}</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if remaining <= 0:
        st.warning(t("⚠️ وصلت للحد اليومي (30 رسالة). عود غداً!", "⚠️ You reached the daily limit (30 messages). Come back tomorrow!", "⚠️ Vous avez atteint la limite quotidienne (30 messages). Revenez demain !"))
    else:
        user_input = st.chat_input(t("اكتب سؤالك هنا...", "Ask your question...", "Écrivez votre question..."))
        if user_input:
            st.session_state.chat_messages.append({"role": "user", "content": user_input})
            st.session_state.chat_count += 1
            with st.spinner(t("بصير يفكر...", "Psyer is thinking...", "Le Psyer réfléchit...")):
                reply = call_groq(GROQ_KEY, SYSTEM_PROMPT, st.session_state.chat_messages)
            st.session_state.chat_messages.append({"role": "assistant", "content": reply})
            st.rerun()


def call_groq(api_key, system_prompt, messages):
    """Call Groq API (Qwen model) and return cleaned assistant response."""
    import re
    try:
        msgs = [{"role":"system","content":system_prompt}] + messages
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization":f"Bearer {api_key}","Content-Type":"application/json"},
            json={"model":"qwen/qwen3-32b","messages":msgs,"max_tokens":500,"temperature":0.2},
            timeout=30
        )
        if res.status_code == 200:
            text = res.json()["choices"][0]["message"]["content"]
            text = re.sub(r'<think>[\s\S]*?</think>', '', text).strip()
            return text
        return f"Error {res.status_code}"
    except Exception as e:
        return str(e)


def page_stats():
    """Fetch aggregated statistics from Supabase and display a horizontal bar chart."""
    if st.button(t("‹ رجوع","‹ Back","‹ Retour"), key="back_stats"):
        go("home")

    st.markdown(f"""
    <div class='psyera-card' style='text-align:center;'>
        <div style='font-size:40px;'>📊</div>
        <h2>{t('إحصائيات المستخدمين','User Statistics','Statistiques des utilisateurs')}</h2>
    </div>
    """, unsafe_allow_html=True)

    SUPABASE_URL = "https://zrsqufwcpfiifchqbhvp.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpyc3F1ZndjcGZpaWZjaHFiaHZwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3NDgxMjgsImV4cCI6MjA5MTMyNDEyOH0.RDXOg_87waYn54jPNqIPK_yf0Czt_HiZRrE19wc1KRE"

    with st.spinner(t("جارٍ تحميل البيانات...","Loading data...","Chargement des données...")):
        try:
            res = requests.get(
                f"{SUPABASE_URL}/rest/v1/assessments?select=top_disorder,disorder_2,disorder_3",
                headers={"apikey":SUPABASE_KEY,"Authorization":f"Bearer {SUPABASE_KEY}"},
                timeout=10
            )
            if res.status_code == 200:
                data = res.json()
                counts = {}
                total = 0
                for row in data:
                    for field in ["top_disorder","disorder_2","disorder_3"]:
                        val = row.get(field)
                        if val:
                            counts[val] = counts.get(val, 0) + 1
                            total += 1

                if not counts:
                    st.info(t("لا توجد بيانات بعد","No data yet","Pas encore de données"))
                else:
                    percentages = {k: round(v/total*100, 1) for k, v in counts.items()}
                    sorted_pct = sorted(percentages.items(), key=lambda x: x[1], reverse=True)

                    import plotly.graph_objects as go_plotly
                    labels = []
                    for k, _ in sorted_pct:
                        if k not in disorders:
                            continue
                        if st.session_state.lang == "ar":
                            labels.append(disorders[k]["nameAr"])
                        elif st.session_state.lang == "fr":
                            labels.append(disorders[k].get("nameFr", disorders[k]["nameEn"]))
                        else:
                            labels.append(disorders[k]["nameEn"])
                    values = [v for k, v in sorted_pct if k in disorders]
                    colors = [disorders[k]["color"] for k, _ in sorted_pct if k in disorders]

                    fig = go_plotly.Figure(go_plotly.Bar(
                        x=values, y=labels, orientation='h',
                        marker=dict(color=colors),
                        text=[f"{v}%" for v in values],
                        textposition='outside',
                        textfont=dict(color='white', family='Cairo'),
                    ))
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(showgrid=False, color='rgba(255,255,255,0.3)'),
                        yaxis=dict(color='white', tickfont=dict(family='Cairo')),
                        margin=dict(l=10, r=60, t=10, b=10), height=400,
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(t("فشل تحميل البيانات","Failed to load data","Échec du chargement des données"))
        except Exception as e:
            st.error(str(e))


def page_forecast():
    """Display historical and forecast prevalence data (Egypt/World) for selected disorders."""
    if st.button(t("‹ رجوع","‹ Back","‹ Retour"), key="back_forecast"):
        go("home")

    st.markdown(f"""
    <div class='psyera-card' style='text-align:center;'>
        <div style='font-size:40px;'>📈</div>
        <h2>{t('توقعات انتشار الاضطرابات','Mental Health Disorder Forecasts','Prévisions des troubles mentaux')}</h2>
    </div>
    """, unsafe_allow_html=True)

    from data.forecast_data import EGYPT_DATA, WORLD_DATA

    region_options = [t("مصر","Egypt","Égypte"), t("العالم","World","Monde")]
    region_selected = st.radio(t("المنطقة","Region","Région"), region_options, horizontal=True)
    data_source = EGYPT_DATA if region_selected == t("مصر","Egypt","Égypte") else WORLD_DATA

    disorder_names = list(data_source.keys())
    if st.session_state.lang == "ar":
        display_names = {d: d for d in disorder_names}
    elif st.session_state.lang == "fr":
        mapping = {
            'Major depressive disorder': 'Trouble dépressif majeur',
            'Anxiety disorders': 'Troubles anxieux',
            'Bipolar disorder': 'Trouble bipolaire',
            'Schizophrenia': 'Schizophrénie',
            'Anorexia nervosa': 'Anorexie mentale',
            'Substance use disorders': "Troubles liés à l'usage de substances"
        }
        display_names = {k: mapping.get(k, k) for k in disorder_names}
    else:
        display_names = {k: k for k in disorder_names}
    selected_display = st.selectbox(t("اختر الاضطراب","Select Disorder","Choisir le trouble"), list(display_names.values()))
    selected = [k for k, v in display_names.items() if v == selected_display][0]

    if selected:
        dis_data = data_source[selected]
        historical = dis_data["historical"]
        forecast = dis_data["forecast"]

        import plotly.graph_objects as go_plotly
        hist_years = list(historical.keys())
        hist_vals = list(historical.values())
        fore_years = list(forecast.keys())
        fore_vals = list(forecast.values())

        fig = go_plotly.Figure()
        fig.add_trace(go_plotly.Scatter(
            x=hist_years, y=hist_vals, mode='lines+markers',
            name=t('بيانات تاريخية','Historical','Historique'), line=dict(color='#667eea', width=2), marker=dict(size=4),
        ))
        fig.add_trace(go_plotly.Scatter(
            x=fore_years, y=fore_vals, mode='lines+markers',
            name=t('توقعات','Forecast','Prévision'), line=dict(color='#f093fb', width=2, dash='dash'), marker=dict(size=4),
        ))
        fig.add_vline(x=2023, line_dash="dot", line_color="rgba(255,255,255,0.3)")

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(color='rgba(255,255,255,0.5)', gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(color='rgba(255,255,255,0.5)', gridcolor='rgba(255,255,255,0.05)'),
            legend=dict(font=dict(color='white'), bgcolor='rgba(0,0,0,0)'),
            margin=dict(l=10, r=10, t=20, b=10), height=350,
        )
        st.plotly_chart(fig, use_container_width=True)

        last_hist = hist_vals[-1]
        last_fore = fore_vals[-1]
        change_pct = (last_fore - last_hist) / last_hist * 100

        c1, c2, c3 = st.columns(3)
        with c1: st.metric(t("آخر بيانات (2023)","Last Data (2023)","Dernières données (2023)"), f"{last_hist:,}")
        with c2: st.metric(t("توقع 2035","Forecast 2035","Prévision 2035"), f"{last_fore:,}")
        with c3: st.metric(t("التغيير المتوقع","Expected Change","Changement attendu"), f"{change_pct:+.1f}%")

    st.markdown(f"<div class='footer-text'>PsyEra v1.0 | Bioinformatics Graduation Project 2026</div>", unsafe_allow_html=True)


def page_doctor():
    """Placeholder screen for the doctor/psychiatrist section (coming soon)."""
    if st.button(t("‹ رجوع", "‹ Back", "‹ Retour"), key="back_doctor"):
        go("home")

    st.markdown(f"""
    <div class='psyera-card' style='text-align:center;'>
        <div style='font-size:44px;'>👨‍⚕️</div>
        <h2>{t('كلم الدوك','Talk to the Doc','Parler au Doc')}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='psyera-card' style='text-align:center; padding:60px 28px;'>
        <div style='font-size:64px;'>🚧</div>
        <br>
        <p style='font-size:18px; color:rgba(255,255,255,0.7); line-height:1.6;'>
            {t('هذه الصفحة قيد التطوير<br>ستتوفر قريباً!',
               'This page is under development<br>Coming soon!',
               'Cette page est en développement<br>Bientôt disponible!')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div class='footer-text'>PsyEra v1.0 | Bioinformatics Graduation Project 2026</div>", unsafe_allow_html=True)


def page_reviews():
    """Placeholder screen for user reviews / ratings (coming soon)."""
    if st.button(t("‹ رجوع", "‹ Back", "‹ Retour"), key="back_reviews"):
        go("home")

    st.markdown(f"""
    <div class='psyera-card' style='text-align:center;'>
        <div style='font-size:44px;'>⭐</div>
        <h2>{t('التقييمات','Reviews','Évaluations')}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='psyera-card' style='text-align:center; padding:60px 28px;'>
        <div style='font-size:64px;'>🚧</div>
        <br>
        <p style='font-size:18px; color:rgba(255,255,255,0.7); line-height:1.6;'>
            {t('هذه الصفحة قيد التطوير<br>ستتوفر قريباً!',
               'This page is under development<br>Coming soon!',
               'Cette page est en développement<br>Bientôt disponible!')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div class='footer-text'>PsyEra v1.0 | Bioinformatics Graduation Project 2026</div>", unsafe_allow_html=True)


# ─── Router ───────────────────────────────────────────────────────────────────
page = st.session_state.page
if page == "home":
    page_home()
elif page == "about":
    page_about()
elif page == "disclaimer":
    page_disclaimer()
elif page == "mode":
    page_mode()
elif page == "age_select":
    page_age_select()
elif page == "info":
    page_info()
elif page == "quiz":
    page_quiz()
elif page == "result":
    page_result()
elif page == "chat":
    page_chat()
elif page == "stats":
    page_stats()
elif page == "forecast":
    page_forecast()
elif page == "doctor":
    page_doctor()
elif page == "reviews":
    page_reviews()
else:
    go("home")