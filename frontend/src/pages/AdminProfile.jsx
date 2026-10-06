import React, { useState, useEffect } from 'react';
import HolographicHUDPanel from '../components/HolographicHUDPanel';
import { adminAPI } from '../services/api';
import CreateStaffAccountModal from './admin/CreateStaffAccountModal';
import SystemReset2FAModal from './admin/SystemReset2FAModal';
import { 
  ShieldCheck, ShieldAlert, Key, Lock, Mail, Shield, Clock, CheckCircle2, 
  Monitor, Globe, Server, Database, RefreshCw, Trash2, Download, Send, 
  Cpu, AlertTriangle, FileText, Bell, Layers, ToggleLeft, ToggleRight, Sparkles, UserPlus, Flame
} from 'lucide-react';

export default function AdminProfile({ user }) {
  // --- 1. System Settings State ---
  const [settings, setSettings] = useState({
    maintenance_mode: false,
    maintenance_message: "SmartCare AI is temporarily unavailable due to scheduled maintenance.",
    maintenance_access_roles: ["admin", "super_admin"],
    website_status: "ONLINE",
    ai_service_enabled: true,
    interactive_report_enabled: true,
    pdf_report_enabled: true,
    report_disclaimer: "This report provides AI-assisted clinical decision support and is not a substitute for professional medical diagnosis or treatment.",
    session_timeout: 1440,
    supported_languages: ["en", "ta", "hi"]
  });

  const [loadingSettings, setLoadingSettings] = useState(false);
  const [savingSettings, setSavingSettings] = useState(false);
  const [savedBanner, setSavedBanner] = useState('');
  const [errorBanner, setErrorBanner] = useState('');
  const [isDoctorModalOpen, setIsDoctorModalOpen] = useState(false);
  const [isResetModalOpen, setIsResetModalOpen] = useState(false);

  // --- 2. Operational Actions State ---
  const [opLoading, setOpLoading] = useState({});
  const [opFeedback, setOpFeedback] = useState({});

  // --- 3. Broadcast Announcement State ---
  const [broadcast, setBroadcast] = useState({
    title: '',
    message: '',
    type: 'system',
    priority: 'Medium',
    target_role: 'all'
  });
  const [sendingBroadcast, setSendingBroadcast] = useState(false);
  const [broadcastResult, setBroadcastResult] = useState('');

  // Load Settings on Mount
  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    setLoadingSettings(true);
    try {
      const res = await adminAPI.getSystemSettings();
      if (res.data) {
        setSettings(prev => ({ ...prev, ...res.data }));
      }
    } catch (err) {
      console.error("Failed to load settings:", err);
    } finally {
      setLoadingSettings(false);
    }
  };

  // --- Maintenance Handlers ---
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

  const handleToggleLanguage = (lang) => {
    setSettings(prev => {
      const current = prev.supported_languages || [];
      const updated = current.includes(lang)
        ? current.filter(l => l !== lang)
        : [...current, lang];
      return { ...prev, supported_languages: updated };
    });
  };

  const handleSaveSettings = async () => {
    setSavingSettings(true);
    setSavedBanner('');
    setErrorBanner('');
    try {
      const payload = {
        maintenance_mode: settings.maintenance_mode,
        maintenance_message: settings.maintenance_message,
        maintenance_access_roles: settings.maintenance_access_roles,
        website_status: settings.website_status,
        ai_service_enabled: settings.ai_service_enabled,
        interactive_report_enabled: settings.interactive_report_enabled,
        pdf_report_enabled: settings.pdf_report_enabled,
        report_disclaimer: settings.report_disclaimer,
        session_timeout: Number(settings.session_timeout) || 1440,
        supported_languages: settings.supported_languages
      };
      const res = await adminAPI.updateSystemSettings(payload);
      if (res.data) {
        setSettings(prev => ({ ...prev, ...res.data }));
      }
      setSavedBanner("Platform controls and maintenance configurations saved successfully.");
      setTimeout(() => setSavedBanner(''), 6000);
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || "Failed to save settings.";
      setErrorBanner(`Error saving settings: ${msg}`);
    } finally {
      setSavingSettings(false);
    }
  };

  // --- Operational Actions Handlers ---
  const handleReindexDB = async () => {
    setOpLoading(prev => ({ ...prev, reindex: true }));
    try {
      const res = await adminAPI.reindexDatabase();
      setOpFeedback(prev => ({ ...prev, reindex: res.data?.message || 'Database indexes optimized.' }));
      setTimeout(() => setOpFeedback(prev => ({ ...prev, reindex: '' })), 5000);
    } catch (err) {
      alert("Reindexing failed: " + (err.response?.data?.detail || err.message));
    } finally {
      setOpLoading(prev => ({ ...prev, reindex: false }));
    }
  };

  const handleClearCache = async () => {
    setOpLoading(prev => ({ ...prev, cache: true }));
    try {
      const res = await adminAPI.clearCache();
      setOpFeedback(prev => ({ ...prev, cache: res.data?.message || 'System cache cleared.' }));
      setTimeout(() => setOpFeedback(prev => ({ ...prev, cache: '' })), 5000);
    } catch (err) {
      alert("Cache flush failed: " + (err.response?.data?.detail || err.message));
    } finally {
      setOpLoading(prev => ({ ...prev, cache: false }));
    }
  };

  const handleCreateBackup = async () => {
    setOpLoading(prev => ({ ...prev, backup: true }));
    try {
      const res = await adminAPI.generateBackup();
      const bkp = res.data;
      setOpFeedback(prev => ({
        ...prev,
        backup: `Backup ${bkp.backup_id} generated (${bkp.records_count?.predictions || 0} predictions, ${bkp.records_count?.users || 0} users).`
      }));
      setTimeout(() => setOpFeedback(prev => ({ ...prev, backup: '' })), 8000);
    } catch (err) {
      alert("Backup creation failed: " + (err.response?.data?.detail || err.message));
    } finally {
      setOpLoading(prev => ({ ...prev, backup: false }));
    }
  };

  // --- Broadcast Dispatch Handler ---
  const handleSendBroadcast = async (e) => {
    e.preventDefault();
    if (!broadcast.title.trim() || !broadcast.message.trim()) {
      alert("Please provide both a broadcast title and message.");
      return;
    }
    setSendingBroadcast(true);
    setBroadcastResult('');
    try {
      const res = await adminAPI.broadcastNotice(broadcast);
      setBroadcastResult(res.data?.message || `Dispatched to ${res.data?.recipients_notified} users.`);
      setBroadcast({ title: '', message: '', type: 'system', priority: 'Medium', target_role: 'all' });
      setTimeout(() => setBroadcastResult(''), 6000);
    } catch (err) {
      alert("Broadcast failed: " + (err.response?.data?.detail || err.message));
    } finally {
      setSendingBroadcast(false);
    }
  };

  return (
    <div className="w-full space-y-6 z-10 font-sans pb-16">
      
      {/* Global Status Banner Notifications */}
      {savedBanner && (
        <div className="p-4 rounded-2xl bg-emerald-500/20 border border-emerald-500/50 text-emerald-300 font-mono text-xs font-bold flex items-center justify-between shadow-lg shadow-emerald-500/10 animate-in fade-in slide-in-from-top-2">
          <div className="flex items-center space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span>{savedBanner}</span>
          </div>
          <button onClick={() => setSavedBanner('')} className="text-emerald-400 hover:text-white text-sm cursor-pointer">✕</button>
        </div>
      )}

      {errorBanner && (
        <div className="p-4 rounded-2xl bg-red-500/20 border border-red-500/50 text-red-300 font-mono text-xs font-bold flex items-center justify-between shadow-lg shadow-red-500/10 animate-in fade-in slide-in-from-top-2">
          <div className="flex items-center space-x-2">
            <AlertTriangle className="w-4 h-4 text-red-400" />
            <span>{errorBanner}</span>
          </div>
          <button onClick={() => setErrorBanner('')} className="text-red-400 hover:text-white text-sm cursor-pointer">✕</button>
        </div>
      )}

      {/* 1. TOP SECTION: PROFILE SUMMARY + AUTHENTICATED PARAMETERS */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* Left: Admin Identity HUD */}
        <div className="lg:col-span-5 space-y-4">
          <HolographicHUDPanel glowColor="red" className="p-6 text-center">
            <div className="w-24 h-24 rounded-full bg-gradient-to-tr from-red-500 via-purple-600 to-cyan-400 p-1 mx-auto shadow-xl shadow-red-500/20">
              <div className="w-full h-full rounded-full bg-[#080214] flex items-center justify-center font-extrabold text-3xl text-white">
                {user?.full_name ? user.full_name.charAt(0) : 'A'}
              </div>
            </div>

            <div className="mt-4 space-y-1">
              <div className="text-2xl font-extrabold text-white">{user?.full_name || 'Dr. Administrator'}</div>
              <div className="text-xs font-mono font-bold text-red-400 uppercase tracking-widest">{user?.role || 'SUPER ADMINISTRATOR'}</div>
            </div>

            <div className="mt-4 px-4 py-1.5 rounded-full bg-red-500/20 text-red-300 border border-red-500/40 text-xs font-mono font-bold inline-flex items-center space-x-2">
              <span className="w-2 h-2 rounded-full bg-red-400 animate-ping" />
              <span>SUPER ADMIN PRIVILEGES • FULL SCOPE</span>
            </div>

            <div className="mt-5 pt-4 border-t border-[#2A1A4E] grid grid-cols-2 gap-2 text-[11px] font-mono">
              <div className="bg-[#120A24] p-2.5 rounded-xl border border-[#2A1A4E] text-slate-300">
                <span className="text-[10px] text-slate-400 block uppercase">Status</span>
                <span className="font-bold text-emerald-400">ACTIVE SESSION</span>
              </div>
              <div className="bg-[#120A24] p-2.5 rounded-xl border border-[#2A1A4E] text-slate-300">
                <span className="text-[10px] text-slate-400 block uppercase">Protocol</span>
                <span className="font-bold text-purple-300">HIPAA & RBAC</span>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-[#2A1A4E]">
              <button
                type="button"
                onClick={() => setIsDoctorModalOpen(true)}
                className="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-[#6D28D9] to-[#7C3AED] hover:brightness-110 text-white font-mono font-bold text-xs flex items-center justify-center space-x-2 shadow-lg shadow-[#7C3AED]/25 cursor-pointer transition"
              >
                <UserPlus className="w-4 h-4" />
                <span>+ Provision Doctor Account</span>
              </button>
            </div>
          </HolographicHUDPanel>
        </div>

        {/* Right: Platform Health & Active Session Parameters */}
        <div className="lg:col-span-7 space-y-4 font-mono text-xs">
          <HolographicHUDPanel 
            title="ADMINISTRATOR SESSION & SYSTEM PARAMETERS" 
            subtitle="Authenticated Session Parameters, Clearance & Global State"
            glowColor="purple"
          >
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
              <div className="bg-[#0D0718] p-3.5 rounded-xl border border-[#2A1A4E] space-y-1">
                <span className="text-[10px] text-slate-400 uppercase font-bold">AUTHENTICATED USERNAME</span>
                <div className="text-sm font-bold text-white flex items-center space-x-1.5">
                  <ShieldCheck className="w-4 h-4 text-red-400" />
                  <span>{user?.username || 'admin'}</span>
                </div>
              </div>

              <div className="bg-[#0D0718] p-3.5 rounded-xl border border-[#2A1A4E] space-y-1">
                <span className="text-[10px] text-slate-400 uppercase font-bold">ADMINISTRATOR EMAIL</span>
                <div className="text-sm font-bold text-purple-300 flex items-center space-x-1.5">
                  <Mail className="w-4 h-4 text-purple-400" />
                  <span>{user?.email || 'admin@smartcare.ai'}</span>
                </div>
              </div>

              <div className="bg-[#0D0718] p-3.5 rounded-xl border border-[#2A1A4E] space-y-1">
                <span className="text-[10px] text-slate-400 uppercase font-bold">PLATFORM MODE</span>
                <div className="text-sm font-bold">
                  {settings.maintenance_mode ? (
                    <span className="text-amber-400 flex items-center space-x-1">
                      <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse" />
                      <span>MAINTENANCE (Restricted)</span>
                    </span>
                  ) : (
                    <span className="text-emerald-400 flex items-center space-x-1">
                      <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                      <span>ONLINE (Operational)</span>
                    </span>
                  )}
                </div>
              </div>

              <div className="bg-[#0D0718] p-3.5 rounded-xl border border-[#2A1A4E] space-y-1">
                <span className="text-[10px] text-slate-400 uppercase font-bold">AI INFERENCE ENGINE</span>
                <div className="text-sm font-bold">
                  {settings.ai_service_enabled ? (
                    <span className="text-emerald-400 flex items-center space-x-1">
                      <Cpu className="w-4 h-4 text-emerald-400" />
                      <span>ACTIVE ONLINE</span>
                    </span>
                  ) : (
                    <span className="text-red-400 flex items-center space-x-1">
                      <AlertTriangle className="w-4 h-4 text-red-400" />
                      <span>PAUSED</span>
                    </span>
                  )}
                </div>
              </div>
            </div>

            <div className="mt-3.5 p-3 rounded-xl bg-[#120A24] border border-[#2A1A4E] flex items-center justify-between text-[11px]">
              <div className="flex items-center space-x-2 text-slate-300">
                <Server className="w-4 h-4 text-cyan-400" />
                <span>MongoDB Primary Cluster: <strong className="text-white">smartcare_ai</strong> (14 Primary Collections)</span>
              </div>
              <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/30 text-[10px]">
                CONNECTED
              </span>
            </div>
          </HolographicHUDPanel>
        </div>

      </div>

      {/* 2. SECTION: WEBSITE & PLATFORM MAINTENANCE CONTROLS */}
      <HolographicHUDPanel 
        title="1. WEBSITE & SYSTEM MAINTENANCE CONTROL CENTER" 
        subtitle="Global Platform Availability, Maintenance Access Rules & AI Service Governance"
        glowColor="red"
      >
        <div className="space-y-5 text-xs font-mono">
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            
            {/* Maintenance Mode Switch Card */}
            <div className="p-4 rounded-2xl bg-[#0D0718] border border-[#2A1A4E] space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-white font-bold text-sm font-sans flex items-center space-x-2">
                    <ShieldAlert className="w-4 h-4 text-amber-400" />
                    <span>Maintenance Mode</span>
                  </div>
                  <div className="text-[10px] text-slate-400">Restrict access to authorized roles only</div>
                </div>
                <button
                  type="button"
                  onClick={handleToggleMaintenance}
                  className={`px-4 py-2 rounded-full font-bold text-xs uppercase cursor-pointer transition shadow-md flex items-center space-x-1.5 ${
                    settings.maintenance_mode 
                      ? 'bg-amber-500 text-black shadow-amber-500/30 ring-2 ring-amber-400' 
                      : 'bg-emerald-600/30 text-emerald-400 border border-emerald-500/40 hover:bg-emerald-600/40'
                  }`}
                >
                  {settings.maintenance_mode ? <ToggleRight className="w-4 h-4" /> : <ToggleLeft className="w-4 h-4" />}
                  <span>{settings.maintenance_mode ? 'ENABLED (Restricted)' : 'DISABLED (Online)'}</span>
                </button>
              </div>

              {settings.maintenance_mode && (
                <div className="space-y-2 pt-2 border-t border-[#2A1A4E] animate-in fade-in">
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
                              : 'bg-[#120A24] text-slate-400 border border-[#2A1A4E] hover:border-purple-500/50'
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
                  <div className="text-white font-bold text-sm font-sans flex items-center space-x-2">
                    <Cpu className="w-4 h-4 text-purple-400" />
                    <span>AI Inference Engine</span>
                  </div>
                  <div className="text-[10px] text-slate-400">Multi-Disease Ensemble & Tree SHAP</div>
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
                <label className="text-[10px] text-[#C084FC] uppercase font-bold">Website Operational Status</label>
                <select
                  value={settings.website_status || (settings.maintenance_mode ? "MAINTENANCE" : "ONLINE")}
                  onChange={(e) => handleWebsiteStatusChange(e.target.value)}
                  className="w-full bg-[#120A24] border border-[#3B206B] rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-red-500 cursor-pointer"
                >
                  <option value="ONLINE">Website Online (Operational)</option>
                  <option value="MAINTENANCE">Maintenance Mode (Restricted Access)</option>
                  <option value="OFFLINE">Website Offline</option>
                </select>
              </div>
            </div>

          </div>

          {/* Maintenance Notice & Report Settings Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            
            {/* Patient Maintenance Notice */}
            <div className="space-y-1.5">
              <label className="text-[10px] text-[#C084FC] uppercase font-bold">Patient Maintenance Notice Message</label>
              <input
                type="text"
                value={settings.maintenance_message || ''}
                onChange={(e) => setSettings(s => ({ ...s, maintenance_message: e.target.value }))}
                placeholder="SmartCare AI is temporarily unavailable due to scheduled maintenance."
                className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-purple-500"
              />
            </div>

            {/* Session Timeout */}
            <div className="space-y-1.5">
              <label className="text-[10px] text-[#C084FC] uppercase font-bold">Session Inactivity Timeout</label>
              <select
                value={settings.session_timeout || 1440}
                onChange={(e) => setSettings(s => ({ ...s, session_timeout: Number(e.target.value) }))}
                className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-purple-500 cursor-pointer"
              >
                <option value={15}>15 Minutes (High Security)</option>
                <option value={30}>30 Minutes</option>
                <option value={60}>60 Minutes (1 Hour)</option>
                <option value={480}>8 Hours (Clinical Shift)</option>
                <option value={1440}>24 Hours (Standard Session)</option>
              </select>
            </div>

          </div>

          {/* Regulatory Clinical Disclaimer */}
          <div className="space-y-1.5">
            <label className="text-[10px] text-[#C084FC] uppercase font-bold">Clinical Regulatory Disclaimer (Appears on all 7-Page Reports)</label>
            <textarea
              rows={2}
              value={settings.report_disclaimer || ''}
              onChange={(e) => setSettings(s => ({ ...s, report_disclaimer: e.target.value }))}
              className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-purple-500 resize-none"
            />
          </div>

          {/* Multilingual Support Toggles */}
          <div className="space-y-2">
            <label className="text-[10px] text-[#C084FC] uppercase font-bold">Supported Report & Chatbot Languages</label>
            <div className="flex flex-wrap gap-2.5">
              {[
                { code: 'en', label: 'English (US/UK)' },
                { code: 'ta', label: 'Tamil (தமிழ்)' },
                { code: 'hi', label: 'Hindi (हिन्दी)' }
              ].map(lang => {
                const isActive = (settings.supported_languages || []).includes(lang.code);
                return (
                  <button
                    key={lang.code}
                    type="button"
                    onClick={() => handleToggleLanguage(lang.code)}
                    className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 cursor-pointer ${
                      isActive 
                        ? 'bg-purple-600/40 text-purple-200 border border-purple-500 shadow-sm shadow-purple-500/30' 
                        : 'bg-[#0D0718] text-slate-400 border border-[#2A1A4E]'
                    }`}
                  >
                    <span>{lang.label}</span>
                    <span className="text-[10px]">{isActive ? '✓' : '+'}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Save Controls Button */}
          <div className="flex justify-end pt-2">
            <button
              type="button"
              onClick={handleSaveSettings}
              disabled={savingSettings}
              className="px-6 py-3 rounded-xl bg-gradient-to-r from-[#6D28D9] to-[#EF4444] text-white font-bold text-xs uppercase tracking-wider hover:brightness-110 transition shadow-lg shadow-red-500/20 cursor-pointer disabled:opacity-50 flex items-center space-x-2"
            >
              {savingSettings ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Applying System Controls...</span>
                </>
              ) : (
                <>
                  <ShieldCheck className="w-4 h-4" />
                  <span>Save Global Platform Controls</span>
                </>
              )}
            </button>
          </div>

        </div>
      </HolographicHUDPanel>

      {/* 3. SECTION: LIVE DATABASE & SYSTEM INFRASTRUCTURE OPERATIONS */}
      <HolographicHUDPanel 
        title="2. DATABASE & INFRASTRUCTURE OPERATIONS" 
        subtitle="Direct Database Indexing, Cache Invalidation, Snapshot Archival & Backup Controls"
        glowColor="cyan"
      >
        <div className="space-y-4 text-xs font-mono">
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            
            {/* Action 1: Reindex MongoDB */}
            <div className="p-4 rounded-2xl bg-[#0D0718] border border-[#2A1A4E] flex flex-col justify-between space-y-3">
              <div className="space-y-1.5">
                <div className="text-white font-bold text-sm font-sans flex items-center space-x-2">
                  <Database className="w-4 h-4 text-cyan-400" />
                  <span>MongoDB Re-Indexing</span>
                </div>
                <p className="text-[11px] text-slate-400">
                  Rebuild and optimize query indexes across all 14 MongoDB collections.
                </p>
                {opFeedback.reindex && (
                  <div className="text-[10px] text-emerald-400 font-bold animate-in fade-in">
                    ✓ {opFeedback.reindex}
                  </div>
                )}
              </div>
              <button
                type="button"
                onClick={handleReindexDB}
                disabled={opLoading.reindex}
                className="w-full py-2.5 px-4 rounded-xl bg-cyan-600/20 hover:bg-cyan-600/30 border border-cyan-500/40 text-cyan-300 font-bold transition flex items-center justify-center space-x-2 cursor-pointer disabled:opacity-50"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${opLoading.reindex ? 'animate-spin' : ''}`} />
                <span>{opLoading.reindex ? 'Optimizing Indexes...' : 'Re-Index Collections'}</span>
              </button>
            </div>

            {/* Action 2: Purge Cache */}
            <div className="p-4 rounded-2xl bg-[#0D0718] border border-[#2A1A4E] flex flex-col justify-between space-y-3">
              <div className="space-y-1.5">
                <div className="text-white font-bold text-sm font-sans flex items-center space-x-2">
                  <Trash2 className="w-4 h-4 text-purple-400" />
                  <span>Purge Prediction Cache</span>
                </div>
                <p className="text-[11px] text-slate-400">
                  Flush transient tensor memory, XAI SHAP cache, and temporary buffers.
                </p>
                {opFeedback.cache && (
                  <div className="text-[10px] text-emerald-400 font-bold animate-in fade-in">
                    ✓ {opFeedback.cache}
                  </div>
                )}
              </div>
              <button
                type="button"
                onClick={handleClearCache}
                disabled={opLoading.cache}
                className="w-full py-2.5 px-4 rounded-xl bg-purple-600/20 hover:bg-purple-600/30 border border-purple-500/40 text-purple-300 font-bold transition flex items-center justify-center space-x-2 cursor-pointer disabled:opacity-50"
              >
                <Sparkles className="w-3.5 h-3.5" />
                <span>{opLoading.cache ? 'Purging Cache...' : 'Clear Prediction Cache'}</span>
              </button>
            </div>

            {/* Action 3: Generate System Backup */}
            <div className="p-4 rounded-2xl bg-[#0D0718] border border-[#2A1A4E] flex flex-col justify-between space-y-3">
              <div className="space-y-1.5">
                <div className="text-white font-bold text-sm font-sans flex items-center space-x-2">
                  <Download className="w-4 h-4 text-emerald-400" />
                  <span>Snapshot Archival</span>
                </div>
                <p className="text-[11px] text-slate-400">
                  Export an encrypted snapshot of all patient records, predictions and audit logs.
                </p>
                {opFeedback.backup && (
                  <div className="text-[10px] text-emerald-400 font-bold animate-in fade-in">
                    ✓ {opFeedback.backup}
                  </div>
                )}
              </div>
              <button
                type="button"
                onClick={handleCreateBackup}
                disabled={opLoading.backup}
                className="w-full py-2.5 px-4 rounded-xl bg-emerald-600/20 hover:bg-emerald-600/30 border border-emerald-500/40 text-emerald-300 font-bold transition flex items-center justify-center space-x-2 cursor-pointer disabled:opacity-50"
              >
                <Download className="w-3.5 h-3.5" />
                <span>{opLoading.backup ? 'Creating Snapshot...' : 'Export Platform Backup'}</span>
              </button>
            </div>

          </div>

        </div>
      </HolographicHUDPanel>

      {/* CRITICAL DANGER ZONE: 2FA-SECURED SYSTEM FACTORY RESET & DATA PURGE */}
      <HolographicHUDPanel 
        title="⚠️ CRITICAL DANGER ZONE • 2FA SYSTEM FACTORY RESET" 
        subtitle="Exclusive to Super Administrator • Requires 2-Factor Authentication & Cryptographic Verification"
        glowColor="red"
        className="border-2 border-red-500/50 bg-[#0E0614]"
      >
        <div className="space-y-4 text-xs font-mono">
          <div className="p-4 rounded-2xl bg-red-950/30 border border-red-500/40 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="space-y-1.5 max-w-2xl">
              <div className="flex items-center space-x-2">
                <Flame className="w-5 h-5 text-red-400 animate-pulse" />
                <span className="text-white font-bold text-sm font-sans">
                  Total SmartCare AI Data Wipe & Factory Reset
                </span>
                <span className="px-2 py-0.5 rounded-full bg-red-500/20 text-red-300 font-bold border border-red-500/40 text-[9px] uppercase">
                  Admin Only • 2FA Guarded
                </span>
              </div>
              <p className="text-[11px] text-red-200/80 leading-relaxed font-sans">
                Permanently purge all patient records, ML disease predictions, SHAP explainability caches, 
                wellness plans, chatbot sessions, clinical alerts, and custom doctor/staff accounts. 
                Re-seeds the entire platform back to the pristine genesis state with default seed accounts (<span className="text-red-300 font-mono">admin@smartcare.ai</span>, <span className="text-purple-300 font-mono">doctor@smartcare.ai</span>, <span className="text-teal-300 font-mono">patient@smartcare.ai</span>).
              </p>
            </div>

            <button
              type="button"
              onClick={() => setIsResetModalOpen(true)}
              className="shrink-0 px-6 py-3.5 rounded-xl bg-gradient-to-r from-red-600 via-rose-600 to-red-700 hover:brightness-110 text-white font-extrabold text-xs tracking-wider uppercase transition shadow-xl shadow-red-600/30 flex items-center justify-center space-x-2.5 cursor-pointer ring-2 ring-red-500/50 hover:scale-[1.02] active:scale-95"
            >
              <Flame className="w-4 h-4 text-amber-300" />
              <span>Reset Total SmartCare AI Data</span>
            </button>
          </div>
        </div>
      </HolographicHUDPanel>

      {/* 4. SECTION: SYSTEM BROADCAST ANNOUNCEMENT DISPATCHER */}
      <HolographicHUDPanel 
        title="3. PLATFORM-WIDE BROADCAST ANNOUNCEMENT DISPATCHER" 
        subtitle="Push Instant System Notifications to Patients, Doctors, or All Platform Users"
        glowColor="purple"
      >
        <form onSubmit={handleSendBroadcast} className="space-y-4 text-xs font-mono">
          
          {broadcastResult && (
            <div className="p-3 rounded-xl bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 font-bold flex items-center space-x-2 animate-in fade-in">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>✓ {broadcastResult}</span>
            </div>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="space-y-1">
              <label className="text-[10px] text-[#C084FC] uppercase font-bold">Target Audience</label>
              <select
                value={broadcast.target_role}
                onChange={(e) => setBroadcast(b => ({ ...b, target_role: e.target.value }))}
                className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-purple-500 cursor-pointer"
              >
                <option value="all">All Platform Users (Global)</option>
                <option value="patient">Patients Only</option>
                <option value="doctor">Doctors / Clinicians Only</option>
                <option value="staff">Staff Only</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-[10px] text-[#C084FC] uppercase font-bold">Alert Category</label>
              <select
                value={broadcast.type}
                onChange={(e) => setBroadcast(b => ({ ...b, type: e.target.value }))}
                className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-purple-500 cursor-pointer"
              >
                <option value="system">System Notification</option>
                <option value="warning">Maintenance Notice</option>
                <option value="info">Platform Information</option>
                <option value="security">Security Alert</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-[10px] text-[#C084FC] uppercase font-bold">Priority Level</label>
              <select
                value={broadcast.priority}
                onChange={(e) => setBroadcast(b => ({ ...b, priority: e.target.value }))}
                className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-purple-500 cursor-pointer"
              >
                <option value="Low">Low Priority</option>
                <option value="Medium">Medium Priority</option>
                <option value="High">High Priority</option>
                <option value="Critical">Critical Priority (Immediate)</option>
              </select>
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-[10px] text-[#C084FC] uppercase font-bold">Broadcast Title / Headline</label>
            <input
              type="text"
              value={broadcast.title}
              onChange={(e) => setBroadcast(b => ({ ...b, title: e.target.value }))}
              placeholder="e.g. Scheduled Maintenance Window • SmartCare AI Platform Update"
              className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-purple-500"
            />
          </div>

          <div className="space-y-1">
            <label className="text-[10px] text-[#C084FC] uppercase font-bold">Broadcast Message Content</label>
            <textarea
              rows={2}
              value={broadcast.message}
              onChange={(e) => setBroadcast(b => ({ ...b, message: e.target.value }))}
              placeholder="Enter message text that will be received in real-time by all targeted users..."
              className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-purple-500 resize-none"
            />
          </div>

          <div className="flex justify-end pt-1">
            <button
              type="submit"
              disabled={sendingBroadcast}
              className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-purple-600 to-cyan-500 hover:brightness-110 text-white font-bold text-xs uppercase tracking-wider transition shadow-lg shadow-purple-500/20 cursor-pointer disabled:opacity-50 flex items-center space-x-2"
            >
              <Send className="w-3.5 h-3.5" />
              <span>{sendingBroadcast ? 'Dispatching Notice...' : 'Dispatch Broadcast Notice'}</span>
            </button>
          </div>

        </form>
      </HolographicHUDPanel>

      {/* 5. SECTION: MODULE CLEARANCE & ACCESS POLICIES */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start font-mono text-xs">
        
        {/* Module Permissions Clearance */}
        <div className="lg:col-span-6 space-y-4">
          <HolographicHUDPanel 
            title="ROLE & MODULE CLEARANCE MATRIX" 
            subtitle="Access control policies across SmartCare clinical AI modules"
            glowColor="purple"
          >
            <div className="space-y-2.5">
              {[
                { perm: 'Module 1: Preprocessing & Data Profiling', status: 'FULL CONTROL' },
                { perm: 'Module 2: Multi-Task Risk Inference', status: 'FULL CONTROL' },
                { perm: 'Module 3: SHAP Explainability Engine', status: 'FULL CONTROL' },
                { perm: 'Module 4: Personalized Wellness AI', status: 'FULL CONTROL' },
                { perm: 'Module 5: Clinical Decision Support & CDS', status: 'FULL CONTROL' },
                { perm: 'Module 6: Dashboard & Wellness Chatbot', status: 'FULL CONTROL' },
                { perm: 'Model Registry & Deployment', status: 'ADMIN ACCESS' },
                { perm: 'User Account & System Security', status: 'SUPER ADMIN' }
              ].map((p, i) => (
                <div key={i} className="p-3 rounded-xl bg-[#0D0718] border border-[#2A1A4E] flex justify-between items-center">
                  <span className="text-slate-300 font-bold">{p.perm}</span>
                  <span className="px-2.5 py-0.5 rounded-full text-[9px] font-bold bg-purple-500/20 text-purple-300 border border-purple-500/40">
                    {p.status}
                  </span>
                </div>
              ))}
            </div>
          </HolographicHUDPanel>
        </div>

        {/* Active Security Sessions & Access Protocols */}
        <div className="lg:col-span-6 space-y-4">
          <HolographicHUDPanel 
            title="ACTIVE SESSIONS & SECURITY AUDIT" 
            subtitle="Recent login history, cryptographic tokens & security compliance"
            glowColor="cyan"
          >
            <div className="space-y-3">
              <div className="p-3.5 rounded-xl bg-[#0D0718] border border-[#2A1A4E] space-y-1">
                <div className="flex justify-between items-center">
                  <span className="text-white font-bold flex items-center space-x-1.5 font-sans">
                    <Monitor className="w-4 h-4 text-cyan-400" />
                    <span>Current Active Session</span>
                  </span>
                  <span className="text-[9px] bg-teal-500/20 text-teal-300 px-2 py-0.5 rounded font-bold border border-teal-500/30">
                    ONLINE (ENCRYPTED)
                  </span>
                </div>
                <div className="text-[10px] text-slate-400 pt-1 flex justify-between">
                  <span>Client: Web Client</span>
                  <span>Scope: System Administrator</span>
                  <span>JWT Encrypted</span>
                </div>
              </div>

              <div className="p-3.5 rounded-xl bg-[#0D0718] border border-[#2A1A4E] space-y-1">
                <div className="flex justify-between items-center">
                  <span className="text-slate-300 font-bold flex items-center space-x-1.5 font-sans">
                    <ShieldCheck className="w-4 h-4 text-purple-400" />
                    <span>System Access Protocol</span>
                  </span>
                  <span className="text-cyan-400 font-bold text-[10px]">HIPAA & SOC-2 COMPLIANT</span>
                </div>
                <div className="text-[10px] text-slate-400 pt-1">
                  OAuth2 Password Flow + JWT Bearer Token Authentication with Role Isolation
                </div>
              </div>

              <div className="p-3.5 rounded-xl bg-[#0D0718] border border-[#2A1A4E] space-y-1">
                <div className="flex justify-between items-center">
                  <span className="text-slate-300 font-bold flex items-center space-x-1.5 font-sans">
                    <Lock className="w-4 h-4 text-red-400" />
                    <span>Audit Trail Immortality</span>
                  </span>
                  <span className="text-emerald-400 font-bold text-[10px]">APPEND ONLY</span>
                </div>
                <div className="text-[10px] text-slate-400 pt-1">
                  All administrative mutations are recorded in immutable MongoDB security audit logs.
                </div>
              </div>
            </div>
          </HolographicHUDPanel>
        </div>

      </div>

      {/* Provision Doctor Modal */}
      <CreateStaffAccountModal
        isOpen={isDoctorModalOpen}
        onClose={() => setIsDoctorModalOpen(false)}
        defaultRole="DOCTOR"
        onSuccess={(doc) => {
          setSavedBanner(`Doctor account '${doc?.full_name || doc?.username}' provisioned and activated successfully!`);
          setTimeout(() => setSavedBanner(''), 6000);
        }}
      />

      {/* 2FA System Factory Reset Modal (Admin Role Only) */}
      <SystemReset2FAModal
        isOpen={isResetModalOpen}
        onClose={() => setIsResetModalOpen(false)}
        onSuccess={(res) => {
          setSavedBanner("Total SmartCare AI system has been reset to baseline defaults successfully.");
        }}
      />

    </div>
  );
}
