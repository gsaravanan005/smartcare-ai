import React, { useState, useEffect } from 'react';
import { adminAPI } from '../../services/api';
import { 
  AlertTriangle, ShieldAlert, Key, Lock, RefreshCw, CheckCircle2, 
  X, Eye, EyeOff, ShieldCheck, Flame, Database, Clock, Copy
} from 'lucide-react';

export default function SystemReset2FAModal({ isOpen, onClose, onSuccess }) {
  const [adminPassword, setAdminPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [twoFactorCode, setTwoFactorCode] = useState('');
  const [confirmPhrase, setConfirmPhrase] = useState('');

  const [requestingOTP, setRequestingOTP] = useState(false);
  const [otpInfo, setOtpInfo] = useState(null);
  const [countdown, setCountdown] = useState(0);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [resetComplete, setResetComplete] = useState(null);
  const [copied, setCopied] = useState(false);

  const REQUIRED_PHRASE = "DELETE ALL DATA AND RESET";

  // Countdown timer for 2FA OTP validity
  useEffect(() => {
    let timer;
    if (countdown > 0) {
      timer = setInterval(() => {
        setCountdown((prev) => Math.max(0, prev - 1));
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [countdown]);

  if (!isOpen) return null;

  const handleRequestOTP = async () => {
    setRequestingOTP(true);
    setError('');
    try {
      const res = await adminAPI.requestResetOTP();
      if (res.data) {
        setOtpInfo(res.data);
        setCountdown(res.data.expires_in_seconds || 600);
        // Auto-fill the 2FA code for immediate ease of testing/verification
        if (res.data.otp_code) {
          setTwoFactorCode(res.data.otp_code);
        }
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to generate 2FA security code.");
    } finally {
      setRequestingOTP(false);
    }
  };

  const handleCopyOTP = () => {
    if (otpInfo?.otp_code) {
      navigator.clipboard.writeText(otpInfo.otp_code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleExecuteReset = async (e) => {
    e.preventDefault();
    setError('');

    if (!adminPassword.trim()) {
      setError("Please enter your Administrator password.");
      return;
    }

    if (!twoFactorCode.trim()) {
      setError("Please enter the 6-digit Two-Factor Authentication (2FA) code.");
      return;
    }

    if (confirmPhrase.trim().toUpperCase() !== REQUIRED_PHRASE) {
      setError(`Confirmation phrase mismatch. Please type exactly: "${REQUIRED_PHRASE}"`);
      return;
    }

    setLoading(true);
    try {
      const payload = {
        admin_password: adminPassword.trim(),
        two_factor_code: twoFactorCode.trim(),
        confirm_phrase: confirmPhrase.trim()
      };

      const res = await adminAPI.systemFactoryReset(payload);
      setResetComplete(res.data);

      if (onSuccess) {
        onSuccess(res.data);
      }

      // Auto reload after 4 seconds so clean baseline is mounted
      setTimeout(() => {
        window.location.reload();
      }, 4000);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "System Factory Reset failed.");
    } finally {
      setLoading(false);
    }
  };

  const isFormValid = 
    adminPassword.trim().length > 0 && 
    twoFactorCode.trim().length >= 6 && 
    confirmPhrase.trim().toUpperCase() === REQUIRED_PHRASE;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md overflow-y-auto animate-in fade-in duration-200">
      <div className="relative w-full max-w-2xl bg-[#0E061A] border-2 border-red-500/70 rounded-3xl shadow-2xl shadow-red-950/80 p-6 md:p-8 space-y-6 font-mono text-xs my-8 max-h-[92vh] overflow-y-auto">
        
        {/* Modal Top Header */}
        <div className="flex items-start justify-between border-b border-red-500/30 pb-4">
          <div className="flex items-center space-x-3">
            <div className="p-3 rounded-2xl bg-red-500/20 border border-red-500/40 text-red-400">
              <Flame className="w-6 h-6 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="px-2.5 py-0.5 rounded-full bg-red-500/20 text-red-300 font-bold border border-red-500/40 text-[10px] uppercase">
                  Admin Only • 2FA Protected
                </span>
                <span className="text-[10px] text-amber-400 font-bold">IRREVERSIBLE ACTION</span>
              </div>
              <h2 className="text-xl font-extrabold text-white font-sans mt-1">
                System Factory Reset & Complete Data Wipe
              </h2>
            </div>
          </div>
          
          {!loading && !resetComplete && (
            <button
              type="button"
              onClick={onClose}
              className="p-2 rounded-xl bg-[#1A0F33] hover:bg-red-500/20 text-slate-400 hover:text-white transition cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* Success Completion Screen */}
        {resetComplete ? (
          <div className="p-6 rounded-2xl bg-emerald-500/10 border border-emerald-500/40 text-center space-y-4 animate-in zoom-in-95">
            <div className="w-16 h-16 rounded-full bg-emerald-500/20 border border-emerald-500/40 text-emerald-400 flex items-center justify-center mx-auto shadow-lg shadow-emerald-500/20">
              <CheckCircle2 className="w-8 h-8" />
            </div>
            <div className="space-y-1">
              <h3 className="text-lg font-extrabold text-white font-sans">
                SmartCare AI Reset Successfully Completed
              </h3>
              <p className="text-emerald-300 text-xs font-sans">
                All platform records have been securely purged and re-seeded with pristine default accounts.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-[#080214] border border-[#2A1A4E] text-left space-y-2">
              <div className="text-[11px] font-bold text-slate-300 uppercase">Reseeded Baseline Accounts:</div>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-[10px]">
                <div className="p-2 rounded bg-[#120A24] border border-[#3B206B]">
                  <span className="text-red-400 font-bold block">ADMIN</span>
                  <span className="text-white">admin@smartcare.ai</span>
                  <span className="text-slate-400 block mt-0.5">pwd: admin123</span>
                </div>
                <div className="p-2 rounded bg-[#120A24] border border-[#3B206B]">
                  <span className="text-purple-400 font-bold block">DOCTOR</span>
                  <span className="text-white">doctor@smartcare.ai</span>
                  <span className="text-slate-400 block mt-0.5">pwd: doctor123</span>
                </div>
                <div className="p-2 rounded bg-[#120A24] border border-[#3B206B]">
                  <span className="text-teal-400 font-bold block">PATIENT</span>
                  <span className="text-white">patient@smartcare.ai</span>
                  <span className="text-slate-400 block mt-0.5">pwd: patient123</span>
                </div>
              </div>
            </div>

            <div className="flex items-center justify-center space-x-2 text-slate-400 text-[11px] pt-2">
              <RefreshCw className="w-4 h-4 animate-spin text-emerald-400" />
              <span>Reloading platform workspace in 3 seconds...</span>
            </div>
          </div>
        ) : (
          /* Reset Form */
          <form onSubmit={handleExecuteReset} className="space-y-5">
            
            {/* Warning Callout Box */}
            <div className="p-4 rounded-2xl bg-red-950/40 border border-red-500/50 space-y-2 text-red-200">
              <div className="flex items-center space-x-2 font-bold text-red-300 text-xs font-sans">
                <AlertTriangle className="w-4 h-4 text-red-400 shrink-0" />
                <span>WARNING: This action will permanently erase all data in SmartCare AI:</span>
              </div>
              <ul className="list-disc list-inside space-y-1 text-[11px] text-red-300/90 pl-1">
                <li>All registered patient accounts, clinical histories, and vital submissions</li>
                <li>All diabetes, cardiovascular, and CKD machine learning risk predictions</li>
                <li>All SHAP explainability matrices and personalized wellness plans</li>
                <li>All clinician feedback, doctor-patient assignments, and notification queues</li>
                <li>All system audit trails (re-initialized with pristine genesis log)</li>
              </ul>
            </div>

            {error && (
              <div className="p-3.5 rounded-xl bg-red-500/20 border border-red-500/50 text-red-300 text-xs font-bold flex items-center space-x-2 animate-in fade-in">
                <ShieldAlert className="w-4 h-4 text-red-400 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            {/* STEP 1: Admin Password */}
            <div className="space-y-1.5 p-4 rounded-2xl bg-[#120A24] border border-[#2A1A4E]">
              <div className="flex items-center justify-between">
                <label className="text-[11px] font-bold text-white uppercase flex items-center space-x-1.5">
                  <span className="w-5 h-5 rounded-full bg-red-500/30 border border-red-500/50 text-red-300 flex items-center justify-center text-[10px]">1</span>
                  <span>Administrator Password Verification</span>
                </label>
                <span className="text-[10px] text-slate-400">Required</span>
              </div>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  value={adminPassword}
                  onChange={(e) => setAdminPassword(e.target.value)}
                  placeholder="Enter your Administrator password (e.g. admin123)"
                  className="w-full bg-[#080214] border border-[#3B206B] rounded-xl px-3.5 py-2.5 text-xs text-white outline-none focus:border-red-500 pr-10"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-2.5 text-slate-400 hover:text-white cursor-pointer"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            {/* STEP 2: Two-Factor Authentication (2FA) Code */}
            <div className="space-y-3 p-4 rounded-2xl bg-[#120A24] border border-[#2A1A4E]">
              <div className="flex items-center justify-between">
                <label className="text-[11px] font-bold text-white uppercase flex items-center space-x-1.5">
                  <span className="w-5 h-5 rounded-full bg-red-500/30 border border-red-500/50 text-red-300 flex items-center justify-center text-[10px]">2</span>
                  <span>Two-Factor Authentication (2FA) Security OTP</span>
                </label>
                <button
                  type="button"
                  onClick={handleRequestOTP}
                  disabled={requestingOTP}
                  className="px-3 py-1 rounded-lg bg-red-600/30 hover:bg-red-600/50 border border-red-500/50 text-red-300 font-bold text-[10px] uppercase transition cursor-pointer flex items-center space-x-1 disabled:opacity-50"
                >
                  <RefreshCw className={`w-3 h-3 ${requestingOTP ? 'animate-spin' : ''}`} />
                  <span>{otpInfo ? 'Regenerate 2FA Code' : 'Generate 2FA Code'}</span>
                </button>
              </div>

              {otpInfo && (
                <div className="p-3 rounded-xl bg-purple-950/40 border border-purple-500/40 flex items-center justify-between animate-in fade-in">
                  <div className="flex items-center space-x-2.5">
                    <ShieldCheck className="w-4 h-4 text-purple-400 shrink-0" />
                    <div>
                      <div className="text-slate-300 text-[10px]">Active 2FA OTP Code:</div>
                      <div className="text-sm font-extrabold text-white tracking-widest font-mono">
                        {otpInfo.otp_code}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center space-x-2">
                    <div className="text-right text-[10px] text-amber-400 font-mono">
                      <Clock className="w-3 h-3 inline mr-1" />
                      <span>{Math.floor(countdown / 60)}:{(countdown % 60).toString().padStart(2, '0')}</span>
                    </div>
                    <button
                      type="button"
                      onClick={handleCopyOTP}
                      className="p-1.5 rounded-lg bg-purple-600/30 hover:bg-purple-600/50 text-purple-300 transition cursor-pointer"
                      title="Copy OTP"
                    >
                      {copied ? <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                    </button>
                  </div>
                </div>
              )}

              <div>
                <input
                  type="text"
                  value={twoFactorCode}
                  onChange={(e) => setTwoFactorCode(e.target.value)}
                  placeholder="Enter 6-digit 2FA code or Master Key (e.g. SMARTCARE-2026-RESET)"
                  className="w-full bg-[#080214] border border-[#3B206B] rounded-xl px-3.5 py-2.5 text-xs text-white outline-none focus:border-red-500 tracking-widest uppercase font-mono"
                />
                <span className="text-[10px] text-slate-500 mt-1 block">
                  Tip: Master Emergency Key <strong className="text-slate-400">SMARTCARE-2026-RESET</strong> is accepted.
                </span>
              </div>
            </div>

            {/* STEP 3: Explicit Confirmation Phrase */}
            <div className="space-y-1.5 p-4 rounded-2xl bg-[#120A24] border border-[#2A1A4E]">
              <div className="flex items-center justify-between">
                <label className="text-[11px] font-bold text-white uppercase flex items-center space-x-1.5">
                  <span className="w-5 h-5 rounded-full bg-red-500/30 border border-red-500/50 text-red-300 flex items-center justify-center text-[10px]">3</span>
                  <span>Type Confirmation Phrase</span>
                </label>
                <span className="text-[10px] text-red-400 font-bold font-mono select-all">
                  "{REQUIRED_PHRASE}"
                </span>
              </div>
              <input
                type="text"
                value={confirmPhrase}
                onChange={(e) => setConfirmPhrase(e.target.value)}
                placeholder={`Type "${REQUIRED_PHRASE}" to confirm`}
                className={`w-full bg-[#080214] border rounded-xl px-3.5 py-2.5 text-xs text-white outline-none font-mono transition ${
                  confirmPhrase.trim().toUpperCase() === REQUIRED_PHRASE
                    ? 'border-emerald-500 text-emerald-300'
                    : 'border-[#3B206B] focus:border-red-500'
                }`}
              />
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={onClose}
                disabled={loading}
                className="w-full sm:w-auto px-5 py-2.5 rounded-xl bg-[#1A0F33] hover:bg-[#2A1A4E] text-slate-300 font-bold text-xs uppercase tracking-wider transition cursor-pointer disabled:opacity-50"
              >
                Cancel
              </button>

              <button
                type="submit"
                disabled={!isFormValid || loading}
                className={`w-full sm:w-auto px-6 py-3 rounded-xl font-bold text-xs uppercase tracking-wider transition flex items-center justify-center space-x-2 shadow-xl ${
                  isFormValid && !loading
                    ? 'bg-gradient-to-r from-red-600 via-rose-600 to-red-700 hover:brightness-110 text-white shadow-red-600/30 ring-2 ring-red-500/50 cursor-pointer animate-pulse'
                    : 'bg-red-950/40 text-slate-500 border border-red-900/40 cursor-not-allowed'
                }`}
              >
                {loading ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    <span>Executing 2FA Factory Reset...</span>
                  </>
                ) : (
                  <>
                    <Flame className="w-4 h-4 text-amber-300" />
                    <span>PERMANENTLY WIPE & FACTORY RESET</span>
                  </>
                )}
              </button>
            </div>

          </form>
        )}

      </div>
    </div>
  );
}
