import sys
import os
import json

sys.path.insert(0, os.path.abspath('backend'))
from app.services.prediction_service import PredictionService

patient_data = {
    'age': 56,
    'sex': 1,
    'height_cm': 172,
    'weight_kg': 84,
    'ap_hi': 142,
    'ap_lo': 92,
    'glucose': 148,
    'serum_creatinine': 1.55,
    'blood_urea': 42,
    'hemoglobin': 12.8,
    'high_bp': 1,
    'high_chol': 1,
    'smoker': 1,
    'phys_activity': 0
}

res = PredictionService.predict_multi_disease_risk(patient_data, patient_id=8942)
print("=== PREDICTION RESULTS FOR PATIENT ID 8942 ===")
for d, p in res["predictions"].items():
    print(f"{d.upper()}: Probability = {p['probability']} ({p['risk_percentage']}%), Category = {p['risk_category']}, Model = {p['model_version']}")

print("\n=== SHAP TOP RISK FACTORS ===")
for d, factors in res["shap"].items():
    print(f"\n--- {d.upper()} Top Factors ---")
    for f in factors:
        print(f"  Rank {f['rank']}: {f['feature_name']} (val={f['patient_value']}) -> SHAP: {f['shap_value']:+.4f} | {f['direction']}")
        print(f"     Explanation: {f['human_explanation']}")
