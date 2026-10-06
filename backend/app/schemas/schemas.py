from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- Auth Schemas ---
class UserCreate(BaseModel):
    username: Optional[str] = None
    email: str
    password: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    role: Optional[str] = None # Ignored by backend during public registration

class AdminStaffCreate(BaseModel):
    name: str
    email: str
    username: Optional[str] = None
    phone: Optional[str] = None
    staff_id: Optional[str] = None
    department: Optional[str] = "General Medicine"
    designation: Optional[str] = "Senior Clinician"
    specialization: Optional[str] = "General Medicine"
    qualification: Optional[str] = "MD"
    license_number: Optional[str] = None
    hospital: Optional[str] = "SmartCare AI Hospital & Medical Center"
    experience: Optional[int] = 5
    verification_status: Optional[str] = "approved"
    role: str = "DOCTOR" # DOCTOR or STAFF
    password: Optional[str] = "smartcare123"

class UserLogin(BaseModel):
    username: str
    password: str
    target_role: Optional[str] = None # 'patient', 'doctor', 'admin'

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str
    role: str
    status: Optional[str] = "active"
    patient_profile_id: Optional[int] = None
    patient_id: Optional[int] = None
    doctor_profile_id: Optional[int] = None
    doctor_id: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    username: str
    email: str
    full_name: Optional[str] = None
    role: str
    status: Optional[str] = "active"
    patient_profile_id: Optional[int] = None
    patient_id: Optional[int] = None
    doctor_profile_id: Optional[int] = None
    doctor_id: Optional[int] = None
    created_at: Optional[Any] = None
    updated_at: Optional[Any] = None
    last_login: Optional[Any] = None

    class Config:
        from_attributes = True

class ForgotPasswordRequest(BaseModel):
    email_or_id: str

class ForgotPasswordResponse(BaseModel):
    message: str

class LogoutResponse(BaseModel):
    message: str

# --- Patient & Health Data Schemas ---
class PatientProfileUpdate(BaseModel):
    age: Optional[float] = Field(None, ge=1, le=120)
    sex: Optional[int] = Field(None, ge=0, le=1) # 1: Male, 0: Female
    height_cm: Optional[float] = Field(None, ge=50, le=250)
    weight_kg: Optional[float] = Field(None, ge=20, le=300)
    education_level: Optional[float] = None
    income_level: Optional[float] = None

class PatientProfileResponse(BaseModel):
    id: int
    user_id: int
    age: Optional[float] = None
    sex: Optional[int] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    bmi: Optional[float] = None
    education_level: Optional[float] = None
    income_level: Optional[float] = None

    class Config:
        from_attributes = True

class HealthRecordCreate(BaseModel):
    # Demographics / Patient Profile Override
    age: Optional[float] = None
    sex: Optional[float] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    
    # Medical History
    high_bp: Optional[float] = 0.0
    high_chol: Optional[float] = 0.0
    chol_check: Optional[float] = 1.0
    stroke: Optional[float] = 0.0
    heart_disease_or_attack: Optional[float] = 0.0
    any_healthcare: Optional[float] = 1.0
    no_doc_bc_cost: Optional[float] = 0.0
    diff_walk: Optional[float] = 0.0

    # Lifestyle
    smoker: Optional[float] = 0.0
    hvy_alcohol_consump: Optional[float] = 0.0
    phys_activity: Optional[float] = 1.0
    fruits: Optional[float] = 1.0
    veggies: Optional[float] = 1.0
    gen_hlth: Optional[float] = 2.0
    ment_hlth: Optional[float] = 0.0
    phys_hlth: Optional[float] = 0.0

    # Clinical Measurements (CVD / General)
    ap_hi: Optional[float] = 120.0
    ap_lo: Optional[float] = 80.0
    glucose: Optional[float] = 100.0
    cholesterol: Optional[float] = 1.0

    # CKD Measurements
    serum_creatinine: Optional[float] = 1.0
    blood_urea: Optional[float] = 30.0
    hemoglobin: Optional[float] = 14.0
    sodium: Optional[float] = 138.0
    potassium: Optional[float] = 4.2
    packed_cell_volume: Optional[float] = 40.0
    white_blood_cell_count: Optional[float] = 7500.0
    red_blood_cell_count: Optional[float] = 4.8
    hypertension_flag: Optional[str] = "no"
    diabetes_mellitus_flag: Optional[str] = "no"
    coronary_artery_disease: Optional[str] = "no"
    appetite: Optional[str] = "good"
    pedal_edema: Optional[str] = "no"
    anemia: Optional[str] = "no"

class HealthRecordResponse(BaseModel):
    id: int
    patient_id: int
    created_at: datetime
    preprocessed_features: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

# --- Dataset & Pipeline Analysis Schemas ---
class DatasetProfileResponse(BaseModel):
    dataset_name: str
    num_rows: int
    num_columns: int
    target_column: str
    columns: List[str]
    dtypes: Dict[str, str]
    numerical_features: List[str]
    categorical_features: List[str]
    binary_features: List[str]
    missing_summary: Dict[str, int]
    target_distribution: Dict[str, Any]
    summary_stats: Dict[str, Dict[str, float]]
    duplicate_count: int

class PipelineRunRequest(BaseModel):
    dataset_name: str # diabetes, cardio, ckd, or all
    imputation_method: str = "median" # mean, median, mode, knn, iterative
    outlier_strategy: str = "iqr_capping" # iqr_capping, zscore_capping, removal, keep
    encoding_strategy: str = "onehot" # onehot, ordinal
    scaling_strategy: str = "standard" # standard, minmax
    feature_selection_method: str = "select_k_best" # select_k_best, mutual_info, rfe, all
    k_features: int = 15
    class_imbalance_method: str = "smote" # smote, oversampling, undersampling, class_weights, none
    missingness_injection_scenario: Optional[str] = None # scenario_a, scenario_b, scenario_c, scenario_d
    missingness_injection_rate: float = 0.0 # 0.0, 0.05, 0.10, 0.15, 0.20
    random_seed: int = 42
    train_ratio: float = 0.70
    val_ratio: float = 0.15
    test_ratio: float = 0.15

class PipelineRunResponse(BaseModel):
    status: str
    experiment_id: str
    dataset_name: str
    pipeline_version: str
    train_shape: List[int]
    val_shape: List[int]
    test_shape: List[int]
    selected_features: List[str]
    vif_summary: Dict[str, float]
    artifacts_exported: List[str]
    message: str

# --- Module 5 Risk Monitoring & Clinician Decision Schemas ---
class ClinicalAlertResponse(BaseModel):
    id: int
    patient_id: int
    assessment_id: Optional[str] = None
    alert_type: str
    severity: str
    message: str
    reason: str
    status: str
    created_at: datetime
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[str] = None

    class Config:
        from_attributes = True

class AlertUpdate(BaseModel):
    status: str # OPEN, REVIEWED, RESOLVED

class RiskTrendItem(BaseModel):
    disease: str
    previous_risk_percentage: float
    current_risk_percentage: float
    percentage_point_difference: float
    trend_status: str # Increasing, Decreasing, Stable
    safe_clinical_wording: str

class RiskTrendResponse(BaseModel):
    patient_id: int
    latest_assessment_id: Optional[str] = None
    previous_assessment_id: Optional[str] = None
    trends: Dict[str, RiskTrendItem]
    overall_alert_status: str
    calculated_at: datetime

class ClinicianFeedbackCreate(BaseModel):
    assessment_id: str
    patient_id: int
    feedback_text: str
    clinical_action: Optional[str] = "Reviewed" # Reviewed, Follow-up Recommended, Continue Monitoring, No Further Action

class ClinicianFeedbackResponse(BaseModel):
    id: int
    assessment_id: str
    patient_id: int
    clinician_id: int
    feedback_text: str
    clinical_action: str
    created_at: datetime

    class Config:
        from_attributes = True

class ClinicianDashboardResponse(BaseModel):
    total_patients: int
    patients_requiring_review: int
    recent_assessments_count: int
    open_alerts_count: int
    recent_alerts: List[ClinicalAlertResponse]

