import React, { useState } from 'react';
import Logo from '../components/Logo';
import HolographicHUDPanel from '../components/HolographicHUDPanel';
import DataFlowVisualization from '../components/DataFlowVisualization';
import { authAPI } from '../services/api';
import { Shield, Sparkles, ArrowRight, CheckCircle2, UserCheck, Stethoscope } from 'lucide-react';

export default function Register({ onRegisterSuccess, onSwitchToLogin }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [role, setRole] = useState('patient');
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
        role
      });
      setSuccess(true);
      setTimeout(() => {
        onRegisterSuccess();
      }, 1500);
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed. Verify details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-7xl mx-auto px-4 py-8 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center min-h-[85vh] z-10 relative">
      
      {/* LEFT 55%: Branding + Logo + AI Healthcare Visualization */}
      <div className="lg:col-span-7 space-y-6 text-center lg:text-left">
        <div className="space-y-4">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-[#7C3AED]/20 border border-[#7C3AED]/40 text-[#C084FC] text-[10px] font-mono font-bold uppercase tracking-widest">
            <Sparkles className="w-3.5 h-3.5" />
            <span>ACCOUNT PROVISIONING GATEWAY</span>
          </div>

          <div className="flex justify-center lg:justify-start">
            <Logo variant="full" size="xl" />
          </div>

          <p className="text-[#C084FC] text-xs sm:text-sm font-mono font-bold tracking-widest uppercase pt-2">
            AI + IT + Healthcare + Human Care
          </p>

          <p className="text-slate-300 text-xs sm:text-sm max-w-xl leading-relaxed">
            Register your Patient or Doctor account to access SmartCare AI clinical risk intelligence, personalized wellness plans, and SHAP explainability.
          </p>
        </div>

        {/* 2D/2.5D Animated Data Flow Visualization */}
        <div className="w-full pt-4">
          <DataFlowVisualization />
        </div>
      </div>

      {/* RIGHT 45%: Register Card Interface */}
      <div className="lg:col-span-5 w-full">
        <HolographicHUDPanel 
          title="CREATE ACCOUNT" 
          subtitle="PATIENT & DOCTOR REGISTRATION"
          glowColor="purple"
          className="shadow-2xl"
        >
          <div className="space-y-4">
            
            {error && (
              <div className="p-3.5 rounded-xl bg-red-500/15 border border-red-500/40 text-red-300 text-xs flex items-center space-x-2 font-mono">
                <Shield className="w-4 h-4 text-red-400 flex-shrink-0" />
                <span>{error}</span>
              </div>
            )}

            {success && (
              <div className="p-3.5 rounded-xl bg-[#22C55E]/15 border border-[#22C55E]/40 text-emerald-300 text-xs flex items-center space-x-2 font-mono">
                <CheckCircle2 className="w-4 h-4 text-[#22C55E] flex-shrink-0" />
                <span>Account provisioned successfully! Redirecting to Sign In...</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-3 font-mono text-xs">
              <div>
                <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px] tracking-wider">Full Name</label>
                <input
                  type="text"
                  required
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl px-3.5 py-2.5 text-white focus:border-[#7C3AED] outline-none transition"
                  placeholder="Dr. Jane Doe or Patient Name"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px] tracking-wider">Username / ID</label>
                <input
                  type="text"
                  required
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl px-3.5 py-2.5 text-white focus:border-[#7C3AED] outline-none transition"
                  placeholder="janedoe"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px] tracking-wider">Email Address</label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl px-3.5 py-2.5 text-white focus:border-[#7C3AED] outline-none transition"
                  placeholder="jane@smartcare.ai"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px] tracking-wider">Password</label>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl px-3.5 py-2.5 text-white focus:border-[#7C3AED] outline-none transition"
                  placeholder="••••••••"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px] tracking-wider">Account Role</label>
                <div className="grid grid-cols-2 gap-2 pt-1">
                  <button
                    type="button"
                    onClick={() => setRole('patient')}
                    className={`py-2 px-3 rounded-xl border text-xs font-bold uppercase transition flex items-center justify-center space-x-1.5 ${
                      role === 'patient'
                        ? 'bg-[#7C3AED] border-[#8B5CF6] text-white'
                        : 'bg-[#0D0718] border-[#2A1A4E] text-slate-400 hover:text-white'
                    }`}
                  >
                    <UserCheck className="w-3.5 h-3.5" />
                    <span>Patient</span>
                  </button>

                  <button
                    type="button"
                    onClick={() => setRole('doctor')}
                    className={`py-2 px-3 rounded-xl border text-xs font-bold uppercase transition flex items-center justify-center space-x-1.5 ${
                      role === 'doctor'
                        ? 'bg-[#A855F7] border-[#C084FC] text-white'
                        : 'bg-[#0D0718] border-[#2A1A4E] text-slate-400 hover:text-white'
                    }`}
                  >
                    <Stethoscope className="w-3.5 h-3.5" />
                    <span>Doctor</span>
                  </button>
                </div>
              </div>

              <button
                type="submit"
                disabled={loading || success}
                className="w-full py-3 rounded-xl bg-gradient-to-r from-[#6D28D9] via-[#7C3AED] to-[#A855F7] hover:brightness-110 text-white font-extrabold text-xs uppercase tracking-wider transition shadow-lg shadow-[#7C3AED]/30 flex items-center justify-center space-x-2 mt-2 cursor-pointer"
              >
                {loading ? <span>PROVISIONING ACCOUNT...</span> : (
                  <>
                    <span>CREATE {role.toUpperCase()} ACCOUNT</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </form>

            <div className="text-center pt-2 text-xs text-slate-400 font-mono">
              Already have an account?{' '}
              <button onClick={onSwitchToLogin} className="text-[#C084FC] font-bold hover:underline">
                Sign In
              </button>
            </div>

          </div>
        </HolographicHUDPanel>
      </div>

    </div>
  );
}
