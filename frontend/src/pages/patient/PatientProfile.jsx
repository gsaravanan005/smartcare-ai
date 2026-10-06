import React, { useState, useEffect } from 'react';
import HolographicHUDPanel from '../../components/HolographicHUDPanel';
import { patientAPI } from '../../services/api';
import { 
  User, Mail, Phone, Calendar, ShieldCheck, Heart, 
  Activity, Sparkles, CheckCircle2, RefreshCw, AlertCircle,
  Save, Lock, FileText, Settings, KeyRound
} from 'lucide-react';

export default function PatientProfile({ user }) {
  const [profile, setProfile] = useState({
    age: '',
    sex: 'Male',
    height_cm: '',
    weight_kg: '',
    bmi: '',
    education_level: '',
    income_level: ''
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [savedBanner, setSavedBanner] = useState('');
  const [errorBanner, setErrorBanner] = useState('');

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    setLoading(true);
    setErrorBanner('');
    try {
      const res = await patientAPI.getProfile();
      if (res.data) {
        setProfile({
          age: res.data.age || '',
          sex: res.data.sex === 1 ? 'Male' : (res.data.sex === 0 ? 'Female' : 'Male'),
          height_cm: res.data.height_cm || '',
          weight_kg: res.data.weight_kg || '',
          bmi: res.data.bmi || '',
          education_level: res.data.education_level || '',
          income_level: res.data.income_level || ''
        });
      }
    } catch (err) {
      console.error("Failed to load patient profile:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveProfile = async (e) => {
    e.preventDefault();
    setSaving(true);
    setSavedBanner('');
    setErrorBanner('');

    try {
      const payload = {
        age: profile.age ? parseInt(profile.age) : null,
        sex: profile.sex === 'Male' ? 1 : 0,
        height_cm: profile.height_cm ? parseFloat(profile.height_cm) : null,
        weight_kg: profile.weight_kg ? parseFloat(profile.weight_kg) : null,
        education_level: profile.education_level ? parseInt(profile.education_level) : null,
        income_level: profile.income_level ? parseInt(profile.income_level) : null
      };

      const res = await patientAPI.updateProfile(payload);
      if (res.data && res.data.bmi) {
        setProfile(prev => ({ ...prev, bmi: res.data.bmi }));
      }
      setSavedBanner('Your patient profile and baseline vitals have been successfully updated.');
      setTimeout(() => setSavedBanner(''), 4000);
    } catch (err) {
      setErrorBanner('Failed to save profile changes. Please check your inputs.');
      setTimeout(() => setErrorBanner(''), 4000);
    } finally {
      setSaving(false);
    }
  };

  const computedBMI = () => {
    if (profile.bmi) return profile.bmi;
    if (profile.height_cm && profile.weight_kg) {
      const h_m = parseFloat(profile.height_cm) / 100;
      const w_kg = parseFloat(profile.weight_kg);
      if (h_m > 0) return (w_kg / (h_m * h_m)).toFixed(2);
    }
    return '--';
  };

  return (
    <div className="w-full space-y-6 font-sans pb-12">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-[#0D0A1A] via-[#141025] to-[#0D0A1A] border border-[#29213F] rounded-3xl p-6 shadow-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-xs font-mono text-purple-400 mb-1">
            <User className="w-4 h-4 text-[#C084FC]" />
            <span className="font-bold uppercase tracking-widest text-[#C084FC]">PATIENT IDENTITY & HEALTH PROFILE</span>
          </div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
            {user?.full_name || user?.username || 'Patient Profile'}
          </h1>
          <p className="text-xs text-slate-300 font-sans mt-1">
            Manage your personal demographics, clinical baseline vitals, and privacy settings.
          </p>
        </div>

        <div className="flex items-center space-x-3 text-xs font-mono">
          <div className="px-3.5 py-2 rounded-xl bg-purple-500/10 border border-purple-500/30 text-purple-300 flex items-center space-x-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>ACCOUNT STATUS: ACTIVE</span>
          </div>
        </div>
      </div>

      {/* Status Notifications */}
      {savedBanner && (
        <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/40 text-emerald-300 text-xs font-mono flex items-center space-x-2 animate-in fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
          <span>{savedBanner}</span>
        </div>
      )}

      {errorBanner && (
        <div className="p-4 rounded-2xl bg-red-500/10 border border-red-500/40 text-red-300 text-xs font-mono flex items-center space-x-2 animate-in fade-in">
          <AlertCircle className="w-4 h-4 text-red-400 flex-shrink-0" />
          <span>{errorBanner}</span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Account Details Card */}
        <div className="space-y-6">
          <HolographicHUDPanel title="ACCOUNT INFORMATION" subtitle="SECURITY & CREDENTIALS" glowColor="purple">
            <div className="space-y-4 font-mono text-xs">
              <div className="flex items-center justify-center py-4">
                <div className="w-20 h-20 rounded-2xl bg-gradient-to-tr from-[#7C3AED] to-[#C084FC] flex items-center justify-center text-white text-2xl font-bold shadow-lg shadow-purple-900/40 border border-purple-400/40">
                  {(user?.full_name || user?.username || 'P')[0].toUpperCase()}
                </div>
              </div>

              <div className="space-y-3 divide-y divide-[#2A1A4E]/60">
                <div className="pt-2 flex justify-between items-center">
                  <span className="text-slate-400">Full Name</span>
                  <span className="text-white font-bold">{user?.full_name || user?.username || 'Patient'}</span>
                </div>
                <div className="pt-2 flex justify-between items-center">
                  <span className="text-slate-400">Username</span>
                  <span className="text-purple-300">{user?.username || 'patient'}</span>
                </div>
                <div className="pt-2 flex justify-between items-center">
                  <span className="text-slate-400">Email Address</span>
                  <span className="text-white">{user?.email || 'patient@smartcare.ai'}</span>
                </div>
                <div className="pt-2 flex justify-between items-center">
                  <span className="text-slate-400">Role</span>
                  <span className="px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30 uppercase text-[10px]">
                    {user?.role || 'patient'}
                  </span>
                </div>
                <div className="pt-2 flex justify-between items-center">
                  <span className="text-slate-400">Patient ID</span>
                  <span className="text-emerald-400 font-bold">#{user?.id || 100}</span>
                </div>
              </div>
            </div>
          </HolographicHUDPanel>

          {/* Privacy & Compliance Card */}
          <div className="p-5 rounded-2xl bg-[#0D0718]/90 border border-[#2A1A4E] space-y-3 font-mono text-xs">
            <div className="flex items-center space-x-2 text-emerald-400 font-bold">
              <ShieldCheck className="w-4 h-4" />
              <span>HIPAA DATA PRIVACY</span>
            </div>
            <p className="text-slate-400 text-[11px] leading-relaxed">
              Your medical health records, AI risk assessments, and lifestyle logs are encrypted at rest with AES-256 and protected by role-isolated data boundaries.
            </p>
          </div>
        </div>

        {/* Right Column: Editable Baseline Biometrics */}
        <div className="lg:col-span-2 space-y-6">
          <HolographicHUDPanel title="CLINICAL BASELINE & DEMOGRAPHICS" subtitle="UPDATE HEALTH METRICS" glowColor="purple">
            {loading ? (
              <div className="py-12 flex flex-col items-center justify-center space-y-3 text-purple-400 font-mono text-xs">
                <RefreshCw className="w-6 h-6 animate-spin" />
                <span>Loading patient profile...</span>
              </div>
            ) : (
              <form onSubmit={handleSaveProfile} className="space-y-6 font-mono text-xs">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {/* Age */}
                  <div className="space-y-1.5">
                    <label className="text-slate-300 font-semibold flex items-center space-x-1.5">
                      <Calendar className="w-3.5 h-3.5 text-purple-400" />
                      <span>Age (Years)</span>
                    </label>
                    <input
                      type="number"
                      min="1"
                      max="120"
                      value={profile.age}
                      onChange={(e) => setProfile({ ...profile, age: e.target.value })}
                      placeholder="e.g. 45"
                      className="w-full px-3.5 py-2.5 rounded-xl bg-[#120826] border border-[#2B1854] text-white focus:outline-none focus:border-[#7C3AED] focus:ring-1 focus:ring-[#7C3AED]"
                    />
                  </div>

                  {/* Sex */}
                  <div className="space-y-1.5">
                    <label className="text-slate-300 font-semibold flex items-center space-x-1.5">
                      <User className="w-3.5 h-3.5 text-purple-400" />
                      <span>Biological Sex</span>
                    </label>
                    <select
                      value={profile.sex}
                      onChange={(e) => setProfile({ ...profile, sex: e.target.value })}
                      className="w-full px-3.5 py-2.5 rounded-xl bg-[#120826] border border-[#2B1854] text-white focus:outline-none focus:border-[#7C3AED] focus:ring-1 focus:ring-[#7C3AED]"
                    >
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                    </select>
                  </div>

                  {/* Height */}
                  <div className="space-y-1.5">
                    <label className="text-slate-300 font-semibold flex items-center space-x-1.5">
                      <Activity className="w-3.5 h-3.5 text-purple-400" />
                      <span>Height (cm)</span>
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      min="50"
                      max="250"
                      value={profile.height_cm}
                      onChange={(e) => setProfile({ ...profile, height_cm: e.target.value })}
                      placeholder="e.g. 175"
                      className="w-full px-3.5 py-2.5 rounded-xl bg-[#120826] border border-[#2B1854] text-white focus:outline-none focus:border-[#7C3AED] focus:ring-1 focus:ring-[#7C3AED]"
                    />
                  </div>

                  {/* Weight */}
                  <div className="space-y-1.5">
                    <label className="text-slate-300 font-semibold flex items-center space-x-1.5">
                      <Heart className="w-3.5 h-3.5 text-purple-400" />
                      <span>Weight (kg)</span>
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      min="20"
                      max="300"
                      value={profile.weight_kg}
                      onChange={(e) => setProfile({ ...profile, weight_kg: e.target.value })}
                      placeholder="e.g. 78"
                      className="w-full px-3.5 py-2.5 rounded-xl bg-[#120826] border border-[#2B1854] text-white focus:outline-none focus:border-[#7C3AED] focus:ring-1 focus:ring-[#7C3AED]"
                    />
                  </div>
                </div>

                {/* BMI Display Banner */}
                <div className="p-4 rounded-xl bg-[#150B33] border border-[#2B1854] flex items-center justify-between">
                  <div>
                    <div className="text-slate-400 text-[11px]">CALCULATED BODY MASS INDEX (BMI)</div>
                    <div className="text-xl font-bold text-white mt-0.5">
                      {computedBMI()} <span className="text-xs font-normal text-slate-400">kg/m²</span>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className="text-[10px] px-2.5 py-1 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30">
                      Auto-Calculated
                    </span>
                  </div>
                </div>

                <div className="flex justify-end space-x-3 pt-2">
                  <button
                    type="button"
                    onClick={fetchProfile}
                    className="px-4 py-2.5 rounded-xl bg-[#150B33] hover:bg-[#1E1045] border border-[#2B1854] text-slate-300 hover:text-white transition flex items-center space-x-1.5 cursor-pointer"
                  >
                    <RefreshCw className="w-3.5 h-3.5" />
                    <span>Reset</span>
                  </button>

                  <button
                    type="submit"
                    disabled={saving}
                    className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-[#7C3AED] to-[#9333EA] hover:brightness-110 text-white font-bold transition flex items-center space-x-2 shadow-lg shadow-purple-900/40 cursor-pointer disabled:opacity-50"
                  >
                    <Save className="w-4 h-4" />
                    <span>{saving ? 'Saving...' : 'Save Profile Changes'}</span>
                  </button>
                </div>
              </form>
            )}
          </HolographicHUDPanel>
        </div>
      </div>
    </div>
  );
}
