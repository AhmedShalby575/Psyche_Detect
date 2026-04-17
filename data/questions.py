# ─── Questions Data ───────────────────────────────────────────────────────────

QUESTIONS_COMMON = [
    {"textAr":"هل تشعر بحزن أو مزاج مكتئب معظم اليوم؟","textEn":"Do you feel sad or depressed most of the day?","weights":{"MDD":3,"Bipolar":1},"category":"mood"},
    {"textAr":"هل فقدت الاهتمام بالأشياء التي كانت تسعدك؟","textEn":"Have you lost interest in things that used to make you happy?","weights":{"MDD":3,"Bipolar":1},"category":"mood"},
    {"textAr":"هل تعاني من اضطراب في النوم (أرق أو نوم زائد)؟","textEn":"Do you have sleep disturbances (insomnia or oversleeping)?","weights":{"MDD":2,"Bipolar":2,"GAD":2},"category":"sleep"},
    {"textAr":"هل تشعر بتعب وفقدان طاقة يومياً دون سبب واضح؟","textEn":"Do you feel fatigued and lack energy daily without clear reason?","weights":{"MDD":2,"GAD":1},"category":"energy"},
    {"textAr":"هل راودتك أفكار عن الموت أو إيذاء نفسك؟","textEn":"Have you had thoughts of death or self-harm?","weights":{"MDD":3,"BPD":2},"category":"critical"},
    {"textAr":"هل مررت بفترة طاقة مفرطة مع عدم الحاجة للنوم؟","textEn":"Have you had periods of excessive energy with little need for sleep?","weights":{"Bipolar":3},"category":"mania"},
    {"textAr":"هل تصرفت باندفاعية دون تفكير في العواقب؟","textEn":"Do you act impulsively without thinking about consequences?","weights":{"Bipolar":2,"BPD":2,"SUD":1},"category":"impulse"},
    {"textAr":"هل شعرت بأن أفكارك تتسارع أو تتكلم بسرعة كبيرة؟","textEn":"Do your thoughts race or do you talk much faster than usual?","weights":{"Bipolar":2},"category":"mania"},
    {"textAr":"هل تشعر بقلق مستمر ومفرط يصعب التحكم به؟","textEn":"Do you experience persistent, excessive worry hard to control?","weights":{"GAD":3},"category":"anxiety"},
    {"textAr":"هل تعاني من توتر عضلي مزمن أو شد في الجسم؟","textEn":"Do you have chronic muscle tension or body tension?","weights":{"GAD":2},"category":"physical"},
    {"textAr":"هل تخاف من المواقف الاجتماعية أو التحدث أمام الآخرين؟","textEn":"Are you afraid of social situations or speaking in front of others?","weights":{"GAD":1,"SAD":3},"category":"social"},
    {"textAr":"هل تتجنب المواقف الاجتماعية بسبب الخوف من التقييم السلبي؟","textEn":"Do you avoid social situations out of fear of negative judgment?","weights":{"SAD":3},"category":"social"},
    {"textAr":"هل أصابتك نوبات هلع مفاجئة مع خفقان وضيق تنفس؟","textEn":"Have you experienced sudden panic attacks with palpitations and shortness of breath?","weights":{"GAD":2,"PD":3},"category":"panic"},
    {"textAr":"هل تخاف باستمرار من حدوث نوبة هلع جديدة؟","textEn":"Do you constantly fear having another panic attack?","weights":{"PD":3},"category":"panic"},
    {"textAr":"هل سمعت أصواتاً أو رأيت أشياء لا يراها الآخرون؟","textEn":"Have you heard voices or seen things others cannot see?","weights":{"SCZ":3},"category":"psychosis"},
    {"textAr":"هل شعرت بأن هناك من يراقبك أو يتحكم في أفكارك؟","textEn":"Do you feel like someone is watching you or controlling your thoughts?","weights":{"SCZ":3},"category":"psychosis"},
    {"textAr":"هل لاحظ المقربون تغيراً واضحاً في سلوكك أو كلامك؟","textEn":"Have people close to you noticed a clear change in your behavior or speech?","weights":{"SCZ":2},"category":"behavior"},
    {"textAr":"هل تجد صعوبة في الاعتناء بنظافتك الشخصية؟","textEn":"Do you have difficulty caring for your personal hygiene?","weights":{"SCZ":2},"category":"selfcare"},
    {"textAr":"هل تتجنب الأكل أو تقلل منه خوفاً من زيادة الوزن؟","textEn":"Do you avoid or severely restrict food intake out of fear of gaining weight?","weights":{"ANO":3},"category":"eating"},
    {"textAr":"هل ترى جسمك أسمن مما يراه الآخرون؟","textEn":"Do you see your body as heavier than others perceive it?","weights":{"ANO":3},"category":"body_image"},
    {"textAr":"هل تمارس الرياضة بشكل مفرط لحرق سعرات حرارية؟","textEn":"Do you exercise excessively to burn calories?","weights":{"ANO":2},"category":"eating"},
    {"textAr":"هل انقطعت دورتك الشهرية بسبب انخفاض الوزن؟ (للإناث)","textEn":"Has your menstrual cycle stopped due to low weight? (Females)","weights":{"ANO":2},"category":"physical"},
    {"textAr":"هل لديك أفكار متطفلة متكررة تسبب لك قلقاً شديداً؟","textEn":"Do you have recurrent intrusive thoughts that cause significant distress?","weights":{"OCD":3},"category":"obsession"},
    {"textAr":"هل تقوم بأفعال متكررة (كالتحقق أو التنظيف) للتخفيف من القلق؟","textEn":"Do you perform repetitive actions (checking, cleaning) to relieve anxiety?","weights":{"OCD":3},"category":"compulsion"},
    {"textAr":"هل تعرضت لحدث صادم وتعاني من استرجاعه بشكل مفاجئ؟","textEn":"Have you experienced trauma and suffer from sudden flashbacks?","weights":{"PTSD":3},"category":"trauma"},
    {"textAr":"هل تتجنب أماكن أو أشخاصاً يذكّرونك بصدمة سابقة؟","textEn":"Do you avoid places or people that remind you of a past trauma?","weights":{"PTSD":3},"category":"trauma"},
    {"textAr":"هل تعاني من علاقات غير مستقرة وخوف شديد من الهجر؟","textEn":"Do you have unstable relationships and intense fear of abandonment?","weights":{"BPD":3},"category":"bpd"},
    {"textAr":"هل تشعر بفراغ داخلي مزمن وتقلبات مزاجية سريعة؟","textEn":"Do you feel chronic inner emptiness and rapid mood shifts (hours, not days)?","weights":{"BPD":3},"category":"bpd"},
    {"textAr":"هل تستخدم مواد (كحول، أدوية، مخدرات) بشكل متكرر؟","textEn":"Do you use substances (alcohol, medications, drugs) repeatedly?","weights":{"SUD":3},"category":"substance_gate"},
    {"textAr":"هل تحتاج كميات أكبر من المادة للحصول على نفس التأثير؟","textEn":"Do you need larger amounts to get the same effect?","weights":{"SUD":3},"category":"sub_followup"},
    {"textAr":"هل أثّر استخدام المواد على علاقاتك أو عملك أو دراستك؟","textEn":"Has substance use affected your relationships, work, or studies?","weights":{"SUD":2},"category":"sub_followup"},
    {"textAr":"هل جربت التوقف عن استخدام المادة وفشلت؟","textEn":"Have you tried to stop using the substance and failed?","weights":{"SUD":2},"category":"sub_followup"},
    {"textAr":"هل تعاني من أعراض جسدية عند التوقف (رجفة، تعرق، قلق)؟","textEn":"Do you experience physical symptoms when stopping (tremors, sweating, anxiety)?","weights":{"SUD":2},"category":"sub_followup"},
]

QUESTIONS_AGE = {
    "15-24": [
        {"textAr":"هل تشعر بضغط شديد من المدرسة أو الجامعة أو محيطك؟","textEn":"Do you feel intense pressure from peers, school, or university?","weights":{"GAD":2,"MDD":1},"category":"age_specific"},
        {"textAr":"هل تنسحب من الأنشطة الاجتماعية التي كنت تستمتع بها؟","textEn":"Do you withdraw from social activities you used to enjoy?","weights":{"MDD":2,"SAD":1},"category":"age_specific"},
        {"textAr":"هل تعاني من تغييرات مفاجئة في هويتك أو أهدافك الحياتية؟","textEn":"Do you experience sudden changes in your identity or life goals?","weights":{"BPD":2},"category":"age_specific"},
    ],
    "25-39": [
        {"textAr":"هل تشعر بضغط مزمن من العمل أو المسؤوليات الأسرية؟","textEn":"Do you feel chronic pressure from work or family responsibilities?","weights":{"GAD":2,"MDD":1},"category":"age_specific"},
        {"textAr":"هل لاحظت تراجعاً في أدائك المهني أو الأسري بسبب حالتك النفسية؟","textEn":"Have you noticed a decline in your professional or family performance due to your mental state?","weights":{"MDD":2,"SCZ":1},"category":"age_specific"},
        {"textAr":"هل تشعر باليأس من تحقيق أهدافك في الحياة؟","textEn":"Do you feel hopeless about achieving your life goals?","weights":{"MDD":2,"BPD":1},"category":"age_specific"},
    ],
    "40-54": [
        {"textAr":"هل تشعر بأن حياتك فقدت معناها أو هدفها؟","textEn":"Do you feel that your life has lost its meaning or purpose?","weights":{"MDD":3},"category":"age_specific"},
        {"textAr":"هل تعاني من أعراض جسدية غير مفسرة (آلام، صداع، إرهاق مزمن)؟","textEn":"Do you experience unexplained physical symptoms (pain, headaches, chronic fatigue)?","weights":{"MDD":2,"GAD":2},"category":"age_specific"},
        {"textAr":"هل لاحظت تغيرات ملحوظة في ذاكرتك أو تركيزك؟","textEn":"Have you noticed significant changes in your memory or concentration?","weights":{"MDD":2,"GAD":1},"category":"age_specific"},
    ],
}

def get_questions(age_group):
    all_q = list(QUESTIONS_COMMON)
    all_q.extend(QUESTIONS_AGE.get(age_group, QUESTIONS_AGE["15-24"]))
    return all_q

def build_flow(questions, answers, gender):
    flow = []
    is_male = gender == "Male"
    for i, q in enumerate(questions):
        cat = q["category"]
        # Skip sub_followup if substance_gate not answered yes/sometimes
        if cat == "sub_followup":
            sub_idx = next((j for j, qq in enumerate(questions) if qq["category"] == "substance_gate"), None)
            if sub_idx is not None and answers.get(sub_idx) not in ("yes","sometimes"):
                continue
        # Skip female-specific question for males (index 21 = menstrual cycle)
        if i == 21 and is_male:
            continue
        flow.append(i)
    return flow

MAX_SCORES = {"MDD":18,"Bipolar":13,"GAD":13,"SCZ":12,"ANO":12,"SUD":12,
              "PD":6,"SAD":9,"OCD":6,"PTSD":6,"BPD":11}

def score_answers(questions, answers, age_group):
    raw = {k: 0.0 for k in MAX_SCORES}
    for i, q in enumerate(questions):
        if q["category"] == "sub_followup":
            sub_idx = next((j for j, qq in enumerate(questions) if qq["category"] == "substance_gate"), None)
            if sub_idx is not None and answers.get(sub_idx) not in ("yes","sometimes"):
                continue
        val = answers.get(i, "no")
        mult = 1.0 if val == "yes" else (0.5 if val == "sometimes" else 0.0)
        for disorder, weight in q["weights"].items():
            if disorder in raw:
                raw[disorder] += weight * mult

    # Convert to percentages (capped at 100)
    result = {}
    for disorder, score in raw.items():
        max_s = MAX_SCORES.get(disorder, 1)
        pct = min(round(score / max_s * 100, 1), 100.0)
        result[disorder] = pct
    return result
