import React, { useState } from 'react';
import HolographicHUDPanel from '../components/HolographicHUDPanel';
import { healthDataAPI, api } from '../services/api';
import { 
  Activity, Heart, ShieldAlert, CheckCircle2, ArrowRight, 
  Sparkles, RefreshCw, Cpu, Layers, Sliders, Database, AlertCircle, UserCheck, Zap, HeartHandshake
} from 'lucide-react';

export default function RiskAssessment({ user, onNavigate, currentAssessment, onAssessmentChange }) {
  const [loading, setLoading] = useState(false);
  const [selectedDiseaseTarget, setSelectedDiseaseTarget] = useState('all');
  const [selectedPatient, setSelectedPatient] = useState('new');
  const [assessment, setAssessment] = useState(currentAssessment);
  const [error, setError] = useState(null);

  const DEMO_PROFILES = {
    pat_8942: {
      patient_id: 'PAT-2026-8942',
      age: '56',
      sex: '1',
      height_cm: '172',
      weight_kg: '84',
      ap_hi: '142',
      ap_lo: '92',
      glucose: '148',
      serum_creatinine: '1.55',
      blood_urea: '42',
      hemoglobin: '12.8',
      high_bp: '1',
      high_chol: '1',
      smoker: '1',
      phys_activity: '0'
    },
    pat_3104: {
      patient_id: 'PAT-2026-3104',
      age: '38',
      sex: '0',
      height_cm: '165',
      weight_kg: '62',
      ap_hi: '115',
      ap_lo: '75',
      glucose: '92',
      serum_creatinine: '0.85',
      blood_urea: '22',
      hemoglobin: '14.1',
      high_bp: '0',
      high_chol: '0',
      smoker: '0',
      phys_activity: '1'
    }
  };

  // Form Fields
  const [inputData, setInputData] = useState(DEMO_PROFILES.pat_8942);

  const handlePatientSelect = (val) => {
    setSelectedPatient(val);
    if (val in DEMO_PROFILES) {
      setInputData(DEMO_PROFILES[val]);
    } else if (val === 'new') {
      setInputData({
        age: '', sex: '', height_cm: '', weight_kg: '',
        ap_hi: '', ap_lo: '', glucose: '', serum_creatinine: '',
        blood_urea: '', hemoglobin: '', high_bp: '', high_chol: '',
        smoker: '', phys_activity: ''
      });
    }
  };

  const validateInputs = () => {
    if (inputData.age === '' || isNaN(inputData.age)) return "Please enter patient Age.";
    if (inputData.ap_hi === '' || isNaN(inputData.ap_hi)) return "Please enter Systolic Blood Pressure (ap_hi).";
    if (inputData.glucose === '' || isNaN(inputData.glucose)) return "Please enter Blood Glucose level.";
    if (inputData.serum_creatinine === '' || isNaN(inputData.serum_creatinine)) return "Please enter Serum Creatinine level.";
    if (inputData.high_chol === '') return "Please select High Cholesterol status.";
    if (inputData.smoker === '') return "Please select Smoker status.";
    return null;
  };

  const handleRunAssessment = async () => {
    const valErr = validateInputs();
    if (valErr) {
      setError(valErr);
      return;
    }

    setLoading(true);
    setError(null);

    const payload = {
      age: Number(inputData.age),
      sex: Number(inputData.sex || 1),
      height_cm: Number(inputData.height_cm || 170),
      weight_kg: Number(inputData.weight_kg || 70),
      high_bp: Number(inputData.high_bp || 0),
      high_chol: Number(inputData.high_chol || 0),
      smoker: Number(inputData.smoker || 0),
      phys_activity: Number(inputData.phys_activity || 0),
      ap_hi: Number(inputData.ap_hi),
      ap_lo: Number(inputData.ap_lo || 80),
      glucose: Number(inputData.glucose),
      serum_creatinine: Number(inputData.serum_creatinine),
      blood_urea: Number(inputData.blood_urea || 30),
      hemoglobin: Number(inputData.hemoglobin || 14)
    };

    try {
      await healthDataAPI.submitRecord(payload);
      const predRes = await api.post('/predictions', payload);
      setAssessment(predRes.data);
      if (onAssessmentChange) {
        onAssessmentChange(predRes.data);
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to execute AI Risk Assessment.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full space-y-6 z-10 font-sans pb-12">
      
      {/* 1. TOP TOOLBAR BAR */}
      <div className="w-full bg-slate-950/80 p-3.5 rounded-2xl border border-slate-800 flex flex-wrap items-center justify-between gap-4 font-mono text-xs shadow-xl">
        <div className="flex items-center space-x-4 flex-wrap gap-2">
          {/* Target Disease Selector */}
          <div className="flex items-center space-x-2">
            <span className="text-slate-400 font-bold uppercase text-[10px]">DISEASE TARGET:</span>
            <select
              value={selectedDiseaseTarget}
              onChange={(e) => setSelectedDiseaseTarget(e.target.value)}
              className="bg-slate-900 border border-slate-700 rounded-xl px-3 py-1.5 text-white font-bold outline-none focus:border-cyan-400"
            >
              <option value="all">ALL DISEASES (MULTI-TASK)</option>
              <option value="diabetes">DIABETES MELLITUS ONLY</option>
              <option value="cardio">CARDIOVASCULAR (CVD) ONLY</option>
              <option value="ckd">CHRONIC KIDNEY (CKD) ONLY</option>
            </select>
          </div>

          {/* Patient Selector */}
          <div className="flex items-center space-x-2">
            <span className="text-slate-400 font-bold uppercase text-[10px]">PATIENT PROFILE:</span>
            <select
              value={selectedPatient}
              onChange={(e) => handlePatientSelect(e.target.value)}
              className="bg-slate-900 border border-slate-700 rounded-xl px-3 py-1.5 text-white font-bold outline-none focus:border-cyan-400"
            >
              <option value="pat_8942">DEMO PATIENT (PAT-2026-8942 - HIGH RISK)</option>
              <option value="pat_3104">DEMO PATIENT (PAT-2026-3104 - LOW RISK)</option>
              <option value="new">NEW PATIENT RECORD (LIVE ENTRY)</option>
            </select>
          </div>
        </div>

        <button
          onClick={handleRunAssessment}
          disabled={loading}
          className="px-5 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-extrabold text-xs uppercase tracking-wider transition shadow-lg shadow-cyan-500/20 flex items-center space-x-2 cursor-pointer"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>{loading ? 'RUNNING AI INFERENCE...' : 'RUN RISK ASSESSMENT'}</span>
        </button>
      </div>

      {/* ERROR ALERT */}
      {error && (
        <div className="p-3.5 rounded-xl bg-red-500/15 border border-red-500/40 text-red-300 text-xs font-mono flex items-center space-x-2">
          <AlertCircle className="w-4 h-4 text-red-400 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* 2. MAIN CLINICAL WORKSPACE (LEFT INPUT WORKSPACE + RIGHT LIVE PREDICTION PANEL) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* LEFT COLUMN (60%): PATIENT CLINICAL INPUT WORKSPACE */}
        <div className="lg:col-span-7 space-y-4">
          <HolographicHUDPanel 
            title="PATIENT CLINICAL INPUT WORKSPACE" 
            subtitle="Structured Clinical Vector Input Parameters (All fields required)"
            glowColor="teal"
          >
            <div className="space-y-5 font-mono text-xs">
              
              {/* SECTION 1: DEMOGRAPHICS */}
              <div className="space-y-2">
                <div className="text-[10px] text-cyan-400 font-extrabold uppercase tracking-wider border-b border-slate-800 pb-1 flex items-center justify-between">
                  <span>DEMOGRAPHICS</span>
                  <span className="text-slate-500">4 Parameters</span>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1">AGE (YEARS) *</label>
                    <input
                      type="number"
                      value={inputData.age}
                      onChange={(e) => setInputData({ ...inputData, age: e.target.value })}
                      placeholder="e.g. 54"
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-white font-bold outline-none focus:border-cyan-400"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1">SEX *</label>
                    <select
                      value={inputData.sex}
                      onChange={(e) => setInputData({ ...inputData, sex: e.target.value })}
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-white font-bold outline-none focus:border-cyan-400"
                    >
                      <option value="">Select...</option>
                      <option value={1}>Male (1)</option>
                      <option value={0}>Female (0)</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1">HEIGHT (CM)</label>
                    <input
                      type="number"
                      value={inputData.height_cm}
                      onChange={(e) => setInputData({ ...inputData, height_cm: e.target.value })}
                      placeholder="e.g. 172"
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-white font-bold outline-none focus:border-cyan-400"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1">WEIGHT (KG)</label>
                    <input
                      type="number"
                      value={inputData.weight_kg}
                      onChange={(e) => setInputData({ ...inputData, weight_kg: e.target.value })}
                      placeholder="e.g. 78"
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-white font-bold outline-none focus:border-cyan-400"
                    />
                  </div>
                </div>
              </div>

              {/* SECTION 2: CLINICAL MEASUREMENTS */}
              <div className="space-y-2">
                <div className="text-[10px] text-cyan-400 font-extrabold uppercase tracking-wider border-b border-slate-800 pb-1 flex items-center justify-between">
                  <span>CLINICAL MEASUREMENTS</span>
                  <span className="text-slate-500">6 Biomarkers</span>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1">SYSTOLIC (AP_HI) *</label>
                    <input
                      type="number"
                      value={inputData.ap_hi}
                      onChange={(e) => setInputData({ ...inputData, ap_hi: e.target.value })}
                      placeholder="e.g. 138"
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-white font-bold outline-none focus:border-cyan-400"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1">DIASTOLIC (AP_LO)</label>
                    <input
                      type="number"
                      value={inputData.ap_lo}
                      onChange={(e) => setInputData({ ...inputData, ap_lo: e.target.value })}
                      placeholder="e.g. 88"
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-white font-bold outline-none focus:border-cyan-400"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1">GLUCOSE (BGR) *</label>
                    <input
                      type="number"
                      value={inputData.glucose}
                      onChange={(e) => setInputData({ ...inputData, glucose: e.target.value })}
                      placeholder="e.g. 135"
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-white font-bold outline-none focus:border-cyan-400"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1">CREATININE (SC) *</label>
                    <input
                      type="number"
                      step="0.1"
                      value={inputData.serum_creatinine}
                      onChange={(e) => setInputData({ ...inputData, serum_creatinine: e.target.value })}
                      placeholder="e.g. 1.4"
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-white font-bold outline-none focus:border-cyan-400"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1">BLOOD UREA (BU)</label>
                    <input
                      type="number"
                      value={inputData.blood_urea}
                      onChange={(e) => setInputData({ ...inputData, blood_urea: e.target.value })}
                      placeholder="e.g. 38"
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-white font-bold outline-none focus:border-cyan-400"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1">HEMOGLOBIN (HGB)</label>
                    <input
                      type="number"
                      step="0.1"
                      value={inputData.hemoglobin}
                      onChange={(e) => setInputData({ ...inputData, hemoglobin: e.target.value })}
                      placeholder="e.g. 13.2"
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-white font-bold outline-none focus:border-cyan-400"
                    />
                  </div>
                </div>
              </div>

              {/* SECTION 3: LIFESTYLE / RISK FACTORS */}
              <div className="space-y-2">
                <div className="text-[10px] text-cyan-400 font-extrabold uppercase tracking-wider border-b border-slate-800 pb-1 flex items-center justify-between">
                  <span>LIFESTYLE & RISK FACTORS</span>
                  <span className="text-slate-500">4 Indicators</span>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1">HIGH BP HISTORY *</label>
                    <select
                      value={inputData.high_bp}
                      onChange={(e) => setInputData({ ...inputData, high_bp: e.target.value })}
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-white font-bold outline-none focus:border-cyan-400"
                    >
                      <option value="">Select...</option>
                      <option value={1}>Yes (1)</option>
                      <option value={0}>No (0)</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1">HIGH CHOLESTEROL *</label>
                    <select
                      value={inputData.high_chol}
                      onChange={(e) => setInputData({ ...inputData, high_chol: e.target.value })}
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-white font-bold outline-none focus:border-cyan-400"
                    >
                      <option value="">Select...</option>
                      <option value={1}>Yes (1)</option>
                      <option value={0}>No (0)</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1">SMOKER STATUS *</label>
                    <select
                      value={inputData.smoker}
                      onChange={(e) => setInputData({ ...inputData, smoker: e.target.value })}
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-white font-bold outline-none focus:border-cyan-400"
                    >
                      <option value="">Select...</option>
                      <option value={1}>Yes (1)</option>
                      <option value={0}>No (0)</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-[10px] text-slate-400 mb-1">PHYSICAL ACTIVITY</label>
                    <select
                      value={inputData.phys_activity}
                      onChange={(e) => setInputData({ ...inputData, phys_activity: e.target.value })}
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-white font-bold outline-none focus:border-cyan-400"
                    >
                      <option value="">Select...</option>
                      <option value={1}>Active (1)</option>
                      <option value={0}>Sedentary (0)</option>
                    </select>
                  </div>
                </div>
              </div>

            </div>
          </HolographicHUDPanel>
        </div>

        {/* RIGHT COLUMN (40%): LIVE PREDICTION PANEL */}
        <div className="lg:col-span-5 space-y-4 font-mono text-xs">
          
          {/* DIABETES RESULT MODULE */}
          <HolographicHUDPanel glowColor="cyan" className="p-3.5">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Zap className="w-4 h-4 text-cyan-400" />
                <span className="font-extrabold text-white text-xs">DIABETES MELLITUS</span>
              </div>
              <span className={`px-2 py-0.5 rounded text-[9px] font-bold border ${
                assessment?.predictions?.diabetes?.risk_category === 'HIGH' 
                  ? 'bg-red-500/20 text-red-400 border-red-500/30' 
                  : assessment?.predictions?.diabetes?.risk_category === 'MODERATE'
                  ? 'bg-amber-500/20 text-amber-400 border-amber-500/30'
                  : assessment?.predictions?.diabetes?.risk_category === 'LOW'
                  ? 'bg-teal-500/20 text-teal-300 border-teal-500/30'
                  : 'bg-slate-800 text-slate-400 border-slate-700'
              }`}>
                {assessment?.predictions?.diabetes?.risk_category || 'AWAITING INPUT'}
              </span>
            </div>

            <div className="flex items-baseline justify-between pt-3">
              <span className="text-2xl font-extrabold text-cyan-300">
                {assessment?.predictions?.diabetes?.risk_percentage !== undefined ? `${assessment.predictions.diabetes.risk_percentage}%` : '--'}
              </span>
              <span className="text-[10px] text-slate-400">
                Threshold: {assessment?.predictions?.diabetes?.decision_threshold || '0.50'}
              </span>
            </div>

            <div className="w-full bg-slate-950 rounded-full h-1.5 mt-2 overflow-hidden border border-slate-800">
              <div className="bg-cyan-400 h-full transition-all duration-700" style={{ width: `${assessment?.predictions?.diabetes?.risk_percentage || 0}%` }} />
            </div>

            <div className="flex justify-between items-center text-[9px] text-slate-400 pt-2">
              <span>Model: XGBoost Classifier v1.4</span>
              <span className="text-teal-400 font-bold">{assessment ? 'Calibrated (Isotonic)' : 'Standby'}</span>
            </div>
          </HolographicHUDPanel>

          {/* CVD RESULT MODULE */}
          <HolographicHUDPanel glowColor="red" className="p-3.5">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Heart className="w-4 h-4 text-red-400" />
                <span className="font-extrabold text-white text-xs">CARDIOVASCULAR (CVD)</span>
              </div>
              <span className={`px-2 py-0.5 rounded text-[9px] font-bold border ${
                assessment?.predictions?.cardio?.risk_category === 'HIGH' 
                  ? 'bg-red-500/20 text-red-400 border-red-500/30' 
                  : assessment?.predictions?.cardio?.risk_category === 'MODERATE'
                  ? 'bg-amber-500/20 text-amber-400 border-amber-500/30'
                  : assessment?.predictions?.cardio?.risk_category === 'LOW'
                  ? 'bg-teal-500/20 text-teal-300 border-teal-500/30'
                  : 'bg-slate-800 text-slate-400 border-slate-700'
              }`}>
                {assessment?.predictions?.cardio?.risk_category || 'AWAITING INPUT'}
              </span>
            </div>

            <div className="flex items-baseline justify-between pt-3">
              <span className="text-2xl font-extrabold text-red-400">
                {assessment?.predictions?.cardio?.risk_percentage !== undefined ? `${assessment.predictions.cardio.risk_percentage}%` : '--'}
              </span>
              <span className="text-[10px] text-slate-400">
                Threshold: {assessment?.predictions?.cardio?.decision_threshold || '0.50'}
              </span>
            </div>

            <div className="w-full bg-slate-950 rounded-full h-1.5 mt-2 overflow-hidden border border-slate-800">
              <div className="bg-red-400 h-full transition-all duration-700" style={{ width: `${assessment?.predictions?.cardio?.risk_percentage || 0}%` }} />
            </div>

            <div className="flex justify-between items-center text-[9px] text-slate-400 pt-2">
              <span>Model: Random Forest v1.3</span>
              <span className="text-teal-400 font-bold">{assessment ? 'Calibrated (Platt)' : 'Standby'}</span>
            </div>
          </HolographicHUDPanel>

          {/* CKD RESULT MODULE */}
          <HolographicHUDPanel glowColor="purple" className="p-3.5">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Activity className="w-4 h-4 text-purple-400" />
                <span className="font-extrabold text-white text-xs">CHRONIC KIDNEY (CKD)</span>
              </div>
              <span className={`px-2 py-0.5 rounded text-[9px] font-bold border ${
                assessment?.predictions?.ckd?.risk_category === 'HIGH' 
                  ? 'bg-red-500/20 text-red-400 border-red-500/30' 
                  : assessment?.predictions?.ckd?.risk_category === 'MODERATE'
                  ? 'bg-amber-500/20 text-amber-400 border-amber-500/30'
                  : assessment?.predictions?.ckd?.risk_category === 'LOW'
                  ? 'bg-teal-500/20 text-teal-300 border-teal-500/30'
                  : 'bg-slate-800 text-slate-400 border-slate-700'
              }`}>
                {assessment?.predictions?.ckd?.risk_category || 'AWAITING INPUT'}
              </span>
            </div>

            <div className="flex items-baseline justify-between pt-3">
              <span className="text-2xl font-extrabold text-purple-300">
                {assessment?.predictions?.ckd?.risk_percentage !== undefined ? `${assessment.predictions.ckd.risk_percentage}%` : '--'}
              </span>
              <span className="text-[10px] text-slate-400">
                Threshold: {assessment?.predictions?.ckd?.decision_threshold || '0.50'}
              </span>
            </div>

            <div className="w-full bg-slate-950 rounded-full h-1.5 mt-2 overflow-hidden border border-slate-800">
              <div className="bg-purple-400 h-full transition-all duration-700" style={{ width: `${assessment?.predictions?.ckd?.risk_percentage || 0}%` }} />
            </div>

            <div className="flex justify-between items-center text-[9px] text-slate-400 pt-2">
              <span>Model: Multi-Task Classifier v2.1</span>
              <span className="text-teal-400 font-bold">{assessment ? 'Calibrated (Isotonic)' : 'Standby'}</span>
            </div>
          </HolographicHUDPanel>

          {/* PREDICTION SUMMARY & EXPLAIN THIS RESULT BUTTON */}
          <div className="p-4 rounded-2xl bg-slate-950/80 border border-purple-500/40 space-y-3 shadow-xl">
            <div className="text-[10px] font-bold text-purple-300 uppercase tracking-wider flex items-center justify-between">
              <span>PREDICTION SUMMARY</span>
              <span className={assessment ? "text-teal-400 font-extrabold" : "text-slate-500"}>
                {assessment ? 'VERIFIED' : 'AWAITING RUN'}
              </span>
            </div>

            <p className="text-[11px] text-slate-300 leading-relaxed">
              {assessment 
                ? "Multi-task prediction complete. Review disease risk outcomes above or inspect SHAP feature attributions."
                : "Fill clinical parameters on the left and click RUN RISK ASSESSMENT to execute multi-task risk predictions."
              }
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 pt-1">
              <button
                onClick={() => onNavigate && onNavigate('explain')}
                disabled={!assessment}
                className={`py-2.5 px-3 rounded-xl text-white font-mono font-bold text-xs uppercase tracking-wider transition flex items-center justify-center space-x-2 cursor-pointer ${
                  assessment 
                    ? 'bg-purple-600/80 hover:bg-purple-500 border border-purple-400/50 shadow-lg shadow-purple-600/30' 
                    : 'bg-slate-800 opacity-60 cursor-not-allowed'
                }`}
              >
                <Sparkles className="w-4 h-4 text-purple-200" />
                <span>EXPLAIN RESULT (SHAP)</span>
              </button>

              <button
                onClick={() => onNavigate && onNavigate('wellness')}
                disabled={!assessment}
                className={`py-2.5 px-3 rounded-xl text-slate-950 font-mono font-extrabold text-xs uppercase tracking-wider transition flex items-center justify-center space-x-2 cursor-pointer ${
                  assessment 
                    ? 'bg-gradient-to-r from-amber-400 to-amber-300 hover:from-amber-300 hover:to-amber-200 shadow-lg shadow-amber-400/20' 
                    : 'bg-slate-800 text-slate-400 opacity-60 cursor-not-allowed'
                }`}
              >
                <HeartHandshake className="w-4 h-4 text-slate-950" />
                <span>WELLNESS GUIDANCE</span>
              </button>
            </div>
          </div>

        </div>

      </div>

    </div>
  );
}
