import React, { useState, useEffect } from 'react';
import HolographicHUDPanel from '../components/HolographicHUDPanel';
import { dashboardAPI, healthDataAPI } from '../services/api';
import { 
  Heart, Activity, Zap, Cpu, Database, ShieldCheck, 
  Sparkles, CheckCircle2, RefreshCw, AlertCircle, ArrowUpRight, User, ArrowRight,
  BarChart2, FileText, Layers, CheckSquare, Eye, Sliders, TrendingUp, TrendingDown, Stethoscope,
  Clock, HelpCircle, MessageSquare, AlertTriangle, ChevronRight, Compass
} from 'lucide-react';

import ReportViewerModal from '../components/ReportViewerModal';

export default function DashboardOverview({ user, onNavigate }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isReportModalOpen, setIsReportModalOpen] = useState(false);

  const fetchOverview = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await dashboardAPI.getOverview();
      setData(res.data);
    } catch (e) {
      console.error("Dashboard overview load error:", e);
      setError("Unable to query live health overview. Complete a Patient Data entry to activate predictions.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOverview();
  }, []);

  const patientName = data?.patient_name || user?.full_name || user?.username || 'Patient';
  const risks = data?.disease_risks || {};
  const trends = data?.risk_trends?.trends || {};
  const topFactors = data?.top_risk_factors || [];
  const wellnessPreview = data?.wellness_preview;
  const alerts = data?.open_alerts || [];
  const totalAssessments = data?.total_assessments || 0;
  const assessmentDate = data?.latest_assessment_date;

  if (loading) {
    return (
      <div className="w-full min-h-[60vh] flex flex-col items-center justify-center space-y-4 font-mono text-xs text-purple-400">
        <div className="w-12 h-12 rounded-full border-2 border-purple-500 border-t-transparent animate-spin" />
        <div className="text-purple-300 font-bold uppercase tracking-widest animate-pulse">
          INITIALIZING SMARTCARE AI HEALTH INTELLIGENCE DASHBOARD...
        </div>
      </div>
    );
  }

  return (
    <div className="w-full space-y-6 z-10 font-sans pb-16">
      
      {/* 1. WELCOME SECTION */}
      <div className="bg-gradient-to-r from-[#0D0A1A] via-[#141025] to-[#0D0A1A] border border-[#29213F] rounded-3xl p-6 shadow-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4 select-none">
        <div className="space-y-1">
          <div className="flex items-center space-x-2 text-xs font-mono text-purple-400">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
            <span className="font-bold uppercase tracking-widest text-emerald-400">CLINICAL OPERATING SYSTEM ONLINE</span>
          </div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
            Welcome back, {patientName}
          </h1>
          <p className="text-xs text-slate-300 font-sans">
            Your SmartCare AI health overview & multi-task risk intelligence telemetry.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2 font-mono text-xs">
          <button
            onClick={() => setIsReportModalOpen(true)}
            className="px-4 py-2 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:brightness-110 text-white font-bold tracking-wider flex items-center space-x-1.5 transition cursor-pointer shadow-lg shadow-emerald-900/40"
          >
            <FileText className="w-3.5 h-3.5" />
            <span>VIEW HEALTH REPORT (PDF)</span>
          </button>

          <button
            onClick={() => onNavigate && onNavigate('risk')}
            className="px-4 py-2 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold tracking-wider flex items-center space-x-1.5 transition cursor-pointer shadow-lg shadow-purple-900/40"
          >
            <Activity className="w-3.5 h-3.5" />
            <span>New Risk Assessment</span>
          </button>
        </div>
      </div>

      {/* 2. CURRENT RISK SUMMARY CARDS (DIABETES, CVD, CKD) */}
      <div>
        <div className="flex items-center justify-between mb-3 font-mono text-xs">
          <div className="flex items-center space-x-2 font-bold text-white uppercase tracking-wider">
            <Zap className="w-4 h-4 text-cyan-400" />
            <span>Current Estimated Risk Summary</span>
          </div>
          {assessmentDate && (
            <div className="text-slate-400 text-[11px]">
              Last assessed: <span className="text-purple-300 font-bold">{assessmentDate}</span>
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          
          {/* DIABETES RISK CARD */}
          <HolographicHUDPanel glowColor="cyan" className="p-5 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono text-slate-300 font-bold uppercase tracking-wider">Diabetes Risk</span>
                <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-extrabold border uppercase ${
                  risks?.diabetes?.category === 'HIGH'
                    ? 'bg-rose-500/20 text-rose-300 border-rose-500/40'
                    : risks?.diabetes?.category === 'MODERATE'
                    ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                    : 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                }`}>
                  {risks?.diabetes?.category || 'N/A'}
                </span>
              </div>

              <div className="mt-3 flex items-baseline justify-between">
                <div className="text-4xl font-extrabold text-white font-mono">
                  {risks?.diabetes?.percentage !== undefined ? `${risks.diabetes.percentage}%` : 'N/A'}
                </div>
                <div className="text-[10px] font-mono text-slate-400">
                  Model-based estimate
                </div>
              </div>

              <div className="w-full bg-slate-900 rounded-full h-2 mt-3 overflow-hidden">
                <div 
                  className={`h-full transition-all duration-500 ${
                    (risks?.diabetes?.percentage || 0) > 60 ? 'bg-rose-500' : (risks?.diabetes?.percentage || 0) > 30 ? 'bg-amber-500' : 'bg-emerald-400'
                  }`}
                  style={{ width: `${Math.min(100, risks?.diabetes?.percentage || 0)}%` }}
                />
              </div>
            </div>

            <button
              onClick={() => onNavigate && onNavigate('risk')}
              className="mt-4 w-full py-2 rounded-xl bg-[#111025] hover:bg-[#1C1633] border border-[#29213F] text-xs font-mono font-bold text-slate-300 hover:text-white transition flex items-center justify-center space-x-1 cursor-pointer"
            >
              <span>View Details</span>
              <ChevronRight className="w-3.5 h-3.5 text-cyan-400" />
            </button>
          </HolographicHUDPanel>

          {/* CARDIOVASCULAR (CVD) RISK CARD */}
          <HolographicHUDPanel glowColor="purple" className="p-5 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono text-slate-300 font-bold uppercase tracking-wider">CVD Risk</span>
                <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-extrabold border uppercase ${
                  risks?.cvd?.category === 'HIGH'
                    ? 'bg-rose-500/20 text-rose-300 border-rose-500/40'
                    : risks?.cvd?.category === 'MODERATE'
                    ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                    : 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                }`}>
                  {risks?.cvd?.category || 'N/A'}
                </span>
              </div>

              <div className="mt-3 flex items-baseline justify-between">
                <div className="text-4xl font-extrabold text-white font-mono">
                  {risks?.cvd?.percentage !== undefined ? `${risks.cvd.percentage}%` : 'N/A'}
                </div>
                <div className="text-[10px] font-mono text-slate-400">
                  Model-based estimate
                </div>
              </div>

              <div className="w-full bg-slate-900 rounded-full h-2 mt-3 overflow-hidden">
                <div 
                  className={`h-full transition-all duration-500 ${
                    (risks?.cvd?.percentage || 0) > 60 ? 'bg-rose-500' : (risks?.cvd?.percentage || 0) > 30 ? 'bg-amber-500' : 'bg-emerald-400'
                  }`}
                  style={{ width: `${Math.min(100, risks?.cvd?.percentage || 0)}%` }}
                />
              </div>
            </div>

            <button
              onClick={() => onNavigate && onNavigate('risk')}
              className="mt-4 w-full py-2 rounded-xl bg-[#111025] hover:bg-[#1C1633] border border-[#29213F] text-xs font-mono font-bold text-slate-300 hover:text-white transition flex items-center justify-center space-x-1 cursor-pointer"
            >
              <span>View Details</span>
              <ChevronRight className="w-3.5 h-3.5 text-purple-400" />
            </button>
          </HolographicHUDPanel>

          {/* CHRONIC KIDNEY DISEASE (CKD) RISK CARD */}
          <HolographicHUDPanel glowColor="teal" className="p-5 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono text-slate-300 font-bold uppercase tracking-wider">CKD Risk</span>
                <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-extrabold border uppercase ${
                  risks?.ckd?.category === 'HIGH'
                    ? 'bg-rose-500/20 text-rose-300 border-rose-500/40'
                    : risks?.ckd?.category === 'MODERATE'
                    ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                    : 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                }`}>
                  {risks?.ckd?.category || 'N/A'}
                </span>
              </div>

              <div className="mt-3 flex items-baseline justify-between">
                <div className="text-4xl font-extrabold text-white font-mono">
                  {risks?.ckd?.percentage !== undefined ? `${risks.ckd.percentage}%` : 'N/A'}
                </div>
                <div className="text-[10px] font-mono text-slate-400">
                  Model-based estimate
                </div>
              </div>

              <div className="w-full bg-slate-900 rounded-full h-2 mt-3 overflow-hidden">
                <div 
                  className={`h-full transition-all duration-500 ${
                    (risks?.ckd?.percentage || 0) > 60 ? 'bg-rose-500' : (risks?.ckd?.percentage || 0) > 30 ? 'bg-amber-500' : 'bg-emerald-400'
                  }`}
                  style={{ width: `${Math.min(100, risks?.ckd?.percentage || 0)}%` }}
                />
              </div>
            </div>

            <button
              onClick={() => onNavigate && onNavigate('risk')}
              className="mt-4 w-full py-2 rounded-xl bg-[#111025] hover:bg-[#1C1633] border border-[#29213F] text-xs font-mono font-bold text-slate-300 hover:text-white transition flex items-center justify-center space-x-1 cursor-pointer"
            >
              <span>View Details</span>
              <ChevronRight className="w-3.5 h-3.5 text-teal-400" />
            </button>
          </HolographicHUDPanel>

        </div>
      </div>

      {/* 3. ROW: RISK TREND WIDGET (MODULE 5) & TOP RISK FACTORS (MODULE 3) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left 50%: Risk Trends Widget */}
        <div className="lg:col-span-6">
          <HolographicHUDPanel 
            title="LONGITUDINAL RISK TRENDS" 
            subtitle="Module 5 historical trajectory comparison"
            glowColor="purple"
          >
            <div className="space-y-3 font-mono text-xs">
              {Object.keys(trends).length > 0 ? (
                Object.entries(trends).map(([dis, tr]) => (
                  <div key={dis} className="p-3 rounded-xl bg-[#080612] border border-[#29213F] flex items-center justify-between">
                    <div>
                      <div className="font-extrabold text-white uppercase text-[11px]">
                        {dis}
                      </div>
                      <div className="text-[10px] text-slate-400 mt-0.5">
                        {tr.safe_clinical_wording}
                      </div>
                    </div>

                    <div className="text-right flex-shrink-0 ml-3">
                      <div className="flex items-center justify-end space-x-1 font-bold">
                        {tr.trend_status === 'Increasing' ? (
                          <span className="text-rose-400 flex items-center">
                            <TrendingUp className="w-3.5 h-3.5 mr-0.5" />
                            <span>+{tr.percentage_point_difference}%</span>
                          </span>
                        ) : tr.trend_status === 'Decreasing' ? (
                          <span className="text-emerald-400 flex items-center">
                            <TrendingDown className="w-3.5 h-3.5 mr-0.5" />
                            <span>{tr.percentage_point_difference}%</span>
                          </span>
                        ) : (
                          <span className="text-slate-400">Stable</span>
                        )}
                      </div>
                      <div className="text-[10px] text-purple-300">
                        {tr.previous_risk_percentage}% → {tr.current_risk_percentage}%
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="p-4 text-center text-slate-400 text-xs font-sans">
                  Complete multiple assessments over time to activate longitudinal trend comparisons.
                </div>
              )}

              <button
                onClick={() => onNavigate && onNavigate('risk_history')}
                className="w-full py-2.5 rounded-xl bg-[#111025] hover:bg-[#1C1633] border border-[#7C3AED]/40 text-purple-300 hover:text-white font-bold transition flex items-center justify-center space-x-2 cursor-pointer mt-2"
              >
                <Clock className="w-3.5 h-3.5" />
                <span>View Full Risk History</span>
              </button>
            </div>
          </HolographicHUDPanel>
        </div>

        {/* Right 50%: Top Risk Factors (Module 3 SHAP) */}
        <div className="lg:col-span-6">
          <HolographicHUDPanel 
            title="TOP RISK INFLUENCERS (SHAP)" 
            subtitle="Module 3 feature attributions influencing your scores"
            glowColor="cyan"
          >
            <div className="space-y-2.5 font-mono text-xs">
              {topFactors.length > 0 ? (
                topFactors.slice(0, 4).map((f, idx) => (
                  <div key={idx} className="p-3 rounded-xl bg-[#080612] border border-[#29213F] flex items-start justify-between space-x-3">
                    <div className="w-6 h-6 rounded-lg bg-purple-950/80 border border-purple-800 text-purple-300 flex items-center justify-center font-extrabold text-[10px] flex-shrink-0 mt-0.5">
                      #{idx + 1}
                    </div>
                    <div className="flex-1">
                      <div className="font-bold text-white text-[11px] uppercase">
                        {f.feature} <span className="text-slate-400 font-normal">({f.value})</span>
                      </div>
                      <div className="text-[10px] text-slate-400 font-sans mt-0.5 leading-tight">
                        {f.explanation}
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="p-4 text-center text-slate-400 text-xs font-sans">
                  No SHAP attributions recorded yet. Run a risk assessment to analyze risk factors.
                </div>
              )}

              <button
                onClick={() => onNavigate && onNavigate('explain')}
                className="w-full py-2.5 rounded-xl bg-[#111025] hover:bg-[#1C1633] border border-[#7C3AED]/40 text-cyan-300 hover:text-white font-bold transition flex items-center justify-center space-x-2 cursor-pointer mt-2"
              >
                <HelpCircle className="w-3.5 h-3.5 text-cyan-400" />
                <span>Why is my risk high? (SHAP Laboratory)</span>
              </button>
            </div>
          </HolographicHUDPanel>
        </div>

      </div>

      {/* 4. ROW: PERSONALIZED WELLNESS PREVIEW (MODULE 4) & ALERTS (MODULE 5) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left 60%: Personalized Wellness Preview */}
        <div className="lg:col-span-7">
          <HolographicHUDPanel 
            title="PERSONALIZED WELLNESS PLAN PREVIEW" 
            subtitle="Module 4 AI risk-targeted lifestyle guidance"
            glowColor="teal"
          >
            {wellnessPreview ? (
              <div className="space-y-3 font-sans text-xs">
                <div className="p-3.5 rounded-xl bg-[#080612] border border-[#29213F] space-y-2">
                  <div className="flex items-center justify-between font-mono">
                    <span className="text-[10px] font-bold text-teal-300 uppercase px-2 py-0.5 rounded bg-teal-950/80 border border-teal-800">
                      {wellnessPreview.category}
                    </span>
                    <span className="text-[10px] text-slate-400">Target: {wellnessPreview.risk_factor}</span>
                  </div>

                  <p className="text-slate-200 text-xs leading-relaxed font-semibold">
                    "{wellnessPreview.recommendation_text}"
                  </p>

                  {wellnessPreview.safety_note && (
                    <div className="text-[10px] text-amber-300 bg-amber-950/30 border border-amber-800/50 p-2 rounded-lg font-mono">
                      ⚠️ {wellnessPreview.safety_note}
                    </div>
                  )}
                </div>

                <div className="grid grid-cols-3 gap-2 font-mono text-[10px]">
                  <div className="p-2 rounded-lg bg-[#111025] border border-[#29213F] text-center text-slate-300">
                    🥗 5-Meal Daily Guide
                  </div>
                  <div className="p-2 rounded-lg bg-[#111025] border border-[#29213F] text-center text-slate-300">
                    🏃 Morning Exercise
                  </div>
                  <div className="p-2 rounded-lg bg-[#111025] border border-[#29213F] text-center text-slate-300">
                    🌿 Herbal Guidance
                  </div>
                </div>

                <button
                  onClick={() => onNavigate && onNavigate('wellness')}
                  className="w-full py-2.5 rounded-xl bg-gradient-to-r from-teal-600 to-cyan-600 hover:from-teal-500 hover:to-cyan-500 text-white font-bold font-mono uppercase tracking-wider transition flex items-center justify-center space-x-2 cursor-pointer shadow-lg shadow-teal-900/30 mt-2"
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>View Full Wellness Plan</span>
                </button>
              </div>
            ) : (
              <div className="p-6 text-center space-y-3 font-sans">
                <p className="text-xs text-slate-400">Generate a risk assessment to receive custom 5-meal nutrition and exercise recommendations.</p>
                <button
                  onClick={() => onNavigate && onNavigate('risk')}
                  className="px-4 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-mono font-bold text-xs cursor-pointer"
                >
                  Generate Plan
                </button>
              </div>
            )}
          </HolographicHUDPanel>
        </div>

        {/* Right 40%: Alerts & Notifications (Module 5) */}
        <div className="lg:col-span-5">
          <HolographicHUDPanel 
            title="ALERTS & CLINICAL NOTIFICATIONS" 
            subtitle="Module 5 open review flags"
            glowColor="cyan"
          >
            <div className="space-y-2.5 font-mono text-xs">
              {alerts.length > 0 ? (
                alerts.map((a, idx) => (
                  <div key={idx} className="p-3 rounded-xl bg-[#080612] border border-amber-900/50 space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-bold text-amber-400 flex items-center space-x-1">
                        <AlertTriangle className="w-3 h-3 text-amber-400" />
                        <span>{a.type}</span>
                      </span>
                      <span className="text-[9px] text-slate-400 px-1.5 py-0.5 rounded bg-slate-900 border border-slate-800">
                        {a.severity}
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-200 font-sans">
                      {a.message}
                    </p>
                  </div>
                ))
              ) : (
                <div className="p-4 rounded-xl bg-[#080612] border border-[#29213F] text-center text-slate-400 text-xs font-sans space-y-1">
                  <CheckCircle2 className="w-5 h-5 text-emerald-400 mx-auto" />
                  <div className="font-bold text-white">No Open Clinical Alerts</div>
                  <div className="text-[10px]">Your telemetry is operating within baseline bounds.</div>
                </div>
              )}

              <button
                onClick={() => onNavigate && onNavigate('risk_history')}
                className="w-full py-2.5 rounded-xl bg-[#111025] hover:bg-[#1C1633] border border-[#29213F] text-slate-300 hover:text-white font-bold transition flex items-center justify-center space-x-2 cursor-pointer mt-2"
              >
                <Activity className="w-3.5 h-3.5 text-purple-400" />
                <span>View Alert Details</span>
              </button>
            </div>
          </HolographicHUDPanel>
        </div>

      </div>

      {/* 5. QUICK ACTION DOCK */}
      <div className="bg-[#0D0A1A]/90 border border-[#29213F] rounded-2xl p-4 shadow-xl select-none">
        <div className="text-[10px] font-mono font-bold text-slate-400 uppercase tracking-widest mb-3 flex items-center space-x-2">
          <Compass className="w-3.5 h-3.5 text-purple-400" />
          <span>Quick Workspace Actions</span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 font-mono text-xs">
          <button
            onClick={() => onNavigate && onNavigate('risk')}
            className="p-3 rounded-xl bg-[#111025] hover:bg-[#1C1633] border border-[#29213F] hover:border-[#7C3AED] text-slate-200 font-bold transition flex flex-col items-center justify-center space-y-1.5 text-center cursor-pointer group"
          >
            <Activity className="w-4 h-4 text-purple-400 group-hover:scale-110 transition" />
            <span>New Risk Assessment</span>
          </button>

          <button
            onClick={() => onNavigate && onNavigate('risk_history')}
            className="p-3 rounded-xl bg-[#111025] hover:bg-[#1C1633] border border-[#29213F] hover:border-[#7C3AED] text-slate-200 font-bold transition flex flex-col items-center justify-center space-y-1.5 text-center cursor-pointer group"
          >
            <Clock className="w-4 h-4 text-cyan-400 group-hover:scale-110 transition" />
            <span>View Risk History</span>
          </button>

          <button
            onClick={() => onNavigate && onNavigate('explain')}
            className="p-3 rounded-xl bg-[#111025] hover:bg-[#1C1633] border border-[#29213F] hover:border-[#7C3AED] text-slate-200 font-bold transition flex flex-col items-center justify-center space-y-1.5 text-center cursor-pointer group"
          >
            <HelpCircle className="w-4 h-4 text-teal-400 group-hover:scale-110 transition" />
            <span>View Explanation</span>
          </button>

          <button
            onClick={() => onNavigate && onNavigate('wellness')}
            className="p-3 rounded-xl bg-[#111025] hover:bg-[#1C1633] border border-[#29213F] hover:border-[#7C3AED] text-slate-200 font-bold transition flex flex-col items-center justify-center space-y-1.5 text-center cursor-pointer group"
          >
            <Sparkles className="w-4 h-4 text-amber-400 group-hover:scale-110 transition" />
            <span>Wellness Plan</span>
          </button>

          <button
            onClick={() => onNavigate && onNavigate('reports')}
            className="p-3 rounded-xl bg-[#111025] hover:bg-[#1C1633] border border-[#29213F] hover:border-[#7C3AED] text-slate-200 font-bold transition flex flex-col items-center justify-center space-y-1.5 text-center cursor-pointer group col-span-2 sm:col-span-1"
          >
            <FileText className="w-4 h-4 text-emerald-400 group-hover:scale-110 transition" />
            <span>Clinical Reports</span>
          </button>
        </div>
      </div>

      <ReportViewerModal
        isOpen={isReportModalOpen}
        onClose={() => setIsReportModalOpen(false)}
        patientId={user?.id || 100}
      />
    </div>
  );
}
