import React, { useState, useEffect } from 'react';
import HolographicHUDPanel from '../../components/HolographicHUDPanel';
import { adminAPI } from '../../services/api';
import CreateStaffAccountModal from './CreateStaffAccountModal';
import { UserCheck, Stethoscope, Search, CheckCircle2, XCircle, Clock, Award, UserPlus } from 'lucide-react';

export default function DoctorManagementPanel() {
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('');
  const [actionMsg, setActionMsg] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);

  const fetchDoctors = async () => {
    setLoading(true);
    try {
      const res = await adminAPI.listDoctors(statusFilter || undefined);
      setDoctors(res.data || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDoctors();
  }, [statusFilter]);

  const handleVerify = async (doctorId, newStatus) => {
    try {
      await adminAPI.verifyDoctor(doctorId, newStatus);
      setActionMsg(`Doctor #${doctorId} status updated to ${newStatus.toUpperCase()}`);
      fetchDoctors();
      setTimeout(() => setActionMsg(''), 4000);
    } catch (e) {
      alert("Failed to update doctor verification status");
    }
  };

  return (
    <div className="space-y-6 font-mono">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-extrabold text-white flex items-center space-x-2">
            <Stethoscope className="w-6 h-6 text-red-400" />
            <span>Doctor Verification & Clinical Credentialing</span>
          </h2>
          <p className="text-xs text-[#C084FC]">Provision, verify and credential clinical physician accounts</p>
        </div>

        <div className="flex items-center space-x-3 flex-wrap">
          <button
            type="button"
            onClick={() => setIsModalOpen(true)}
            className="px-4 py-2 rounded-xl bg-gradient-to-r from-[#6D28D9] to-[#7C3AED] hover:brightness-110 text-white font-bold text-xs flex items-center space-x-2 shadow-lg shadow-[#7C3AED]/20 cursor-pointer transition"
          >
            <UserPlus className="w-4 h-4" />
            <span>+ Provision Doctor Account</span>
          </button>

          <div className="flex items-center space-x-2">
            <span className="text-xs text-slate-400 font-bold uppercase">Filter:</span>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="bg-[#0D0718] border border-[#2A1A4E] rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-red-500 cursor-pointer"
            >
              <option value="">All Statuses</option>
              <option value="pending">Pending Verification</option>
              <option value="approved">Approved</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>
        </div>
      </div>

      {actionMsg && (
        <div className="p-3.5 rounded-xl bg-[#22C55E]/15 border border-[#22C55E]/40 text-[#22C55E] text-xs flex items-center space-x-2">
          <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
          <span>{actionMsg}</span>
        </div>
      )}

      <HolographicHUDPanel title="DOCTOR CREDENTIALING REGISTRY" subtitle="VERIFICATION PORTAL" glowColor="red">
        {loading ? (
          <div className="py-12 text-center text-slate-400 text-xs animate-pulse">Fetching clinician registry...</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-[#2A1A4E] text-[#C084FC] font-bold uppercase text-[10px] tracking-wider">
                  <th className="py-3 px-4">Doctor ID</th>
                  <th className="py-3 px-4">Name</th>
                  <th className="py-3 px-4">Specialization</th>
                  <th className="py-3 px-4">License Number</th>
                  <th className="py-3 px-4">Hospital</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Verification Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#2A1A4E]/50">
                {doctors.map((d) => {
                  const status = (d.verification_status || 'pending').toLowerCase();
                  return (
                    <tr key={d.doctor_id} className="hover:bg-[#120A24] transition">
                      <td className="py-3 px-4 font-bold text-white">#{d.doctor_id}</td>
                      <td className="py-3 px-4 font-semibold text-slate-200">{d.full_name || 'Dr. Practitioner'}</td>
                      <td className="py-3 px-4 text-slate-300">{d.specialization || 'General Medicine'}</td>
                      <td className="py-3 px-4 text-[#C084FC] font-bold">{d.license_number || 'LIC-000000'}</td>
                      <td className="py-3 px-4 text-slate-400">{d.hospital || 'SmartCare Hospital'}</td>
                      <td className="py-3 px-4">
                        <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase flex items-center space-x-1 w-max ${
                          status === 'approved' 
                            ? 'bg-[#22C55E]/20 text-[#22C55E] border border-[#22C55E]/40' 
                            : status === 'pending'
                            ? 'bg-amber-500/20 text-amber-400 border border-amber-500/40'
                            : 'bg-red-500/20 text-red-400 border border-red-500/40'
                        }`}>
                          {status === 'approved' && <CheckCircle2 className="w-3 h-3" />}
                          {status === 'pending' && <Clock className="w-3 h-3" />}
                          {status === 'rejected' && <XCircle className="w-3 h-3" />}
                          <span>{status}</span>
                        </span>
                      </td>
                      <td className="py-3 px-4 text-right">
                        <div className="flex items-center justify-end space-x-1.5">
                          <button
                            onClick={() => handleVerify(d.doctor_id || d.user_id, 'approved')}
                            className={`px-2.5 py-1 rounded-lg text-xs font-bold transition cursor-pointer flex items-center space-x-1 ${
                              status === 'approved'
                                ? 'bg-[#22C55E]/30 text-white border border-[#22C55E]'
                                : 'bg-[#22C55E]/10 hover:bg-[#22C55E]/20 text-[#22C55E] border border-[#22C55E]/30'
                            }`}
                            title="Approve and activate doctor credentials"
                          >
                            <CheckCircle2 className="w-3 h-3" />
                            <span>Approve</span>
                          </button>

                          <button
                            onClick={() => handleVerify(d.doctor_id || d.user_id, 'pending')}
                            className={`px-2.5 py-1 rounded-lg text-xs font-bold transition cursor-pointer flex items-center space-x-1 ${
                              status === 'pending'
                                ? 'bg-amber-500/30 text-white border border-amber-500'
                                : 'bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30'
                            }`}
                            title="Set doctor status to pending verification"
                          >
                            <Clock className="w-3 h-3" />
                            <span>Pending</span>
                          </button>

                          <button
                            onClick={() => handleVerify(d.doctor_id || d.user_id, 'rejected')}
                            className={`px-2.5 py-1 rounded-lg text-xs font-bold transition cursor-pointer flex items-center space-x-1 ${
                              status === 'rejected'
                                ? 'bg-red-500/30 text-white border border-red-500'
                                : 'bg-red-500/10 hover:bg-red-500/20 text-red-300 border border-red-500/30'
                            }`}
                            title="Reject doctor application"
                          >
                            <XCircle className="w-3 h-3" />
                            <span>Reject</span>
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </HolographicHUDPanel>

      {/* Doctor-Patient Assignment Management */}
      <DoctorPatientAssignmentSubpanel doctors={doctors} />

      {/* Provision Doctor Modal */}
      <CreateStaffAccountModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        defaultRole="DOCTOR"
        onSuccess={() => {
          fetchDoctors();
          setActionMsg('Doctor account provisioned and activated successfully!');
        }}
      />
    </div>
  );
}

function DoctorPatientAssignmentSubpanel({ doctors }) {
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedDoctorId, setSelectedDoctorId] = useState('');
  const [patientIdInput, setPatientIdInput] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [assignMsg, setAssignMsg] = useState('');

  const fetchAssignments = async () => {
    setLoading(true);
    try {
      const res = await adminAPI.getDoctorAssignments();
      setAssignments(res.data || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAssignments();
  }, []);

  const handleAssign = async (e) => {
    e.preventDefault();
    if (!selectedDoctorId || !patientIdInput) return;
    setSubmitting(true);
    try {
      const doc = doctors.find(d => String(d.doctor_id) === String(selectedDoctorId));
      await adminAPI.assignDoctorPatient({
        doctor_id: parseInt(selectedDoctorId),
        doctor_name: doc?.full_name || `Doctor #${selectedDoctorId}`,
        patient_id: parseInt(patientIdInput),
        notes: "Assigned by System Administrator"
      });
      setAssignMsg(`Patient #${patientIdInput} successfully assigned to Doctor #${selectedDoctorId}`);
      setPatientIdInput('');
      fetchAssignments();
      setTimeout(() => setAssignMsg(''), 4000);
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to assign patient to doctor");
    } finally {
      setSubmitting(false);
    }
  };

  const handleRemove = async (docId, patId) => {
    if (!window.confirm(`Remove assignment between Doctor #${docId} and Patient #${patId}?`)) return;
    try {
      await adminAPI.removeDoctorPatientAssignment(docId, patId);
      setAssignMsg(`Assignment removed successfully`);
      fetchAssignments();
      setTimeout(() => setAssignMsg(''), 4000);
    } catch (err) {
      alert("Failed to remove assignment");
    }
  };

  return (
    <HolographicHUDPanel title="CLINICAL DOCTOR-PATIENT ASSIGNMENTS" subtitle="ROSTER ACCESS CONTROL" glowColor="purple">
      <div className="space-y-4">
        {assignMsg && (
          <div className="p-3 rounded-xl bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 text-xs flex items-center space-x-2">
            <CheckCircle2 className="w-4 h-4 shrink-0" />
            <span>{assignMsg}</span>
          </div>
        )}

        {/* Assignment Form */}
        <form onSubmit={handleAssign} className="p-4 rounded-2xl bg-[#0D0718] border border-[#2A1A4E] flex flex-wrap items-end gap-3">
          <div className="space-y-1">
            <label className="text-[10px] text-[#C084FC] uppercase font-bold">Select Doctor</label>
            <select
              value={selectedDoctorId}
              onChange={(e) => setSelectedDoctorId(e.target.value)}
              className="bg-[#120A24] border border-[#3B206B] rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-[#7C3AED]"
              required
            >
              <option value="">-- Choose Doctor --</option>
              {doctors.map(d => (
                <option key={d.doctor_id} value={d.doctor_id}>
                  #{d.doctor_id} - {d.full_name || 'Dr. Specialist'} ({d.specialization || 'Clinical'})
                </option>
              ))}
            </select>
          </div>

          <div className="space-y-1">
            <label className="text-[10px] text-[#C084FC] uppercase font-bold">Patient ID #</label>
            <input
              type="number"
              value={patientIdInput}
              onChange={(e) => setPatientIdInput(e.target.value)}
              placeholder="e.g. 4 or 100"
              className="bg-[#120A24] border border-[#3B206B] rounded-xl px-3 py-2 text-xs text-white outline-none focus:border-[#7C3AED] w-36"
              required
            />
          </div>

          <button
            type="submit"
            disabled={submitting}
            className="px-4 py-2 rounded-xl bg-gradient-to-r from-[#6D28D9] to-[#7C3AED] hover:brightness-110 text-white text-xs font-bold transition cursor-pointer shadow-md"
          >
            {submitting ? 'Assigning...' : '+ Assign Patient'}
          </button>
        </form>

        {/* Existing Assignments Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-[#2A1A4E] text-[#C084FC] font-bold uppercase text-[10px] tracking-wider">
                <th className="py-2.5 px-3">Doctor</th>
                <th className="py-2.5 px-3">Patient ID</th>
                <th className="py-2.5 px-3">Status</th>
                <th className="py-2.5 px-3">Assigned Date</th>
                <th className="py-2.5 px-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#2A1A4E]/40">
              {loading ? (
                <tr><td colSpan="5" className="py-6 text-center text-slate-400">Loading assignments...</td></tr>
              ) : assignments.length === 0 ? (
                <tr><td colSpan="5" className="py-6 text-center text-slate-500">No active doctor-patient assignments found.</td></tr>
              ) : (
                assignments.map((a, idx) => (
                  <tr key={idx} className="hover:bg-[#120A24] transition">
                    <td className="py-2.5 px-3 font-semibold text-white">
                      #{a.doctor_id} - {a.doctor_name || 'Dr. Assigned'}
                    </td>
                    <td className="py-2.5 px-3 font-bold text-[#C084FC]">
                      Patient #{a.patient_id}
                    </td>
                    <td className="py-2.5 px-3">
                      <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                        {a.relationship_status || 'ASSIGNED'}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 text-slate-400 text-[11px]">
                      {a.created_at ? new Date(a.created_at).toLocaleDateString() : 'Active'}
                    </td>
                    <td className="py-2.5 px-3 text-right">
                      <button
                        onClick={() => handleRemove(a.doctor_id, a.patient_id)}
                        className="px-2.5 py-1 rounded-lg bg-red-500/20 hover:bg-red-500/30 border border-red-500/40 text-[11px] text-red-300 cursor-pointer"
                      >
                        Remove
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </HolographicHUDPanel>
  );
}
