import React, { useState, useEffect } from 'react';
import { riskMonitoringAPI } from '../services/api';
import { 
  Activity, TrendingUp, TrendingDown, Minus, Calendar, ShieldCheck, 
  AlertCircle, Eye, RefreshCw, ArrowLeft, Layers, CheckCircle2, ChevronRight, X
} from 'lucide-react';

export default function RiskHistory({ user, onNavigate }) {
  const [history, setHistory] = useState([]);
  const [trends, setTrends] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedAssessment, setSelectedAssessment] = useState(null);
  const [inspectorLoading, setInspectorLoading] = useState(false);

  const patientId = user?.patient_profile_id || user?.patient_id || user?.patient_profile?.id || user?.id || 1;

  const fetchRiskHistory = async () => {
    setLoading(true);
    setError(null);
    try {
      const [histRes, trendRes, alertRes] = await Promise.all([
        riskMonitoringAPI.getRiskHistory(patientId).catch(() => ({ data: [] })),
        riskMonitoringAPI.getRiskTrends(patientId).catch(() => ({ data: null })),
        riskMonitoringAPI.getPatientAlerts(patientId).catch(() => ({ data: [] }))
      ]);
      setHistory(histRes.data || []);
      setTrends(trendRes.data || null);
      setAlerts(alertRes.data || []);
    } catch (err) {
      console.error("Error fetching risk history:", err);
      setError("Failed to load risk history and trend analysis. Complete a risk assessment first.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRiskHistory();
  }, [patientId]);

  const handleInspectAssessment = async (assessmentId) => {
    setInspectorLoading(true);
    try {
      const res = await riskMonitoringAPI.getAssessmentDetails(assessmentId);
      setSelectedAssessment(res.data);
    } catch (e) {
      console.error("Failed to load assessment details:", e);
    } finally {
      setInspectorLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="w-full min-h-[60vh] flex flex-col items-center justify-center space-y-4 font-mono text-xs">
        <div className="w-12 h-12 rounded-full border-2 border-purple-500 border-t-transparent animate-spin" />
        <div className="text-purple-300 font-bold uppercase tracking-widest animate-pulse">
          LOADING PATIENT RISK MONITORING & HISTORICAL TRENDS...
        </div>
      </div>
    );
  }

  const latestAssessment = history.length > 0 ? history[0] : null;

  return (
    <div className="w-full space-y-8 z-10 font-sans pb-16">
      
      {/* 1. TOP HEADER & NAVIGATION */}
      <div className="bg-gradient-to-r from-[#0D0A1A] via-[#140F2E] to-[#0D0A1A] border border-[#2B2347] rounded-3xl p-6 sm:p-8 shadow-2xl relative overflow-hidden">
        <div className="flex flex-wrap items-center justify-between gap-4 relative z-10">
          <div className="flex items-center space-x-3">
            <div className="p-3 rounded-2xl bg-purple-600/20 border border-purple-500/40 text-purple-300 shadow-lg shadow-purple-900/30">
              <Activity className="w-6 h-6" />
            </div>
            <div>
              <span className="text-[11px] font-mono font-extrabold uppercase tracking-widest text-purple-400 bg-purple-950/60 px-2.5 py-0.5 rounded-md border border-purple-800/50">
                MODULE 5 — RISK MONITORING & DECISION SUPPORT
              </span>
              <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight pt-1">
                Patient Risk History & Trend Analysis
              </h1>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={fetchRiskHistory}
              className="px-3.5 py-1.5 rounded-xl bg-[#1A1536] hover:bg-[#251F4A] border border-[#372E5C] text-slate-200 text-xs font-mono font-bold flex items-center space-x-1.5 transition cursor-pointer shadow-md"
            >
              <RefreshCw className="w-3.5 h-3.5 text-purple-400" />
              <span>Refresh History</span>
            </button>

            {onNavigate && (
              <button
                onClick={() => onNavigate('dashboard')}
                className="px-3.5 py-1.5 rounded-xl bg-purple-600/30 hover:bg-purple-600/40 border border-purple-500/50 text-purple-200 text-xs font-mono font-bold flex items-center space-x-1 transition cursor-pointer"
              >
                <ArrowLeft className="w-3.5 h-3.5" />
                <span>Dashboard</span>
              </button>
            )}
          </div>
        </div>

        <p className="text-sm text-slate-300 max-w-3xl font-sans leading-relaxed pt-4 relative z-10">
          Track longitudinal disease risk trajectories over time across Diabetes, Cardiovascular Disease, and Chronic Kidney Disease. Compare current vs previous assessments with safe clinical decision support.
        </p>
      </div>

      {/* 2. CURRENT RISK SUMMARY CARDS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Diabetes Risk Card */}
        <div className="bg-[#0D0A1A] border border-purple-900/40 rounded-3xl p-6 shadow-xl relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono text-purple-400 font-bold uppercase tracking-wider">DIABETES RISK SCORE</span>
            <span className={`px-2.5 py-1 rounded-full text-[10px] font-mono font-bold border uppercase ${
              latestAssessment?.diabetes?.risk_category === 'HIGH' ? 'bg-rose-950/60 border-rose-700/80 text-rose-300' :
              latestAssessment?.diabetes?.risk_category === 'MODERATE' ? 'bg-amber-950/60 border-amber-700/80 text-amber-300' :
              'bg-emerald-950/60 border-emerald-700/80 text-emerald-300'
            }`}>
              {latestAssessment?.diabetes?.risk_category || 'LOW'}
            </span>
          </div>
          <div className="mt-4 flex items-baseline justify-between">
            <span className="text-4xl font-extrabold text-white font-mono">
              {latestAssessment ? `${latestAssessment.diabetes.risk_percentage}%` : 'N/A'}
            </span>
            {trends?.trends?.diabetes && (
              <span className={`text-xs font-mono font-bold flex items-center space-x-1 ${
                trends.trends.diabetes.trend_status === 'Increasing' ? 'text-amber-400' :
                trends.trends.diabetes.trend_status === 'Decreasing' ? 'text-emerald-400' : 'text-slate-400'
              }`}>
                {trends.trends.diabetes.trend_status === 'Increasing' && <TrendingUp className="w-4 h-4" />}
                {trends.trends.diabetes.trend_status === 'Decreasing' && <TrendingDown className="w-4 h-4" />}
                {trends.trends.diabetes.trend_status === 'Stable' && <Minus className="w-4 h-4" />}
                <span>{trends.trends.diabetes.percentage_point_difference > 0 ? `+${trends.trends.diabetes.percentage_point_difference}%` : `${trends.trends.diabetes.percentage_point_difference}%`}</span>
              </span>
            )}
          </div>
          <p className="text-[11px] text-slate-400 pt-2 font-mono">
            {trends?.trends?.diabetes?.safe_clinical_wording || "Baseline assessment established."}
          </p>
        </div>

        {/* CVD Risk Card */}
        <div className="bg-[#0D0A1A] border border-cyan-900/40 rounded-3xl p-6 shadow-xl relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono text-cyan-400 font-bold uppercase tracking-wider">CVD RISK SCORE</span>
            <span className={`px-2.5 py-1 rounded-full text-[10px] font-mono font-bold border uppercase ${
              latestAssessment?.cvd?.risk_category === 'HIGH' ? 'bg-rose-950/60 border-rose-700/80 text-rose-300' :
              latestAssessment?.cvd?.risk_category === 'MODERATE' ? 'bg-amber-950/60 border-amber-700/80 text-amber-300' :
              'bg-emerald-950/60 border-emerald-700/80 text-emerald-300'
            }`}>
              {latestAssessment?.cvd?.risk_category || 'LOW'}
            </span>
          </div>
          <div className="mt-4 flex items-baseline justify-between">
            <span className="text-4xl font-extrabold text-white font-mono">
              {latestAssessment ? `${latestAssessment.cvd.risk_percentage}%` : 'N/A'}
            </span>
            {trends?.trends?.cvd && (
              <span className={`text-xs font-mono font-bold flex items-center space-x-1 ${
                trends.trends.cvd.trend_status === 'Increasing' ? 'text-amber-400' :
                trends.trends.cvd.trend_status === 'Decreasing' ? 'text-emerald-400' : 'text-slate-400'
              }`}>
                {trends.trends.cvd.trend_status === 'Increasing' && <TrendingUp className="w-4 h-4" />}
                {trends.trends.cvd.trend_status === 'Decreasing' && <TrendingDown className="w-4 h-4" />}
                {trends.trends.cvd.trend_status === 'Stable' && <Minus className="w-4 h-4" />}
                <span>{trends.trends.cvd.percentage_point_difference > 0 ? `+${trends.trends.cvd.percentage_point_difference}%` : `${trends.trends.cvd.percentage_point_difference}%`}</span>
              </span>
            )}
          </div>
          <p className="text-[11px] text-slate-400 pt-2 font-mono">
            {trends?.trends?.cvd?.safe_clinical_wording || "Baseline assessment established."}
          </p>
        </div>

        {/* CKD Risk Card */}
        <div className="bg-[#0D0A1A] border border-teal-900/40 rounded-3xl p-6 shadow-xl relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono text-teal-400 font-bold uppercase tracking-wider">CKD RISK SCORE</span>
            <span className={`px-2.5 py-1 rounded-full text-[10px] font-mono font-bold border uppercase ${
              latestAssessment?.ckd?.risk_category === 'HIGH' ? 'bg-rose-950/60 border-rose-700/80 text-rose-300' :
              latestAssessment?.ckd?.risk_category === 'MODERATE' ? 'bg-amber-950/60 border-amber-700/80 text-amber-300' :
              'bg-emerald-950/60 border-emerald-700/80 text-emerald-300'
            }`}>
              {latestAssessment?.ckd?.risk_category || 'LOW'}
            </span>
          </div>
          <div className="mt-4 flex items-baseline justify-between">
            <span className="text-4xl font-extrabold text-white font-mono">
              {latestAssessment ? `${latestAssessment.ckd.risk_percentage}%` : 'N/A'}
            </span>
            {trends?.trends?.ckd && (
              <span className={`text-xs font-mono font-bold flex items-center space-x-1 ${
                trends.trends.ckd.trend_status === 'Increasing' ? 'text-amber-400' :
                trends.trends.ckd.trend_status === 'Decreasing' ? 'text-emerald-400' : 'text-slate-400'
              }`}>
                {trends.trends.ckd.trend_status === 'Increasing' && <TrendingUp className="w-4 h-4" />}
                {trends.trends.ckd.trend_status === 'Decreasing' && <TrendingDown className="w-4 h-4" />}
                {trends.trends.ckd.trend_status === 'Stable' && <Minus className="w-4 h-4" />}
                <span>{trends.trends.ckd.percentage_point_difference > 0 ? `+${trends.trends.ckd.percentage_point_difference}%` : `${trends.trends.ckd.percentage_point_difference}%`}</span>
              </span>
            )}
          </div>
          <p className="text-[11px] text-slate-400 pt-2 font-mono">
            {trends?.trends?.ckd?.safe_clinical_wording || "Baseline assessment established."}
          </p>
        </div>
      </div>

      {/* 3. CHRONOLOGICAL ASSESSMENT HISTORY TABLE */}
      <div className="bg-[#0D0A1A] border border-[#2B2347] rounded-3xl p-6 shadow-2xl space-y-4">
        <div className="flex items-center justify-between border-b border-[#251F42] pb-4">
          <div className="flex items-center space-x-2">
            <Calendar className="w-5 h-5 text-purple-400" />
            <h2 className="text-lg font-bold text-white tracking-tight">Assessment History & Clinical Log</h2>
          </div>
          <span className="text-xs font-mono text-purple-400 font-bold bg-purple-950/60 px-3 py-1 rounded-full border border-purple-800/40">
            {history.length} Record{history.length === 1 ? '' : 's'} Stored
          </span>
        </div>

        {history.length === 0 ? (
          <div className="py-12 text-center text-slate-400 font-mono text-xs space-y-2">
            <AlertCircle className="w-8 h-8 text-purple-400 mx-auto opacity-60" />
            <p>No historical risk assessments recorded for this patient.</p>
            <button
              onClick={() => onNavigate && onNavigate('risk')}
              className="mt-2 px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold transition cursor-pointer"
            >
              Execute First Assessment
            </button>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono border-collapse">
              <thead>
                <tr className="border-b border-[#251F42] text-slate-400 uppercase tracking-wider text-[10px]">
                  <th className="py-3 px-4">Date & Time</th>
                  <th className="py-3 px-4">Assessment ID</th>
                  <th className="py-3 px-4">Diabetes Risk</th>
                  <th className="py-3 px-4">CVD Risk</th>
                  <th className="py-3 px-4">CKD Risk</th>
                  <th className="py-3 px-4">Alert Status</th>
                  <th className="py-3 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1D1738] text-slate-200">
                {history.map((item) => (
                  <tr key={item.assessment_id} className="hover:bg-[#15102E] transition">
                    <td className="py-3.5 px-4 font-bold text-white">
                      {new Date(item.created_at).toLocaleString()}
                    </td>
                    <td className="py-3.5 px-4 font-mono text-purple-300">
                      {item.assessment_id}
                    </td>
                    <td className="py-3.5 px-4 font-bold">
                      <span className={item.diabetes.risk_category === 'HIGH' ? 'text-rose-400' : 'text-slate-200'}>
                        {item.diabetes.risk_percentage}% ({item.diabetes.risk_category})
                      </span>
                    </td>
                    <td className="py-3.5 px-4 font-bold">
                      <span className={item.cvd.risk_category === 'HIGH' ? 'text-rose-400' : 'text-slate-200'}>
                        {item.cvd.risk_percentage}% ({item.cvd.risk_category})
                      </span>
                    </td>
                    <td className="py-3.5 px-4 font-bold">
                      <span className={item.ckd.risk_category === 'HIGH' ? 'text-rose-400' : 'text-slate-200'}>
                        {item.ckd.risk_percentage}% ({item.ckd.risk_category})
                      </span>
                    </td>
                    <td className="py-3.5 px-4">
                      <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase border ${
                        item.alert_status === 'Clinical Review' ? 'bg-rose-950/60 border-rose-700/80 text-rose-300' :
                        item.alert_status === 'Monitor' ? 'bg-amber-950/60 border-amber-700/80 text-amber-300' :
                        'bg-emerald-950/60 border-emerald-700/80 text-emerald-300'
                      }`}>
                        {item.alert_status}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <button
                        onClick={() => handleInspectAssessment(item.assessment_id)}
                        className="px-3 py-1 rounded-lg bg-purple-600/30 hover:bg-purple-600/50 border border-purple-500/40 text-purple-200 font-bold flex items-center space-x-1 ml-auto transition cursor-pointer"
                      >
                        <Eye className="w-3.5 h-3.5" />
                        <span>Inspect</span>
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* 4. ASSESSMENT DETAILS INSPECTOR MODAL */}
      {selectedAssessment && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-[#0D0A1A] border border-purple-500/50 rounded-3xl max-w-4xl w-full max-h-[90vh] overflow-y-auto p-6 sm:p-8 space-y-6 shadow-2xl relative">
            <div className="flex items-center justify-between border-b border-[#251F42] pb-4">
              <div>
                <span className="text-[10px] font-mono text-purple-400 uppercase font-bold tracking-widest">
                  ASSESSMENT INSPECTOR
                </span>
                <h3 className="text-xl font-extrabold text-white font-mono">
                  {selectedAssessment.assessment_id}
                </h3>
              </div>
              <button
                onClick={() => setSelectedAssessment(null)}
                className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Risk Scores Grid */}
            <div className="grid grid-cols-3 gap-4 font-mono">
              <div className="p-4 rounded-2xl bg-[#14102B] border border-purple-900/50">
                <span className="text-[10px] text-slate-400">DIABETES</span>
                <div className="text-xl font-bold text-white mt-1">
                  {roundPct(selectedAssessment.prediction?.diabetes?.probability)}%
                </div>
              </div>
              <div className="p-4 rounded-2xl bg-[#14102B] border border-cyan-900/50">
                <span className="text-[10px] text-slate-400">CARDIO</span>
                <div className="text-xl font-bold text-white mt-1">
                  {roundPct(selectedAssessment.prediction?.cvd?.probability)}%
                </div>
              </div>
              <div className="p-4 rounded-2xl bg-[#14102B] border border-teal-900/50">
                <span className="text-[10px] text-slate-400">CKD</span>
                <div className="text-xl font-bold text-white mt-1">
                  {roundPct(selectedAssessment.prediction?.ckd?.probability)}%
                </div>
              </div>
            </div>

            {/* Recommendations List */}
            {selectedAssessment.recommendations && selectedAssessment.recommendations.length > 0 && (
              <div className="space-y-3 font-sans">
                <h4 className="text-xs font-mono font-bold text-purple-300 uppercase tracking-wider">
                  PERSISTED WELLNESS RECOMMENDATIONS ({selectedAssessment.recommendations.length})
                </h4>
                <div className="space-y-2 max-h-60 overflow-y-auto pr-2">
                  {selectedAssessment.recommendations.map((rec, i) => (
                    <div key={i} className="p-3 rounded-xl bg-[#15102E] border border-purple-950 text-xs text-slate-200 space-y-1">
                      <div className="font-bold text-purple-300">{rec.category} - {rec.risk_factor}</div>
                      <p>{rec.recommendation}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="flex justify-end pt-2">
              <button
                onClick={() => setSelectedAssessment(null)}
                className="px-5 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-mono font-bold text-xs uppercase tracking-wider transition cursor-pointer"
              >
                Close Inspector
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}

function roundPct(prob) {
  return prob !== undefined ? roundVal(prob * 100, 1) : 0.0;
}

function roundVal(v, dec) {
  return Math.round(v * Math.pow(10, dec)) / Math.pow(10, dec);
}
