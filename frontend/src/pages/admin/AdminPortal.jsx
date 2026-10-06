import React, { useState } from 'react';
import Logo from '../../components/Logo';
import WorkspaceBackground from '../../components/WorkspaceBackground';
import ModelRegistry from '../ModelRegistry';
import AdminProfile from '../AdminProfile';
import UserManagementPanel from './UserManagementPanel';
import DoctorManagementPanel from './DoctorManagementPanel';
import PredictionAnalyticsPanel from './PredictionAnalyticsPanel';
import AuditLogsPanel from './AuditLogsPanel';

import { 
  ShieldAlert, LayoutDashboard, Users, UserCheck, Cpu, 
  Settings, ShieldCheck, LogOut, Lock
} from 'lucide-react';

export default function AdminPortal({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState('dashboard');

  const navItems = [
    { id: 'dashboard', label: 'System Dashboard', icon: LayoutDashboard, badge: 'Live' },
    { id: 'patients', label: 'Patient Management', icon: Users },
    { id: 'doctors', label: 'Doctor Verification', icon: UserCheck },
    { id: 'admins', label: 'Admin Management', icon: ShieldCheck, badge: 'SuperAdmin' },
    { id: 'models', label: 'AI Model Registry', icon: Cpu },
    { id: 'audit', label: 'RBAC Audit Logs', icon: Lock },
    { id: 'settings', label: 'System Settings', icon: Settings }
  ];

  return (
    <div className="relative h-screen max-h-screen overflow-hidden bg-[#080512] text-slate-100 flex flex-col font-sans selection:bg-[#EF4444]/40">
      <WorkspaceBackground />

      {/* Admin Header */}
      <header className="relative z-20 shrink-0 px-6 py-3.5 border-b border-[#2A1A4E] bg-[#0D0718]/90 backdrop-blur-md flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Logo variant="full" size="md" />
          <div className="hidden md:flex items-center space-x-2 px-3 py-1 rounded-full bg-red-500/20 border border-red-500/40 text-red-400 text-[10px] font-mono font-bold uppercase tracking-wider">
            <ShieldAlert className="w-3.5 h-3.5 text-red-400" />
            <span>SYSTEM ADMINISTRATION PORTAL</span>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <div className="text-right hidden sm:block font-mono">
            <div className="text-xs font-bold text-white flex items-center space-x-1 justify-end">
              <ShieldCheck className="w-3.5 h-3.5 text-red-400" />
              <span>{user?.full_name || user?.username || 'System Administrator'}</span>
            </div>
            <div className="text-[10px] text-red-400 font-semibold">Super Administrator • Full System Scope</div>
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
        
        {/* Admin Sidebar */}
        <aside className="w-64 shrink-0 border-r border-[#2A1A4E] bg-[#0D0718]/70 backdrop-blur-md p-4 hidden lg:flex flex-col justify-between overflow-y-auto">
          <div className="space-y-1">
            <div className="px-3 py-2 text-[10px] font-mono uppercase tracking-widest text-red-400 font-bold">
              ADMINISTRATION NAVIGATION
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
                      ? 'bg-gradient-to-r from-[#6D28D9] to-[#EF4444] text-white shadow-lg shadow-red-500/20 border border-red-500/50'
                      : 'text-slate-300 hover:text-white hover:bg-[#1A0F33]'
                  }`}
                >
                  <div className="flex items-center space-x-2.5">
                    <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-red-400'}`} />
                    <span>{item.label}</span>
                  </div>
                  {item.badge && (
                    <span className="text-[9px] px-2 py-0.5 rounded-full bg-[#080512] text-red-400 border border-red-500/30">
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </div>

          <div className="p-3.5 rounded-2xl bg-[#120A24] border border-[#2A1A4E] text-[10px] font-mono text-slate-400 space-y-1">
            <div className="flex items-center space-x-1.5 text-red-400 font-bold">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>SUPER ADMIN PRIVILEGES</span>
            </div>
            <p className="leading-tight">All administrative actions are logged in immutable security audit logs.</p>
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
                    isActive ? 'bg-red-600 text-white' : 'bg-[#120A24] text-slate-300'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </div>

          <div className="animate-in fade-in slide-in-from-bottom-2 duration-300">
            {activeTab === 'dashboard' && <PredictionAnalyticsPanel />}
            {activeTab === 'patients' && <UserManagementPanel />}
            {activeTab === 'doctors' && <DoctorManagementPanel />}
            {activeTab === 'admins' && <UserManagementPanel adminOnly={true} />}
            {activeTab === 'models' && <ModelRegistry />}
            {activeTab === 'audit' && <AuditLogsPanel />}
            {activeTab === 'settings' && <AdminProfile user={user} />}
          </div>

        </main>
      </div>

    </div>
  );
}
