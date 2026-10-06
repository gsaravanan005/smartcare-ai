import React, { useState } from 'react';
import Logo from './Logo';
import { Activity, Bell, Search, ShieldCheck, LogOut, User, ChevronDown, Stethoscope, ShieldAlert, UserCheck } from 'lucide-react';

export default function GlobalHeader({ user, activeTab, setActiveTab, onLogout }) {
  const [profileOpen, setProfileOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const role = (user?.role || 'patient').toLowerCase();

  const roleBadge = {
    patient: { label: 'PATIENT', bg: 'bg-[#7C3AED]/20 text-[#C084FC] border-[#7C3AED]/40', icon: UserCheck },
    doctor: { label: 'DOCTOR', bg: 'bg-[#A855F7]/20 text-[#E879F9] border-[#A855F7]/40', icon: Stethoscope },
    clinician: { label: 'DOCTOR', bg: 'bg-[#A855F7]/20 text-[#E879F9] border-[#A855F7]/40', icon: Stethoscope },
    admin: { label: 'ADMIN', bg: 'bg-[#EF4444]/20 text-[#EF4444] border-[#EF4444]/40', icon: ShieldAlert }
  }[role] || { label: 'PATIENT', bg: 'bg-[#7C3AED]/20 text-[#C084FC] border-[#7C3AED]/40', icon: UserCheck };

  const RoleIcon = roleBadge.icon;

  return (
    <header className="w-full bg-[#0D0718]/90 backdrop-blur-xl border-b border-[#2A1A4E] px-4 md:px-6 sticky top-0 z-50 h-[56px] flex items-center justify-between shadow-lg flex-shrink-0 font-sans select-none">
      
      {/* LEFT: Official SmartCare AI Logo Integration */}
      <div 
        onClick={() => {
          if (role === 'doctor' || role === 'clinician') {
            setActiveTab('clinician_dashboard');
          } else {
            setActiveTab('dashboard');
          }
        }}
        className="flex items-center cursor-pointer group flex-shrink-0"
      >
        <Logo variant="full" size="md" />
      </div>

      {/* CENTER: Minimal Global Search Input */}
      <div className="flex-1 max-w-md mx-6 hidden sm:block">
        <div className="relative">
          <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search patients, vitals, SHAP analysis, models..."
            className="w-full bg-[#080512] border border-[#2A1A4E] rounded-xl pl-9 pr-3 py-1.5 text-xs text-white placeholder-slate-500 focus:border-[#7C3AED] outline-none transition font-mono"
          />
        </div>
      </div>

      {/* RIGHT: User Role Badge, Notifications & Profile Menu */}
      <div className="flex items-center space-x-3 flex-shrink-0">
        
        {/* User Role Badge */}
        <div className={`hidden md:flex items-center space-x-1.5 px-2.5 py-1 rounded-xl text-[10px] font-mono font-bold border ${roleBadge.bg}`}>
          <RoleIcon className="w-3.5 h-3.5" />
          <span>{roleBadge.label}</span>
        </div>

        {/* Live System Status Indicator */}
        <div className="hidden xl:flex items-center space-x-1.5 bg-[#080512] border border-[#2A1A4E] px-2.5 py-1 rounded-xl text-[10px] font-mono text-slate-300">
          <span className="w-1.5 h-1.5 rounded-full bg-[#22C55E] animate-ping" />
          <span className="text-[#22C55E] font-bold uppercase">AI CORE ACTIVE</span>
        </div>

        {/* Notifications Bell */}
        <button 
          onClick={() => {
            if (role === 'patient') setActiveTab('risk_history');
            else if (role === 'admin' || role === 'doctor' || role === 'clinician') setActiveTab('clinician_dashboard');
          }}
          className="relative p-2 rounded-xl bg-[#080512] border border-[#2A1A4E] text-slate-300 hover:text-white hover:border-[#7C3AED] transition cursor-pointer"
          title="Notifications & Clinical Alerts"
        >
          <Bell className="w-4 h-4 text-[#C084FC]" />
          <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-[#E879F9] animate-ping" />
        </button>

        {/* Profile Menu Dropdown */}
        <div className="relative">
          <button
            onClick={() => setProfileOpen(!profileOpen)}
            className="flex items-center space-x-2.5 px-2.5 py-1.5 rounded-xl bg-[#080512] border border-[#2A1A4E] hover:border-[#7C3AED] transition cursor-pointer"
          >
            <div className="w-6 h-6 rounded-full bg-gradient-to-tr from-[#6D28D9] to-[#C084FC] text-white font-extrabold text-xs flex items-center justify-center shadow-md">
              {user?.full_name ? user.full_name.charAt(0) : 'U'}
            </div>

            <div className="text-left hidden sm:block">
              <div className="text-xs font-extrabold text-white leading-tight">
                {user?.full_name || user?.username || 'User'}
              </div>
            </div>

            <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
          </button>

          {profileOpen && (
            <div className="absolute right-0 mt-2 w-52 rounded-xl bg-[#0D0718] border border-[#2A1A4E] p-2 space-y-1 shadow-2xl z-50 font-mono text-xs">
              <div className="px-3 py-2 border-b border-[#2A1A4E]">
                <div className="font-bold text-white truncate">{user?.full_name || user?.username}</div>
                <div className="text-[10px] text-[#C084FC] truncate">{user?.email}</div>
                <div className="text-[9px] text-slate-400 mt-1 uppercase font-bold">Role: {role}</div>
              </div>

              <button
                onClick={() => { setActiveTab('profile'); setProfileOpen(false); }}
                className="w-full text-left px-3 py-2 rounded-lg text-xs font-semibold text-slate-300 hover:bg-[#120A24] hover:text-[#C084FC] transition flex items-center space-x-2 cursor-pointer"
              >
                <User className="w-4 h-4" />
                <span>My Profile</span>
              </button>

              <button
                onClick={onLogout}
                className="w-full text-left px-3 py-2 rounded-lg text-xs font-semibold text-red-400 hover:bg-red-500/10 transition flex items-center space-x-2 cursor-pointer"
              >
                <LogOut className="w-4 h-4" />
                <span>Sign Out</span>
              </button>
            </div>
          )}
        </div>

      </div>

    </header>
  );
}
