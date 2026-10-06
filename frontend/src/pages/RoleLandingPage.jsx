import React from 'react';
import Logo from '../components/Logo';
import WorkspaceBackground from '../components/WorkspaceBackground';
import DataFlowVisualization from '../components/DataFlowVisualization';
import { UserCheck, Stethoscope, ShieldAlert, Sparkles, ArrowRight, ShieldCheck } from 'lucide-react';

export default function RoleLandingPage({ onSelectRole }) {
  const roles = [
    {
      id: 'patient',
      title: 'PATIENT',
      subtitle: 'Patient Portal Login',
      description: 'Access your health records, view AI risk predictions, SHAP explanations, and personalized wellness plans.',
      icon: UserCheck,
      badge: 'PATIENT ACCESS',
      accentColor: 'from-[#6D28D9] to-[#7C3AED]',
      borderGlow: 'hover:border-[#8B5CF6] hover:shadow-[#7C3AED]/30',
      btnColor: 'bg-[#7C3AED] hover:bg-[#8B5CF6]',
      route: '/login/patient'
    },
    {
      id: 'doctor',
      title: 'DOCTOR',
      subtitle: 'Doctor Portal Login',
      description: 'Clinical decision support, patient risk monitoring, SHAP factor analysis, and clinician feedback workflows.',
      icon: Stethoscope,
      badge: 'CLINICIAN ACCESS',
      accentColor: 'from-[#7C3AED] to-[#A855F7]',
      borderGlow: 'hover:border-[#C084FC] hover:shadow-[#A855F7]/30',
      btnColor: 'bg-[#A855F7] hover:bg-[#C084FC]',
      route: '/login/doctor'
    },
    {
      id: 'admin',
      title: 'ADMIN',
      subtitle: 'Admin Portal Login',
      description: 'System administration, RBAC security audit logging, ML pipeline benchmarking, and dataset management.',
      icon: ShieldAlert,
      badge: 'ADMINISTRATION ACCESS',
      accentColor: 'from-[#6D28D9] to-[#EF4444]',
      borderGlow: 'hover:border-[#EF4444] hover:shadow-[#EF4444]/30',
      btnColor: 'bg-gradient-to-r from-[#7C3AED] to-[#EF4444] hover:brightness-110',
      route: '/login/admin'
    }
  ];

  return (
    <div className="relative min-h-screen bg-[#080512] text-slate-100 flex flex-col font-sans selection:bg-[#7C3AED]/40">
      <WorkspaceBackground />

      {/* Header Bar */}
      <header className="relative z-20 px-6 py-4 flex items-center justify-between border-b border-[#2A1A4E] bg-[#0D0718]/80 backdrop-blur-md">
        <Logo variant="full" size="md" />
        <div className="text-xs text-[#C084FC] uppercase tracking-widest font-mono font-bold flex items-center space-x-2">
          <span className="w-2 h-2 rounded-full bg-[#7C3AED] animate-ping" />
          <span className="hidden sm:inline">SMARTCARE AI HEALTHCARE PLATFORM</span>
        </div>
      </header>

      {/* Main Container */}
      <main className="relative z-20 flex-1 max-w-7xl w-full mx-auto px-4 py-10 flex flex-col justify-center items-center space-y-10">
        
        {/* Title Header */}
        <div className="text-center space-y-4 max-w-3xl">
          <div className="inline-flex items-center space-x-2 px-4 py-1.5 rounded-full bg-[#7C3AED]/20 border border-[#7C3AED]/40 text-[#C084FC] text-xs font-mono font-bold uppercase tracking-widest">
            <Sparkles className="w-4 h-4 text-[#C084FC]" />
            <span>ROLE-BASED AUTHENTICATION GATEWAY</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white uppercase font-sans">
            SMARTCARE AI
          </h1>

          <p className="text-lg sm:text-xl font-mono text-[#C084FC] font-semibold tracking-wider">
            Healthcare Intelligence & IT
          </p>

          <p className="text-xs sm:text-sm text-slate-300 max-w-xl mx-auto leading-relaxed">
            Select your assigned role to access the dedicated login portal. Every workspace is protected by server-side Role-Based Access Control (RBAC).
          </p>
        </div>

        {/* 3 Role Selection Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-5xl">
          {roles.map((role) => {
            const Icon = role.icon;
            return (
              <div
                key={role.id}
                onClick={() => onSelectRole(role.id)}
                className={`group relative bg-[#0D0718]/90 border border-[#2A1A4E] ${role.borderGlow} rounded-3xl p-6 flex flex-col justify-between space-y-6 transition-all duration-300 transform hover:-translate-y-1.5 shadow-xl cursor-pointer backdrop-blur-sm`}
              >
                {/* Role Header */}
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="px-3 py-1 rounded-full bg-[#2A1A4E]/80 border border-[#7C3AED]/40 text-[10px] font-mono font-bold text-[#C084FC] tracking-wider uppercase">
                      {role.badge}
                    </span>
                    <div className="w-10 h-10 rounded-2xl bg-[#1A0F33] border border-[#7C3AED]/40 flex items-center justify-center text-[#C084FC] group-hover:scale-110 transition duration-300">
                      <Icon className="w-5 h-5" />
                    </div>
                  </div>

                  <div>
                    <h2 className="text-2xl font-extrabold text-white tracking-wide flex items-center space-x-2">
                      <span>{role.title}</span>
                    </h2>
                    <p className="text-xs font-mono text-[#C084FC] mt-0.5 font-bold">
                      {role.subtitle}
                    </p>
                  </div>

                  <p className="text-xs text-slate-300 leading-relaxed font-sans">
                    {role.description}
                  </p>
                </div>

                {/* Login Action Button */}
                <div>
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      onSelectRole(role.id);
                    }}
                    className={`w-full py-3 px-4 rounded-xl ${role.btnColor} text-white font-extrabold text-xs uppercase tracking-wider transition shadow-lg flex items-center justify-center space-x-2 group-hover:brightness-110 cursor-pointer`}
                  >
                    <span>Login</span>
                    <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>

        {/* Pipeline Preview Data Visualization */}
        <div className="w-full max-w-4xl pt-4">
          <DataFlowVisualization />
        </div>

        {/* Footer Security Badge */}
        <div className="flex items-center justify-center space-x-2 text-slate-400 text-xs font-mono">
          <ShieldCheck className="w-4 h-4 text-[#22C55E]" />
          <span>ENCRYPTED ROLE-BASED ACCESS CONTROL (RBAC) SYSTEM</span>
        </div>

      </main>
    </div>
  );
}
