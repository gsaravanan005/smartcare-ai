import React, { useState } from 'react';
import Logo from '../components/Logo';
import HolographicHUDPanel from '../components/HolographicHUDPanel';
import DataFlowVisualization from '../components/DataFlowVisualization';
import { authAPI } from '../services/api';
import { Shield, Sparkles, ArrowRight, CheckCircle2, UserCheck } from 'lucide-react';

export default function PatientRegister({ onRegisterSuccess, onSwitchToLogin }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [phone, setPhone] = useState('');
  const [dateOfBirth, setDateOfBirth] = useState('');
  const [gender, setGender] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await authAPI.register({
        username,
        email,
        password,
        full_name: fullName,
        phone,
        date_of_birth: dateOfBirth,
        gender
      });
      setSuccess(true);
      setTimeout(() => {
        if (onRegisterSuccess) onRegisterSuccess();
      }, 1500);
    } catch (err) {
      setError(err.response?.data?.detail || "Patient registration failed. Please verify input fields.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-7xl mx-auto px-4 py-8 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center min-h-[85vh] z-10 relative font-sans">
      
      {/* LEFT 55%: Branding + Logo + AI Healthcare Visualization */}
      <div className="lg:col-span-7 space-y-6 text-center lg:text-left">
        <div className="space-y-4">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-[#7C3AED]/20 border border-[#7C3AED]/40 text-[#C084FC] text-[10px] font-mono font-bold uppercase tracking-widest">
            <Sparkles className="w-3.5 h-3.5" />
            <span>PATIENT SELF-REGISTRATION GATEWAY</span>
          </div>

          <div className="flex justify-center lg:justify-start">
            <Logo variant="full" size="xl" />
          </div>

          <p className="text-[#C084FC] text-xs sm:text-sm font-mono font-bold tracking-widest uppercase pt-2">
            Healthcare Intelligence & IT Platform
          </p>

          <p className="text-slate-300 text-xs sm:text-sm max-w-xl leading-relaxed">
            Create your confidential Patient Account to access SmartCare AI multi-disease risk evaluations, automated clinical wellness plans, and interactive health twin analytics.
          </p>
        </div>

        {/* 2D/2.5D Animated Data Flow Visualization */}
        <div className="w-full pt-4">
          <DataFlowVisualization />
        </div>
      </div>

      {/* RIGHT 45%: Patient Register Form Card */}
      <div className="lg:col-span-5 w-full">
        <HolographicHUDPanel 
          title="PATIENT REGISTRATION" 
          subtitle="CREATE PATIENT ACCOUNT"
          glowColor="purple"
          className="shadow-2xl"
        >
          <div className="space-y-4">
            
            {error && (
              <div className="p-3 rounded-xl bg-red-500/15 border border-red-500/40 text-red-300 text-xs flex items-center space-x-2 font-mono">
                <Shield className="w-4 h-4 text-red-400 flex-shrink-0" />
                <span>{error}</span>
              </div>
            )}

            {success && (
              <div className="p-3 rounded-xl bg-[#22C55E]/15 border border-[#22C55E]/40 text-emerald-300 text-xs flex items-center space-x-2 font-mono">
                <CheckCircle2 className="w-4 h-4 text-[#22C55E] flex-shrink-0" />
                <span>Patient account created successfully! Redirecting to Sign In...</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-3 font-mono text-xs">
              <div>
                <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px] tracking-wider">Full Name *</label>
                <input
                  type="text"
                  required
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl px-3.5 py-2 text-white focus:border-[#7C3AED] outline-none transition"
                  placeholder="e.g. Eleanor Vance"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px] tracking-wider">Username *</label>
                  <input
                    type="text"
                    required
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl px-3.5 py-2 text-white focus:border-[#7C3AED] outline-none transition"
                    placeholder="eleanor_vance"
                  />
                </div>
                <div>
                  <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px] tracking-wider">Email Address *</label>
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl px-3.5 py-2 text-white focus:border-[#7C3AED] outline-none transition"
                    placeholder="eleanor@example.com"
                  />
                </div>
              </div>

              <div>
                <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px] tracking-wider">Password *</label>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl px-3.5 py-2 text-white focus:border-[#7C3AED] outline-none transition"
                  placeholder="••••••••••••"
                />
              </div>

              <div className="grid grid-cols-3 gap-2">
                <div>
                  <label className="block text-slate-300 font-bold mb-1 uppercase text-[9px] tracking-wider">Phone</label>
                  <input
                    type="text"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl px-2.5 py-2 text-white focus:border-[#7C3AED] outline-none transition text-xs"
                    placeholder="+1-555-0199"
                  />
                </div>
                <div>
                  <label className="block text-slate-300 font-bold mb-1 uppercase text-[9px] tracking-wider">Date of Birth</label>
                  <input
                    type="date"
                    value={dateOfBirth}
                    onChange={(e) => setDateOfBirth(e.target.value)}
                    className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl px-2.5 py-2 text-white focus:border-[#7C3AED] outline-none transition text-xs"
                  />
                </div>
                <div>
                  <label className="block text-slate-300 font-bold mb-1 uppercase text-[9px] tracking-wider">Gender</label>
                  <select
                    value={gender}
                    onChange={(e) => setGender(e.target.value)}
                    className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl px-2.5 py-2 text-white focus:border-[#7C3AED] outline-none transition text-xs"
                  >
                    <option value="">Select</option>
                    <option value="Female">Female</option>
                    <option value="Male">Male</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
              </div>

              <div className="bg-[#140B2E] p-2.5 rounded-xl border border-[#241349] text-[10px] text-slate-400 flex items-center space-x-2">
                <UserCheck className="w-4 h-4 text-[#C084FC] flex-shrink-0" />
                <span>Notice: Clinician & Staff accounts are provisioned directly by System Administrators.</span>
              </div>

              <button
                type="submit"
                disabled={loading || success}
                className="w-full py-3 rounded-xl bg-gradient-to-r from-[#6D28D9] via-[#7C3AED] to-[#A855F7] hover:brightness-110 text-white font-extrabold text-xs uppercase tracking-wider transition shadow-lg shadow-[#7C3AED]/30 flex items-center justify-center space-x-2 mt-2 cursor-pointer"
              >
                {loading ? <span>REGISTERING PATIENT...</span> : (
                  <>
                    <span>REGISTER PATIENT ACCOUNT</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </form>

            <div className="text-center pt-2 text-xs text-slate-400 font-mono">
              Already registered?{' '}
              <button onClick={onSwitchToLogin} className="text-[#C084FC] font-bold hover:underline cursor-pointer">
                Sign In to SmartCare AI
              </button>
            </div>

          </div>
        </HolographicHUDPanel>
      </div>

    </div>
  );
}
