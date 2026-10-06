"""
SmartCare AI - Report Generator: Chapters 1, 2, and 3
Configured with actual figure image integration and user references [1] to [20].
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from report_builder_core import (
    set_cell_background, set_cell_margins, set_table_borders,
    add_callout_box, add_figure_with_image, add_styled_paragraph, add_heading_1,
    add_heading_2, add_heading_3, add_bullet_item
)

PROJECT_TITLE = "SmartCare AI: Comorbidity-Aware Explainable Multi-Task Learning for Integrated Diabetes, Cardiovascular, and Chronic Kidney Disease Risk Prediction"
FIG_DIR = os.path.abspath("artifacts/report_figures")

def build_chapter_1(doc):
    """Generates Chapter 1: Introduction."""
    add_heading_1(doc, "CHAPTER 1\nINTRODUCTION")
    
    add_heading_2(doc, "1.1 MOTIVATION")
    add_styled_paragraph(
        doc,
        "Healthcare remains one of the most critical sectors affecting human well-being and socio-economic stability worldwide. Despite rapid advancements in clinical diagnostics and pharmacology, the global healthcare ecosystem faces unprecedented challenges due to the escalating burden of chronic non-communicable diseases (NCDs), prolonged asymptomatic disease latency, fragmented diagnostic services, and a lack of timely, personalized, data-driven clinical support. Most existing diagnostic portals and computerized risk assessment tools still provide generalized, single-disease recommendations that fail to consider the intricate pathophysiological interdependencies among co-occurring chronic conditions. As a result, healthcare practitioners and patients often make uncoordinated therapeutic decisions, leading to late-stage diagnoses, accelerated comorbidity progression, higher mortality rates, and unsustainable healthcare costs."
    )
    
    add_styled_paragraph(
        doc,
        f"The motivation behind this project — {PROJECT_TITLE} — stems from the critical need to bridge this clinical and technological gap. By integrating Artificial Intelligence (AI), Multi-Task Deep Learning (MTL), Explainable AI (XAI), and Clinical Knowledge Engineering, the project aims to provide localized, highly accurate, and comorbidity-aware risk stratifications at the individual patient and primary care levels. Through the use of a unified Shared Feature Neural Encoder, the system simultaneously models the complex cardiorenal-metabolic cross-talk connecting Type 2 Diabetes Mellitus (T2D), Cardiovascular Disease (CVD), and Chronic Kidney Disease (CKD). This multi-task innovation ensures that predictive risk assessments are holistic, statistically calibrated, and actionable, rather than fragmented and one-size-fits-all."
    )
    
    add_styled_paragraph(
        doc,
        "The project is designed to empower clinicians and patients with actionable intelligence, assisting in early subclinical detection, optimizing multi-condition lifestyle and pharmacological interventions, and minimizing severe adverse events such as myocardial infarctions, strokes, and end-stage renal disease (ESRD). By promoting precision preventative medicine and evidence-based decision-making, the system directly contributes to individual longevity, healthcare equity, and national economic productivity. Ultimately, the motivation lies in transforming traditional episodic and reactive healthcare into a smart, proactive, comorbidity-aware, and sustainable healthcare intelligence ecosystem that enhances clinical outcomes while safeguarding public health resources for future generations."
    )

    add_heading_2(doc, "1.2 EXISTING SYSTEM")
    add_styled_paragraph(
        doc,
        "Existing computerized disease prediction platforms and clinical risk calculators primarily rely on static, isolated, or generalized datasets. These legacy systems often evaluate each medical condition in complete clinical isolation, failing to provide joint multi-disease risk assessments or account for real-time dynamic biomarkers such as blood pressure fluctuations, glycemic variability, or renal function indices."
    )
    
    add_styled_paragraph(
        doc,
        "Traditional risk tools like the Framingham Risk Score, ASCVD risk calculators, or standard online screening portals provide useful but broad statistical scores that lack precision for patient-specific, micro-level clinical decision-making. Moreover, current tools lack integration across disparate electronic health cohorts, physiological vitals, laboratory biomarkers, and lifestyle parameters, leading to one-size-fits-all risk estimates. This uncoordinated approach is ineffective in managing complex comorbid patients where diabetes, hypertension, and renal impairment interact continuously. As a result, clinicians and patients are left with limited or disconnected guidance, causing delayed interventions and increased clinical risk."
    )
    
    add_styled_paragraph(
        doc,
        "Additionally, most existing automated diagnostic platforms are rule-based or rely on opaque 'black-box' tree ensembles and shallow classifiers that lack explainability and probability calibration. These systems do not evolve dynamically with changing patient physiological trajectories or newly identified biomarker patterns. As a result, they cannot accurately capture dynamic clinical progressions or respond to sudden health deteriorations. Furthermore, data ingestion in many existing systems suffers from unhandled missingness, naive listwise deletion, or data leakage, which severely degrades predictive accuracy and clinical trust. The lack of interpretability prevents physicians from verifying the physiological rationale underlying AI predictions."
    )

    # Table 1.1: Existing vs Proposed System
    p_tbl = doc.add_paragraph()
    p_tbl.paragraph_format.space_before = Pt(8)
    p_tbl.paragraph_format.space_after = Pt(4)
    r = p_tbl.add_run("Table 1.1: Existing Vs Proposed System")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.italic = True
    
    tbl_data = [
        ("Parameter", "Existing System", "Proposed System"),
        ("Data Source", "Static, single-cohort clinical datasets", "Harmonized multi-cohort clinical datasets (CDC BRFSS, Kaggle CVD, UCI CKD: 139k+ records)"),
        ("Granularity", "Population-level or single-disease level", "Micro-level (individual biomarker, vital sign, and patient trajectory level)"),
        ("Technology Used", "Traditional single-task regression or shallow ML models", "Multi-Task Learning (MTL) Neural Network, Platt Calibration, and SHAP Explainable AI"),
        ("Disease Prediction", "Based on static isolated parameters (glucose or cholesterol only)", "Dynamic, simultaneous comorbidity risk stratification for T2D, CVD, and CKD"),
        ("Clinical Decision Support", "Limited or none; raw numerical scores only", "Automated clinical rules engine generating ADA/ACC/KDIGO-adherent care plans"),
        ("Longitudinal Telemetry", "Manual or periodic hospital visits", "Continuous longitudinal vital tracking with automated SMS/Email emergency alerts"),
        ("Explainability & Trust", "Opaque 'black-box' predictions with zero feature attribution", "Game-theoretic SHAP waterfall plots and global biomarker importance rankings"),
        ("Multi-Lingual Access", "Monolingual (English only) with technical jargon", "Localized 4-language support (English, Tamil, Hindi, Spanish) & AI Copilot")
    ]
    
    tbl_comp = doc.add_table(rows=len(tbl_data), cols=3)
    tbl_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_comp.autofit = False
    tbl_comp.columns[0].width = Inches(1.5)
    tbl_comp.columns[1].width = Inches(2.4)
    tbl_comp.columns[2].width = Inches(2.6)
    set_table_borders(tbl_comp)
    
    for idx, (c1, c2, c3) in enumerate(tbl_data):
        row = tbl_comp.rows[idx]
        for col_i, txt in enumerate([c1, c2, c3]):
            cell = row.cells[col_i]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(txt)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5 if idx > 0 else 10)
            if idx == 0:
                r.font.bold = True
                set_cell_background(cell, "F1F5F9")
            elif col_i == 0:
                r.font.bold = True

    add_heading_2(doc, "1.3 PROBLEM STATEMENT")
    add_styled_paragraph(
        doc,
        "Chronic non-communicable diseases remain the leading cause of premature mortality and healthcare burden globally, yet a vast number of patients and healthcare providers continue to face uncertainty in early risk detection, comorbidity management, and preventative care planning. Many individuals rely on episodic health check-ups, word-of-mouth advice, or subjective symptom awareness when managing chronic health risks. However, the silent, asymptomatic onset of Type 2 Diabetes, Cardiovascular Disease, and Chronic Kidney Disease makes these conventional, reactive approaches unreliable and dangerously delayed."
    )
    
    add_styled_paragraph(
        doc,
        "One of the major challenges faced by clinicians is the lack of personalized, comorbidity-aware diagnostic decision support. Physiological biomarkers, blood pressure, renal filtration rate, glycemic status, and lifestyle behaviors collectively influence long-term cardiometabolic and renal prognosis. However, medical practitioners often do not have access to unified computational tools that analyze these interconnected parameters simultaneously to provide coherent, multi-disease risk assessments. As a result, fragmented diagnostic evaluations lead to missed subclinical complications, delayed therapeutic escalations, and avoidable multi-organ damage."
    )
    
    add_styled_paragraph(
        doc,
        "Another pressing issue is the lack of explainability and statistical calibration in modern clinical machine learning. While deep learning models achieve high classification benchmarks, their 'black-box' nature prevents clinicians from understanding the underlying physiological factors driving individual risk scores. Furthermore, uncalibrated probability outputs mislead clinical triage thresholds. In addition, existing systems fail to link predictive risk scores directly to evidence-based medical guidelines, leaving patients without structured, actionable lifestyle and dietary intervention plans."
    )
    
    add_styled_paragraph(
        doc,
        "Therefore, the problem addressed in this project is the lack of an integrated, explainable, and comorbidity-aware AI clinical decision-support system that empowers healthcare practitioners and patients with simultaneous risk stratification, calibrated probabilities, game-theoretic biomarker attributions, and guideline-adherent multi-condition care plans within an accessible, multi-lingual web platform."
    )

    add_heading_2(doc, "1.4 OBJECTIVES OF THE PROJECT")
    add_styled_paragraph(
        doc,
        "• The main objective of this project is to develop an intelligent, data-driven clinical decision-support platform that can simultaneously analyze comorbidity risks and predict the onset of Type 2 Diabetes, Cardiovascular Disease, and Chronic Kidney Disease using Multi-Task Deep Learning (MTL) and Explainable AI (XAI). The system is designed to integrate heterogeneous clinical data sources—including CDC epidemiological surveys, cardiovascular cohorts, and nephrology records—to create a standardized 30-dimensional clinical feature space for multi-disease predictive modeling."
    )
    
    add_styled_paragraph(
        doc,
        "• A key goal of this project is to utilize a Shared Feature Neural Encoder to capture latent pathophysiological dependencies and metabolic cross-talk across diabetes, hypertension, and renal impairment. This shared representation enables the system to transfer representation capacity from data-rich domains to data-scarce conditions (such as CKD), leading to superior diagnostic sensitivity and generalization across heterogeneous clinical populations."
    )
    
    add_styled_paragraph(
        doc,
        "• Another major objective is to implement post-hoc Platt Sigmoid Scaling to ensure strict statistical probability calibration (minimizing Expected Calibration Error to < 0.011) and integrate game-theoretic SHAP (SHapley Additive exPlanations) for transparent biomarker attribution. This provides clinicians with clear, visual waterfall charts that elucidate positive and negative risk contributors for every individual patient."
    )
    
    add_styled_paragraph(
        doc,
        "• The project also intends to translate predictive risks into actionable clinical care plans using an automated clinical rules engine adhering to American Diabetes Association (ADA), American Heart Association (AHA/ACC), and Kidney Disease: Improving Global Outcomes (KDIGO) guidelines. It further incorporates longitudinal vital tracking, automated SMS/email emergency alerting via Twilio, multi-lingual localization (English, Tamil, Hindi, Spanish), and a conversational clinical AI copilot to maximize accessibility."
    )

    add_heading_2(doc, "1.5 PROPOSED SYSTEM")
    add_styled_paragraph(
        doc,
        f"The proposed system, {PROJECT_TITLE}, aims to revolutionize chronic disease prevention and clinical decision support through multi-task deep learning and transparent artificial intelligence. Unlike traditional single-disease diagnostic calculators that evaluate conditions in isolation, SmartCare AI focuses on comprehensive comorbidity modeling. It integrates demographic parameters, physiological vitals, biochemical laboratory markers, lifestyle habits, and computed cardiovascular/renal indices into a standardized 30-feature clinical vector to generate simultaneous risk assessments for Type 2 Diabetes, Cardiovascular Disease, and Chronic Kidney Disease."
    )
    
    add_styled_paragraph(
        doc,
        "At the core of SmartCare AI lies the Multi-Task Shared Feature Neural Encoder, which maps the 30-dimensional input vector into a joint 32-dimensional latent embedding space. While traditional models treat each disease independently, the shared neural encoder learns invariant representations governing systemic vascular and metabolic damage. Three dedicated task heads branch from this shared latent layer to predict individual calibrated risk probabilities."
    )
    
    add_styled_paragraph(
        doc,
        "The SmartCare AI web platform serves as the interactive clinical interface for medical practitioners and patients. It presents intuitive dashboards displaying calibrated comorbidity risk gauges, longitudinal vital trajectories, and interactive SHAP biomarker waterfall plots. Furthermore, the platform integrates an automated clinical rules engine that synthesizes personalized dietary, physical activity, pharmacological review, and follow-up intervention schedules. The entire system is built upon a modular, cloud-ready FastAPI backend and a responsive React frontend, secured by JWT authentication and Role-Based Access Control."
    )

    add_heading_2(doc, "1.6 BENEFITS OF THE PROJECT")
    add_bullet_item(doc, "Better Clinical Decision-Making based on Comorbidity-Aware Insights", "Provides clinicians with a holistic view of the patient's cardiorenal-metabolic status, transcending isolated single-disease assessments and preventing overlooked subclinical complications.")
    add_bullet_item(doc, "Transparent and Trustworthy Explainable AI", "Eliminates 'black-box' opacity by presenting exact game-theoretic SHAP feature attributions and biomarker contribution rankings for every patient diagnosis.")
    add_bullet_item(doc, "Statistically Calibrated Risk Probabilities", "Applies Platt Sigmoid Scaling to ensure reported risk scores represent genuine posterior probabilities (ECE < 0.011), supporting reliable clinical triage.")
    add_bullet_item(doc, "Actionable Guideline-Concordant Intervention Regimens", "Automates evidence-based lifestyle, dietary, and medical guidance conforming strictly to ADA, ACC/AHA, and KDIGO clinical standards.")
    add_bullet_item(doc, "Proactive Longitudinal Telemetry and Emergency Alerting", "Monitors temporal vital trends and automatically dispatches real-time SMS (Twilio) and email alerts upon detecting acute threshold breaches (e.g., SBP >= 180 mmHg).")
    add_bullet_item(doc, "Multi-Lingual Accessibility and Conversational AI Assistance", "Democratizes health intelligence across diverse populations through 4-language localization (English, Tamil, Hindi, Spanish) and an empathetic conversational AI copilot.")
    add_bullet_item(doc, "Contribution to Sustainable Development Goals (SDGs)", "Directly supports UN SDGs: SDG 3 (Good Health and Well-Being), SDG 8 (Decent Work & Economic Growth), SDG 9 (Industry, Innovation & Infrastructure), SDG 10 (Reduced Inequalities), and SDG 12 (Responsible Resource Utilization).")

    doc.add_page_break()

def build_chapter_2(doc):
    """Generates Chapter 2: Literature Survey citing exact references [1] to [20]."""
    add_heading_1(doc, "CHAPTER 2\nLITERATURE SURVEY")
    
    add_heading_2(doc, "2.1 INTRODUCTION")
    add_styled_paragraph(
        doc,
        "A literature review serves as the foundation for understanding the technological, methodological, and clinical landscape relevant to chronic disease risk stratification and artificial intelligence in healthcare. Numerous studies in medical informatics, machine learning, and clinical decision support have demonstrated the immense potential of data integration in improving diagnostic accuracy. However, most existing computerized systems remain limited in their ability to model multi-disease comorbidity interactions or fail to provide explainable, calibrated risk predictions suitable for real-world clinical deployment."
    )
    add_styled_paragraph(
        doc,
        "This chapter reviews existing research on machine learning for diabetes screening, cardiovascular disease prediction, chronic kidney disease detection, multi-task learning paradigms, explainable AI (XAI) frameworks, and clinical decision-support architectures. It also highlights the recent evolution of calibrated and explainable multi-task methodologies that improve predictive performance and clinical trustworthiness by capturing interdependencies across co-occurring chronic conditions."
    )

    add_heading_2(doc, "2.2 RELATED WORK")
    
    add_heading_3(doc, "2.2.1 Multi-Disease and Cardiorenal-Metabolic Risk Prediction")
    add_styled_paragraph(
        doc,
        "Recent investigations have underscored the necessity of evaluating cardiovascular and renal outcomes jointly in diabetic populations. Kwiendacz et al. [1] conducted a pivotal machine learning study within the Silesia Diabetes-Heart Project, demonstrating that major adverse cardiac events (MACE) in patients with diabetes are heavily exacerbated by concomitant chronic kidney disease. Their findings proved that isolated cardiac calculators consistently underestimate risk in patients with impaired renal function. In a related breakthrough, Hossain et al. [2] introduced CardioMeta, a calibrated multi-task learning framework designed to simultaneously predict diabetes, hypertension, and cardiovascular disease, establishing that multi-task parameter sharing significantly improves prediction stability across interrelated cardiometabolic endpoints."
    )
    
    add_heading_3(doc, "2.2.2 Multi-Task Learning and Neural Graph Modeling in Chronic Disease")
    add_styled_paragraph(
        doc,
        "The application of deep multi-task architectures in nephrology and complex chronic disease management was further advanced by Sakil et al. [3], who combined Transformer representations and graph neural networks for multi-task learning in chronic kidney disease management. Their architecture validated that joint representation learning effectively mitigates sample sparsity in specialized nephrology cohorts. Furthermore, Rajwade et al. [5] developed 'Diagnosify', a multidisclose predictive system using ensemble machine learning to detect co-occurring chronic illnesses, emphasizing the operational value of unified diagnostic platforms in outpatient primary care settings."
    )

    add_heading_3(doc, "2.2.3 Explainable AI (XAI) and SHAP Interpretability in Healthcare")
    add_styled_paragraph(
        doc,
        "Model interpretability is paramount for clinical adoption. Sridevi et al. [4] developed a machine learning framework for chronic kidney disease and diabetes prediction augmented with SHAP (SHapley Additive exPlanations) interpretability, proving that game-theoretic feature attribution provides actionable insights into key metabolic drivers. Similarly, Shah et al. [13] evaluated cardiovascular risk prediction using hybrid ensemble learning coupled with explainable AI, illustrating how patient-level attribution plots enhance clinician confidence. In nephrology, Jawad et al. [14] and Nguycharoen et al. [15] applied explainable ensemble methods to predict chronic kidney disease in primary care settings, demonstrating that visualizing biomarker contributions drastically reduces diagnostic turnaround times."
    )

    add_heading_3(doc, "2.2.4 Cardiovascular Disease Modeling in Diabetic and Renal Cohorts")
    add_styled_paragraph(
        doc,
        "The intimate physiological coupling between renal decline, diabetes, and cardiovascular complications has been extensively investigated. Zhu et al. [6] implemented machine learning models specifically for cardiovascular disease risk prediction in patients with chronic kidney disease, identifying proteinuria and arterial stiffness as critical cross-domain predictors. Sang et al. [7] and Jiang et al. [8] developed and systematically reviewed machine learning predictive models for cardiovascular complications in Type 2 Diabetes cohorts, noting that multi-feature architectures combining glycemic biomarkers with blood pressure indices significantly outperform conventional linear risk scores."
    )

    add_heading_3(doc, "2.2.5 Predictive Modeling of Chronic Kidney Disease and Diabetic Nephropathy")
    add_styled_paragraph(
        doc,
        "Predicting diabetic kidney disease progression before irreversible structural damage occurs is a major focus of modern bioinformatics. Nayak et al. [9] demonstrated high-precision machine learning models for diabetic kidney disease progression, while Zhou et al. [10] developed predictive algorithms for CKD progression specifically in hyperglycemic older adults. Wu et al. [11] investigated explainable machine learning for renal function progression, emphasizing the diagnostic value of tracking longitudinal eGFR trajectories. Furthermore, Fu et al. [12] developed a nationwide predictive model for CKD progression in diabetic patients, demonstrating that early predictive intervention substantially reduces dialysis incidence."
    )

    add_heading_3(doc, "2.2.6 Ensemble Learning and Feature Selection in Chronic Disease Screening")
    add_styled_paragraph(
        doc,
        "Ensemble methodologies have demonstrated robust classification performance across diverse medical benchmarks. Endalew et al. [16] implemented ensemble machine learning models for diabetes prediction based on clinical and lifestyle risk factors, achieving superior classification accuracy over single decision trees. Pathak et al. [17] and Jeribi et al. [18] investigated heart disease risk prediction using advanced feature selection and engineering techniques, proving that derived hemodynamic indices (such as Pulse Pressure and Mean Arterial Pressure) substantially enhance model discrimination."
    )

    add_heading_3(doc, "2.2.7 Systematic Reviews on Clinical AI and Vascular Risk Modeling")
    add_styled_paragraph(
        doc,
        "Comprehensive systematic literature reviews by Sanmarchi et al. [19] surveyed the global state of machine learning for predicting, diagnosing, and treating chronic kidney disease, highlighting the urgent need for model calibration, external validation, and seamless EHR integration. Finally, Liu et al. [20] conducted predictive modeling and risk analysis for peripheral vascular disease in Type 2 Diabetes, confirming that systemic microvascular damage in diabetes serves as a common pathophysiological substrate across all major organ systems."
    )

    add_heading_2(doc, "2.3 INFERENCE FROM RELATED WORK")
    add_styled_paragraph(
        doc,
        "From the literature review, several critical insights shape the foundation of the proposed SmartCare AI system:"
    )
    
    add_bullet_item(doc, "Gap in Comorbidity-Aware Modeling", "Traditional machine learning models excel in single-disease prediction [7, 16, 17] but fail to capture the mutual pathophysiological cross-talk connecting diabetes, cardiovascular events, and renal decline [1, 6, 8]. Multi-Task Learning (MTL) provides a mathematically sound solution by learning shared latent representations [2, 3].")
    add_bullet_item(doc, "Data Scarcity and Cross-Cohort Harmonization", "Specialized clinical datasets (such as CKD) are often limited in sample size [3, 19]. Harmonizing diverse cohorts (CDC BRFSS, Kaggle CVD, UCI CKD) and employing task-balanced sampling allows data-rich tasks to reinforce data-scarce domains.")
    add_bullet_item(doc, "Essential Role of Probability Calibration", "Raw neural network and ensemble logits are frequently miscalibrated [2]. Implementing Platt Sigmoid Scaling ensures that risk outputs reflect true clinical posterior probabilities (ECE < 0.011).")
    add_bullet_item(doc, "Necessity of Game-Theoretic Explainability", "Clinicians require interpretable feature attributions before adopting AI in medical practice [4, 11, 13, 14, 15]. Game-theoretic SHAP waterfall plots provide exact local and global biomarker explanations.")
    add_bullet_item(doc, "Bridging Prediction to Clinical Action", "Predictive models must not stop at numerical scores; integrating deterministic rules engines adhering to global clinical guidelines (ADA, ACC/AHA, KDIGO) translates risk predictions into actionable care plans.")
    add_bullet_item(doc, "Continuous Longitudinal Telemetry and Multi-Lingual Accessibility", "Modern clinical platforms require real-time emergency alerting (Twilio SMS, Email) and regional language localization to ensure equitable and proactive healthcare delivery.")

    doc.add_page_break()

def build_chapter_3(doc):
    """Generates Chapter 3: System Design with actual figures."""
    add_heading_1(doc, "CHAPTER 3\nSYSTEM DESIGN")
    
    add_heading_2(doc, "3.1 INTRODUCTION")
    add_styled_paragraph(
        doc,
        "System design forms the backbone of the SmartCare AI platform, defining how various hardware, software, machine learning, and data components interact to achieve the project’s clinical objectives. It establishes a structured framework that governs clinical data acquisition, cross-cohort harmonization, multi-task neural inference, probability calibration, explainability generation, clinical rule translation, and interactive presentation. The purpose of system design is to ensure that each stage—ranging from patient data ingestion to the generation of predictive comorbidity insights—is efficiently coordinated and executed with high accuracy. This phase bridges conceptual algorithmic design with practical implementation by transforming theoretical models into a robust, enterprise-grade clinical software architecture."
    )
    add_styled_paragraph(
        doc,
        "The SmartCare AI system design emphasizes modularity, loose coupling, and scalability, ensuring that functional components such as data preprocessing, multi-task neural modeling, SHAP explainability, guideline rules execution, emergency telemetry alerting, and user interfaces can operate independently yet cohesively within a microservices ecosystem."
    )

    add_heading_2(doc, "3.2 SYSTEM ARCHITECTURE")
    add_styled_paragraph(
        doc,
        "The system is designed with a modular, six-tier layered architecture to efficiently handle complex, data-driven comorbidity risk assessment. At the foundation, the Data Ingestion and Harmonization Layer integrates 30 standardized clinical features across demographics, physiological vitals, laboratory biomarkers, and lifestyle factors. The raw data passes through a zero-leakage preprocessing pipeline that executes training-fitted median imputation and RobustScaler normalization."
    )
    add_styled_paragraph(
        doc,
        "The core analytical engine is the Multi-Task Neural Network, which utilizes a Shared Feature Encoder (Dense 30->64 -> Dense 64->32) to map patient features into a 32-dimensional latent representation space capturing joint cardiorenal-metabolic patterns. Three dedicated task heads branch from this shared latent space to generate simultaneous prediction logits for Type 2 Diabetes, Cardiovascular Disease, and Chronic Kidney Disease. The Probability Calibration Subsystem applies Platt Sigmoid Scaling to ensure true statistical probabilities, while the SHAP Explainability Engine calculates exact Shapley attributions. The Clinical Rules Engine translates risks into ADA/ACC/KDIGO-adherent care plans, which are served via a FastAPI REST service to an interactive React dashboard."
    )

    # Insert Figure 3.1: System Architecture
    fig_3_1_path = os.path.join(FIG_DIR, "fig_3_1_system_architecture.png")
    add_figure_with_image(doc, fig_3_1_path, "Figure 3.1: System Architecture Diagram", width_inches=6.0)

    add_heading_2(doc, "3.3 SYSTEM REQUIREMENTS")
    add_styled_paragraph(
        doc,
        "The system requirements define the essential hardware and software specifications necessary for the efficient development, training, deployment, and operation of the SmartCare AI platform. These requirements ensure that all modules—including multi-task comorbidity risk stratification, SHAP explainability, clinical rules execution, longitudinal vital tracking, and conversational AI assistance—function smoothly and deliver real-time, accurate insights to clinicians and patients."
    )

    # Table 3.1: Software Tools
    p_tbl = doc.add_paragraph()
    p_tbl.paragraph_format.space_before = Pt(8)
    p_tbl.paragraph_format.space_after = Pt(4)
    r = p_tbl.add_run("Table 3.1: Software Tools")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.italic = True
    
    sw_data = [
        ("Component", "Technology", "Role"),
        ("Frontend Framework", "HTML, CSS, JavaScript, React.js, TailwindCSS", "Provides interactive web dashboard for visualizing risk gauges, SHAP waterfall charts, vital trends, and care plans."),
        ("Backend Framework", "FastAPI / Python 3.13, Uvicorn", "Handles high-performance asynchronous REST API endpoints, processes clinical requests, and integrates frontend with ML models."),
        ("Database", "SQLite / MongoDB / SQLAlchemy", "Stores user profiles, patient clinical records, longitudinal vital logs, audit trails, and authentication tokens."),
        ("Machine Learning", "PyTorch, Scikit-learn, XGBoost", "Implements Multi-Task Shared Feature Encoder, baseline benchmark models, Platt calibration, and pipeline scalers."),
        ("Explainability & Visuals", "SHAP (v0.52.0), Recharts, Matplotlib", "Computes game-theoretic Shapley values, rendering local waterfall plots and interactive dashboard radar/line charts."),
        ("Data Handling", "Pandas, NumPy", "Cleans, normalizes, harmonizes multi-cohort datasets (139k+ records), and computes derived clinical indices."),
        ("Emergency Telemetry", "Twilio REST API, smtplib", "Dispatches automated emergency SMS alerts and structured clinical summary emails upon acute threshold breaches."),
        ("Operating System", "Windows 11 / Linux Ubuntu", "Provides a stable, high-performance environment for model training, microservice hosting, and production web deployment.")
    ]
    
    tbl_sw = doc.add_table(rows=len(sw_data), cols=3)
    tbl_sw.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sw.autofit = False
    tbl_sw.columns[0].width = Inches(1.5)
    tbl_sw.columns[1].width = Inches(2.2)
    tbl_sw.columns[2].width = Inches(2.8)
    set_table_borders(tbl_sw)
    
    for idx, (c1, c2, c3) in enumerate(sw_data):
        row = tbl_sw.rows[idx]
        for col_i, txt in enumerate([c1, c2, c3]):
            cell = row.cells[col_i]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(txt)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5 if idx > 0 else 10)
            if idx == 0:
                r.font.bold = True
                set_cell_background(cell, "F1F5F9")
            elif col_i == 0:
                r.font.bold = True

    # Table 3.2: Functional Requirements
    p_tbl = doc.add_paragraph()
    p_tbl.paragraph_format.space_before = Pt(12)
    p_tbl.paragraph_format.space_after = Pt(4)
    r = p_tbl.add_run("Table 3.2: Functional Requirements")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.italic = True
    
    fr_data = [
        ("S. No", "Functional Requirement", "Description"),
        ("1", "User Authentication & RBAC", "Allows patients and clinicians to securely sign up and log in with bcrypt password hashing and JWT authentication to protect clinical records."),
        ("2", "Clinical Data Harmonization", "Fetches, validates, and cleans 30 standardized clinical features across demographics, vitals, labs, and lifestyle metrics with zero-leakage median imputation."),
        ("3", "Multi-Task Risk Stratification", "Simultaneously predicts calibrated risk probabilities for Type 2 Diabetes, Cardiovascular Disease, and Chronic Kidney Disease in sub-second inference."),
        ("4", "SHAP Feature Attribution", "Decomposes predicted risk scores into positive and negative Shapley contributions, generating interactive patient waterfall charts and global biomarker rankings."),
        ("5", "Clinical Guideline Translation", "Translates predicted comorbidity risks and abnormal biomarkers into actionable lifestyle, dietary, pharmacological, and follow-up plans adhering to ADA, ACC/AHA, and KDIGO guidelines."),
        ("6", "Longitudinal Vital Tracking & Telemetry", "Monitors historical vital logs over time, computes trend trajectories, and dispatches automated emergency SMS/Email alerts upon acute threshold breaches.")
    ]
    
    tbl_fr = doc.add_table(rows=len(fr_data), cols=3)
    tbl_fr.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_fr.autofit = False
    tbl_fr.columns[0].width = Inches(0.8)
    tbl_fr.columns[1].width = Inches(2.2)
    tbl_fr.columns[2].width = Inches(3.5)
    set_table_borders(tbl_fr)
    
    for idx, (c1, c2, c3) in enumerate(fr_data):
        row = tbl_fr.rows[idx]
        for col_i, txt in enumerate([c1, c2, c3]):
            cell = row.cells[col_i]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(txt)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5 if idx > 0 else 10)
            if idx == 0:
                r.font.bold = True
                set_cell_background(cell, "F1F5F9")
            elif col_i == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r.font.bold = True

    # Table 3.3: Hardware Requirements
    p_tbl = doc.add_paragraph()
    p_tbl.paragraph_format.space_before = Pt(12)
    p_tbl.paragraph_format.space_after = Pt(4)
    r = p_tbl.add_run("Table 3.3: Hardware Requirements")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.italic = True
    
    hw_data = [
        ("Component", "Minimum Specification", "Justification"),
        ("Processor", "Intel Core i5 / AMD Ryzen 5 or higher", "Required to handle multi-cohort data preprocessing, SHAP TreeExplainer computations, and real-time inference efficiently."),
        ("RAM", "8 GB (16 GB recommended)", "Supports large dataset operations (139k+ records), multi-task tensor training, and parallel API request handling."),
        ("Storage", "250 GB Solid State Drive (SSD)", "Facilitates fast read/write operations for large datasets, serialized models, database logs, and web assets."),
        ("Display", "1080p Resolution Monitor", "Provides clear visualization of analytics dashboards, SHAP waterfall plots, radar charts, and longitudinal trend graphs."),
        ("Network", "Broadband Internet (10+ Mbps)", "Required for accessing external APIs (Twilio SMS, cloud databases, SMTP servers) and web client deployment.")
    ]
    
    tbl_hw = doc.add_table(rows=len(hw_data), cols=3)
    tbl_hw.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_hw.autofit = False
    tbl_hw.columns[0].width = Inches(1.5)
    tbl_hw.columns[1].width = Inches(2.2)
    tbl_hw.columns[2].width = Inches(2.8)
    set_table_borders(tbl_hw)
    
    for idx, (c1, c2, c3) in enumerate(hw_data):
        row = tbl_hw.rows[idx]
        for col_i, txt in enumerate([c1, c2, c3]):
            cell = row.cells[col_i]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(txt)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5 if idx > 0 else 10)
            if idx == 0:
                r.font.bold = True
                set_cell_background(cell, "F1F5F9")
            elif col_i == 0:
                r.font.bold = True

    add_heading_2(doc, "3.4 DATA FLOW DIAGRAM / USE CASE DIAGRAM")
    
    add_heading_3(doc, "3.4.1 DATA FLOW DIAGRAM (DFD)")
    add_styled_paragraph(
        doc,
        "The system is designed using a microservices architecture, where each functional module operates independently while communicating through a centralized FastAPI gateway. This design allows for modularity, scalability, and efficient data sharing between components. At the user interface level, the system accepts clinical inputs such as blood pressure readings, glucose levels, lipid profiles, renal function markers, and lifestyle habits, which serve as the primary parameters for both comorbidity risk prediction and SHAP explainability modules."
    )

    # Insert Figure 3.2: DFD
    fig_3_2_path = os.path.join(FIG_DIR, "fig_3_2_data_flow_diagram.png")
    add_figure_with_image(doc, fig_3_2_path, "Figure 3.2: Data Flow Diagram", width_inches=6.0)
    
    add_styled_paragraph(
        doc,
        "The Multi-Task Comorbidity Risk Stratification System analyzes these inputs to simultaneously predict calibrated risk scores for Type 2 Diabetes, Cardiovascular Disease, and Chronic Kidney Disease, taking into account mutual pathophysiological dependencies. Simultaneously, the SHAP Explainability module assesses biomarker contributions, generating actionable visual waterfall charts for clinicians. Both these modules feed into the Clinical Intervention Engine, which synthesizes evidence-based dietary, lifestyle, and pharmacological care plans adhering to ADA, ACC/AHA, and KDIGO guidelines. Following this, the Longitudinal Telemetry module tracks historical vital trends and dispatches real-time emergency SMS/Email alerts upon acute threshold breaches. To support patient interaction and query resolution, the system incorporates an AI-powered conversational copilot, which answers queries and provides personalized medical advice based on predictive analytics."
    )

    add_heading_3(doc, "3.4.2 USE CASE DIAGRAM")
    add_styled_paragraph(
        doc,
        "The Use Case Diagram illustrates the interactions between different actors and the core functionalities of the SmartCare AI system, specifically focused on comorbidity risk prediction, SHAP biomarker explainability, clinical guideline recommendations, longitudinal tracking, and AI-assisted conversational guidance. The primary actors in the system are Patients and Clinicians (Physicians/Specialists), each of whom can log in or sign up to access the platform. Patients enter vital logs and view personalized care plans, while Clinicians evaluate comprehensive diagnostic dossiers and review SHAP waterfall attributions."
    )
    add_styled_paragraph(
        doc,
        "Once authenticated, both actors interact with the system’s core modules. The Multi-Task Risk Stratification module processes clinical parameters to compute calibrated risk tiers. The SHAP Explainability module continuously visualizes positive and negative feature contributions. The Clinical Rules Engine automatically generates multi-condition care regimens, while the Emergency Telemetry module dispatches real-time SMS/Email alerts when severe vital breaches are detected. The AI Assistance module acts as an intelligent medical copilot, answering queries and guiding patients through their diagnostic findings."
    )

    # Insert Figure 3.3: Use Case Diagram
    fig_3_3_path = os.path.join(FIG_DIR, "fig_3_3_use_case_diagram.png")
    add_figure_with_image(doc, fig_3_3_path, "Figure 3.3 Use Case Diagram", width_inches=6.0)

    doc.add_page_break()
