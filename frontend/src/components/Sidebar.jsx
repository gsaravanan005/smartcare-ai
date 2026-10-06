import React from 'react';
import Logo from './Logo';
import { 
  LayoutDashboard, Activity, HelpCircle, User, Database, 
  GitMerge, BarChart2, Clock, Box, UserCheck, Sparkles, Stethoscope, MessageSquare, ShieldCheck, X 
} from 'lucide-react';

export default function Sidebar({ user, activeTab, setActiveTab, isOpen, onClose }) {
  if (!isOpen) return null;

  const role = (user?.role || 'patient').toLowerCase();

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard Overview', icon: LayoutDashboard, roles: ['patient', 'admin'] },
    { id: 'clinician_dashboard', label: 'Doctor Dashboard', icon: Stethoscope, roles: ['doctor', 'clinician', 'admin'] },
    { id: 'risk', label: 'Risk Assessment', icon: Activity, roles: ['patient', 'doctor', 'clinician', 'admin'] },
    { id: 'explain', label: 'SHAP Explainability', icon: HelpCircle, roles: ['patient', 'doctor', 'clinician', 'admin'] },
    { id: 'wellness', label: 'Personalized Wellness Plan', icon: Sparkles, roles: ['patient', 'doctor', 'clinician', 'admin'] },
    { id: 'risk_history', label: 'Health Trends & History', icon: Clock, roles: ['patient', 'doctor', 'clinician', 'admin'] },
    { id: 'form', label: 'Health Vitals Input', icon: User, roles: ['patient', 'doctor', 'clinician', 'admin'] },
    { id: 'data_quality', label: 'Data Quality Profiling', icon: Database, roles: ['admin'] },
    { id: 'pipeline', label: 'Pipeline Runner', icon: GitMerge, roles: ['admin'] },
    { id: 'models', label: 'Model Benchmark', icon: BarChart2, roles: ['admin'] },
    { id: 'experiments', label: 'Experiment Tracking', icon: Clock, roles: ['admin'] },
    { id: 'registry', label: 'AI Model Registry', icon: Box, roles: ['admin'] },
    { id: 'profile', label: 'My Profile & Security', icon: ShieldCheck, roles: ['patient', 'doctor', 'clinician', 'admin'] }
  ].filter(item => item.roles.includes(role));

  return (
    <div className="fixed inset-0 z-50 flex font-mono text-xs select-none">
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black/70 backdrop-blur-sm" onClick={onClose} />

      {/* Drawer */}
      <div className="relative w-72 max-w-[80vw] bg-[#0D0718] border-r border-[#2A1A4E] h-full p-4 flex flex-col justify-between z-10 shadow-2xl animate-in slide-in-from-left duration-250">
        <div className="space-y-6">
          <div className="flex items-center justify-between border-b border-[#2A1A4E] pb-3">
            <Logo variant="full" size="sm" />
            <button onClick={onClose} className="p-1 rounded-lg text-slate-400 hover:text-white">
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="space-y-1">
            <div className="text-[10px] font-bold text-[#C084FC] uppercase tracking-wider px-2 py-1">
              {role.toUpperCase()} NAVIGATION
            </div>
            {menuItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;

              return (
                <button
                  key={item.id}
                  onClick={() => { setActiveTab(item.id); onClose(); }}
                  className={`w-full text-left px-3 py-2.5 rounded-xl transition flex items-center space-x-3 ${
                    isActive
                      ? 'bg-[#7C3AED] text-white font-bold shadow-lg shadow-[#7C3AED]/30'
                      : 'text-slate-300 hover:bg-[#120A24] hover:text-[#C084FC]'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        <div className="border-t border-[#2A1A4E] pt-3 text-[10px] text-slate-400 text-center">
          SmartCare AI v6.0 • Dark Purple Healthcare Theme
        </div>
      </div>
    </div>
  );
}
