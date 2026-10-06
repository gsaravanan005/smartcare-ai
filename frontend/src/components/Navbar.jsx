import React, { useState } from 'react';
import { Activity, HelpCircle, User, BarChart2, Database, GitMerge, Bell, LogOut, Sparkles, ChevronDown } from 'lucide-react';

export default function Navbar({ user, activeTab, setActiveTab, onLogout }) {
  const [profileOpen, setProfileOpen] = useState(false);

  const TOP_TABS = [
    { id: 'risk', label: 'Risk Assessment', icon: Activity },
    { id: 'explain', label: 'Why This Risk? (SHAP)', icon: HelpCircle },
    { id: 'form', label: 'Health Form', icon: User },
    { id: 'models', label: 'Model Benchmark', icon: BarChart2 },
    { id: 'data_quality', label: 'Data Quality', icon: Database },
    { id: 'pipeline', label: 'Pipeline Runner', icon: GitMerge }
  ];

  return (
    <header className="sticky top-0 z-40 glass-panel border-b border-slate-800/80 px-4 lg:px-6 py-3">
      <div className="flex items-center justify-between">
        
        {/* Left: Brand Identity */}
        <div 
          onClick={() => setActiveTab('dashboard')}
          className="flex items-center space-x-3 cursor-pointer group"
        >
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-sky-500 to-teal-400 p-0.5 shadow-lg shadow-sky-500/20 group-hover:scale-105 transition">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <Activity className="w-5 h-5 text-sky-400" />
            </div>
          </div>

          <div>
            <div className="font-extrabold text-white text-base tracking-tight flex items-center space-x-1.5">
              <span>SMARTCARE AI</span>
            </div>
            <div className="text-[9px] text-slate-400 font-mono tracking-widest uppercase">
              AI HEALTH INTELLIGENCE PLATFORM
            </div>
          </div>
        </div>

        {/* Center: Top Navigation Pills Bar */}
        <nav className="hidden xl:flex items-center space-x-1.5 bg-slate-950/60 p-1.5 rounded-2xl border border-slate-800/80">
          {TOP_TABS.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;

            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all duration-200 ${
                  isActive
                    ? 'bg-sky-500/20 text-sky-300 border border-sky-500/40 shadow-md shadow-sky-500/10'
                    : 'text-slate-400 hover:text-white hover:bg-slate-900/60'
                }`}
              >
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Right: Administrator Profile & Notifications */}
        <div className="flex items-center space-x-3">
          
          {/* Notification Indicator */}
          <button className="relative p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-white transition">
            <Bell className="w-4 h-4" />
            <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-sky-400 animate-ping" />
            <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-sky-400" />
          </button>

          {/* Profile Dropdown Badge */}
          <div className="relative">
            <button
              onClick={() => setProfileOpen(!profileOpen)}
              className="flex items-center space-x-2.5 px-3 py-1.5 rounded-2xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition"
            >
              <div className="w-7 h-7 rounded-full bg-gradient-to-tr from-sky-400 to-teal-400 text-slate-950 font-extrabold text-xs flex items-center justify-center">
                {user?.full_name ? user.full_name.charAt(0) : 'A'}
              </div>

              <div className="text-left hidden sm:block">
                <div className="text-xs font-extrabold text-white leading-tight">
                  {user?.full_name || 'Dr. Administrator'}
                </div>
                <div className="text-[9px] text-teal-400 font-mono font-bold uppercase flex items-center space-x-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-teal-400" />
                  <span>{user?.role || 'ADMIN'}</span>
                </div>
              </div>

              <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
            </button>

            {profileOpen && (
              <div className="absolute right-0 mt-2 w-48 rounded-2xl glass-panel border border-slate-800 p-2 space-y-1 shadow-2xl z-50">
                <div className="px-3 py-2 border-b border-slate-800 text-xs">
                  <div className="font-bold text-white">{user?.username || 'admin'}</div>
                  <div className="text-[10px] text-slate-400">{user?.email || 'admin@smartcare.ai'}</div>
                </div>

                <button
                  onClick={() => { setActiveTab('profile'); setProfileOpen(false); }}
                  className="w-full text-left px-3 py-2 rounded-xl text-xs font-semibold text-slate-300 hover:bg-slate-800 hover:text-white transition"
                >
                  Admin Profile
                </button>

                <button
                  onClick={onLogout}
                  className="w-full text-left px-3 py-2 rounded-xl text-xs font-semibold text-red-400 hover:bg-red-500/10 transition flex items-center space-x-2"
                >
                  <LogOut className="w-3.5 h-3.5" />
                  <span>Sign Out</span>
                </button>
              </div>
            )}
          </div>

        </div>

      </div>
    </header>
  );
}
