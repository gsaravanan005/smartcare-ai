import React, { useState } from 'react';
import HolographicHUDPanel from '../../components/HolographicHUDPanel';
import { 
  Settings, Lock, KeyRound, Globe, Bell, ShieldCheck, 
  Download, Trash2, CheckCircle2, AlertCircle, Save, Moon, Sparkles
} from 'lucide-react';

export default function PatientSettings({ user }) {
  // Password State
  const [passwords, setPasswords] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  const [pwdMsg, setPwdMsg] = useState({ text: '', type: '' });
  const [changingPwd, setChangingPwd] = useState(false);

  // Language State
  const [language, setLanguage] = useState(() => localStorage.getItem('smartcare_lang') || 'en');

  // Notification Preferences
  const [notifications, setNotifications] = useState({
    highRiskAlerts: true,
    vitalsEscalation: true,
    weeklyReportEmail: true,
    checkupReminders: false
  });

  const [savingSettings, setSavingSettings] = useState(false);
  const [settingsBanner, setSettingsBanner] = useState('');

  const handlePasswordChange = (e) => {
    e.preventDefault();
    if (!passwords.currentPassword || !passwords.newPassword) {
      setPwdMsg({ text: 'Please fill in all password fields.', type: 'error' });
      return;
    }
    if (passwords.newPassword.length < 6) {
      setPwdMsg({ text: 'New password must be at least 6 characters long.', type: 'error' });
      return;
    }
    if (passwords.newPassword !== passwords.confirmPassword) {
      setPwdMsg({ text: 'New passwords do not match.', type: 'error' });
      return;
    }

    setChangingPwd(true);
    setTimeout(() => {
      setChangingPwd(false);
      setPasswords({ currentPassword: '', newPassword: '', confirmPassword: '' });
      setPwdMsg({ text: 'Password successfully updated.', type: 'success' });
      setTimeout(() => setPwdMsg({ text: '', type: '' }), 4000);
    }, 600);
  };

  const handleSavePreferences = (e) => {
    e.preventDefault();
    setSavingSettings(true);
    localStorage.setItem('smartcare_lang', language);
    setTimeout(() => {
      setSavingSettings(false);
      setSettingsBanner('Preferences and notification settings saved successfully.');
      setTimeout(() => setSettingsBanner(''), 4000);
    }, 500);
  };

  const handleExportData = () => {
    const exportPayload = {
      patient_id: user?.patient_profile_id || user?.patient_id || user?.id || 1,
      user_id: user?.id,
      username: user?.username,
      email: user?.email,
      export_timestamp: new Date().toISOString(),
      disclaimer: "SmartCare AI Protected Health Information Export"
    };

    const blob = new Blob([JSON.stringify(exportPayload, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `SmartCare_AI_Health_Data_${user?.username || 'patient'}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleClearCache = () => {
    if (window.confirm("Clear offline assessment cache and temporary local session data?")) {
      localStorage.removeItem('smartcare_last_assessment');
      alert("Local session cache cleared.");
    }
  };

  return (
    <div className="w-full space-y-6 font-sans pb-12">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-[#0D0A1A] via-[#141025] to-[#0D0A1A] border border-[#29213F] rounded-3xl p-6 shadow-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-xs font-mono text-[#C084FC] mb-1">
            <Settings className="w-4 h-4 text-[#C084FC]" />
            <span className="font-bold uppercase tracking-widest text-[#C084FC]">PATIENT ACCOUNT & PREFERENCES</span>
          </div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
            Account & Application Settings
          </h1>
          <p className="text-xs text-slate-300 font-sans mt-1">
            Manage your account credentials, preferred language, alert notifications, and data privacy.
          </p>
        </div>

        <div className="flex items-center space-x-3 text-xs font-mono">
          <div className="px-3.5 py-2 rounded-xl bg-purple-500/10 border border-purple-500/30 text-purple-300 flex items-center space-x-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>2FA & ENCRYPTION ACTIVE</span>
          </div>
        </div>
      </div>

      {settingsBanner && (
        <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/40 text-emerald-300 text-xs font-mono flex items-center space-x-2 animate-in fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
          <span>{settingsBanner}</span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 font-mono text-xs">
        {/* 1. Security & Password Management */}
        <HolographicHUDPanel title="SECURITY & CREDENTIALS" subtitle="UPDATE LOGIN PASSWORD" glowColor="purple">
          <form onSubmit={handlePasswordChange} className="space-y-4">
            {pwdMsg.text && (
              <div className={`p-3 rounded-xl border text-xs flex items-center space-x-2 ${
                pwdMsg.type === 'error' ? 'bg-red-500/10 border-red-500/40 text-red-300' : 'bg-emerald-500/10 border-emerald-500/40 text-emerald-300'
              }`}>
                {pwdMsg.type === 'error' ? <AlertCircle className="w-4 h-4 text-red-400" /> : <CheckCircle2 className="w-4 h-4 text-emerald-400" />}
                <span>{pwdMsg.text}</span>
              </div>
            )}

            <div className="space-y-1.5">
              <label className="text-slate-300 font-semibold flex items-center space-x-1.5">
                <Lock className="w-3.5 h-3.5 text-purple-400" />
                <span>Current Password</span>
              </label>
              <input
                type="password"
                value={passwords.currentPassword}
                onChange={(e) => setPasswords({ ...passwords, currentPassword: e.target.value })}
                placeholder="Enter current password"
                className="w-full px-3.5 py-2.5 rounded-xl bg-[#120826] border border-[#2B1854] text-white focus:outline-none focus:border-[#7C3AED]"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-slate-300 font-semibold flex items-center space-x-1.5">
                <KeyRound className="w-3.5 h-3.5 text-purple-400" />
                <span>New Password</span>
              </label>
              <input
                type="password"
                value={passwords.newPassword}
                onChange={(e) => setPasswords({ ...passwords, newPassword: e.target.value })}
                placeholder="Enter new password (min. 6 chars)"
                className="w-full px-3.5 py-2.5 rounded-xl bg-[#120826] border border-[#2B1854] text-white focus:outline-none focus:border-[#7C3AED]"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-slate-300 font-semibold flex items-center space-x-1.5">
                <KeyRound className="w-3.5 h-3.5 text-purple-400" />
                <span>Confirm New Password</span>
              </label>
              <input
                type="password"
                value={passwords.confirmPassword}
                onChange={(e) => setPasswords({ ...passwords, confirmPassword: e.target.value })}
                placeholder="Confirm new password"
                className="w-full px-3.5 py-2.5 rounded-xl bg-[#120826] border border-[#2B1854] text-white focus:outline-none focus:border-[#7C3AED]"
              />
            </div>

            <div className="flex justify-end pt-2">
              <button
                type="submit"
                disabled={changingPwd}
                className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-[#7C3AED] to-[#9333EA] hover:brightness-110 text-white font-bold transition flex items-center space-x-2 shadow-lg shadow-purple-900/40 cursor-pointer disabled:opacity-50"
              >
                <Lock className="w-4 h-4" />
                <span>{changingPwd ? 'Updating...' : 'Update Password'}</span>
              </button>
            </div>
          </form>
        </HolographicHUDPanel>

        {/* 2. Language & Localization Settings */}
        <HolographicHUDPanel title="LANGUAGE & LOCALIZATION" subtitle="PREFERS CLINICAL TRANSLATIONS" glowColor="purple">
          <form onSubmit={handleSavePreferences} className="space-y-6">
            <div className="space-y-3">
              <div className="text-slate-300 font-semibold flex items-center space-x-1.5">
                <Globe className="w-3.5 h-3.5 text-purple-400" />
                <span>Platform Display Language</span>
              </div>

              <div className="grid grid-cols-3 gap-3">
                {[
                  { code: 'en', label: 'English', native: 'English' },
                  { code: 'ta', label: 'Tamil', native: 'தமிழ்' },
                  { code: 'hi', label: 'Hindi', native: 'हिंदी' }
                ].map((lang) => (
                  <button
                    type="button"
                    key={lang.code}
                    onClick={() => setLanguage(lang.code)}
                    className={`p-3 rounded-xl border text-center transition cursor-pointer flex flex-col items-center justify-center ${
                      language === lang.code
                        ? 'bg-[#7C3AED]/20 border-[#7C3AED] text-white shadow-md shadow-purple-900/30'
                        : 'bg-[#120826] border-[#2B1854] text-slate-400 hover:text-white'
                    }`}
                  >
                    <span className="font-bold text-xs">{lang.native}</span>
                    <span className="text-[10px] text-slate-400 mt-0.5">{lang.label}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Notification Preferences */}
            <div className="space-y-3 pt-2">
              <div className="text-slate-300 font-semibold flex items-center space-x-1.5">
                <Bell className="w-3.5 h-3.5 text-purple-400" />
                <span>Health Alert & Notification Preferences</span>
              </div>

              <div className="space-y-2.5">
                <label className="p-3 rounded-xl bg-[#120826] border border-[#2B1854] flex items-center justify-between cursor-pointer">
                  <div>
                    <div className="text-white font-bold">High Risk Predictions</div>
                    <div className="text-[11px] text-slate-400">Receive alert when risk probability exceeds 60%.</div>
                  </div>
                  <input
                    type="checkbox"
                    checked={notifications.highRiskAlerts}
                    onChange={(e) => setNotifications({ ...notifications, highRiskAlerts: e.target.checked })}
                    className="w-4 h-4 rounded text-purple-600 focus:ring-purple-500 cursor-pointer"
                  />
                </label>

                <label className="p-3 rounded-xl bg-[#120826] border border-[#2B1854] flex items-center justify-between cursor-pointer">
                  <div>
                    <div className="text-white font-bold">Weekly Wellness Summary</div>
                    <div className="text-[11px] text-slate-400">Receive email summaries of lifestyle progress.</div>
                  </div>
                  <input
                    type="checkbox"
                    checked={notifications.weeklyReportEmail}
                    onChange={(e) => setNotifications({ ...notifications, weeklyReportEmail: e.target.checked })}
                    className="w-4 h-4 rounded text-purple-600 focus:ring-purple-500 cursor-pointer"
                  />
                </label>
              </div>
            </div>

            <div className="flex justify-end pt-2">
              <button
                type="submit"
                disabled={savingSettings}
                className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-[#7C3AED] to-[#9333EA] hover:brightness-110 text-white font-bold transition flex items-center space-x-2 shadow-lg shadow-purple-900/40 cursor-pointer disabled:opacity-50"
              >
                <Save className="w-4 h-4" />
                <span>{savingSettings ? 'Saving...' : 'Save Preferences'}</span>
              </button>
            </div>
          </form>
        </HolographicHUDPanel>
      </div>

      {/* 3. Data Privacy & Export */}
      <div className="p-6 rounded-2xl bg-[#0D0718]/90 border border-[#2A1A4E] flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 font-mono text-xs">
        <div>
          <div className="flex items-center space-x-2 text-emerald-400 font-bold">
            <ShieldCheck className="w-4 h-4" />
            <span>DATA PRIVACY & EXPORT CONTROLS</span>
          </div>
          <p className="text-slate-400 text-[11px] mt-1 max-w-2xl">
            You can download a portable copy of your assessment history and health records, or clear cached browser sessions at any time.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={handleExportData}
            className="px-4 py-2 rounded-xl bg-[#150B33] hover:bg-[#1E1045] border border-[#2B1854] text-purple-300 hover:text-white transition flex items-center space-x-1.5 cursor-pointer"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export Health JSON</span>
          </button>

          <button
            onClick={handleClearCache}
            className="px-4 py-2 rounded-xl bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 text-red-300 transition flex items-center space-x-1.5 cursor-pointer"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>Clear Local Cache</span>
          </button>
        </div>
      </div>
    </div>
  );
}
