import React, { useState } from 'react';
import Logo from '../../components/Logo';
import WorkspaceBackground from '../../components/WorkspaceBackground';
import DashboardOverview from '../DashboardOverview';
import RiskAssessment from '../RiskAssessment';
import Explainability from '../Explainability';
import PersonalizedWellnessPlan from '../PersonalizedWellnessPlan';
import RiskHistory from '../RiskHistory';
import HealthDataForm from '../HealthDataForm';
import PatientProfile from './PatientProfile';
import PatientSettings from './PatientSettings';
import PatientReports from './PatientReports';
import { 
  HeartPulse, User, ClipboardList, Activity, Sparkles, FileText, 
  TrendingUp, Settings, LogOut, ShieldCheck, ChevronRight, FileCheck2
} from 'lucide-react';

export default function PatientPortal({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [currentAssessment, setCurrentAssessment] = useState(() => {
    try {
      const saved = localStorage.getItem('smartcare_last_assessment');
      return saved ? JSON.parse(saved) : null;
    } catch (e) {
      return null;
    }
  });

  const handleAssessmentChange = (newAssessment) => {
    setCurrentAssessment(newAssessment);
    try {
      if (newAssessment) {
        localStorage.setItem('smartcare_last_assessment', JSON.stringify(newAssessment));
      }
    } catch (e) {
      console.error(e);
    }
  };

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: HeartPulse, badge: 'Overview' },
    { id: 'reports', label: 'My Reports', icon: FileCheck2, badge: 'Clinical' },
    { id: 'profile', label: 'My Profile', icon: User },
    { id: 'form', label: 'Health Assessment', icon: ClipboardList, badge: 'Input' },
    { id: 'risk', label: 'Risk Prediction', icon: Activity },
    { id: 'explain', label: 'SHAP Explanation', icon: Sparkles },
    { id: 'wellness', label: 'Wellness Plan', icon: FileText },
    { id: 'risk_history', label: 'Health Trends', icon: TrendingUp },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <div className="relative h-screen max-h-screen overflow-hidden bg-[#080512] text-slate-100 flex flex-col font-sans selection:bg-[#7C3AED]/40">
      <WorkspaceBackground />

      {/* Patient Header */}
      <header className="relative z-20 shrink-0 px-6 py-3.5 border-b border-[#2A1A4E] bg-[#0D0718]/90 backdrop-blur-md flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Logo variant="full" size="md" />
          <div className="hidden md:flex items-center space-x-2 px-3 py-1 rounded-full bg-[#7C3AED]/20 border border-[#7C3AED]/40 text-[#C084FC] text-[10px] font-mono font-bold uppercase tracking-wider">
            <span className="w-2 h-2 rounded-full bg-[#7C3AED] animate-pulse" />
            <span>PATIENT WELLNESS PORTAL</span>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <div className="text-right hidden sm:block font-mono">
            <div className="text-xs font-bold text-white">{user?.full_name || user?.username || 'Patient'}</div>
            <div className="text-[10px] text-[#C084FC] font-semibold">Patient Account #{user?.id || 100}</div>
          </div>
          
          <button
            onClick={onLogout}
            className="p-2.5 rounded-xl bg-[#1A0F33] hover:bg-red-500/20 border border-[#2A1A4E] hover:border-red-500/50 text-slate-300 hover:text-red-300 transition flex items-center space-x-1.5 text-xs font-mono cursor-pointer"
            title="Sign Out"
          >
            <LogOut className="w-4 h-4" />
            <span className="hidden sm:inline">Logout</span>
          </button>
        </div>
      </header>

      {/* Main Body */}
      <div className="relative z-10 flex-1 flex overflow-hidden min-h-0">
        
        {/* Patient Sidebar */}
        <aside className="w-64 shrink-0 border-r border-[#2A1A4E] bg-[#0D0718]/70 backdrop-blur-md p-4 hidden lg:flex flex-col justify-between overflow-y-auto">
          <div className="space-y-1">
            <div className="px-3 py-2 text-[10px] font-mono uppercase tracking-widest text-[#C084FC] font-bold">
              PATIENT NAVIGATION
            </div>

            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full py-2.5 px-3.5 rounded-xl text-xs font-mono font-bold transition flex items-center justify-between cursor-pointer ${
                    isActive
                      ? 'bg-gradient-to-r from-[#6D28D9] to-[#7C3AED] text-white shadow-lg shadow-[#7C3AED]/20 border border-[#8B5CF6]'
                      : 'text-slate-300 hover:text-white hover:bg-[#1A0F33]'
                  }`}
                >
                  <div className="flex items-center space-x-2.5">
                    <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-[#C084FC]'}`} />
                    <span>{item.label}</span>
                  </div>
                  {item.badge && (
                    <span className="text-[9px] px-2 py-0.5 rounded-full bg-[#080512] text-[#C084FC] border border-[#7C3AED]/30">
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </div>

          <div className="p-3.5 rounded-2xl bg-[#120A24] border border-[#2A1A4E] text-[10px] font-mono text-slate-400 space-y-1">
            <div className="flex items-center space-x-1.5 text-[#22C55E] font-bold">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>HIPAA DATA PRIVACY</span>
            </div>
            <p className="leading-tight">Your personal health data is encrypted and strictly isolated.</p>
          </div>
        </aside>

        {/* Workspace Content View */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8 overflow-y-auto max-w-[1600px] mx-auto pb-28">
          
          {/* Mobile Nav Tabs */}
          <div className="lg:hidden flex overflow-x-auto space-x-2 pb-4 mb-4 border-b border-[#2A1A4E]">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`py-2 px-3 rounded-xl text-xs font-mono font-bold whitespace-nowrap flex items-center space-x-1.5 ${
                    isActive ? 'bg-[#7C3AED] text-white' : 'bg-[#120A24] text-slate-300'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </div>

          <div className="animate-in fade-in slide-in-from-bottom-2 duration-300">
            {activeTab === 'dashboard' && <DashboardOverview user={user} onNavigate={setActiveTab} />}
            {activeTab === 'reports' && <PatientReports user={user} onNavigate={setActiveTab} />}
            {activeTab === 'profile' && <PatientProfile user={user} />}
            {activeTab === 'form' && <HealthDataForm user={user} onNavigate={setActiveTab} />}
            {activeTab === 'risk' && <RiskAssessment user={user} onNavigate={setActiveTab} currentAssessment={currentAssessment} onAssessmentChange={handleAssessmentChange} />}
            {activeTab === 'explain' && <Explainability currentAssessment={currentAssessment} />}
            {activeTab === 'wellness' && <PersonalizedWellnessPlan user={user} currentAssessment={currentAssessment} onNavigate={setActiveTab} />}
            {activeTab === 'risk_history' && <RiskHistory user={user} onNavigate={setActiveTab} />}
            {activeTab === 'settings' && <PatientSettings user={user} />}
          </div>

        </main>
      </div>
    </div>
  );
}
