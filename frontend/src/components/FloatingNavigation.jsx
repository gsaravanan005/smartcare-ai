import React from 'react';
import { 
  LayoutDashboard, Activity, HelpCircle, User, BarChart2, Database, 
  GitMerge, Clock, Box, UserCheck 
} from 'lucide-react';

export default function FloatingNavigation({ activeTab, setActiveTab }) {
  const NAV_ITEMS = [
    { id: 'dashboard', label: 'Overview', icon: LayoutDashboard },
    { id: 'risk', label: 'Risk Assessment', icon: Activity },
    { id: 'explain', label: 'Why This Risk?', icon: HelpCircle },
    { id: 'form', label: 'Patient Data', icon: User },
    { id: 'data_quality', label: 'Data Quality', icon: Database },
    { id: 'pipeline', label: 'Pipeline Runner', icon: GitMerge },
    { id: 'models', label: 'Model Benchmark', icon: BarChart2 },
    { id: 'experiments', label: 'Experiment Tracking', icon: Clock },
    { id: 'registry', label: 'Model Registry', icon: Box },
    { id: 'profile', label: 'Admin Profile', icon: UserCheck }
  ];

  return (
    <div className="fixed bottom-4 left-1/2 transform -translate-x-1/2 z-50 w-auto max-w-[95vw] pointer-events-auto px-2">
      <nav className="flex items-center gap-1.5 px-4 py-2.5 rounded-full backdrop-blur-2xl bg-slate-950/95 border border-cyan-500/40 shadow-2xl shadow-cyan-950/80 overflow-x-auto no-scrollbar scroll-smooth">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;

          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex-shrink-0 relative group flex items-center space-x-2 px-3.5 py-1.5 rounded-full text-[11px] font-mono font-bold transition-all duration-200 cursor-pointer ${
                isActive
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-400/70 shadow-md shadow-cyan-500/25 scale-102'
                  : 'text-slate-400 hover:text-white hover:bg-slate-900/80 border border-transparent'
              }`}
            >
              {/* Illuminated Active Node Icon */}
              <Icon className={`w-3.5 h-3.5 flex-shrink-0 transition-transform duration-200 ${isActive ? 'text-cyan-400 animate-pulse scale-110' : 'text-slate-400 group-hover:text-cyan-300'}`} />

              {/* Text Label: Always Visible & Protected Inside Border */}
              <span className="whitespace-nowrap tracking-tight">
                {item.label}
              </span>

              {/* Active Cyan Glow Dot Indicator */}
              {isActive && (
                <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 shadow-sm shadow-cyan-400 animate-ping absolute -top-0.5 right-1" />
              )}
            </button>
          );
        })}
      </nav>
    </div>
  );
}
