import React, { useState, useEffect } from 'react';
import HolographicHUDPanel from '../../components/HolographicHUDPanel';
import { adminAPI } from '../../services/api';
import { Users, Search, RefreshCw, UserCheck, ShieldCheck, Mail, Phone, Calendar } from 'lucide-react';

export default function StaffPatientDirectory() {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  const fetchPatients = async () => {
    setLoading(true);
    try {
      const res = await adminAPI.listPatients();
      setPatients(res.data || []);
    } catch (e) {
      console.error("Staff directory load error:", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPatients();
  }, []);

  const filtered = patients.filter(p => 
    !search || 
    (p.full_name || '').toLowerCase().includes(search.toLowerCase()) || 
    (p.email || '').toLowerCase().includes(search.toLowerCase()) || 
    String(p.patient_id || p.user_id || '').includes(search)
  );

  return (
    <div className="space-y-6 font-mono text-xs">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-extrabold text-white flex items-center space-x-2">
            <Users className="w-5 h-5 text-emerald-400" />
            <span>Hospital Patient Directory</span>
          </h2>
          <p className="text-slate-400 text-[11px]">Search registered patients and verify intake records</p>
        </div>

        <div className="flex items-center space-x-3 w-full sm:w-auto">
          <div className="relative flex-1 sm:w-64">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search by Name, Email, ID..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-3 py-2 rounded-xl bg-[#120826] border border-[#2B1854] text-white focus:outline-none focus:border-[#7C3AED]"
            />
          </div>

          <button
            onClick={fetchPatients}
            className="p-2 rounded-xl bg-[#120826] border border-[#2B1854] text-slate-300 hover:text-white cursor-pointer"
            title="Refresh Directory"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      <HolographicHUDPanel title="REGISTERED PATIENTS" subtitle={`SHOWING ${filtered.length} RECORDS`} glowColor="purple">
        {loading ? (
          <div className="py-12 flex flex-col items-center justify-center space-y-2 text-purple-400">
            <RefreshCw className="w-6 h-6 animate-spin" />
            <span>Loading patient records...</span>
          </div>
        ) : filtered.length === 0 ? (
          <div className="py-8 text-center text-slate-500">
            No matching patient records found.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-[#2A1A4E] text-slate-400 text-[10px] uppercase tracking-wider">
                  <th className="py-3 px-3">Patient ID</th>
                  <th className="py-3 px-3">Full Name</th>
                  <th className="py-3 px-3">Contact</th>
                  <th className="py-3 px-3">Age / Sex</th>
                  <th className="py-3 px-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#2A1A4E]/50 text-slate-300">
                {filtered.map((p) => (
                  <tr key={p.patient_id || p.user_id} className="hover:bg-[#150B33]/50 transition">
                    <td className="py-3 px-3 font-bold text-emerald-400">
                      #{p.patient_id || p.user_id}
                    </td>
                    <td className="py-3 px-3 font-bold text-white">
                      {p.full_name || p.username || 'Patient'}
                    </td>
                    <td className="py-3 px-3 text-slate-400">
                      <div>{p.email || 'N/A'}</div>
                      <div className="text-[10px] text-slate-500">{p.phone || 'No phone'}</div>
                    </td>
                    <td className="py-3 px-3">
                      {p.age ? `${p.age} yrs` : '--'} • {p.gender || (p.sex === 1 ? 'Male' : (p.sex === 0 ? 'Female' : '--'))}
                    </td>
                    <td className="py-3 px-3">
                      <span className="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-bold uppercase">
                        {p.status || 'Active'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </HolographicHUDPanel>
    </div>
  );
}
