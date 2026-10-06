import React, { useState, useEffect } from 'react';
import { 
  FileText, Download, Eye, Clock, CheckCircle2, ShieldCheck, 
  AlertCircle, Sparkles, User, Calendar, Stethoscope, RefreshCw 
} from 'lucide-react';
import ReportViewerModal from '../../components/ReportViewerModal';

export default function PatientReports({ user, onNavigate }) {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedReportId, setSelectedReportId] = useState(null);
  const [isViewerOpen, setIsViewerOpen] = useState(false);
  const [downloadingId, setDownloadingId] = useState(null);

  const fetchReports = async () => {
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('token') || localStorage.getItem('smartcare_token');
      // Request reports strictly via authenticated user identity session
      const res = await fetch('/api/reports/my-reports', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (res.status === 403 || res.status === 401) {
        setError('UNAUTHORIZED');
        setReports([]);
        return;
      }

      if (!res.ok) {
        throw new Error('Failed to load health assessment reports');
      }

      const data = await res.json();
      setReports(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error('Error fetching patient reports:', err);
      setError('FAILED');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const handleDownloadPdf = async (reportId) => {
    try {
      setDownloadingId(reportId);
      const token = localStorage.getItem('token') || localStorage.getItem('smartcare_token');
      const res = await fetch(`/api/reports/${reportId}/download`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!res.ok) {
        if (res.status === 403) {
          alert('This report is not associated with your account or is under clinical review.');
        } else {
          alert('Could not download report. Please try again later.');
        }
        return;
      }

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `SmartCare_AI_Report_${reportId}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error('Download error:', err);
      alert('Error downloading report PDF.');
    } finally {
      setDownloadingId(null);
    }
  };

  const openInteractiveViewer = (reportId) => {
    setSelectedReportId(reportId);
    setIsViewerOpen(true);
  };

  if (error === 'UNAUTHORIZED') {
    return (
      <div className="max-w-2xl mx-auto my-12 p-8 rounded-3xl bg-[#120A24] border border-[#2A1A4E] text-center space-y-4">
        <div className="w-14 h-14 rounded-2xl bg-amber-500/20 border border-amber-500/40 text-amber-400 flex items-center justify-center mx-auto">
          <AlertCircle className="w-8 h-8" />
        </div>
        <h2 className="text-xl font-mono font-bold text-white">Patient Record Unavailable</h2>
        <p className="text-sm text-slate-300">This health record is not associated with your account.</p>
        <button
          onClick={() => onNavigate && onNavigate('dashboard')}
          className="px-6 py-2.5 rounded-xl bg-[#7C3AED] hover:bg-[#6D28D9] text-white text-xs font-mono font-bold transition shadow-lg shadow-[#7C3AED]/20 cursor-pointer"
        >
          Return to Dashboard
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="p-6 sm:p-8 rounded-3xl bg-gradient-to-r from-[#1A0F33] via-[#150A2A] to-[#0D0718] border border-[#2A1A4E] shadow-2xl relative overflow-hidden">
        <div className="absolute right-0 top-0 w-96 h-96 bg-[#7C3AED]/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-2">
            <div className="flex items-center space-x-2 text-[#C084FC] text-xs font-mono font-bold uppercase tracking-wider">
              <FileText className="w-4 h-4" />
              <span>OFFICIAL CLINICAL DOCUMENTATION</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              My Health Reports
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 max-w-2xl font-mono">
              Access your physician-reviewed clinical assessment reports, personalized health risk breakdowns, and multi-disease diagnostic findings.
            </p>
          </div>

          <button
            onClick={fetchReports}
            disabled={loading}
            className="self-start md:self-auto px-4 py-2 rounded-xl bg-[#1A0F33] hover:bg-[#2A1A4E] border border-[#3B206B] text-[#C084FC] text-xs font-mono font-bold flex items-center space-x-2 transition cursor-pointer"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Content Section */}
      {loading ? (
        <div className="p-12 rounded-3xl bg-[#120A24] border border-[#2A1A4E] text-center space-y-3">
          <div className="w-10 h-10 border-2 border-[#7C3AED] border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-xs font-mono text-slate-400">Loading your verified health reports...</p>
        </div>
      ) : reports.length === 0 ? (
        <div className="p-12 rounded-3xl bg-[#120A24] border border-[#2A1A4E] text-center space-y-4">
          <div className="w-16 h-16 rounded-2xl bg-[#7C3AED]/10 border border-[#7C3AED]/30 text-[#C084FC] flex items-center justify-center mx-auto">
            <FileText className="w-8 h-8 opacity-60" />
          </div>
          <div className="space-y-1">
            <h3 className="text-base font-bold text-white font-mono">No health assessment report is currently available.</h3>
            <p className="text-xs text-slate-400 max-w-md mx-auto">
              Complete your health assessment questionnaire to generate a comprehensive multi-disease risk evaluation.
            </p>
          </div>
          <button
            onClick={() => onNavigate && onNavigate('form')}
            className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-[#6D28D9] to-[#7C3AED] text-white text-xs font-mono font-bold hover:shadow-lg hover:shadow-[#7C3AED]/25 transition cursor-pointer"
          >
            Start Health Assessment
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-5">
          {reports.map((report) => {
            const isReviewed = report.report_status === 'Clinician Reviewed' || report.status === 'Clinician Reviewed';
            const isVisible = report.patient_visible !== false;
            const doctorName = report.doctor_name || report.reviewed_by || 'Assigned Healthcare Provider';
            const assessmentDate = report.assessment_date || (report.created_at ? new Date(report.created_at).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' }) : 'Recent');

            return (
              <div 
                key={report.report_id} 
                className="p-6 rounded-3xl bg-[#120A24] border border-[#2A1A4E] hover:border-[#7C3AED]/50 transition-all duration-300 shadow-xl relative group overflow-hidden"
              >
                <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
                  
                  {/* Left Report Info */}
                  <div className="space-y-3 flex-1">
                    <div className="flex flex-wrap items-center gap-2.5">
                      <span className="px-3 py-1 rounded-full bg-[#7C3AED]/20 border border-[#7C3AED]/40 text-[#C084FC] text-[11px] font-mono font-bold">
                        Report ID: {report.report_id}
                      </span>
                      
                      {isReviewed ? (
                        <span className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-[11px] font-mono font-bold flex items-center space-x-1.5">
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          <span>Clinician Reviewed</span>
                        </span>
                      ) : (
                        <span className="px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-[11px] font-mono font-bold flex items-center space-x-1.5">
                          <Clock className="w-3.5 h-3.5" />
                          <span>Under Clinical Review</span>
                        </span>
                      )}

                      <span className="text-[10px] font-mono text-slate-400">
                        v{report.report_version || '6.2.0'}
                      </span>
                    </div>

                    <div>
                      <h3 className="text-lg font-bold text-white group-hover:text-[#C084FC] transition">
                        SmartCare AI Health Assessment Report
                      </h3>
                      <div className="mt-1 flex flex-wrap items-center gap-y-1 gap-x-4 text-xs font-mono text-slate-400">
                        <div className="flex items-center space-x-1.5">
                          <Calendar className="w-3.5 h-3.5 text-[#C084FC]" />
                          <span>Assessment Date: {assessmentDate}</span>
                        </div>
                        <div className="flex items-center space-x-1.5">
                          <Stethoscope className="w-3.5 h-3.5 text-[#C084FC]" />
                          <span>Assigned Doctor: {doctorName}</span>
                        </div>
                      </div>
                    </div>

                    {!isReviewed && (
                      <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-300 text-xs font-mono flex items-start space-x-2">
                        <Clock className="w-4 h-4 mt-0.5 shrink-0" />
                        <span>Your health assessment has been generated and is currently being reviewed by your healthcare provider.</span>
                      </div>
                    )}

                    {/* Vitals Summary Strip */}
                    {report.vitals && (
                      <div className="pt-2 flex flex-wrap gap-2 text-[11px] font-mono">
                        <div className="px-2.5 py-1 rounded-lg bg-[#1A0F33] border border-[#2A1A4E] text-slate-300">
                          BMI: <span className="text-white font-bold">{report.vitals.bmi || 'N/A'}</span>
                        </div>
                        <div className="px-2.5 py-1 rounded-lg bg-[#1A0F33] border border-[#2A1A4E] text-slate-300">
                          BP: <span className="text-white font-bold">{report.vitals.sbp ? `${report.vitals.sbp}/${report.vitals.dbp}` : 'N/A'}</span>
                        </div>
                        <div className="px-2.5 py-1 rounded-lg bg-[#1A0F33] border border-[#2A1A4E] text-slate-300">
                          Glucose: <span className="text-white font-bold">{report.vitals.glucose || 'N/A'}</span>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Right Action Buttons */}
                  <div className="flex flex-col sm:flex-row lg:flex-col gap-2.5 shrink-0 justify-center">
                    {isVisible ? (
                      <>
                        <button
                          onClick={() => openInteractiveViewer(report.report_id)}
                          className="px-5 py-2.5 rounded-xl bg-[#7C3AED] hover:bg-[#6D28D9] text-white text-xs font-mono font-bold flex items-center justify-center space-x-2 transition shadow-lg shadow-[#7C3AED]/20 cursor-pointer"
                        >
                          <Eye className="w-4 h-4" />
                          <span>View Interactive Report</span>
                        </button>

                        <button
                          onClick={() => handleDownloadPdf(report.report_id)}
                          disabled={downloadingId === report.report_id}
                          className="px-5 py-2.5 rounded-xl bg-[#1A0F33] hover:bg-[#2A1A4E] border border-[#3B206B] hover:border-[#7C3AED] text-[#C084FC] hover:text-white text-xs font-mono font-bold flex items-center justify-center space-x-2 transition cursor-pointer"
                        >
                          <Download className={`w-4 h-4 ${downloadingId === report.report_id ? 'animate-bounce' : ''}`} />
                          <span>{downloadingId === report.report_id ? 'Generating PDF...' : 'View PDF'}</span>
                        </button>
                      </>
                    ) : (
                      <div className="px-5 py-2.5 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-mono font-bold flex items-center justify-center space-x-2">
                        <Clock className="w-4 h-4" />
                        <span>UNDER CLINICAL REVIEW</span>
                      </div>
                    )}
                  </div>

                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Interactive Report Modal */}
      {isViewerOpen && (
        <ReportViewerModal
          isOpen={isViewerOpen}
          onClose={() => setIsViewerOpen(false)}
          reportId={selectedReportId}
          patientId={user?.patient_profile_id || user?.id || 100}
        />
      )}
    </div>
  );
}
