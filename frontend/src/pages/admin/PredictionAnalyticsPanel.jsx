import React, { useState, useEffect } from 'react';
import HolographicHUDPanel from '../../components/HolographicHUDPanel';
import { adminAPI } from '../../services/api';
import { BarChart3, Activity, Cpu, ShieldAlert, Users, MessageSquare, TrendingUp, Sparkles } from 'lucide-react';

export default function PredictionAnalyticsPanel() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const res = await adminAPI.getSystemAnalytics();
        setAnalytics(res.data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (loading) {
    return <div className="py-12 text-center text-slate-400 text-xs font-mono animate-pulse">Gathering system-level prediction analytics...</div>;
  }

  const overview = analytics?.overview || {};
  const riskDist = analytics?.risk_distribution || {};
  const models = analytics?.model_performance_summary || {};

  return (
    <div className="space-y-6 font-mono">
      <div>
        <h2 className="text-2xl font-extrabold text-white flex items-center space-x-2">
          <BarChart3 className="w-6 h-6 text-red-400" />
          <span>System-Wide Prediction Analytics & AI Metrics</span>
        </h2>
        <p className="text-xs text-[#C084FC]">System performance, multi-disease risk distribution, and ensemble metrics</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <div className="p-4 rounded-2xl bg-[#0D0718] border border-[#2A1A4E] space-y-2">
          <div className="flex items-center justify-between text-slate-400 text-[10px] uppercase font-bold">
            <span>Total Patients</span>
            <Users className="w-4 h-4 text-[#7C3AED]" />
          </div>
          <div className="text-2xl font-extrabold text-white">{overview.total_patients || 0}</div>
        </div>

        <div className="p-4 rounded-2xl bg-[#0D0718] border border-[#2A1A4E] space-y-2">
          <div className="flex items-center justify-between text-slate-400 text-[10px] uppercase font-bold">
            <span>Total Predictions</span>
            <Activity className="w-4 h-4 text-[#C084FC]" />
          </div>
          <div className="text-2xl font-extrabold text-[#C084FC]">{overview.total_predictions || 0}</div>
        </div>

        <div className="p-4 rounded-2xl bg-[#0D0718] border border-[#2A1A4E] space-y-2">
          <div className="flex items-center justify-between text-slate-400 text-[10px] uppercase font-bold">
            <span>High Risk Patients</span>
            <ShieldAlert className="w-4 h-4 text-red-400" />
          </div>
          <div className="text-2xl font-extrabold text-red-400">{overview.high_risk_patients || 0}</div>
        </div>

        <div className="p-4 rounded-2xl bg-[#0D0718] border border-[#2A1A4E] space-y-2">
          <div className="flex items-center justify-between text-slate-400 text-[10px] uppercase font-bold">
            <span>Chat Sessions</span>
            <MessageSquare className="w-4 h-4 text-[#22C55E]" />
          </div>
          <div className="text-2xl font-extrabold text-[#22C55E]">{overview.active_chat_sessions || 0}</div>
        </div>

        <div className="p-4 rounded-2xl bg-[#0D0718] border border-[#2A1A4E] space-y-2">
          <div className="flex items-center justify-between text-slate-400 text-[10px] uppercase font-bold">
            <span>System Users</span>
            <Sparkles className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-extrabold text-amber-400">{overview.total_users || 0}</div>
        </div>
      </div>

      {/* Disease Distribution Breakdown */}
      <HolographicHUDPanel title="MULTI-DISEASE RISK BREAKDOWN" subtitle="PREDICTION METRICS" glowColor="purple">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 rounded-xl bg-[#120A24] border border-[#2A1A4E] space-y-2 text-center">
            <div className="text-xs text-[#C084FC] font-bold uppercase">Diabetes Mellitus</div>
            <div className="text-3xl font-extrabold text-white">{riskDist.diabetes || 0}</div>
            <div className="text-[10px] text-slate-400">High Risk Identified Cases</div>
          </div>

          <div className="p-4 rounded-xl bg-[#120A24] border border-[#2A1A4E] space-y-2 text-center">
            <div className="text-xs text-indigo-400 font-bold uppercase">Cardiovascular Disease (CVD)</div>
            <div className="text-3xl font-extrabold text-white">{riskDist.cvd || 0}</div>
            <div className="text-[10px] text-slate-400">Elevated Risk Cases</div>
          </div>

          <div className="p-4 rounded-xl bg-[#120A24] border border-[#2A1A4E] space-y-2 text-center">
            <div className="text-xs text-rose-400 font-bold uppercase">Chronic Kidney Disease (CKD)</div>
            <div className="text-3xl font-extrabold text-white">{riskDist.ckd || 0}</div>
            <div className="text-[10px] text-slate-400">Critical Stage Alerts</div>
          </div>
        </div>
      </HolographicHUDPanel>

      {/* Model Performance Registry Table */}
      <HolographicHUDPanel title="AI ENSEMBLE MODEL BENCHMARK" subtitle="MODEL METRICS & ACCURACY" glowColor="red">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-[#2A1A4E] text-[#C084FC] font-bold uppercase text-[10px] tracking-wider">
                <th className="py-3 px-4">Model Key</th>
                <th className="py-3 px-4">Accuracy</th>
                <th className="py-3 px-4">F1 Score</th>
                <th className="py-3 px-4">ROC-AUC</th>
                <th className="py-3 px-4">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#2A1A4E]/50">
              {Object.entries(models).map(([mKey, mData]) => (
                <tr key={mKey} className="hover:bg-[#120A24]">
                  <td className="py-3 px-4 font-bold text-white uppercase">{mKey.replace('_', ' ')}</td>
                  <td className="py-3 px-4 text-[#22C55E] font-bold">{(mData.accuracy * 100).toFixed(1)}%</td>
                  <td className="py-3 px-4 text-[#C084FC] font-bold">{(mData.f1_score * 100).toFixed(1)}%</td>
                  <td className="py-3 px-4 text-indigo-300 font-bold">{(mData.roc_auc * 100).toFixed(1)}%</td>
                  <td className="py-3 px-4">
                    <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-[#22C55E]/20 text-[#22C55E] border border-[#22C55E]/40 uppercase">
                      {mData.status || 'Active'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </HolographicHUDPanel>

      {/* Platform Website & Maintenance Mode Control Center */}
      <PlatformMaintenanceControlPanel />
    </div>
  );
}

function PlatformMaintenanceControlPanel() {
  const [settings, setSettings] = useState({
    maintenance_mode: false,
    maintenance_message: "SmartCare AI is temporarily unavailable due to scheduled maintenance.",
    maintenance_access_roles: ["admin", "super_admin"],
    website_status: "ONLINE",
    ai_service_enabled: true,
    report_disclaimer: "SmartCare AI Risk Assessment is a clinical decision support system. It is not an automated diagnosis."
  });
  const [loading, setLoading] = useState(false);
  const [savedMsg, setSavedMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    adminAPI.getSystemSettings().then(res => {
      if (res.data) setSettings(prev => ({ ...prev, ...res.data }));
    }).catch(console.error);
  }, []);

  const handleToggleMaintenance = () => {
    setSettings(prev => {
      const nextMode = !prev.maintenance_mode;
      return {
        ...prev,
        maintenance_mode: nextMode,
        website_status: nextMode ? 'MAINTENANCE' : 'ONLINE'
      };
    });
  };

  const handleWebsiteStatusChange = (val) => {
    setSettings(prev => ({
      ...prev,
      website_status: val,
      maintenance_mode: val === 'MAINTENANCE'
    }));
  };

  const handleToggleRole = (role) => {
    setSettings(prev => {
      const current = prev.maintenance_access_roles || [];
      const updated = current.includes(role) 
        ? current.filter(r => r !== role) 
        : [...current, role];
      return { ...prev, maintenance_access_roles: updated };
    });
  };

  const handleSave = async () => {
    setLoading(true);
    setSavedMsg('');
    setErrorMsg('');
    try {
      // Send clean payload
      const payload = {
        maintenance_mode: settings.maintenance_mode,
        maintenance_message: settings.maintenance_message,
        maintenance_access_roles: settings.maintenance_access_roles,
        website_status: settings.website_status,
        ai_service_enabled: settings.ai_service_enabled,
        report_disclaimer: settings.report_disclaimer
      };
      const res = await adminAPI.updateSystemSettings(payload);
      if (res.data) {
        setSettings(prev => ({ ...prev, ...res.data }));
      }
      setSavedMsg("Platform system controls updated and applied successfully.");
      setTimeout(() => setSavedMsg(''), 5000);
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || "Failed to save system settings.";
      setErrorMsg(`Failed to save: ${msg}`);
      alert(`Failed to save system settings: ${msg}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <HolographicHUDPanel title="WEBSITE & SYSTEM MAINTENANCE CONTROL" subtitle="GLOBAL PLATFORM MANAGEMENT" glowColor="red">
      <div className="space-y-5 text-xs">
        {savedMsg && (
          <div className="p-3 rounded-xl bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 font-bold flex items-center justify-between animate-in fade-in">
            <span>✓ {savedMsg}</span>
          </div>
        )}
        {errorMsg && (
          <div className="p-3 rounded-xl bg-red-500/20 border border-red-500/40 text-red-300 font-bold flex items-center justify-between animate-in fade-in">
            <span>⚠ {errorMsg}</span>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Maintenance Mode Switch */}
          <div className="p-4 rounded-2xl bg-[#0D0718] border border-[#2A1A4E] space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-white font-bold text-sm">Maintenance Mode</div>
                <div className="text-[10px] text-slate-400">Restrict platform access to authorized roles only</div>
              </div>
              <button
                type="button"
                onClick={handleToggleMaintenance}
                className={`px-4 py-1.5 rounded-full font-bold text-xs uppercase cursor-pointer transition shadow-md ${
                  settings.maintenance_mode 
                    ? 'bg-amber-500 text-black shadow-amber-500/30 ring-2 ring-amber-400' 
                    : 'bg-emerald-600/30 text-emerald-400 border border-emerald-500/40'
                }`}
              >
                {settings.maintenance_mode ? 'ENABLED (Restricted)' : 'DISABLED (Online)'}
              </button>
            </div>

            {settings.maintenance_mode && (
              <div className="space-y-2 pt-2 border-t border-[#2A1A4E]">
                <label className="text-[10px] text-[#C084FC] uppercase font-bold">Allowed Roles During Maintenance</label>
                <div className="flex flex-wrap gap-2">
                  {['admin', 'super_admin', 'doctor', 'staff', 'clinician'].map(role => {
                    const isAllowed = (settings.maintenance_access_roles || []).includes(role);
                    return (
                      <button
                        key={role}
                        type="button"
                        onClick={() => handleToggleRole(role)}
                        className={`px-3 py-1 rounded-lg text-[11px] font-bold uppercase transition cursor-pointer ${
                          isAllowed 
                            ? 'bg-[#7C3AED] text-white shadow-sm shadow-purple-500/50' 
                            : 'bg-[#120A24] text-slate-400 border border-[#2A1A4E]'
                        }`}
                      >
                        {role} {isAllowed ? '✓' : ''}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}
          </div>

          {/* AI Services & Website Status */}
          <div className="p-4 rounded-2xl bg-[#0D0718] border border-[#2A1A4E] space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-white font-bold text-sm">AI Inference Engine</div>
                <div className="text-[10px] text-slate-400">Multi-Disease Ensemble & XAI Services</div>
              </div>
              <button
                type="button"
                onClick={() => setSettings(s => ({ ...s, ai_service_enabled: !s.ai_service_enabled }))}
                className={`px-4 py-1.5 rounded-full font-bold text-xs uppercase cursor-pointer transition ${
                  settings.ai_service_enabled 
                    ? 'bg-[#22C55E]/20 text-[#22C55E] border border-[#22C55E]/40' 
                    : 'bg-red-500/20 text-red-400 border border-red-500/40'
                }`}
              >
                {settings.ai_service_enabled ? 'Active Online' : 'Paused'}
              </button>
            </div>

            <div className="space-y-1 pt-2 border-t border-[#2A1A4E]">
              <label className="text-[10px] text-[#C084FC] uppercase font-bold">Website Status</label>
              <select
                value={settings.website_status || (settings.maintenance_mode ? "MAINTENANCE" : "ONLINE")}
                onChange={(e) => handleWebsiteStatusChange(e.target.value)}
                className="w-full bg-[#120A24] border border-[#3B206B] rounded-xl px-3 py-1.5 text-xs text-white outline-none focus:border-red-500"
              >
                <option value="ONLINE">Website Online (Operational)</option>
                <option value="MAINTENANCE">Maintenance Mode (Restricted Access)</option>
                <option value="OFFLINE">Website Offline</option>
              </select>
            </div>
          </div>
        </div>

        {/* Maintenance User Banner Message */}
        <div className="space-y-1.5">
          <label className="text-[10px] text-[#C084FC] uppercase font-bold">Patient Maintenance Notice</label>
          <input
            type="text"
            value={settings.maintenance_message || ''}
            onChange={(e) => setSettings(s => ({ ...s, maintenance_message: e.target.value }))}
            className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-red-500"
          />
        </div>

        {/* Save Button */}
        <div className="flex justify-end">
          <button
            type="button"
            onClick={handleSave}
            disabled={loading}
            className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-[#6D28D9] to-[#EF4444] text-white font-bold text-xs uppercase tracking-wider hover:brightness-110 transition shadow-lg shadow-red-500/20 cursor-pointer disabled:opacity-50"
          >
            {loading ? 'Applying Changes...' : 'Save Global Platform Controls'}
          </button>
        </div>
      </div>
    </HolographicHUDPanel>
  );
}
