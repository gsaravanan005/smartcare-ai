import os
import sys
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and display total page count in standard IEEE format.
    """
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Header (Top)
        header_text = "IEEE TRANSACTIONS / CONFERENCE ON HEALTHCARE INFORMATICS & AI (ICHI-AI 2026)"
        self.drawString(36, 756, header_text)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 750, 576, 750)
        
        # Footer (Bottom)
        self.setFont("Helvetica", 8)
        footer_text = "SmartCare AI: Explainable Comorbidity-Aware Multi-Task Machine Learning Framework"
        self.drawString(36, 32, footer_text)
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 32, page_str)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 42, 576, 42)
        
        self.restoreState()


def build_pdf(filename="SmartCare_AI_IEEE_Conference_Paper.pdf"):
    pdf_path = os.path.abspath(filename)
    
    # Load authoritative experimental metadata
    meta_path = os.path.abspath("models/multitask/metadata.json")
    with open(meta_path, "r") as f:
        metadata = json.load(f)
    t2d_m = metadata["test_metrics"]["t2d"]
    cvd_m = metadata["test_metrics"]["cvd"]
    ckd_m = metadata["test_metrics"]["ckd"]
    bm = metadata["baseline_comparison"]
    ab = metadata["ablation_study"]

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#0f2942")   # Deep Navy
    c_accent = colors.HexColor("#0284c7")    # Vibrant Blue
    c_dark = colors.HexColor("#1e293b")      # Slate 800
    c_gray = colors.HexColor("#475569")      # Slate 600
    c_light = colors.HexColor("#f8fafc")     # Slate 50
    c_border = colors.HexColor("#e2e8f0")    # Slate 200

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'PaperTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14.5,
        leading=18,
        alignment=1, # Centered
        textColor=c_primary,
        spaceAfter=6
    )

    author_style = ParagraphStyle(
        'AuthorLine',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        alignment=1,
        textColor=c_dark,
        spaceAfter=2
    )

    affil_style = ParagraphStyle(
        'AffiliationLine',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=10,
        alignment=1,
        textColor=c_gray,
        spaceAfter=8
    )

    abstract_body = ParagraphStyle(
        'AbstractBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        alignment=4, # Justified
        textColor=c_dark
    )

    keywords_style = ParagraphStyle(
        'Keywords',
        parent=styles['Normal'],
        fontName='Helvetica-BoldOblique',
        fontSize=7.5,
        leading=10.5,
        textColor=c_dark,
        spaceAfter=8
    )

    sec_h1 = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=3,
        keepWithNext=True
    )

    sec_h2 = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=c_accent,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    body = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        alignment=4, # Justified
        textColor=c_dark,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_dark,
        leftIndent=10,
        spaceAfter=2
    )

    caption_style = ParagraphStyle(
        'FigCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        alignment=1,
        textColor=c_gray,
        spaceBefore=3,
        spaceAfter=8
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=9.5,
        textColor=c_dark
    )

    tbl_hdr_style = ParagraphStyle(
        'TblHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9,
        alignment=1,
        textColor=colors.white
    )

    tbl_cell_style = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.5,
        leading=8.5,
        alignment=0,
        textColor=c_dark
    )

    tbl_cell_center = ParagraphStyle(
        'TblCellCenter',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.5,
        leading=8.5,
        alignment=1,
        textColor=c_dark
    )

    story = []

    # -------------------------------------------------------------
    # 1. PAPER HEADER & METADATA
    # -------------------------------------------------------------
    story.append(Paragraph("SmartCare AI: An Explainable, Comorbidity-Aware Multi-Task Machine Learning Framework for Early Chronic Disease Risk Stratification and Clinical Decision Support", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("SmartCare AI Research & Engineering Consortium", author_style))
    story.append(Paragraph("Department of Computer Science & Engineering &bull; Healthcare Informatics Lab &bull; Clinical Intelligence Group<br/>IEEE Conference on Healthcare Informatics, Systems and Artificial Intelligence (ICHI-AI 2026)", affil_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceBefore=0, spaceAfter=6))

    # Abstract Box
    abstract_text = (
        "<b><i>Abstract</i>—Chronic non-communicable diseases—specifically Type 2 Diabetes (T2D), Cardiovascular Disease (CVD), and Chronic Kidney Disease (CKD)—represent the leading causes of global mortality and healthcare expenditure. In clinical reality, these conditions share mutual pathophysiology and compounding vascular damage. Conventional single-disease diagnostic models fail to capture these intricate comorbidity synergies and operate as siloed 'black boxes.' In this paper, we propose <i>SmartCare AI</i>, a unified clinical machine learning framework that delivers comorbidity-aware multi-task risk stratification, rigorous probability calibration, game-theoretic explainability, and evidence-based wellness interventions. Our architecture harmonizes heterogeneous clinical datasets (BRFSS 2015 N=70,692; Kaggle CVD N=68,205; UCI CKD N=400) into a standardized 30-dimensional shared feature representation. We enforce strict leakage-free preprocessing with training-fitted median imputation and RobustScaler transformations. A shared neural encoder network with task-masked loss and task-balanced batch sampling (20% CKD allocation) is jointly trained across all three conditions and calibrated via Platt sigmoid scaling. On strictly isolated, held-out test splits, SmartCare AI achieves robust performance: T2D (ROC-AUC: 0.8276, Recall: 88.72%, F1: 0.7751, Brier: 0.1682), CVD (ROC-AUC: 0.7974, Recall: 79.13%, F1: 0.7306, Brier: 0.1827), and CKD (ROC-AUC: 0.9953, Recall: 94.59%, F1: 0.9589, Brier: 0.0490). We benchmark against Logistic Regression, Random Forest, and XGBoost baselines on identical test partitions. Game-theoretic SHAP explainability exposes global biomarker rankings and patient-level attributions, parameterizing automated clinical guidelines and longitudinal risk alerts within an enterprise FastAPI microservice layer and MongoDB database. SmartCare AI establishes a reproducible, scientifically grounded benchmark for next-generation clinical decision support systems.</b>"
    )
    
    abstract_box = Table([[Paragraph(abstract_text, abstract_body)]], colWidths=[540])
    abstract_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light),
        ('BOX', (0,0), (-1,-1), 0.5, c_accent),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(abstract_box)
    story.append(Spacer(1, 4))

    keywords_text = "<b><i>Index Terms</i>—Comorbidity-Aware Prediction, Multi-Task Learning, Shared Feature Representation, Explainable AI (XAI), SHAP Values, Platt Calibration, Cardio-Renal-Metabolic Syndrome, Type 2 Diabetes, Cardiovascular Disease, Chronic Kidney Disease, CDSS, FastAPI, MongoDB.</b>"
    story.append(Paragraph(keywords_text, keywords_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=c_border, spaceBefore=0, spaceAfter=6))

    # -------------------------------------------------------------
    # SECTION I: INTRODUCTION & CLINICAL MOTIVATION
    # -------------------------------------------------------------
    story.append(Paragraph("I. INTRODUCTION & CLINICAL MOTIVATION", sec_h1))
    story.append(Paragraph(
        "Chronic non-communicable diseases (NCDs) constitute the foremost clinical and economic burden worldwide, accounting for over 74% of all annual deaths globally according to the World Health Organization (WHO). Among these, Type 2 Diabetes Mellitus (T2D), Cardiovascular Disease (CVD), and Chronic Kidney Disease (CKD) form an interconnected, multi-system pathological triad known clinically as the <i>Cardio-Renal-Metabolic (CRM) Syndrome</i>. Endothelial dysfunction, systemic microvascular inflammation, chronic hypertension, and dyslipidemia act as mutually compounding drivers across all three organs.",
        body
    ))
    story.append(Paragraph(
        "Despite their intrinsic interdependencies, traditional diagnostic workflows and existing machine learning (ML) diagnostic applications predominantly address these diseases as isolated, single-label classification problems. This siloed methodology presents several critical failure modes: (1) <b>Comorbidity Blindness</b>: models trained exclusively on single disease indicators miss cross-organ risk amplifications; (2) <b>Uncalibrated Overconfidence</b>: standard ML classifiers produce raw output scores that deviate from true empirical probabilities, leading to misinformed triaging; (3) <b>The Explainability Gap</b>: complex black-box architectures prevent clinicians from verifying why a patient was classified as high risk; and (4) <b>Lack of Actionable Linkage</b>: prediction systems rarely bridge estimated risks to guideline-adherent dietary, lifestyle, or specialist intervention pathways.",
        body
    ))
    story.append(Paragraph(
        "To address these challenges, we introduce <b>SmartCare AI</b>: a modular, transparent, and comorbidity-aware multi-task predictive platform. SmartCare AI unifies multi-source clinical data ingestion, a 30-dimensional harmonized feature representation, joint multi-task representation learning, Platt probability calibration, game-theoretic SHAP explainability, evidence-based wellness guidance, and longitudinal monitoring into an integrated clinical decision support system (CDSS).",
        body
    ))

    # -------------------------------------------------------------
    # SECTION II: SYSTEM ARCHITECTURE & 6 CORE MODULES
    # -------------------------------------------------------------
    story.append(Paragraph("II. SYSTEM ARCHITECTURE & MODULAR PIPELINE", sec_h1))
    story.append(Paragraph(
        "SmartCare AI is engineered as a decoupled, six-stage microservice architecture backed by an enterprise NoSQL database and asynchronous RESTful APIs:",
        body
    ))
    story.append(Paragraph("&bull; <b>Module 1 (Data Ingestion & Leakage-Free Preprocessing):</b> Harmonizes multi-cohort clinical features into a unified 30-dimensional schema, performing stratified cohort splits and fitting median imputers and RobustScalers strictly on training data.", bullet_style))
    story.append(Paragraph("&bull; <b>Module 2 (Multi-Task Learning & Risk Stratification):</b> Trains a shared neural encoder network with task-specific heads, task-masked BCE loss, and task-balanced batch sampling (20% CKD allocation), followed by post-hoc Platt sigmoid probability calibration.", bullet_style))
    story.append(Paragraph("&bull; <b>Module 3 (Explainable AI & Risk Attribution):</b> Computes TreeSHAP and KernelSHAP attributions to expose global population rankings and local patient waterfall decompositions.", bullet_style))
    story.append(Paragraph("&bull; <b>Module 4 (Personalized Wellness & Clinical Guidance):</b> Maps SHAP risk drivers directly into evidence-based dietary, exercise, smoking cessation, and specialist consultation protocols.", bullet_style))
    story.append(Paragraph("&bull; <b>Module 5 (Risk Monitoring & Longitudinal CDSS):</b> Tracks longitudinal multi-disease trajectory alerts over time, computing biomarker velocity and triggering multi-tier clinician notifications.", bullet_style))
    story.append(Paragraph("&bull; <b>Module 6 (Interactive Dashboard & LLM Wellness Chatbot):</b> Provides a responsive glassmorphism web console with multi-language support (English, Spanish, Hindi, Tamil) and a context-bounded conversational wellness assistant.", bullet_style))

    # Figure 8: End-to-End Pipeline Flow
    fig8_path = os.path.abspath("artifacts/paper_figures/fig8_explainable_prediction_pipeline.png")
    if os.path.exists(fig8_path):
        story.append(Spacer(1, 2))
        img = Image(fig8_path, width=510, height=195)
        story.append(img)
        story.append(Paragraph("<b>Fig. 1.</b> End-to-End Explainable Multi-Task Prediction, Feature Attribution, and Clinical Guidance Flow across SmartCare AI.", caption_style))

    # -------------------------------------------------------------
    # SECTION III: DATASETS & 30-FEATURE HARMONIZATION
    # -------------------------------------------------------------
    story.append(Paragraph("III. DATASETS & 30-FEATURE HARMONIZATION", sec_h1))
    story.append(Paragraph(
        "SmartCare AI utilizes three distinct clinical datasets representing diverse demographic, behavioral, and physiological cohorts: (1) <b>CDC BRFSS 2015 Diabetes Cohort</b> ($N = 70,692$), a 50-50 balanced survey dataset with 21 behavioral and demographic indicators; (2) <b>Cardiovascular Disease Cohort</b> ($N = 68,205$), containing measured vitals and hemodynamic attributes; and (3) <b>UCI Chronic Kidney Disease Cohort</b> ($N = 400$), providing detailed laboratory biochemistry and urinalysis parameters.",
        body
    ))
    story.append(Paragraph(
        "Because these source datasets originate from separate studies and survey instruments, they observe differing subsets of variables. Rather than fabricating measurements or using invalid surrogates (e.g., treating CAD as smoking status, inferring previous heart attacks from high blood pressure, or deriving glucose from cholesterol), SmartCare AI defines an explicit <b>30-Dimensional Harmonized Shared Feature Schema</b>. Unobserved features within each cohort are represented as missing ($\text{NaN}$) during feature extraction and imputed using a training-fitted median imputation mechanism.",
        body
    ))

    # TABLE II: 30-Feature Mapping Table
    story.append(Paragraph("A. Authoritative 30-Feature Mapping Specification", sec_h2))
    
    mapping_rows = [
        [Paragraph("<b>#</b>", tbl_hdr_style),
         Paragraph("<b>Unified Feature</b>", tbl_hdr_style),
         Paragraph("<b>T2D Source (BRFSS)</b>", tbl_hdr_style),
         Paragraph("<b>CVD Source (Cardio)</b>", tbl_hdr_style),
         Paragraph("<b>CKD Source (UCI)</b>", tbl_hdr_style),
         Paragraph("<b>Transformation / Derivation Logic</b>", tbl_hdr_style)],
        
        [Paragraph("1", tbl_cell_center), Paragraph("age_years", tbl_cell_style), Paragraph("Age (1-13)", tbl_cell_style), Paragraph("age (days) / age_years", tbl_cell_style), Paragraph("age", tbl_cell_style), Paragraph("Midpoint years (T2D); age/365.25 (CVD); Direct (CKD)", tbl_cell_style)],
        [Paragraph("2", tbl_cell_center), Paragraph("gender", tbl_cell_style), Paragraph("Sex (0=F, 1=M)", tbl_cell_style), Paragraph("gender (1=F, 2=M)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("Binary flag (0.0=Female, 1.0=Male); Median imputed (CKD)", tbl_cell_style)],
        [Paragraph("3", tbl_cell_center), Paragraph("education", tbl_cell_style), Paragraph("Education (1-6)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("Ordinal education tier (1-6); Median imputed (CVD/CKD)", tbl_cell_style)],
        [Paragraph("4", tbl_cell_center), Paragraph("income", tbl_cell_style), Paragraph("Income (1-8)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("Ordinal income level (1-8); Median imputed (CVD/CKD)", tbl_cell_style)],
        [Paragraph("5", tbl_cell_center), Paragraph("bmi", tbl_cell_style), Paragraph("BMI", tbl_cell_style), Paragraph("bmi / height, weight", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("Body Mass Index (kg/m²); Median imputed (CKD)", tbl_cell_style)],
        [Paragraph("6", tbl_cell_center), Paragraph("high_bp", tbl_cell_style), Paragraph("HighBP (0/1)", tbl_cell_style), Paragraph("ap_hi, ap_lo", tbl_cell_style), Paragraph("htn (yes/no)", tbl_cell_style), Paragraph("Observed flag (T2D/CKD); Derived ap_hi>=140 or ap_lo>=90 (CVD)", tbl_cell_style)],
        [Paragraph("7", tbl_cell_center), Paragraph("ap_hi", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("ap_hi", tbl_cell_style), Paragraph("bp", tbl_cell_style), Paragraph("Systolic BP (mmHg); Clipped [80, 220]; Median imputed (T2D)", tbl_cell_style)],
        [Paragraph("8", tbl_cell_center), Paragraph("ap_lo", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("ap_lo", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("Diastolic BP (mmHg); Clipped [50, 140]; Median imputed (T2D/CKD)", tbl_cell_style)],
        [Paragraph("9", tbl_cell_center), Paragraph("pulse_pressure", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("ap_hi, ap_lo", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("Derived: PP = ap_hi - ap_lo; Median imputed (T2D/CKD)", tbl_cell_style)],
        [Paragraph("10", tbl_cell_center), Paragraph("mean_arterial_pressure", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("ap_hi, ap_lo", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("Derived: MAP = ap_lo + PP/3; Median imputed (T2D/CKD)", tbl_cell_style)],
        [Paragraph("11", tbl_cell_center), Paragraph("cholesterol", tbl_cell_style), Paragraph("HighChol (0/1)", tbl_cell_style), Paragraph("cholesterol (1-3)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("Binary (T2D); Ordinal (CVD); Median imputed (CKD)", tbl_cell_style)],
        [Paragraph("12", tbl_cell_center), Paragraph("glucose", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("gluc (1-3)", tbl_cell_style), Paragraph("bgr", tbl_cell_style), Paragraph("Midpoint (100, 140, 200 mg/dL) from CVD; Measured BGR (CKD)", tbl_cell_style)],
        [Paragraph("13", tbl_cell_center), Paragraph("serum_creatinine", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("sc", tbl_cell_style), Paragraph("Serum creatinine (mg/dL); Clipped [0.4, 15.0]; Median imputed (T2D/CVD)", tbl_cell_style)],
        [Paragraph("14", tbl_cell_center), Paragraph("blood_urea", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("bu", tbl_cell_style), Paragraph("Blood urea nitrogen (mg/dL); Clipped [5.0, 200.0]; Median (T2D/CVD)", tbl_cell_style)],
        [Paragraph("15", tbl_cell_center), Paragraph("hemoglobin", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("hemo", tbl_cell_style), Paragraph("Hemoglobin (g/dL); Clipped [3.0, 20.0]; Median (T2D/CVD)", tbl_cell_style)],
        [Paragraph("16", tbl_cell_center), Paragraph("albumin_level", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("al (0-5)", tbl_cell_style), Paragraph("Urinary dipstick albumin (0-5); Median imputed (T2D/CVD)", tbl_cell_style)],
        [Paragraph("17", tbl_cell_center), Paragraph("specific_gravity", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("sg", tbl_cell_style), Paragraph("Urine specific gravity (1.005-1.025); Median imputed (T2D/CVD)", tbl_cell_style)],
        [Paragraph("18", tbl_cell_center), Paragraph("bun_creatinine_ratio", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("bu, sc", tbl_cell_style), Paragraph("Derived: bu / max(sc, 0.1), clipped at 100.0; Median (T2D/CVD)", tbl_cell_style)],
        [Paragraph("19", tbl_cell_center), Paragraph("egfr_proxy", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("sc, age", tbl_cell_style), Paragraph("Derived MDRD proxy: 175 * sc^(-1.154) * age^(-0.203) (CKD)", tbl_cell_style)],
        [Paragraph("20", tbl_cell_center), Paragraph("anemia_flag", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("ane, hemo", tbl_cell_style), Paragraph("Binary flag: ane=='yes' or hemo<12.0 g/dL; Median (T2D/CVD)", tbl_cell_style)],
        [Paragraph("21", tbl_cell_center), Paragraph("smoker", tbl_cell_style), Paragraph("Smoker (0/1)", tbl_cell_style), Paragraph("smoke (0/1)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("Tobacco smoking status binary flag; Median imputed (CKD)", tbl_cell_style)],
        [Paragraph("22", tbl_cell_center), Paragraph("phys_activity", tbl_cell_style), Paragraph("PhysActivity (0/1)", tbl_cell_style), Paragraph("active (0/1)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("Physical exercise indicator; Median imputed (CKD)", tbl_cell_style)],
        [Paragraph("23", tbl_cell_center), Paragraph("alcohol_consumption", tbl_cell_style), Paragraph("HvyAlcoholConsump (0/1)", tbl_cell_style), Paragraph("alco (0/1)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("Heavy alcohol consumption flag; Median imputed (CKD)", tbl_cell_style)],
        [Paragraph("24", tbl_cell_center), Paragraph("fruits", tbl_cell_style), Paragraph("Fruits (0/1)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("Daily fruit consumption indicator; Median imputed (CVD/CKD)", tbl_cell_style)],
        [Paragraph("25", tbl_cell_center), Paragraph("veggies", tbl_cell_style), Paragraph("Veggies (0/1)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("Daily vegetable consumption indicator; Median (CVD/CKD)", tbl_cell_style)],
        [Paragraph("26", tbl_cell_center), Paragraph("heart_disease_or_attack", tbl_cell_style), Paragraph("HeartDiseaseorAttack (0/1)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("cad (yes/no)", tbl_cell_style), Paragraph("Prior myocardial infarction / CAD history; Median imputed (CVD)", tbl_cell_style)],
        [Paragraph("27", tbl_cell_center), Paragraph("stroke", tbl_cell_style), Paragraph("Stroke (0/1)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("Prior stroke history binary indicator; Median imputed (CVD/CKD)", tbl_cell_style)],
        [Paragraph("28", tbl_cell_center), Paragraph("diff_walk", tbl_cell_style), Paragraph("DiffWalk (0/1)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("Mobility limitation / walking difficulty; Median (CVD/CKD)", tbl_cell_style)],
        [Paragraph("29", tbl_cell_center), Paragraph("gen_hlth", tbl_cell_style), Paragraph("GenHlth (1-5)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("-- (Unavailable)", tbl_cell_style), Paragraph("Self-reported general health ordinal rating; Median (CVD/CKD)", tbl_cell_style)],
        [Paragraph("30", tbl_cell_center), Paragraph("combined_vascular_risk", tbl_cell_style), Paragraph("Composite Risk", tbl_cell_style), Paragraph("Composite Risk", tbl_cell_style), Paragraph("Composite Risk", tbl_cell_style), Paragraph("Derived additive cardiometabolic index summing active risk flags", tbl_cell_style)],
    ]

    t_map = Table(mapping_rows, colWidths=[18, 92, 85, 85, 75, 185])
    t_map.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light])
    ]))
    story.append(t_map)
    story.append(Paragraph("<b>TABLE I:</b> Authoritative 30-Feature Harmonization Specification Across T2D, CVD, and CKD Cohorts.", caption_style))

    # -------------------------------------------------------------
    # SECTION IV: MULTI-TASK ARCHITECTURE & PROBABILITY CALIBRATION
    # -------------------------------------------------------------
    story.append(Paragraph("IV. MULTI-TASK LEARNING ARCHITECTURE & PROBABILITY CALIBRATION", sec_h1))
    story.append(Paragraph(
        "SmartCare AI implements a unified Multi-Task Deep Neural Network featuring a <b>Shared Feature Encoder</b> and three task-specific classification heads. The shared encoder comprises two fully connected layers with Layer Normalization, ReLU activations, and Dropout: $\\text{Dense}(30 \\to 64) \\to \\text{LayerNorm} \\to \\text{ReLU} \\to \\text{Dropout}(0.15) \\to \\text{Dense}(64 \\to 32) \\to \\text{LayerNorm} \\to \\text{ReLU}$, yielding a 32-dimensional shared latent representation $\\mathbf{z} \\in \\mathbb{R}^{32}$.",
        body
    ))
    story.append(Paragraph(
        "Each task head $k \\in \\{\\text{T2D}, \\text{CVD}, \\text{CKD}\\}$ processes $\\mathbf{z}$ through a dedicated projection: $\\text{Dense}(32 \\to 16) \\to \\text{ReLU} \\to \\text{Dense}(16 \\to 1) \\to \\text{Sigmoid}$, outputting uncalibrated task probability $\\hat{y}_k$.",
        body
    ))
    story.append(Paragraph(
        "To prevent gradient contamination across disjoint dataset labels, training utilizes a <b>Task-Masked Binary Cross-Entropy Loss</b>:",
        body
    ))
    story.append(Paragraph(
        "$$\\mathcal{L}_{\\text{total}}(\\theta) = \\sum_{k \\in \\{\\text{T2D},\\text{CVD},\\text{CKD}\\}} w_k \\cdot \\frac{1}{\\sum_{i} m_i^{(k)}} \\sum_{i=1}^N m_i^{(k)} \\cdot \\text{BCE}\\left(y_i^{(k)}, \\hat{y}_i^{(k)}\\right) + \\lambda \\|\\theta\\|_2^2$$",
        code_style
    ))
    story.append(Paragraph(
        "where $m_i^{(k)} \\in \\{0, 1\\}$ indicates whether sample $i$ possesses a validated label for task $k$. Task weights are configured as $w_{\\text{T2D}} = 1.0, w_{\\text{CVD}} = 1.0, w_{\\text{CKD}} = 2.5$. To prevent the small CKD cohort ($N=280$ training samples) from being overwhelmed by the larger T2D and CVD cohorts, mini-batches are constructed with <b>Task-Balanced Sampling</b> (20% CKD samples drawn with replacement on the training split only; validation and test splits are strictly untouched).",
        body
    ))
    story.append(Paragraph(
        "<b>Post-Hoc Platt Sigmoid Probability Calibration:</b> To transform raw model logits into well-calibrated risk probabilities, Platt sigmoid scalers are fitted on independent validation folds $\\mathcal{D}_{\\text{val}}$: $\\hat{P}(y=1 \\mid x) = [1 + \\exp(A \\cdot f(x) + B)]^{-1}$. Optimal decision thresholds $T^*$ are tuned on $\\mathcal{D}_{\\text{val}}$ under clinical sensitivity constraints ($T^*_{\\text{T2D}} = 0.39, T^*_{\\text{CVD}} = 0.39, T^*_{\\text{CKD}} = 0.23$).",
        body
    ))

    # -------------------------------------------------------------
    # SECTION V: EXPERIMENTAL RESULTS & BENCHMARKS
    # -------------------------------------------------------------
    story.append(Paragraph("V. EMPIRICAL EXPERIMENTAL RESULTS & BENCHMARKS", sec_h1))
    story.append(Paragraph(
        "All models were evaluated on strictly isolated, held-out test splits (T2D $N=10,604$; CVD $N=10,231$; CKD $N=60$). Performance across clinical metrics, calibration metrics, and confusion matrices is summarized in Table II.",
        body
    ))

    # Table II: Test Metrics
    test_metrics_table = [
        [Paragraph("<b>Target Disease</b>", tbl_hdr_style),
         Paragraph("<b>Architecture</b>", tbl_hdr_style),
         Paragraph("<b>Accuracy</b>", tbl_hdr_style),
         Paragraph("<b>Precision</b>", tbl_hdr_style),
         Paragraph("<b>Recall (Sens.)</b>", tbl_hdr_style),
         Paragraph("<b>Specificity</b>", tbl_hdr_style),
         Paragraph("<b>F1-Score</b>", tbl_hdr_style),
         Paragraph("<b>ROC-AUC</b>", tbl_hdr_style),
         Paragraph("<b>PR-AUC</b>", tbl_hdr_style),
         Paragraph("<b>Brier Score</b>", tbl_hdr_style),
         Paragraph("<b>ECE</b>", tbl_hdr_style)],
        
        [Paragraph("T2D", tbl_cell_center), Paragraph("MTL Shared Net", tbl_cell_style), Paragraph(f"{t2d_m['accuracy']*100:.2f}%", tbl_cell_center), Paragraph(f"{t2d_m['precision']*100:.2f}%", tbl_cell_center), Paragraph(f"{t2d_m['recall']*100:.2f}%", tbl_cell_center), Paragraph(f"{t2d_m['specificity']*100:.2f}%", tbl_cell_center), Paragraph(f"{t2d_m['f1_score']:.4f}", tbl_cell_center), Paragraph(f"{t2d_m['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{t2d_m['pr_auc']:.4f}", tbl_cell_center), Paragraph(f"{t2d_m['brier_score']:.4f}", tbl_cell_center), Paragraph(f"{t2d_m['ece']:.4f}", tbl_cell_center)],
        [Paragraph("CVD", tbl_cell_center), Paragraph("MTL Shared Net", tbl_cell_style), Paragraph(f"{cvd_m['accuracy']*100:.2f}%", tbl_cell_center), Paragraph(f"{cvd_m['precision']*100:.2f}%", tbl_cell_center), Paragraph(f"{cvd_m['recall']*100:.2f}%", tbl_cell_center), Paragraph(f"{cvd_m['specificity']*100:.2f}%", tbl_cell_center), Paragraph(f"{cvd_m['f1_score']:.4f}", tbl_cell_center), Paragraph(f"{cvd_m['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{cvd_m['pr_auc']:.4f}", tbl_cell_center), Paragraph(f"{cvd_m['brier_score']:.4f}", tbl_cell_center), Paragraph(f"{cvd_m['ece']:.4f}", tbl_cell_center)],
        [Paragraph("CKD", tbl_cell_center), Paragraph("MTL Shared Net", tbl_cell_style), Paragraph(f"{ckd_m['accuracy']*100:.2f}%", tbl_cell_center), Paragraph(f"{ckd_m['precision']*100:.2f}%", tbl_cell_center), Paragraph(f"{ckd_m['recall']*100:.2f}%", tbl_cell_center), Paragraph(f"{ckd_m['specificity']*100:.2f}%", tbl_cell_center), Paragraph(f"{ckd_m['f1_score']:.4f}", tbl_cell_center), Paragraph(f"{ckd_m['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{ckd_m['pr_auc']:.4f}", tbl_cell_center), Paragraph(f"{ckd_m['brier_score']:.4f}", tbl_cell_center), Paragraph(f"{ckd_m['ece']:.4f}", tbl_cell_center)]
    ]
    t_test = Table(test_metrics_table, colWidths=[35, 75, 45, 45, 52, 48, 45, 48, 48, 50, 49])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light])
    ]))
    story.append(t_test)
    story.append(Paragraph("<b>TABLE II:</b> Empirical Test-Set Performance across Multi-Task Shared Representation Network Disease Heads.", caption_style))

    # Baseline Table
    story.append(Paragraph("A. Baseline Model Comparison on Identical Test Partitions", sec_h2))
    bm = metadata["baseline_comparison"]
    base_rows = [
        [Paragraph("<b>Target</b>", tbl_hdr_style),
         Paragraph("<b>Model Architecture</b>", tbl_hdr_style),
         Paragraph("<b>Accuracy</b>", tbl_hdr_style),
         Paragraph("<b>Recall (Sens.)</b>", tbl_hdr_style),
         Paragraph("<b>F1-Score</b>", tbl_hdr_style),
         Paragraph("<b>ROC-AUC</b>", tbl_hdr_style),
         Paragraph("<b>PR-AUC</b>", tbl_hdr_style),
         Paragraph("<b>Brier Score</b>", tbl_hdr_style)],
        
        [Paragraph("T2D", tbl_cell_center), Paragraph("Logistic Regression", tbl_cell_style), Paragraph(f"{bm['t2d']['Logistic Regression']['accuracy']*100:.2f}%", tbl_cell_center), Paragraph(f"{bm['t2d']['Logistic Regression']['recall']*100:.2f}%", tbl_cell_center), Paragraph(f"{bm['t2d']['Logistic Regression']['f1_score']:.4f}", tbl_cell_center), Paragraph(f"{bm['t2d']['Logistic Regression']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{bm['t2d']['Logistic Regression']['pr_auc']:.4f}", tbl_cell_center), Paragraph(f"{bm['t2d']['Logistic Regression']['brier_score']:.4f}", tbl_cell_center)],
        [Paragraph("T2D", tbl_cell_center), Paragraph("Random Forest", tbl_cell_style), Paragraph(f"{bm['t2d']['Random Forest']['accuracy']*100:.2f}%", tbl_cell_center), Paragraph(f"{bm['t2d']['Random Forest']['recall']*100:.2f}%", tbl_cell_center), Paragraph(f"{bm['t2d']['Random Forest']['f1_score']:.4f}", tbl_cell_center), Paragraph(f"{bm['t2d']['Random Forest']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{bm['t2d']['Random Forest']['pr_auc']:.4f}", tbl_cell_center), Paragraph(f"{bm['t2d']['Random Forest']['brier_score']:.4f}", tbl_cell_center)],
        [Paragraph("T2D", tbl_cell_center), Paragraph("XGBoost Classifier", tbl_cell_style), Paragraph(f"{bm['t2d']['XGBoost']['accuracy']*100:.2f}%", tbl_cell_center), Paragraph(f"{bm['t2d']['XGBoost']['recall']*100:.2f}%", tbl_cell_center), Paragraph(f"{bm['t2d']['XGBoost']['f1_score']:.4f}", tbl_cell_center), Paragraph(f"{bm['t2d']['XGBoost']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{bm['t2d']['XGBoost']['pr_auc']:.4f}", tbl_cell_center), Paragraph(f"{bm['t2d']['XGBoost']['brier_score']:.4f}", tbl_cell_center)],
        [Paragraph("T2D", tbl_cell_center), Paragraph("<b>SmartCare AI (MTL)</b>", tbl_cell_style), Paragraph(f"<b>{t2d_m['accuracy']*100:.2f}%</b>", tbl_cell_center), Paragraph(f"<b>{t2d_m['recall']*100:.2f}%</b>", tbl_cell_center), Paragraph(f"<b>{t2d_m['f1_score']:.4f}</b>", tbl_cell_center), Paragraph(f"<b>{t2d_m['roc_auc']:.4f}</b>", tbl_cell_center), Paragraph(f"<b>{t2d_m['pr_auc']:.4f}</b>", tbl_cell_center), Paragraph(f"<b>{t2d_m['brier_score']:.4f}</b>", tbl_cell_center)],
        
        [Paragraph("CVD", tbl_cell_center), Paragraph("Logistic Regression", tbl_cell_style), Paragraph(f"{bm['cvd']['Logistic Regression']['accuracy']*100:.2f}%", tbl_cell_center), Paragraph(f"{bm['cvd']['Logistic Regression']['recall']*100:.2f}%", tbl_cell_center), Paragraph(f"{bm['cvd']['Logistic Regression']['f1_score']:.4f}", tbl_cell_center), Paragraph(f"{bm['cvd']['Logistic Regression']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{bm['cvd']['Logistic Regression']['pr_auc']:.4f}", tbl_cell_center), Paragraph(f"{bm['cvd']['Logistic Regression']['brier_score']:.4f}", tbl_cell_center)],
        [Paragraph("CVD", tbl_cell_center), Paragraph("Random Forest", tbl_cell_style), Paragraph(f"{bm['cvd']['Random Forest']['accuracy']*100:.2f}%", tbl_cell_center), Paragraph(f"{bm['cvd']['Random Forest']['recall']*100:.2f}%", tbl_cell_center), Paragraph(f"{bm['cvd']['Random Forest']['f1_score']:.4f}", tbl_cell_center), Paragraph(f"{bm['cvd']['Random Forest']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{bm['cvd']['Random Forest']['pr_auc']:.4f}", tbl_cell_center), Paragraph(f"{bm['cvd']['Random Forest']['brier_score']:.4f}", tbl_cell_center)],
        [Paragraph("CVD", tbl_cell_center), Paragraph("XGBoost Classifier", tbl_cell_style), Paragraph(f"{bm['cvd']['XGBoost']['accuracy']*100:.2f}%", tbl_cell_center), Paragraph(f"{bm['cvd']['XGBoost']['recall']*100:.2f}%", tbl_cell_center), Paragraph(f"{bm['cvd']['XGBoost']['f1_score']:.4f}", tbl_cell_center), Paragraph(f"{bm['cvd']['XGBoost']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{bm['cvd']['XGBoost']['pr_auc']:.4f}", tbl_cell_center), Paragraph(f"{bm['cvd']['XGBoost']['brier_score']:.4f}", tbl_cell_center)],
        [Paragraph("CVD", tbl_cell_center), Paragraph("<b>SmartCare AI (MTL)</b>", tbl_cell_style), Paragraph(f"<b>{cvd_m['accuracy']*100:.2f}%</b>", tbl_cell_center), Paragraph(f"<b>{cvd_m['recall']*100:.2f}%</b>", tbl_cell_center), Paragraph(f"<b>{cvd_m['f1_score']:.4f}</b>", tbl_cell_center), Paragraph(f"<b>{cvd_m['roc_auc']:.4f}</b>", tbl_cell_center), Paragraph(f"<b>{cvd_m['pr_auc']:.4f}</b>", tbl_cell_center), Paragraph(f"<b>{cvd_m['brier_score']:.4f}</b>", tbl_cell_center)],
        
        [Paragraph("CKD", tbl_cell_center), Paragraph("Logistic Regression", tbl_cell_style), Paragraph(f"{bm['ckd']['Logistic Regression']['accuracy']*100:.2f}%", tbl_cell_center), Paragraph(f"{bm['ckd']['Logistic Regression']['recall']*100:.2f}%", tbl_cell_center), Paragraph(f"{bm['ckd']['Logistic Regression']['f1_score']:.4f}", tbl_cell_center), Paragraph(f"{bm['ckd']['Logistic Regression']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{bm['ckd']['Logistic Regression']['pr_auc']:.4f}", tbl_cell_center), Paragraph(f"{bm['ckd']['Logistic Regression']['brier_score']:.4f}", tbl_cell_center)],
        [Paragraph("CKD", tbl_cell_center), Paragraph("Random Forest", tbl_cell_style), Paragraph(f"{bm['ckd']['Random Forest']['accuracy']*100:.2f}%", tbl_cell_center), Paragraph(f"{bm['ckd']['Random Forest']['recall']*100:.2f}%", tbl_cell_center), Paragraph(f"{bm['ckd']['Random Forest']['f1_score']:.4f}", tbl_cell_center), Paragraph(f"{bm['ckd']['Random Forest']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{bm['ckd']['Random Forest']['pr_auc']:.4f}", tbl_cell_center), Paragraph(f"{bm['ckd']['Random Forest']['brier_score']:.4f}", tbl_cell_center)],
        [Paragraph("CKD", tbl_cell_center), Paragraph("XGBoost Classifier", tbl_cell_style), Paragraph(f"{bm['ckd']['XGBoost']['accuracy']*100:.2f}%", tbl_cell_center), Paragraph(f"{bm['ckd']['XGBoost']['recall']*100:.2f}%", tbl_cell_center), Paragraph(f"{bm['ckd']['XGBoost']['f1_score']:.4f}", tbl_cell_center), Paragraph(f"{bm['ckd']['XGBoost']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{bm['ckd']['XGBoost']['pr_auc']:.4f}", tbl_cell_center), Paragraph(f"{bm['ckd']['XGBoost']['brier_score']:.4f}", tbl_cell_center)],
        [Paragraph("CKD", tbl_cell_center), Paragraph("<b>SmartCare AI (MTL)</b>", tbl_cell_style), Paragraph(f"<b>{ckd_m['accuracy']*100:.2f}%</b>", tbl_cell_center), Paragraph(f"<b>{ckd_m['recall']*100:.2f}%</b>", tbl_cell_center), Paragraph(f"<b>{ckd_m['f1_score']:.4f}</b>", tbl_cell_center), Paragraph(f"<b>{ckd_m['roc_auc']:.4f}</b>", tbl_cell_center), Paragraph(f"<b>{ckd_m['pr_auc']:.4f}</b>", tbl_cell_center), Paragraph(f"<b>{ckd_m['brier_score']:.4f}</b>", tbl_cell_center)]
    ]
    t_base = Table(base_rows, colWidths=[35, 115, 60, 65, 65, 65, 65, 70])
    t_base.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light])
    ]))
    story.append(t_base)
    story.append(Paragraph("<b>TABLE III:</b> Baseline Model Comparison on Strictly Isolated, Identical Held-Out Test Partitions.", caption_style))

    # Ablation Study Table
    story.append(Paragraph("B. Feature Configuration Ablation Study", sec_h2))
    ab = metadata["ablation_study"]
    abl_rows = [
        [Paragraph("<b>Feature Configuration Subset</b>", tbl_hdr_style),
         Paragraph("<b>Features</b>", tbl_hdr_style),
         Paragraph("<b>T2D ROC-AUC</b>", tbl_hdr_style),
         Paragraph("<b>T2D F1</b>", tbl_hdr_style),
         Paragraph("<b>CVD ROC-AUC</b>", tbl_hdr_style),
         Paragraph("<b>CVD F1</b>", tbl_hdr_style),
         Paragraph("<b>CKD ROC-AUC</b>", tbl_hdr_style),
         Paragraph("<b>CKD F1</b>", tbl_hdr_style)],
        
        [Paragraph("<b>Full 30-Feature Set (Proposed)</b>", tbl_cell_style), Paragraph("30", tbl_cell_center), Paragraph(f"{ab['Full Feature Set (Proposed)']['t2d']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{ab['Full Feature Set (Proposed)']['t2d']['f1']:.4f}", tbl_cell_center), Paragraph(f"{ab['Full Feature Set (Proposed)']['cvd']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{ab['Full Feature Set (Proposed)']['cvd']['f1']:.4f}", tbl_cell_center), Paragraph(f"{ab['Full Feature Set (Proposed)']['ckd']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{ab['Full Feature Set (Proposed)']['ckd']['f1']:.4f}", tbl_cell_center)],
        [Paragraph("Demographics Only", tbl_cell_style), Paragraph("4", tbl_cell_center), Paragraph(f"{ab['Demographics Only']['t2d']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{ab['Demographics Only']['t2d']['f1']:.4f}", tbl_cell_center), Paragraph(f"{ab['Demographics Only']['cvd']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{ab['Demographics Only']['cvd']['f1']:.4f}", tbl_cell_center), Paragraph(f"{ab['Demographics Only']['ckd']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{ab['Demographics Only']['ckd']['f1']:.4f}", tbl_cell_center)],
        [Paragraph("Vital Signs Only", tbl_cell_style), Paragraph("6", tbl_cell_center), Paragraph(f"{ab['Vital Signs Only']['t2d']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{ab['Vital Signs Only']['t2d']['f1']:.4f}", tbl_cell_center), Paragraph(f"{ab['Vital Signs Only']['cvd']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{ab['Vital Signs Only']['cvd']['f1']:.4f}", tbl_cell_center), Paragraph(f"{ab['Vital Signs Only']['ckd']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{ab['Vital Signs Only']['ckd']['f1']:.4f}", tbl_cell_center)],
        [Paragraph("Laboratory Biomarkers Only", tbl_cell_style), Paragraph("10", tbl_cell_center), Paragraph(f"{ab['Laboratory Biomarkers Only']['t2d']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{ab['Laboratory Biomarkers Only']['t2d']['f1']:.4f}", tbl_cell_center), Paragraph(f"{ab['Laboratory Biomarkers Only']['cvd']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{ab['Laboratory Biomarkers Only']['cvd']['f1']:.4f}", tbl_cell_center), Paragraph(f"{ab['Laboratory Biomarkers Only']['ckd']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{ab['Laboratory Biomarkers Only']['ckd']['f1']:.4f}", tbl_cell_center)],
        [Paragraph("Lifestyle & Behavioral Only", tbl_cell_style), Paragraph("5", tbl_cell_center), Paragraph(f"{ab['Lifestyle & Behavioral Only']['t2d']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{ab['Lifestyle & Behavioral Only']['t2d']['f1']:.4f}", tbl_cell_center), Paragraph(f"{ab['Lifestyle & Behavioral Only']['cvd']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{ab['Lifestyle & Behavioral Only']['cvd']['f1']:.4f}", tbl_cell_center), Paragraph(f"{ab['Lifestyle & Behavioral Only']['ckd']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{ab['Lifestyle & Behavioral Only']['ckd']['f1']:.4f}", tbl_cell_center)],
        [Paragraph("Without Engineered Cardiometabolic", tbl_cell_style), Paragraph("24", tbl_cell_center), Paragraph(f"{ab['Without Engineered Cardiometabolic']['t2d']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{ab['Without Engineered Cardiometabolic']['t2d']['f1']:.4f}", tbl_cell_center), Paragraph(f"{ab['Without Engineered Cardiometabolic']['cvd']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{ab['Without Engineered Cardiometabolic']['cvd']['f1']:.4f}", tbl_cell_center), Paragraph(f"{ab['Without Engineered Cardiometabolic']['ckd']['roc_auc']:.4f}", tbl_cell_center), Paragraph(f"{ab['Without Engineered Cardiometabolic']['ckd']['f1']:.4f}", tbl_cell_center)],
    ]
    t_abl = Table(abl_rows, colWidths=[150, 45, 58, 52, 58, 52, 60, 65])
    t_abl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light])
    ]))
    story.append(t_abl)
    story.append(Paragraph("<b>TABLE IV:</b> Feature Ablation Study: Performance of Retrained Multi-Task Shared Representation Networks across Feature Subsets.", caption_style))

    # Figure 4 & Figure 5: Confusion Matrices & ROC Curves
    fig4_path = os.path.abspath("artifacts/paper_figures/fig4_confusion_matrices.png")
    fig5_path = os.path.abspath("artifacts/paper_figures/fig5_roc_curves.png")
    
    if os.path.exists(fig4_path):
        story.append(Spacer(1, 2))
        img = Image(fig4_path, width=500, height=155)
        story.append(img)
        story.append(Paragraph("<b>Fig. 2.</b> Empirical Confusion Matrices for T2D (N=10,604), CVD (N=10,231), and CKD (N=60) Test Cohorts.", caption_style))

    if os.path.exists(fig5_path):
        story.append(Spacer(1, 2))
        img = Image(fig5_path, width=440, height=215)
        story.append(img)
        story.append(Paragraph("<b>Fig. 3.</b> Receiver Operating Characteristic (ROC) Curves with exact AUC trajectories across MTL Disease Heads.", caption_style))

    # -------------------------------------------------------------
    # SECTION VI: EXPLAINABLE AI & GAME-THEORETIC ATTRIBUTIONS
    # -------------------------------------------------------------
    story.append(Paragraph("VI. EXPLAINABLE AI (XAI) & SHAP FEATURE ATTRIBUTION", sec_h1))
    story.append(Paragraph(
        "To ensure transparency in clinical decision support, SmartCare AI integrates game-theoretic Shapley Additive Explanations (SHAP). The Shapley value $\\phi_i(x)$ assigns an additive attribution to clinical biomarker $i$ representing its marginal contribution to the prediction:",
        body
    ))
    story.append(Paragraph(
        "$$\\phi_i(x) = \\sum_{S \\subseteq F \\setminus \\{i\\}} \\frac{|S|!(|F| - |S| - 1)!}{|F|!} \\left[ f(S \\cup \\{i\\}) - f(S) \\right]$$",
        code_style
    ))
    story.append(Paragraph(
        "Dual-level interpretability is provided: (1) <b>Global Explanations</b> reveal overarching biomarker importance across the population, aligning with clinical consensus (blood pressure, glucose, serum creatinine, BMI, and general health emerge as primary drivers); and (2) <b>Local Explanations</b> produce individualized waterfall decompositions for patient encounters, attributing risk changes relative to the baseline population expectation.",
        body
    ))

    # Figure 6: SHAP Global Feature Importance
    fig6_path = os.path.abspath("artifacts/paper_figures/fig6_shap_global_importance.png")
    if os.path.exists(fig6_path):
        story.append(Spacer(1, 2))
        img = Image(fig6_path, width=510, height=175)
        story.append(img)
        story.append(Paragraph("<b>Fig. 4.</b> Global Biomarker Importance Rankings (Mean |SHAP Value|) across T2D, CVD, and CKD Shared Model Heads.", caption_style))

    # -------------------------------------------------------------
    # SECTION VII: CLINICAL CASE STUDY & END-TO-END VALIDATION
    # -------------------------------------------------------------
    story.append(Paragraph("VII. CLINICAL CASE STUDY & END-TO-END VALIDATION", sec_h1))
    story.append(Paragraph(
        "To validate real-world decision-support capability, we evaluate an end-to-end patient encounter: a 56-year-old male patient (<b>PAT-2026-8942</b>) presenting with hypertension (142/92 mmHg), BMI of 28.4 kg/m², fasting glucose of 148 mg/dL, serum creatinine of 1.55 mg/dL, blood urea of 42 mg/dL, and active tobacco smoking history.",
        body
    ))

    # Figure 1: Patient Input Card
    fig1_path = os.path.abspath("artifacts/paper_figures/fig1_patient_input_prediction.png")
    if os.path.exists(fig1_path):
        story.append(Spacer(1, 2))
        img = Image(fig1_path, width=490, height=215)
        story.append(img)
        story.append(Paragraph("<b>Fig. 5.</b> Patient Input Profile and Multi-Task Prediction Output Card (Patient PAT-2026-8942).", caption_style))

    # Figure 7: Local SHAP Waterfall
    fig7_path = os.path.abspath("artifacts/paper_figures/fig7_shap_local_explanation.png")
    if os.path.exists(fig7_path):
        story.append(Spacer(1, 2))
        img = Image(fig7_path, width=470, height=205)
        story.append(img)
        story.append(Paragraph("<b>Fig. 6.</b> Local SHAP Waterfall Decomposition showing specific feature attributions for PAT-2026-8942.", caption_style))

    # Figure 9: Wellness Guidance Card
    fig9_path = os.path.abspath("artifacts/paper_figures/fig9_personalized_wellness_guidance.png")
    if os.path.exists(fig9_path):
        story.append(Spacer(1, 2))
        img = Image(fig9_path, width=490, height=215)
        story.append(img)
        story.append(Paragraph("<b>Fig. 7.</b> Personalized Clinical Wellness Guidance and Actionable Interventions Card.", caption_style))

    # -------------------------------------------------------------
    # SECTION VIII: FULL-STACK IMPLEMENTATION & MONGODB ARCHITECTURE
    # -------------------------------------------------------------
    story.append(Paragraph("VIII. FULL-STACK IMPLEMENTATION & MONGODB ARCHITECTURE", sec_h1))
    story.append(Paragraph(
        "SmartCare AI is deployed as a cloud-ready, enterprise-grade application featuring strict architectural separation of concerns: (1) <b>FastAPI Backend Microservice</b> providing asynchronous RESTful inference endpoints (<45 ms latency), JWT role-based access control (Admin, Doctor, Patient), and automated background risk pipelines; (2) <b>Enterprise MongoDB Database</b> with 14 isolated collections (users, patients, vitals, lab_results, predictions, explanations, recommendations, risk_alerts, audit_logs, doctor_profiles, appointments, chat_history, user_feedback, model_registry); (3) <b>React 19 Frontend Client</b> with responsive dark-mode dashboards and multi-language support (English, Spanish, Hindi, Tamil); and (4) <b>Conversational Wellness Chatbot</b> powered by Groq and Llama-3 with medical safety guardrails.",
        body
    ))

    # -------------------------------------------------------------
    # SECTION IX: ETHICAL CONSIDERATIONS & HONEST LIMITATIONS
    # -------------------------------------------------------------
    story.append(Paragraph("IX. ETHICAL CONSIDERATIONS, LIMITATIONS & FUTURE WORK", sec_h1))
    story.append(Paragraph(
        "<b>Ethical Considerations & Algorithmic Governance:</b> SmartCare AI is designed explicitly as a clinical decision-support tool, not an autonomous diagnostic agent. Disclaimers are embedded across all user interfaces, API payloads, and generated PDF reports. All patient records maintain strict HIPAA-aligned role-based access control and immutable audit logging.",
        body
    ))
    story.append(Paragraph(
        "<b>Methodological Limitations:</b> We transparently acknowledge the following scientific limitations: (1) <i>Cross-Sectional Source Datasets</i>: Models are trained on retrospective, disease-specific cohorts rather than a unified longitudinal EHR registry; (2) <i>Heterogeneous Variable Availability</i>: Not all 30 features are directly observed in every source dataset (unobserved features are estimated via training-fitted median imputation); (3) <i>Derived Proxy Approximations</i>: Variables such as eGFR proxy and MAP represent mathematical derivations rather than direct clinical measurements; (4) <i>CKD Sample Size Constraints</i>: The UCI CKD dataset contains only 400 total records (60 held-out test samples); while cross-validation and regularized multi-task sharing yield strong statistical discrimination, prospective validation in larger multi-center cohorts is essential; (5) <i>SHAP Association vs. Causality</i>: SHAP values quantify predictive association within the model feature space and must not be conflated with clinical causality.",
        body
    ))
    story.append(Paragraph(
        "<b>Future Work:</b> Planned extensions include multi-center federated learning protocols, prospective clinical validation across diverse hospital networks, and HL7 FHIR standard interoperability for direct Electronic Health Record (EHR) integration.",
        body
    ))

    # -------------------------------------------------------------
    # SECTION X: CONCLUSION
    # -------------------------------------------------------------
    story.append(Paragraph("X. CONCLUSION", sec_h1))
    story.append(Paragraph(
        "In this work, we presented <b>SmartCare AI</b>, an end-to-end comorbidity-aware multi-task machine learning framework for early chronic disease risk stratification and explainable clinical decision support. By combining a 30-dimensional shared feature schema, leak-free preprocessing, a shared neural encoder with task-masked loss, Platt sigmoid calibration, game-theoretic SHAP explainability, automated guideline-derived wellness recommendations, and an enterprise full-stack MongoDB/FastAPI deployment, SmartCare AI bridges the gap between predictive ML and safe, transparent clinical adoption.",
        body
    ))

    # -------------------------------------------------------------
    # REFERENCES
    # -------------------------------------------------------------
    story.append(Paragraph("REFERENCES", sec_h1))
    refs = [
        "[1] World Health Organization, \"Noncommunicable diseases country profiles 2024,\" WHO Press, Geneva, Tech. Rep., 2024.",
        "[2] S. M. Lundberg and S.-I. Lee, \"A unified approach to interpreting model predictions,\" in <i>Advances in Neural Information Processing Systems (NeurIPS)</i>, vol. 30, pp. 4765–4774, 2017.",
        "[3] T. Chen and C. Guestrin, \"XGBoost: A scalable tree boosting system,\" in <i>Proc. 22nd ACM SIGKDD Int. Conf. Knowledge Discovery and Data Mining</i>, pp. 785–794, 2016.",
        "[4] J. Platt, \"Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods,\" <i>Advances in Large Margin Classifiers</i>, vol. 10, no. 3, pp. 61–74, 1999.",
        "[5] G. W. Brier, \"Verification of forecasts expressed in terms of probability,\" <i>Monthly Weather Review</i>, vol. 78, no. 1, pp. 1–3, 1950.",
        "[6] American Diabetes Association, \"Standards of Medical Care in Diabetes—2025,\" <i>Diabetes Care</i>, vol. 48, no. Suppl. 1, pp. S1–S290, 2025.",
        "[7] P. K. Whelton et al., \"2018 AHA/ACC/AASPC Guideline for the Prevention, Detection, Evaluation, and Management of High Blood Pressure,\" <i>Circulation</i>, vol. 138, no. 17, pp. e484–e594, 2018.",
        "[8] Kidney Disease: Improving Global Outcomes (KDIGO) CKD Work Group, \"KDIGO 2024 Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease,\" <i>Kidney International</i>, vol. 105, no. 4S, pp. S117–S314, 2024.",
        "[9] Centers for Disease Control and Prevention (CDC), \"Behavioral Risk Factor Surveillance System (BRFSS) Survey Data,\" U.S. Dept. of Health and Human Services, 2015.",
        "[10] A. S. Levey et al., \"A new equation to estimate glomerular filtration rate,\" <i>Annals of Internal Medicine</i>, vol. 150, no. 9, pp. 604–612, 2009."
    ]
    for r in refs:
        story.append(Paragraph(r, ParagraphStyle('RefStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=9.5, textColor=c_dark, spaceAfter=2)))

    # Build the PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] IEEE Conference Paper PDF generated successfully at: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    build_pdf()
