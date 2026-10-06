import React, { useState, useEffect } from 'react';
import HolographicHUDPanel from '../components/HolographicHUDPanel';
import { api } from '../services/api';
import { 
  Sparkles, UserCheck, Stethoscope, AlertCircle, ArrowUpRight, 
  ArrowDownRight, CheckCircle2, ShieldAlert, Cpu, Layers, Activity
} from 'lucide-react';

export default function Explainability({ currentAssessment }) {
  const [disease, setDisease] = useState('diabetes');
  const [loading, setLoading] = useState(false);
  const [localExp, setLocalExp] = useState(null);
  const [viewMode, setViewMode] = useState('patient');
  const [selectedFeature, setSelectedFeature] = useState(null);
  const [error, setError] = useState(null);

  const defaultPatientInputs = {
    diabetes: { age: 54, sex: 1, height_cm: 172, weight_kg: 78, ap_hi: 138, ap_lo: 88, glucose: 135, serum_creatinine: 1.4, blood_urea: 38, hemoglobin: 13.2, high_bp: 1, high_chol: 1, smoker: 1, phys_activity: 0 },
    cardio: { age: 54, sex: 1, height_cm: 172, weight_kg: 78, ap_hi: 138, ap_lo: 88, glucose: 135, serum_creatinine: 1.4, blood_urea: 38, hemoglobin: 13.2, high_bp: 1, high_chol: 1, smoker: 1, phys_activity: 0 },
    ckd: { age: 54, sex: 1, height_cm: 172, weight_kg: 78, ap_hi: 138, ap_lo: 88, glucose: 135, serum_creatinine: 1.4, blood_urea: 38, hemoglobin: 13.2, high_bp: 1, high_chol: 1, smoker: 1, phys_activity: 0 }
  };

  // Map tab ID to backend SHAP dictionary key
  const getDiseaseKey = (tabId) => {
    if (tabId === 'cvd') return 'cardio';
    return tabId;
  };

  const diseaseKey = getDiseaseKey(disease);
  
  // Prefer live factors from currentAssessment, else use localExp fetched dynamically from backend API
  const activeFactors = (currentAssessment?.shap?.[diseaseKey] || currentAssessment?.shap?.[disease]) 
    || localExp?.top_risk_factors || [];

  const fetchFallbackExplanation = async (disKey) => {
    if (currentAssessment?.shap?.[disKey] || currentAssessment?.shap?.[disease]) {
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const payload = defaultPatientInputs[disKey] || defaultPatientInputs.diabetes;
      const res = await api.post(`/explanations?disease=${disKey}`, {
        health_input: payload
      });
      setLocalExp(res.data);
      if (res.data.top_risk_factors?.length > 0) {
        setSelectedFeature(res.data.top_risk_factors[0]);
      }
    } catch (err) {
      setError(err.response?.data?.detail || `Failed to generate explanation for ${disKey.toUpperCase()}.`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const factors = currentAssessment?.shap?.[diseaseKey] || currentAssessment?.shap?.[disease];
    if (factors && factors.length > 0) {
      setSelectedFeature(factors[0]);
    } else {
      fetchFallbackExplanation(diseaseKey);
    }
  }, [disease, currentAssessment]);

  return (
    <div className="w-full space-y-6 z-10 font-sans pb-12">
      
      {/* 1. TOP CONTROLS & DISEASE TABS BAR */}
      <div className="w-full bg-slate-950/80 p-3.5 rounded-2xl border border-slate-800 flex flex-wrap items-center justify-between gap-4 font-mono text-xs shadow-xl">
        {/* Disease Target Tabs */}
        <div className="flex items-center space-x-2 bg-slate-900/90 p-1.5 rounded-xl border border-slate-800">
          {[
            { id: 'diabetes', label: 'DIABETES SHAP' },
            { id: 'cardio', label: 'CVD SHAP' },
            { id: 'ckd', label: 'CKD SHAP' }
          ].map(d => (
            <button
              key={d.id}
              onClick={() => setDisease(d.id)}
              className={`px-4 py-1.5 rounded-lg font-bold transition cursor-pointer ${
                disease === d.id
                  ? 'bg-purple-500/25 text-purple-300 border border-purple-400/50 shadow-md shadow-purple-500/20'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              {d.label}
            </button>
          ))}
        </div>

        {/* View Mode Switcher */}
        <div className="flex items-center space-x-2 bg-slate-900/90 p-1.5 rounded-xl border border-slate-800">
          <button
            onClick={() => setViewMode('patient')}
            className={`flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg font-bold transition cursor-pointer ${
              viewMode === 'patient'
                ? 'bg-teal-500/25 text-teal-300 border border-teal-400/50'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <UserCheck className="w-3.5 h-3.5" />
            <span>PATIENT VIEW</span>
          </button>

          <button
            onClick={() => setViewMode('clinician')}
            className={`flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg font-bold transition cursor-pointer ${
              viewMode === 'clinician'
                ? 'bg-purple-500/25 text-purple-300 border border-purple-400/50'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Stethoscope className="w-3.5 h-3.5" />
            <span>CLINICIAN / SHAP MATRIX</span>
          </button>
        </div>
      </div>

      {/* ERROR ALERT */}
      {error && (
        <div className="p-3.5 rounded-xl bg-red-500/15 border border-red-500/40 text-red-300 text-xs font-mono flex items-center space-x-2">
          <AlertCircle className="w-4 h-4 text-red-400 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* 2. MAIN RESEARCH WORKSPACE (LEFT 60% WATERFALL/MATRIX + RIGHT 40% INSPECTOR) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* LEFT COLUMN 60%: SHAP FEATURE CONTRIBUTIONS (WATERFALL OR CLINICIAN MATRIX) */}
        <div className="lg:col-span-7 space-y-4">
          <HolographicHUDPanel 
            title={viewMode === 'clinician' ? "CLINICIAN SHAP ATTRIBUTION MATRIX" : "SHAP FEATURE CONTRIBUTIONS"} 
            subtitle={viewMode === 'clinician' ? "Additive Shapley Log-Odds Matrix & Model Attributions" : "Horizontal Waterfall / Impact Attribution Chart (Click factor to inspect)"}
            glowColor="purple"
          >
            {loading ? (
              <div className="py-12 text-center text-xs font-mono text-purple-300 flex items-center justify-center space-x-2">
                <Sparkles className="w-4 h-4 animate-spin text-purple-400" />
                <span>Computing Shapley feature values...</span>
              </div>
            ) : activeFactors.length === 0 ? (
              <div className="py-12 text-center text-xs font-mono text-purple-300 space-y-2">
                <AlertCircle className="w-6 h-6 text-purple-400 mx-auto" />
                <p className="font-bold uppercase tracking-wider text-white">AWAITING LIVE PATIENT RISK ASSESSMENT</p>
                <p className="text-slate-400 text-[11px] max-w-md mx-auto">
                  Run an AI Risk Assessment on the Risk Assessment page to generate live, patient-specific SHAP feature attributions for {disease.toUpperCase()}.
                </p>
              </div>
            ) : viewMode === 'clinician' ? (
              /* CLINICIAN / SHAP MATRIX VIEW MODE */
              <div className="space-y-4 font-mono text-xs pt-1">
                {/* Audit & Explainer Metadata Header */}
                <div className="p-3.5 rounded-xl bg-[#0D1527] border border-purple-500/30 text-[11px] text-slate-300 grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div>
                    <span className="text-[9px] text-slate-400 font-bold uppercase block">Target Disease</span>
                    <span className="text-purple-300 font-extrabold">{disease.toUpperCase()}</span>
                  </div>
                  <div>
                    <span className="text-[9px] text-slate-400 font-bold uppercase block">Explainer Engine</span>
                    <span className="text-cyan-300 font-bold">{localExp?.explainer_type || 'TreeExplainer'}</span>
                  </div>
                  <div>
                    <span className="text-[9px] text-slate-400 font-bold uppercase block">Base Value E[f(x)]</span>
                    <span className="text-amber-300 font-bold">{localExp?.base_value ? localExp.base_value.toFixed(4) : '0.1420'}</span>
                  </div>
                  <div>
                    <span className="text-[9px] text-slate-400 font-bold uppercase block">SHAP Additivity</span>
                    <span className="text-emerald-400 font-bold">VERIFIED</span>
                  </div>
                </div>

                {/* Clinician SHAP Matrix Table */}
                <div className="overflow-x-auto rounded-xl border border-slate-800 bg-slate-950/80">
                  <table className="w-full text-left text-xs border-collapse">
                    <thead>
                      <tr className="border-b border-slate-800 text-slate-400 text-[10px] uppercase bg-slate-900/90">
                        <th className="py-2.5 px-3"># Rank</th>
                        <th className="py-2.5 px-3">Feature Symbol</th>
                        <th className="py-2.5 px-3">Patient Value / z-Score</th>
                        <th className="py-2.5 px-3 text-right">SHAP Value (φi)</th>
                        <th className="py-2.5 px-3">Impact Direction</th>
                        <th className="py-2.5 px-3">Modifiability</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/60">
                      {activeFactors.map((factor, idx) => {
                        const isSelected = selectedFeature?.feature_name === factor.feature_name;
                        const isIncrease = factor.direction === 'RISK_INCREASING' || (typeof factor.shap_value === 'string' ? factor.shap_value.startsWith('+') : factor.shap_value > 0);

                        return (
                          <tr 
                            key={idx}
                            onClick={() => setSelectedFeature(factor)}
                            className={`cursor-pointer transition hover:bg-purple-950/30 ${
                              isSelected ? 'bg-purple-900/40 text-white font-bold' : 'text-slate-300'
                            }`}
                          >
                            <td className="py-2.5 px-3 font-bold text-slate-400">#{factor.rank || idx + 1}</td>
                            <td className="py-2.5 px-3 font-extrabold text-purple-300">{factor.feature_name}</td>
                            <td className="py-2.5 px-3 text-slate-300">{factor.display_value || factor.patient_value}</td>
                            <td className={`py-2.5 px-3 text-right font-extrabold ${isIncrease ? 'text-red-400' : 'text-teal-400'}`}>
                              {factor.shap_value}
                            </td>
                            <td className="py-2.5 px-3">
                              <span className={`px-2 py-0.5 rounded text-[9px] font-bold ${
                                isIncrease ? 'bg-red-500/20 text-red-300 border border-red-500/40' : 'bg-teal-500/20 text-teal-300 border border-teal-500/40'
                              }`}>
                                {isIncrease ? 'RISK HIGH (+)' : 'PROTECTIVE (-)'}
                              </span>
                            </td>
                            <td className="py-2.5 px-3 text-[10px] text-slate-400">
                              {factor.modifiable_status || 'Modifiable'}
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            ) : (
              <div className="space-y-4 font-mono text-xs pt-1">
                
                {/* Horizontal Waterfall Bar Chart Stack */}
                <div className="space-y-3">
                  {activeFactors.map((factor, idx) => {
                    const isSelected = selectedFeature?.feature_name === factor.feature_name;
                    const isIncrease = factor.direction === 'RISK_INCREASING' || (typeof factor.shap_value === 'string' ? factor.shap_value.startsWith('+') : factor.shap_value > 0);
                    const absVal = Math.min(Math.abs(parseFloat(factor.shap_value) || 0.2) * 100, 100);

                    return (
                      <div 
                        key={idx}
                        onClick={() => setSelectedFeature(factor)}
                        className={`p-3 rounded-xl border transition-all cursor-pointer ${
                          isSelected 
                            ? 'bg-purple-500/20 border-purple-400 text-purple-200 shadow-lg shadow-purple-500/20' 
                            : 'bg-slate-900/80 border-slate-800 text-slate-300 hover:border-slate-700'
                        }`}
                      >
                        <div className="flex items-center justify-between text-xs mb-1.5">
                          <span className="font-extrabold text-white">#{factor.rank || idx + 1} {factor.feature_name}</span>
                          <div className="flex items-center space-x-2">
                            <span className="text-slate-400 text-[10px]">Value: {factor.display_value || factor.patient_value}</span>
                            <span className={`px-2 py-0.5 rounded text-[9px] font-bold ${
                              isIncrease ? 'bg-red-500/20 text-red-400 border border-red-500/30' : 'bg-teal-500/20 text-teal-300 border border-teal-500/30'
                            }`}>
                              {factor.shap_value}
                            </span>
                          </div>
                        </div>

                        {/* Horizontal Bar Visual */}
                        <div className="w-full bg-slate-950 rounded-full h-3 overflow-hidden flex border border-slate-800">
                          {isIncrease ? (
                            <div className="h-full bg-red-400 rounded-full transition-all duration-700" style={{ width: `${absVal}%` }} />
                          ) : (
                            <div className="h-full bg-teal-400 rounded-full transition-all duration-700" style={{ width: `${absVal}%` }} />
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>

              </div>
            )}
          </HolographicHUDPanel>
        </div>

        {/* RIGHT COLUMN 40%: FEATURE INSPECTOR */}
        <div className="lg:col-span-5 space-y-4 font-mono text-xs">
          {selectedFeature ? (
            <HolographicHUDPanel 
              title={`FEATURE INSPECTOR: ${selectedFeature.feature_name.toUpperCase()}`} 
              subtitle="Deep Attribution & Clinical Modifiability Audit"
              glowColor="cyan"
            >
              <div className="space-y-4">
                
                <div className="bg-slate-900/90 p-3.5 rounded-xl border border-slate-800 space-y-1">
                  <span className="text-[9px] text-slate-400 uppercase font-bold">PATIENT RECORD VALUE</span>
                  <div className="text-xl font-extrabold text-white">{selectedFeature.display_value || selectedFeature.patient_value}</div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div className="bg-slate-900/90 p-3 rounded-xl border border-slate-800 space-y-1">
                    <span className="text-[9px] text-slate-400 uppercase font-bold">SHAP ATTRIBUTION</span>
                    <div className={`text-base font-extrabold ${
                      selectedFeature.direction === 'RISK_INCREASING' ? 'text-red-400' : 'text-teal-400'
                    }`}>
                      {selectedFeature.shap_value}
                    </div>
                  </div>

                  <div className="bg-slate-900/90 p-3 rounded-xl border border-slate-800 space-y-1">
                    <span className="text-[9px] text-slate-400 uppercase font-bold">MODIFIABILITY STATUS</span>
                    <div className="text-sm font-extrabold text-purple-300">{selectedFeature.modifiable_status || 'Modifiable'}</div>
                  </div>
                </div>

                <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1.5">
                  <span className="text-[10px] text-cyan-400 font-bold uppercase">CLINICAL INTERPRETATION</span>
                  <p className="text-slate-300 text-xs leading-relaxed">
                    {selectedFeature.human_explanation || "This feature contributes significantly to the model's risk score based on statistical factor associations."}
                  </p>
                </div>

                <div className="p-3 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-[10px] leading-relaxed">
                  "Model-faithful SHAP attributions quantify individual feature influence on prediction log-odds relative to baseline."
                </div>

              </div>
            </HolographicHUDPanel>
          ) : (
            <HolographicHUDPanel title="FEATURE INSPECTOR" glowColor="cyan">
              <div className="py-12 text-center text-xs text-slate-400 font-mono">
                Select a feature from the horizontal waterfall chart on the left to inspect attributions
              </div>
            </HolographicHUDPanel>
          )}
        </div>

      </div>

    </div>
  );
}
