import React, { useState } from 'react';
import HolographicHUDPanel from '../components/HolographicHUDPanel';
import { healthDataAPI } from '../services/api';
import { 
  User, Heart, Activity, TestTube, CheckCircle, AlertCircle, 
  ArrowRight, ArrowLeft, Send, Sparkles, Stethoscope, RefreshCw 
} from 'lucide-react';

const STEPS = [
  { id: 1, label: '01 PROFILE' },
  { id: 2, label: '02 MEDICAL HISTORY' },
  { id: 3, label: '03 LIFESTYLE' },
  { id: 4, label: '04 CLINICAL MEASUREMENTS' },
  { id: 5, label: '05 REVIEW' },
  { id: 6, label: '06 SUBMIT' }
];

export default function HealthDataForm({ user, onNavigate }) {
  const [currentStep, setCurrentStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successResult, setSuccessResult] = useState(null);

  // Form Data State - ALL START COMPLETELY EMPTY
  const [formData, setFormData] = useState({
    age: '',
    sex: '',
    height_cm: '',
    weight_kg: '',

    high_bp: '',
    high_chol: '',
    chol_check: '',
    stroke: '',
    heart_disease_or_attack: '',
    any_healthcare: '',
    no_doc_bc_cost: '',
    diff_walk: '',

    smoker: '',
    hvy_alcohol_consump: '',
    phys_activity: '',
    fruits: '',
    veggies: '',
    gen_hlth: '',
    ment_hlth: '',
    phys_hlth: '',

    ap_hi: '',
    ap_lo: '',
    glucose: '',
    cholesterol: '',
    serum_creatinine: '',
    blood_urea: '',
    hemoglobin: '',
    sodium: '',
    potassium: '',
    packed_cell_volume: '',
    white_blood_cell_count: '',
    red_blood_cell_count: ''
  });

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? (value === '' ? '' : parseFloat(value)) : value
    }));
  };

  const bmi = (formData.height_cm && formData.weight_kg && !isNaN(formData.height_cm) && !isNaN(formData.weight_kg))
    ? (formData.weight_kg / Math.pow(formData.height_cm / 100, 2)).toFixed(1)
    : 'N/A';

  // Validation Rules
  const validateStep = (stepNumber) => {
    if (stepNumber === 1) {
      if (formData.age === '' || isNaN(formData.age) || formData.age < 1 || formData.age > 120) {
        return "Step 01 Incomplete: Please enter a valid Age (1 - 120 years).";
      }
      if (formData.sex === '') {
        return "Step 01 Incomplete: Please select Sex.";
      }
      if (formData.height_cm === '' || isNaN(formData.height_cm) || formData.height_cm < 50 || formData.height_cm > 250) {
        return "Step 01 Incomplete: Please enter a valid Height (50 - 250 cm).";
      }
      if (formData.weight_kg === '' || isNaN(formData.weight_kg) || formData.weight_kg < 20 || formData.weight_kg > 300) {
        return "Step 01 Incomplete: Please enter a valid Weight (20 - 300 kg).";
      }
    } else if (stepNumber === 2) {
      if (formData.high_bp === '' || formData.high_chol === '' || formData.stroke === '' || 
          formData.heart_disease_or_attack === '' || formData.diff_walk === '' || formData.any_healthcare === '') {
        return "Step 02 Incomplete: Please select options for all Medical History fields.";
      }
    } else if (stepNumber === 3) {
      if (formData.smoker === '' || formData.hvy_alcohol_consump === '' || formData.phys_activity === '' || 
          formData.fruits === '' || formData.veggies === '' || formData.gen_hlth === '') {
        return "Step 03 Incomplete: Please select options for all Lifestyle fields.";
      }
    } else if (stepNumber === 4) {
      if (formData.ap_hi === '' || isNaN(formData.ap_hi) || formData.ap_hi < 60 || formData.ap_hi > 250) {
        return "Step 04 Incomplete: Please enter valid Systolic Blood Pressure (ap_hi mmHg).";
      }
      if (formData.ap_lo === '' || isNaN(formData.ap_lo) || formData.ap_lo < 40 || formData.ap_lo > 180) {
        return "Step 04 Incomplete: Please enter valid Diastolic Blood Pressure (ap_lo mmHg).";
      }
      if (formData.glucose === '' || isNaN(formData.glucose) || formData.glucose < 40 || formData.glucose > 500) {
        return "Step 04 Incomplete: Please enter valid Blood Glucose (bgr mg/dL).";
      }
      if (formData.serum_creatinine === '' || isNaN(formData.serum_creatinine) || formData.serum_creatinine < 0.1 || formData.serum_creatinine > 20) {
        return "Step 04 Incomplete: Please enter valid Serum Creatinine (sc mg/dL).";
      }
      if (formData.blood_urea === '' || isNaN(formData.blood_urea) || formData.blood_urea < 1 || formData.blood_urea > 300) {
        return "Step 04 Incomplete: Please enter valid Blood Urea (bu mg/dL).";
      }
      if (formData.hemoglobin === '' || isNaN(formData.hemoglobin) || formData.hemoglobin < 2 || formData.hemoglobin > 25) {
        return "Step 04 Incomplete: Please enter valid Hemoglobin (g/dL).";
      }
    }
    return null;
  };

  const handleStepClick = (targetStepId) => {
    if (targetStepId <= currentStep) {
      setError(null);
      setCurrentStep(targetStepId);
      return;
    }

    for (let s = 1; s < targetStepId; s++) {
      const err = validateStep(s);
      if (err) {
        setError(err);
        setCurrentStep(s);
        return;
      }
    }

    setError(null);
    setCurrentStep(targetStepId);
  };

  const handleNext = () => {
    const err = validateStep(currentStep);
    if (err) {
      setError(err);
      return;
    }
    setError(null);
    if (currentStep < 6) setCurrentStep(prev => prev + 1);
  };

  const handlePrev = () => {
    setError(null);
    if (currentStep > 1) setCurrentStep(prev => prev - 1);
  };

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();

    for (let s = 1; s <= 4; s++) {
      const err = validateStep(s);
      if (err) {
        setError(err);
        setCurrentStep(s);
        return;
      }
    }

    setLoading(true);
    setError(null);

    const submitPayload = {
      ...formData,
      age: Number(formData.age),
      sex: Number(formData.sex),
      height_cm: Number(formData.height_cm),
      weight_kg: Number(formData.weight_kg),
      high_bp: Number(formData.high_bp),
      high_chol: Number(formData.high_chol),
      chol_check: Number(formData.chol_check || 1),
      stroke: Number(formData.stroke),
      heart_disease_or_attack: Number(formData.heart_disease_or_attack),
      diff_walk: Number(formData.diff_walk),
      any_healthcare: Number(formData.any_healthcare),
      no_doc_bc_cost: Number(formData.no_doc_bc_cost || 0),
      smoker: Number(formData.smoker),
      hvy_alcohol_consump: Number(formData.hvy_alcohol_consump),
      phys_activity: Number(formData.phys_activity),
      fruits: Number(formData.fruits),
      veggies: Number(formData.veggies),
      gen_hlth: Number(formData.gen_hlth),
      ment_hlth: Number(formData.ment_hlth || 0),
      phys_hlth: Number(formData.phys_hlth || 0),
      ap_hi: Number(formData.ap_hi),
      ap_lo: Number(formData.ap_lo),
      glucose: Number(formData.glucose),
      cholesterol: Number(formData.cholesterol || 1),
      serum_creatinine: Number(formData.serum_creatinine),
      blood_urea: Number(formData.blood_urea),
      hemoglobin: Number(formData.hemoglobin),
      sodium: Number(formData.sodium || 138),
      potassium: Number(formData.potassium || 4.2),
      packed_cell_volume: Number(formData.packed_cell_volume || 40),
      white_blood_cell_count: Number(formData.white_blood_cell_count || 7500),
      red_blood_cell_count: Number(formData.red_blood_cell_count || 4.8)
    };

    try {
      const res = await healthDataAPI.submitRecord(submitPayload);
      setSuccessResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to submit health record. Please check field inputs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full space-y-6 z-10 font-sans pb-12">
      
      {/* 1. HORIZONTAL WIZARD STEP INDICATOR */}
      <div className="w-full bg-slate-950/80 p-3 rounded-2xl border border-slate-800 shadow-xl">
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-2">
          {STEPS.map((s) => {
            const isActive = currentStep === s.id;
            const isPassed = currentStep > s.id;
            return (
              <div
                key={s.id}
                onClick={() => handleStepClick(s.id)}
                className={`p-2.5 rounded-xl text-center font-mono cursor-pointer transition-all duration-300 border ${
                  isActive 
                    ? 'bg-cyan-500/20 border-cyan-400 text-cyan-300 shadow-md shadow-cyan-500/20 scale-102'
                    : isPassed
                    ? 'bg-teal-500/10 border-teal-500/40 text-teal-300'
                    : 'bg-slate-900/60 border-slate-800 text-slate-500'
                }`}
              >
                <div className="text-[10px] font-extrabold truncate">{s.label}</div>
              </div>
            );
          })}
        </div>
      </div>

      {/* ERROR ALERT */}
      {error && (
        <div className="p-3.5 rounded-xl bg-red-500/15 border border-red-500/40 text-red-300 text-xs font-mono flex items-center space-x-2">
          <AlertCircle className="w-4 h-4 text-red-400 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* 2. FORM MAIN WORKSPACE (FULL WIDTH CONTAINER) */}
      <div className="w-full">
        <HolographicHUDPanel 
          title={`STEP 0${currentStep}: ${STEPS[currentStep - 1].label.replace(/^[0-9]+\s*/, '')}`} 
          subtitle="Clinical Data Acquisition & Validation Workspace"
          glowColor="cyan"
        >
          {successResult ? (
            <div className="space-y-6 py-6 font-mono text-xs max-w-2xl mx-auto text-center">
              <div className="p-6 rounded-2xl bg-teal-500/10 border border-teal-400/40 text-teal-300 space-y-3">
                <CheckCircle className="w-12 h-12 text-teal-400 mx-auto" />
                <div className="text-base font-extrabold">PATIENT RECORD #{successResult.id} REGISTERED</div>
                <p className="text-xs text-slate-300">
                  Preprocessed through Module 1 pipelines & persistent in SmartCare DB.
                </p>
              </div>

              <button
                onClick={() => onNavigate && onNavigate('risk')}
                className="w-full py-3.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-extrabold text-xs uppercase tracking-wider transition shadow-lg shadow-cyan-500/20 flex items-center justify-center space-x-2 cursor-pointer"
              >
                <Stethoscope className="w-4 h-4" />
                <span>PROCEED TO AI RISK ASSESSMENT</span>
              </button>
            </div>
          ) : (
            <div className="space-y-6 font-mono text-xs">
              
              {/* STEP 1: PATIENT PROFILE */}
              {currentStep === 1 && (
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1.5 font-bold">AGE (YEARS) *</label>
                    <input
                      type="number"
                      name="age"
                      value={formData.age}
                      onChange={handleChange}
                      placeholder="e.g. 54"
                      className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white font-bold outline-none focus:border-cyan-400"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1.5 font-bold">SEX *</label>
                    <select
                      name="sex"
                      value={formData.sex}
                      onChange={handleChange}
                      className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white font-bold outline-none focus:border-cyan-400"
                    >
                      <option value="">Select Sex...</option>
                      <option value={1}>Male (1)</option>
                      <option value={0}>Female (0)</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1.5 font-bold">HEIGHT (CM) *</label>
                    <input
                      type="number"
                      name="height_cm"
                      value={formData.height_cm}
                      onChange={handleChange}
                      placeholder="e.g. 172"
                      className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white font-bold outline-none focus:border-cyan-400"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1.5 font-bold">WEIGHT (KG) *</label>
                    <input
                      type="number"
                      name="weight_kg"
                      value={formData.weight_kg}
                      onChange={handleChange}
                      placeholder="e.g. 78"
                      className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white font-bold outline-none focus:border-cyan-400"
                    />
                  </div>
                  <div className="col-span-1 sm:col-span-2 md:col-span-4 p-3.5 rounded-xl bg-slate-900 border border-slate-800 flex justify-between items-center">
                    <span className="text-slate-400">CALCULATED BODY MASS INDEX (BMI):</span>
                    <span className="text-cyan-400 font-extrabold text-base">{bmi !== 'N/A' ? `${bmi} kg/m²` : 'Enter Height & Weight'}</span>
                  </div>
                </div>
              )}

              {/* STEP 2: MEDICAL HISTORY */}
              {currentStep === 2 && (
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                  {[
                    { key: 'high_bp', label: 'HIGH BP HISTORY *' },
                    { key: 'high_chol', label: 'HIGH CHOLESTEROL *' },
                    { key: 'stroke', label: 'PREVIOUS STROKE *' },
                    { key: 'heart_disease_or_attack', label: 'CORONARY DISEASE *' },
                    { key: 'diff_walk', label: 'DIFFICULTY WALKING *' },
                    { key: 'any_healthcare', label: 'HEALTHCARE COVERAGE *' }
                  ].map(item => (
                    <div key={item.key} className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 flex justify-between items-center">
                      <span className="text-slate-300 font-bold">{item.label}</span>
                      <select
                        name={item.key}
                        value={formData[item.key]}
                        onChange={handleChange}
                        className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-white outline-none focus:border-cyan-400"
                      >
                        <option value="">Select...</option>
                        <option value={1}>YES (1)</option>
                        <option value={0}>NO (0)</option>
                      </select>
                    </div>
                  ))}
                </div>
              )}

              {/* STEP 3: LIFESTYLE */}
              {currentStep === 3 && (
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                  {[
                    { key: 'smoker', label: 'SMOKER HISTORY *' },
                    { key: 'hvy_alcohol_consump', label: 'HEAVY ALCOHOL *' },
                    { key: 'phys_activity', label: 'PHYSICAL ACTIVITY *' },
                    { key: 'fruits', label: 'DAILY FRUIT *' },
                    { key: 'veggies', label: 'DAILY VEGGIES *' }
                  ].map(item => (
                    <div key={item.key} className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 flex justify-between items-center">
                      <span className="text-slate-300 font-bold">{item.label}</span>
                      <select
                        name={item.key}
                        value={formData[item.key]}
                        onChange={handleChange}
                        className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-white outline-none focus:border-cyan-400"
                      >
                        <option value="">Select...</option>
                        <option value={1}>YES (1)</option>
                        <option value={0}>NO (0)</option>
                      </select>
                    </div>
                  ))}

                  <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 flex justify-between items-center">
                    <span className="text-slate-300 font-bold">GENERAL HEALTH *</span>
                    <select
                      name="gen_hlth"
                      value={formData.gen_hlth}
                      onChange={handleChange}
                      className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-white outline-none focus:border-cyan-400"
                    >
                      <option value="">Select...</option>
                      <option value={1}>1 - Excellent</option>
                      <option value={2}>2 - Very Good</option>
                      <option value={3}>3 - Good</option>
                      <option value={4}>4 - Fair</option>
                      <option value={5}>5 - Poor</option>
                    </select>
                  </div>
                </div>
              )}

              {/* STEP 4: CLINICAL MEASUREMENTS */}
              {currentStep === 4 && (
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1.5 font-bold">SYSTOLIC (AP_HI mmHg) *</label>
                    <input
                      type="number"
                      name="ap_hi"
                      value={formData.ap_hi}
                      onChange={handleChange}
                      placeholder="e.g. 138"
                      className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white font-bold outline-none focus:border-cyan-400"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1.5 font-bold">DIASTOLIC (AP_LO mmHg) *</label>
                    <input
                      type="number"
                      name="ap_lo"
                      value={formData.ap_lo}
                      onChange={handleChange}
                      placeholder="e.g. 88"
                      className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white font-bold outline-none focus:border-cyan-400"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1.5 font-bold">GLUCOSE (BGR mg/dL) *</label>
                    <input
                      type="number"
                      name="glucose"
                      value={formData.glucose}
                      onChange={handleChange}
                      placeholder="e.g. 135"
                      className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white font-bold outline-none focus:border-cyan-400"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1.5 font-bold">CREATININE (SC mg/dL) *</label>
                    <input
                      type="number"
                      step="0.1"
                      name="serum_creatinine"
                      value={formData.serum_creatinine}
                      onChange={handleChange}
                      placeholder="e.g. 1.4"
                      className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white font-bold outline-none focus:border-cyan-400"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1.5 font-bold">BLOOD UREA (BU mg/dL) *</label>
                    <input
                      type="number"
                      name="blood_urea"
                      value={formData.blood_urea}
                      onChange={handleChange}
                      placeholder="e.g. 38"
                      className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white font-bold outline-none focus:border-cyan-400"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1.5 font-bold">HEMOGLOBIN (g/dL) *</label>
                    <input
                      type="number"
                      step="0.1"
                      name="hemoglobin"
                      value={formData.hemoglobin}
                      onChange={handleChange}
                      placeholder="e.g. 13.2"
                      className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white font-bold outline-none focus:border-cyan-400"
                    />
                  </div>
                </div>
              )}

              {/* STEP 5: REVIEW */}
              {currentStep === 5 && (
                <div className="space-y-4">
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    <div className="bg-slate-900 p-3.5 rounded-xl border border-slate-800">
                      <span className="text-[9px] text-slate-400 block">AGE & SEX</span>
                      <div className="text-sm font-bold text-white mt-1">{formData.age || 'Not entered'} yrs / {formData.sex === 1 ? 'Male' : formData.sex === 0 ? 'Female' : 'Not set'}</div>
                    </div>
                    <div className="bg-slate-900 p-3.5 rounded-xl border border-slate-800">
                      <span className="text-[9px] text-slate-400 block">BMI</span>
                      <div className="text-sm font-bold text-cyan-400 mt-1">{bmi}</div>
                    </div>
                    <div className="bg-slate-900 p-3.5 rounded-xl border border-slate-800">
                      <span className="text-[9px] text-slate-400 block">BLOOD PRESSURE</span>
                      <div className="text-sm font-bold text-white mt-1">{formData.ap_hi || '--'} / {formData.ap_lo || '--'} mmHg</div>
                    </div>
                    <div className="bg-slate-900 p-3.5 rounded-xl border border-slate-800">
                      <span className="text-[9px] text-slate-400 block">SERUM CREATININE</span>
                      <div className="text-sm font-bold text-teal-400 mt-1">{formData.serum_creatinine || '--'} mg/dL</div>
                    </div>
                  </div>
                  <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-400">
                    All required clinical parameters validated. Click NEXT STEP to proceed to Step 06 SUBMIT.
                  </div>
                </div>
              )}

              {/* STEP 6: SUBMIT */}
              {currentStep === 6 && (
                <div className="space-y-6 text-center py-4 max-w-xl mx-auto">
                  <div className="p-6 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 space-y-2">
                    <Send className="w-10 h-10 text-cyan-400 mx-auto" />
                    <div className="font-extrabold text-base uppercase">READY TO SUBMIT CLINICAL VECTOR</div>
                    <p className="text-xs text-slate-400">Triggers Module 1 cleaning, scaling, and database persistence</p>
                  </div>

                  <button
                    onClick={handleSubmit}
                    disabled={loading}
                    className="w-full py-3.5 rounded-xl bg-teal-400 hover:bg-teal-300 text-slate-950 font-extrabold text-xs uppercase tracking-wider transition shadow-lg shadow-teal-500/20 flex items-center justify-center space-x-2 cursor-pointer"
                  >
                    {loading ? (
                      <>
                        <RefreshCw className="w-4 h-4 animate-spin" />
                        <span>SUBMITTING VECTOR...</span>
                      </>
                    ) : (
                      <>
                        <Send className="w-4 h-4" />
                        <span>CONFIRM & SUBMIT HEALTH RECORD</span>
                      </>
                    )}
                  </button>
                </div>
              )}

              {/* Navigation Bar */}
              {currentStep < 6 && (
                <div className="flex items-center justify-between pt-6 border-t border-slate-800">
                  {currentStep > 1 ? (
                    <button
                      type="button"
                      onClick={handlePrev}
                      className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 text-xs font-mono font-bold flex items-center space-x-1 cursor-pointer hover:bg-slate-700"
                    >
                      <ArrowLeft className="w-4 h-4" />
                      <span>PREVIOUS</span>
                    </button>
                  ) : <div />}

                  <button
                    type="button"
                    onClick={handleNext}
                    className="px-5 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 text-xs font-mono font-extrabold flex items-center space-x-1.5 shadow-lg shadow-cyan-500/20 cursor-pointer"
                  >
                    <span>NEXT STEP</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              )}

            </div>
          )}
        </HolographicHUDPanel>
      </div>

    </div>
  );
}
