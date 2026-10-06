import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and display total page count and professional headers/footers.
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
        self.setFillColor(colors.HexColor("#0284c7")) # Accent blue
        
        # Header (Top) - show on page 2+
        if self._pageNumber > 1:
            header_left = "SMARTCARE AI — COMPLETE PROJECT BLUEPRINT & TECHNICAL SPECIFICATION (A TO Z)"
            self.drawString(36, 756, header_left)
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.75)
            self.line(36, 750, 576, 750)
        
        # Footer (Bottom)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        footer_text = "SmartCare AI Healthcare Platform • Confidential & Proprietary System Architecture"
        self.drawString(36, 30, footer_text)
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 30, page_str)
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.75)
        self.line(36, 40, 576, 40)
        
        self.restoreState()

def build_pdf(filename="SmartCare_AI_Complete_Project_Documentation.pdf"):
    pdf_path = os.path.abspath(filename)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()
    
    # Palette
    c_primary = colors.HexColor("#0f172a")   # Slate 900
    c_secondary = colors.HexColor("#0369a1") # Sky 700
    c_accent = colors.HexColor("#0284c7")    # Sky 600
    c_dark = colors.HexColor("#1e293b")      # Slate 800
    c_gray = colors.HexColor("#475569")      # Slate 600
    c_light = colors.HexColor("#f8fafc")     # Slate 50
    c_border = colors.HexColor("#cbd5e1")    # Slate 300
    c_card = colors.HexColor("#f1f5f9")      # Slate 100
    c_highlight = colors.HexColor("#0284c7")

    # Typography Styles
    title_main = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        alignment=0,
        textColor=c_primary,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        alignment=0,
        textColor=c_secondary,
        spaceAfter=8
    )

    meta_style = ParagraphStyle(
        'MetaLine',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_gray,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.white,
        spaceBefore=0,
        spaceAfter=0
    )

    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'Heading3',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=c_dark,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    body = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        alignment=4, # Justified
        textColor=c_dark,
        spaceAfter=5
    )

    bullet = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_dark,
        leftIndent=12,
        spaceAfter=3
    )

    caption = ParagraphStyle(
        'CaptionCustom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        alignment=1,
        textColor=c_gray,
        spaceBefore=4,
        spaceAfter=8
    )

    code_inline = ParagraphStyle(
        'CodeInline',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#0f172a")
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        alignment=1,
        textColor=colors.white
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=c_dark
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=c_dark
    )

    def section_header(title_text):
        t = Table(
            [[Paragraph(f"<b>{title_text}</b>", h1_style)]],
            colWidths=[540],
            rowHeights=[22]
        )
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_primary),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 2),
        ]))
        return t

    story = []

    # =========================================================================
    # DOCUMENT COVER / HEADER
    # =========================================================================
    story.append(Paragraph("SMARTCARE AI — COMPREHENSIVE MASTER PROJECT BLUEPRINT", title_main))
    story.append(Paragraph("An Explainable, Comorbidity-Aware Multi-Task Machine Learning Platform for Chronic Disease Risk Stratification, Longitudinal Risk Monitoring & Clinical Decision Support (A to Z Technical Architecture)", subtitle_style))
    story.append(Paragraph("<b>Author / Engineering Team:</b> SmartCare AI Core Development Team &bull; <b>System Version:</b> 6.2.0 (Production / Release) &bull; <b>Database:</b> MongoDB Atlas / Enterprise NoSQL &bull; <b>Backend:</b> FastAPI &bull; <b>Frontend:</b> React 19 + Vite", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=0, spaceAfter=8))

    # Executive Summary Card
    exec_text = (
        "<b>EXECUTIVE BLUEPRINT SUMMARY:</b><br/>"
        "SmartCare AI is an enterprise-grade, end-to-end intelligent healthcare platform engineered to address the global crisis of chronic disease comorbidity. "
        "Focusing on the <b>Cardio-Renal-Metabolic (CRM) Triad</b>—specifically <b>Type 2 Diabetes (T2D)</b>, <b>Cardiovascular Disease (CVD)</b>, and <b>Chronic Kidney Disease (CKD)</b>—the platform replaces fragmented, uninterpretable single-disease tools with a unified comorbidity-aware multi-task predictive architecture. "
        "SmartCare AI integrates multimodal clinical datasets ($N=139,297$ records), advanced machine learning (XGBoost, Random Forest) with Platt probability calibration, game-theoretic explainability (TreeSHAP), automated evidence-based wellness guidelines, continuous longitudinal risk alerts, role-based portals for Patients, Doctors, and Admins, and an interactive LLM-driven medical wellness assistant."
    )
    exec_table = Table([[Paragraph(exec_text, body)]], colWidths=[540])
    exec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card),
        ('BOX', (0,0), (-1,-1), 1, c_accent),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(exec_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # CHAPTER 1: COMPLETE SYSTEM ARCHITECTURE & TECH STACK
    # =========================================================================
    story.append(section_header("CHAPTER 1: FULL-STACK SYSTEM ARCHITECTURE & TECH STACK"))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "SmartCare AI is architected as a high-performance, asynchronous, decoupled microservice ecosystem designed for clinical scalability, zero-latency inference (&lt;45 ms), and strict data compliance.",
        body
    ))
    
    # Tech Stack Table
    tech_data = [
        [Paragraph("Layer", table_header), Paragraph("Technology / Framework", table_header), Paragraph("Key Purpose & Capabilities", table_header)],
        [Paragraph("<b>Frontend UI/UX</b>", table_cell_bold), Paragraph("React 19, Vite, Vanilla Glassmorphism CSS, Tailwind CSS", table_cell), Paragraph("Responsive glassmorphic UI, real-time risk gauges, role-based views (Patient/Doctor/Admin), accessible color palettes, dark mode.", table_cell)],
        [Paragraph("<b>Visualizations</b>", table_cell_bold), Paragraph("Recharts, Lucide React, HTML5 Canvas", table_cell), Paragraph("Interactive risk trend charts, SHAP feature waterfalls, vital velocity telemetry, biomarker comparison graphs.", table_cell)],
        [Paragraph("<b>Localization (i18n)</b>", table_cell_bold), Paragraph("React Context i18n Engine", table_cell), Paragraph("Dynamic multilingual translation across 4 languages: English, Spanish (Español), Hindi (हिंदी), and Tamil (தமிழ்).", table_cell)],
        [Paragraph("<b>Backend API</b>", table_cell_bold), Paragraph("FastAPI (Python 3.11), Uvicorn, Pydantic v2", table_cell), Paragraph("Asynchronous REST microservice, high throughput, automatic OpenAPI/Swagger docs, schema validation, CORS security.", table_cell)],
        [Paragraph("<b>Database</b>", table_cell_bold), Paragraph("MongoDB Atlas / Community (NoSQL)", table_cell), Paragraph("14 primary collections, compound/unique indexes, in-memory high-performance fallback store, JSON document agility.", table_cell)],
        [Paragraph("<b>Machine Learning</b>", table_cell_bold), Paragraph("Scikit-Learn, XGBoost, SHAP, Joblib", table_cell), Paragraph("Gradient boosted trees, Random Forests, Platt sigmoid probability calibration, 5-fold cross-validation, TreeExplainer.", table_cell)],
        [Paragraph("<b>AI Wellness Chat</b>", table_cell_bold), Paragraph("Groq API / Llama-3-8b-8192 LLM", table_cell), Paragraph("Context-bounded medical conversational agent, safety guardrails, personalized lifestyle coaching, emergency escalation.", table_cell)],
        [Paragraph("<b>Security & Auth</b>", table_cell_bold), Paragraph("JWT (JSON Web Tokens), Bcrypt, RBAC", table_cell), Paragraph("Stateless HMAC-SHA256 tokens, password salting, 4-tier Role-Based Access Control (Admin, Doctor, Patient, Staff).", table_cell)],
    ]
    t_tech = Table(tech_data, colWidths=[95, 155, 290])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light])
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 8))

    # Figure 8: End-to-End Pipeline
    fig8_path = os.path.abspath("artifacts/paper_figures/fig8_explainable_prediction_pipeline.png")
    if os.path.exists(fig8_path):
        img = Image(fig8_path, width=520, height=210)
        story.append(img)
        story.append(Paragraph("<b>Figure 1.1:</b> SmartCare AI End-to-End Prediction, Explainability, and Clinical Guidance Pipeline.", caption))

    # =========================================================================
    # CHAPTER 2: THE 6 CORE SYSTEM MODULES (IN-DEPTH)
    # =========================================================================
    story.append(section_header("CHAPTER 2: DETAILED SPECIFICATIONS OF THE 6 CORE MODULES"))
    story.append(Spacer(1, 6))

    # Module 1
    story.append(Paragraph("Module 1: Multimodal Clinical Data Acquisition & Preprocessing Engine", h2_style))
    story.append(Paragraph(
        "Module 1 ingests, sanitizes, and standardizes multi-source health records while eliminating data leakage:",
        body
    ))
    story.append(Paragraph("&bull; <b>CDC BRFSS 2015 Diabetes Cohort (N = 70,692):</b> 21 demographic, health status, and lifestyle indicators (HighBP, HighChol, BMI, Smoker, Stroke, HeartDisease, PhysActivity, GenHlth, MentHlth, PhysHlth, DiffWalk, Age, Education, Income).", bullet))
    story.append(Paragraph("&bull; <b>Cardiovascular Disease Cohort (N = 68,205):</b> Real patient records capturing Age, Sex, Height, Weight, Systolic BP (<code>ap_hi</code>), Diastolic BP (<code>ap_lo</code>), Cholesterol, Glucose, Smoking, Alcohol, and Physical Activity.", bullet))
    story.append(Paragraph("&bull; <b>UCI Chronic Kidney Disease Cohort (N = 400):</b> 24 clinical, urinalysis, and biochemical parameters (Blood Pressure, Specific Gravity, Albumin, Sugar, Blood Urea, Serum Creatinine, Sodium, Potassium, Hemoglobin, WBC count, RBC count, Hypertension, Diabetes).", bullet))
    story.append(Paragraph("&bull; <b>Preprocessing Pipeline:</b> Missing value imputation using K-Nearest Neighbors ($k=5$); biological outlier clipping via Tukey's IQR rule; scaling using <code>RobustScaler</code> (median and IQR); leak-free 70/15/15 train/val/test temporal splitting.", bullet))
    story.append(Paragraph("&bull; <b>Biochemical Feature Engineering:</b><br/>"
                           "1) <i>Mean Arterial Pressure:</i> $\\text{MAP} = \\frac{2 \\times \\text{ap\\_lo} + \\text{ap\\_hi}}{3}$ (systemic vascular resistance)<br/>"
                           "2) <i>Pulse Pressure:</i> $\\text{PP} = \\text{ap\\_hi} - \\text{ap\\_lo}$ (arterial stiffness indicator)<br/>"
                           "3) <i>eGFR Proxy Index:</i> Estimated filtration rate derived from serum creatinine ($S_{cr}$), age, and sex.", bullet))

    # Module 2
    story.append(Spacer(1, 4))
    story.append(Paragraph("Module 2: Comorbidity-Aware Multi-Task Risk Prediction Engine", h2_style))
    story.append(Paragraph(
        "Module 2 trains, evaluates, calibrates, and benchmarks machine learning classifiers for each chronic target:",
        body
    ))
    story.append(Paragraph("&bull; <b>Benchmarked Model Families:</b> L2-Regularized Logistic Regression (linear baseline), Random Forest (100 bagged decision trees), and Extreme Gradient Boosting (XGBoost with tree pruning and histogram binning).", bullet))
    story.append(Paragraph("&bull; <b>5-Fold Stratified Cross-Validation:</b> Systematic grid search optimizing ROC-AUC, Precision, and Recall across hyperparameter spaces.", bullet))
    story.append(Paragraph("&bull; <b>Platt Sigmoid Probability Calibration:</b> Converts uncalibrated margins $f(x)$ into true posterior event probabilities $\\hat{P}(y=1|x) = [1 + \\exp(A f(x) + B)]^{-1}$, drastically reducing Brier error scores.", bullet))
    story.append(Paragraph("&bull; <b>Clinical Sensitivity-Targeted Decision Thresholds ($T^*$):</b> Rather than arbitrary 0.50 cutoffs, thresholds are optimized on validation sets to guarantee $\\text{Recall} \\ge 70\\%$, yielding $T^*=0.40$ (T2D), $T^*=0.35$ (CVD), and $T^*=0.35$ (CKD).", bullet))

    # Module 3
    story.append(Spacer(1, 4))
    story.append(Paragraph("Module 3: Explainable AI (XAI) & Game-Theoretic SHAP Attributions", h2_style))
    story.append(Paragraph(
        "Module 3 unlocks model transparency using cooperative game theory via TreeSHAP:",
        body
    ))
    story.append(Paragraph("&bull; <b>Mathematical Formulation:</b> Computes exact Shapley values $\\phi_i(x) = \\sum_{S \\subseteq F \\setminus \\{i\\}} \\frac{|S|!(|F| - |S| - 1)!}{|F|!} [f(S \\cup \\{i\\}) - f(S)]$.", bullet))
    story.append(Paragraph("&bull; <b>Global Biomarker Rankings:</b> Mean $|\\text{SHAP}|$ across populations reveals population-level risk hierarchy (Systolic BP, Blood Glucose, BMI, Serum Creatinine, Hemoglobin).", bullet))
    story.append(Paragraph("&bull; <b>Local Waterfall Decompositions:</b> Patient-specific attributions show exact additive risk push (+ red / - green) relative to the population baseline.", bullet))

    # Module 4
    story.append(Spacer(1, 4))
    story.append(Paragraph("Module 4: Evidence-Based Personalized Wellness & Clinical Interventions", h2_style))
    story.append(Paragraph(
        "Module 4 dynamically maps SHAP attributions and predicted risk categories into clinical guidelines:",
        body
    ))
    story.append(Paragraph("&bull; <b>Dietary Guidelines:</b> Strict sodium restriction (&lt;2,000 mg/day for elevated BP/MAP), low glycemic index diet (for elevated glucose), DASH / Mediterranean dietary protocols.", bullet))
    story.append(Paragraph("&bull; <b>Physical Activity:</b> 150 minutes/week moderate aerobic exercise for elevated BMI/sedentary status upon clinical clearance.", bullet))
    story.append(Paragraph("&bull; <b>Targeted Specialist Referrals:</b> Automatic triggers for Nephrology consultations (if CKD risk &gt;60% or creatinine &gt;1.4 mg/dL), Cardiology consultations (if CVD risk &gt;60%), and Endocrinology referrals.", bullet))

    # Module 5
    story.append(Spacer(1, 4))
    story.append(Paragraph("Module 5: Continuous Longitudinal Risk Monitoring & Clinical Decision Support", h2_style))
    story.append(Paragraph(
        "Module 5 monitors patient vital sign trajectories over time to detect acute deterioration:",
        body
    ))
    story.append(Paragraph("&bull; <b>Vital Velocity & Slope Tracking:</b> Calculates rate of biomarker change ($\\Delta \\text{BP}/\\Delta t$, $\\Delta S_{cr}/\\Delta t$).", bullet))
    story.append(Paragraph("&bull; <b>Multi-Tier Alert Engine:</b> Green (Low Risk &lt;30%), Amber/Yellow (Moderate Risk 30-60%), Red (Critical High Risk &gt;60% or rapid slope increase).", bullet))
    story.append(Paragraph("&bull; <b>Automated Clinical Escalation:</b> Dispatches instant dashboard notifications and alerts to attending physicians.", bullet))

    # Module 6
    story.append(Spacer(1, 4))
    story.append(Paragraph("Module 6: Multi-Role Dashboard & AI Wellness Chatbot", h2_style))
    story.append(Paragraph(
        "Module 6 delivers specialized web portals for Patients, Clinicians, and Administrators, backed by an LLM wellness chatbot powered by Groq/Llama-3 with medical safety guardrails.",
        body
    ))

    # =========================================================================
    # CHAPTER 3: EMPIRICAL BENCHMARK RESULTS & FIGURES
    # =========================================================================
    story.append(Spacer(1, 6))
    story.append(section_header("CHAPTER 3: QUANTITATIVE MODEL EVALUATION & EXPERIMENTAL BENCHMARKS"))
    story.append(Spacer(1, 6))

    # Table of Results
    res_data = [
        [Paragraph("Target Chronic Disease", table_header), Paragraph("Champion Model", table_header), Paragraph("Decision Threshold ($T^*$)", table_header), Paragraph("Accuracy", table_header), Paragraph("Precision", table_header), Paragraph("Recall (Sens.)", table_header), Paragraph("F1-Score", table_header), Paragraph("ROC-AUC", table_header), Paragraph("PR-AUC", table_header), Paragraph("Brier Score", table_header)],
        [Paragraph("<b>Type 2 Diabetes (T2D)</b>", table_cell_bold), Paragraph("XGBoost Classifier", table_cell), Paragraph("0.40", table_cell), Paragraph("74.41%", table_cell), Paragraph("70.19%", table_cell), Paragraph("<b>84.85%</b>", table_cell_bold), Paragraph("0.7683", table_cell), Paragraph("<b>0.8233</b>", table_cell_bold), Paragraph("0.8142", table_cell), Paragraph("0.1702", table_cell)],
        [Paragraph("<b>Cardiovascular (CVD)</b>", table_cell_bold), Paragraph("XGBoost Classifier", table_cell), Paragraph("0.35", table_cell), Paragraph("70.10%", table_cell), Paragraph("66.20%", table_cell), Paragraph("<b>80.60%</b>", table_cell_bold), Paragraph("0.7269", table_cell), Paragraph("<b>0.7876</b>", table_cell_bold), Paragraph("0.7715", table_cell), Paragraph("0.1945", table_cell)],
        [Paragraph("<b>Chronic Kidney (CKD)</b>", table_cell_bold), Paragraph("Random Forest", table_cell), Paragraph("0.35", table_cell), Paragraph("96.67%", table_cell), Paragraph("94.87%", table_cell), Paragraph("<b>100.00%</b>", table_cell_bold), Paragraph("0.9737", table_cell), Paragraph("<b>0.9953</b>", table_cell_bold), Paragraph("0.9968", table_cell), Paragraph("0.0271", table_cell)],
    ]
    t_res = Table(res_data, colWidths=[90, 75, 45, 45, 45, 55, 45, 45, 45, 50])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (2,1), (-1,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light])
    ]))
    story.append(t_res)
    story.append(Paragraph("<b>Table 3.1:</b> Empirical Test-Set Performance Evaluation across Independent Calibrated Models.", caption))
    story.append(Spacer(1, 6))

    # Figure 3: Performance Bar Chart
    fig3_path = os.path.abspath("artifacts/paper_figures/fig3_model_performance_comparison.png")
    if os.path.exists(fig3_path):
        img = Image(fig3_path, width=490, height=215)
        story.append(img)
        story.append(Paragraph("<b>Figure 3.1:</b> Empirical Test-Set Performance Metric Comparison across T2D, CVD, and CKD Models.", caption))

    # Figure 4 & Figure 5: Confusion Matrices & ROC
    fig4_path = os.path.abspath("artifacts/paper_figures/fig4_confusion_matrices.png")
    if os.path.exists(fig4_path):
        story.append(Spacer(1, 4))
        img = Image(fig4_path, width=500, height=160)
        story.append(img)
        story.append(Paragraph("<b>Figure 3.2:</b> Confusion Matrices for T2D (N=10,604), CVD (N=10,231), and CKD (N=60) Test Sets.", caption))

    fig5_path = os.path.abspath("artifacts/paper_figures/fig5_roc_curves.png")
    if os.path.exists(fig5_path):
        story.append(Spacer(1, 4))
        img = Image(fig5_path, width=440, height=220)
        story.append(img)
        story.append(Paragraph("<b>Figure 3.3:</b> Receiver Operating Characteristic (ROC) Trajectories and exact AUC values.", caption))

    # Figure 6: Global SHAP
    fig6_path = os.path.abspath("artifacts/paper_figures/fig6_shap_global_importance.png")
    if os.path.exists(fig6_path):
        story.append(Spacer(1, 4))
        img = Image(fig6_path, width=510, height=185)
        story.append(img)
        story.append(Paragraph("<b>Figure 3.4:</b> Global SHAP Feature Importance Rankings across Disease Models.", caption))

    # =========================================================================
    # CHAPTER 4: MONGODB DATABASE ARCHITECTURE (14 COLLECTIONS)
    # =========================================================================
    story.append(Spacer(1, 6))
    story.append(section_header("CHAPTER 4: MONGODB DATABASE ARCHITECTURE & 14 COLLECTIONS"))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "The SmartCare AI database (<code>smartcare_ai</code>) is structured across 14 collections with unique/compound indexing to ensure sub-millisecond retrieval and complete HIPAA-compliant data separation:",
        body
    ))

    db_collections = [
        [Paragraph("Collection Name", table_header), Paragraph("Primary / Unique Indexes", table_header), Paragraph("Schema Description & Stored Attributes", table_header)],
        [Paragraph("<code>users</code>", table_cell_bold), Paragraph("<code>email (unique)</code>, <code>user_id (unique)</code>, <code>role</code>", table_cell), Paragraph("User credentials, salted bcrypt hashed passwords, roles (patient, doctor, admin, staff), account status, timestamps.", table_cell)],
        [Paragraph("<code>patients</code>", table_cell_bold), Paragraph("<code>patient_id (unique)</code>, <code>user_id</code>", table_cell), Paragraph("Patient demographics: age, sex, height, weight, BMI, emergency contacts, attending physician assignments.", table_cell)],
        [Paragraph("<code>doctors</code>", table_cell_bold), Paragraph("<code>doctor_id (unique)</code>, <code>user_id</code>", table_cell), Paragraph("Clinician profiles, medical license numbers, specialties (Cardiology, Nephrology, Endocrine), assigned patient arrays.", table_cell)],
        [Paragraph("<code>admins</code>", table_cell_bold), Paragraph("<code>admin_id (unique)</code>, <code>user_id</code>", table_cell), Paragraph("System administrator metadata, access clearance levels, permission configurations.", table_cell)],
        [Paragraph("<code>health_records</code>", table_cell_bold), Paragraph("<code>patient_id</code>, <code>record_date</code>", table_cell), Paragraph("Aggregated clinical snapshots combining vitals, physical activity, smoking, alcohol, and symptom checklists.", table_cell)],
        [Paragraph("<code>vitals</code>", table_cell_bold), Paragraph("<code>patient_id</code>, <code>recorded_at</code>", table_cell), Paragraph("Longitudinal physiological telemetry: Systolic BP, Diastolic BP, MAP, Pulse Pressure, Heart Rate, Respiratory Rate.", table_cell)],
        [Paragraph("<code>lab_results</code>", table_cell_bold), Paragraph("<code>patient_id</code>, <code>test_date</code>", table_cell), Paragraph("Biochemical test panels: Fasting Blood Glucose, HbA1c, Serum Creatinine, Blood Urea, Hemoglobin, Albumin, eGFR proxy.", table_cell)],
        [Paragraph("<code>predictions</code>", table_cell_bold), Paragraph("<code>prediction_id (unique)</code>, <code>patient_id</code>", table_cell), Paragraph("Multi-disease output records: T2D risk, CVD risk, CKD risk, probabilities, risk tiers (Low/Mod/High), model version.", table_cell)],
        [Paragraph("<code>explanations</code>", table_cell_bold), Paragraph("<code>prediction_id</code>, <code>patient_id</code>", table_cell), Paragraph("TreeSHAP attributions: base value, per-feature Shapley values, top positive/negative risk contributors.", table_cell)],
        [Paragraph("<code>recommendations</code>", table_cell_bold), Paragraph("<code>prediction_id</code>, <code>patient_id</code>", table_cell), Paragraph("Actionable clinical guidance: dietary rules, exercise limits, lifestyle guidance, specialist referral flags.", table_cell)],
        [Paragraph("<code>risk_alerts</code>", table_cell_bold), Paragraph("<code>patient_id</code>, <code>severity</code>, <code>status</code>", table_cell), Paragraph("Longitudinal clinical alerts: alert level (Normal/Warning/Critical), trigger biomarker, acknowledged status, clinician notes.", table_cell)],
        [Paragraph("<code>audit_logs</code>", table_cell_bold), Paragraph("<code>user_id</code>, <code>timestamp</code>, <code>action</code>", table_cell), Paragraph("Immutable security logs: timestamp, user ID, IP address, endpoint accessed, action performed, status code.", table_cell)],
        [Paragraph("<code>appointments</code>", table_cell_bold), Paragraph("<code>patient_id</code>, <code>doctor_id</code>, <code>date</code>", table_cell), Paragraph("Consultation scheduling: appointment time, clinical reason, status (scheduled, completed, cancelled), consult notes.", table_cell)],
        [Paragraph("<code>chat_history</code>", table_cell_bold), Paragraph("<code>user_id</code>, <code>timestamp</code>", table_cell), Paragraph("LLM conversational logs: user query, assistant response, medical intent tags, escalation flags.", table_cell)],
    ]
    t_db = Table(db_collections, colWidths=[90, 150, 300])
    t_db.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light])
    ]))
    story.append(t_db)
    story.append(Spacer(1, 8))

    # =========================================================================
    # CHAPTER 5: COMPLETE REST API ENDPOINTS CATALOG
    # =========================================================================
    story.append(section_header("CHAPTER 5: COMPLETE REST API ENDPOINTS SPECIFICATION"))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "The FastAPI backend exposes fully documented asynchronous endpoints under the <code>/api/v1</code> prefix with JWT authentication and RBAC authorization:",
        body
    ))

    api_routes = [
        [Paragraph("HTTP Method & Route Path", table_header), Paragraph("Auth Role", table_header), Paragraph("Request / Response Functionality", table_header)],
        [Paragraph("<code>POST /api/v1/auth/login</code>", table_cell_bold), Paragraph("Public", table_cell), Paragraph("Authenticates credentials, returns JWT bearer token, user role, and session expiration.", table_cell)],
        [Paragraph("<code>POST /api/v1/auth/register</code>", table_cell_bold), Paragraph("Public", table_cell), Paragraph("Registers new patient or clinician account with encrypted password hashing.", table_cell)],
        [Paragraph("<code>GET /api/v1/patients/me</code>", table_cell_bold), Paragraph("Patient", table_cell), Paragraph("Retrieves logged-in patient profile, assigned doctor, and medical history.", table_cell)],
        [Paragraph("<code>POST /api/v1/health-data/submit</code>", table_cell_bold), Paragraph("Patient / Doctor", table_cell), Paragraph("Ingests vitals and lab biomarkers, triggering automated risk pipeline evaluation.", table_cell)],
        [Paragraph("<code>POST /api/v1/predictions/predict</code>", table_cell_bold), Paragraph("Any Auth", table_cell), Paragraph("Executes comorbidity-aware multi-task inference, returning calibrated probabilities for T2D, CVD, and CKD.", table_cell)],
        [Paragraph("<code>GET /api/v1/explanations/{pred_id}</code>", table_cell_bold), Paragraph("Any Auth", table_cell), Paragraph("Fetches TreeSHAP global and local waterfall feature attributions for a given prediction.", table_cell)],
        [Paragraph("<code>GET /api/v1/recommendations/{pred_id}</code>", table_cell_bold), Paragraph("Any Auth", table_cell), Paragraph("Generates personalized evidence-based clinical wellness guidance, dietary rules, and specialist referrals.", table_cell)],
        [Paragraph("<code>GET /api/v1/risk-monitoring/alerts</code>", table_cell_bold), Paragraph("Doctor / Admin", table_cell), Paragraph("Retrieves queue of active clinical alerts across patient cohort with vital trajectory velocity.", table_cell)],
        [Paragraph("<code>POST /api/v1/chat/message</code>", table_cell_bold), Paragraph("Any Auth", table_cell), Paragraph("Interacts with the Groq/Llama-3 medical wellness conversational assistant with safety guardrails.", table_cell)],
        [Paragraph("<code>GET /api/v1/admin/models</code>", table_cell_bold), Paragraph("Admin", table_cell), Paragraph("Lists registered champion and candidate model versions, hyperparameters, and CV metrics.", table_cell)],
        [Paragraph("<code>GET /api/v1/reports/pdf/{patient_id}</code>", table_cell_bold), Paragraph("Doctor / Patient", table_cell), Paragraph("Generates and downloads a comprehensive patient clinical summary report in PDF format.", table_cell)],
    ]
    t_api = Table(api_routes, colWidths=[160, 80, 300])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light])
    ]))
    story.append(t_api)
    story.append(Spacer(1, 8))

    # =========================================================================
    # CHAPTER 6: END-TO-END CLINICAL CASE STUDY (PAT-2026-8942)
    # =========================================================================
    story.append(section_header("CHAPTER 6: END-TO-END CLINICAL CASE STUDY (PAT-2026-8942)"))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "To validate the real-world utility of SmartCare AI, we examine the complete diagnostic encounter for Patient <b>PAT-2026-8942</b>:",
        body
    ))
    story.append(Paragraph("&bull; <b>Patient Demographics:</b> 56-year-old Male, Height: 172 cm, Weight: 84 kg (BMI: 28.4 kg/m² — Overweight).", bullet))
    story.append(Paragraph("&bull; <b>Vitals & Clinical Labs:</b> Systolic BP: 142 mmHg, Diastolic BP: 92 mmHg (Hypertension Stage 2), Fasting Glucose: 148 mg/dL, Serum Creatinine: 1.55 mg/dL (Elevated), Blood Urea: 42 mg/dL, Hemoglobin: 12.8 g/dL, Smoker: Yes, Physical Activity: Sedentary.", bullet))
    story.append(Paragraph("&bull; <b>Multi-Disease AI Prediction Output:</b><br/>"
                           "1) <i>Type 2 Diabetes (T2D):</i> <b>52.8% Risk (MODERATE)</b> — XGBoost (Threshold: 0.40)<br/>"
                           "2) <i>Cardiovascular Disease (CVD):</i> <b>82.7% Risk (HIGH)</b> — XGBoost (Threshold: 0.35)<br/>"
                           "3) <i>Chronic Kidney Disease (CKD):</i> <b>95.4% Risk (HIGH)</b> — Random Forest (Threshold: 0.35)", bullet))

    # Figure 1: Patient Input Card
    fig1_path = os.path.abspath("artifacts/paper_figures/fig1_patient_input_prediction.png")
    if os.path.exists(fig1_path):
        story.append(Spacer(1, 4))
        img = Image(fig1_path, width=490, height=225)
        story.append(img)
        story.append(Paragraph("<b>Figure 6.1:</b> Patient Clinical Prediction Profile Card for Patient PAT-2026-8942.", caption))

    # Figure 2: Risk Bar Chart
    fig2_path = os.path.abspath("artifacts/paper_figures/fig2_risk_score_visualization.png")
    if os.path.exists(fig2_path):
        story.append(Spacer(1, 4))
        img = Image(fig2_path, width=450, height=190)
        story.append(img)
        story.append(Paragraph("<b>Figure 6.2:</b> Multi-Disease Risk Score Visualization across Risk Zones.", caption))

    # Figure 7: Local SHAP Waterfall
    fig7_path = os.path.abspath("artifacts/paper_figures/fig7_shap_local_explanation.png")
    if os.path.exists(fig7_path):
        story.append(Spacer(1, 4))
        img = Image(fig7_path, width=470, height=215)
        story.append(img)
        story.append(Paragraph("<b>Figure 6.3:</b> Local SHAP Waterfall Decomposition for Patient PAT-2026-8942.", caption))

    # Figure 9: Wellness Guidance Card
    fig9_path = os.path.abspath("artifacts/paper_figures/fig9_personalized_wellness_guidance.png")
    if os.path.exists(fig9_path):
        story.append(Spacer(1, 4))
        img = Image(fig9_path, width=490, height=225)
        story.append(img)
        story.append(Paragraph("<b>Figure 6.4:</b> Actionable Clinical Wellness & Intervention Plan for PAT-2026-8942.", caption))

    # =========================================================================
    # CHAPTER 7: SECURITY, COMPLIANCE & INSTALLATION GUIDE
    # =========================================================================
    story.append(Spacer(1, 6))
    story.append(section_header("CHAPTER 7: SECURITY, COMPLIANCE & SYSTEM DEPLOYMENT"))
    story.append(Spacer(1, 6))
    story.append(Paragraph("A. Security, RBAC & Compliance Architecture", h2_style))
    story.append(Paragraph(
        "SmartCare AI implements defense-in-depth security principles: passwords salted and hashed via <code>bcrypt</code>; stateless JWT authentication with strict token expiration; granular role-based access control protecting clinical routes; and immutable audit logging storing client IP addresses, timestamps, and accessed resources.",
        body
    ))

    story.append(Paragraph("B. Setup & Execution Instructions (Quickstart)", h2_style))
    story.append(Paragraph("1) <b>Prerequisites:</b> Python 3.11+, Node.js 18+, MongoDB Community / Atlas instance.", bullet))
    story.append(Paragraph("2) <b>Backend Setup:</b><br/>"
                           "<code>cd backend</code><br/>"
                           "<code>pip install -r requirements.txt</code><br/>"
                           "<code>uvicorn app.main:app --reload --port 8000</code>", bullet))
    story.append(Paragraph("3) <b>Frontend Setup:</b><br/>"
                           "<code>cd frontend</code><br/>"
                           "<code>npm install</code><br/>"
                           "<code>npm run dev</code> (Launches on <code>http://localhost:5173</code>)", bullet))
    story.append(Paragraph("4) <b>Model Training & Artifact Generation:</b><br/>"
                           "<code>python train_models.py --mode all</code> (Trains models and updates MongoDB registry)<br/>"
                           "<code>python generate_paper_artifacts.py</code> (Generates all 300 DPI high-res charts)", bullet))

    # Build the complete PDF document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Complete Project Blueprint PDF generated at: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    build_pdf()
