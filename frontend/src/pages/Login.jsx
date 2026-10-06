import React, { useState } from 'react';
import Logo from '../components/Logo';
import HolographicHUDPanel from '../components/HolographicHUDPanel';
import DataFlowVisualization from '../components/DataFlowVisualization';
import { authAPI } from '../services/api';
import { Shield, Lock, User, Eye, EyeOff, Sparkles, ArrowRight, ShieldCheck, UserCheck, Stethoscope, ShieldAlert, KeyRound, CheckCircle2 } from 'lucide-react';

export default function Login({ onLoginSuccess, onSwitchToRegister }) {
  const [selectedRole, setSelectedRole] = useState('patient'); // 'patient' | 'doctor' | 'admin'
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Forgot password modal state
  const [showForgotModal, setShowForgotModal] = useState(false);
  const [forgotEmail, setForgotEmail] = useState('');
  const [forgotSubmitted, setForgotSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await authAPI.login({ username, password });
      localStorage.setItem('smartcare_token', res.data.access_token);
      const userRes = await authAPI.getMe();
      const authenticatedUser = userRes.data;

      // Validate role authorization match
      const userRole = (authenticatedUser.role || 'patient').toLowerCase();
      const expectedRole = selectedRole === 'doctor' ? ['doctor', 'clinician'] : [selectedRole];
      
      if (!expectedRole.includes(userRole) && userRole !== 'admin') {
        // If user logged into wrong portal (and is not admin superuser)
        setError(`Account authenticated as '${userRole.toUpperCase()}', but you selected the ${selectedRole.toUpperCase()} Login tab. Please switch tabs.`);
        setLoading(false);
        return;
      }

      onLoginSuccess(authenticatedUser);
    } catch (err) {
      setError(err.response?.data?.detail || "Authentication failed. Verify ID/Email and Password.");
    } finally {
      setLoading(false);
    }
  };

  const handleForgotSubmit = (e) => {
    e.preventDefault();
    setForgotSubmitted(true);
  };

  const roleConfig = {
    patient: {
      title: 'Patient Login',
      badge: 'PATIENT PORTAL',
      idLabel: 'Patient ID / Email',
      idPlaceholder: 'patient@smartcare.ai or patient ID',
      icon: UserCheck,
      color: 'from-purple-600 to-indigo-600',
      tabBorder: 'border-[#8B5CF6]'
    },
    doctor: {
      title: 'Doctor Login',
      badge: 'CLINICIAN PORTAL',
      idLabel: 'Doctor ID / Professional Email',
      idPlaceholder: 'doctor@smartcare.ai or doctor ID',
      icon: Stethoscope,
      color: 'from-purple-600 to-pink-600',
      tabBorder: 'border-[#E879F9]'
    },
    admin: {
      title: 'Admin Login',
      badge: 'SYSTEM ADMIN PORTAL',
      idLabel: 'Admin ID / Email',
      idPlaceholder: 'admin@smartcare.ai or admin ID',
      icon: ShieldAlert,
      color: 'from-purple-700 to-red-600',
      tabBorder: 'border-[#EF4444]'
    }
  };

  const currentRoleCfg = roleConfig[selectedRole];

  return (
    <div className="w-full max-w-7xl mx-auto px-4 py-8 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center min-h-[85vh] z-10 relative">
      
      {/* LEFT 55%: BRANDING & SMARTCARE AI LOGO INTEGRATION */}
      <div className="lg:col-span-7 space-y-6 text-center lg:text-left">
        
        {/* Top Animated ECG Waveform */}
        <div className="w-full h-8 overflow-hidden opacity-50 mb-2">
          <svg className="w-full h-full stroke-[#C084FC] fill-none" viewBox="0 0 500 40">
            <path d="M 0 20 L 150 20 L 165 5 L 180 35 L 195 10 L 210 25 L 225 20 L 500 20" strokeWidth="2" strokeDasharray="300" strokeDashoffset="0" />
          </svg>
        </div>

        <div className="space-y-4">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-[#7C3AED]/20 border border-[#7C3AED]/40 text-[#C084FC] text-[10px] font-mono font-bold uppercase tracking-widest">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AUTHENTICATION & ACCESS GATEWAY</span>
          </div>

          {/* Prominent SmartCare AI Logo Header */}
          <div className="flex justify-center lg:justify-start">
            <Logo variant="full" size="xl" />
          </div>

          <p className="text-[#C084FC] text-xs sm:text-sm font-mono font-bold tracking-widest uppercase pt-2">
            AI + IT + Healthcare + Human-Centered Care
          </p>

          <p className="text-slate-300 text-xs sm:text-sm max-w-xl leading-relaxed">
            Multi-disease clinical risk intelligence platform integrating predictive analytics, explainable SHAP AI, personalized wellness plans, and clinical decision support for Diabetes, Cardiovascular, and Chronic Kidney Disease.
          </p>
        </div>

        {/* 2D Pipeline Data Flow Diagram */}
        <div className="w-full pt-4">
          <DataFlowVisualization />
        </div>
      </div>

      {/* RIGHT 45%: MULTI-ROLE LOGIN PANEL */}
      <div className="lg:col-span-5 w-full">
        
        {/* Role Selector Tabs (PATIENT / DOCTOR / ADMIN) */}
        <div className="grid grid-cols-3 gap-2 mb-4 p-1.5 rounded-2xl bg-[#0D0718] border border-[#2A1A4E]">
          <button
            type="button"
            onClick={() => { setSelectedRole('patient'); setError(null); }}
            className={`py-2.5 px-3 rounded-xl text-xs font-mono font-bold uppercase transition flex items-center justify-center space-x-1.5 cursor-pointer ${
              selectedRole === 'patient'
                ? 'bg-gradient-to-r from-[#6D28D9] to-[#7C3AED] text-white shadow-lg shadow-[#7C3AED]/30 border border-[#8B5CF6]'
                : 'text-slate-400 hover:text-white hover:bg-[#120A24]'
            }`}
          >
            <UserCheck className="w-3.5 h-3.5" />
            <span>Patient</span>
          </button>

          <button
            type="button"
            onClick={() => { setSelectedRole('doctor'); setError(null); }}
            className={`py-2.5 px-3 rounded-xl text-xs font-mono font-bold uppercase transition flex items-center justify-center space-x-1.5 cursor-pointer ${
              selectedRole === 'doctor'
                ? 'bg-gradient-to-r from-[#7C3AED] to-[#A855F7] text-white shadow-lg shadow-[#A855F7]/30 border border-[#C084FC]'
                : 'text-slate-400 hover:text-white hover:bg-[#120A24]'
            }`}
          >
            <Stethoscope className="w-3.5 h-3.5" />
            <span>Doctor</span>
          </button>

          <button
            type="button"
            onClick={() => { setSelectedRole('admin'); setError(null); }}
            className={`py-2.5 px-3 rounded-xl text-xs font-mono font-bold uppercase transition flex items-center justify-center space-x-1.5 cursor-pointer ${
              selectedRole === 'admin'
                ? 'bg-gradient-to-r from-[#6D28D9] to-[#EF4444] text-white shadow-lg shadow-[#EF4444]/30 border border-[#EF4444]'
                : 'text-slate-400 hover:text-white hover:bg-[#120A24]'
            }`}
          >
            <ShieldAlert className="w-3.5 h-3.5" />
            <span>Admin</span>
          </button>
        </div>

        {/* Login Form Panel */}
        <HolographicHUDPanel 
          title={currentRoleCfg.title.toUpperCase()} 
          subtitle={currentRoleCfg.badge}
          glowColor="purple"
          className="shadow-2xl"
        >
          <div className="space-y-5">
            
            <div className="flex items-center justify-between">
              <div>
                <div className="text-xl font-extrabold text-white">{currentRoleCfg.title}</div>
                <div className="text-xs text-[#C084FC] font-mono">Sign in to authorized workspace</div>
              </div>
              <div className="w-9 h-9 rounded-xl bg-[#2A1A4E] border border-[#7C3AED]/40 flex items-center justify-center text-[#C084FC]">
                <currentRoleCfg.icon className="w-5 h-5" />
              </div>
            </div>

            {error && (
              <div className="p-3.5 rounded-xl bg-red-500/15 border border-red-500/40 text-red-300 text-xs flex items-center space-x-2 font-mono">
                <Shield className="w-4 h-4 text-red-400 flex-shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4 text-xs font-mono">
              <div>
                <label className="block text-slate-300 font-bold mb-1.5 uppercase text-[10px] tracking-wider">
                  {currentRoleCfg.idLabel}
                </label>
                <div className="relative">
                  <User className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
                  <input
                    type="text"
                    required
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl pl-10 pr-4 py-2.5 text-white focus:border-[#7C3AED] outline-none transition"
                    placeholder={currentRoleCfg.idPlaceholder}
                  />
                </div>
              </div>

              <div>
                <label className="block text-slate-300 font-bold mb-1.5 uppercase text-[10px] tracking-wider">Password</label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
                  <input
                    type={showPassword ? "text" : "password"}
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl pl-10 pr-10 py-2.5 text-white focus:border-[#7C3AED] outline-none transition"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3.5 top-3.5 text-slate-400 hover:text-white"
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              <div className="flex items-center justify-between text-[11px] text-slate-400">
                <label className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    className="rounded bg-[#0D0718] border-[#2A1A4E] text-[#7C3AED] focus:ring-0"
                  />
                  <span>Remember Session</span>
                </label>
                <button 
                  type="button" 
                  onClick={() => { setShowForgotModal(true); setForgotSubmitted(false); }}
                  className="text-[#C084FC] hover:underline"
                >
                  Forgot Password?
                </button>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 rounded-xl bg-gradient-to-r from-[#6D28D9] via-[#7C3AED] to-[#A855F7] hover:brightness-110 text-white font-extrabold text-xs uppercase tracking-wider transition shadow-lg shadow-[#7C3AED]/30 flex items-center justify-center space-x-2 mt-2 cursor-pointer"
              >
                {loading ? <span>AUTHENTICATING {selectedRole.toUpperCase()}...</span> : (
                  <>
                    <span>SIGN IN AS {selectedRole.toUpperCase()}</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </form>

            {/* Public Registration link available ONLY for Patient/Doctor, restricted for Admin */}
            {selectedRole !== 'admin' ? (
              <div className="text-center pt-2 text-xs text-slate-400 font-mono">
                Don't have an account?{' '}
                <button onClick={onSwitchToRegister} className="text-[#C084FC] font-bold hover:underline">
                  Create {selectedRole === 'doctor' ? 'Doctor' : 'Patient'} Account
                </button>
              </div>
            ) : (
              <div className="text-center pt-2 text-[11px] text-slate-400 font-mono">
                Admin registration is restricted. Public sign-up is disabled.
              </div>
            )}

            <div className="p-3 rounded-xl bg-[#0D0718]/80 border border-[#2A1A4E] text-[10px] font-mono text-slate-400 text-center flex items-center justify-center space-x-1.5">
              <ShieldCheck className="w-3.5 h-3.5 text-[#22C55E]" />
              <span>ENCRYPTED ROLE-BASED ACCESS CONTROL (RBAC)</span>
            </div>

          </div>
        </HolographicHUDPanel>
      </div>

      {/* Forgot Password Modal */}
      {showForgotModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-md animate-in fade-in">
          <div className="w-full max-w-md bg-[#0D0718] border border-[#7C3AED]/50 rounded-2xl p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between border-b border-[#2A1A4E] pb-3">
              <div className="flex items-center space-x-2">
                <KeyRound className="w-5 h-5 text-[#C084FC]" />
                <h3 className="text-base font-extrabold text-white">Reset Password</h3>
              </div>
              <button 
                onClick={() => setShowForgotModal(false)}
                className="text-slate-400 hover:text-white font-mono text-sm"
              >
                ✕
              </button>
            </div>

            {!forgotSubmitted ? (
              <form onSubmit={handleForgotSubmit} className="space-y-4 text-xs font-mono">
                <p className="text-slate-300 leading-relaxed">
                  Enter your registered {selectedRole.toUpperCase()} email or ID. We will send password recovery instructions.
                </p>
                <div>
                  <label className="block text-slate-300 font-bold mb-1.5 uppercase text-[10px]">Email Address</label>
                  <input 
                    type="email"
                    required
                    value={forgotEmail}
                    onChange={(e) => setForgotEmail(e.target.value)}
                    placeholder="user@smartcare.ai"
                    className="w-full bg-[#120A24] border border-[#2A1A4E] rounded-xl px-4 py-2.5 text-white focus:border-[#7C3AED] outline-none"
                  />
                </div>
                <div className="flex items-center justify-end space-x-2 pt-2">
                  <button
                    type="button"
                    onClick={() => setShowForgotModal(false)}
                    className="px-4 py-2 rounded-xl bg-[#120A24] text-slate-300 hover:text-white"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 rounded-xl bg-[#7C3AED] hover:bg-[#8B5CF6] text-white font-bold"
                  >
                    Send Instructions
                  </button>
                </div>
              </form>
            ) : (
              <div className="space-y-4 text-center font-mono py-4">
                <CheckCircle2 className="w-12 h-12 text-[#22C55E] mx-auto" />
                <div className="text-sm font-bold text-white">Instructions Sent</div>
                <p className="text-xs text-slate-300">
                  Password reset details have been dispatched to <span className="text-[#C084FC]">{forgotEmail}</span> if registered in SmartCare AI.
                </p>
                <button
                  onClick={() => setShowForgotModal(false)}
                  className="w-full py-2.5 rounded-xl bg-[#7C3AED] text-white font-bold text-xs uppercase"
                >
                  Return to Login
                </button>
              </div>
            )}
          </div>
        </div>
      )}

    </div>
  );
}
