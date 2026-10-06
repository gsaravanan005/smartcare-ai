"""
SmartCare AI - Module 4 Controlled Translation Dictionary
Supports English (en), Tamil (ta), Hindi (hi), Telugu (te), Malayalam (ml), and Kannada (kn).
"""

TRANSLATIONS = {
    # Page Header
    "page_title": {
        "en": "Personalized Wellness Plan",
        "ta": "தனிப்பயனாக்கப்பட்ட ஆரோக்கிய திட்டம்",
        "hi": "व्यक्तिगत वेलनेस योजना",
        "te": "వ్యక్తిగత ఆరోగ్య ప్రణాళిక",
        "ml": "വ്യക്തിഗത വെൽനസ് പ്ലാൻ",
        "kn": "ವೈಯಕ್ತಿಕಗೊಳಿಸಿದ ವೆಲ್ನೆಸ್ ಯೋಜನೆ"
    },
    "page_subtitle": {
        "en": "Guidance based on your SmartCare AI assessment",
        "ta": "உங்கள் ஸ்மார்ட்கேர் AI மதிப்பீட்டின் அடிப்படையிலான வழிகாட்டுதல்",
        "hi": "आपके स्मार्टकेयर एआई मूल्यांकन पर आधारित मार्गदर्शन",
        "te": "మీ మార్ట్‌కేర్ AI అంచనా ఆధారంగా మార్గదర్శకత్వం",
        "ml": "നിങ്ങളുടെ സ്മാർട്ട്കെയർ AI വിലയിരുത്തലിനെ അടിസ്ഥാനമാക്കിയുള്ള മാർഗ്ഗനിർദ്ദേശം",
        "kn": "ನಿಮ್ಮ ಸ್ಮಾರ್ಟ್‌ಕೇರ್ AI ಮೌಲ್ಯಮಾಪನವನ್ನು ಆಧರಿಸಿದ ಮಾರ್ಗದರ್ಶನ"
    },

    # Section Headers
    "risk_summary_title": {
        "en": "AI Risk Assessment Summary",
        "ta": "AI ஆபத்து மதிப்பீட்டு சுருக்கம்",
        "hi": "एआई जोखिम मूल्यांकन सारांश",
        "te": "AI ప్రమాద అంచనా సారాంశం",
        "ml": "AI അപകടസാധ്യത വിലയിരുത്തൽ സംഗ്രഹം",
        "kn": "AI ಅಪಾಯದ ಮೌಲ್ಯಮಾಪನ ಸಾರಾಂಶ"
    },
    "key_factors_title": {
        "en": "Key Modifiable Risk Factors (SHAP Identified)",
        "ta": "முக்கிய மாற்றியமைக்கக்கூடிய அபாயக் காரணிகள்",
        "hi": "प्रमुख परिवर्तनीय जोखिम कारक (SHAP द्वारा पहचाने गए)",
        "te": "ప్రధాన మార్చగల ప్రమాద కారకాలు",
        "ml": "പ്രധാന മാറ്റം വരുത്താവുന്ന അപകടസാധ്യത ഘടകങ്ങൾ",
        "kn": "ಪ್ರಮುಖ ಮಾರ್ಪಡಿಸಬಹುದಾದ ಅಪಾಯದ ಅಂಶಗಳು"
    },
    "recommendations_title": {
        "en": "Tailored Recommendations",
        "ta": "பிரத்யேக பரிந்துரைகள்",
        "hi": "अनुकूलित सिफारिशें",
        "te": "అనుకూల సిఫార్సులు",
        "ml": "ക്രമീകരിച്ച ശുപാർശകൾ",
        "kn": "ಅನುಗುಣವಾದ ಶಿಫಾರಸುಗಳು"
    },
    "food_plan_title": {
        "en": "Daily Food Plan",
        "ta": "தினசரி உணவுத் திட்டம்",
        "hi": "दैनिक भोजन योजना",
        "te": "రోజువారీ ఆహార ప్రణాళిక",
        "ml": "ദിനചര്യ ഭക്ഷണ പ്ലാൻ",
        "kn": "ದೈನಂದಿನ ಆಹಾರ ಯೋಜನೆ"
    },
    "exercise_plan_title": {
        "en": "Home Exercise Plan",
        "ta": "வீட்டு உடற்பயிற்சி திட்டம்",
        "hi": "घरेलू व्यायाम योजना",
        "te": "ఇంటి వ్యాయామ ప్రణాళిక",
        "ml": "വീട്ടിലെ വ്യായാമ പ്ലാൻ",
        "kn": "ಮನೆಯ ವ್ಯಾಯಾಮ ಯೋಜನೆ"
    },
    "habits_title": {
        "en": "Good Daily Habits",
        "ta": "நல்ல தினசரி பழக்கங்கள்",
        "hi": "अच्छी दैनिक आदतें",
        "te": "మంచి రోజువారీ అలవాట్లు",
        "ml": "നല്ല ദിനചര്യ ശീലങ്ങൾ",
        "kn": "ಉತ್ತಮ ದೈನಂದಿನ ಅಭ್ಯಾಸಗಳು"
    },
    "herbal_title": {
        "en": "Home Herbal & Natural Wellness",
        "ta": "வீட்டு மூலிகை மற்றும் இயற்கை ஆரோக்கியம்",
        "hi": "घरेलू हर्बल और प्राकृतिक कल्याण",
        "te": "ఇంటి మూలికా మరియు సహజ ఆరోగ్యం",
        "ml": "വീട്ടിലെ ഹെർബൽ, പ്രകൃതിദത്ത വെൽനസ്",
        "kn": "ಮನೆಯ ಮೂಲಿಕೆ ಮತ್ತು ನೈಸರ್ಗಿಕ ವೆಲ್ನೆಸ್"
    },
    "monitoring_title": {
        "en": "Suggested Routine Monitoring & Follow-Up Schedule",
        "ta": "பரிந்துரைக்கப்பட்ட வழக்கமான கண்காணிப்பு அட்டவணை",
        "hi": "सुझाई गई नियमित निगरानी और अनुवर्ती अनुसूची",
        "te": "సూచించిన దినచర్య పర్యవేక్షణ సమయం",
        "ml": "നിർദ്ദേശിച്ച പതിവ് നിരീക്ഷണ ഷെഡ്യൂൾ",
        "kn": "ಸೂಚಿಸಿದ ನಿಯಮಿತ ಮೇಲ್ವಿಚಾರಣೆ ವೇಳಾಪಟ್ಟಿ"
    },
    "clinical_alert_title": {
        "en": "Professional Medical Evaluation Recommended",
        "ta": "தொழில்முறை மருத்துவ பரிசோதனை பரிந்துரைக்கப்படுகிறது",
        "hi": "पेशेवर चिकित्सा मूल्यांकन की सिफारिश की जाती है",
        "te": "వృత్తిపరమైన వైద్య మూల్యాంకనం సిఫార్సు చేయబడింది",
        "ml": "പ്രൊഫഷണൽ മെഡിക്കൽ മൂല്യനിർണ്ണയം ശുപാർശ ചെയ്യുന്നു",
        "kn": "ವೃತ್ತಿಪರ ವೈದ್ಯಕೀಯ ಮೌಲ್ಯಮಾಪನವನ್ನು ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ"
    },
    "high_risk_message": {
        "en": "Professional medical evaluation is recommended. One or more evaluated disease risk scores indicated elevated risk. Please discuss your results with a qualified healthcare professional.",
        "ta": "தொழில்முறை மருத்துவ பரிசோதனை பரிந்துரைக்கப்படுகிறது. ஒன்று அல்லது அதற்கு மேற்பட்ட நோய் அபாய மதிப்பெண்கள் அதிகரித்துள்ளன. தயவுசெய்து உங்கள் தகுதியான மருத்துவரிடம் ஆலோசிக்கவும்.",
        "hi": "पेशेवर चिकित्सा मूल्यांकन की सिफारिश की जाती है। एक या अधिक मूल्यांकित बीमारी के जोखिम स्कोर में वृद्धि देखी गई है। कृपया अपने योग्य स्वास्थ्य पेशेवर से चर्चा करें।",
        "te": "వృత్తిపరమైన వైద్య మూల్యాంకనం సిఫార్సు చేయబడింది. ఒకటి లేదా అంతకంటే ఎక్కువ వ్యాధి ప్రమాద స్కోర్లు పెరిగిన ప్రమాదాన్ని సూచించాయి.",
        "ml": "പ്രൊഫഷണൽ മെഡിക്കൽ മൂല്യനിർണ്ണയം ശുപാർശ ചെയ്യുന്നു. ഒന്നോ അതിലധികമോ രോഗസാധ്യത സ്കോറുകൾ ഉയർന്ന അപകടസാധ്യത കാണിക്കുന്നു.",
        "kn": "ವೃತ್ತಿಪರ ವೈದ್ಯಕೀಯ ಮೌಲ್ಯಮಾಪನವನ್ನು ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ. ಒಂದಕ್ಕಿಂತ ಹೆಚ್ಚು ಮೌಲ್ಯಮಾಪನ ಮಾಡಿದ ರೋಗದ ಅಪಾಯದ ಅಂಕಗಳು ಹೆಚ್ಚಿನ ಅಪಾಯವನ್ನು ಸೂಚಿಸಿವೆ."
    },
    "disclaimer_text": {
        "en": "SmartCare AI wellness recommendations provide general lifestyle guidance based on machine learning risk assessments and SHAP risk factor analysis. They do NOT constitute medical diagnosis, treatment plans, or medication prescriptions.",
        "ta": "ஸ்மார்ட்கேர் AI ஆரோக்கிய பரிந்துரைகள் பொதுவான வாழ்க்கை முறை வழிகாட்டுதலை மட்டுமே வழங்குகின்றன. இவை மருத்துவ நோய் கண்டறிதல் அல்லது மருந்து பரிந்துரைகள் அல்ல.",
        "hi": "स्मार्टकेयर एआई वेलनेस सिफारिशें सामान्य जीवनशैली मार्गदर्शन प्रदान करती हैं। ये चिकित्सा निदान या दवा के पर्चे नहीं हैं।",
        "te": "స్మార్ట్‌కేర్ AI వెల్నెస్ సిఫార్సులు సాధారణ జీవనశైలి మార్గదర్శకత్వాన్ని అందిస్తాయి. ఇవి వైద్య నిర్ధారణ లేదా ఔషధ సూచనలు కావు.",
        "ml": "സ്മാർട്ട്കെയർ AI വെൽനസ് ശുപാർശകൾ പൊതുവായ ജീവിതശൈലി മാർഗ്ഗനിർദ്ദേശം നൽകുന്നു. ഇവ മെഡിക്കൽ രോഗനിർണ്ണയമോ മരുന്നുകളോ അല്ല.",
        "kn": "ಸ್ಮಾರ್ಟ್‌ಕೇರ್ AI ವೆಲ್ನೆಸ್ ಶಿಫಾರಸುಗಳು ಸಾಮಾನ್ಯ ಜೀವನಶೈಲಿ ಮಾರ್ಗದರ್ಶನವನ್ನು ನೀಡುತ್ತವೆ. ಇವು ವೈದ್ಯಕೀಯ ರೋಗನಿರ್ಣಯ ಅಥವಾ ಔಷಧಿಯ ಸೂಚನೆಗಳಲ್ಲ."
    },

    # Meal Labels
    "breakfast": {"en": "Breakfast", "ta": "காலை உணவு", "hi": "नाश्ता", "te": "ఉదయం ఉపహారం", "ml": "പ്രഭാതഭക്ഷണം", "kn": "ಬೆಳಗಿನ ಉಪಹಾರ"},
    "mid_morning": {"en": "Mid-Morning", "ta": "முற்பகல் சிற்றுண்டி", "hi": "सुबह का स्नैक", "te": "మధ్యాహ్న సమయం", "ml": "ഉച്ചയ്ക്ക് മുമ്പ്", "kn": "ಮಧ್ಯ-ಬೆಳಿಗ್ಗೆ"},
    "lunch": {"en": "Lunch", "ta": "மதிய உணவு", "hi": "दोपहर का भोजन", "te": "మధ్యాహ్న భోజనం", "ml": "ഉച്ചഭക്ഷണം", "kn": "ಮಧ್ಯಾಹ್ನದ ಊಟ"},
    "evening_snack": {"en": "Evening Snack", "ta": "மாலை சிற்றுண்டி", "hi": "शाम का नाश्ता", "te": "సాయంత్రం స్నాక్", "ml": "വൈകുന്നേരത്തെ പലഹാരം", "kn": "ಸಂಜೆಯ ಉಪಹಾರ"},
    "dinner": {"en": "Dinner", "ta": "இரவு உணவு", "hi": "रात का खाना", "te": "రాత్రి భోజనం", "ml": "അത്താഴം", "kn": "ರಾತ್ರಿಯ ಊಟ"},
    "Breakfast": {"en": "Breakfast", "ta": "காலை உணவு", "hi": "नाश्ता", "te": "ఉదయం ఉపహారం", "ml": "പ്രഭാതഭക്ഷണം", "kn": "ಬೆಳಗಿನ ಉಪಹಾರ"},
    "Mid-Morning": {"en": "Mid-Morning", "ta": "முற்பகல் சிற்றுண்டி", "hi": "सुबह का स्नैक", "te": "మధ్యాహ్న సమయం", "ml": "ഉച്ചയ്ക്ക് മുമ്പ്", "kn": "ಮಧ್ಯ-ಬೆಳಿಗ್ಗೆ"},
    "Lunch": {"en": "Lunch", "ta": "மதிய உணவு", "hi": "दोपहर का भोजन", "te": "మధ్యాహ్ன భోజனம்", "ml": "ഉച്ചഭക്ഷണം", "kn": "ಮಧ್ಯಾಹ್ನದ ಊಟ"},
    "Evening Snack": {"en": "Evening Snack", "ta": "மாலை சிற்றுண்டி", "hi": "शाम का नाश्ता", "te": "సాయంత్రం స్నాక్", "ml": "വൈകുന്നேரത്തെ பலஹாரம்", "kn": "ಸಂಜೆಯ ಉಪಹಾರ"},
    "Dinner": {"en": "Dinner", "ta": "இரவு உணவு", "hi": "रात का खाना", "te": "రాత్రి భోజనం", "ml": "അത്താഴം", "kn": "ರಾತ್ರಿಯ ಊಟ"},

    # Priority Labels
    "High": {"en": "High", "ta": "அதிகம்", "hi": "उच्च", "te": "ఎక్కువ", "ml": "ഉയർന്നത്", "kn": "ಹೆಚ್ಚಿನ"},
    "Medium": {"en": "Medium", "ta": "மிதமான", "hi": "मध्यम", "te": "మధ్యస్థ", "ml": "ഇടത്തരം", "kn": "ಮಧ್ಯಮ"},
    "Low": {"en": "Low", "ta": "குறைந்த", "hi": "कम", "te": "తక్కువ", "ml": "കുറഞ്ഞത്", "kn": "ಕಡಿಮೆ"},

    # Categories
    "Cardiovascular Wellness": {"en": "Cardiovascular Wellness", "ta": "இதய ஆரோக்கியம்", "hi": "हृदय स्वास्थ्य", "te": "గుండె ఆరోగ్యం", "ml": "ഹൃദയ വെൽനസ്", "kn": "ಹೃದಯ ಆರೋಗ್ಯ"},
    "Metabolic Health": {"en": "Metabolic Health", "ta": "பரிணாம ஆரோக்கியம் (சர்க்கரை)", "hi": "चयापचय स्वास्थ्य", "te": "జీవక్రియ ఆరోగ్యం", "ml": "മെറ്റബോളിക് ആരോഗ്യം", "kn": "ಚಯಾಪചಯ ಆರೋಗ್ಯ"},
    "Physical Activity": {"en": "Physical Activity", "ta": "உடற்பயிற்சி மற்றும் இயக்கம்", "hi": "शारीरिक गतिविधि", "te": "శారీరక శ్రమ", "ml": "ശാരീരിക അധ്വാനം", "kn": "ದೈಹಿಕ ಚಟುವಟಿಕೆ"},
    "Behavioral Health": {"en": "Behavioral Health", "ta": "நடத்தை ஆரோக்கியம் (புகைபிடித்தல்)", "hi": "व्यवहार स्वास्थ्य", "te": "ప్రవర్తనా ఆరోగ్యం", "ml": "പെരുമാറ്റ ആരോഗ്യം", "kn": "ವರ್ತನೆಯ ಆರೋಗ್ಯ"},
    "Weight Management": {"en": "Weight Management", "ta": "எடை மேலாண்மை", "hi": "वजन प्रबंधन", "te": "బరువు నిర్వహణ", "ml": "ഭാര നിയന്ത്രണം", "kn": "ತೂಕ ನಿರ್ವಹಣೆ"},
    "Lipid Management": {"en": "Lipid Management", "ta": "கொழுப்பு மேலாண்மை", "hi": "लिपिड प्रबंधन", "te": "లిపిడ్ నిర్వహణ", "ml": "ലിപിഡ് നിയന്ത്രണം", "kn": "ಲಿಪಿಡ್ ನಿರ್ವಹಣೆ"},
    "Renal Health": {"en": "Renal Health", "ta": "சிறுநீரக ஆரோக்கியம்", "hi": "गुर्दे का स्वास्थ्य", "te": "కిడ్నీ ఆరోగ్యం", "ml": "വൃക്ക വെൽനസ്", "kn": "ಮೂತ್ರಪಿಂಡದ ಆರೋಗ್ಯ"},
    "Assessment Status": {"en": "Assessment Status", "ta": "மதிப்பீட்டு நிலை", "hi": "मूल्यांकन की स्थिति", "te": "అంచనా స్థితి", "ml": "മൂല്യനിർണ്ണയ അവസ്ഥ", "kn": "ಮೌಲ್ಯಮಾಪನ ಸ್ಥಿತಿ"},
    "Rest & Recovery": {"en": "Rest & Recovery", "ta": "ஓய்வு & மீட்சி", "hi": "विश्राम और पुनर्प्राप्ति", "te": "విశ్రాంతి", "ml": "വിശ്രമം", "kn": "ವಿಶ್ರಾಂತಿ"},
    "Physical Movement": {"en": "Physical Movement", "ta": "உடல் இயக்கம்", "hi": "शारीरिक गतिविधि", "te": "శారీరక కదలిక", "ml": "ശാരീരിക ചലനം", "kn": "ದೈಹಿಕ ಚಲನೆ"},
    "Hydration": {"en": "Hydration", "ta": "நீர்ச்சத்து", "hi": "जल संतुलन", "te": "హైడ్రేషన్", "ml": "ജലാംശം", "kn": "ಹೈಡ್ರೇಶನ್"},
    "Nutrition": {"en": "Nutrition", "ta": "ஊட்டச்சத்து", "hi": "पोषण", "te": "పోషకాహారం", "ml": "പോഷകാഹാരം", "kn": "ಪೋಷಣೆ"},
    "Mental Wellness": {"en": "Mental Wellness", "ta": "மன ஆரோக்கியம்", "hi": "मानसिक कल्याण", "te": "మానసిక ఆరోగ్యం", "ml": "മാനസിക വെൽനസ്", "kn": "ಮಾನಸಿಕ ವೆಲ್ನೆಸ್"},
    "Monitoring": {"en": "Monitoring", "ta": "கண்காணிப்பு", "hi": "निगरानी", "te": "పర్యవేక్షణ", "ml": "നിരീക്ഷണം", "kn": "ಮೇಲ್ವಿಚಾರಣೆ"},

    # Food Suggestions & Whys
    "Steel-cut oatmeal or whole-grain porridge topped with ground flaxseed and a handful of berries.": {
        "en": "Steel-cut oatmeal or whole-grain porridge topped with ground flaxseed and a handful of berries.",
        "ta": "ஸ்டீல்-கட் ஓட்ஸ் அல்லது தானிய கஞ்சி, ஆளி விதை மற்றும் பழங்களுடன் சேர்த்து சாப்பிடவும்.",
        "hi": "पिसी हुई अलसी और जामुन के साथ ओट्स या साबुत अनाज का दलिया खाएं।",
        "te": "ఓట్స్ లేదా ధాన్యాల జావను ఫ్లాక్స్ సీడ్స్ మరియు బెర్రీలతో తీసుకోండి.",
        "ml": "ഓട്സ് അല്ലെങ്കിൽ ധാന്യക്കഞ്ഞി ഫ്ളാക്സ് സീഡും പഴങ്ങളും ചേർത്ത് കഴിക്കുക.",
        "kn": "ಫ್ಲಾಕ್ಸ್ ಸೀಡ್ಸ್ ಮತ್ತು ಹಣ್ಣುಗಳೊಂದಿಗೆ ಓಟ್ಸ್ ಅಥವಾ ಧಾನ್ಯದ ಗಂಜಿಯನ್ನು ಸೇವಿಸಿ."
    },
    "Provides complex carbohydrates and high soluble fiber to encourage steady glycemic response.": {
        "en": "Provides complex carbohydrates and high soluble fiber to encourage steady glycemic response.",
        "ta": "சிக்கலான கார்போஹைட்ரேட்டுகள் மற்றும் நார்ச்சத்து வழங்கி சர்க்கரை அளவை சீராக வைக்க உதவுகிறது.",
        "hi": "जटिल कार्बोहाइड्रेट और उच्च घुलनशील फाइबर रक्त शर्करा को स्थिर रखते हैं।",
        "te": "రక్తంలో చక్కెర స్థాయిలను స్థిరంగా ఉంచడానికి పీచు పదార్థాన్ని అందిస్తుంది.",
        "ml": "രക്തത്തിലെ പഞ്ചസാരയുടെ അളവ് നിലനിർത്താൻ നാരുള്ള ഭക്ഷണം സഹായിക്കുന്നു.",
        "kn": "ರಕ್ತದ ಸಕ್ಕರೆ ಮಟ್ಟವನ್ನು ಸ್ಥಿರವಾಗಿಡಲು ಕರಗುವ ನಾರಿನಂಶವನ್ನು ಒದಗಿಸುತ್ತದೆ."
    },
    "Handful of raw unsalted almonds or walnuts with cucumber slices.": {
        "en": "Handful of raw unsalted almonds or walnuts with cucumber slices.",
        "ta": "உப்பு சேர்க்காத பாதாம் அல்லது வால்நட்ஸ் மற்றும் வெள்ளரிக்காய் துண்டுகள்.",
        "hi": "ककड़ी के टुकड़ों के साथ बिना नमक वाले बादाम या अखरोट खाएं।",
        "te": "కీరా ముక్కలతో పాటు ఉప్పు లేని బాదం లేదా అక్రోట్లను తీసుకోండి.",
        "ml": "വെള്ളരിക്ക കഷണങ്ങളോടൊപ്പം ബദാം അല്ലെങ്കിൽ വാൽനട്ട് കഴിക്കുക.",
        "kn": "ಸೌತೆಕಾಯಿ ತುಂಡುಗಳೊಂದಿಗೆ ಉಪ್ಪಿಲ್ಲದ ಬಾದಾಮಿ ಅಥವಾ ವಾಲ್‌ನಟ್‌ಗಳನ್ನು ಸೇವಿಸಿ."
    },
    "Healthy fats and low-glycemic crunch stabilize hunger without blood sugar spikes.": {
        "en": "Healthy fats and low-glycemic crunch stabilize hunger without blood sugar spikes.",
        "ta": "ஆரோக்கியமான கொழுப்புகள் சர்க்கரை அளவு உயராமல் பசியைக் கட்டுப்படுத்துகின்றன.",
        "hi": "स्वस्थ वसा और कम ग्लाइसेमिक भोजन रक्त शर्करा को बढ़ाए बिना भूख शांत करते हैं।",
        "te": "ఆరోగ్యకరమైన కొవ్వులు రక్తంలో చక్కెర పెరగకుండా ఆకలిని నింత్రిస్తాయి.",
        "ml": "ആരോഗ്യകരമായ കൊഴുപ്പുകൾ പഞ്ചസാര കൂട്ടാതെ വിശപ്പ് മാറ്റുന്നു.",
        "kn": "ಆರೋಗ್ಯಕರ ಕೊಬ್ಬುಗಳು ರಕ್ತದ ಸಕ್ಕರೆಯನ್ನು ಹೆಚ್ಚಿಸದೆ ಹಸಿವನ್ನು ನಿಯಂತ್ರಿಸುತ್ತವೆ."
    },
    "Steamed or grilled lean protein (chicken breast, fish, or lentils) with a large leafy green salad dressed in olive oil and lemon.": {
        "en": "Steamed or grilled lean protein (chicken breast, fish, or lentils) with a large leafy green salad dressed in olive oil and lemon.",
        "ta": "ஆவியில் வேகவைத்த புரத உணவு (கோழி, மீன் அல்லது பருப்பு) மற்றும் ஒலிவ் எண்ணெய் சேர்த்த பச்சைக் காய்கறி சாலட்.",
        "hi": "जैतून के तेल और नींबू के साथ हरी पत्तेदार सलाद और उबला हुआ प्रोटीन।",
        "te": "ఆలివ్ ఆయిల్ మరియు నిమ్మకాయతో కూడిన ఆకుకూరల సలాడ్ మరియు ప్రోటీన్.",
        "ml": "ഒലിവ് ഓയിലും നാരങ്ങയും ചേർത്ത പച്ചക്കറി സലാഡും പ്രോട്ടീൻ உணവും.",
        "kn": "ಆಲೀವ್ ಎಣ್ಣೆ ಮತ್ತು ನಿಂಬೆಹಣ್ಣಿನೊಂದಿಗೆ ಹಸಿರು ತರಕಾರಿ ಸಲಾಡ್ ಮತ್ತು ಪ್ರೋಟೀನ್."
    },
    "Low sodium and rich in unsaturated fatty acids for heart-healthy lipid and BP support.": {
        "en": "Low sodium and rich in unsaturated fatty acids for heart-healthy lipid and BP support.",
        "ta": "குறைந்த சோடியம் மற்றும் ஆரோக்கியமான கொழுப்பு அமிலங்கள் இதயத்திற்கும் இரத்த அழுத்தத்திற்கும் நல்லது.",
        "hi": "कम सोडियम और स्वस्थ फैटी एसिड हृदय और रक्तचाप के लिए लाभदायक हैं।",
        "te": "తక్కువ సోడియం గుండె ఆరోగ్యం మరియు రక్తపోటుకు సహాయపడుతుంది.",
        "ml": "കുറഞ്ഞ സോഡിയം ഹൃദയാരോഗ്യത്തിനും രക്തസമ്മർദ്ദത്തിനും നല്ലതാണ്.",
        "kn": "ಕಡಿಮೆ ಸೋಡಿಯಂ ಹೃದಯದ ಆರೋಗ್ಯ ಮತ್ತು ರಕ್ತದೊತ್ತಡಕ್ಕೆ ಒಳ್ಳೆಯದು."
    },
    "Homemade unsalted roasted chickpeas or fresh carrot sticks with hummus.": {
        "en": "Homemade unsalted roasted chickpeas or fresh carrot sticks with hummus.",
        "ta": "வீட்டில் வறுத்த உப்பு இல்லாத கொண்டைக்கடலை அல்லது புதிய கேரட் துண்டுகள்.",
        "hi": "बिना नमक के भुने चने या ताजा गाजर के टुकड़े खाएं।",
        "te": "ఉప్పు లేని వేయించిన శనగలు లేదా క్యారట్ ముక్కలు.",
        "ml": "വറുത്ത കടല അല്ലെങ്കിൽ കാരറ്റ് കഷണങ്ങൾ.",
        "kn": "ಉಪ್ಪಿಲ್ಲದ ಹುರಿದ ಕಡಲೆ ಅಥವಾ ಕ್ಯಾರೆಟ್ ತುಂಡುಗಳು."
    },
    "Low-sodium, fiber-rich snack alternative to processed salty chips.": {
        "en": "Low-sodium, fiber-rich snack alternative to processed salty chips.",
        "ta": "சிப்ஸ்களுக்கு மாற்றாக குறைந்த சோடியம் கொண்ட நார்ச்சத்து நிறைந்த சிற்றுண்டி.",
        "hi": "नमकीन चिप्स के स्थान पर कम सोडियम वाला फाइबर युक्त नाश्ता।",
        "te": "చిప్స్‌కు ప్రత్యామ్నాయంగా తక్కువ సోడియం ఉన్న స్నాక్.",
        "ml": "ഉപ്പുള്ള ചിപ്സിന് പകരം നാരുള്ള ലഘുഭക്ഷണം.",
        "kn": "ಚಿಪ್ಸ್‌ಗೆ ಪರ್ಯಾಯವಾಗಿ ಕಡಿಮೆ ಸೋಡಿಯಂ ನಾರಿನ ಉಪಹಾರ."
    },
    "Baked fish or steamed tofu with roasted broccoli, cauliflower, and a small serving of sweet potato.": {
        "en": "Baked fish or steamed tofu with roasted broccoli, cauliflower, and a small serving of sweet potato.",
        "ta": "வேகவைத்த மீன் அல்லது டோஃபு, வறுத்த புரோக்கோலி, காலிஃப்ளவர் மற்றும் சர்க்கரைவள்ளிக்கிழங்கு.",
        "hi": "बेक्ड मछली या टोफू के साथ ब्रोकली, फूलगोभी और शकरकंद।",
        "te": "చేప లేదా టోఫుతో పాటు బ్రోకోలీ మరియు కాలీఫ్లవర్.",
        "ml": "വേവിച്ച മീൻ അല്ലെങ്കിൽ ടോഫു പച്ചക്കറികളോടൊപ്പം.",
        "kn": "ಬೇಯಿಸಿದ ಮೀನು ಅಥವಾ ಟೋಫು ತರಕಾರಿಗಳೊಂದಿಗೆ."
    },
    "Light evening meal with lean protein and non-starchy vegetables prevents overnight blood sugar elevation.": {
        "en": "Light evening meal with lean protein and non-starchy vegetables prevents overnight blood sugar elevation.",
        "ta": "இரவில் சர்க்கரை அளவு உயராமல் தடுக்க புரதம் மற்றும் காய்கறிகள் நிறைந்த இலகுவான உணவு.",
        "hi": "हल्का रात का भोजन रात भर रक्त शर्करा को बढ़ने से रोकता है।",
        "te": "లలితమైన రాత్రి భోజనం రాత్రి చక్కెర పెరగకుండా చూస్తుంది.",
        "ml": "ലഘുവായ അത്താഴം രാത്രിയിലെ പഞ്ചസാര വർദ്ധനവ് തടയുന്നു.",
        "kn": "ಹಗುರವಾದ ರಾತ್ರಿ ಊಟವು ರಕ್ತದ ಸಕ್ಕರೆ ಹೆಚ್ಚಾಗುವುದನ್ನು ತಡೆಯುತ್ತದೆ."
    },
    "General kidney wellness guidance only. Do NOT start restrictive renal diets, protein restrictions, or potassium/phosphorus adjustments without clinical dietitian oversight.": {
        "en": "General kidney wellness guidance only. Do NOT start restrictive renal diets, protein restrictions, or potassium/phosphorus adjustments without clinical dietitian oversight.",
        "ta": "பொதுவான சிறுநீரக ஆரோக்கிய வழிகாட்டுதல் மட்டுமே. தகுதியான உணவு நிபுணரின் ஆலோசனையின்றி கடுமையான உணவுக் கட்டுப்பாடுகளைத் தொடங்க வேண்டாம்.",
        "hi": "केवल सामान्य गुर्दे कल्याण मार्गदर्शन। आहार विशेषज्ञ की सलाह के बिना सख्त आहार शुरू न करें।",
        "te": "సాధారణ కిడ్నీ ఆరోగ్య మార్గదర్శకత్వం మాత్రమే. నిపుణుడి సలహా లేకుండా ఆహార నియమాలు ప్రారంభించవద్దు.",
        "ml": "പൊതുവായ വൃക്ക വെൽനസ് മാർഗ്ഗനിർദ്ദേശം മാത്രം. വിദഗ്ദ്ധന്റെ ഉപദേശമില്ലാതെ കടുത്ത ഭക്ഷണക്രമം ആരംഭിക്കരുത്.",
        "kn": "ಸಾಮಾನ್ಯ ಮೂತ್ರಪಿಂಡದ ವೆಲ್ನೆಸ್ ಮಾರ್ಗದರ್ಶನ ಮಾತ್ರ. ತಜ್ಞರ ಸಲಹೆಯಿಲ್ಲದೆ ಕಟ್ಟುನಿಟ್ಟಿನ ಆಹಾರಕ್ರಮವನ್ನು ಪ್ರಾರಂಭಿಸಬೇಡಿ."
    },

    # Exercise Strings
    "Morning Movement": {"en": "Morning Movement", "ta": "காலை உடற்பயிற்சி", "hi": "सुबह का व्यायाम", "te": "ఉదయం వ్యాయామం", "ml": "രാവിലത്തെ വ്യായാമം", "kn": "ಬೆಳಗಿನ ಚಟುವಟಿಕೆ"},
    "Afternoon Activity": {"en": "Afternoon Activity", "ta": "மதிய உடற்பயிற்சி", "hi": "दोपहर की गतिविधि", "te": "మధ్యాహ్నం వ్యాయామం", "ml": "ഉച്ചയ്ക്കത്തെ വ്യായാമം", "kn": "ಮಧ್ಯಾಹ್ನದ ಚಟುವಟಿಕೆ"},
    "Evening Stretch": {"en": "Evening Stretch", "ta": "மாலை உடற்பயிற்சி", "hi": "शाम का व्यायाम", "te": "సాయంత్రం వ్యాయామం", "ml": "വൈകുന്നേരത്തെ വ്യായാമം", "kn": "ಸಂಜೆಯ ಚಟುವಟಿಕೆ"},
    "Gentle morning warm-up and light joint mobility stretching.": {
        "en": "Gentle morning warm-up and light joint mobility stretching.",
        "ta": "மிதமான காலை பயிற்சி மற்றும் மூட்டு பயிற்சிகள்.",
        "hi": "हल्का सुबह का वार्म-अप और जोड़ों का व्यायाम।",
        "te": "ఉదయాన్నే తేలికపాటి వ్యాయామం మరియు స్ట్రెచింగ్.",
        "ml": "രാവിലത്തെ ലഘുവായ വ്യായാമവും സന്ധികളുടെ സ്ട്രെച്ചിംഗും.",
        "kn": "ಬೆಳಗಿನ ಹಗುರವಾದ ವ್ಯಾಯಾಮ ಮತ್ತು ಕೀಲುಗಳ ಚಲನೆ."
    },
    "Short indoor movement breaks or comfortable brisk walking around home/office.": {
        "en": "Short indoor movement breaks or comfortable brisk walking around home/office.",
        "ta": "வீடு அல்லது அலுவலகத்தில் மிதமான வேக நடைபயிற்சி.",
        "hi": "घर या कार्यालय के आसपास आरामदायक तेज चाल।",
        "te": "ఇల్లు లేదా ఆఫీసు చుట్టూ తేలికపాటి నడక.",
        "ml": "വീട്ടിലോ ഓഫീസിലോ ലഘുവായ നടത്തം.",
        "kn": "ಮನೆ ಅಥವಾ ಕಚೇರಿಯ ಸುತ್ತಲೂ ಹಗುರವಾದ ನಡಿಗೆ."
    },
    "Continuous outdoor or indoor brisk walking at a steady, comfortable pace.": {
        "en": "Continuous outdoor or indoor brisk walking at a steady, comfortable pace.",
        "ta": "சீரான வேகத்தில் தொடர்ச்சியான நடைபயிற்சி.",
        "hi": "एक समान, आरामदायक गति से निरंतर तेज चलना।",
        "te": "స్థిరమైన వేగంతో నిరంతర వేగవంతమైన నడక.",
        "ml": "സ്ഥിരമായ വേഗതയിലുള്ള തുടർച്ചയായ നടത്തം.",
        "kn": "ಸ್ಥಿರವಾದ ವೇಗದಲ್ಲಿ ಸತತ ಚುರುಕಾದ ನಡಿಗೆ."
    },
    "Relaxing evening posture stretching and slow deep-breathing mobility exercises.": {
        "en": "Relaxing evening posture stretching and slow deep-breathing mobility exercises.",
        "ta": "மாலை நேர தளர்வு பயிற்சிகள் மற்றும் ஆழ்ந்த மூச்சுப் பயிற்சி.",
        "hi": "शाम को आराम देने वाला खिंचाव और गहरा सांस लेने का व्यायाम।",
        "te": "సాయంత్రం విశ్రాంతి స్ట్రెచింగ్ మరియు దీర్ఘ శ్వాస వ్యాయామాలు.",
        "ml": "വൈകുന്നേരത്തെ റിലാക്സിംഗ് സ്ട്രെച്ചിംഗും ദീർഘ ശ്വാസോച്ഛ്വാസവും.",
        "kn": "ಸಂಜೆಯ ವಿಶ್ರಾಂತಿ ವ್ಯಾಯಾಮ ಮತ್ತು ಆಳವಾದ ಉಸಿರಾಟ."
    },
    "Discuss an appropriate exercise plan with a qualified healthcare professional before starting a new exercise program.": {
        "en": "Discuss an appropriate exercise plan with a qualified healthcare professional before starting a new exercise program.",
        "ta": "புதிய உடற்பயிற்சி திட்டத்தைத் தொடங்குவதற்கு முன் தகுதியான மருத்துவரிடம் ஆலோசிக்கவும்.",
        "hi": "नया व्यायाम शुरू करने से पहले डॉक्टर से परामर्श लें।",
        "te": "కొత్త వ్యాయామం ప్రారంభించే ముందు వైద్యుడిని సంప్రదించండి.",
        "ml": "പുതിയ വ്യായാമം തുടങ്ങുന്നതിന് മുൻപ് ഡോക്ടറോട് സംസാരിക്കുക.",
        "kn": "ಹೊಸ ವ್ಯಾಯಾಮ ಪ್ರಾರಂಭಿಸುವ ಮೊದಲು ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ."
    },
    "Pace your activities gradually. Listen to your body and stop immediately if you experience dizziness, shortness of breath, or chest discomfort.": {
        "en": "Pace your activities gradually. Listen to your body and stop immediately if you experience dizziness, shortness of breath, or chest discomfort.",
        "ta": "படிப்படியாக உடற்பயிற்சி செய்யுங்கள். தலைச்சுற்றல் அல்லது மூச்சுத்திணறல் ஏற்பட்டால் உடனடியாக நிறுத்தவும்.",
        "hi": "धीरे-धीरे शुरुआत करें। चक्कर आने या सांस फूलने पर तुरंत रुकें।",
        "te": "నెమ్మదిగా ప్రారంభించండి. మైకం లేదా శ్వాస తీసుకోవడంలో ఇబ్బంది ఉంటే వెంటనే ఆపండి.",
        "ml": "പതുക്കെ ആരംഭിക്കുക. തലകറക്കമോ ശ്വാസംമുട്ടലോ ഉണ്ടായാൽ ഉടൻ നിർത്തുക.",
        "kn": "ಮೆಲ್ಲನೆ ಪ್ರಾರಂಭಿಸಿ. ತಲೆತಿರುಗುವಿಕೆ ಅಥವಾ ಉಸಿರಾಟದ ತೊಂದರೆಯಾದರೆ ತಕ್ಷಣ ನಿಲ್ಲಿಸಿ."
    },

    "5–10 minutes": {"en": "5–10 minutes", "ta": "5-10 நிமிடங்கள்", "hi": "5-10 मिनट", "te": "5-10 నిమిషాలు", "ml": "5-10 മിനിറ്റ്", "kn": "5-10 ನಿಮಿಷಗಳು"},
    "10–15 minutes": {"en": "10–15 minutes", "ta": "10-15 நிமிடங்கள்", "hi": "10-15 मिनट", "te": "10-15 నిమిషాలు", "ml": "10-15 മിനിറ്റ്", "kn": "10-15 ನಿಮಿಷಗಳು"},
    "20–30 minutes": {"en": "20–30 minutes", "ta": "20-30 நிமிடங்கள்", "hi": "20-30 मिनट", "te": "20-30 నిమిషాలు", "ml": "20-30 മിനിറ്റ്", "kn": "20-30 ನಿಮಿಷಗಳು"},
    "Daily": {"en": "Daily", "ta": "தினமும்", "hi": "प्रतिदिन", "te": "ప్రతిరోజూ", "ml": "ദിവസവും", "kn": "ದಿನನಿತ್ಯ"},
    "5 days / week": {"en": "5 days / week", "ta": "வாரத்திற்கு 5 நாட்கள்", "hi": "सप्ताह में 5 दिन", "te": "వారానికి 5 రోజులు", "ml": "ആഴ്ചയിൽ 5 ദിവസം", "kn": "ವಾರಕ್ಕೆ 5 ದಿನಗಳು"},
    "Light / Low Intensity": {"en": "Light / Low Intensity", "ta": "லேசான தீவிரத்தன்மை", "hi": "हल्का/कम तीव्रता", "te": "తేలికపాటి తీవ్రత", "ml": "ലഘുവായ തീവ്രത", "kn": "ಹಗುರವಾದ ತೀವ್ರತೆ"},
    "Light to Moderate Intensity": {"en": "Light to Moderate Intensity", "ta": "லேசான முதல் மிதமான தீவிரத்தன்மை", "hi": "हल्का से मध्यम तीव्रता", "te": "తేలికపాటి నుండి మధ్యస్థ తీవ్రత", "ml": "ലഘുവിൽ നിന്ന് ഇടത്തരം തീവ്രത", "kn": "ಹಗುರದಿಂದ ಮಧ್ಯಮ ತೀವ್ರತೆ"},
    "Moderate Intensity": {"en": "Moderate Intensity", "ta": "மிதமான தீவிரத்தன்மை", "hi": "मध्यम तीव्रता", "te": "మధ్యస్థ తీవ్రత", "ml": "ഇടത്തരം തീവ്രത", "kn": "ಮಧ್ಯಮ ತೀವ್ರತೆ"},
    "Very Light / Restorative Intensity": {"en": "Very Light / Restorative Intensity", "ta": "மிக லேசான / தளர்வு தீவிரத்தன்மை", "hi": "बहुत हल्का/विश्राम तीव्रता", "te": "చాలా తేలికపాటి తీవ్రత", "ml": "വളരെ ലഘുവായ തീവ്രത", "kn": "ತುಂಬಾ ಹಗುರವಾದ ತೀವ್ರತೆ"},

    # Daily Habits Strings
    "Consistent Sleep Schedule": {"en": "Consistent Sleep Schedule", "ta": "சீராக உறங்கும் பழக்கம்", "hi": "निरंतर नींद का समय", "te": "స్థిరమైన నిద్ర సమయం", "ml": "കൃത്യമായ ഉറക്ക സമയം", "kn": "ಸ್ಥಿರವಾದ ನಿದ್ರೆಯ ವೇಳಾಪಟ್ಟಿ"},
    "Maintain 7–8 hours of uninterrupted sleep nightly to support metabolic and cardiovascular recovery.": {
        "en": "Maintain 7–8 hours of uninterrupted sleep nightly to support metabolic and cardiovascular recovery.",
        "ta": "இதயம் மற்றும் உடலின் ஆரோக்கியத்திற்காக இரவில் 7-8 மணிநேரம் தடையற்ற தூக்கத்தைப் பேணுங்கள்.",
        "hi": "हृदय और चयापचय के लिए हर रात 7-8 घंटे की नींद लें।",
        "te": "ఆరోగ్యం కోసం రాత్రికి 7-8 గంటల నిరంతర నిద్రపోవాలి.",
        "ml": "ആരോഗ്യത്തിന് രാത്രിയിൽ 7-8 മണിക്കൂർ തടസ്സമില്ലാത്ത ഉറക്കം ഉറപ്പാക്കുക.",
        "kn": "ಆರೋಗ್ಯಕ್ಕಾಗಿ ಪ್ರತಿ ರಾತ್ರಿ 7-8 ಗಂಟೆಗಳ ತಡೆರಹಿತ ನಿದ್ರೆ ಮಾಡಿ."
    },
    "Hourly Movement Breaks": {"en": "Hourly Movement Breaks", "ta": "மணிநேர இயக்கம்", "hi": "हर घंटे चलने का ब्रेक", "te": "గంటకోసారి నడక", "ml": "മണിക്കൂറിലുള്ള നടത്തം", "kn": "ಪ್ರತಿ ಗಂಟೆಗೆ ನಡಿಗೆ"},
    "Stand up and walk for 2–3 minutes for every hour of sitting to reduce vascular stiffness.": {
        "en": "Stand up and walk for 2–3 minutes for every hour of sitting to reduce vascular stiffness.",
        "ta": "ரத்த ஓட்டம் சீராக இருக்க ஒரு மணி நேரம் அமர்ந்த பிறகு 2-3 நிமிடங்கள் நடக்கவும்.",
        "hi": "रक्त वाहिकाओं के लिए हर घंटे 2-3 मिनट टहलें।",
        "te": "రక్త ప్రసరణ కోసం ప్రతి గంటకూ 2-3 నిమిషాలు నడవండి.",
        "ml": "രക്തചംക്രമണത്തിന് ഓരോ മണിക്കൂറിലും 2-3 മിനിറ്റ് നടക്കുക.",
        "kn": "ರಕ್ತಪರಿಚಲನೆಗಾಗಿ ಪ್ರತಿ ಗಂಟೆಗೆ 2-3 ನಿಮಿಷ ನಡೆಯಿರಿ."
    },
    "Adequate Water Intake": {"en": "Adequate Water Intake", "ta": "போதுமான நீர் அருந்துதல்", "hi": "पर्याप्त पानी का सेवन", "te": "సరిపడా నీరు తాగడం", "ml": "ആവശ്യത്തിന് വെള്ളം കുടിക്കുക", "kn": "ಸಾಕಷ್ಟು ನೀರು ಕುಡಿಯುವುದು"},
    "Drink sufficient water throughout the day to support kidney filtration and circulation.": {
        "en": "Drink sufficient water throughout the day to support kidney filtration and circulation.",
        "ta": "சிறுநீரகச் செயல்பாடு மற்றும் ரத்த ஓட்டத்திற்கு நாள் முழுவதும் தேவையான அளவு தண்ணீர் குடியுங்கள்.",
        "hi": "गुर्दे और रक्त परिसंचरण के लिए दिन भर पर्याप्त पानी पीएं।",
        "te": "కిడ్నీ ఆరోగ్యం కోసం రోజంతా తగినంత నీరు తాగండి.",
        "ml": "വൃക്ക ആരോഗ്യത്തിനായി ദിവസം മുഴുവൻ ആവശ്യത്തിന് വെള്ളം കുടിക്കുക.",
        "kn": "ಮೂತ್ರಪಿಂಡದ ಆರೋಗ್ಯಕ್ಕಾಗಿ ದಿನಪೂರ್ತಿ ಸಾಕಷ್ಟು ನೀರು ಕುಡಿಯಿರಿ."
    },
    "Mindful & Timely Meals": {"en": "Mindful & Timely Meals", "ta": "நேரத்திற்கு உணவு உட்கொள்ளல்", "hi": "समय पर भोजन", "te": "సమయానికి భోజనం", "ml": "കൃത്യസമയത്തുള്ള ഭക്ഷണം", "kn": "ಸಮಯಕ್ಕೆ ಸರಿಯಾಗಿ ಊಟ"},
    "Eat meals at consistent daily times and avoid heavy late-night snacking.": {
        "en": "Eat meals at consistent daily times and avoid heavy late-night snacking.",
        "ta": "தினமும் குறிப்பிட்ட நேரத்தில் சாப்பிடுங்கள், இரவில் தாமதமாக அதிக உணவு உண்பதைத் தவிர்க்கவும்.",
        "hi": "नियमित समय पर भोजन करें और देर रात भारी नाश्ते से बचें।",
        "te": "క్రమం తప్పకుండా సమయానికి తినండి మరియు రాత్రి ఆలస్యంగా తినవద్దు.",
        "ml": "കൃത്യസമയത്ത് ഭക്ഷണം കഴിക്കുക, വൈകുന്നേരത്തെ കനത്ത ഭക്ഷണം ഒഴിവാക്കുക.",
        "kn": "ಸರಿಯಾದ ಸಮಯಕ್ಕೆ ಊಟ ಮಾಡಿ ಮತ್ತು ರಾತ್ರಿ ತಡವಾಗಿ ತಿನ್ನುವುದನ್ನು ತಪ್ಪಿಸಿ."
    },
    "Tobacco Cessation Focus": {"en": "Tobacco Cessation Focus", "ta": "புகைபிடித்தலைத் தவிர்த்தல்", "hi": "तंबाकू छोड़ना", "te": "పొగాకు మానడం", "ml": "പുകയില ഉപേക്ഷിക്കുക", "kn": "ತಂಬಾಕು ಸೇವನೆ ತ್ಯಜಿಸುವುದು"},
    "Avoid direct smoking and secondhand tobacco smoke exposure to protect arterial walls.": {
        "en": "Avoid direct smoking and secondhand tobacco smoke exposure to protect arterial walls.",
        "ta": "இரத்த நாளங்களைப் பாதுகாக்க புகைபிடித்தல் மற்றும் புகையிலையைத் தவிர்க்கவும்.",
        "hi": "धमनियों की सुरक्षा के लिए धूम्रपान और तंबाकू से बचें।",
        "te": "రక్తనాళాల రక్షణ కోసం ధూమపానానికి దూరంగా ఉండండి.",
        "ml": "രക്തധമനികളുടെ സംരക്ഷണത്തിനായി പുകവലി ഒഴിവാക്കുക.",
        "kn": "ರಕ್ತನಾಳಗಳ ರಕ್ಷಣೆಗಾಗಿ ಧೂಮಪಾನವನ್ನು ತ್ಯಜಿಸಿ."
    },
    "Daily Stress Reduction": {"en": "Daily Stress Reduction", "ta": "தினசரி மன அழுத்தக் குறைப்பு", "hi": "दैनिक तनाव में कमी", "te": "రోజువారీ ఒత్తిడి నివారణ", "ml": "ദിനചര്യ സമ്മർദ്ദം കുറയ്ക്കൽ", "kn": "ದೈನಂದಿನ ಮಾನಸಿಕ ಒತ್ತಡ ಕಡಿಮೆ ಮಾಡುವುದು"},
    "Practice 10 minutes of deep abdominal breathing or mindfulness daily to lower sympathetic stress.": {
        "en": "Practice 10 minutes of deep abdominal breathing or mindfulness daily to lower sympathetic stress.",
        "ta": "மன அழுத்தத்தைக் குறைக்க தினமும் 10 நிமிடங்கள் ஆழ்ந்த மூச்சுப் பயிற்சி செய்யுங்கள்.",
        "hi": "तनाव कम करने के लिए रोजाना 10 मिनट गहरा सांस लें।",
        "te": "ఒత్తిడి తగ్గించుకోవడానికి ప్రతిరోజూ 10 నిమిషాలు ప్రాణాయామం చేయండి.",
        "ml": "സമ്മർദ്ദം കുറയ്ക്കാൻ ദിവസവും 10 മിനിറ്റ് ദീർഘ ശ്വാസമെടുക്കുക.",
        "kn": "ಒತ್ತಡವನ್ನು ಕಡಿಮೆ ಮಾಡಲು ಪ್ರತಿದಿನ 10 ನಿಮಿಷಗಳ ಕಾಲ ಆಳವಾದ ಉಸಿರಾಟದ ವ್ಯಾಯಾಮ ಮಾಡಿ."
    },
    "Routine Self-Monitoring": {"en": "Routine Self-Monitoring", "ta": "வழக்கமான சுய கண்காணிப்பு", "hi": "नियमित स्व-निगरानी", "te": "క్రమం తప్పకుండా స్వయంచాలక తనిఖీ", "ml": "പതിവ് സ്വയം പരിശോധന", "kn": "ನಿಯಮಿತ ಸ್ವಯಂ ಪರೀಕ್ಷೆ"},
    "Consistently log blood pressure, blood glucose, or weight as advised by your clinical team.": {
        "en": "Consistently log blood pressure, blood glucose, or weight as advised by your clinical team.",
        "ta": "மருத்துவரின் ஆலோசனைப்படி இரத்த அழுத்தம், சர்க்கரை அளவு அல்லது எடையைப் பதிவு செய்யுங்கள்.",
        "hi": "चिकित्सक की सलाह के अनुसार बीपी, शुगर और वजन रिकॉर्ड करें।",
        "te": "వైద్యుడి సలహా ప్రకారం బిపి, షుగర్ మరియు బరువును నమోదు చేయండి.",
        "ml": "ഡോക്ടറുടെ നിർദ്ദേശപ്രകാരം ബിപി, ഷുഗർ, ഭാരം എന്നിവ രേഖപ്പെടുത്തുക.",
        "kn": "ವೈದ್ಯರ ಸಲಹೆಯಂತೆ ಬಿಪಿ, ಸಕ್ಕರೆ ಮತ್ತು ತೂಕವನ್ನು ದಾಖಲಿಸಿ."
    },

    # Herbal Wellness Strings
    "Culinary Turmeric (Curcuma longa)": {"en": "Culinary Turmeric (Curcuma longa)", "ta": "சமையல் மஞ்சள் (Curcuma longa)", "hi": "रसोई की हल्दी", "te": "పసుపు", "ml": "മഞ്ഞൾ", "kn": "ಅರಿಶಿನ"},
    "Add a small pinch (1/4 tsp) to soups, cooked lentils, or warm food preparation.": {
        "en": "Add a small pinch (1/4 tsp) to soups, cooked lentils, or warm food preparation.",
        "ta": "சூப், சமைத்த பருப்பு அல்லது சூடான உணவில் ஒரு சிட்டிகை (1/4 தேக்கரண்டி) மஞ்சள் சேர்க்கவும்.",
        "hi": "सूप, दाल या गरम खाने में एक चुटकी हल्दी मिलाएं।",
        "te": "పప్పు లేదా సూప్‌లలో ఒక చిటికెడు పసుపు కలపండి.",
        "ml": "സൂപ്പിലോ പരിപ്പിലോ ഒരു നുള്ള് മഞ്ഞൾ ചേർക്കുക.",
        "kn": "ಸೂಪ್ ಅಥವಾ ಬೇಳೆಗೆ ಒಂದು ಚಿಟಿಕೆ ಅರಿಶಿನ ಸೇರಿಸಿ."
    },
    "Provides natural antioxidant phytonutrients for general culinary flavor and meal variety.": {
        "en": "Provides natural antioxidant phytonutrients for general culinary flavor and meal variety.",
        "ta": "உணவின் சுவைக்கும் ஆரோக்கியத்திற்கும் இயற்கை ஆன்டிஆக்ஸிடன்ட்களை வழங்குகிறது.",
        "hi": "भोजन के स्वाद और सामान्य स्वास्थ्य के लिए प्राकृतिक एंटीऑक्सीडेंट प्रदान करता है।",
        "te": "సహజమైన యాంటీఆక్సిడెంట్లను అందిస్తుంది.",
        "ml": "സ്വാഭാവിക ആന്റിഓക്സിഡന്റുകൾ നൽകുന്നു.",
        "kn": "ನೈಸರ್ಗಿಕ ಆಂಟಿಆಕ್ಸಿಡೆಂಟ್‌ಗಳನ್ನು ಒದಗಿಸುತ್ತದೆ."
    },
    "Fresh Ginger (Zingiber officinale)": {"en": "Fresh Ginger (Zingiber officinale)", "ta": "புதிய இஞ்சி (Zingiber officinale)", "hi": "ताजा अदरक", "te": "అల్లం", "ml": "ഇഞ്ചി", "kn": "ಶುಂಠಿ"},
    "Grate fresh ginger into warm water or culinary dishes.": {
        "en": "Grate fresh ginger into warm water or culinary dishes.",
        "ta": "சூடான நீர் அல்லது உணவில் புதிய இஞ்சியைத் துருவி சேர்க்கவும்.",
        "hi": "गुनगुने पानी या खाने में ताजा अदरक कद्दूकस करके डालें।",
        "te": "వేడి నీటిలో లేదా వంటలలో అల్లం తురుము కలపండి.",
        "ml": "ചൂടുവെള്ളത്തിലോ ഭക്ഷണത്തിലോ ഇഞ്ചി ചിരകിയത് ചേർക്കുക.",
        "kn": "ಬಿಸಿ ನೀರು ಅಥವಾ ಅಡುಗೆಯಲ್ಲಿ ಶುಂಠಿ ತುರಿ ಸೇರಿಸಿ."
    },
    "Aids digestion and adds natural flavor without added salt or sodium.": {
        "en": "Aids digestion and adds natural flavor without added salt or sodium.",
        "ta": "செரிமானத்திற்கு உதவுகிறது மற்றும் உப்பு இல்லாமல் இயற்கையான சுவையைத் தருகிறது.",
        "hi": "पाचन में मदद करता है और बिना नमक के प्राकृतिक स्वाद जोड़ता है।",
        "te": "జీర్ణక్రియకు సహాయపడుతుంది మరియు రుచిని ఇస్తుంది.",
        "ml": "ദഹനത്തിന് സഹായിക്കുകയും സ്വാഭാവിക രുചി നൽകുകയും ചെയ്യുന്നു.",
        "kn": "ಜೀರ್ಣಕ್ರಿಯೆಗೆ ಸಹಾಯ ಮಾಡುತ್ತದೆ."
    },
    "Ceylon Cinnamon (Cinnamomum verum)": {"en": "Ceylon Cinnamon (Cinnamomum verum)", "ta": "இலங்கை இலவங்கப்பட்டை (Cinnamomum verum)", "hi": "दालचीनी", "te": "దాల్చిన చెక్క", "ml": "കറുവാപ്പട്ട", "kn": "ದಾಲ್ಚಿನ್ನಿ"},
    "Sprinkle a pinch over morning oatmeal or unsweetened yogurt.": {
        "en": "Sprinkle a pinch over morning oatmeal or unsweetened yogurt.",
        "ta": "காலை ஓட்ஸ் அல்லது தயிரில் ஒரு சிட்டிகை இலவங்கப்பட்டை பொடி தூவவும்.",
        "hi": "सुबह के ओट्स या दही पर एक चुटकी दालचीनी छिड़कें।",
        "te": "ఉదయం ఓట్స్ లేదా పెరుగుపై ఒక చిటికెడు దాల్చిన పొడి చల్లండి.",
        "ml": "രാവിലത്തെ ഓട്സിലോ തൈരിലോ ഒരു നുള്ള് കറുവാപ്പട്ട പൊടി വിതറുക.",
        "kn": "ಬೆಳಗಿನ ಓಟ್ಸ್ ಅಥವಾ ಮೊಸರಿನ ಮೇಲೆ ಒಂದು ಚಿಟಿಕೆ ದಾಲ್ಚಿನ್ನಿ ಪುಡಿ ಉದುರಿಸಿ."
    },
    "Provides natural aromatic sweetness to meals without refined sugar.": {
        "en": "Provides natural aromatic sweetness to meals without refined sugar.",
        "ta": "சர்க்கரை இல்லாமல் உணவிற்கு இயற்கையான இனிப்பு சுவையைத் தருகிறது.",
        "hi": "बिना चीनी के भोजन को प्राकृतिक मिठास प्रदान करता है।",
        "te": "చక్కెర లేకుండా సహజ తియ్యదనాన్ని ఇస్తుంది.",
        "ml": "പഞ്ചസാരയില്ലാതെ സ്വാഭാവിക മധുരം നൽകുന്നു.",
        "kn": "ಸಕ್ಕರೆಯಿಲ್ಲದೆ ನೈಸರ್ಗಿಕ ಸಿಹಿಯನ್ನು ನೀಡುತ್ತದೆ."
    },
    "Fresh Mint & Holy Basil Leaves": {"en": "Fresh Mint & Holy Basil Leaves", "ta": "புதினா மற்றும் துளசி இலைகள்", "hi": "पुदीना और तुलसी की पत्तियां", "te": "పుదీనా మరియు తులసి ఆకులు", "ml": "പുതിന, തുളസി ഇലകൾ", "kn": "ಪುದೀನ ಮತ್ತು ತುಳಸಿ ಎಲೆಗಳು"},
    "Steep fresh mint leaves in warm water as a light home beverage.": {
        "en": "Steep fresh mint leaves in warm water as a light home beverage.",
        "ta": "புதிய புதினா இலைகளை சூடான நீரில் ஊறவைத்து லேசான பானமாக அருந்தவும்.",
        "hi": "ताजी पुदीने की पत्तियों को गरम पानी में मिलाकर पिएं।",
        "te": "వేడి నీటిలో పుదీనా ఆకులను నానబెట్టి తాగండి.",
        "ml": "ചൂടുവെള്ളത്തിൽ പുതിനയില ഇട്ട് പാനീയമായി കുടിക്കുക.",
        "kn": "ಬಿಸಿ ನೀರಿನಲ್ಲಿ ಪುದೀನ ಎಲೆಗಳನ್ನು ಹಾಕಿ ಪಾನೀಯವಾಗಿ ಕುಡಿಯಿರಿ."
    },
    "Comforting, soothing non-caffeinated herbal drink option.": {
        "en": "Comforting, soothing non-caffeinated herbal drink option.",
        "ta": "காஃபின் இல்லாத அமைதியான இயற்கை பானம்.",
        "hi": "कैफीन मुक्त आरामदायक हर्बल पेय।",
        "te": "కెఫిన్ లేని ప్రశాంతమైన మూలికా పానీయం.",
        "ml": "കഫീൻ ഇല്ലാത്ത ആശ്വാസകരമായ പാനീയം.",
        "kn": "ಕೆಫೀನ್ ಇಲ್ಲದ ಪ್ರಶಾಂತ ಮೂಲಿಕೆ ಪಾನೀಯ."
    },
    "Food-level herbs and spices may be used for meal variety, but herbal supplements or concentrated preparations should not be started based on this AI recommendation. Discuss herbal products with a qualified healthcare professional first.": {
        "en": "Food-level herbs and spices may be used for meal variety, but herbal supplements or concentrated preparations should not be started based on this AI recommendation. Discuss herbal products with a qualified healthcare professional first.",
        "ta": "உணவில் நறுமணப் பொருட்களைப் பயன்படுத்தலாம், ஆனால் AI பரிந்துரையின் அடிப்படையில் மூலிகைச் சாறுகளைப் பயன்படுத்தக் கூடாது.",
        "hi": "मसालों का उपयोग भोजन में किया जा सकता है, लेकिन इस AI सिफारिश के आधार पर सप्लीमेंट शुरू न करें।",
        "te": "వంటలలో సుగంధ ద్రవ్యాలు వాడవచ్చు, కానీ AI సూచనతో సప్లిమెంట్లను ప్రారంభించవద్దు.",
        "ml": "ഭക്ഷണത്തിൽ മസാലകൾ ഉപയോഗിക്കാം, എന്നാൽ AI നിർദ്ദേശപ്രകാരം സപ്ലിമെന്റുകൾ ആരംഭിക്കരുത്.",
        "kn": "ಅಡುಗೆಯಲ್ಲಿ ಸಾಂಬಾರು ಪದಾರ್ಥಗಳನ್ನು ಬಳಸಬಹುದು, ಆದರೆ AI ಸಲಹೆಯಂತೆ ಸಪ್ಲಿಮೆಂಟ್ಗಳನ್ನು ಪ್ರಾರಂಭಿಸಬೇಡಿ."
    },
    "Herbal and natural wellness suggestions are culinary food-level culinary options only and do not replace medical treatment. Do NOT start concentrated herbal extracts, capsules, or supplements without consulting a qualified healthcare professional.": {
        "en": "Herbal and natural wellness suggestions are culinary food-level culinary options only and do not replace medical treatment. Do NOT start concentrated herbal extracts, capsules, or supplements without consulting a qualified healthcare professional.",
        "ta": "மூலிகை மற்றும் இயற்கை ஆரோக்கிய பரிந்துரைகள் உணவு அளவிலான விருப்பங்கள் மட்டுமே. மருத்துவரை கலந்தாலோசிக்காமல் மூலிகை மாத்திரைகளைத் தொடங்க வேண்டாம்.",
        "hi": "हर्बल सुझाव केवल भोजन स्तर के विकल्प हैं। डॉक्टर की सलाह के बिना हर्बल सप्लीमेंट शुरू न करें।",
        "te": "మూలికా సూచనలు ఆహార స్థాయి ఎంపికలు మాత్రమే. డాక్టర్ సలహా లేకుండా మూలికా సప్లిమెంట్లను ఉపయోగించవద్దు.",
        "ml": "ഹെർബൽ നിർദ്ദേശങ്ങൾ ഭക്ഷണ തലത്തിലുള്ള ഓപ്ഷനുകൾ മാത്രമാണ്. ഡോക്ടറുടെ ഉപദേശമില്ലാതെ മരുന്നുകൾ ആരംഭിക്കരുത്.",
        "kn": "ಮೂಲಿಕೆ ಸಲಹೆಗಳು ಆಹಾರ ಮಟ್ಟದ ಆಯ್ಕೆಗಳು ಮಾತ್ರ. ವೈದ್ಯರ ಸಲಹೆಯಿಲ್ಲದೆ ಮೂಲಿಕೆ ಸಪ್ಲಿಮೆಂಟ್ಗಳನ್ನು ಪ್ರಾರಂಭಿಸಬೇಡಿ."
    }
}
