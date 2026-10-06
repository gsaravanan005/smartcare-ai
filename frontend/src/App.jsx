import React, { useState, useEffect } from 'react';
import Logo from './components/Logo';
import WorkspaceBackground from './components/WorkspaceBackground';
import SingleLogin from './pages/SingleLogin';
import PatientRegister from './pages/PatientRegister';

import PatientPortal from './pages/patient/PatientPortal';
import DoctorPortal from './pages/doctor/DoctorPortal';
import StaffPortal from './pages/staff/StaffPortal';
import AdminPortal from './pages/admin/AdminPortal';
import { authAPI } from './services/api';

export default function App() {
  const [user, setUser] = useState(null);
  const [view, setView] = useState('login'); // 'login' or 'register'
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('smartcare_token');
      if (token) {
        try {
          const res = await authAPI.getMe();
          setUser(res.data);
        } catch (e) {
          localStorage.removeItem('smartcare_token');
          setUser(null);
        }
      }
      setLoading(false);
    };
    checkAuth();
  }, []);

  const handleLoginSuccess = (usr) => {
    setUser(usr);
  };

  const handleLogout = async () => {
    try {
      await authAPI.logout();
    } catch (e) {
      // Ignore network errors on logout
    }
    localStorage.removeItem('smartcare_token');
    setUser(null);
    setView('login');
  };

  if (loading) {
    return (
      <div className="relative min-h-screen flex flex-col items-center justify-center bg-[#080512] text-[#C084FC] font-mono text-xs">
        <WorkspaceBackground />
        <div className="relative z-10 flex flex-col items-center space-y-6">
          <Logo variant="full" size="xl" />
          <div className="w-12 h-12 rounded-full border-2 border-[#7C3AED] border-t-transparent animate-spin" />
          <div className="tracking-widest uppercase font-bold text-center text-slate-300">
            INITIALIZING SMARTCARE AI HEALTHCARE PLATFORM...
          </div>
        </div>
      </div>
    );
  }

  // -------------------------------------------------------------
  // 1. UNAUTHENTICATED STATE: Single Login or Patient Registration
  // -------------------------------------------------------------
  if (!user) {
    if (view === 'register') {
      return (
        <PatientRegister
          onRegisterSuccess={() => setView('login')}
          onSwitchToLogin={() => setView('login')}
        />
      );
    }

    return (
      <SingleLogin
        onLoginSuccess={handleLoginSuccess}
        onSwitchToRegister={() => setView('register')}
      />
    );
  }

  // -------------------------------------------------------------
  // 2. AUTHENTICATED STATE: Render Dedicated Role Portal
  // -------------------------------------------------------------
  const userRole = (user.role || 'patient').toLowerCase().trim();

  if (userRole === 'doctor' || userRole === 'clinician') {
    return <DoctorPortal user={user} onLogout={handleLogout} />;
  }

  if (userRole === 'staff') {
    return <StaffPortal user={user} onLogout={handleLogout} />;
  }

  if (userRole === 'admin' || userRole === 'super_admin') {
    return <AdminPortal user={user} onLogout={handleLogout} />;
  }

  // Default: Patient Portal
  return <PatientPortal user={user} onLogout={handleLogout} />;
}
