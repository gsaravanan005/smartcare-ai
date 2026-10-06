import React, { useState, useEffect } from 'react';
import HolographicHUDPanel from '../../components/HolographicHUDPanel';
import { adminAPI } from '../../services/api';
import CreateStaffAccountModal from './CreateStaffAccountModal';
import { Users, Search, UserCheck, ShieldAlert, KeyRound, CheckCircle2, UserX, RefreshCw, UserPlus } from 'lucide-react';

export default function UserManagementPanel({ adminOnly = false }) {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [actionMsg, setActionMsg] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);

  const fetchPatients = async () => {
    setLoading(true);
    try {
      const res = await adminAPI.listPatients();
      setPatients(res.data || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPatients();
  }, []);

  const handleStatusToggle = async (userId, currentStatus) => {
    const nextStatus = currentStatus === 'active' ? 'inactive' : 'active';
    try {
      await adminAPI.updateUserStatus(userId, nextStatus);
      setActionMsg(`User #${userId} status updated to ${nextStatus.toUpperCase()}`);
      fetchPatients();
      setTimeout(() => setActionMsg(''), 4000);
    } catch (e) {
      alert("Failed to update status");
    }
  };

  const handleResetAccess = async (userId) => {
    if (!window.confirm(`Reset password for User #${userId} to temporary default ('smartcare123')?`)) return;
    try {
      await adminAPI.resetUserPassword(userId);
      setActionMsg(`Password reset for User #${userId} to 'smartcare123'`);
      setTimeout(() => setActionMsg(''), 4000);
    } catch (e) {
      alert("Failed to reset password");
    }
  };

  const filtered = patients.filter(p => 
    !search || 
    (p.full_name || '').toLowerCase().includes(search.toLowerCase()) || 
    (p.email || '').toLowerCase().includes(search.toLowerCase()) || 
    String(p.patient_id || p.user_id || '').includes(search)
  );

  return (
    <div className="space-y-6 font-mono">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-extrabold text-white flex items-center space-x-2">
            <Users className="w-6 h-6 text-red-400" />
            <span>{adminOnly ? 'Administrator Management' : 'Patient & User Management'}</span>
          </h2>
          <p className="text-xs text-[#C084FC]">Manage accounts, toggle statuses, and handle access resets</p>
        </div>

        <div className="flex flex-col sm:flex-row items-center gap-3 w-full sm:w-auto">
          <button
            onClick={() => setIsModalOpen(true)}
            className="w-full sm:w-auto px-4 py-2 bg-gradient-to-r from-[#7C3AED] to-[#A855F7] hover:brightness-110 text-white rounded-xl text-xs font-bold flex items-center justify-center space-x-2 transition cursor-pointer shadow-lg shadow-purple-900/30"
          >
            <UserPlus className="w-4 h-4" />
            <span>Create Staff Account</span>
          </button>

          <div className="relative w-full sm:w-72">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search name, email, or ID..."
              className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl pl-10 pr-4 py-2 text-xs text-white focus:border-red-500 outline-none"
            />
          </div>
        </div>
      </div>

      {actionMsg && (
        <div className="p-3.5 rounded-xl bg-[#22C55E]/15 border border-[#22C55E]/40 text-[#22C55E] text-xs flex items-center space-x-2">
          <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
          <span>{actionMsg}</span>
        </div>
      )}

      <HolographicHUDPanel title="USER REGISTRY & RBAC AUDIT" subtitle="MANAGEMENT PORTAL" glowColor="red">
        {loading ? (
          <div className="py-12 text-center text-slate-400 text-xs animate-pulse">Loading registry data...</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-[#2A1A4E] text-[#C084FC] font-bold uppercase text-[10px] tracking-wider">
                  <th className="py-3 px-4">User ID</th>
                  <th className="py-3 px-4">Name</th>
                  <th className="py-3 px-4">Email</th>
                  <th className="py-3 px-4">BMI</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#2A1A4E]/50">
                {filtered.map((p) => (
                  <tr key={p.patient_id || p.user_id} className="hover:bg-[#120A24] transition">
                    <td className="py-3 px-4 font-bold text-white">#{p.patient_id || p.user_id}</td>
                    <td className="py-3 px-4 font-semibold text-slate-200">{p.full_name || 'Patient'}</td>
                    <td className="py-3 px-4 text-slate-400">{p.email || 'N/A'}</td>
                    <td className="py-3 px-4 text-[#C084FC]">{p.bmi ? p.bmi.toFixed(1) : 'N/A'}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase ${
                        (p.status || 'active').toLowerCase() === 'active' 
                          ? 'bg-[#22C55E]/20 text-[#22C55E] border border-[#22C55E]/40' 
                          : 'bg-red-500/20 text-red-400 border border-red-500/40'
                      }`}>
                        {p.status || 'active'}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right space-x-2">
                      <button
                        onClick={() => handleStatusToggle(p.user_id || p.patient_id, p.status || 'active')}
                        className="px-2.5 py-1 rounded-lg bg-[#1A0F33] hover:bg-[#2A1A4E] border border-[#7C3AED]/40 text-xs text-white"
                        title="Toggle Active/Inactive"
                      >
                        {(p.status || 'active').toLowerCase() === 'active' ? 'Deactivate' : 'Activate'}
                      </button>
                      <button
                        onClick={() => handleResetAccess(p.user_id || p.patient_id)}
                        className="px-2.5 py-1 rounded-lg bg-red-500/20 hover:bg-red-500/30 border border-red-500/40 text-xs text-red-300"
                        title="Reset Access Password"
                      >
                        Reset Access
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </HolographicHUDPanel>

      <CreateStaffAccountModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSuccess={() => {
          setActionMsg('Staff account provisioned successfully!');
          fetchPatients();
          setTimeout(() => setActionMsg(''), 4000);
        }}
      />
    </div>
  );
}
