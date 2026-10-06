import React, { useState, useEffect } from 'react';
import { clinicianAPI, riskMonitoringAPI } from '../services/api';
import { 
  Users, AlertTriangle, ShieldCheck, Activity, Search, Eye, 
  CheckCircle2, RefreshCw, ArrowRight, UserCheck, Stethoscope
} from 'lucide-react';

export default function ClinicianDashboard({ user, onNavigate, onSelectPatient }) {
  const [metrics, setMetrics] = useState(null);
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  const fetchClinicianData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [dashRes, patRes] = await Promise.all([
        clinicianAPI.getDashboard(),
        clinicianAPI.getPatientList()
      ]);
      setMetrics(dashRes.data);
      setPatients(patRes.data || []);
    } catch (err) {
      console.error("Error fetching clinician dashboard:", err);
      setError("Failed to load clinician dashboard. Clinician or Admin privileges required.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchClinicianData();
  }, []);

  const handleResolveAlert = async (alertId) => {
    try {
      await riskMonitoringAPI.updateAlertStatus(alertId, { status: "RESOLVED" });
      fetchClinicianData();
    } catch (e) {
      console.error("Failed to resolve alert:", e);
    }
  };

  const filteredPatients = patients.filter(p => 
    p.patient_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    String(p.patient_id).includes(searchTerm)
  );

  if (loading) {
    return (
      <div className="w-full min-h-[60vh] flex flex-col items-center justify-center space-y-4 font-mono text-xs">
        <div className="w-12 h-12 rounded-full border-2 border-cyan-500 border-t-transparent animate-spin" />
        <div className="text-cyan-300 font-bold uppercase tracking-widest animate-pulse">
          INITIALIZING CLINICIAN DECISION PORTAL & PATIENT ROSTER...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="w-full max-w-xl mx-auto mt-12 bg-rose-950/40 border border-rose-800/60 rounded-3xl p-8 text-center space-y-4 font-sans">
        <AlertTriangle className="w-12 h-12 text-rose-400 mx-auto" />
        <h3 className="text-lg font-bold text-white font-mono">Access Restricted</h3>
        <p className="text-xs text-rose-200 font-sans">{error}</p>
        <button
          onClick={fetchClinicianData}
          className="px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-xl font-mono text-xs font-bold uppercase tracking-wider transition cursor-pointer"
        >
          Retry Access
        </button>
      </div>
    );
  }

  return (
    <div className="w-full space-y-8 z-10 font-sans pb-16">
      
      {/* 1. CLINICIAN HEADER */}
      <div className="bg-gradient-to-r from-[#080E1E] via-[#0E172E] to-[#080E1E] border border-[#1E2E54] rounded-3xl p-6 sm:p-8 shadow-2xl relative overflow-hidden">
        <div className="flex flex-wrap items-center justify-between gap-4 relative z-10">
          <div className="flex items-center space-x-3">
            <div className="p-3 rounded-2xl bg-cyan-600/20 border border-cyan-500/40 text-cyan-300 shadow-lg shadow-cyan-900/30">
              <Stethoscope className="w-6 h-6" />
            </div>
            <div>
              <span className="text-[11px] font-mono font-extrabold uppercase tracking-widest text-cyan-400 bg-cyan-950/60 px-2.5 py-0.5 rounded-md border border-cyan-800/50">
                MODULE 5 — CLINICIAN PORTAL
              </span>
              <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight pt-1">
                Clinical Decision Support Dashboard
              </h1>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={fetchClinicianData}
              className="px-3.5 py-1.5 rounded-xl bg-[#101B38] hover:bg-[#1A2A54] border border-[#243970] text-slate-200 text-xs font-mono font-bold flex items-center space-x-1.5 transition cursor-pointer"
            >
              <RefreshCw className="w-3.5 h-3.5 text-cyan-400" />
              <span>Refresh Portal</span>
            </button>
          </div>
        </div>

        <p className="text-sm text-slate-300 max-w-3xl font-sans leading-relaxed pt-4 relative z-10">
          Review patient risk trajectories, manage automated high-risk alerts, inspect SHAP attributions, and log clinician recommendations with full decision-support traceability.
        </p>
      </div>

      {/* 2. STATS OVERVIEW CARDS */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 font-mono">
        <div className="bg-[#0A1224] border border-[#1C2C52] rounded-3xl p-5 shadow-xl">
          <div className="flex items-center justify-between text-slate-400 text-xs font-bold uppercase">
            <span>Total Patients</span>
            <Users className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-3xl font-extrabold text-white mt-2">
            {metrics?.total_patients || 0}
          </div>
          <span className="text-[10px] text-slate-400">Registered patient profiles</span>
        </div>

        <div className="bg-[#0A1224] border border-rose-900/50 rounded-3xl p-5 shadow-xl">
          <div className="flex items-center justify-between text-rose-400 text-xs font-bold uppercase">
            <span>Clinical Reviews</span>
            <AlertTriangle className="w-4 h-4 text-rose-400" />
          </div>
          <div className="text-3xl font-extrabold text-rose-300 mt-2">
            {metrics?.patients_requiring_review || 0}
          </div>
          <span className="text-[10px] text-rose-300/70">Patients with high-risk alerts</span>
        </div>

        <div className="bg-[#0A1224] border border-amber-900/50 rounded-3xl p-5 shadow-xl">
          <div className="flex items-center justify-between text-amber-400 text-xs font-bold uppercase">
            <span>Open Alerts</span>
            <Activity className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-3xl font-extrabold text-amber-300 mt-2">
            {metrics?.open_alerts_count || 0}
          </div>
          <span className="text-[10px] text-amber-300/70">Unresolved system alerts</span>
        </div>

        <div className="bg-[#0A1224] border border-teal-900/50 rounded-3xl p-5 shadow-xl">
          <div className="flex items-center justify-between text-teal-400 text-xs font-bold uppercase">
            <span>Total Assessments</span>
            <ShieldCheck className="w-4 h-4 text-teal-400" />
          </div>
          <div className="text-3xl font-extrabold text-teal-300 mt-2">
            {metrics?.recent_assessments_count || 0}
          </div>
          <span className="text-[10px] text-teal-300/70">Evaluated risk predictions</span>
        </div>
      </div>

      {/* 3. URGENT OPEN ALERTS SECTION */}
      {metrics?.recent_alerts && metrics.recent_alerts.length > 0 && (
        <div className="bg-[#0A1224] border border-rose-900/40 rounded-3xl p-6 shadow-2xl space-y-4">
          <div className="flex items-center justify-between border-b border-[#1C2C52] pb-4">
            <div className="flex items-center space-x-2">
              <AlertTriangle className="w-5 h-5 text-rose-400 animate-pulse" />
              <h2 className="text-lg font-bold text-white tracking-tight font-mono">
                Urgent Open Clinical Alerts ({metrics.recent_alerts.length})
              </h2>
            </div>
            <span className="text-xs font-mono text-rose-300 bg-rose-950/60 px-3 py-1 rounded-full border border-rose-800/40 font-bold">
              Action Required
            </span>
          </div>

          <div className="space-y-3">
            {metrics.recent_alerts.map((alert) => (
              <div 
                key={alert.id} 
                className="p-4 rounded-2xl bg-[#111A33] border border-rose-950/80 flex flex-wrap items-center justify-between gap-4 hover:border-rose-800/60 transition"
              >
                <div className="space-y-1">
                  <div className="flex items-center space-x-2 font-mono text-xs">
                    <span className="font-bold text-white">Patient #{alert.patient_id}</span>
                    <span className="text-slate-400">•</span>
                    <span className="text-rose-400 font-bold uppercase">{alert.alert_type}</span>
                    <span className="text-slate-400">•</span>
                    <span className="text-slate-400">{new Date(alert.created_at).toLocaleString()}</span>
                  </div>
                  <p className="text-xs text-slate-200 font-sans font-medium">{alert.message}</p>
                  <p className="text-[11px] text-slate-400 font-mono">{alert.reason}</p>
                </div>

                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => onSelectPatient && onSelectPatient(alert.patient_id)}
                    className="px-3 py-1.5 rounded-xl bg-cyan-600/30 hover:bg-cyan-600/50 border border-cyan-500/40 text-cyan-200 text-xs font-mono font-bold flex items-center space-x-1 transition cursor-pointer"
                  >
                    <Eye className="w-3.5 h-3.5" />
                    <span>View Patient</span>
                  </button>
                  <button
                    onClick={() => handleResolveAlert(alert.id)}
                    className="px-3 py-1.5 rounded-xl bg-emerald-600/30 hover:bg-emerald-600/50 border border-emerald-500/40 text-emerald-200 text-xs font-mono font-bold flex items-center space-x-1 transition cursor-pointer"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Resolve</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 4. AUTHORIZED PATIENT ROSTER TABLE */}
      <div className="bg-[#0A1224] border border-[#1C2C52] rounded-3xl p-6 shadow-2xl space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1C2C52] pb-4">
          <div className="flex items-center space-x-2">
            <Users className="w-5 h-5 text-cyan-400" />
            <h2 className="text-lg font-bold text-white tracking-tight font-mono">
              Authorized Patient Roster
            </h2>
          </div>

          <div className="relative w-full sm:w-64">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search by name or ID..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-[#111A33] border border-[#243970] rounded-xl pl-9 pr-3 py-1.5 text-xs text-white placeholder-slate-400 font-mono focus:outline-none focus:border-cyan-400"
            />
          </div>
        </div>

        {filteredPatients.length === 0 ? (
          <div className="py-12 text-center text-slate-400 font-mono text-xs">
            No matching patient records found.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono border-collapse">
              <thead>
                <tr className="border-b border-[#1C2C52] text-slate-400 uppercase tracking-wider text-[10px]">
                  <th className="py-3 px-4">Patient Name / ID</th>
                  <th className="py-3 px-4">Demographics</th>
                  <th className="py-3 px-4">Last Assessment</th>
                  <th className="py-3 px-4">Diabetes Risk</th>
                  <th className="py-3 px-4">CVD Risk</th>
                  <th className="py-3 px-4">CKD Risk</th>
                  <th className="py-3 px-4">Alert Status</th>
                  <th className="py-3 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#162447] text-slate-200">
                {filteredPatients.map((p) => (
                  <tr key={p.patient_id} className="hover:bg-[#111A33] transition">
                    <td className="py-3.5 px-4">
                      <div className="font-bold text-white">{p.patient_name}</div>
                      <div className="text-[10px] text-cyan-400">ID: #{p.patient_id}</div>
                    </td>
                    <td className="py-3.5 px-4 text-slate-300">
                      {p.age ? `${p.age} yrs` : 'N/A'}, {p.sex}
                    </td>
                    <td className="py-3.5 px-4 text-slate-300">
                      {p.last_assessment_date ? new Date(p.last_assessment_date).toLocaleDateString() : 'None'}
                    </td>
                    <td className="py-3.5 px-4 font-bold">
                      <span className={p.diabetes_risk_percentage >= 60 ? 'text-rose-400' : 'text-slate-200'}>
                        {p.diabetes_risk_percentage}%
                      </span>
                    </td>
                    <td className="py-3.5 px-4 font-bold">
                      <span className={p.cvd_risk_percentage >= 60 ? 'text-rose-400' : 'text-slate-200'}>
                        {p.cvd_risk_percentage}%
                      </span>
                    </td>
                    <td className="py-3.5 px-4 font-bold">
                      <span className={p.ckd_risk_percentage >= 60 ? 'text-rose-400' : 'text-slate-200'}>
                        {p.ckd_risk_percentage}%
                      </span>
                    </td>
                    <td className="py-3.5 px-4">
                      <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase border ${
                        p.alert_status === 'Clinical Review' ? 'bg-rose-950/60 border-rose-700/80 text-rose-300' :
                        p.alert_status === 'Monitor' ? 'bg-amber-950/60 border-amber-700/80 text-amber-300' :
                        'bg-emerald-950/60 border-emerald-700/80 text-emerald-300'
                      }`}>
                        {p.alert_status}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <button
                        onClick={() => onSelectPatient && onSelectPatient(p.patient_id)}
                        className="px-3 py-1 rounded-lg bg-cyan-600/30 hover:bg-cyan-600/50 border border-cyan-500/40 text-cyan-200 font-bold flex items-center space-x-1 ml-auto transition cursor-pointer"
                      >
                        <Eye className="w-3.5 h-3.5" />
                        <span>Inspect Patient</span>
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

    </div>
  );
}
