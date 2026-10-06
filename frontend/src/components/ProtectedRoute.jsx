import React from 'react';
import HolographicHUDPanel from './HolographicHUDPanel';
import { ShieldAlert, ArrowLeft } from 'lucide-react';

export default function ProtectedRoute({ user, allowedRoles = [], children, onNavigateToRoleLanding }) {
  if (!user) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center p-6 text-center font-mono">
        <HolographicHUDPanel title="401 UNAUTHENTICATED" subtitle="ACCESS RESTRICTED" glowColor="red" className="max-w-md w-full">
          <div className="space-y-4 py-4">
            <ShieldAlert className="w-12 h-12 text-red-500 mx-auto animate-pulse" />
            <div className="text-lg font-bold text-white uppercase">Authentication Required</div>
            <p className="text-xs text-slate-300">
              Please sign in with your authorized credentials to access this portal.
            </p>
            <button
              onClick={onNavigateToRoleLanding}
              className="w-full py-2.5 rounded-xl bg-[#7C3AED] hover:bg-[#8B5CF6] text-white font-bold text-xs uppercase transition flex items-center justify-center space-x-2"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Go to Role Selection</span>
            </button>
          </div>
        </HolographicHUDPanel>
      </div>
    );
  }

  const userRole = (user.role || 'patient').toLowerCase();
  const normalizedAllowed = allowedRoles.map(r => r.toLowerCase());
  
  // Super admin can access all routes
  const isAllowed = normalizedAllowed.includes(userRole) || userRole === 'admin' || userRole === 'super_admin';

  if (!isAllowed) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center p-6 text-center font-mono">
        <HolographicHUDPanel title="403 FORBIDDEN" subtitle="ROLE ACCESS DENIED" glowColor="red" className="max-w-md w-full border-red-500/50">
          <div className="space-y-4 py-4">
            <ShieldAlert className="w-12 h-12 text-red-500 mx-auto" />
            <div className="text-lg font-bold text-white uppercase">Access Forbidden</div>
            <p className="text-xs text-slate-300">
              Your account role (<span className="text-[#C084FC] font-bold uppercase">{userRole}</span>) is not authorized to access this portal path.
            </p>
            <div className="p-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-[11px]">
              Server-side Security Enforcement Rule: 403 Forbidden
            </div>
            <button
              onClick={onNavigateToRoleLanding}
              className="w-full py-2.5 rounded-xl bg-[#7C3AED] hover:bg-[#8B5CF6] text-white font-bold text-xs uppercase transition flex items-center justify-center space-x-2"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Return to Authorized Workspace</span>
            </button>
          </div>
        </HolographicHUDPanel>
      </div>
    );
  }

  return <>{children}</>;
}
