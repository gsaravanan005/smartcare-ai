import React, { useState } from 'react';
import { authAPI } from '../services/api';
import Logo from '../components/Logo';
import WorkspaceBackground from '../components/WorkspaceBackground';

export default function SingleLogin({ onLoginSuccess, onSwitchToRegister }) {
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (!identifier || !password) {
      setError('Please provide both username/email and password.');
      return;
    }

    setLoading(true);
    try {
      const response = await authAPI.login({
        username: identifier,
        password: password
      });

      const { access_token, role, user_id, username } = response.data;
      localStorage.setItem('smartcare_token', access_token);

      // Fetch complete user profile
      const userRes = await authAPI.getMe();
      if (onLoginSuccess) {
        onLoginSuccess(userRes.data);
      }
    } catch (err) {
      const errMsg = err.response?.data?.detail || 'Authentication failed. Please verify credentials.';
      setError(errMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen bg-transparent text-slate-100 flex flex-col font-sans selection:bg-[#7C3AED] selection:text-white overflow-hidden">
      <WorkspaceBackground />

      <main className="relative z-10 flex-1 flex flex-col justify-center items-center p-4">
        <div className="w-full max-w-md bg-[#0F0826]/90 border border-[#2A1A4E] backdrop-blur-xl rounded-2xl p-8 shadow-2xl shadow-purple-950/40">
        <div className="flex flex-col items-center text-center mb-8">
          <Logo variant="full" size="lg" />
          <p className="mt-2 text-xs uppercase tracking-widest font-mono text-[#C084FC]">
            Healthcare Intelligence & IT System
          </p>
          <div className="mt-4 px-3 py-1 rounded-full bg-[#1F103F] border border-[#3B1F75] text-[11px] font-mono text-purple-300">
            🔒 Secure Single Gateway Access
          </div>
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-xl bg-red-950/50 border border-red-500/30 text-red-300 text-xs flex items-start space-x-2">
            <span className="text-red-400 font-bold">⚠️</span>
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-xs font-mono text-slate-300 mb-2 uppercase tracking-wider">
              Email or Username
            </label>
            <input
              type="text"
              value={identifier}
              onChange={(e) => setIdentifier(e.target.value)}
              placeholder="e.g. patient@smartcare.ai or doctor@smartcare.ai"
              required
              className="w-full px-4 py-3 bg-[#150C33] border border-[#2A1A4E] rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-[#7C3AED] focus:ring-1 focus:ring-[#7C3AED] transition"
            />
          </div>

          <div>
            <label className="block text-xs font-mono text-slate-300 mb-2 uppercase tracking-wider">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••••••"
              required
              className="w-full px-4 py-3 bg-[#150C33] border border-[#2A1A4E] rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-[#7C3AED] focus:ring-1 focus:ring-[#7C3AED] transition"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 px-6 bg-gradient-to-r from-[#7C3AED] to-[#A855F7] hover:from-[#6D28D9] hover:to-[#9333EA] text-white text-sm font-semibold rounded-xl shadow-lg shadow-purple-900/30 flex items-center justify-center space-x-2 transition cursor-pointer disabled:opacity-50"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <span>LOGIN</span>
                <span>→</span>
              </>
            )}
          </button>
        </form>

        <div className="mt-6 pt-6 border-t border-[#1F103F] text-center space-y-4">
          <p className="text-[11px] font-mono text-slate-400 bg-[#140B2E] p-3 rounded-lg border border-[#231349]">
            💡 <strong className="text-purple-300">Notice:</strong> Your access is automatically determined from your account.
          </p>

          {onSwitchToRegister && (
            <div>
              <span className="text-xs text-slate-400">New Patient? </span>
              <button
                type="button"
                onClick={onSwitchToRegister}
                className="text-xs font-semibold text-[#C084FC] hover:text-white underline underline-offset-4 cursor-pointer transition"
              >
                Patient Self-Registration
              </button>
            </div>
          )}
        </div>
      </div>
    </main>
  </div>
);
}

