from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, default="patient", nullable=False) # patient, doctor/clinician, admin/super_admin
    status = Column(String, default="active", nullable=False) # active, inactive, suspended, pending
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow)

    patient_profile = relationship("Patient", back_populates="user", uselist=False)
    chat_history = relationship("ChatHistory", back_populates="user")

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    age = Column(Float, nullable=True)
    sex = Column(Integer, nullable=True) # 1: Male, 0: Female
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    bmi = Column(Float, nullable=True)
    education_level = Column(Float, nullable=True)
    income_level = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="patient_profile")
    health_records = relationship("HealthRecord", back_populates="patient")
    predictions = relationship("PredictionRecord", back_populates="patient")
    explanations = relationship("ExplanationRecord", back_populates="patient")
    recommendations = relationship("RecommendationRecord", back_populates="patient")
    alerts = relationship("ClinicalAlert", back_populates="patient")
    feedbacks = relationship("ClinicianFeedback", back_populates="patient")

class HealthRecord(Base):
    __tablename__ = "health_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    high_bp = Column(Float, nullable=True)
    high_chol = Column(Float, nullable=True)
    chol_check = Column(Float, nullable=True)
    stroke = Column(Float, nullable=True)
    heart_disease_or_attack = Column(Float, nullable=True)
    any_healthcare = Column(Float, nullable=True)
    no_doc_bc_cost = Column(Float, nullable=True)
    diff_walk = Column(Float, nullable=True)
    
    smoker = Column(Float, nullable=True)
    hvy_alcohol_consump = Column(Float, nullable=True)
    phys_activity = Column(Float, nullable=True)
    fruits = Column(Float, nullable=True)
    veggies = Column(Float, nullable=True)
    gen_hlth = Column(Float, nullable=True)
    ment_hlth = Column(Float, nullable=True)
    phys_hlth = Column(Float, nullable=True)
    
    ap_hi = Column(Float, nullable=True)
    ap_lo = Column(Float, nullable=True)
    glucose = Column(Float, nullable=True)
    cholesterol = Column(Float, nullable=True)
    
    serum_creatinine = Column(Float, nullable=True)
    blood_urea = Column(Float, nullable=True)
    hemoglobin = Column(Float, nullable=True)
    sodium = Column(Float, nullable=True)
    potassium = Column(Float, nullable=True)
    packed_cell_volume = Column(Float, nullable=True)
    white_blood_cell_count = Column(Float, nullable=True)
    red_blood_cell_count = Column(Float, nullable=True)
    hypertension_flag = Column(String, nullable=True)
    diabetes_mellitus_flag = Column(String, nullable=True)
    coronary_artery_disease = Column(String, nullable=True)
    appetite = Column(String, nullable=True)
    pedal_edema = Column(String, nullable=True)
    anemia = Column(String, nullable=True)
    
    preprocessed_features = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="health_records")

class DatasetMetadata(Base):
    __tablename__ = "dataset_metadata"

    id = Column(Integer, primary_key=True, index=True)
    dataset_name = Column(String, unique=True, nullable=False)
    file_name = Column(String, nullable=False)
    dataset_version = Column(String, default="1.0.0")
    num_rows = Column(Integer, nullable=False)
    num_columns = Column(Integer, nullable=False)
    target_column = Column(String, nullable=False)
    processing_status = Column(String, default="RAW")
    schema_details = Column(JSON, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PreprocessingExperiment(Base):
    __tablename__ = "preprocessing_experiments"

    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(String, unique=True, index=True, nullable=False)
    dataset_name = Column(String, nullable=False)
    dataset_version = Column(String, default="1.0.0")
    missingness_scenario = Column(String, nullable=True)
    missingness_percentage = Column(Float, default=0.0)
    imputation_method = Column(String, default="median")
    outlier_strategy = Column(String, default="iqr_capping")
    encoding_strategy = Column(String, default="onehot")
    scaling_strategy = Column(String, default="standard")
    feature_selection_method = Column(String, default="select_k_best")
    class_imbalance_method = Column(String, default="smote")
    train_val_test_ratio = Column(String, default="70/15/15")
    random_seed = Column(Integer, default=42)
    pipeline_version = Column(String, nullable=False)
    metrics_summary = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PipelineVersion(Base):
    __tablename__ = "pipeline_versions"

    id = Column(Integer, primary_key=True, index=True)
    pipeline_version = Column(String, unique=True, nullable=False)
    dataset_name = Column(String, nullable=False)
    artifact_path = Column(String, nullable=False)
    configuration = Column(JSON, nullable=False)
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow)

# ================= MODULE 2 DATABASE MODELS =================

class ModelRegistry(Base):
    __tablename__ = "model_registry"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, nullable=False)
    disease = Column(String, nullable=False)
    model_version = Column(String, unique=True, index=True, nullable=False)
    framework = Column(String, default="scikit-learn")
    training_dataset_version = Column(String, default="v1.0.0")
    preprocessing_version = Column(String, default="v1.0.0")
    artifact_path = Column(String, nullable=False)
    status = Column(String, default="ACTIVE")
    performance_metrics = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ModelExperiment(Base):
    __tablename__ = "model_experiments"

    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(String, unique=True, index=True, nullable=False)
    disease = Column(String, nullable=False)
    model_type = Column(String, nullable=False)
    architecture_type = Column(String, default="independent")
    hyperparameters = Column(JSON, nullable=False)
    cv_score_mean = Column(Float, nullable=True)
    cv_score_std = Column(Float, nullable=True)
    test_roc_auc = Column(Float, nullable=True)
    test_recall = Column(Float, nullable=True)
    test_f1 = Column(Float, nullable=True)
    brier_score = Column(Float, nullable=True)
    metrics_full = Column(JSON, nullable=True)
    random_seed = Column(Integer, default=42)
    created_at = Column(DateTime, default=datetime.utcnow)

class PredictionRecord(Base):
    __tablename__ = "prediction_records"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(String, unique=True, index=True, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)
    
    diabetes_probability = Column(Float, nullable=False)
    diabetes_risk_category = Column(String, nullable=False)
    
    cvd_probability = Column(Float, nullable=False)
    cvd_risk_category = Column(String, nullable=False)
    
    ckd_probability = Column(Float, nullable=False)
    ckd_risk_category = Column(String, nullable=False)
    
    model_version = Column(String, nullable=False)
    preprocessing_version = Column(String, default="v1.0.0")
    calibration_version = Column(String, default="platt_sigmoid")
    module3_handoff_payload = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="predictions")
    explanations = relationship("ExplanationRecord", back_populates="prediction")

class ModelEvaluation(Base):
    __tablename__ = "model_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    model_version = Column(String, nullable=False)
    disease = Column(String, nullable=False)
    accuracy = Column(Float, nullable=False)
    precision = Column(Float, nullable=False)
    recall = Column(Float, nullable=False)
    f1_score = Column(Float, nullable=False)
    roc_auc = Column(Float, nullable=False)
    pr_auc = Column(Float, nullable=True)
    brier_score = Column(Float, nullable=True)
    confusion_matrix = Column(JSON, nullable=True)
    calibration_details = Column(JSON, nullable=True)
    evaluated_at = Column(DateTime, default=datetime.utcnow)

# ================= MODULE 3 DATABASE MODELS =================

class ExplanationRecord(Base):
    __tablename__ = "explanation_records"

    id = Column(Integer, primary_key=True, index=True)
    explanation_id = Column(String, unique=True, index=True, nullable=False)
    prediction_id = Column(String, ForeignKey("prediction_records.prediction_id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)
    disease = Column(String, nullable=False)
    model_version = Column(String, nullable=False)
    preprocessing_version = Column(String, default="v1.0.0")
    explainer_type = Column(String, default="TreeExplainer") # TreeExplainer, LinearExplainer, KernelExplainer
    base_value = Column(Float, nullable=False)
    explanation_status = Column(String, default="VALIDATED")
    module4_handoff_payload = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="explanations")
    prediction = relationship("PredictionRecord", back_populates="explanations")
    feature_contributions = relationship("FeatureContribution", back_populates="explanation")

class FeatureContribution(Base):
    __tablename__ = "feature_contributions"

    id = Column(Integer, primary_key=True, index=True)
    explanation_id = Column(String, ForeignKey("explanation_records.explanation_id"), nullable=False)
    feature_name = Column(String, nullable=False)
    patient_value = Column(Float, nullable=False)
    shap_value = Column(Float, nullable=False)
    abs_shap_value = Column(Float, nullable=False)
    direction = Column(String, nullable=False) # RISK_INCREASING, RISK_DECREASING
    rank = Column(Integer, nullable=False)
    modifiable_status = Column(String, nullable=False) # Modifiable, Non-Modifiable
    human_explanation = Column(Text, nullable=True)

    explanation = relationship("ExplanationRecord", back_populates="feature_contributions")

class GlobalFeatureImportance(Base):
    __tablename__ = "global_feature_importance"

    id = Column(Integer, primary_key=True, index=True)
    disease = Column(String, nullable=False)
    model_version = Column(String, nullable=False)
    feature_name = Column(String, nullable=False)
    mean_abs_shap = Column(Float, nullable=False)
    rank = Column(Integer, nullable=False)
    evaluated_at = Column(DateTime, default=datetime.utcnow)

# ================= MODULE 4 DATABASE MODELS =================

class RecommendationRecord(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)
    prediction_id = Column(String, ForeignKey("prediction_records.prediction_id"), nullable=True)
    assessment_id = Column(String, nullable=True)
    language = Column(String, default="en")
    disease = Column(String, nullable=False, default="MULTI-DISEASE")
    risk_factor = Column(String, nullable=False)
    category = Column(String, nullable=False)
    recommendation_text = Column(Text, nullable=False)
    reason = Column(Text, nullable=False)
    priority = Column(String, nullable=False, default="Medium")
    safety_note = Column(Text, nullable=True)
    daily_food_plan = Column(JSON, nullable=True)
    exercise_plan = Column(JSON, nullable=True)
    daily_habits = Column(JSON, nullable=True)
    herbal_wellness = Column(JSON, nullable=True)
    monitoring_guidance = Column(JSON, nullable=True)
    clinical_followup_required = Column(Boolean, default=False)
    clinical_followup_message = Column(Text, nullable=True)
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="recommendations")

# ================= MODULE 5 DATABASE MODELS =================

class ClinicalAlert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    assessment_id = Column(String, nullable=True)
    alert_type = Column(String, nullable=False) # HIGH_RISK, LOW_CONFIDENCE, RISK_INCREASE, SAFETY_ESCALATION, CLINICAL_REVIEW
    severity = Column(String, nullable=False, default="Monitor") # Normal, Monitor, Clinical Review
    message = Column(Text, nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(String, default="OPEN", nullable=False) # OPEN, REVIEWED, RESOLVED
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)
    reviewed_by = Column(String, nullable=True)

    patient = relationship("Patient", back_populates="alerts")

class ClinicianFeedback(Base):
    __tablename__ = "clinician_feedback"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(String, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    clinician_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    feedback_text = Column(Text, nullable=False)
    clinical_action = Column(String, nullable=False, default="Reviewed") # Reviewed, Follow-up Recommended, Continue Monitoring, No Further Action
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="feedbacks")

# ================= MODULE 6 DATABASE MODELS =================

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(String, default="default", nullable=False)
    role = Column(String, nullable=False) # user, assistant
    message = Column(Text, nullable=False)
    intent = Column(String, nullable=True) # RISK_SUMMARY, RISK_EXPLANATION, RISK_FACTORS, WELLNESS_RECOMMENDATION, RISK_HISTORY, ALERT_INFORMATION, GENERAL_WELLNESS
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chat_history")




