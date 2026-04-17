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

# ─── CSS ──────────────────────────────────────────────────────────────────────
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

/* Stars background effect */
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

/* Cards */
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

/* Buttons */
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

/* Inputs */
.stTextInput > div > div > input, .stSelectbox > div > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 14px !important;
    color: white !important;
    font-family: 'Cairo', sans-serif !important;
}

/* Progress bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #667eea, #764ba2) !important;
    border-radius: 50px !important;
}

/* Radio */
.stRadio > div { gap: 10px; }
.stRadio > div > label { color: rgba(255,255,255,0.8) !important; }

/* Text */
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

/* Answer buttons */
.ans-btn-yes { background: rgba(16,185,129,0.2) !important; border: 2px solid #10B981 !important; }
.ans-btn-sometimes { background: rgba(245,158,11,0.2) !important; border: 2px solid #F59E0B !important; }
.ans-btn-no { background: rgba(239,68,68,0.2) !important; border: 2px solid #EF4444 !important; }

/* Chat */
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

/* Metric cards */
.metric-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 16px;
    text-align: center;
}

/* Nav pills */
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

# ─── Session State Init ────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "home",
        "lang": "ar",
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

L = st.session_state.lang
IS_AR = L == "ar"

def t(ar, en):
    return ar if IS_AR else en

def go(page):
    st.session_state.page = page
    st.rerun()

# ─── National ID ──────────────────────────────────────────────────────────────
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

# ─── Pages ────────────────────────────────────────────────────────────────────

def page_home():
    # Header bar
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if st.button("🌐 AR" if not IS_AR else "🌐 EN", key="lang_btn"):
            st.session_state.lang = "en" if IS_AR else "ar"
            st.rerun()
    with c3:
        if st.button(t("عن التطبيق", "About"), key="about_btn"):
            go("about")

    st.markdown("<br>", unsafe_allow_html=True)

    # Logo & Title
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        try:
            st.image("assets/psyera_logo_home.png", width=120)
        except FileNotFoundError:
            st.markdown("<div style='font-size:72px; text-align:center;'>🧠</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; margin:0 0 4px 0;'>
        <span style='font-size:46px; font-weight:900; background: linear-gradient(90deg,#667eea,#f093fb,#764ba2); -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>PsyEra</span>
    </div>
    """, unsafe_allow_html=True)

    subtitle = t("الكشف المبكر عن الاضطرابات النفسية", "Early Detection of Mental Health Disorders")
    st.markdown(f"<p style='text-align:center; color:rgba(255,255,255,0.65); font-size:15px;'>{subtitle}</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(t("🧠 ابدأ التقييم", "🧠 Start Assessment"), key="start_btn",
                 use_container_width=True):
        go("disclaimer")

    st.markdown("<br style='margin:4px'>", unsafe_allow_html=True)

    if st.button(t("🤖 اسأل الدوك", "🤖 Ask the Doc"), key="chat_btn",
                 use_container_width=True):
        go("chat")

    st.markdown("<br style='margin:4px'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button(t("📊 إحصائيات", "📊 Statistics"), key="stats_btn", use_container_width=True):
            go("stats")
    with col2:
        if st.button(t("📈 توقعات الانتشار", "📈 Forecasts"), key="forecast_btn", use_container_width=True):
            go("forecast")

    st.markdown(f"<div class='footer-text'>PsyEra v1.0 | Bioinformatics Graduation Project 2026</div>", unsafe_allow_html=True)


def page_about():
    if st.button(t("‹ رجوع", "‹ Back"), key="back_about"):
        go("home")

    st.markdown(f"""
    <div class='psyera-card' style='text-align:center;'>
        <div style='font-size:44px;'>🧠</div>
        <h2 style='margin:8px 0;'>PsyEra v1.0</h2>
        <p style='color:rgba(255,255,255,0.6); font-size:13px;'>Bioinformatics Graduation Project 2026<br>Faculty of Science — Port Said University</p>
    </div>
    """, unsafe_allow_html=True)

    team = ["أحمد السيد شلبي","أحمد أسامة عوض","أحمد محمد سماحة","إياد محمد طه","إسلام حسام الدين","لؤي السيد زكريا"] if IS_AR else \
           ["Ahmed Elsayed Shalaby","Ahmed Osama Awad","Ahmed Mohammed Samaha","Eyad Mohammed Taha","Eslam Hossam Eldin","Loay Elsayed Zakaria"]
    supervisors = ["د. محمد الجنيدي","د. هدير عبد الحق راشد"] if IS_AR else ["Dr. Mohammed Elgenedy","Dr. Hadeer Abd Elhak Rashed"]

    st.markdown(f"<div class='psyera-card'><b style='color:#667eea;'>{t('فريق العمل','Team')}</b><br><br>" +
                "<br>".join([f"• {m}" for m in team]) + "</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='psyera-card'><b style='color:#667eea;'>{t('إشراف','Supervision')}</b><br><br>" +
                "<br>".join([f"• {s}" for s in supervisors]) + "</div>", unsafe_allow_html=True)

    try:
        col = st.columns([1,2,1])[1]
        with col:
            st.image("assets/faculty_logo.png", width=120)
    except:
        pass


def page_disclaimer():
    if st.button(t("‹ رجوع", "‹ Back"), key="back_disc"):
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
        title=t("تنبيه مهم","Important Notice"),
        body=t(
            "هذا التطبيق أُعد لأغراض أكاديمية وتعليمية فقط.<br>لا يُغني عن استشارة طبيب أو متخصص نفسي.",
            "This app was developed for academic and educational purposes only.<br>It does not replace a consultation with a doctor or mental health professional."
        )
    ), unsafe_allow_html=True)

    if st.button(t("✅ فهمت، متابعة", "✅ Understood, Continue"), key="disc_ok", use_container_width=True):
        go("mode")


def page_mode():
    if st.button(t("‹ رجوع", "‹ Back"), key="back_mode"):
        go("disclaimer")

    st.markdown(f"""
    <div class='psyera-card' style='text-align:center;'>
        <div style='font-size:44px;'>🎯</div>
        <h2>{t('اختر نوع التقييم','Select Assessment Type')}</h2>
    </div>
    """, unsafe_allow_html=True)

    if st.button(f"🧠 {t('الاضطرابات النفسية — 11 اضطراباً','Mental Health Disorders — 11 Disorders')}", key="mode_mental", use_container_width=True):
        go("age_select")

    st.markdown(f"""
    <div class='psyera-card' style='text-align:center; opacity:0.4;'>
        <div style='font-size:40px;'>🔒</div>
        <p>{t('إدمان المواد — قريباً','Substance Use — Coming Soon')}</p>
    </div>
    """, unsafe_allow_html=True)


def page_age_select():
    if st.button(t("‹ رجوع", "‹ Back"), key="back_age"):
        go("mode")

    st.markdown(f"""
    <div class='psyera-card' style='text-align:center;'>
        <div style='font-size:44px;'>👤</div>
        <h2>{t('اختر فئتك العمرية','Select Your Age Group')}</h2>
    </div>
    """, unsafe_allow_html=True)

    ages = [
        ("15-24", t("الشباب — 15 إلى 24 سنة","Youth — 15 to 24 years")),
        ("25-39", t("البالغون — 25 إلى 39 سنة","Adults — 25 to 39 years")),
        ("40-54", t("منتصف العمر — 40 إلى 54 سنة","Middle Age — 40 to 54 years")),
    ]
    for code, label in ages:
        if st.button(label, key=f"age_{code}", use_container_width=True):
            st.session_state.age_group = code
            go("info")


def page_info():
    if st.button(t("‹ رجوع", "‹ Back"), key="back_info"):
        go("age_select")

    st.markdown(f"""
    <div class='psyera-card' style='text-align:center;'>
        <div style='font-size:44px;'>📋</div>
        <h2>{t('بياناتك الشخصية','Your Personal Info')}</h2>
        <p style='color:rgba(255,255,255,0.5); font-size:13px;'>{t('البيانات اختيارية وتُستخدم لتحسين التقييم','Data is optional and used to improve the assessment')}</p>
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input(t("الاسم (اختياري)", "Name (optional)"), value=st.session_state.name, key="info_name",
                         placeholder=t("اكتب اسمك هنا...","Enter your name..."))

    nid = st.text_input(t("الرقم القومي (اختياري)", "National ID (optional)"), value=st.session_state.national_id, key="info_nid",
                        placeholder="14 " + t("رقم","digits"), max_chars=14)

    nid_result = None
    if nid and len(nid) == 14:
        nid_result = extract_national_id(nid)
        if nid_result:
            st.success(f"✅ {t('تم التحقق','Verified')} — {t('العمر','Age')}: {nid_result['age']} | {t('الجنس','Gender')}: {t('ذكر','Male') if nid_result['gender']=='Male' else t('أنثى','Female')} | {nid_result['governorate']}")
        else:
            st.error(t("❌ رقم قومي غير صحيح","❌ Invalid national ID"))

    gender_options = [t("ذكر","Male"), t("أنثى","Female")]
    default_idx = 0
    if nid_result:
        default_idx = 0 if nid_result["gender"] == "Male" else 1
    elif st.session_state.gender:
        default_idx = 0 if st.session_state.gender == "Male" else 1

    gender_label = st.radio(t("الجنس *","Gender *"), gender_options, index=default_idx, horizontal=True)
    gender_val = "Male" if gender_label == t("ذكر","Male") else "Female"

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(t("متابعة ›","Continue ›"), key="info_next", use_container_width=True):
        if nid and len(nid) == 14 and not nid_result:
            st.error(t("الرقم القومي غير صحيح — صححه أو اتركه فارغاً","Invalid national ID — correct it or leave empty"))
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
    questions = get_questions(st.session_state.age_group)
    flow = build_flow(questions, st.session_state.answers, st.session_state.gender)
    pos = st.session_state.quiz_pos
    total = len(flow) + 1  # +1 for duration question

    # Duration screen
    if pos >= len(flow):
        st.markdown(f"""
        <div class='psyera-card' style='text-align:center;'>
            <div style='font-size:40px;'>⏱️</div>
            <h3>{t('منذ متى تعاني من هذه الأعراض؟','How long have you been experiencing these symptoms?')}</h3>
        </div>
        """, unsafe_allow_html=True)

        durations = [
            ("dur_week", t("أسبوع أو أقل","A week or less")),
            ("dur_month", t("شهر تقريباً","About a month")),
            ("dur_months", t("عدة أشهر","Several months")),
            ("dur_year", t("سنة أو أكثر","A year or more")),
        ]

        for code, label in durations:
            is_selected = st.session_state.duration == code
            style = "background: rgba(102,126,234,0.3); border: 2px solid #667eea;" if is_selected else ""
            col1, col2 = st.columns([9, 1])
            with col1:
                if st.button(label, key=f"dur_{code}", use_container_width=True):
                    st.session_state.duration = code
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button(t("‹ رجوع","‹ Back"), key="quiz_back_dur"):
                st.session_state.quiz_pos -= 1
                st.rerun()
        with c2:
            if st.button(t("عرض النتائج ›","Show Results ›"), key="quiz_submit",
                        use_container_width=True, disabled=not st.session_state.duration):
                # Calculate scores
                scores = score_answers(questions, st.session_state.answers, st.session_state.age_group)
                st.session_state.scores = scores
                # Save to supabase (optional, silent fail)
                try:
                    save_assessment(scores)
                except:
                    pass
                go("result")
        return

    qi = flow[pos]
    q = questions[qi]
    q_text = q["textAr"] if IS_AR else q["textEn"]
    name = st.session_state.name

    # Progress
    progress_val = pos / total
    st.progress(progress_val)
    st.markdown(f"<p style='color:rgba(255,255,255,0.5); font-size:13px; text-align:center;'>{t('السؤال','Question')} {pos+1} {t('من','of')} {total}</p>", unsafe_allow_html=True)

    if q.get("category") == "sub_followup":
        st.markdown(f"""
        <div style='background:rgba(102,126,234,0.15); border-radius:10px; padding:12px; margin-bottom:12px; font-size:13px; color:rgba(255,255,255,0.8);'>
            {t('بما أنك ذكرت استخدام المواد، نود الاستفسار أكثر...','Since you mentioned substance use, we would like to ask more...')}
        </div>
        """, unsafe_allow_html=True)

    display_text = f"{name}، {q_text}" if name and IS_AR else (f"{name}, {q_text}" if name else q_text)
    st.markdown(f"""
    <div class='psyera-card' style='text-align:center; min-height:120px; display:flex; align-items:center; justify-content:center;'>
        <p style='font-size:19px; line-height:1.7; margin:0;'>{display_text}</p>
    </div>
    """, unsafe_allow_html=True)

    cur = st.session_state.answers.get(qi, "")

    c1, c2, c3 = st.columns(3)
    with c1:
        selected = cur == "yes"
        style = "border: 2px solid #10B981 !important; background: rgba(16,185,129,0.2) !important;" if selected else ""
        if st.button(f"✅ {t('نعم','Yes')}", key=f"ans_yes_{pos}", use_container_width=True):
            st.session_state.answers[qi] = "yes"
            st.session_state.quiz_pos += 1
            st.rerun()
    with c2:
        if st.button(f"🔸 {t('أحياناً','Sometimes')}", key=f"ans_some_{pos}", use_container_width=True):
            st.session_state.answers[qi] = "sometimes"
            st.session_state.quiz_pos += 1
            st.rerun()
    with c3:
        if st.button(f"❌ {t('لا','No')}", key=f"ans_no_{pos}", use_container_width=True):
            st.session_state.answers[qi] = "no"
            st.session_state.quiz_pos += 1
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if pos > 0:
        if st.button(t("‹ رجوع","‹ Back"), key=f"quiz_back_{pos}"):
            st.session_state.quiz_pos -= 1
            st.rerun()


def page_result():
    scores = st.session_state.scores or {}
    name = st.session_state.name
    name_str = f" {name}" if name else ""

    # Header
    st.markdown(f"""
    <div class='psyera-card' style='text-align:center;'>
        <div style='font-size:44px;'>📊</div>
        <h2>{t('نتائج التقييم','Assessment Results')}{name_str}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='psyera-card-warning'>
        ⚠️ {t('هذا التطبيق للأغراض التعليمية فقط وليس بديلاً عن التشخيص الطبي.','This app is for educational purposes only and is not a substitute for medical diagnosis.')}
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
                {t('الأعراض غير كافية للتشخيص','Symptoms are not sufficient for diagnosis')}<br>
                <span style='color:rgba(255,255,255,0.6); font-size:14px;'>
                    {t('لم تظهر نتائج واضحة. إذا كنت تشعر بضيق، تحدث مع متخصص.','No significant results. If you feel distressed, speak with a professional.')}
                </span>
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Pie chart using st.plotly_chart or simple bars
        import plotly.graph_objects as go_plotly
        total_score = sum(v for _, v in top_disorders)
        pie_labels = [disorders[k]["nameAr"] if IS_AR else disorders[k]["nameEn"] for k, _ in top_disorders]
        pie_values = [v for _, v in top_disorders]
        pie_colors = [disorders[k]["color"] for k, _ in top_disorders]

        fig = go_plotly.Figure(data=[go_plotly.Pie(
            labels=pie_labels,
            values=pie_values,
            hole=0.5,
            marker=dict(colors=pie_colors, line=dict(color='#1a1535', width=2)),
            textfont=dict(color='white', size=12, family='Cairo'),
            showlegend=True,
        )])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=20, b=20, l=20, r=20),
            height=280,
            legend=dict(font=dict(color='white', family='Cairo'), bgcolor='rgba(0,0,0,0)'),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Disorder cards — using st.button toggle instead of expander
        for key, pct in top_disorders:
            dis = disorders[key]
            name_dis = dis["nameAr"] if IS_AR else dis["nameEn"]
            color = dis["color"]
            exp_key = f"show_{key}"
            if exp_key not in st.session_state:
                st.session_state[exp_key] = False

            # Header card
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

            btn_label = t("▲ إخفاء", "▲ Hide") if st.session_state[exp_key] else t("📖 تعرف على المرض", "📖 Learn More")
            if st.button(btn_label, key=f"toggle_{key}"):
                st.session_state[exp_key] = not st.session_state[exp_key]
                st.rerun()

            if st.session_state[exp_key]:
                st.markdown(
                    '<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);'
                    'border-radius:12px;padding:16px 20px;margin-bottom:12px;">'
                    '<p style="color:#a78bfa;font-size:12px;font-weight:700;text-transform:uppercase;margin:0 0 6px 0">'
                    + t("عن المرض","About") + '</p>'
                    '<p style="color:rgba(255,255,255,0.88);font-size:14px;line-height:1.8;margin:0 0 12px 0">'
                    + (dis["aboutAr"] if IS_AR else dis["aboutEn"]) + '</p>'
                    '<p style="color:#a78bfa;font-size:12px;font-weight:700;text-transform:uppercase;margin:0 0 6px 0">'
                    + t("الأدوية الشائعة","Common Medications") + '</p>'
                    '<p style="color:rgba(255,255,255,0.88);font-size:14px;line-height:1.8;white-space:pre-line;margin:0 0 10px 0">'
                    + dis["meds"] + '</p>'
                    '<div style="background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);'
                    'border-radius:8px;padding:10px 14px;">'
                    '<p style="color:#FCA5A5;font-size:12px;margin:0;">⚕️ '
                    + t("تنبيه: هذه أدوية للإرشاد فقط. يجب استشارة طبيب متخصص.","Warning: These are for guidance only. Always consult a specialist.")
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
    msg = random.choice(encourage_ar if IS_AR else encourage_en)
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,rgba(102,126,234,0.2),rgba(118,75,162,0.2)); border:1px solid rgba(102,126,234,0.4); border-radius:16px; padding:20px; text-align:center; margin:16px 0;'>
        <p style='font-size:15px; line-height:1.7; margin:0;'>{msg}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(t("🏠 القائمة الرئيسية","🏠 Home"), key="result_home", use_container_width=True):
        # Reset quiz state
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
    top = sorted([(k,v) for k,v in scores.items() if v >= 35], key=lambda x: x[1], reverse=True)[:3]
    data = {
        "top_disorder": top[0][0] if len(top) > 0 else None,
        "disorder_2": top[1][0] if len(top) > 1 else None,
        "disorder_3": top[2][0] if len(top) > 2 else None,
        "age_group": st.session_state.age_group,
        "gender": st.session_state.gender,
        "governorate": st.session_state.governorate,
    }
    SUPABASE_URL = "https://zrsqufwcpfiifchqbhvp.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpyc3F1ZndjcGZpaWZjaHFiaHZwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3NDgxMjgsImV4cCI6MjA5MTMyNDEyOH0.RDXOg_87waYn54jPNqIPK_yf0Czt_HiZRrE19wc1KRE"
    requests.post(
        f"{SUPABASE_URL}/rest/v1/assessments",
        headers={"Content-Type":"application/json","apikey":SUPABASE_KEY,"Authorization":f"Bearer {SUPABASE_KEY}","Prefer":"return=minimal"},
        json=data,
        timeout=10
    )


def page_chat():
    GROQ_KEY = ""
    DAILY_LIMIT = 30

    SYSTEM_PROMPT = """أنت "الدوك" (DOC)، المساعد الذكي والودود لتطبيق PsyEra للصحة النفسية.

# قواعد الرد الأساسية
1. الإيجاز: رد بإيجاز وبدون تكرار. قدم المعلومة الأساسية فقط إلا إذا طُلب تفصيل.
2. اللغة: استخدم نفس لغة المستخدم بالضبط (عربي أو إنجليزي).
3. التشجيع: استخدمه فقط عند مشاركة المستخدم شعوراً صعباً، وليس في كل رد.

# نطاق اختصاصك
أنت مخصص للصحة النفسية: التوعية والمعلومات العامة. لا تقدم تشخيصاً نهائياً.

# الاضطرابات التي يركز عليها التطبيق
MDD، Bipolar I، GAD، Schizophrenia، Anorexia Nervosa، SUD، Panic Disorder، Social Anxiety، OCD، PTSD، BPD.

# المشروع
مشروع تخرج 2026، قسم الحوسبة (Bioinformatics)، كلية العلوم، جامعة بورسعيد.
الفريق: أحمد السيد شلبي، أحمد أسامة عوض، أحمد محمد سماحة، إياد محمد طه، إسلام حسام الدين، لؤي السيد زكريا.
المشرفون: الدكتور محمد الجنيدي والدكتورة هدير عبد الحق راشد.

# قاعدة الأسماء
إذا ذُكر: شلبس/الاوس/سماحة/ايدو/لولو/سوي — رد بحماس وود كأنهم أصدقاؤك المقربون.

# الأدوية
إذا سُئلت عن دواء: قدم معلومات عامة مختصرة ثم "تنبيه: هذه معلومات عامة فقط. لا تتناول أي دواء بدون وصفة طبية.\""""

    # Header
    c1, c2, c3 = st.columns([1, 4, 1])
    with c1:
        if st.button(t("‹","‹"), key="back_chat"):
            go("home")
    with c2:
        remaining = DAILY_LIMIT - st.session_state.chat_count
        st.markdown(f"""
        <div style='text-align:center;'>
            <span style='font-size:20px;'>🧠</span>
            <b style='font-size:16px;'> {t('اسأل الدوك','Ask the Doc')}</b><br>
            <span style='color:rgba(255,255,255,0.5); font-size:11px;'>{t('متخصص في الصحة النفسية','Mental Health Specialist')}</span>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        color = "#EF4444" if remaining <= 5 else "#667eea"
        st.markdown(f"<div style='text-align:center; color:{color}; font-weight:bold; font-size:13px; padding-top:8px;'>{remaining}/{DAILY_LIMIT}</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08);margin:8px 0;'>", unsafe_allow_html=True)

    # Chat history
    if not st.session_state.chat_messages:
        suggestions = ["ما هو الاكتئاب؟","أعراض القلق","ما هو OCD؟","كيف أساعد نفسي؟"] if IS_AR else \
                     ["What is MDD?","Anxiety symptoms","What is OCD?","How to cope?"]
        st.markdown(f"""
        <div style='text-align:center; padding:32px;'>
            <div style='font-size:60px;'>🧠</div>
            <p style='color:rgba(255,255,255,0.7); font-size:15px; line-height:1.6;'>
                {t('مرحباً! أنا الدوك 👋<br>أنا هنا لدعمك، تحدث معي براحتك', "Hello! I'm Doc 👋<br>I'm here to support you, speak freely")}            </p>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(2)
        for i, sug in enumerate(suggestions):
            with cols[i % 2]:
                if st.button(sug, key=f"sug_{i}", use_container_width=True):
                    st.session_state.chat_messages.append({"role":"user","content":sug})
                    st.session_state.chat_count += 1
                    with st.spinner(t("الدوك يفكر...","Doc is thinking...")):
                        reply = call_groq(GROQ_KEY, SYSTEM_PROMPT, st.session_state.chat_messages)
                    st.session_state.chat_messages.append({"role":"assistant","content":reply})
                    st.rerun()
    else:
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f"<div style='display:flex; justify-content:flex-end; margin:6px 0;'><div class='chat-bubble-user'>{msg['content']}</div></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='display:flex; align-items:flex-end; gap:8px; margin:6px 0;'><span style='font-size:20px;'>🧠</span><div class='chat-bubble-bot'>{msg['content']}</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Input
    if remaining <= 0:
        st.warning(t("⚠️ وصلت للحد اليومي (30 رسالة). عود غداً!","⚠️ You reached the daily limit (30 messages). Come back tomorrow!"))
    else:
        user_input = st.chat_input(t("اكتب سؤالك هنا...","Ask your question..."))
        if user_input:
            st.session_state.chat_messages.append({"role":"user","content":user_input})
            st.session_state.chat_count += 1
            with st.spinner(t("الدوك يفكر...","Doc is thinking...")):
                reply = call_groq(GROQ_KEY, SYSTEM_PROMPT, st.session_state.chat_messages)
            st.session_state.chat_messages.append({"role":"assistant","content":reply})
            st.rerun()


def call_groq(api_key, system_prompt, messages):
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
    if st.button(t("‹ رجوع","‹ Back"), key="back_stats"):
        go("home")

    st.markdown(f"""
    <div class='psyera-card' style='text-align:center;'>
        <div style='font-size:40px;'>📊</div>
        <h2>{t('إحصائيات المستخدمين','User Statistics')}</h2>
    </div>
    """, unsafe_allow_html=True)

    SUPABASE_URL = "https://zrsqufwcpfiifchqbhvp.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpyc3F1ZndjcGZpaWZjaHFiaHZwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3NDgxMjgsImV4cCI6MjA5MTMyNDEyOH0.RDXOg_87waYn54jPNqIPK_yf0Czt_HiZRrE19wc1KRE"

    with st.spinner(t("جارٍ تحميل البيانات...","Loading data...")):
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
                    st.info(t("لا توجد بيانات بعد","No data yet"))
                else:
                    percentages = {k: round(v/total*100, 1) for k, v in counts.items()}
                    sorted_pct = sorted(percentages.items(), key=lambda x: x[1], reverse=True)

                    import plotly.graph_objects as go_plotly
                    labels = [disorders[k]["nameAr"] if IS_AR else disorders[k]["nameEn"] for k, _ in sorted_pct if k in disorders]
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
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(showgrid=False, color='rgba(255,255,255,0.3)'),
                        yaxis=dict(color='white', tickfont=dict(family='Cairo')),
                        margin=dict(l=10, r=60, t=10, b=10),
                        height=400,
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(t("فشل تحميل البيانات","Failed to load data"))
        except Exception as e:
            st.error(str(e))


def page_forecast():
    if st.button(t("‹ رجوع","‹ Back"), key="back_forecast"):
        go("home")

    st.markdown(f"""
    <div class='psyera-card' style='text-align:center;'>
        <div style='font-size:40px;'>📈</div>
        <h2>{t('توقعات انتشار الاضطرابات','Mental Health Disorder Forecasts')}</h2>
    </div>
    """, unsafe_allow_html=True)

    from data.forecast_data import EGYPT_DATA, WORLD_DATA

    region = st.radio(t("المنطقة","Region"), [t("مصر","Egypt"), t("العالم","World")], horizontal=True)
    data_source = EGYPT_DATA if region == t("مصر","Egypt") else WORLD_DATA

    disorder_names = list(data_source.keys())
    selected = st.selectbox(t("اختر الاضطراب","Select Disorder"), disorder_names)

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
            x=hist_years, y=hist_vals,
            mode='lines+markers',
            name=t('بيانات تاريخية','Historical'),
            line=dict(color='#667eea', width=2),
            marker=dict(size=4),
        ))
        fig.add_trace(go_plotly.Scatter(
            x=fore_years, y=fore_vals,
            mode='lines+markers',
            name=t('توقعات','Forecast'),
            line=dict(color='#f093fb', width=2, dash='dash'),
            marker=dict(size=4),
        ))
        fig.add_vline(x=2023, line_dash="dot", line_color="rgba(255,255,255,0.3)")

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(color='rgba(255,255,255,0.5)', gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(color='rgba(255,255,255,0.5)', gridcolor='rgba(255,255,255,0.05)'),
            legend=dict(font=dict(color='white'), bgcolor='rgba(0,0,0,0)'),
            margin=dict(l=10, r=10, t=20, b=10),
            height=350,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Summary
        last_hist = hist_vals[-1]
        last_fore = fore_vals[-1]
        change_pct = (last_fore - last_hist) / last_hist * 100

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(t("آخر بيانات (2023)","Last Data (2023)"), f"{last_hist:,}")
        with c2:
            st.metric(t("توقع 2035","Forecast 2035"), f"{last_fore:,}")
        with c3:
            st.metric(t("التغيير المتوقع","Expected Change"), f"{change_pct:+.1f}%")

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
else:
    go("home")