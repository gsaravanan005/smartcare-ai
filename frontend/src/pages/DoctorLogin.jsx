import React, { useState } from 'react';
import Logo from '../components/Logo';
import HolographicHUDPanel from '../components/HolographicHUDPanel';
import { authAPI } from '../services/api';
import { Stethoscope, User, Lock, Eye, EyeOff, Shield, ArrowRight, ShieldCheck, KeyRound, CheckCircle2, ArrowLeft } from 'lucide-react';

export default function DoctorLogin({ onLoginSuccess, onBackToRoles, onSwitchToRegister }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Forgot password modal
  const [showForgotModal, setShowForgotModal] = useState(false);
  const [forgotEmail, setForgotEmail] = useState('');
  const [forgotSubmitted, setForgotSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await authAPI.login({ username, password, target_role: 'doctor' });
      localStorage.setItem('smartcare_token', res.data.access_token);
      const userRes = await authAPI.getMe();
      const authenticatedUser = userRes.data;

      // Ensure user role is doctor/clinician/admin
      const userRole = (authenticatedUser.role || 'patient').toLowerCase();
      if (!['doctor', 'clinician', 'admin', 'super_admin'].includes(userRole)) {
        setError("You are not authorized to access this portal.");
        setLoading(false);
        return;
      }

      onLoginSuccess(authenticatedUser);
    } catch (err) {
      setError(err.response?.data?.detail || "Invalid email/ID or password.");
    } finally {
      setLoading(false);
    }
  };

  const handleForgotSubmit = async (e) => {
    e.preventDefault();
    try {
      await authAPI.forgotPassword(forgotEmail);
    } catch (err) {
      // Intentionally swallow
    }
    setForgotSubmitted(true);
  };

  return (
    <div className="w-full max-w-md mx-auto py-8 px-4 z-10 relative">
      
      {/* Back to Role Selection */}
      <button 
        type="button"
        onClick={onBackToRoles}
        className="mb-6 inline-flex items-center space-x-2 text-xs font-mono text-[#C084FC] hover:text-white transition cursor-pointer"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Role Selection</span>
      </button>

      <HolographicHUDPanel 
        title="SMARTCARE AI — DOCTOR PORTAL" 
        subtitle="CLINICIAN ACCESS"
        glowColor="purple"
        className="shadow-2xl"
      >
        <div className="space-y-5">
          
          <div className="flex items-center justify-between">
            <div>
              <div className="text-xl font-extrabold text-white">Doctor Portal</div>
              <div className="text-xs text-[#C084FC] font-mono">Sign in to clinician decision support</div>
            </div>
            <div className="w-10 h-10 rounded-2xl bg-[#2A1A4E] border border-[#A855F7]/40 flex items-center justify-center text-[#C084FC]">
              <Stethoscope className="w-5 h-5" />
            </div>
          </div>

          {/* Logo */}
          <div className="flex justify-center py-1">
            <Logo variant="full" size="md" />
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
                Doctor ID / Professional Email
              </label>
              <div className="relative">
                <User className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
                <input
                  type="text"
                  required
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl pl-10 pr-4 py-2.5 text-white focus:border-[#A855F7] outline-none transition"
                  placeholder="doctor@smartcare.ai or Doctor ID"
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
                  className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl pl-10 pr-10 py-2.5 text-white focus:border-[#A855F7] outline-none transition"
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

            <div className="flex items-center justify-end text-[11px] text-slate-400">
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
              className="w-full py-3 rounded-xl bg-gradient-to-r from-[#7C3AED] via-[#A855F7] to-[#C084FC] hover:brightness-110 text-white font-extrabold text-xs uppercase tracking-wider transition shadow-lg shadow-[#A855F7]/30 flex items-center justify-center space-x-2 cursor-pointer"
            >
              {loading ? <span>AUTHENTICATING DOCTOR...</span> : (
                <>
                  <span>LOGIN AS DOCTOR</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          {onSwitchToRegister && (
            <div className="text-center pt-2 text-xs text-slate-400 font-mono">
              New Clinician?{' '}
              <button onClick={onSwitchToRegister} className="text-[#C084FC] font-bold hover:underline">
                Apply for Doctor Account
              </button>
            </div>
          )}

          <div className="p-3 rounded-xl bg-[#0D0718]/80 border border-[#2A1A4E] text-[10px] font-mono text-slate-400 text-center flex items-center justify-center space-x-1.5">
            <ShieldCheck className="w-3.5 h-3.5 text-[#22C55E]" />
            <span>CLINICIAN DECISION SUPPORT (VERIFIED DOCTORS ONLY)</span>
          </div>

        </div>
      </HolographicHUDPanel>

      {/* Forgot Password Modal */}
      {showForgotModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-md animate-in fade-in">
          <div className="w-full max-w-md bg-[#0D0718] border border-[#A855F7]/50 rounded-2xl p-6 space-y-4 shadow-2xl">
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
                  Enter your registered Doctor ID or Professional Email address.
                </p>
                <div>
                  <label className="block text-slate-300 font-bold mb-1.5 uppercase text-[10px]">Professional Email or Doctor ID</label>
                  <input 
                    type="text"
                    required
                    value={forgotEmail}
                    onChange={(e) => setForgotEmail(e.target.value)}
                    placeholder="doctor@smartcare.ai"
                    className="w-full bg-[#120A24] border border-[#2A1A4E] rounded-xl px-4 py-2.5 text-white focus:border-[#A855F7] outline-none"
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
                    className="px-4 py-2 rounded-xl bg-[#A855F7] hover:bg-[#C084FC] text-white font-bold"
                  >
                    Send Reset Instructions
                  </button>
                </div>
              </form>
            ) : (
              <div className="space-y-4 text-center font-mono py-4">
                <CheckCircle2 className="w-12 h-12 text-[#22C55E] mx-auto" />
                <div className="text-sm font-bold text-white">Instructions Sent</div>
                <p className="text-xs text-slate-300">
                  If an account with that email or ID exists, password reset instructions have been sent.
                </p>
                <button
                  onClick={() => setShowForgotModal(false)}
                  className="w-full py-2.5 rounded-xl bg-[#A855F7] text-white font-bold text-xs uppercase"
                >
                  Return to Doctor Login
                </button>
              </div>
            )}
          </div>
        </div>
      )}

    </div>
  );
}
