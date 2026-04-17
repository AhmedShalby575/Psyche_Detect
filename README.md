# PsyEra — Streamlit Version 🧠

تطبيق PsyEra محوّل من Flutter إلى Python/Streamlit.

## مشروع تخرج 2026
قسم الحوسبة (Bioinformatics) — كلية العلوم، جامعة بورسعيد

---

## 🚀 طريقة التشغيل

### 1. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### 2. تشغيل التطبيق
```bash
streamlit run app.py
```

---

## 📤 رفع على Streamlit Cloud

1. ارفع المجلد على GitHub كـ repository
2. اذهب إلى [share.streamlit.io](https://share.streamlit.io)
3. اختار الـ repo وحدد `app.py` كملف رئيسي
4. اضغط Deploy!

---

## 📁 هيكل الملفات

```
psyera_streamlit/
├── app.py                    # التطبيق الرئيسي
├── requirements.txt          # المكتبات المطلوبة
├── .streamlit/
│   └── config.toml           # إعدادات الثيم
├── assets/
│   ├── psyera_logo_home.png
│   ├── faculty_logo.png
│   └── ...
└── data/
    ├── questions.py          # بيانات الأسئلة والحسابات
    ├── disorders.py          # بيانات الاضطرابات
    └── forecast_data.py      # بيانات التوقعات
```

---

## ✨ الميزات

- 🧠 **تقييم نفسي** — 11 اضطراباً نفسياً مع نظام scoring ذكي
- 🤖 **اسأل الدوك** — شات مدعوم بـ Groq AI (qwen3-32b)
- 📊 **إحصائيات** — بيانات حية من Supabase
- 📈 **توقعات الانتشار** — رسوم بيانية تاريخية ومستقبلية
- 🌐 **ثنائي اللغة** — عربي وإنجليزي
- 🪪 **الرقم القومي** — استخراج تلقائي للعمر والجنس والمحافظة
