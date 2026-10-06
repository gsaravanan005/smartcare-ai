import React, { useState } from 'react';
import { adminAPI } from '../../services/api';
import { 
  UserPlus, X, ShieldCheck, Stethoscope, Building, Award, 
  FileText, Phone, Mail, Lock, User, CheckCircle2, AlertCircle, Eye, EyeOff
} from 'lucide-react';

export default function CreateStaffAccountModal({ isOpen, onClose, onSuccess, defaultRole = 'DOCTOR' }) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    username: '',
    phone: '',
    staff_id: '',
    role: defaultRole,
    department: 'Cardiology & Metabolic Health',
    designation: 'Senior Attending Physician',
    specialization: 'Cardiology & Cardiovascular Medicine',
    qualification: 'MD',
    license_number: '',
    hospital: 'SmartCare AI Hospital & Medical Research Center',
    experience: 8,
    verification_status: 'approved',
    password: 'smartcare123'
  });

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMsg, setSuccessMsg] = useState(null);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleRoleSwitch = (role) => {
    setFormData(prev => ({
      ...prev,
      role: role,
      department: role === 'DOCTOR' ? 'Cardiology & Metabolic Health' : 'Hospital Operations',
      designation: role === 'DOCTOR' ? 'Senior Attending Physician' : 'Clinical Support Staff'
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccessMsg(null);

    try {
      const payload = {
        name: formData.name.trim(),
        email: formData.email.trim(),
        username: formData.username.trim() || undefined,
        phone: formData.phone.trim() || undefined,
        staff_id: formData.staff_id.trim() || undefined,
        role: formData.role,
        department: formData.department,
        designation: formData.designation,
        specialization: formData.specialization,
        qualification: formData.qualification,
        license_number: formData.license_number.trim() || undefined,
        hospital: formData.hospital.trim() || undefined,
        experience: Number(formData.experience) || 5,
        verification_status: formData.verification_status,
        password: formData.password || 'smartcare123'
      };

      const res = await adminAPI.createStaffUser(payload);
      setSuccessMsg(`Account for ${formData.name} created successfully as ${formData.role}!`);
      
      setTimeout(() => {
        if (onSuccess) onSuccess(res.data);
        onClose();
      }, 1200);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create account. Please verify details.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-black/85 backdrop-blur-md animate-fade-in font-sans overflow-y-auto">
      <div className="relative w-full max-w-2xl bg-[#0C061B] border border-[#3B1F75] rounded-3xl shadow-2xl overflow-hidden text-slate-100 my-8">
        
        {/* Modal Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-[#2A154D] bg-gradient-to-r from-[#14082B] to-[#1C0D3A]">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-2xl bg-[#7C3AED]/20 border border-[#7C3AED]/50 flex items-center justify-center text-[#C084FC] shadow-lg shadow-[#7C3AED]/20">
              {formData.role === 'DOCTOR' ? <Stethoscope className="w-5 h-5" /> : <UserPlus className="w-5 h-5" />}
            </div>
            <div>
              <h3 className="text-sm font-extrabold uppercase tracking-wider text-white">
                {formData.role === 'DOCTOR' ? 'Provision Clinical Doctor Account' : 'Create Staff Personnel Account'}
              </h3>
              <p className="text-[11px] font-mono text-[#C084FC]">
                Official SmartCare AI Healthcare Platform Identity
              </p>
            </div>
          </div>
          <button 
            type="button"
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-[#2A154D] transition cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4 font-mono text-xs max-h-[80vh] overflow-y-auto">
          
          {/* Status Banners */}
          {error && (
            <div className="p-3.5 rounded-2xl bg-red-500/20 border border-red-500/50 text-red-300 flex items-center space-x-2 animate-in fade-in">
              <AlertCircle className="w-4 h-4 text-red-400 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {successMsg && (
            <div className="p-3.5 rounded-2xl bg-emerald-500/20 border border-emerald-500/50 text-emerald-300 font-bold flex items-center space-x-2 animate-in fade-in">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
              <span>✓ {successMsg}</span>
            </div>
          )}

          {/* Role Selection Tabs */}
          <div className="grid grid-cols-2 gap-3">
            <button
              type="button"
              onClick={() => handleRoleSwitch('DOCTOR')}
              className={`p-3 rounded-2xl border text-left transition flex items-center space-x-3 cursor-pointer ${
                formData.role === 'DOCTOR'
                  ? 'bg-gradient-to-r from-[#6D28D9]/40 to-[#7C3AED]/30 border-[#A855F7] text-white shadow-lg shadow-[#7C3AED]/20'
                  : 'bg-[#120726] border-[#2A154D] text-slate-400 hover:text-slate-200'
              }`}
            >
              <Stethoscope className={`w-5 h-5 ${formData.role === 'DOCTOR' ? 'text-[#C084FC]' : 'text-slate-500'}`} />
              <div>
                <div className="font-bold font-sans text-xs">Doctor / Clinician</div>
                <div className="text-[10px] text-slate-400">Diagnosis, sign-off & patient queue</div>
              </div>
            </button>

            <button
              type="button"
              onClick={() => handleRoleSwitch('STAFF')}
              className={`p-3 rounded-2xl border text-left transition flex items-center space-x-3 cursor-pointer ${
                formData.role === 'STAFF'
                  ? 'bg-gradient-to-r from-[#6D28D9]/40 to-[#7C3AED]/30 border-[#A855F7] text-white shadow-lg shadow-[#7C3AED]/20'
                  : 'bg-[#120726] border-[#2A154D] text-slate-400 hover:text-slate-200'
              }`}
            >
              <UserPlus className={`w-5 h-5 ${formData.role === 'STAFF' ? 'text-[#C084FC]' : 'text-slate-500'}`} />
              <div>
                <div className="font-bold font-sans text-xs">Medical Staff</div>
                <div className="text-[10px] text-slate-400">Operations, intake & scheduling</div>
              </div>
            </button>
          </div>

          {/* 1. BASIC IDENTITY SECTION */}
          <div className="space-y-3 pt-2">
            <div className="text-[10px] text-[#C084FC] uppercase font-bold tracking-wider flex items-center space-x-1.5">
              <User className="w-3.5 h-3.5" />
              <span>1. Clinician Identity & Authentication</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px]">Full Name *</label>
                <input
                  type="text"
                  name="name"
                  required
                  value={formData.name}
                  onChange={handleChange}
                  placeholder={formData.role === 'DOCTOR' ? "Dr. Sarah Jenkins" : "Nurse Emma Watson"}
                  className="w-full bg-[#120726] border border-[#2A154D] rounded-xl px-3 py-2 text-xs text-white focus:border-[#7C3AED] outline-none"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px]">Official Email *</label>
                <input
                  type="email"
                  name="email"
                  required
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="doctor.jenkins@smartcare.ai"
                  className="w-full bg-[#120726] border border-[#2A154D] rounded-xl px-3 py-2 text-xs text-white focus:border-[#7C3AED] outline-none"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div>
                <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px]">Username (Optional)</label>
                <input
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  placeholder="dr_jenkins"
                  className="w-full bg-[#120726] border border-[#2A154D] rounded-xl px-3 py-2 text-xs text-white focus:border-[#7C3AED] outline-none"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px]">Phone Number</label>
                <input
                  type="text"
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                  placeholder="+1-800-555-0199"
                  className="w-full bg-[#120726] border border-[#2A154D] rounded-xl px-3 py-2 text-xs text-white focus:border-[#7C3AED] outline-none"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px]">Temporary Password</label>
                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    className="w-full bg-[#120726] border border-[#2A154D] rounded-xl px-3 py-2 text-xs text-white focus:border-[#7C3AED] outline-none pr-8"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white cursor-pointer"
                  >
                    {showPassword ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* 2. CLINICAL & CREDENTIALS SECTION (For DOCTOR Role) */}
          {formData.role === 'DOCTOR' && (
            <div className="space-y-3 pt-3 border-t border-[#2A154D]">
              <div className="text-[10px] text-[#C084FC] uppercase font-bold tracking-wider flex items-center space-x-1.5">
                <Award className="w-3.5 h-3.5" />
                <span>2. Medical Specialization & Licensing</span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {/* Specialization Dropdown */}
                <div>
                  <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px]">Medical Specialization *</label>
                  <select
                    name="specialization"
                    value={formData.specialization}
                    onChange={handleChange}
                    className="w-full bg-[#120726] border border-[#2A154D] rounded-xl px-3 py-2 text-xs text-white focus:border-[#7C3AED] outline-none cursor-pointer"
                  >
                    <option value="Cardiology & Cardiovascular Medicine">Cardiology & Cardiovascular Medicine</option>
                    <option value="Endocrinology & Diabetes Care">Endocrinology & Diabetes Care</option>
                    <option value="Nephrology & Renal Medicine">Nephrology & Renal Medicine</option>
                    <option value="Internal Medicine">Internal Medicine</option>
                    <option value="General Medicine & Primary Care">General Medicine & Primary Care</option>
                    <option value="Neurology & Neurovascular Care">Neurology & Neurovascular Care</option>
                    <option value="Pulmonology & Respiratory Care">Pulmonology & Respiratory Care</option>
                    <option value="Critical Care Medicine (ICU)">Critical Care Medicine (ICU)</option>
                    <option value="Emergency & Trauma Medicine">Emergency & Trauma Medicine</option>
                    <option value="Gastroenterology">Gastroenterology</option>
                    <option value="Clinical Oncology">Clinical Oncology</option>
                  </select>
                </div>

                {/* Department Dropdown */}
                <div>
                  <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px]">Clinical Department *</label>
                  <select
                    name="department"
                    value={formData.department}
                    onChange={handleChange}
                    className="w-full bg-[#120726] border border-[#2A154D] rounded-xl px-3 py-2 text-xs text-white focus:border-[#7C3AED] outline-none cursor-pointer"
                  >
                    <option value="Cardiology & Metabolic Health">Cardiology & Metabolic Health</option>
                    <option value="Renal & Internal Medicine">Renal & Internal Medicine</option>
                    <option value="Clinical Risk Intelligence">Clinical Risk Intelligence</option>
                    <option value="Outpatient Clinical Department">Outpatient Clinical Department</option>
                    <option value="Intensive Care Unit (ICU)">Intensive Care Unit (ICU)</option>
                    <option value="Emergency Medicine">Emergency Medicine</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {/* Qualification Dropdown */}
                <div>
                  <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px]">Medical Degree / Qualification</label>
                  <select
                    name="qualification"
                    value={formData.qualification}
                    onChange={handleChange}
                    className="w-full bg-[#120726] border border-[#2A154D] rounded-xl px-3 py-2 text-xs text-white focus:border-[#7C3AED] outline-none cursor-pointer"
                  >
                    <option value="MD">MD (Doctor of Medicine)</option>
                    <option value="MBBS">MBBS</option>
                    <option value="DO">DO (Doctor of Osteopathic Medicine)</option>
                    <option value="MS">MS (Master of Surgery)</option>
                    <option value="MD/PhD">MD / PhD</option>
                    <option value="FACC">MD, FACC</option>
                    <option value="FACP">MD, FACP</option>
                  </select>
                </div>

                {/* Medical License Number */}
                <div>
                  <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px]">License Number *</label>
                  <input
                    type="text"
                    name="license_number"
                    value={formData.license_number}
                    onChange={handleChange}
                    placeholder="MD-84920-CA"
                    className="w-full bg-[#120726] border border-[#2A154D] rounded-xl px-3 py-2 text-xs text-white focus:border-[#7C3AED] outline-none"
                  />
                </div>

                {/* Experience Dropdown */}
                <div>
                  <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px]">Years of Experience</label>
                  <select
                    name="experience"
                    value={formData.experience}
                    onChange={handleChange}
                    className="w-full bg-[#120726] border border-[#2A154D] rounded-xl px-3 py-2 text-xs text-white focus:border-[#7C3AED] outline-none cursor-pointer"
                  >
                    <option value={2}>2 Years (Junior Resident)</option>
                    <option value={5}>5 Years (Specialist)</option>
                    <option value={8}>8 Years (Senior Specialist)</option>
                    <option value={12}>12 Years (Consultant)</option>
                    <option value={18}>18+ Years (Chief of Service)</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {/* Hospital Institution */}
                <div>
                  <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px]">Hospital / Medical Center</label>
                  <input
                    type="text"
                    name="hospital"
                    value={formData.hospital}
                    onChange={handleChange}
                    placeholder="SmartCare AI Hospital & Research Center"
                    className="w-full bg-[#120726] border border-[#2A154D] rounded-xl px-3 py-2 text-xs text-white focus:border-[#7C3AED] outline-none"
                  />
                </div>

                {/* Verification Status Dropdown */}
                <div>
                  <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px]">Initial Verification Status</label>
                  <select
                    name="verification_status"
                    value={formData.verification_status}
                    onChange={handleChange}
                    className="w-full bg-[#120726] border border-[#2A154D] rounded-xl px-3 py-2 text-xs text-white focus:border-[#7C3AED] outline-none cursor-pointer"
                  >
                    <option value="approved">Approved & Active (Immediate Clearance)</option>
                    <option value="pending">Pending Credential Review</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {/* 3. STAFF SPECIFIC SECTION (For STAFF Role) */}
          {formData.role === 'STAFF' && (
            <div className="space-y-3 pt-3 border-t border-[#2A154D]">
              <div className="text-[10px] text-[#C084FC] uppercase font-bold tracking-wider flex items-center space-x-1.5">
                <Building className="w-3.5 h-3.5" />
                <span>2. Staff Role & Operations</span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px]">Staff Designation *</label>
                  <input
                    type="text"
                    name="designation"
                    value={formData.designation}
                    onChange={handleChange}
                    placeholder="Clinical Intake Coordinator"
                    className="w-full bg-[#120726] border border-[#2A154D] rounded-xl px-3 py-2 text-xs text-white focus:border-[#7C3AED] outline-none"
                  />
                </div>

                <div>
                  <label className="block text-slate-300 font-bold mb-1 uppercase text-[10px]">Operations Department</label>
                  <select
                    name="department"
                    value={formData.department}
                    onChange={handleChange}
                    className="w-full bg-[#120726] border border-[#2A154D] rounded-xl px-3 py-2 text-xs text-white focus:border-[#7C3AED] outline-none cursor-pointer"
                  >
                    <option value="Hospital Operations">Hospital Operations</option>
                    <option value="Patient Admissions & Intake">Patient Admissions & Intake</option>
                    <option value="Diagnostic Laboratory Coordination">Diagnostic Laboratory Coordination</option>
                    <option value="Clinical IT Support">Clinical IT Support</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {/* Modal Footer Actions */}
          <div className="flex items-center justify-end space-x-3 pt-4 border-t border-[#2A154D]">
            <button
              type="button"
              onClick={onClose}
              className="px-5 py-2.5 rounded-xl bg-[#15092A] hover:bg-[#200E3D] border border-[#2B144E] text-slate-300 text-xs font-bold transition cursor-pointer"
            >
              Cancel
            </button>

            <button
              type="submit"
              disabled={loading}
              className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-[#6D28D9] to-[#7C3AED] hover:brightness-110 text-white font-bold text-xs uppercase tracking-wider transition shadow-lg shadow-[#7C3AED]/25 cursor-pointer disabled:opacity-50 flex items-center space-x-2"
            >
              {loading ? (
                <>
                  <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>Provisioning Account...</span>
                </>
              ) : (
                <>
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Create {formData.role === 'DOCTOR' ? 'Doctor' : 'Staff'} Account</span>
                </>
              )}
            </button>
          </div>

        </form>
      </div>
    </div>
  );
}
