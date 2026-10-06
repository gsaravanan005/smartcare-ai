import React, { useState, useEffect, useRef } from 'react';
import { 
  Stethoscope, Cpu, FlaskConical, Settings, LayoutDashboard, Activity, User, 
  HelpCircle, Database, GitMerge, BarChart2, Clock, Box, UserCheck, ChevronDown, Sparkles, MessageSquare, ShieldCheck
} from 'lucide-react';

export default function AICommandBar({ user, activeTab, setActiveTab }) {
  const [openCategory, setOpenCategory] = useState(null);
  const containerRef = useRef(null);

  const role = (user?.role || 'patient').toLowerCase();

  let categories = [];

  if (role === 'patient') {
    categories = [
      {
        id: 'PATIENT_WELLNESS',
        label: 'PATIENT WELLNESS',
        icon: Activity,
        items: [
          { id: 'dashboard', label: 'Patient Dashboard', desc: 'Overview, Wellness Score & Vitals', icon: LayoutDashboard },
          { id: 'risk', label: 'Risk Prediction', desc: 'Predictive health risk assessment', icon: Activity },
          { id: 'explain', label: 'SHAP Risk Explanation', desc: 'Personalized risk factor breakdown', icon: HelpCircle },
          { id: 'wellness', label: 'Personalized Wellness Plan', desc: 'Diet, exercise, habits & herbal advice', icon: Sparkles },
          { id: 'risk_history', label: 'Health Trends & History', desc: 'Longitudinal risk trajectory over time', icon: Clock },
          { id: 'form', label: 'Health Information Vitals', desc: 'Update personal vitals & medical inputs', icon: User }
        ]
      }
    ];
  } else if (role === 'doctor' || role === 'clinician') {
    categories = [
      {
        id: 'DOCTOR_PORTAL',
        label: 'DOCTOR PORTAL',
        icon: Stethoscope,
        items: [
          { id: 'clinician_dashboard', label: 'Doctor Dashboard', desc: 'Clinical stats, alerts & reviews required', icon: LayoutDashboard },
          { id: 'risk', label: 'Risk Predictions & Inference', desc: 'Multi-disease clinical assessment', icon: Activity },
          { id: 'explain', label: 'SHAP Explanations', desc: 'Explainable AI feature attribution', icon: HelpCircle },
          { id: 'wellness', label: 'Wellness Plans', desc: 'Personalized wellness recommendations', icon: Sparkles }
        ]
      }
    ];
  } else {
    // ADMIN role
    categories = [
      {
        id: 'CLINICAL',
        label: 'CLINICAL & PATIENTS',
        icon: Stethoscope,
        items: [
          { id: 'dashboard', label: 'Dashboard Overview', desc: 'Live multi-task risk telemetry', icon: LayoutDashboard },
          { id: 'clinician_dashboard', label: 'Doctor Dashboard', desc: 'Patient roster & clinical decision support', icon: UserCheck },
          { id: 'risk', label: 'Risk Assessment Engine', desc: 'Multi-disease risk prediction', icon: Activity },
          { id: 'explain', label: 'SHAP Explainability Lab', desc: 'Feature attribution & risk factors', icon: HelpCircle },
          { id: 'wellness', label: 'Wellness Plan Engine', desc: 'Personalized recommendation engine', icon: Sparkles }
        ]
      },
      {
        id: 'AI_INTELLIGENCE',
        label: 'AI & PIPELINES',
        icon: Cpu,
        items: [
          { id: 'data_quality', label: 'Data Quality & Profiling', desc: 'Dataset profiling & missingness analysis', icon: Database },
          { id: 'pipeline', label: 'Pipeline Runner', desc: 'Preprocessing & feature engineering graph', icon: GitMerge }
        ]
      },
      {
        id: 'MODEL_LAB',
        label: 'MODEL MANAGEMENT',
        icon: FlaskConical,
        items: [
          { id: 'models', label: 'Model Benchmark & Analytics', desc: 'Performance ROC/PR & calibration', icon: BarChart2 },
          { id: 'experiments', label: 'Experiment Tracking', desc: 'Hyperparameter runs & ML audit', icon: Clock },
          { id: 'registry', label: 'AI Model Registry', desc: 'Production models & version lineage', icon: Box }
        ]
      },
      {
        id: 'SYSTEM',
        label: 'ADMIN & SECURITY',
        icon: Settings,
        items: [
          { id: 'profile', label: 'Admin Management & Security', desc: 'Account permissions & audit log clearance', icon: ShieldCheck },
          { id: 'settings', label: 'System Settings', desc: 'System configuration & credentials', icon: Settings }
        ]
      }
    ];
  }

  // Close menu when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setOpenCategory(null);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div ref={containerRef} className="w-full bg-[#080512]/95 backdrop-blur-md border-b border-[#2A1A4E] py-2 px-4 sticky top-[56px] z-40 select-none">
      <div className="max-w-[1920px] mx-auto flex items-center justify-between font-mono text-xs">
        
        {/* Category Buttons Row */}
        <div className="flex items-center space-x-2 relative w-full justify-center sm:justify-start">
          {categories.map((cat) => {
            const CatIcon = cat.icon;
            const isOpen = openCategory === cat.id;
            const hasActiveTab = cat.items.some(item => item.id === activeTab);

            return (
              <div 
                key={cat.id} 
                className="relative"
                onMouseEnter={() => setOpenCategory(cat.id)}
                onMouseLeave={() => setOpenCategory(null)}
              >
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    setOpenCategory(isOpen ? null : cat.id);
                  }}
                  className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-xl font-bold uppercase text-[11px] tracking-wider transition-all duration-200 cursor-pointer outline-none focus:outline-none ${
                    isOpen || hasActiveTab
                      ? 'bg-[#7C3AED]/30 text-[#C084FC] border border-[#8B5CF6] shadow-lg shadow-[#7C3AED]/30'
                      : 'bg-[#0D0718] text-slate-400 hover:text-white hover:bg-[#120A24] border border-[#2A1A4E]'
                  }`}
                >
                  <CatIcon className={`w-3.5 h-3.5 ${hasActiveTab || isOpen ? 'text-[#C084FC]' : 'text-slate-400'}`} />
                  <span>{cat.label}</span>
                  <ChevronDown className={`w-3 h-3 transition-transform duration-200 ${isOpen ? 'rotate-180 text-[#C084FC]' : 'text-slate-500'}`} />
                </button>

                {/* Animated Floating Glass Command Panel */}
                {isOpen && (
                  <div className="absolute left-0 top-full mt-1.5 w-64 rounded-2xl bg-[#0D0718] border border-[#7C3AED]/60 p-2.5 shadow-2xl z-[100] font-sans">
                    <div className="text-[9px] font-mono font-extrabold text-[#C084FC] tracking-wider uppercase px-2 py-1 border-b border-[#2A1A4E] mb-1.5 flex items-center justify-between">
                      <span>{cat.label} WORKSPACES</span>
                      <Sparkles className="w-3 h-3 text-[#C084FC]" />
                    </div>

                    <div className="space-y-1 font-mono">
                      {cat.items.map((item) => {
                        const ItemIcon = item.icon;
                        const isActive = activeTab === item.id;

                        return (
                          <button
                            key={item.id}
                            type="button"
                            onClick={() => {
                              setActiveTab(item.id);
                              setOpenCategory(null);
                            }}
                            className={`w-full text-left px-2.5 py-2 rounded-xl transition-all flex items-start space-x-2.5 group cursor-pointer outline-none ${
                              isActive
                                ? 'bg-gradient-to-r from-[#7C3AED]/40 to-[#120A24] text-white border border-[#8B5CF6] font-bold shadow-md shadow-[#7C3AED]/30'
                                : 'text-slate-300 hover:bg-[#120A24] hover:text-[#C084FC] border border-transparent'
                            }`}
                          >
                            <ItemIcon className={`w-4 h-4 mt-0.5 flex-shrink-0 ${isActive ? 'text-[#C084FC]' : 'text-slate-400 group-hover:text-[#C084FC]'}`} />
                            <div>
                              <div className="text-xs font-bold">{item.label}</div>
                              <div className="text-[10px] text-slate-400 font-sans leading-tight mt-0.5">{item.desc}</div>
                            </div>
                          </button>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Current Active Workspace Indicator */}
        <div className="hidden lg:flex items-center space-x-2 px-3 py-1 rounded-xl bg-[#0D0718] border border-[#2A1A4E] text-[10px] text-slate-300 flex-shrink-0">
          <span className="w-1.5 h-1.5 rounded-full bg-[#7C3AED]" />
          <span className="text-[#C084FC] font-bold uppercase">{activeTab.replace('_', ' ')} WORKSPACE</span>
        </div>

      </div>
    </div>
  );
}
