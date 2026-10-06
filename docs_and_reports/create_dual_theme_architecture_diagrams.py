"""
SmartCare AI - Dual-Theme System Architecture Diagram Generator
Generates both Light Theme (Publication/Print) and Dark Theme (Digital/Presentation) diagrams.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_diagram(theme='light'):
    is_light = (theme == 'light')
    
    # Theme Palette
    bg_main = '#ffffff' if is_light else '#0b1120'
    hdr_bg = '#f8fafc' if is_light else '#0f172a'
    hdr_border = '#cbd5e1' if is_light else '#1e293b'
    title_text = '#0f172a' if is_light else '#ffffff'
    sub_text = '#0284c7' if is_light else '#38bdf8'
    
    tier_bg = '#f8fafc' if is_light else '#0f172a'
    tier_border = '#e2e8f0' if is_light else '#1e293b'
    tier_sub = '#64748b' if is_light else '#94a3b8'
    
    card_bg = '#ffffff' if is_light else '#131e36'
    card_border = '#cbd5e1' if is_light else '#334155'
    card_item_text = '#334155' if is_light else '#e2e8f0'

    fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
    fig.patch.set_facecolor(bg_main)
    ax.set_facecolor(bg_main)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # 1. HEADER BANNER
    header_box = patches.FancyBboxPatch(
        (3, 91), 94, 7,
        boxstyle="round,pad=0.5",
        ec=hdr_border, fc=hdr_bg, lw=1.5
    )
    ax.add_patch(header_box)
    
    ax.plot([4, 96], [91.2, 91.2], color="#0284c7", lw=2.5, solid_capstyle='round')
    
    ax.text(50, 95.2, "SMARTCARE AI — SYSTEM ARCHITECTURE DIAGRAM", 
            ha='center', va='center', fontsize=15, fontweight='bold', color=title_text, fontfamily='sans-serif')
    ax.text(50, 92.5, "Comorbidity-Aware Explainable Multi-Task Learning Clinical Decision Support Ecosystem (T2D • CVD • CKD)", 
            ha='center', va='center', fontsize=9.5, fontweight='semibold', color=sub_text, fontfamily='sans-serif')

    def draw_tier_container(x, y, w, h, title, subtitle, badge_color):
        container = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4", ec=tier_border, fc=tier_bg, lw=1.2)
        ax.add_patch(container)
        
        # Badge
        badge = patches.FancyBboxPatch((x + 1.2, y + h - 2.8), len(title)*0.92 + 2, 2.2, boxstyle="round,pad=0.2", ec=badge_color, fc=badge_color, lw=1)
        ax.add_patch(badge)
        ax.text(x + 2.2, y + h - 1.7, title, fontsize=8, fontweight='bold', color='#ffffff', fontfamily='sans-serif')
        ax.text(x + len(title)*0.92 + 4.5, y + h - 1.7, subtitle, fontsize=7.5, color=tier_sub, fontfamily='sans-serif')

    def draw_card(x, y, w, h, title, items, header_bg, title_color="#ffffff"):
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", ec=card_border, fc=card_bg, lw=1.2)
        ax.add_patch(card)
        
        hdr = patches.FancyBboxPatch((x, y + h - 2.6), w, 2.6, boxstyle="round,pad=0.2", ec=header_bg, fc=header_bg, lw=1)
        ax.add_patch(hdr)
        ax.text(x + w/2, y + h - 1.3, title, ha='center', va='center', fontsize=7.5, fontweight='bold', color=title_color, fontfamily='sans-serif')
        
        line_y = y + h - 3.8
        for item in items:
            ax.text(x + 1.0, line_y, item, fontsize=6.5, color=card_item_text, fontfamily='sans-serif')
            line_y -= 1.4

    # TIER 1: CLIENT PRESENTATION TIER (y: 77.5 to 89.5)
    draw_tier_container(3, 77.5, 94, 12, "TIER 1: CLIENT PRESENTATION LAYER", "React 18.2 • TailwindCSS • Responsive Dashboard • Vite", "#0284c7")
    draw_card(4.5, 78.5, 29, 8.2, "Patient Portal (Wellness UI)", [
        "• Interactive 3-Disease Risk Score Gauges",
        "• Longitudinal Vitals & Glucose Telemetry",
        "• ADA/ACC/KDIGO Lifestyle Interventions",
        "• Vernacular Localization (Tamil/Hindi/ES)"
    ], header_bg="#0284c7")

    draw_card(35.5, 78.5, 29, 8.2, "Clinician Clinical Workstation", [
        "• Multi-Patient Triage Roster & EHR Dossiers",
        "• Interactive SHAP Waterfall Biomarker Plots",
        "• Calibrated Probability Risk Categorization",
        "• Pharmacological Contraindication Review"
    ], header_bg="#0d9488")

    draw_card(66.5, 78.5, 29, 8.2, "Conversational Clinical Copilot", [
        "• Multilingual NLP Chatbot (4 Languages)",
        "• Real-Time Medical Report Interpretation",
        "• Context-Aware Dietary & Exercise Guidance",
        "• Medication Adherence Counseling Daemon"
    ], header_bg="#7c3aed")

    # TIER 2: API GATEWAY & SECURITY TIER (y: 64.5 to 76)
    draw_tier_container(3, 64.5, 94, 11.5, "TIER 2: API GATEWAY & SECURITY LAYER", "FastAPI (Async Python 3.13) • Uvicorn • JWT • RBAC", "#0d9488")
    draw_card(4.5, 65.5, 29, 7.8, "FastAPI REST Gateway", [
        "• High-Performance Asynchronous Endpoints",
        "• /predict, /explain, /intervention, /alerts",
        "• OpenAPI / Swagger Auto-Documentation",
        "• CORS & Rate Limiting Middleware"
    ], header_bg="#0f766e")

    draw_card(35.5, 65.5, 29, 7.8, "Authentication & Security Subsystem", [
        "• OAuth2 with JWT Bearer Access Tokens",
        "• Bcrypt Password Hashing with Salt",
        "• Role-Based Access Control (Patient/Doctor)",
        "• End-to-End TLS Encryption & HIPAA Guards"
    ], header_bg="#1e293b" if is_light else "#334155")

    draw_card(66.5, 65.5, 29, 7.8, "Validation & Ingestion Pipeline", [
        "• Strict Pydantic Data Schema Validation",
        "• Clinical Out-of-Bounds Range Rejection",
        "• Dynamic Hemodynamic Derived Indicators",
        "• Structured JSON Audit Trail Telemetry"
    ], header_bg="#4338ca")

    # TIER 3: DATA INGESTION & HARMONIZATION (y: 50.0 to 62.5)
    draw_tier_container(3, 50.0, 94, 12.5, "TIER 3: DATA INGESTION & CROSS-COHORT HARMONIZATION", "CDC BRFSS • Kaggle CVD • UCI CKD (139,297 Multi-Cohort Records)", "#4f46e5")
    draw_card(4.5, 51.0, 29, 8.8, "Multi-Cohort Clinical Data Ingestion", [
        "• CDC BRFSS 2015 Survey (N = 70,692)",
        "• Kaggle Cardiovascular Cohort (N = 68,205)",
        "• UCI Chronic Kidney Dataset (N = 400)",
        "• Heterogeneous Feature Schema Mapping"
    ], header_bg="#4338ca")

    draw_card(35.5, 51.0, 29, 8.8, "Zero-Leakage Preprocessing Engine", [
        "• Training-Partition Fitted Median Imputation",
        "• RobustScaler Outlier-Resilient Normalization",
        "• Task-Balanced Sampling (20% CKD Allocation)",
        "• 80:20 Stratified Train-Test Separation"
    ], header_bg="#312e81")

    draw_card(66.5, 51.0, 29, 8.8, "30-D Standardized Clinical Vector", [
        "• Vitals: SBP, DBP, Heart Rate, BMI (15-50)",
        "• Labs: FBS, HbA1c, Chol, HDL, Trig, Creat, BUN",
        "• Lifestyle & Medical History: Smoking, HTN, Diet",
        "• Computed: Pulse Pressure, MAP, CKD-EPI eGFR"
    ], header_bg="#1e293b" if is_light else "#0f172a")

    # TIER 4: MULTI-TASK NEURAL NETWORK ENGINE (y: 33.5 to 48)
    draw_tier_container(3, 33.5, 94, 14.5, "TIER 4: COMORBIDITY-AWARE MULTI-TASK LEARNING ENGINE", "PyTorch • Shared Latent Representation • Task-Masked Loss Optimization", "#9333ea")
    draw_card(4.5, 34.5, 29, 10.5, "Shared Feature Neural Encoder", [
        "• Input Layer: 30 Harmonized Clinical Features",
        "• Dense Layer 1: 30 → 64 Units (ReLU)",
        "• Layer Normalization + Dropout (p = 0.15)",
        "• Dense Layer 2: 64 → 32 Latent Bottleneck",
        "• Joint Cardiorenal-Metabolic Representation",
        "• Cross-Task Inductive Knowledge Transfer"
    ], header_bg="#6b21a8")

    draw_card(35.5, 34.5, 29, 10.5, "Task-Specific Diagnostic Heads", [
        "• Type 2 Diabetes Head: Dense(32→16→1)",
        "  - ROC-AUC: 0.8276 | Recall: 88.72% | F1: 0.7751",
        "• Cardiovascular Disease Head: Dense(32→16→1)",
        "  - ROC-AUC: 0.7974 | Recall: 79.13% | F1: 0.7306",
        "• Chronic Kidney Disease Head: Dense(32→16→1)",
        "  - ROC-AUC: 0.9953 | Recall: 94.59% | F1: 0.9589",
        "• Simultaneous Forward Inference in < 12ms"
    ], header_bg="#86198f")

    draw_card(66.5, 34.5, 29, 10.5, "Calibration & Explainability (XAI)", [
        "• Post-Hoc Platt Sigmoid Calibration Engine",
        "  - Logit-to-Posterior Mapping (ECE < 0.011)",
        "• Game-Theoretic SHAP Engine (Tree & Kernel)",
        "  - Exact Shapley Feature Attribution (phi_i)",
        "  - Local Patient Risk Waterfall Decomposition",
        "  - Global Cohort Biomarker Importance Hierarchy"
    ], header_bg="#9d174d")

    # TIER 5: CLINICAL DECISION SUPPORT & TELEMETRY (y: 17.5 to 31.5)
    draw_tier_container(3, 17.5, 94, 14.0, "TIER 5: CLINICAL DECISION SUPPORT & TELEMETRY DISPATCHER", "ADA 2026 • ACC/AHA 2026 • KDIGO 2026 Guidelines • Twilio SMS API", "#16a34a")
    draw_card(4.5, 18.5, 29, 10.2, "Clinical Guidelines Rules Engine", [
        "• ADA 2026 Standards: Glycemic Targets & Meds",
        "• ACC/AHA 2026: Lipid Management & BP Control",
        "• KDIGO 2026: eGFR Staging & Proteinuria Care",
        "• Automated Personalized Dietary Care Plans",
        "• Aerobic & Resistance Physical Prescriptions",
        "• Pharmacological Contraindication Warnings"
    ], header_bg="#15803d")

    draw_card(35.5, 18.5, 29, 10.2, "Longitudinal Vital Tracker & Telemetry", [
        "• Continuous Time-Series Vital Signs Log",
        "• SBP, DBP, Fasting Blood Sugar, Body Weight",
        "• Historical Trend Velocity & Rate-of-Change",
        "• Micro-Level Health Trajectory Projection",
        "• Interactive Multi-Axis Trend Visualization",
        "• Routine Check-Up & Screening Reminders"
    ], header_bg="#0369a1")

    draw_card(66.5, 18.5, 29, 10.2, "Emergency Alert & Crisis Dispatcher", [
        "• Real-Time Critical Breach Detection Daemon",
        "  - Hypertensive Crisis (SBP >= 180 mmHg)",
        "  - Severe Hyperglycemia (FBS >= 300 mg/dL)",
        "• Automated Twilio SMS Emergency Broadcast",
        "• Structured Clinical Summary Email Dispatch",
        "• Nearest Emergency Center Geo-Routing"
    ], header_bg="#b91c1c")

    # TIER 6: PERSISTENCE & STORAGE (y: 2.0 to 15.5)
    draw_tier_container(3, 2.0, 94, 13.5, "TIER 6: DATA PERSISTENCE & AUDIT STORAGE LAYER", "SQLite • SQLAlchemy ORM • Model Registry (.pt / .joblib) • Encrypted Audit Store", "#ea580c")
    draw_card(4.5, 3.0, 29, 9.8, "Clinical Database (Relational Store)", [
        "• SQLAlchemy ORM Data Layer (SQLite / PostgreSQL)",
        "• User Accounts & Password Hashes (Bcrypt)",
        "• Patient Clinical Demographic Profiles",
        "• Stored Prediction Sessions & Calibrated Probabilities",
        "• Prescribed Intervention Care Regimens"
    ], header_bg="#c2410c")

    draw_card(35.5, 3.0, 29, 9.8, "AI Model Registry & Artifact Store", [
        "• Trained PyTorch MTL Neural Checkpoint (.pt)",
        "• Scikit-learn RobustScaler Serialized Artifact",
        "• Training-Partition Median Imputer Dictionary",
        "• Platt Sigmoid Parameter Calibration Vectors (A, B)",
        "• Baseline Model Checkpoints (XGBoost, RF, LR)"
    ], header_bg="#9a3412")

    draw_card(66.5, 3.0, 29, 9.8, "Audit Trail & Telemetry Logs", [
        "• HIPAA-Compliant Access & Transaction Audit Logs",
        "• Emergency Telemetry SMS / Email Dispatch Records",
        "• Longitudinal Vital Historical Archive",
        "• Model Inference Latency & Performance Telemetry",
        "• System Health & Diagnostic Event Monitoring"
    ], header_bg="#475569")

    # Connectors
    def draw_down_arrow(x, y1, y2, color):
        ax.annotate('', xy=(x, y2), xytext=(x, y1),
                    arrowprops=dict(facecolor=color, edgecolor=color, width=1.5, headwidth=6, headlength=6, shrink=0.08))

    draw_down_arrow(19, 78.5, 76.0, "#0284c7")
    draw_down_arrow(50, 78.5, 76.0, "#0d9488")
    draw_down_arrow(81, 78.5, 76.0, "#7c3aed")

    draw_down_arrow(19, 65.5, 62.5, "#0d9488")
    draw_down_arrow(50, 65.5, 62.5, "#4f46e5")
    draw_down_arrow(81, 65.5, 62.5, "#38bdf8")

    draw_down_arrow(19, 51.0, 48.0, "#6366f1")
    draw_down_arrow(50, 51.0, 48.0, "#9333ea")
    draw_down_arrow(81, 51.0, 48.0, "#a855f7")

    draw_down_arrow(19, 34.5, 31.5, "#16a34a")
    draw_down_arrow(50, 34.5, 31.5, "#0284c7")
    draw_down_arrow(81, 34.5, 31.5, "#dc2626")

    draw_down_arrow(19, 18.5, 15.5, "#ea580c")
    draw_down_arrow(50, 18.5, 15.5, "#ea580c")
    draw_down_arrow(81, 18.5, 15.5, "#ea580c")

    plt.tight_layout()
    
    out_name = "fig_3_1_system_architecture.png" if is_light else "fig_3_1_system_architecture_dark.png"
    out_path = os.path.abspath(os.path.join("artifacts/report_figures", out_name))
    plt.savefig(out_path, dpi=300, facecolor=bg_main, edgecolor='none')
    
    if is_light:
        plt.savefig(os.path.abspath("artifacts/system_architecture_diagram_light.png"), dpi=300, facecolor=bg_main, edgecolor='none')
        plt.savefig(os.path.abspath("system_architecture_diagram.png"), dpi=300, facecolor=bg_main, edgecolor='none')
    else:
        plt.savefig(os.path.abspath("artifacts/system_architecture_diagram_dark.png"), dpi=300, facecolor=bg_main, edgecolor='none')
        
    plt.close()
    print(f"[OK] Generated {theme.upper()} Theme: {out_path}")

if __name__ == "__main__":
    generate_diagram(theme='light')
    generate_diagram(theme='dark')
