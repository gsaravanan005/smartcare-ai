"""
SmartCare AI - Publication-Grade Architecture Diagram Generator
Complete Dual-Path Flowchart:
  (a) Inference Path: Real-time Patient Intake/Sensors -> Validation Gate -> Harmonized Preprocessing ->
      Shared Latent Encoder -> Multi-Task Prediction & Calibration -> SHAP Explainability & Clinical Interventions.
  (b) Offline Training & Model Selection: Multi-Cohort Harmonization -> Task-Balanced Imputation ->
      Joint Multi-Task Optimization -> Baseline Benchmarking -> Held-Out Test Evaluation -> Production Checkpoint.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_rich_icon_architecture_diagram():
    # 16.0 x 11.5 inches Canvas at 300 DPI for high-resolution clarity
    fig, ax = plt.subplots(figsize=(16.0, 11.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    f_family = 'sans-serif'
    
    # -------------------------------------------------------------
    # 1. COLUMN TITLES
    # -------------------------------------------------------------
    ax.text(26.5, 97.2, "(a) Inference path", ha='center', va='center', fontsize=14, fontweight='bold', color='#0f172a', fontfamily=f_family)
    ax.text(76.5, 97.2, "(b) Offline training and model selection", ha='center', va='center', fontsize=14, fontweight='bold', color='#0f172a', fontfamily=f_family)

    # Helper function for drawing custom vector icons
    def draw_vector_icon(x, y, icon_type, color='#0284c7'):
        bg_circle = patches.Circle((x, y), 1.65, edgecolor=color, facecolor='#f8fafc', lw=1.3)
        ax.add_patch(bg_circle)
        
        if icon_type == 'screen': # 1a: Form/Web Screen
            r = patches.Rectangle((x-0.85, y-0.65), 1.7, 1.2, fill=False, edgecolor=color, lw=1.1)
            ax.add_patch(r)
            ax.plot([x-0.55, x+0.55], [y+0.2, y+0.2], color=color, lw=0.9)
            ax.plot([x-0.55, x+0.25], [y-0.2, y-0.2], color=color, lw=0.9)
            ax.plot([x-0.35, x+0.35], [y-0.95, y-0.95], color=color, lw=1.1)
            ax.plot([x, x], [y-0.65, y-0.95], color=color, lw=1.1)
            
        elif icon_type == 'pulse': # 1b: Sensor / Pulse Wave
            w_r = patches.Rectangle((x-0.55, y-0.75), 1.1, 1.5, fill=False, edgecolor=color, lw=1.1)
            ax.add_patch(w_r)
            ax.plot([x-0.45, x-0.2, x-0.05, x+0.15, x+0.3, x+0.45], [y, y, y+0.45, y-0.45, y, y], color=color, lw=1.0)
            
        elif icon_type == 'shield': # 2: Validation Shield
            ax.text(x, y, "✓", ha='center', va='center', fontsize=11, fontweight='bold', color=color)
            
        elif icon_type == 'gear': # 3: Preprocessing
            ax.text(x, y, "⚙", ha='center', va='center', fontsize=12, fontweight='bold', color=color)
            
        elif icon_type == 'neural': # 4: Neural Network Node Graph
            ax.plot(x-0.65, y+0.45, marker='o', markersize=2.8, color=color)
            ax.plot(x-0.65, y-0.45, marker='o', markersize=2.8, color=color)
            ax.plot(x, y+0.65, marker='o', markersize=2.8, color=color)
            ax.plot(x, y, marker='o', markersize=2.8, color=color)
            ax.plot(x, y-0.65, marker='o', markersize=2.8, color=color)
            ax.plot(x+0.65, y+0.35, marker='o', markersize=2.8, color=color)
            ax.plot(x+0.65, y-0.35, marker='o', markersize=2.8, color=color)
            for y1 in [y+0.45, y-0.45]:
                for y2 in [y+0.65, y, y-0.65]:
                    ax.plot([x-0.65, x], [y1, y2], color=color, lw=0.45, alpha=0.7)
            for y2 in [y+0.65, y, y-0.65]:
                for y3 in [y+0.35, y-0.35]:
                    ax.plot([x, x+0.65], [y2, y3], color=color, lw=0.45, alpha=0.7)
                    
        elif icon_type == 'sliders': # 5: Task Heads & Calibration
            for off in [-0.45, 0, 0.45]:
                ax.plot([x+off, x+off], [y-0.65, y+0.65], color=color, lw=0.85)
            ax.plot(x-0.45, y+0.25, marker='s', markersize=3, color=color)
            ax.plot(x, y-0.2, marker='s', markersize=3, color=color)
            ax.plot(x+0.45, y+0.35, marker='s', markersize=3, color=color)
            
        elif icon_type == 'chart': # 6: Waterfall / Risk Chart
            ax.plot([x-0.75, x-0.75, x+0.75], [y+0.65, y-0.65, y-0.65], color=color, lw=0.9)
            ax.add_patch(patches.Rectangle((x-0.55, y-0.65), 0.28, 0.55, color=color))
            ax.add_patch(patches.Rectangle((x-0.12, y-0.65), 0.28, 0.95, color=color))
            ax.add_patch(patches.Rectangle((x+0.28, y-0.65), 0.28, 0.38, color=color))
            
        elif icon_type == 'cross': # 7: Clinical Action
            ax.plot([x-0.55, x+0.55], [y, y], color=color, lw=2.2, solid_capstyle='round')
            ax.plot([x, x], [y-0.55, y+0.55], color=color, lw=2.2, solid_capstyle='round')
            
        elif icon_type == 'db': # Col B: Database
            for dy in [0.35, 0, -0.35]:
                cyl = patches.Ellipse((x, y+dy), 1.2, 0.45, fill=False, edgecolor=color, lw=0.9)
                ax.add_patch(cyl)
            ax.plot([x-0.6, x-0.6], [y-0.35, y+0.35], color=color, lw=0.9)
            ax.plot([x+0.6, x+0.6], [y-0.35, y+0.35], color=color, lw=0.9)
            
        elif icon_type == 'scale': # Col B: Balance
            ax.text(x, y, "⚖", ha='center', va='center', fontsize=11, fontweight='bold', color=color)
            
        elif icon_type == 'lightning': # Col B: Training
            ax.text(x, y, "⚡", ha='center', va='center', fontsize=11, fontweight='bold', color=color)
            
        elif icon_type == 'grid': # Col B: Benchmark
            ax.text(x, y, "▦", ha='center', va='center', fontsize=11, fontweight='bold', color=color)
            
        elif icon_type == 'target': # Col B: Evaluation
            c_out = patches.Circle((x, y), 0.7, fill=False, edgecolor=color, lw=0.9)
            c_in = patches.Circle((x, y), 0.3, fill=True, color=color)
            ax.add_patch(c_out)
            ax.add_patch(c_in)
            
        elif icon_type == 'star': # Col B: Selected Model
            ax.text(x, y, "★", ha='center', va='center', fontsize=12, fontweight='bold', color=color)

    # Helper function for drawing rich cards with icon and bullets
    def draw_rich_card(x, y, w, h, icon_type, icon_color, title, bullets, is_gray=False, is_dashed=False, bullet_fs=6.8, line_spacing=1.75):
        bg = '#f8fafc' if is_gray else '#ffffff'
        ls = '--' if is_dashed else '-'
        border_col = '#64748b' if is_gray else '#0f172a'
        
        # Container Box
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.25", linewidth=1.3, edgecolor=border_col, facecolor=bg, linestyle=ls)
        ax.add_patch(rect)
        
        # Icon
        ic_x = x + 2.6
        ic_y = y + h - 2.4
        draw_vector_icon(ic_x, ic_y, icon_type, icon_color)
        
        # Title
        ax.text(x + 5.0, y + h - 2.4, title, fontsize=9.2, fontweight='bold', color='#0f172a', fontfamily=f_family, va='center')
        
        # Bullets
        start_by = y + h - 4.4
        for b in bullets:
            ax.text(x + 1.8, start_by, b, fontsize=bullet_fs, color='#334155', fontfamily=f_family, va='center')
            start_by -= line_spacing

    # Helper function for downward arrows
    def draw_down_arrow(x, y_start, y_end, label=""):
        ax.annotate('', xy=(x, y_end), xytext=(x, y_start),
                    arrowprops=dict(facecolor='#0f172a', edgecolor='#0f172a', width=1.1, headwidth=5.0, headlength=5.0, shrink=0.01))
        if label:
            ax.text(x, (y_start + y_end)/2, f"  {label}", ha='left', va='center', fontsize=7.2, fontstyle='italic', color='#0f172a', fontfamily=f_family)

    # -------------------------------------------------------------
    # 2. COLUMN (A): INFERENCE PATH (x: 4.5 to 48.5)
    # -------------------------------------------------------------
    
    # 1a. Patient Data Intake (Solid)
    draw_rich_card(4.5, 83.5, 21.0, 11.2, "screen", "#0284c7", "1a. Patient Intake", [
        "• Web UI / EHR clinical ingestion",
        "• 30 features (vitals, labs, lifestyle)",
        "• Interactive validation & feedback",
        "• Primary evaluated clinical path"
    ], is_gray=False, is_dashed=False, bullet_fs=6.6, line_spacing=1.65)

    # 1b. Wearable Telemetry (Dashed)
    draw_rich_card(27.5, 83.5, 21.0, 11.2, "pulse", "#0d9488", "1b. Wearable Telemetry", [
        "• Continuous BP & CGM glucose sensors",
        "• Real-time vital streaming logs (IoT)",
        "• BLE telemetry & anomaly flags",
        "• Optional longitudinal telemetry path"
    ], is_gray=False, is_dashed=True, bullet_fs=6.6, line_spacing=1.65)

    draw_down_arrow(15.0, 83.5, 77.2)
    draw_down_arrow(38.0, 83.5, 77.2)
    
    # 2. Input Validation Gate
    draw_rich_card(4.5, 66.5, 44.0, 10.7, "shield", "#ea580c", "2. Input Validation & Verification Gate", [
        "• Physiological range audits (SBP: 70–250 mmHg, FBS: 50–500 mg/dL, BMI: 10–70)",
        "• Cross-feature plausibility verification & missingness profiling",
        "• Dynamic schema typing & format integrity validation",
        "• Out-of-bounds input → immediately rejected with clinician re-entry prompt"
    ], is_gray=True, bullet_fs=6.7, line_spacing=1.65)

    draw_down_arrow(26.5, 66.5, 60.5, "verified valid")

    # 3. Clinical Data Preprocessing & Harmonization
    draw_rich_card(4.5, 47.8, 44.0, 12.7, "gear", "#0284c7", "3. Clinical Preprocessing & Feature Harmonization", [
        "• Zero-leakage median imputation (pre-computed strictly on training partition)",
        "• Outlier-resilient RobustScaler normalization: x' = (x - Q2) / (Q3 - Q1)",
        "• Hemodynamic feature derivation (Pulse Pressure, MAP, CKD-EPI eGFR)",
        "• Categorical one-hot encoding & binary alignment across multi-cohort schemas",
        "• Standardized 30-d clinical tensor (identical representation for web & sensor)"
    ], is_gray=False, bullet_fs=6.7, line_spacing=1.65)

    draw_down_arrow(26.5, 47.8, 42.0, "30-d clinical tensor")

    # 4. Feature Extraction - Shared Neural Encoder
    draw_rich_card(4.5, 29.5, 44.0, 12.5, "neural", "#7c3aed", "4. Shared Feature Neural Encoder (Multi-Task Core)", [
        "• Deep Architecture: Dense(30 → 64 → 32) + Layer Normalization + Dropout (p = 0.15)",
        "• Joint cardiorenal-metabolic latent representation learning (ReLU activations)",
        "• Captures shared biological mechanisms & cross-disease phenotypic correlations",
        "• Invariant feature extraction → outputs unified 32-d latent representation (Z ∈ R^32)"
    ], is_gray=True, bullet_fs=6.7, line_spacing=1.65)

    draw_down_arrow(26.5, 29.5, 24.0, "32-d latent representation")

    # 5. Dedicated Task Heads & Calibration
    draw_rich_card(4.5, 14.0, 44.0, 10.0, "sliders", "#4f46e5", "5. Dedicated Multi-Task Heads & Platt Calibration", [
        "• 3 Parallel Task Heads: Dense(32 → 16 → 1) with Sigmoid for T2D, CVD, CKD logits",
        "• Post-hoc Platt Sigmoid Scaling: P(y=1|z) = 1 / (1 + exp(A*z + B))",
        "• Optimizes probability reliability: Expected Calibration Error ECE < 0.011, Brier < 0.18"
    ], is_gray=True, bullet_fs=6.7, line_spacing=1.65)

    draw_down_arrow(26.5, 14.0, 9.0)

    # 6. Comorbidity Prediction & SHAP
    draw_rich_card(4.5, 1.0, 21.0, 8.0, "chart", "#059669", "6. Multi-Disease & SHAP", [
        "• T2D (88.7% rec), CVD (79.1%), CKD (94.6%)",
        "• Game-theoretic Tree/KernelSHAP attributions",
        "• Dynamic patient-specific risk drivers"
    ], is_gray=False, bullet_fs=6.4, line_spacing=1.55)

    # Horizontal connection arrow between 6 and 7
    ax.annotate('', xy=(27.5, 5.0), xytext=(25.5, 5.0),
                arrowprops=dict(facecolor='#0f172a', edgecolor='#0f172a', width=1.1, headwidth=4.5, headlength=4.5, shrink=0.01))

    # 7. Result Display & Clinical Actions
    draw_rich_card(27.5, 1.0, 21.0, 8.0, "cross", "#dc2626", "7. Clinical Care & Alerts", [
        "• Evidence-based ADA / ACC / KDIGO protocols",
        "• Multilingual AI Copilot (EN, Tamil, Hindi)",
        "• Automated Twilio SMS & urgent care alerts"
    ], is_gray=False, bullet_fs=6.4, line_spacing=1.55)

    # -------------------------------------------------------------
    # 3. COLUMN (B): OFFLINE TRAINING & SELECTION (x: 54.5 to 98.5)
    # -------------------------------------------------------------

    # 1. Dataset Management
    draw_rich_card(54.5, 83.5, 44.0, 11.2, "db", "#0284c7", "Dataset Management & Harmonization", [
        "• CDC BRFSS (70,692), Kaggle CVD (68,205), UCI CKD (400) cohorts",
        "• 139,297 unified patient records across 30 standardized clinical features",
        "• Strict 80/10/10 Stratified patient-level partitioning (111,438 / 13,929 / 13,930)",
        "• Resolves domain shift & semantic heterogeneity across population registries"
    ], is_gray=False, bullet_fs=6.7, line_spacing=1.65)

    draw_down_arrow(76.5, 83.5, 77.2)

    # 2. Task-Balanced Sampling
    draw_rich_card(54.5, 66.5, 44.0, 10.7, "scale", "#0d9488", "Task-Balanced Sampling & Imputation", [
        "• 20% dedicated batch allocation for data-scarce Chronic Kidney Disease cohort",
        "• Median imputer & RobustScaler parameters fit strictly on train fold only",
        "• Zero cross-fold leakage guaranteed through frozen preprocessing pipelines",
        "• Stratified mini-batch generation ensuring balanced gradient updates"
    ], is_gray=True, bullet_fs=6.7, line_spacing=1.65)

    draw_down_arrow(76.5, 66.5, 60.5)

    # 3. Multi-Task Training Pipeline
    draw_rich_card(54.5, 47.8, 44.0, 12.7, "lightning", "#d97706", "Multi-Task Optimization Pipeline", [
        "• Joint Task-Masked Loss: L_total = Σ_t I(y_t) * w_t * L_BCE(y_t, ŷ_t)",
        "• Adam optimizer (learning rate = 1e-3, weight decay = 1e-4, 36 epochs, batch 128)",
        "• Post-hoc Platt sigmoid parameter fitting (A, B) on validation partition",
        "• Early stopping checkpointing based on multi-disease validation loss",
        "• Mitigates negative transfer across heterogeneous task distributions"
    ], is_gray=True, bullet_fs=6.7, line_spacing=1.65)

    draw_down_arrow(76.5, 47.8, 42.0)

    # 4. Candidate Architectures
    draw_rich_card(54.5, 29.5, 44.0, 12.5, "grid", "#7c3aed", "Candidate Architecture Benchmarks", [
        "• Single-Task Baselines: Logistic Regression, Random Forest, XGBoost",
        "• Proposed Comorbidity-Aware Multi-Task Neural Network (MTL)",
        "• Latent bottleneck ablation experiments (d ∈ {16, 32, 64} dimensions)",
        "• Cross-validated performance audits across individual & comorbid cohorts"
    ], is_gray=True, bullet_fs=6.7, line_spacing=1.65)

    draw_down_arrow(76.5, 29.5, 24.0)

    # 5. Held-Out Test Evaluation
    draw_rich_card(54.5, 14.0, 44.0, 10.0, "target", "#2563eb", "Held-Out Test Evaluation (13,930 Patients)", [
        "• Comprehensive metrics: ROC-AUC, PR-AUC, Accuracy, Recall, Specificity, F1, ECE",
        "• T2D: 0.8276 AUC (+3.1% F1) | CVD: 0.7974 AUC | CKD: 0.9953 AUC",
        "• Statistically significant outperformance over all single-task baselines (p < 0.001)"
    ], is_gray=False, bullet_fs=6.7, line_spacing=1.65)

    draw_down_arrow(76.5, 14.0, 9.0)

    # 6. Selected Model
    draw_rich_card(54.5, 1.0, 44.0, 8.0, "star", "#059669", "Selected Production Model Checkpoint", [
        "• Optimal Comorbidity-Aware Multi-Task Neural Network (MTL)",
        "• Serialized PyTorch/ONNX .pt weights, scaler parameters & Platt coefficients",
        "• Integrated into high-throughput FastAPI inference microservice"
    ], is_gray=False, bullet_fs=6.7, line_spacing=1.65)

    # -------------------------------------------------------------
    # 4. CROSS-COLUMN CONNECTION: TRAINED WEIGHTS ARROW
    # -------------------------------------------------------------
    ax.plot([54.5, 51.5, 51.5, 48.5], [5.0, 5.0, 35.75, 35.75], color='#0f172a', linestyle='--', linewidth=1.2)
    ax.annotate('', xy=(48.5, 35.75), xytext=(51.5, 35.75),
                arrowprops=dict(facecolor='#0f172a', edgecolor='#0f172a', width=1.1, headwidth=5, headlength=5, shrink=0.01))
    ax.text(53.0, 20.37, "trained weights & scalers", ha='center', va='center', rotation=90, fontsize=7.2, fontstyle='italic', color='#0f172a', fontfamily=f_family)

    # Save outputs in high-resolution
    fig_dir = os.path.abspath("artifacts/report_figures")
    os.makedirs(fig_dir, exist_ok=True)
    
    out_1 = os.path.join(fig_dir, "fig_3_1_system_architecture.png")
    out_2 = os.path.abspath("artifacts/system_architecture_diagram_rich.png")
    out_3 = os.path.abspath("system_architecture_diagram.png")
    
    plt.tight_layout()
    plt.savefig(out_1, dpi=300, facecolor='#ffffff', bbox_inches='tight')
    plt.savefig(out_2, dpi=300, facecolor='#ffffff', bbox_inches='tight')
    plt.savefig(out_3, dpi=300, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    
    print(f"[SUCCESS] Rich-content vector-icon architecture diagram generated:")
    print(f"  -> {out_1}")
    print(f"  -> {out_2}")
    print(f"  -> {out_3}")

if __name__ == "__main__":
    generate_rich_icon_architecture_diagram()
