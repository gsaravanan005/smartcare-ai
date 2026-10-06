import React, { useState } from 'react';
import HolographicHUDPanel from '../../components/HolographicHUDPanel';
import { 
  Stethoscope, Award, Mail, Phone, Building2, ShieldCheck, 
  Settings, CheckCircle2, User, Activity, Bell, FileText
} from 'lucide-react';

export default function DoctorProfile({ user }) {
  const [preferences, setPreferences] = useState({
    alertThreshold: 'High & Moderate',
    defaultModel: 'Ensemble Multi-Task',
    shapExplanationDetail: 'Comprehensive',
    emailAlerts: true
  });

  const [savedBanner, setSavedBanner] = useState('');

  const handleSavePreferences = (e) => {
    e.preventDefault();
    setSavedBanner('Clinical decision support preferences saved successfully.');
    setTimeout(() => setSavedBanner(''), 4000);
  };

  return (
    <div className="w-full space-y-6 font-sans pb-12">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-[#0D0A1A] via-[#141025] to-[#0D0A1A] border border-[#29213F] rounded-3xl p-6 shadow-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-xs font-mono text-[#C084FC] mb-1">
            <Stethoscope className="w-4 h-4 text-[#C084FC]" />
            <span className="font-bold uppercase tracking-widest text-[#C084FC]">CLINICIAN PROFILE & CREDENTIALS</span>
          </div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
            {user?.full_name || user?.username || 'Dr. Sarah Jenkins'}
          </h1>
          <p className="text-xs text-slate-300 font-sans mt-1">
            Verified Clinician Credentials, Practice Department, and Clinical Decision Support Settings.
          </p>
        </div>

        <div className="flex items-center space-x-3 text-xs font-mono">
          <div className="px-3.5 py-2 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 flex items-center space-x-2">
            <Award className="w-4 h-4 text-emerald-400" />
            <span>LICENSE: VERIFIED & ACTIVE</span>
          </div>
        </div>
      </div>

      {savedBanner && (
        <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/40 text-emerald-300 text-xs font-mono flex items-center space-x-2 animate-in fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
          <span>{savedBanner}</span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 font-mono text-xs">
        {/* Clinician Card */}
        <div className="space-y-6">
          <HolographicHUDPanel title="CLINICAL CREDENTIALS" subtitle="PRACTICE VERIFICATION" glowColor="purple">
            <div className="space-y-4">
              <div className="flex items-center justify-center py-4">
                <div className="w-20 h-20 rounded-2xl bg-gradient-to-tr from-[#7C3AED] to-[#A855F7] flex items-center justify-center text-white text-2xl font-bold shadow-lg shadow-purple-900/40 border border-purple-400/40">
                  {(user?.full_name || 'Dr')[0]}
                </div>
              </div>

              <div className="space-y-3 divide-y divide-[#2A1A4E]/60">
                <div className="pt-2 flex justify-between items-center">
                  <span className="text-slate-400">Clinician Name</span>
                  <span className="text-white font-bold">{user?.full_name || 'Dr. Sarah Jenkins'}</span>
                </div>
                <div className="pt-2 flex justify-between items-center">
                  <span className="text-slate-400">Specialization</span>
                  <span className="text-purple-300">Cardiology & Endocrinology</span>
                </div>
                <div className="pt-2 flex justify-between items-center">
                  <span className="text-slate-400">Medical License</span>
                  <span className="text-emerald-400 font-bold">MD-892401-US</span>
                </div>
                <div className="pt-2 flex justify-between items-center">
                  <span className="text-slate-400">Hospital Affiliation</span>
                  <span className="text-slate-200">SmartCare AI Central</span>
                </div>
                <div className="pt-2 flex justify-between items-center">
                  <span className="text-slate-400">Clinical Experience</span>
                  <span className="text-white">14+ Years</span>
                </div>
              </div>
            </div>
          </HolographicHUDPanel>

          <div className="p-5 rounded-2xl bg-[#0D0718]/90 border border-[#2A1A4E] space-y-3">
            <div className="flex items-center space-x-2 text-emerald-400 font-bold">
              <ShieldCheck className="w-4 h-4" />
              <span>DOCTOR-PATIENT RBAC</span>
            </div>
            <p className="text-slate-400 text-[11px] leading-relaxed">
              Your clinician privileges allow you to review and manage diagnostics strictly for patients assigned directly to your clinical care roster.
            </p>
          </div>
        </div>

        {/* Clinical Preferences */}
        <div className="lg:col-span-2">
          <HolographicHUDPanel title="CLINICAL DECISION SUPPORT PREFERENCES" subtitle="CUSTOMIZE AI TRIAGE" glowColor="purple">
            <form onSubmit={handleSavePreferences} className="space-y-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-slate-300 font-semibold flex items-center space-x-1.5">
                    <Activity className="w-3.5 h-3.5 text-purple-400" />
                    <span>Risk Alert Threshold</span>
                  </label>
                  <select
                    value={preferences.alertThreshold}
                    onChange={(e) => setPreferences({ ...preferences, alertThreshold: e.target.value })}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-[#120826] border border-[#2B1854] text-white focus:outline-none focus:border-[#7C3AED]"
                  >
                    <option value="High Only">High Risk Only (&gt;60%)</option>
                    <option value="High & Moderate">High &amp; Moderate Risk (&gt;30%)</option>
                    <option value="All Predictions">All Predictions &amp; Baseline Changes</option>
                  </select>
                </div>

                <div className="space-y-1.5">
                  <label className="text-slate-300 font-semibold flex items-center space-x-1.5">
                    <FileText className="w-3.5 h-3.5 text-purple-400" />
                    <span>SHAP Factor Detail</span>
                  </label>
                  <select
                    value={preferences.shapExplanationDetail}
                    onChange={(e) => setPreferences({ ...preferences, shapExplanationDetail: e.target.value })}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-[#120826] border border-[#2B1854] text-white focus:outline-none focus:border-[#7C3AED]"
                  >
                    <option value="Comprehensive">Comprehensive (Top 10 Biomarkers)</option>
                    <option value="Standard">Standard (Top 5 Biomarkers)</option>
                    <option value="Compact">Compact Summary Only</option>
                  </select>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-[#150B33] border border-[#2B1854] flex items-center justify-between">
                <div>
                  <div className="text-white font-bold">Email Clinical Escalations</div>
                  <div className="text-slate-400 text-[11px] mt-0.5">Receive immediate notification when an assigned patient enters Critical Tier.</div>
                </div>
                <input
                  type="checkbox"
                  checked={preferences.emailAlerts}
                  onChange={(e) => setPreferences({ ...preferences, emailAlerts: e.target.checked })}
                  className="w-4 h-4 rounded text-purple-600 focus:ring-purple-500 cursor-pointer"
                />
              </div>

              <div className="flex justify-end pt-2">
                <button
                  type="submit"
                  className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-[#7C3AED] to-[#9333EA] hover:brightness-110 text-white font-bold transition flex items-center space-x-2 shadow-lg shadow-purple-900/40 cursor-pointer"
                >
                  <Settings className="w-4 h-4" />
                  <span>Save Clinical Preferences</span>
                </button>
              </div>
            </form>
          </HolographicHUDPanel>
        </div>
      </div>
    </div>
  );
}
