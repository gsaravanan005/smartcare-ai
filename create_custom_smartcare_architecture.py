"""
SmartCare AI - Custom Distinctive Publication-Grade System Architecture Diagram
Designed with a unique, high-impact clinical data pipeline layout.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_custom_smartcare_architecture():
    # 16:10 Widescreen High-Resolution Canvas
    fig, ax = plt.subplots(figsize=(16, 10), dpi=300)
    fig.patch.set_facecolor('#f8fafc') # Elegant slate background
    ax.set_facecolor('#f8fafc')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # -------------------------------------------------------------
    # 1. TOP HEADER BANNER
    # -------------------------------------------------------------
    hdr = patches.FancyBboxPatch((2, 91.5), 96, 7.2, boxstyle="round,pad=0.4", ec="#0369a1", fc="#0f172a", lw=1.5)
    ax.add_patch(hdr)
    ax.plot([3, 97], [92.0, 92.0], color="#38bdf8", lw=2)
    
    ax.text(50, 95.8, "SMARTCARE AI — END-TO-END SYSTEM ARCHITECTURE", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#ffffff', fontfamily='sans-serif')
    ax.text(50, 93.3, "Comorbidity-Aware Explainable Multi-Task Learning for Diabetes, Cardiovascular & Kidney Disease Risk Prediction", 
            ha='center', va='center', fontsize=9, fontweight='semibold', color='#7dd3fc', fontfamily='sans-serif')

    # Helper function for drawing styled module containers
    def draw_module_box(x, y, w, h, title, subtitle, hdr_color, bg_color="#ffffff", border_color="#cbd5e1"):
        # Main body
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.35", ec=border_color, fc=bg_color, lw=1.2)
        ax.add_patch(box)
        
        # Header banner
        banner = patches.FancyBboxPatch((x, y + h - 3.2), w, 3.2, boxstyle="round,pad=0.2", ec=hdr_color, fc=hdr_color, lw=1)
        ax.add_patch(banner)
        ax.text(x + w/2, y + h - 1.6, title, ha='center', va='center', fontsize=8, fontweight='bold', color='#ffffff', fontfamily='sans-serif')
        
        # Subtitle below banner
        if subtitle:
            ax.text(x + w/2, y + h - 4.5, subtitle, ha='center', va='center', fontsize=6.5, fontstyle='italic', color='#64748b', fontfamily='sans-serif')

    # Helper for bullet points inside cards
    def draw_bullet_list(x, start_y, items, line_gap=1.5, bullet_color='#0284c7'):
        curr_y = start_y
        for text in items:
            ax.plot(x + 0.8, curr_y + 0.2, marker='o', markersize=3, color=bullet_color)
            ax.text(x + 1.8, curr_y, text, fontsize=6.8, color='#1e293b', fontfamily='sans-serif', va='center')
            curr_y -= line_gap

    # Helper for inner sub-cards
    def draw_subcard(x, y, w, h, title, details, bg_col='#f1f5f9', border_col='#cbd5e1', title_col='#0f172a'):
        sc = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2", ec=border_col, fc=bg_col, lw=0.9)
        ax.add_patch(sc)
        ax.text(x + w/2, y + h - 1.2, title, ha='center', va='center', fontsize=7.2, fontweight='bold', color=title_col, fontfamily='sans-serif')
        
        cy = y + h - 2.5
        for d in details:
            ax.text(x + 0.8, cy, d, fontsize=6.2, color='#334155', fontfamily='sans-serif')
            cy -= 1.15

    # -------------------------------------------------------------
    # 2. COLUMN 1: CLINICAL DATA INGESTION & HARMONIZATION (Left, x: 2 to 24)
    # -------------------------------------------------------------
    draw_module_box(2, 6, 22.5, 83.5, "1. DATA INGESTION & HARMONIZATION", "Cross-Cohort Aggregation & Preprocessing", "#0284c7")
    
    # Cohort Data Sources
    draw_subcard(3.2, 70, 20.1, 14, "Multi-Cohort Clinical Sources", [
        "• CDC BRFSS (70,692 Epidemiological Recs)",
        "• Kaggle CVD (68,205 Vascular Recs)",
        "• UCI CKD (400 Renal Biomarker Recs)",
        "• Total Unified Dataset: 139,297 Records"
    ], bg_col='#eff6ff', border_col='#93c5fd', title_col='#1e40af')

    # Preprocessing Pipeline
    draw_subcard(3.2, 45, 20.1, 23, "Zero-Leakage Preprocessing", [
        "• Missing Value Imputation:",
        "  - Training-Partition Fitted Median",
        "  - Zero Cross-Split Information Leakage",
        "• Normalization & Scaling:",
        "  - Outlier-Resilient RobustScaler",
        "• Task-Balanced Sampling:",
        "  - 20% Allocation for Data-Scarce CKD",
        "• 80:20 Stratified Train-Test Split"
    ], bg_col='#f0fdf4', border_col='#86efac', title_col='#166534')

    # 30-D Harmonized Vector
    draw_subcard(3.2, 8, 20.1, 35, "30-D Harmonized Clinical Vector", [
        "Demographics & Vitals (1-6):",
        "• Age, Sex, SBP, DBP, Heart Rate, BMI",
        "",
        "Biochemical & Lipid Labs (7-13):",
        "• Fasting Glucose, HbA1c, Total Chol,",
        "  HDL, Triglycerides, Creatinine, BUN",
        "",
        "Renal, History & Lifestyle (14-27):",
        "• Albuminuria, Hb, K+, Smoking, Diet,",
        "  Family Hx T2D/CVD, HTN, GenHealth",
        "",
        "Derived Hemodynamic Indices (28-30):",
        "• Pulse Pressure, MAP, CKD-EPI eGFR"
    ], bg_col='#fdf4ff', border_col='#f0abfc', title_col='#86198f')

    # -------------------------------------------------------------
    # 3. COLUMN 2: MULTI-TASK DEEP NEURAL BACKBONE (Middle-Left, x: 26.5 to 50)
    # -------------------------------------------------------------
    draw_module_box(26.5, 6, 23.5, 83.5, "2. MULTI-TASK NEURAL NETWORK", "Shared Latent Representation & Task Heads", "#6366f1")

    # Shared Encoder Box
    draw_subcard(27.8, 62, 20.9, 22, "Shared Feature Neural Encoder", [
        "• Input: 30 Standardized Features",
        "• Dense Layer 1: 30 → 64 Units (ReLU)",
        "• Regularization & Stability:",
        "  - Layer Normalization (gamma, beta)",
        "  - Dropout Regularization (p = 0.15)",
        "• Dense Layer 2: 64 → 32 Bottleneck",
        "• Shared Latent Space (Z ∈ R^32):",
        "  - Joint Cardiorenal-Metabolic Embedding"
    ], bg_col='#e0e7ff', border_col='#818cf8', title_col='#312e81')

    # Multi-Task Parallel Heads
    draw_subcard(27.8, 26, 20.9, 34, "Dedicated Diagnostic Task Heads", [
        "T2D Head (Type 2 Diabetes):",
        "• Dense(32 → 16 → 1) + Sigmoid",
        "• ROC-AUC: 0.8276 | Recall: 88.72%",
        "• F1-Score: 0.7751 | PR-AUC: 0.8038",
        "",
        "CVD Head (Cardiovascular Disease):",
        "• Dense(32 → 16 → 1) + Sigmoid",
        "• ROC-AUC: 0.7974 | Recall: 79.13%",
        "• F1-Score: 0.7306 | PR-AUC: 0.7829",
        "",
        "CKD Head (Chronic Kidney Disease):",
        "• Dense(32 → 16 → 1) + Sigmoid",
        "• ROC-AUC: 0.9953 | Recall: 94.59%",
        "• F1-Score: 0.9589 | PR-AUC: 0.9971"
    ], bg_col='#f5f3ff', border_col='#c4b5fd', title_col='#4c1d95')

    # Multi-Task Loss Optimization
    draw_subcard(27.8, 8, 20.9, 16.5, "Task-Masked Loss Function", [
        "• Joint Objective:",
        "  L_total = Σ_t I(y_t) * w_t * L_BCE(y_t, ŷ_t)",
        "• Cross-Task Gradient Sharing",
        "• Fast Inference Latency: < 12ms"
    ], bg_col='#fef2f2', border_col='#fca5a5', title_col='#991b1b')

    # -------------------------------------------------------------
    # 4. COLUMN 3: CALIBRATION, EXPLAINABILITY & RULES (Middle-Right, x: 52 to 74.5)
    # -------------------------------------------------------------
    draw_module_box(52, 6, 22.5, 83.5, "3. CALIBRATION, XAI & RULES ENGINE", "Trustworthy Post-Processing & Guidelines", "#0d9488")

    # Platt Sigmoid Calibration
    draw_subcard(53.2, 65, 20.1, 19, "Probability Calibration Subsystem", [
        "• Post-Hoc Platt Sigmoid Scaling:",
        "  P(y=1|z) = 1 / (1 + exp(A*z + B))",
        "• Minimizes Expected Calibration Error:",
        "  - T2D: 0.0108 | CVD: 0.0089 | CKD: 0.0042",
        "• Brier Score Optimization (< 0.18)",
        "• Calibrated Clinical Risk Tiers (Low/Mod/High)"
    ], bg_col='#fff7ed', border_col='#fdba74', title_col='#9a3412')

    # SHAP Explainability Engine
    draw_subcard(53.2, 37, 20.1, 26, "Explainable AI (SHAP) Engine", [
        "• Game-Theoretic TreeSHAP & KernelSHAP",
        "• Additive Feature Attribution:",
        "  f(x) = φ_0 + Σ_i φ_i",
        "• Patient-Level Waterfall Plots:",
        "  - Positive Drivers (+SBP, +Glucose, +BMI)",
        "  - Negative Drivers (-Exercise, -HDL)",
        "• Global Cohort Biomarker Importance",
        "• Direct Clinical Verification & Trust"
    ], bg_col='#ecfeff', border_col='#67e8f9', title_col='#155e75')

    # Clinical Guidelines Rules Engine
    draw_subcard(53.2, 8, 20.1, 27.5, "Deterministic Clinical Rules", [
        "• American Diabetes Association (ADA 2026):",
        "  - Target HbA1c < 7.0%, Low Glycemic Diet",
        "• ACC/AHA 2026 Cardiovascular Guidelines:",
        "  - Blood Pressure Goal < 130/80 mmHg",
        "  - Statin / Lipid Lowering Review",
        "• KDIGO 2026 Nephrology Protocols:",
        "  - Proteinuria Staging & SGLT2i / ACEi Review",
        "• Personalized Exercise & Nutrition Plans"
    ], bg_col='#f0fdf4', border_col='#86efac', title_col='#14532d')

    # -------------------------------------------------------------
    # 5. COLUMN 4: FASTAPI GATEWAY, UI & TELEMETRY (Right, x: 76.5 to 98)
    # -------------------------------------------------------------
    draw_module_box(76.5, 6, 21.5, 83.5, "4. PRESENTATION, API & TELEMETRY", "Microservices, Dashboards & Alerting", "#0f766e")

    # FastAPI Gateway & Security
    draw_subcard(77.7, 68, 19.1, 16, "FastAPI Microservice Layer", [
        "• High-Performance Async REST Gateway",
        "• Endpoints: /predict, /explain, /alerts",
        "• OAuth2 with JWT Bearer Authentication",
        "• Role-Based Access Control (Doctor/Patient)",
        "• SQLAlchemy ORM + SQLite / PostgreSQL"
    ], bg_col='#f8fafc', border_col='#cbd5e1', title_col='#0f172a')

    # Interactive Frontend Dashboards
    draw_subcard(77.7, 43, 19.1, 23.5, "React 18.2 Clinical Dashboards", [
        "• Clinician Workstation:",
        "  - Patient Roster, SHAP Waterfall Plot,",
        "  - Comorbidity Risk Gauges, Lab Trends",
        "• Patient Wellness Portal:",
        "  - Risk Score Summary & Lifestyle Goals",
        "• Multilingual Conversational Copilot:",
        "  - English, Tamil, Hindi & Spanish NLP",
        "• Tailored Vernacular Health Guidance"
    ], bg_col='#eff6ff', border_col='#93c5fd', title_col='#1d4ed8')

    # Telemetry & Emergency Alert Dispatcher
    draw_subcard(77.7, 8, 19.1, 33.5, "Longitudinal Telemetry & Alerts", [
        "• Continuous Vital Sign Tracking:",
        "  - Blood Pressure, Glucose, eGFR, Weight",
        "• Health Trajectory Rate-of-Change",
        "• Acute Threshold Crisis Detection:",
        "  - Hypertensive Crisis (SBP ≥ 180 mmHg)",
        "  - Hyperglycemic Emergency (FBS ≥ 300)",
        "• Automated Alert Dispatcher:",
        "  - Real-Time Twilio SMS Gateway",
        "  - SMTP Clinical Summary Email",
        "  - Physician Emergency Notification"
    ], bg_col='#fef2f2', border_col='#fca5a5', title_col='#991b1b')

    # -------------------------------------------------------------
    # 6. DATA FLOW CONNECTORS & ARROWS (Between Columns)
    # -------------------------------------------------------------
    def draw_connecting_arrow(x1, y1, x2, y2, color, label=""):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(facecolor=color, edgecolor=color, width=1.5, headwidth=6, headlength=6, shrink=0.02))
        if label:
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            ax.text(mid_x, mid_y + 0.8, label, ha='center', va='bottom', fontsize=5.8, fontweight='bold', color=color, fontfamily='sans-serif',
                    bbox=dict(boxstyle="round,pad=0.15", facecolor="#ffffff", edgecolor=color, lw=0.6))

    # Col 1 -> Col 2 (Vector -> Shared Encoder)
    draw_connecting_arrow(24.5, 75, 26.5, 75, "#0284c7", "Harmonized Data")
    draw_connecting_arrow(24.5, 25, 26.5, 25, "#6366f1", "30-D Vector (X)")

    # Col 2 -> Col 3 (Task Heads -> Calibration & SHAP)
    draw_connecting_arrow(50.0, 75, 52.0, 75, "#6366f1", "Raw Logits (z)")
    draw_connecting_arrow(50.0, 50, 52.0, 50, "#0d9488", "Latent Z + Weights")
    draw_connecting_arrow(50.0, 20, 52.0, 20, "#0d9488", "Predictions (ŷ)")

    # Col 3 -> Col 4 (Calibrated Scores, SHAP & Rules -> API Gateway & UI)
    draw_connecting_arrow(74.5, 75, 76.5, 75, "#0f766e", "Calibrated (P)")
    draw_connecting_arrow(74.5, 50, 76.5, 50, "#0284c7", "SHAP Attributions (φ)")
    draw_connecting_arrow(74.5, 25, 76.5, 25, "#dc2626", "Care Plans & Alerts")

    # Save outputs in multiple formats and locations
    out_dir = os.path.abspath("artifacts/report_figures")
    os.makedirs(out_dir, exist_ok=True)
    
    out_1 = os.path.join(out_dir, "fig_3_1_system_architecture.png")
    out_2 = os.path.abspath("artifacts/smartcare_ai_system_architecture.png")
    out_3 = os.path.abspath("smartcare_ai_system_architecture.png")
    
    plt.tight_layout()
    plt.savefig(out_1, dpi=300, facecolor='#f8fafc', bbox_inches='tight')
    plt.savefig(out_2, dpi=300, facecolor='#f8fafc', bbox_inches='tight')
    plt.savefig(out_3, dpi=300, facecolor='#f8fafc', bbox_inches='tight')
    plt.close()
    
    print(f"[SUCCESS] Custom SmartCare AI System Architecture Diagram generated:")
    print(f"  -> {out_1}")
    print(f"  -> {out_2}")
    print(f"  -> {out_3}")

if __name__ == "__main__":
    generate_custom_smartcare_architecture()
