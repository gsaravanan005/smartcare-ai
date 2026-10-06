"""
SmartCare AI - Exact Architecture Diagram Generator Matching User Reference Image
Recreates the exact visual layout, color scheme, container cards, circular badges,
and arrow routing from the user's reference diagram.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_reference_matched_architecture_diagram():
    # Canvas setup with ample white margins
    fig, ax = plt.subplots(figsize=(16, 9.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Color Palette matching the reference image
    c_users_bg = '#dbeafe'       # Light Blue
    c_users_border = '#60a5fa'   # Blue border
    c_avatar = '#3b82f6'         # Avatar blue

    c_fe_bg = '#ffedd5'          # Soft Peach/Orange
    c_fe_border = '#fb923c'      # Orange border
    c_fe_icon = '#f97316'        # Icon circle
    c_fe_icon_bg = '#fed7aa'

    c_db_bg = '#dcfce7'          # Light Green
    c_db_border = '#4ade80'      # Green border
    c_db_pill = '#86efac'        # Green oval pill
    c_db_pill_border = '#22c55e'

    c_be_bg = '#fef9c3'          # Light Cream/Yellow
    c_be_border = '#facc15'      # Yellow border

    c_hw_bg = '#fee2e2'          # Light Red/Pink
    c_hw_border = '#f87171'      # Red border
    c_hw_icon_bg = '#fca5a5'
    c_hw_icon = '#ef4444'

    c_ml_bg = '#f3e8ff'          # Light Purple/Lavender
    c_ml_border = '#c084fc'      # Purple border
    c_ml_icon_bg = '#d8b4fe'
    c_ml_icon = '#9333ea'

    # -------------------------------------------------------------
    # 1. USERS BOX (Left Column)
    # -------------------------------------------------------------
    u_box = patches.Rectangle((4, 41), 12, 18, linewidth=1.5, edgecolor=c_users_border, facecolor=c_users_bg)
    ax.add_patch(u_box)
    ax.text(10, 56, "USERS", ha='center', va='center', fontsize=11, fontweight='bold', color='#1e3a8a', fontfamily='sans-serif')

    # Avatar 1: Clinician
    c1 = patches.Circle((7.5, 48), 1.2, color='#93c5fd')
    ax.add_patch(c1)
    c1_head = patches.Circle((7.5, 48.5), 0.5, color='#1d4ed8')
    ax.add_patch(c1_head)
    c1_body = patches.Wedge((7.5, 47.2), 0.85, 0, 180, color='#1d4ed8')
    ax.add_patch(c1_body)
    ax.text(7.5, 44.5, "Clinician", ha='center', va='center', fontsize=7.5, color='#1e3a8a', fontfamily='sans-serif')

    # Avatar 2: Patient
    c2 = patches.Circle((12.5, 48), 1.2, color='#93c5fd')
    ax.add_patch(c2)
    c2_head = patches.Circle((12.5, 48.5), 0.5, color='#1d4ed8')
    ax.add_patch(c2_head)
    c2_body = patches.Wedge((12.5, 47.2), 0.85, 0, 180, color='#1d4ed8')
    ax.add_patch(c2_body)
    ax.text(12.5, 44.5, "Patient", ha='center', va='center', fontsize=7.5, color='#1e3a8a', fontfamily='sans-serif')

    # -------------------------------------------------------------
    # 2. FRONTEND BOX (Column 2)
    # -------------------------------------------------------------
    fe_box = patches.Rectangle((23.5, 12), 19, 76, linewidth=1.5, edgecolor=c_fe_border, facecolor=c_fe_bg)
    ax.add_patch(fe_box)
    ax.text(33, 85, "FRONTEND", ha='center', va='center', fontsize=11, fontweight='bold', color='#7c2d12', fontfamily='sans-serif')

    # 6 Feature rows
    fe_rows = [
        ("Capture & Ingestion", "Input 30 vitals, labs & lifestyle metrics"),
        ("Comorbidity Dashboard", "Real-time T2D, CVD & CKD risk scores"),
        ("SHAP Attribution", "Local patient waterfall decomposition"),
        ("Guideline Interventions", "ADA, ACC/AHA & KDIGO care regimens"),
        ("Longitudinal Telemetry", "Vitals trajectory & rate-of-change tracker"),
        ("Multilingual Copilot", "Tamil, Hindi, Spanish & English AI chat")
    ]

    y_pos = 77
    for title, subtitle in fe_rows:
        # Icon circle
        ic_bg = patches.Circle((26.5, y_pos), 1.4, edgecolor='#ea580c', facecolor=c_fe_icon_bg, lw=1)
        ax.add_patch(ic_bg)
        ic_dot = patches.Circle((26.5, y_pos), 0.35, color='#9a3412')
        ax.add_patch(ic_dot)
        
        # Text
        ax.text(29.2, y_pos + 0.8, title, fontsize=8.5, fontweight='bold', color='#431407', fontfamily='sans-serif')
        ax.text(29.2, y_pos - 1.2, subtitle, fontsize=6.5, color='#7c2d12', fontfamily='sans-serif')
        y_pos -= 11.5

    # -------------------------------------------------------------
    # 3. DATABASE & STORAGE BOX (Column 3, Top)
    # -------------------------------------------------------------
    db_box = patches.Rectangle((51, 52), 18, 36, linewidth=1.5, edgecolor=c_db_border, facecolor=c_db_bg)
    ax.add_patch(db_box)
    ax.text(60, 85, "DATABASE & STORAGE", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#14532d', fontfamily='sans-serif')
    ax.text(60, 81.5, "SQLite + SQLAlchemy Engine", ha='center', va='center', fontsize=7, fontstyle='italic', color='#166534', fontfamily='sans-serif')

    db_pills = [
        "Patient & EHR Records",
        "Historical Telemetry Logs",
        "Model Registry (.pt / .joblib)",
        "Emergency Audit Archives"
    ]
    y_db = 74
    for item in db_pills:
        pill = patches.Ellipse((54, y_db), 2.6, 1.6, edgecolor=c_db_pill_border, facecolor=c_db_pill, lw=1)
        ax.add_patch(pill)
        ax.text(56.5, y_db, item, va='center', fontsize=7.5, color='#14532d', fontfamily='sans-serif')
        y_db -= 6.2

    # -------------------------------------------------------------
    # 4. BACKEND BOX (Column 3, Bottom)
    # -------------------------------------------------------------
    be_box = patches.Rectangle((51, 12), 18, 33, linewidth=1.5, edgecolor=c_be_border, facecolor=c_be_bg)
    ax.add_patch(be_box)
    ax.text(60, 41.5, "BACKEND", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#713f12', fontfamily='sans-serif')

    # REST API Box
    api_box = patches.Rectangle((52.5, 30), 7.5, 5, linewidth=1, edgecolor='#0284c7', facecolor='#0ea5e9')
    ax.add_patch(api_box)
    ax.text(56.25, 32.5, "REST API", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#ffffff', fontfamily='sans-serif')
    ax.text(61, 32.5, "FastAPI Router", va='center', fontsize=7.5, color='#451a03', fontfamily='sans-serif')

    # Clinical Rules Engine Circle
    cr_circle = patches.Circle((55.5, 20), 1.8, edgecolor='#1e40af', facecolor='#1d4ed8')
    ax.add_patch(cr_circle)
    ax.text(55.5, 20, "CR", ha='center', va='center', fontsize=8, fontweight='bold', color='#ffffff', fontfamily='sans-serif')
    ax.text(58.5, 21.2, "Clinical Rules Engine", fontsize=7.5, fontweight='bold', color='#451a03', fontfamily='sans-serif')
    ax.text(58.5, 18.8, "ADA, ACC & KDIGO Logic", fontsize=6.5, color='#713f12', fontfamily='sans-serif')

    # -------------------------------------------------------------
    # 5. HARDWARE & CLINICAL DATASETS (Column 4, Top)
    # -------------------------------------------------------------
    hw_box = patches.Rectangle((80, 52), 16.5, 36, linewidth=1.5, edgecolor=c_hw_border, facecolor=c_hw_bg)
    ax.add_patch(hw_box)
    ax.text(88.25, 85, "DATASETS & TELEMETRY", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#7f1d1d', fontfamily='sans-serif')

    hw_items = [
        ("CDC BRFSS 2015", "70,692 Clinical Records"),
        ("Kaggle CVD Cohort", "68,205 Patient Records"),
        ("UCI CKD Dataset", "400 Nephrology Records"),
        ("Twilio SMS & SMTP", "Real-Time Emergency Alerts")
    ]
    y_hw = 75
    for title, sub in hw_items:
        ic = patches.Circle((83, y_hw), 1.3, edgecolor=c_hw_icon, facecolor=c_hw_icon_bg, lw=1)
        ax.add_patch(ic)
        ax.text(83, y_hw, "o", ha='center', va='center', fontsize=6.5, color='#7f1d1d')
        
        ax.text(85.5, y_hw + 0.6, title, fontsize=7.5, fontweight='bold', color='#450a0a', fontfamily='sans-serif')
        ax.text(85.5, y_hw - 1.0, sub, fontsize=6.2, color='#7f1d1d', fontfamily='sans-serif')
        y_hw -= 6.5

    # -------------------------------------------------------------
    # 6. AI / ML LAYER (Column 4, Bottom)
    # -------------------------------------------------------------
    ml_box = patches.Rectangle((80, 7), 16.5, 42, linewidth=1.5, edgecolor=c_ml_border, facecolor=c_ml_bg)
    ax.add_patch(ml_box)
    ax.text(88.25, 45.5, "AI / ML LAYER", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#581c87', fontfamily='sans-serif')

    ml_items = [
        ("Shared Neural Encoder", "Dense(30->64->32) + LayerNorm"),
        ("Multi-Task Heads", "3x Dense(32->16->1) (T2D/CVD/CKD)"),
        ("Platt Sigmoid Scaling", "Posterior Calibration (ECE < 0.011)"),
        ("SHAP Explainability", "Tree & Kernel Shapley Attributions")
    ]
    y_ml = 37
    for title, sub in ml_items:
        ic = patches.Circle((83, y_ml), 1.4, edgecolor=c_ml_icon, facecolor=c_ml_icon_bg, lw=1)
        ax.add_patch(ic)
        ax.text(83, y_ml, "★", ha='center', va='center', fontsize=8, color='#581c87')
        
        ax.text(85.5, y_ml + 0.7, title, fontsize=7.5, fontweight='bold', color='#3b0764', fontfamily='sans-serif')
        ax.text(85.5, y_ml - 1.1, sub, fontsize=6.2, color='#6b21a8', fontfamily='sans-serif')
        y_ml -= 7.8

    # -------------------------------------------------------------
    # 7. CONNECTING ARROWS
    # -------------------------------------------------------------
    def draw_arrow(x1, y1, x2, y2, color='#64748b'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(facecolor=color, edgecolor=color, width=1.0, headwidth=4.5, headlength=5, shrink=0.01))

    # Users -> Frontend
    draw_arrow(16, 50, 23.5, 50, '#64748b')

    # Frontend -> Database (branch up)
    ax.plot([42.5, 46.5, 46.5], [50, 50, 70], color='#64748b', lw=1.2)
    draw_arrow(46.5, 70, 51, 70, '#64748b')

    # Frontend -> Backend (branch down)
    ax.plot([42.5, 46.5, 46.5], [50, 50, 28.5], color='#64748b', lw=1.2)
    draw_arrow(46.5, 28.5, 51, 28.5, '#64748b')

    # Database & Backend -> Hardware & AI/ML
    ax.plot([69, 73, 73], [70, 70, 50], color='#64748b', lw=1.2)
    ax.plot([69, 73, 73], [28.5, 28.5, 50], color='#64748b', lw=1.2)
    
    # Split to Datasets (top right)
    ax.plot([73, 76.5, 76.5], [50, 50, 67], color='#64748b', lw=1.2)
    draw_arrow(76.5, 67, 80, 67, '#64748b')

    # Split to AI/ML (bottom right)
    ax.plot([73, 76.5, 76.5], [50, 50, 28], color='#64748b', lw=1.2)
    draw_arrow(76.5, 28, 80, 28, '#64748b')

    # Output paths
    fig_dir = os.path.abspath("artifacts/report_figures")
    os.makedirs(fig_dir, exist_ok=True)
    
    out_1 = os.path.join(fig_dir, "fig_3_1_system_architecture.png")
    out_2 = os.path.abspath("artifacts/system_architecture_reference_style.png")
    out_3 = os.path.abspath("system_architecture_reference_style.png")
    
    plt.tight_layout()
    plt.savefig(out_1, dpi=300, facecolor='#ffffff', bbox_inches='tight')
    plt.savefig(out_2, dpi=300, facecolor='#ffffff', bbox_inches='tight')
    plt.savefig(out_3, dpi=300, facecolor='#ffffff', bbox_inches='tight')
    plt.close()
    
    print(f"[SUCCESS] Reference-style architecture diagram generated:")
    print(f"  -> {out_1}")
    print(f"  -> {out_2}")
    print(f"  -> {out_3}")

if __name__ == "__main__":
    create_reference_matched_architecture_diagram()
