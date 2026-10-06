import React, { useState, useEffect } from 'react';
import { reportAPI } from '../services/api';
import Logo from './Logo';
import SmartCareInteractiveReport from './SmartCareInteractiveReport';
import { 
  FileText, Download, Printer, X, CheckCircle2, ShieldAlert, Sparkles, 
  RefreshCw, Monitor, AlertCircle, RotateCcw
} from 'lucide-react';

export default function ReportViewerModal({ isOpen, onClose, predictionId, patientId, reportId: initialReportId }) {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [pdfBlobUrl, setPdfBlobUrl] = useState(null);
  const [viewMode, setViewMode] = useState('interactive'); // 'interactive' | 'pdf'
  const [downloadingPdf, setDownloadingPdf] = useState(false);

  useEffect(() => {
    if (isOpen) {
      // Prevent body scrolling behind modal while preserving layout stability
      document.body.style.overflow = 'hidden';
      fetchOrGenerateReport();
    } else {
      document.body.style.overflow = '';
      if (pdfBlobUrl) {
        URL.revokeObjectURL(pdfBlobUrl);
        setPdfBlobUrl(null);
      }
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen, predictionId, patientId, initialReportId]);

  useEffect(() => {
    let isMounted = true;
    let url = null;

    if (report?.report_id && isOpen && viewMode === 'pdf') {
      reportAPI.downloadReportBlob(report.report_id, true)
        .then((res) => {
          if (!isMounted) return;
          const blob = new Blob([res.data], { type: 'application/pdf' });
          url = URL.createObjectURL(blob);
          setPdfBlobUrl(url);
        })
        .catch((err) => {
          console.warn("[ReportViewerModal] Authenticated blob fetch error:", err);
        });
    }

    return () => {
      isMounted = false;
      if (url) {
        URL.revokeObjectURL(url);
      }
    };
  }, [report?.report_id, viewMode, isOpen]);

  const fetchOrGenerateReport = async () => {
    setLoading(true);
    setError(null);
    try {
      if (initialReportId) {
        const res = await reportAPI.getReportDetails(initialReportId);
        setReport(res.data);
      } else if (predictionId) {
        const res = await reportAPI.generateReport(predictionId);
        setReport(res.data);
      } else if (patientId) {
        const res = await reportAPI.getPatientReports(patientId);
        if (res.data && res.data.length > 0) {
          setReport(res.data[0]);
        } else {
          // Generate on-demand if no report exists
          const genRes = await reportAPI.generateReportForPatient(patientId);
          setReport(genRes.data);
        }
      }
    } catch (err) {
      console.error("[ReportViewerModal] Error loading report:", err);
      if (err.response?.status === 403) {
        setError("This health report is restricted or undergoing clinical review by your healthcare provider.");
      } else {
        setError("Failed to load clinical AI health report. Please verify clinical assessment records.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleRegenerate = async () => {
    if (!patientId && !predictionId && !report?.report_id) return;
    setLoading(true);
    setError(null);
    try {
      let res;
      if (predictionId) {
        res = await reportAPI.generateReport(predictionId);
      } else {
        res = await reportAPI.generateReportForPatient(patientId || report?.patient_id || 100);
      }
      setReport(res.data);
    } catch (err) {
      console.error("[ReportViewerModal] Error regenerating report:", err);
      setError("Failed to regenerate clinical report. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  const handleDownload = async () => {
    if (!report?.report_id) return;
    setDownloadingPdf(true);
    try {
      const res = await reportAPI.downloadReportBlob(report.report_id, false);
      const blobUrl = window.URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }));
      const a = document.createElement('a');
      a.href = blobUrl;
      a.download = report.file_name || `SmartCare_AI_Report_${report.report_id}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(() => window.URL.revokeObjectURL(blobUrl), 1500);
    } catch (e) {
      console.error("Blob download failed:", e);
      const dlUrl = reportAPI.getDownloadUrl(report.report_id, false);
      if (dlUrl) {
        window.open(dlUrl, '_blank');
      }
    } finally {
      setDownloadingPdf(false);
    }
  };

  const handlePrint = () => {
    const inlineUrl = report?.report_id ? reportAPI.getDownloadUrl(report.report_id, true) : null;
    const printTarget = pdfBlobUrl || inlineUrl;
    if (!printTarget) {
      window.print();
      return;
    }
    const printWindow = window.open(printTarget, '_blank');
    if (printWindow) {
      printWindow.focus();
      printWindow.print();
    }
  };

  const isReviewed = report?.status === "Clinician Reviewed" || report?.report_status === "Clinician Reviewed";

  return (
    <div 
      className="fixed inset-0 z-50 flex flex-col bg-[#05010D]/95 backdrop-blur-xl animate-fade-in font-sans overflow-hidden"
      role="dialog"
      aria-modal="true"
      aria-label="SmartCare AI Health Assessment Report Viewer"
    >
      {/* ========================================================================= */}
      {/* 1. REPORT TOP TOOLBAR LAYER */}
      {/* ========================================================================= */}
      <header className="relative z-30 flex items-center justify-between px-4 sm:px-6 py-3 border-b border-[#2A154D] bg-[#0D051C]/95 text-slate-100 shadow-xl flex-shrink-0">
        
        {/* Left: Branding & Report Metadata */}
        <div className="flex items-center space-x-3.5 min-w-0">
          <Logo variant="symbol" size="sm" />
          <div className="min-w-0">
            <div className="flex items-center space-x-2 flex-wrap">
              <h2 className="text-xs sm:text-sm font-extrabold uppercase tracking-wider text-white truncate">
                SMARTCARE AI HEALTH ASSESSMENT REPORT
              </h2>
              <span className={`px-2 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase ${
                isReviewed 
                  ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' 
                  : 'bg-[#7C3AED]/20 text-[#C084FC] border border-[#7C3AED]/40'
              }`}>
                {report?.status || report?.report_status || 'AI Generated'}
              </span>
            </div>
            <div className="text-[11px] font-mono text-[#C084FC] truncate">
              Report ID: <span className="text-white font-bold">{report?.report_id || 'Generating...'}</span>
              <span className="mx-2 text-slate-500">•</span>
              Patient ID: <span className="text-white font-bold">#{patientId || report?.patient_id || '100'}</span>
            </div>
          </div>
        </div>

        {/* Right: View Mode, Print, PDF & Close */}
        <div className="flex items-center space-x-2.5 flex-shrink-0">
          
          {/* Mode Switcher */}
          <div className="hidden sm:flex items-center p-0.5 bg-[#15092A] rounded-xl border border-[#2B144E] text-xs font-mono">
            <button
              onClick={() => setViewMode('interactive')}
              className={`px-3 py-1.5 rounded-lg font-bold flex items-center space-x-1.5 transition cursor-pointer ${
                viewMode === 'interactive'
                  ? 'bg-gradient-to-r from-[#6D28D9] to-[#7C3AED] text-white shadow-md'
                  : 'text-slate-300 hover:text-white'
              }`}
            >
              <Monitor className="w-3.5 h-3.5" />
              <span>Interactive Report</span>
            </button>
            <button
              onClick={() => setViewMode('pdf')}
              className={`px-3 py-1.5 rounded-lg font-bold flex items-center space-x-1.5 transition cursor-pointer ${
                viewMode === 'pdf'
                  ? 'bg-gradient-to-r from-[#6D28D9] to-[#7C3AED] text-white shadow-md'
                  : 'text-slate-300 hover:text-white'
              }`}
            >
              <FileText className="w-3.5 h-3.5" />
              <span>PDF Document</span>
            </button>
          </div>

          {/* Download PDF Button */}
          <button
            onClick={handleDownload}
            disabled={downloadingPdf || loading || !report?.report_id}
            className="px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-[#6D28D9] to-[#7C3AED] hover:brightness-110 text-white font-bold text-xs font-mono flex items-center space-x-1.5 transition shadow-lg shadow-[#7C3AED]/20 cursor-pointer disabled:opacity-40"
            title="Download PDF"
          >
            <Download className={`w-3.5 h-3.5 ${downloadingPdf ? 'animate-bounce' : ''}`} />
            <span className="hidden md:inline">{downloadingPdf ? 'Downloading...' : 'PDF'}</span>
          </button>

          {/* Print Button */}
          <button
            onClick={handlePrint}
            disabled={loading || !report?.report_id}
            className="p-2 rounded-xl bg-[#15092A] hover:bg-[#200E3D] border border-[#2B144E] text-slate-300 hover:text-white transition cursor-pointer disabled:opacity-40"
            title="Print Report"
          >
            <Printer className="w-4 h-4" />
          </button>

          {/* Regenerate Button */}
          <button
            onClick={handleRegenerate}
            disabled={loading}
            className="p-2 rounded-xl bg-[#15092A] hover:bg-[#200E3D] border border-[#2B144E] text-slate-300 hover:text-purple-300 transition cursor-pointer disabled:opacity-40"
            title="Regenerate Report"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>

          {/* Close Button */}
          <button 
            onClick={onClose}
            className="p-2 rounded-xl bg-[#1A0F33] hover:bg-red-500/20 border border-[#2A1A4E] hover:border-red-500/50 text-slate-300 hover:text-red-300 transition cursor-pointer"
            title="Close Report"
            aria-label="Close Report"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </header>

      {/* ========================================================================= */}
      {/* 2. REPORT MAIN VIEWPORT (Single Scrolling Canvas) */}
      {/* ========================================================================= */}
      <main className="relative flex-1 overflow-y-auto flex flex-col bg-[#05010D] scroll-smooth">
        
        {loading ? (
          /* Report Generation / Loading State */
          <div className="my-auto py-16 px-4 flex flex-col items-center justify-center space-y-6 text-slate-100 max-w-lg mx-auto text-center">
            <div className="relative">
              <div className="w-20 h-20 rounded-3xl bg-[#7C3AED]/20 border-2 border-[#7C3AED] flex items-center justify-center shadow-[0_0_40px_rgba(124,58,237,0.5)] animate-pulse">
                <Sparkles className="w-10 h-10 text-[#C084FC]" />
              </div>
              <div className="absolute inset-0 rounded-3xl border border-[#C084FC] animate-ping opacity-40" />
            </div>

            <div className="space-y-2">
              <h3 className="text-lg font-black uppercase tracking-wider text-white">
                SMARTCARE AI CLINICAL REPORT GENERATION
              </h3>
              <p className="text-xs font-mono text-[#C084FC]">
                Synthesizing multi-disease predictive probabilities and SHAP explainability...
              </p>
            </div>

            {/* Checklist */}
            <div className="w-full p-4 rounded-2xl bg-[#0D051C] border border-[#2A154D] text-left space-y-2 font-mono text-xs text-slate-300">
              <div className="flex items-center space-x-2 text-emerald-400">
                <CheckCircle2 className="w-4 h-4" />
                <span>Patient Profile & Biometric Vitals</span>
              </div>
              <div className="flex items-center space-x-2 text-emerald-400">
                <CheckCircle2 className="w-4 h-4" />
                <span>AI Multi-Disease Risk Ensemble</span>
              </div>
              <div className="flex items-center space-x-2 text-emerald-400">
                <CheckCircle2 className="w-4 h-4" />
                <span>SHAP Explainable Feature Attribution</span>
              </div>
              <div className="flex items-center space-x-2 text-emerald-400">
                <CheckCircle2 className="w-4 h-4" />
                <span>Personalized Wellness & Targets</span>
              </div>
              <div className="flex items-center space-x-2 text-[#C084FC] animate-pulse">
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Clinical Monitoring & Sign-Off Protocol...</span>
              </div>
            </div>
          </div>
        ) : error ? (
          /* Error State */
          <div className="my-auto py-16 px-4 flex flex-col items-center justify-center space-y-5 text-center max-w-md mx-auto">
            <div className="w-16 h-16 rounded-3xl bg-red-500/20 border border-red-500/40 text-red-400 flex items-center justify-center">
              <AlertCircle className="w-8 h-8" />
            </div>
            <div className="space-y-1.5">
              <h3 className="text-base font-bold font-mono text-white uppercase">REPORT GENERATION UNAVAILABLE</h3>
              <p className="text-xs text-slate-300">{error}</p>
            </div>
            <div className="flex items-center space-x-3">
              <button
                onClick={fetchOrGenerateReport}
                className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-[#6D28D9] to-[#7C3AED] text-white text-xs font-mono font-bold hover:brightness-110 transition shadow-lg shadow-[#7C3AED]/20 cursor-pointer flex items-center space-x-1.5"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>Retry Report</span>
              </button>
              <button
                onClick={onClose}
                className="px-5 py-2.5 rounded-xl bg-[#15092A] hover:bg-[#200E3D] border border-[#2B144E] text-slate-300 text-xs font-mono font-bold transition cursor-pointer"
              >
                Return to Dashboard
              </button>
            </div>
          </div>
        ) : viewMode === 'interactive' ? (
          /* Interactive 7-Page Canvas */
          <div className="w-full flex-1 flex flex-col">
            <SmartCareInteractiveReport
              reportData={report}
              onDownloadPdf={handleDownload}
              onPrintPdf={handlePrint}
              onRegenerate={handleRegenerate}
              onClose={onClose}
              isLoading={loading}
            />
          </div>
        ) : (
          /* Static PDF Document Viewer */
          <div className="w-full flex-1 p-4 sm:p-6 flex flex-col items-center justify-center">
            {pdfBlobUrl ? (
              <iframe
                src={`${pdfBlobUrl}#toolbar=0&navpanes=0`}
                title="SmartCare AI Health Assessment PDF Report"
                className="w-full max-w-5xl h-[calc(100vh-140px)] rounded-3xl border border-[#2A154D] bg-[#070214] shadow-2xl"
              />
            ) : (
              <div className="py-20 text-center space-y-4">
                <div className="w-12 h-12 border-4 border-[#7C3AED] border-t-transparent rounded-full animate-spin mx-auto" />
                <p className="text-xs font-mono text-slate-400">Loading authenticated PDF document stream...</p>
              </div>
            )}
          </div>
        )}

      </main>
    </div>
  );
}
