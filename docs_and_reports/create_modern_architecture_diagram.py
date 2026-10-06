"""
SmartCare AI - Publication-Grade Modern System Architecture Diagram Generator
Generates a high-definition (300 DPI) multi-tier system architecture diagram.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

def generate_system_architecture_diagram():
    fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
    fig.patch.set_facecolor('#0b1120') # Deep Slate Navy
    ax.set_facecolor('#0b1120')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # -------------------------------------------------------------
    # 1. HEADER BANNER
    # -------------------------------------------------------------
    header_box = patches.FancyBboxPatch(
        (3, 91), 94, 7,
        boxstyle="round,pad=0.5",
        ec="#1e293b", fc="#0f172a", lw=1.5
    )
    ax.add_patch(header_box)
    
    # Glow accent line
    ax.plot([4, 96], [91.2, 91.2], color="#0284c7", lw=2.5, solid_capstyle='round')
    
    ax.text(50, 95.2, "SMARTCARE AI — SYSTEM ARCHITECTURE DIAGRAM", 
            ha='center', va='center', fontsize=15, fontweight='bold', color='#ffffff', fontfamily='sans-serif')
    ax.text(50, 92.5, "Comorbidity-Aware Explainable Multi-Task Learning Clinical Decision Support Ecosystem (T2D • CVD • CKD)", 
            ha='center', va='center', fontsize=9.5, fontweight='semibold', color='#38bdf8', fontfamily='sans-serif')

    # Helper function for drawing rounded tier containers
    def draw_tier_container(x, y, w, h, title, subtitle, badge_color, border_color="#1e293b", bg_color="#0f172a"):
        container = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4", ec=border_color, fc=bg_color, lw=1.2)
        ax.add_patch(container)
        
        # Tier Title Badge
        badge = patches.FancyBboxPatch((x + 1.2, y + h - 2.8), len(title)*0.95 + 2, 2.2, boxstyle="round,pad=0.2", ec=badge_color, fc=badge_color, lw=1)
        ax.add_patch(badge)
        ax.text(x + 2.2, y + h - 1.7, title, fontsize=8, fontweight='bold', color='#ffffff', fontfamily='sans-serif')
        
        # Subtitle
        ax.text(x + len(title)*0.95 + 4.5, y + h - 1.7, subtitle, fontsize=7.5, color='#94a3b8', fontfamily='sans-serif')

    # Helper function for component cards
    def draw_card(x, y, w, h, title, items, header_bg="#1e293b", body_bg="#131e36", border_color="#334155", title_color="#38bdf8"):
        # Body
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", ec=border_color, fc=body_bg, lw=1)
        ax.add_patch(card)
        
        # Header banner
        hdr = patches.FancyBboxPatch((x, y + h - 2.6), w, 2.6, boxstyle="round,pad=0.2", ec=border_color, fc=header_bg, lw=1)
        ax.add_patch(hdr)
        ax.text(x + w/2, y + h - 1.3, title, ha='center', va='center', fontsize=7.5, fontweight='bold', color=title_color, fontfamily='sans-serif')
        
        # Items
        line_y = y + h - 3.8
        for item in items:
            ax.text(x + 1.0, line_y, item, fontsize=6.5, color='#e2e8f0', fontfamily='sans-serif')
            line_y -= 1.4

    # -------------------------------------------------------------
    # 2. TIER 1: CLIENT PRESENTATION TIER (y: 77 to 89)
    # -------------------------------------------------------------
    draw_tier_container(3, 77.5, 94, 12, "TIER 1: CLIENT PRESENTATION LAYER", "React 18.2 • TailwindCSS • Responsive Dashboard • Vite", "#0284c7")
    
    draw_card(4.5, 78.5, 29, 8.2, "Patient Portal (Wellness UI)", [
        "• Interactive 3-Disease Risk Score Gauges",
        "• Longitudinal Vitals & Glucose Telemetry",
        "• ADA/ACC/KDIGO Lifestyle Interventions",
        "• Vernacular Localization (Tamil/Hindi/ES)"
    ], header_bg="#0369a1", title_color="#ffffff")

    draw_card(35.5, 78.5, 29, 8.2, "Clinician Clinical Workstation", [
        "• Multi-Patient Triage Roster & EHR Dossiers",
        "• Interactive SHAP Waterfall Biomarker Plots",
        "• Calibrated Probability Risk Categorization",
        "• Pharmacological Contraindication Review"
    ], header_bg="#0f766e", title_color="#ffffff")

    draw_card(66.5, 78.5, 29, 8.2, "Conversational Clinical Copilot", [
        "• Multilingual NLP Chatbot (4 Languages)",
        "• Real-Time Medical Report Interpretation",
        "• Context-Aware Dietary & Exercise Guidance",
        "• Medication Adherence Counseling Daemon"
    ], header_bg="#7c3aed", title_color="#ffffff")

    # -------------------------------------------------------------
    # 3. TIER 2: API GATEWAY & SECURITY TIER (y: 65 to 75.5)
    # -------------------------------------------------------------
    draw_tier_container(3, 64.5, 94, 11.5, "TIER 2: API GATEWAY & SECURITY LAYER", "FastAPI (Async Python 3.13) • Uvicorn • JWT • RBAC", "#0d9488")
    
    draw_card(4.5, 65.5, 29, 7.8, "FastAPI REST Gateway", [
        "• High-Performance Asynchronous Endpoints",
        "• /predict, /explain, /intervention, /alerts",
        "• OpenAPI / Swagger Auto-Documentation",
        "• CORS & Rate Limiting Middleware"
    ], header_bg="#134e4a", title_color="#5eead4")

    draw_card(35.5, 65.5, 29, 7.8, "Authentication & Security Subsystem", [
        "• OAuth2 with JWT Bearer Access Tokens",
        "• Bcrypt Password Hashing with Salt",
        "• Role-Based Access Control (Patient/Doctor)",
        "• End-to-End TLS Encryption & HIPAA Guards"
    ], header_bg="#1e293b", title_color="#38bdf8")

    draw_card(66.5, 65.5, 29, 7.8, "Validation & Ingestion Pipeline", [
        "• Strict Pydantic Data Schema Validation",
        "• Clinical Out-of-Bounds Range Rejection",
        "• Dynamic Hemodynamic Derived Indicators",
        "• Structured JSON Audit Trail Telemetry"
    ], header_bg="#312e81", title_color="#c7d2fe")

    # -------------------------------------------------------------
    # 4. TIER 3: DATA HARMONIZATION & PREPROCESSING (y: 50.5 to 62.5)
    # -------------------------------------------------------------
    draw_tier_container(3, 50.0, 94, 12.5, "TIER 3: DATA INGESTION & CROSS-COHORT HARMONIZATION", "CDC BRFSS • Kaggle CVD • UCI CKD (139,297 Multi-Cohort Records)", "#4f46e5")
    
    draw_card(4.5, 51.0, 29, 8.8, "Multi-Cohort Clinical Data Ingestion", [
        "• CDC BRFSS 2015 Survey (N = 70,692)",
        "• Kaggle Cardiovascular Cohort (N = 68,205)",
        "• UCI Chronic Kidney Dataset (N = 400)",
        "• Heterogeneous Feature Schema Mapping"
    ], header_bg="#3730a3", title_color="#e0e7ff")

    draw_card(35.5, 51.0, 29, 8.8, "Zero-Leakage Preprocessing Engine", [
        "• Training-Partition Fitted Median Imputation",
        "• RobustScaler Outlier-Resilient Normalization",
        "• Task-Balanced Sampling (20% CKD Allocation)",
        "• 80:20 Stratified Train-Test Separation"
    ], header_bg="#1e1b4b", title_color="#a5b4fc")

    draw_card(66.5, 51.0, 29, 8.8, "30-D Standardized Clinical Vector", [
        "• Vitals: SBP, DBP, Heart Rate, BMI (15-50)",
        "• Labs: FBS, HbA1c, Chol, HDL, Trig, Creat, BUN",
        "• Lifestyle & Medical History: Smoking, HTN, Diet",
        "• Computed: Pulse Pressure, MAP, CKD-EPI eGFR"
    ], header_bg="#0f172a", title_color="#38bdf8")

    # -------------------------------------------------------------
    # 5. TIER 4: MULTI-TASK NEURAL NETWORK ENGINE (y: 33.5 to 48)
    # -------------------------------------------------------------
    draw_tier_container(3, 33.5, 94, 14.5, "TIER 4: COMORBIDITY-AWARE MULTI-TASK LEARNING ENGINE", "PyTorch • Shared Latent Representation • Task-Masked Loss Optimization", "#9333ea")
    
    draw_card(4.5, 34.5, 29, 10.5, "Shared Feature Neural Encoder", [
        "• Input Layer: 30 Harmonized Clinical Features",
        "• Dense Layer 1: 30 → 64 Units (ReLU)",
        "• Layer Normalization + Dropout (p = 0.15)",
        "• Dense Layer 2: 64 → 32 Latent Bottleneck",
        "• Joint Cardiorenal-Metabolic Representation",
        "• Cross-Task Inductive Knowledge Transfer"
    ], header_bg="#581c87", title_color="#f3e8ff")

    draw_card(35.5, 34.5, 29, 10.5, "Task-Specific Diagnostic Heads", [
        "• Type 2 Diabetes Head: Dense(32→16→1)",
        "  - ROC-AUC: 0.8276 | Recall: 88.72% | F1: 0.7751",
        "• Cardiovascular Disease Head: Dense(32→16→1)",
        "  - ROC-AUC: 0.7974 | Recall: 79.13% | F1: 0.7306",
        "• Chronic Kidney Disease Head: Dense(32→16→1)",
        "  - ROC-AUC: 0.9953 | Recall: 94.59% | F1: 0.9589",
        "• Simultaneous Forward Inference in < 12ms"
    ], header_bg="#701a75", title_color="#fdf4ff")

    draw_card(66.5, 34.5, 29, 10.5, "Calibration & Explainability (XAI)", [
        "• Post-Hoc Platt Sigmoid Calibration Engine",
        "  - Logit-to-Posterior Mapping (ECE < 0.011)",
        "• Game-Theoretic SHAP Engine (Tree & Kernel)",
        "  - Exact Shapley Feature Attribution (phi_i)",
        "  - Local Patient Risk Waterfall Decomposition",
        "  - Global Cohort Biomarker Importance Hierarchy"
    ], header_bg="#831843", title_color="#fce7f3")

    # -------------------------------------------------------------
    # 6. TIER 5 & 6: CLINICAL RULES, TELEMETRY & PERSISTENCE (y: 2 to 31.5)
    # -------------------------------------------------------------
    draw_tier_container(3, 17.5, 94, 14.0, "TIER 5: CLINICAL DECISION SUPPORT & TELEMETRY DISPATCHER", "ADA 2026 • ACC/AHA 2026 • KDIGO 2026 Guidelines • Twilio SMS API", "#16a34a")
    
    draw_card(4.5, 18.5, 29, 10.2, "Clinical Guidelines Rules Engine", [
        "• ADA 2026 Standards: Glycemic Targets & Meds",
        "• ACC/AHA 2026: Lipid Management & BP Control",
        "• KDIGO 2026: eGFR Staging & Proteinuria Care",
        "• Automated Personalized Dietary Care Plans",
        "• Aerobic & Resistance Physical Prescriptions",
        "• Pharmacological Contraindication Warnings"
    ], header_bg="#14532d", title_color="#bbf7d0")

    draw_card(35.5, 18.5, 29, 10.2, "Longitudinal Vital Tracker & Telemetry", [
        "• Continuous Time-Series Vital Signs Log",
        "• SBP, DBP, Fasting Blood Sugar, Body Weight",
        "• Historical Trend Velocity & Rate-of-Change",
        "• Micro-Level Health Trajectory Projection",
        "• Interactive Multi-Axis Trend Visualization",
        "• Routine Check-Up & Screening Reminders"
    ], header_bg="#1e3a5f", title_color="#93c5fd")

    draw_card(66.5, 18.5, 29, 10.2, "Emergency Alert & Crisis Dispatcher", [
        "• Real-Time Critical Breach Detection Daemon",
        "  - Hypertensive Crisis (SBP >= 180 mmHg)",
        "  - Severe Hyperglycemia (FBS >= 300 mg/dL)",
        "• Automated Twilio SMS Emergency Broadcast",
        "• Structured Clinical Summary Email Dispatch",
        "• Nearest Emergency Center Geo-Routing"
    ], header_bg="#7f1d1d", title_color="#fecaca")

    # -------------------------------------------------------------
    # 7. TIER 6: PERSISTENCE & STORAGE (y: 2 to 15.5)
    # -------------------------------------------------------------
    draw_tier_container(3, 2.0, 94, 13.5, "TIER 6: DATA PERSISTENCE & AUDIT STORAGE LAYER", "SQLite • SQLAlchemy ORM • Model Registry (.pt / .joblib) • Encrypted Audit Store", "#ea580c")
    
    draw_card(4.5, 3.0, 29, 9.8, "Clinical Database (Relational Store)", [
        "• SQLAlchemy ORM Data Layer (SQLite / PostgreSQL)",
        "• User Accounts & Password Hashes (Bcrypt)",
        "• Patient Clinical Demographic Profiles",
        "• Stored Prediction Sessions & Calibrated Probabilities",
        "• Prescribed Intervention Care Regimens"
    ], header_bg="#7c2d12", title_color="#fed7aa")

    draw_card(35.5, 3.0, 29, 9.8, "AI Model Registry & Artifact Store", [
        "• Trained PyTorch MTL Neural Checkpoint (.pt)",
        "• Scikit-learn RobustScaler Serialized Artifact",
        "• Training-Partition Median Imputer Dictionary",
        "• Platt Sigmoid Parameter Calibration Vectors (A, B)",
        "• Baseline Model Checkpoints (XGBoost, RF, LR)"
    ], header_bg="#431407", title_color="#ffedd5")

    draw_card(66.5, 3.0, 29, 9.8, "Audit Trail & Telemetry Logs", [
        "• HIPAA-Compliant Access & Transaction Audit Logs",
        "• Emergency Telemetry SMS / Email Dispatch Records",
        "• Longitudinal Vital Historical Archive",
        "• Model Inference Latency & Performance Telemetry",
        "• System Health & Diagnostic Event Monitoring"
    ], header_bg="#1c1917", title_color="#f5f5f4")

    # -------------------------------------------------------------
    # 8. DATA FLOW CONNECTORS (INTER-TIER ARROWS)
    # -------------------------------------------------------------
    def draw_down_arrow(x, y1, y2, color="#0284c7"):
        ax.annotate('', xy=(x, y2), xytext=(x, y1),
                    arrowprops=dict(facecolor=color, edgecolor=color, width=1.5, headwidth=6, headlength=6, shrink=0.08))

    def draw_up_arrow(x, y1, y2, color="#10b981"):
        ax.annotate('', xy=(x, y2), xytext=(x, y1),
                    arrowprops=dict(facecolor=color, edgecolor=color, width=1.5, headwidth=6, headlength=6, shrink=0.08))

    # T1 to T2 (Client -> Gateway)
    draw_down_arrow(19, 78.5, 76.0, "#0284c7")
    draw_down_arrow(50, 78.5, 76.0, "#0f766e")
    draw_down_arrow(81, 78.5, 76.0, "#7c3aed")

    # T2 to T3 (Gateway -> Harmonization)
    draw_down_arrow(19, 65.5, 62.5, "#0d9488")
    draw_down_arrow(50, 65.5, 62.5, "#4f46e5")
    draw_down_arrow(81, 65.5, 62.5, "#38bdf8")

    # T3 to T4 (Harmonized Vector -> Neural MTL)
    draw_down_arrow(19, 51.0, 48.0, "#6366f1")
    draw_down_arrow(50, 51.0, 48.0, "#9333ea")
    draw_down_arrow(81, 51.0, 48.0, "#a855f7")

    # T4 to T5 (MTL & Calibration -> Clinical Rules & Telemetry)
    draw_down_arrow(19, 34.5, 31.5, "#16a34a")
    draw_down_arrow(50, 34.5, 31.5, "#2563eb")
    draw_down_arrow(81, 34.5, 31.5, "#dc2626")

    # T5 to T6 (Rules & Telemetry -> Persistence)
    draw_down_arrow(19, 18.5, 15.5, "#ea580c")
    draw_down_arrow(50, 18.5, 15.5, "#f97316")
    draw_down_arrow(81, 18.5, 15.5, "#ef4444")

    # Save High-Resolution Image
    out_dir = os.path.abspath("artifacts/report_figures")
    os.makedirs(out_dir, exist_ok=True)
    
    out_path_1 = os.path.join(out_dir, "fig_3_1_system_architecture.png")
    out_path_2 = os.path.abspath("artifacts/system_architecture_diagram.png")
    out_path_3 = os.path.abspath("system_architecture_diagram.png")
    
    plt.tight_layout()
    plt.savefig(out_path_1, dpi=300, facecolor='#0b1120', edgecolor='none')
    plt.savefig(out_path_2, dpi=300, facecolor='#0b1120', edgecolor='none')
    plt.savefig(out_path_3, dpi=300, facecolor='#0b1120', edgecolor='none')
    plt.close()
    
    print(f"[SUCCESS] System Architecture Diagram generated successfully:")
    print(f"  -> {out_path_1}")
    print(f"  -> {out_path_2}")
    print(f"  -> {out_path_3}")

if __name__ == "__main__":
    generate_system_architecture_diagram()
