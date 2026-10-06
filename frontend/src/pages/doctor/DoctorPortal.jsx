import React, { useState } from 'react';
import Logo from '../../components/Logo';
import WorkspaceBackground from '../../components/WorkspaceBackground';
import ClinicianDashboard from '../ClinicianDashboard';
import ClinicianPatientDetail from '../ClinicianPatientDetail';
import DoctorProfile from './DoctorProfile';
import Explainability from '../Explainability';
import RiskHistory from '../RiskHistory';
import { 
  Stethoscope, Users, Search, Activity, Sparkles, AlertTriangle, 
  FileSpreadsheet, LogOut, ShieldCheck, Settings, Award
} from 'lucide-react';

export default function DoctorPortal({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedPatientId, setSelectedPatientId] = useState(1);

  const navItems = [
    { id: 'dashboard', label: 'Clinical Dashboard', icon: Stethoscope, badge: 'Overview' },
    { id: 'patients', label: 'My Patients', icon: Users },
    { id: 'detail', label: 'Patient Profile & SHAP', icon: Activity },
    { id: 'alerts', label: 'Clinical Alerts', icon: AlertTriangle },
    { id: 'insights', label: 'AI Clinical Insights', icon: Sparkles },
    { id: 'settings', label: 'Account Settings', icon: Settings }
  ];

  return (
    <div className="relative h-screen max-h-screen overflow-hidden bg-[#080512] text-slate-100 flex flex-col font-sans selection:bg-[#A855F7]/40">
      <WorkspaceBackground />

      {/* Doctor Header */}
      <header className="relative z-20 shrink-0 px-6 py-3.5 border-b border-[#2A1A4E] bg-[#0D0718]/90 backdrop-blur-md flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Logo variant="full" size="md" />
          <div className="hidden md:flex items-center space-x-2 px-3 py-1 rounded-full bg-[#A855F7]/20 border border-[#A855F7]/40 text-[#C084FC] text-[10px] font-mono font-bold uppercase tracking-wider">
            <Stethoscope className="w-3.5 h-3.5 text-[#C084FC]" />
            <span>CLINICIAN DECISION SUPPORT PORTAL</span>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <div className="text-right hidden sm:block font-mono">
            <div className="text-xs font-bold text-white flex items-center space-x-1 justify-end">
              <Award className="w-3.5 h-3.5 text-[#C084FC]" />
              <span>{user?.full_name || user?.username || 'Dr. Sarah Jenkins'}</span>
            </div>
            <div className="text-[10px] text-[#C084FC] font-semibold">Verified Clinician • License LIC-000100</div>
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

      {/* Main Container */}
      <div className="relative z-10 flex-1 flex overflow-hidden min-h-0">
        
        {/* Doctor Sidebar */}
        <aside className="w-64 shrink-0 border-r border-[#2A1A4E] bg-[#0D0718]/70 backdrop-blur-md p-4 hidden lg:flex flex-col justify-between overflow-y-auto">
          <div className="space-y-1">
            <div className="px-3 py-2 text-[10px] font-mono uppercase tracking-widest text-[#C084FC] font-bold">
              CLINICAL NAVIGATION
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
                      ? 'bg-gradient-to-r from-[#7C3AED] to-[#A855F7] text-white shadow-lg shadow-[#A855F7]/20 border border-[#C084FC]'
                      : 'text-slate-300 hover:text-white hover:bg-[#1A0F33]'
                  }`}
                >
                  <div className="flex items-center space-x-2.5">
                    <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-[#C084FC]'}`} />
                    <span>{item.label}</span>
                  </div>
                  {item.badge && (
                    <span className="text-[9px] px-2 py-0.5 rounded-full bg-[#080512] text-[#C084FC] border border-[#A855F7]/30">
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
              <span>DOCTOR-PATIENT RBAC</span>
            </div>
            <p className="leading-tight">Access is restricted strictly to authorized patient relationships.</p>
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
                    isActive ? 'bg-[#A855F7] text-white' : 'bg-[#120A24] text-slate-300'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </div>

          <div className="animate-in fade-in slide-in-from-bottom-2 duration-300">
            {activeTab === 'dashboard' && (
              <ClinicianDashboard 
                user={user} 
                onNavigate={setActiveTab} 
                onSelectPatient={(pid) => {
                  setSelectedPatientId(pid);
                  setActiveTab('detail');
                }} 
              />
            )}
            {activeTab === 'patients' && (
              <ClinicianDashboard 
                user={user} 
                onNavigate={setActiveTab} 
                onSelectPatient={(pid) => {
                  setSelectedPatientId(pid);
                  setActiveTab('detail');
                }} 
              />
            )}
            {activeTab === 'detail' && (
              <ClinicianPatientDetail 
                patientId={selectedPatientId} 
                onSelectPatient={(pid) => setSelectedPatientId(pid)}
                onBack={() => setActiveTab('dashboard')} 
              />
            )}
            {activeTab === 'alerts' && (
              <ClinicianDashboard 
                user={user} 
                onNavigate={setActiveTab} 
                onSelectPatient={(pid) => {
                  setSelectedPatientId(pid);
                  setActiveTab('detail');
                }} 
              />
            )}
            {activeTab === 'insights' && (
              <Explainability />
            )}
            {activeTab === 'settings' && <DoctorProfile user={user} />}
          </div>

        </main>
      </div>

    </div>
  );
}
