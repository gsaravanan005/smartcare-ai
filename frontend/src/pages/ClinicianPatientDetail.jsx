import React, { useState, useEffect } from 'react';
import { clinicianAPI } from '../services/api';
import { 
  User, Activity, TrendingUp, TrendingDown, Minus, Layers, ShieldCheck, 
  AlertTriangle, ArrowLeft, Send, CheckCircle2, RefreshCw, FileText
} from 'lucide-react';

import ReportViewerModal from '../components/ReportViewerModal';

export default function ClinicianPatientDetail({ patientId, onSelectPatient, onBack }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [feedbackText, setFeedbackText] = useState('');
  const [clinicalAction, setClinicalAction] = useState('Reviewed');
  const [submitting, setSubmitting] = useState(false);
  const [isReportModalOpen, setIsReportModalOpen] = useState(false);
  const [patientRoster, setPatientRoster] = useState([]);

  useEffect(() => {
    clinicianAPI.getPatientList()
      .then(res => setPatientRoster(res.data || []))
      .catch(err => console.error("Could not fetch patient roster for dropdown:", err));
  }, []);

  const fetchDetail = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await clinicianAPI.getPatientDetail(patientId);
      setData(res.data);
    } catch (err) {
      console.error("Error fetching patient clinician detail:", err);
      try {
        const listRes = await clinicianAPI.getPatientList();
        if (listRes.data && listRes.data.length > 0) {
          const firstId = listRes.data[0].patient_id || listRes.data[0].id || 1;
          if (firstId !== patientId) {
            const fallbackRes = await clinicianAPI.getPatientDetail(firstId);
            setData(fallbackRes.data);
            return;
          }
        }
      } catch (fallbackErr) {
        console.error("Fallback patient load failed:", fallbackErr);
      }
      setError("Failed to load patient clinical view.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (patientId) {
      fetchDetail();
    }
  }, [patientId]);

  const handleSubmitFeedback = async (e) => {
    e.preventDefault();
    if (!feedbackText.trim() || !data?.latest_assessment?.assessment_id) return;
    setSubmitting(true);
    try {
      await clinicianAPI.submitFeedback({
        assessment_id: data.latest_assessment.assessment_id,
        patient_id: patientId,
        feedback_text: feedbackText,
        clinical_action: clinicalAction
      });
      setFeedbackText('');
      fetchDetail();
    } catch (err) {
      console.error("Failed to submit clinician feedback:", err);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="w-full min-h-[60vh] flex flex-col items-center justify-center space-y-4 font-mono text-xs">
        <div className="w-12 h-12 rounded-full border-2 border-cyan-500 border-t-transparent animate-spin" />
        <div className="text-cyan-300 font-bold uppercase tracking-widest animate-pulse">
          LOADING CLINICAL TRACE FOR PATIENT #{patientId}...
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="w-full max-w-xl mx-auto mt-12 bg-rose-950/40 border border-rose-800/60 rounded-3xl p-8 text-center space-y-4 font-sans">
        <AlertTriangle className="w-12 h-12 text-rose-400 mx-auto" />
        <h3 className="text-lg font-bold text-white font-mono">Patient View Error</h3>
        <p className="text-xs text-rose-200">{error || "Patient not found."}</p>
        <button
          onClick={onBack}
          className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-xl font-mono text-xs font-bold uppercase tracking-wider transition cursor-pointer"
        >
          Back to Roster
        </button>
      </div>
    );
  }

  const { patient, latest_assessment, history, trends, alerts, feedbacks } = data;

  return (
    <div className="w-full space-y-8 z-10 font-sans pb-16">
      
      {/* 1. PATIENT HEADER & NAVIGATION */}
      <div className="bg-gradient-to-r from-[#080E1E] via-[#0E172E] to-[#080E1E] border border-[#1E2E54] rounded-3xl p-6 sm:p-8 shadow-2xl space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center space-x-3">
            <button
              onClick={onBack}
              className="p-2.5 rounded-2xl bg-[#101B38] hover:bg-[#1A2A54] border border-[#243970] text-slate-300 transition cursor-pointer"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
            <div>
              <span className="text-[10px] font-mono font-extrabold uppercase tracking-widest text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded-md border border-cyan-800/50">
                CLINICAL PATIENT VIEW
              </span>
              <div className="flex items-center space-x-3 pt-1">
                <h1 className="text-2xl font-extrabold text-white tracking-tight">
                  {patient.name}
                </h1>
                {patientRoster.length > 0 && (
                  <select
                    value={patient.id}
                    onChange={(e) => {
                      const selectedId = Number(e.target.value);
                      if (onSelectPatient) onSelectPatient(selectedId);
                    }}
                    className="bg-[#101B38] border border-[#243970] text-cyan-300 font-mono text-xs px-3 py-1.5 rounded-xl focus:outline-none focus:border-cyan-400 cursor-pointer"
                  >
                    {patientRoster.map((p) => (
                      <option key={p.patient_id || p.id} value={p.patient_id || p.id}>
                        Patient #{p.patient_id || p.id} ({p.patient_name})
                      </option>
                    ))}
                  </select>
                )}
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-2 font-mono text-xs text-slate-300">
            <button
              onClick={() => setIsReportModalOpen(true)}
              className="px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-cyan-600 to-teal-600 hover:brightness-110 text-white font-bold flex items-center space-x-1.5 transition cursor-pointer shadow-lg shadow-cyan-900/40"
            >
              <FileText className="w-3.5 h-3.5" />
              <span>VIEW CLINICAL PDF REPORT</span>
            </button>
            <span className="bg-[#101B38] px-3 py-1.5 rounded-xl border border-[#243970]">{patient.age || 'N/A'} yrs</span>
            <span className="bg-[#101B38] px-3 py-1.5 rounded-xl border border-[#243970]">{patient.sex}</span>
            {patient.bmi && <span className="bg-[#101B38] px-3 py-1.5 rounded-xl border border-[#243970]">BMI: {patient.bmi} kg/m²</span>}
          </div>
        </div>
      </div>

      {/* 2. LATEST PREDICTION & TRENDS GRID */}
      {latest_assessment?.prediction && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 font-mono">
          <div className="bg-[#0A1224] border border-purple-900/50 rounded-3xl p-6 shadow-xl">
            <span className="text-xs text-purple-400 font-bold uppercase">DIABETES RISK</span>
            <div className="text-3xl font-extrabold text-white mt-2">
              {roundPct(latest_assessment.prediction.diabetes.probability)}%
            </div>
            <span className="text-xs text-slate-400 mt-1 block">Category: {latest_assessment.prediction.diabetes.risk_category}</span>
          </div>

          <div className="bg-[#0A1224] border border-cyan-900/50 rounded-3xl p-6 shadow-xl">
            <span className="text-xs text-cyan-400 font-bold uppercase">CVD RISK</span>
            <div className="text-3xl font-extrabold text-white mt-2">
              {roundPct(latest_assessment.prediction.cvd.probability)}%
            </div>
            <span className="text-xs text-slate-400 mt-1 block">Category: {latest_assessment.prediction.cvd.risk_category}</span>
          </div>

          <div className="bg-[#0A1224] border border-teal-900/50 rounded-3xl p-6 shadow-xl">
            <span className="text-xs text-teal-400 font-bold uppercase">CKD RISK</span>
            <div className="text-3xl font-extrabold text-white mt-2">
              {roundPct(latest_assessment.prediction.ckd.probability)}%
            </div>
            <span className="text-xs text-slate-400 mt-1 block">Category: {latest_assessment.prediction.ckd.risk_category}</span>
          </div>
        </div>
      )}

      {/* 3. SHAP EXPLANATION SUMMARY FOR CLINICIAN */}
      {latest_assessment?.shap_factors && latest_assessment.shap_factors.length > 0 && (
        <div className="bg-[#0A1224] border border-[#1C2C52] rounded-3xl p-6 shadow-2xl space-y-4">
          <div className="flex items-center space-x-2 border-b border-[#1C2C52] pb-4">
            <Layers className="w-5 h-5 text-cyan-400" />
            <h2 className="text-lg font-bold text-white tracking-tight font-mono">
              SHAP Risk Factor Attribution Summary
            </h2>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 font-mono text-xs">
            {latest_assessment.shap_factors.map((sf, idx) => (
              <div key={idx} className="p-3.5 rounded-2xl bg-[#111A33] border border-[#1E2E54] flex items-center justify-between">
                <div>
                  <div className="font-bold text-white uppercase">{sf.feature_name}</div>
                  <div className="text-[11px] text-slate-400">Patient Value: {sf.patient_value || 'N/A'}</div>
                </div>
                <div className="text-right">
                  <span className={`font-bold px-2 py-0.5 rounded text-[10px] ${sf.direction === 'RISK_INCREASING' ? 'bg-rose-950 text-rose-300 border border-rose-800' : 'bg-emerald-950 text-emerald-300 border border-emerald-800'}`}>
                    {sf.direction === 'RISK_INCREASING' ? `+${roundVal(sf.abs_shap_value, 4)} SHAP` : `-${roundVal(sf.abs_shap_value, 4)} SHAP`}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 4. CLINICIAN FEEDBACK FORM & HISTORY */}
      <div className="bg-[#0A1224] border border-cyan-900/40 rounded-3xl p-6 sm:p-8 shadow-2xl space-y-6">
        <div className="flex items-center space-x-2 border-b border-[#1C2C52] pb-4">
          <FileText className="w-5 h-5 text-cyan-400" />
          <h2 className="text-lg font-bold text-white tracking-tight font-mono">
            Clinician Review Notes & Recommendations
          </h2>
        </div>

        {/* Feedback Form */}
        <form onSubmit={handleSubmitFeedback} className="space-y-4">
          <div className="space-y-1">
            <label className="text-xs font-mono font-bold text-slate-300">Clinician Assessment Notes</label>
            <textarea
              rows={3}
              value={feedbackText}
              onChange={(e) => setFeedbackText(e.target.value)}
              placeholder="Enter professional clinical notes, observations, or recommended follow-up..."
              className="w-full bg-[#111A33] border border-[#243970] rounded-2xl p-3 text-xs text-white placeholder-slate-400 font-sans focus:outline-none focus:border-cyan-400"
              required
            />
          </div>

          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="space-y-1">
              <label className="text-xs font-mono font-bold text-slate-300">Clinical Action</label>
              <select
                value={clinicalAction}
                onChange={(e) => setClinicalAction(e.target.value)}
                className="bg-[#111A33] border border-[#243970] text-xs text-white font-mono rounded-xl px-3 py-2 focus:outline-none focus:border-cyan-400"
              >
                <option value="Reviewed">Reviewed</option>
                <option value="Follow-up Recommended">Follow-up Recommended</option>
                <option value="Continue Monitoring">Continue Monitoring</option>
                <option value="No Further Action">No Further Action</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={submitting || !feedbackText.trim()}
              className="px-5 py-2.5 rounded-xl bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-white font-mono font-bold text-xs uppercase tracking-wider flex items-center space-x-2 transition cursor-pointer shadow-lg shadow-cyan-900/30"
            >
              <Send className="w-4 h-4" />
              <span>{submitting ? 'Logging...' : 'Submit Clinical Review'}</span>
            </button>
          </div>
        </form>

        {/* Log History */}
        {feedbacks && feedbacks.length > 0 && (
          <div className="space-y-3 pt-4 border-t border-[#1C2C52]">
            <h4 className="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider">
              Previous Clinician Reviews ({feedbacks.length})
            </h4>
            <div className="space-y-2">
              {feedbacks.map((f) => (
                <div key={f.id} className="p-4 rounded-2xl bg-[#111A33] border border-[#1E2E54] text-xs space-y-1 font-sans">
                  <div className="flex items-center justify-between font-mono text-[11px]">
                    <span className="font-bold text-cyan-300">Action: {f.clinical_action}</span>
                    <span className="text-slate-400">{new Date(f.created_at).toLocaleString()}</span>
                  </div>
                  <p className="text-slate-200 pt-1">{f.feedback_text}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <ReportViewerModal
        isOpen={isReportModalOpen}
        onClose={() => setIsReportModalOpen(false)}
        patientId={patientId}
        predictionId={latest_assessment?.assessment_id || latest_assessment?.prediction_id}
      />
    </div>
  );
}

function roundPct(prob) {
  return prob !== undefined ? Math.round(prob * 1000) / 10 : 0.0;
}

function roundVal(v, dec) {
  return Math.round(v * Math.pow(10, dec)) / Math.pow(10, dec);
}
