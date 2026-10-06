import React, { useState, useEffect } from 'react';
import HolographicHUDPanel from '../../components/HolographicHUDPanel';
import { adminAPI } from '../../services/api';
import { Lock, Shield, CheckCircle2, XCircle, Search, RefreshCw } from 'lucide-react';

export default function AuditLogsPanel() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  const fetchLogs = async () => {
    setLoading(true);
    try {
      const res = await adminAPI.getAuditLogs(150);
      setLogs(res.data || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  const filtered = logs.filter(l => 
    !search || 
    (l.action || '').toLowerCase().includes(search.toLowerCase()) || 
    (l.role || '').toLowerCase().includes(search.toLowerCase()) ||
    (l.resource || '').toLowerCase().includes(search.toLowerCase()) ||
    String(l.user_id || '').includes(search)
  );

  return (
    <div className="space-y-6 font-mono">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-extrabold text-white flex items-center space-x-2">
            <Lock className="w-6 h-6 text-red-400" />
            <span>RBAC Security Audit Log Administration</span>
          </h2>
          <p className="text-xs text-[#C084FC]">Immutable security log recording all authentication and RBAC events</p>
        </div>

        <div className="flex items-center space-x-3 w-full sm:w-auto">
          <div className="relative flex-1 sm:w-64">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Filter action, role, resource..."
              className="w-full bg-[#0D0718] border border-[#2A1A4E] rounded-xl pl-10 pr-4 py-2 text-xs text-white focus:border-red-500 outline-none"
            />
          </div>
          <button
            onClick={fetchLogs}
            className="p-2 rounded-xl bg-[#1A0F33] hover:bg-[#2A1A4E] border border-[#7C3AED]/40 text-slate-300 hover:text-white"
            title="Refresh Logs"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      <HolographicHUDPanel title="SECURITY EVENT TRAIL" subtitle="IMMUTABLE AUDIT RECORD" glowColor="red">
        {loading ? (
          <div className="py-12 text-center text-slate-400 text-xs animate-pulse">Retrieving audit event log stream...</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-[#2A1A4E] text-[#C084FC] font-bold uppercase text-[10px] tracking-wider">
                  <th className="py-3 px-4">Timestamp</th>
                  <th className="py-3 px-4">User ID</th>
                  <th className="py-3 px-4">Role</th>
                  <th className="py-3 px-4">Action</th>
                  <th className="py-3 px-4">Resource</th>
                  <th className="py-3 px-4">IP Address</th>
                  <th className="py-3 px-4 text-right">Result</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#2A1A4E]/50">
                {filtered.map((log, idx) => {
                  const result = (log.result || 'SUCCESS').toUpperCase();
                  return (
                    <tr key={idx} className="hover:bg-[#120A24]">
                      <td className="py-3 px-4 text-slate-400 font-mono text-[11px]">
                        {log.timestamp ? new Date(log.timestamp).toLocaleString() : 'N/A'}
                      </td>
                      <td className="py-3 px-4 font-bold text-white">#{log.user_id || 'Anon'}</td>
                      <td className="py-3 px-4">
                        <span className="px-2 py-0.5 rounded-full text-[9px] font-bold uppercase bg-[#7C3AED]/20 text-[#C084FC] border border-[#7C3AED]/30">
                          {log.role || 'unauthenticated'}
                        </span>
                      </td>
                      <td className="py-3 px-4 font-bold text-slate-200">{log.action}</td>
                      <td className="py-3 px-4 text-slate-400">{log.resource || '-'}</td>
                      <td className="py-3 px-4 text-slate-400">{log.ip_address || '127.0.0.1'}</td>
                      <td className="py-3 px-4 text-right">
                        <span className={`px-2 py-0.5 rounded-full text-[9px] font-bold uppercase inline-flex items-center space-x-1 ${
                          result === 'SUCCESS'
                            ? 'bg-[#22C55E]/20 text-[#22C55E] border border-[#22C55E]/40'
                            : 'bg-red-500/20 text-red-400 border border-red-500/40'
                        }`}>
                          {result === 'SUCCESS' ? <CheckCircle2 className="w-3 h-3" /> : <XCircle className="w-3 h-3" />}
                          <span>{result}</span>
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </HolographicHUDPanel>
    </div>
  );
}
