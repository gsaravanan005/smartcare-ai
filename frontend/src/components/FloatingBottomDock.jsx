import React, { useState } from 'react';
import { 
  LayoutDashboard, Activity, HelpCircle, User, Database, 
  GitMerge, BarChart2, Clock, Box, UserCheck, Sparkles, Stethoscope, MessageSquare, ShieldCheck 
} from 'lucide-react';

export default function FloatingBottomDock({ user, activeTab, setActiveTab }) {
  const [hoveredTab, setHoveredTab] = useState(null);

  const role = (user?.role || 'patient').toLowerCase();

  const allItems = [
    { id: 'dashboard', label: 'Dashboard Overview', icon: LayoutDashboard, roles: ['patient', 'admin'] },
    { id: 'clinician_dashboard', label: 'Doctor Portal', icon: Stethoscope, roles: ['doctor', 'clinician', 'admin'] },
    { id: 'risk', label: 'Risk Assessment', icon: Activity, roles: ['patient', 'doctor', 'clinician', 'admin'] },
    { id: 'explain', label: 'SHAP Explainability', icon: HelpCircle, roles: ['patient', 'doctor', 'clinician', 'admin'] },
    { id: 'wellness', label: 'Wellness Plan', icon: Sparkles, roles: ['patient', 'doctor', 'clinician', 'admin'] },
    { id: 'risk_history', label: 'Health Trends & History', icon: Clock, roles: ['patient', 'doctor', 'clinician', 'admin'] },
    { id: 'form', label: 'Patient Vitals Data', icon: User, roles: ['patient', 'doctor', 'clinician', 'admin'] },
    { id: 'data_quality', label: 'Data Quality Profiling', icon: Database, roles: ['admin'] },
    { id: 'pipeline', label: 'Pipeline Runner', icon: GitMerge, roles: ['admin'] },
    { id: 'models', label: 'Model Benchmark', icon: BarChart2, roles: ['admin'] },
    { id: 'experiments', label: 'Experiment Tracking', icon: Clock, roles: ['admin'] },
    { id: 'registry', label: 'AI Model Registry', icon: Box, roles: ['admin'] },
    { id: 'profile', label: 'Account & Security', icon: ShieldCheck, roles: ['patient', 'doctor', 'clinician', 'admin'] }
  ];

  const filteredDockItems = allItems.filter(item => item.roles.includes(role));

  return (
    <div className="fixed bottom-4 left-1/2 -translate-x-1/2 z-50 select-none max-w-[95vw]">
      <div className="relative bg-[#0D0718]/95 backdrop-blur-2xl border border-[#2A1A4E] rounded-2xl px-3 py-2 shadow-2xl shadow-[#080512]/90 flex items-center space-x-1 sm:space-x-2">
        
        {filteredDockItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          const isHovered = hoveredTab === item.id;

          return (
            <div key={item.id} className="relative flex flex-col items-center">
              
              {/* Floating Tooltip Label on Hover */}
              {isHovered && (
                <div className="absolute -top-10 px-2.5 py-1 rounded-xl bg-[#120A24] border border-[#7C3AED]/50 text-white font-mono text-[10px] font-bold shadow-xl whitespace-nowrap animate-in fade-in zoom-in-95 duration-150 z-50">
                  {item.label}
                  <div className="w-2 h-2 bg-[#120A24] border-r border-b border-[#7C3AED]/50 rotate-45 absolute -bottom-1 left-1/2 -translate-x-1/2" />
                </div>
              )}

              {/* Active Indicator Dot */}
              <div className="h-2 flex items-center justify-center mb-0.5">
                {isActive && (
                  <span className="w-1.5 h-1.5 rounded-full bg-[#C084FC] shadow-md shadow-[#C084FC] animate-pulse" />
                )}
              </div>

              {/* Dock Button Icon */}
              <button
                type="button"
                onClick={() => setActiveTab(item.id)}
                onMouseEnter={() => setHoveredTab(item.id)}
                onMouseLeave={() => setHoveredTab(null)}
                className={`p-2.5 rounded-xl transition-all duration-200 cursor-pointer relative group flex items-center justify-center outline-none ${
                  isActive
                    ? 'bg-gradient-to-b from-[#7C3AED]/40 to-[#120A24] text-[#C084FC] border border-[#8B5CF6]/60 shadow-lg shadow-[#7C3AED]/40 scale-110'
                    : isHovered
                    ? 'bg-[#120A24] text-white border border-[#2A1A4E] scale-125 shadow-md shadow-[#7C3AED]/30 -translate-y-1'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-[#0D0718] border border-transparent'
                }`}
              >
                <Icon className={`w-4 h-4 transition-transform ${
                  isActive ? 'text-[#C084FC]' : 'text-slate-400 group-hover:text-[#C084FC]'
                }`} />
              </button>
            </div>
          );
        })}

      </div>
    </div>
  );
}
