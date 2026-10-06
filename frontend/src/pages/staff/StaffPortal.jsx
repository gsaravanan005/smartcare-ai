import React, { useState, useEffect } from 'react';
import Logo from '../../components/Logo';
import WorkspaceBackground from '../../components/WorkspaceBackground';
import HolographicHUDPanel from '../../components/HolographicHUDPanel';
import StaffPatientDirectory from './StaffPatientDirectory';
import { adminAPI, notificationAPI } from '../../services/api';
import { 
  Building2, 
  Users, 
  Bell, 
  Shield, 
  LogOut, 
  ClipboardList, 
  Clock, 
  CheckCircle2, 
  UserPlus, 
  Search,
  Activity
} from 'lucide-react';

export default function StaffPortal({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState('patients'); // 'patients', 'queue', 'notifications', 'audit'
  const [patients, setPatients] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchStaffData();
  }, []);

  const fetchStaffData = async () => {
    setLoading(true);
    try {
      const [patRes, notifRes] = await Promise.all([
        adminAPI.listPatients(),
        notificationAPI.getUserNotifications().catch(() => ({ data: [] }))
      ]);
      setPatients(patRes.data || []);
      setNotifications(notifRes.data || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen bg-[#080512] text-slate-100 flex flex-col font-sans selection:bg-[#7C3AED] selection:text-white">
      <WorkspaceBackground />

      {/* Header */}
      <header className="relative z-20 px-6 py-4 flex items-center justify-between border-b border-[#2A1A4E] bg-[#0D0718]/90 backdrop-blur-md">
        <div className="flex items-center space-x-4">
          <Logo variant="full" size="md" />
          <div className="h-5 w-px bg-[#2A1A4E]" />
          <div className="flex items-center space-x-2 text-xs font-mono font-bold text-[#C084FC] uppercase tracking-wider">
            <Building2 className="w-4 h-4 text-emerald-400" />
            <span>HOSPITAL STAFF & OPERATIONS PORTAL</span>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <div className="text-right hidden sm:block">
            <div className="text-xs font-bold text-white">{user?.full_name || user?.username || 'Staff User'}</div>
            <div className="text-[10px] font-mono text-emerald-400 uppercase tracking-widest">ROLE: STAFF</div>
          </div>
          <button
            onClick={onLogout}
            className="p-2 rounded-xl bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 text-red-300 text-xs font-bold flex items-center space-x-1.5 transition cursor-pointer"
          >
            <LogOut className="w-4 h-4" />
            <span className="hidden sm:inline">Logout</span>
          </button>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="relative z-20 flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 space-y-6">
        
        {/* Top Banner */}
        <div className="p-6 rounded-2xl bg-gradient-to-r from-[#120829] via-[#1A0C38] to-[#120829] border border-[#2A1A4E] shadow-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-xl sm:text-2xl font-extrabold text-white">
              Welcome to SmartCare AI Operations Desk
            </h1>
            <p className="text-xs text-[#C084FC] font-mono mt-1">
              Manage patient intake, verify registrations, track hospital queue, and review operational alerts.
            </p>
          </div>
          <div className="flex items-center space-x-3 text-xs font-mono">
            <div className="px-3 py-1.5 rounded-xl bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 flex items-center space-x-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
              <span>ACTIVE SESSION</span>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="flex space-x-2 border-b border-[#2A1A4E] pb-2 overflow-x-auto font-mono text-xs">
          <button
            onClick={() => setActiveTab('patients')}
            className={`px-4 py-2.5 rounded-xl font-bold transition flex items-center space-x-2 cursor-pointer ${
              activeTab === 'patients'
                ? 'bg-[#7C3AED] text-white shadow-lg shadow-purple-900/40'
                : 'bg-[#12082A] text-slate-400 hover:text-white border border-[#2A1A4E]'
            }`}
          >
            <Users className="w-4 h-4" />
            <span>Patient Registry ({patients.length})</span>
          </button>

          <button
            onClick={() => setActiveTab('queue')}
            className={`px-4 py-2.5 rounded-xl font-bold transition flex items-center space-x-2 cursor-pointer ${
              activeTab === 'queue'
                ? 'bg-[#7C3AED] text-white shadow-lg shadow-purple-900/40'
                : 'bg-[#12082A] text-slate-400 hover:text-white border border-[#2A1A4E]'
            }`}
          >
            <ClipboardList className="w-4 h-4" />
            <span>Hospital Queue & Triage</span>
          </button>

          <button
            onClick={() => setActiveTab('notifications')}
            className={`px-4 py-2.5 rounded-xl font-bold transition flex items-center space-x-2 cursor-pointer ${
              activeTab === 'notifications'
                ? 'bg-[#7C3AED] text-white shadow-lg shadow-purple-900/40'
                : 'bg-[#12082A] text-slate-400 hover:text-white border border-[#2A1A4E]'
            }`}
          >
            <Bell className="w-4 h-4" />
            <span>Notifications ({notifications.length})</span>
          </button>
        </div>

        {/* Tab Contents */}
        {activeTab === 'patients' && (
          <StaffPatientDirectory />
        )}

        {activeTab === 'queue' && (
          <HolographicHUDPanel title="HOSPITAL QUEUE & TRIAGE STATUS" subtitle="LIVE OPERATIONAL BOARD" glowColor="purple">
            <div className="space-y-4 font-mono text-xs">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 rounded-xl bg-[#150B33] border border-[#2B1854]">
                  <div className="text-slate-400 text-[10px] uppercase">Registered Patients Today</div>
                  <div className="text-2xl font-extrabold text-white mt-1">{patients.length}</div>
                </div>
                <div className="p-4 rounded-xl bg-[#150B33] border border-[#2B1854]">
                  <div className="text-slate-400 text-[10px] uppercase">Pending Triage Review</div>
                  <div className="text-2xl font-extrabold text-amber-400 mt-1">2</div>
                </div>
                <div className="p-4 rounded-xl bg-[#150B33] border border-[#2B1854]">
                  <div className="text-slate-400 text-[10px] uppercase">Clinician Assignments</div>
                  <div className="text-2xl font-extrabold text-emerald-400 mt-1">Active</div>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-[#0D0718] border border-[#2A1A4E] text-slate-300">
                <div className="flex items-center space-x-2 text-purple-300 font-bold mb-2">
                  <Activity className="w-4 h-4" />
                  <span>Operations Workflow Guidelines:</span>
                </div>
                <ul className="list-disc list-inside space-y-1 text-[11px] text-slate-400">
                  <li>Verify patient demographics upon initial desk check-in.</li>
                  <li>Ensure patient records contain complete contact and emergency contact details.</li>
                  <li>Direct high-risk flagged patients immediately to attending clinicians.</li>
                </ul>
              </div>
            </div>
          </HolographicHUDPanel>
        )}

        {activeTab === 'notifications' && (
          <HolographicHUDPanel title="OPERATIONAL BROADCASTS" subtitle="SYSTEM NOTIFICATIONS" glowColor="purple">
            <div className="space-y-3 font-mono text-xs">
              {notifications.length === 0 ? (
                <div className="py-8 text-center text-slate-500">No unread system notifications.</div>
              ) : (
                notifications.map((n, idx) => (
                  <div key={idx} className="p-3.5 rounded-xl bg-[#150C33] border border-[#2A1A4E] flex items-start justify-between">
                    <div>
                      <div className="font-bold text-white">{n.title}</div>
                      <div className="text-slate-400 mt-1">{n.message}</div>
                      <div className="text-[10px] text-purple-400 mt-2">{n.timestamp}</div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </HolographicHUDPanel>
        )}

      </main>
    </div>
  );
}
