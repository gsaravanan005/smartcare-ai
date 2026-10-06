import React, { useState, useEffect, useRef } from 'react';
import { 
  Heart, Activity, Brain, Shield, ShieldCheck, Sparkles, User, FileText, 
  ChevronLeft, ChevronRight, Download, Printer, Maximize2, Minimize2, 
  ZoomIn, ZoomOut, RotateCcw, AlertTriangle, CheckCircle2, Clock, 
  Stethoscope, RefreshCw, Cpu, Layers, BarChart3, Database, Lock, 
  TrendingUp, ArrowUpRight, ArrowDownRight, Compass, ShieldAlert, Zap,
  X, Check, Eye
} from 'lucide-react';
import Logo from './Logo';

export default function SmartCareInteractiveReport({ 
  reportData, 
  onDownloadPdf, 
  onPrintPdf, 
  onRegenerate,
  onClose,
  isLoading = false 
}) {
  const [currentPage, setCurrentPage] = useState(1);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [isFlipping, setIsFlipping] = useState(false);
  const [flipDirection, setFlipDirection] = useState('forward'); // 'forward' | 'backward'
  const [zoomLevel, setZoomLevel] = useState(1);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [reducedMotion, setReducedMotion] = useState(false);
  const containerRef = useRef(null);

  // Check prefers-reduced-motion
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setReducedMotion(mediaQuery.matches);
    const handler = (e) => setReducedMotion(e.matches);
    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, []);

  // Normalization of Report Data
  const data = {
    patientName: reportData?.patient_name || reportData?.patientName || "Saravan G",
    patientId: reportData?.patient_id || reportData?.patientId || "4",
    patientAge: reportData?.age || reportData?.patientAge || "21 years",
    patientDob: reportData?.dob || reportData?.date_of_birth || "2005-06-05",
    patientGender: reportData?.gender || "Male",
    patientEmail: reportData?.email || "saravanan@smartcare.ai",
    patientPhone: reportData?.phone || "Not available",
    reportId: reportData?.report_id || reportData?.reportId || "RPT_AC5D7D75",
    assessmentDate: reportData?.assessment_date || "September 10, 2026",
    doctorName: reportData?.doctor_name || "Dr. Sarah Jenkins",
    doctorLicense: reportData?.doctor_license || "MD-84920-CA",
    doctorDept: reportData?.doctor_dept || "Clinical Risk Intelligence",
    doctorSpecialty: reportData?.doctor_specialty || "Cardiology & Endocrinology",
    reportStatus: reportData?.status || reportData?.report_status || "AI GENERATED • DECISION SUPPORT",
    timestamp: reportData?.timestamp || "September 10, 2026 • 16:19 UTC",
    
    // Biomarkers
    vitals: {
      bmi: reportData?.vitals?.bmi || "20.4 kg/m²",
      bmiStatus: reportData?.vitals?.bmiStatus || "Pending",
      sbp: reportData?.vitals?.sbp || "142 mmHg",
      sbpStatus: reportData?.vitals?.sbpStatus || "Elevated",
      dbp: reportData?.vitals?.dbp || "92 mmHg",
      dbpStatus: reportData?.vitals?.dbpStatus || "Borderline",
      glucose: reportData?.vitals?.glucose || "148 mg/dL",
      glucoseStatus: reportData?.vitals?.glucoseStatus || "Pre-diabetic Range",
      cholesterol: reportData?.vitals?.cholesterol || "1 mg/dL",
      cholesterolStatus: reportData?.vitals?.cholesterolStatus || "Desirable",
      heartRate: reportData?.vitals?.heartRate || "72 bpm (Resting)",
      heartRateStatus: reportData?.vitals?.heartRateStatus || "Normal Sinus Rhythm",
    },

    // Risks
    risks: {
      diabetes: reportData?.risks?.diabetes ?? 52.8,
      diabetesTier: reportData?.risks?.diabetesTier || "Elevated",
      cvd: reportData?.risks?.cvd ?? 82.7,
      cvdTier: reportData?.risks?.cvdTier || "High Risk",
      ckd: reportData?.risks?.ckd ?? 95.3,
      ckdTier: reportData?.risks?.ckdTier || "Moderate",
    },

    // SHAP Factors
    shapFactors: reportData?.shapFactors || [
      { name: "Systolic Blood Pressure (ap_hi)", value: "142 mmHg", shap: 0.320, direction: "risk" },
      { name: "Body Mass Index (BMI)", value: "20.4 kg/m²", shap: 0.240, direction: "risk" },
      { name: "Patient Age", value: "21 yrs", shap: 0.190, direction: "risk" },
      { name: "Fasting Blood Glucose", value: "148 mg/dL", shap: -0.150, direction: "risk" },
      { name: "Physical Activity Routine", value: "Active", shap: -0.220, direction: "protective" },
      { name: "Non-Smoking Status", value: "Non-smoker", shap: -0.150, direction: "protective" }
    ]
  };

  const pagesInfo = [
    { num: 1, title: "1 Executive Cover", subtitle: "Platform Overview & Patient Identification" },
    { num: 2, title: "2 Patient Profile & Vitals", subtitle: "Biometric Baseline & Clinical History" },
    { num: 3, title: "3 AI Health Risk Ensemble", subtitle: "Multi-Disease Probability & Stratification" },
    { num: 4, title: "4 Explainable AI (XAI)", subtitle: "SHAP Feature Importance & Attribution" },
    { num: 5, title: "5 Personalized Wellness", subtitle: "Lifestyle Interventions & Targets" },
    { num: 6, title: "6 Clinical Decision Support", subtitle: "Diagnostic Synthesis & Surveillance" },
    { num: 7, title: "7 AI Safety & Sign-Off", subtitle: "Model Registry & Clinician Review" }
  ];

  const handlePageChange = (newPage) => {
    if (newPage < 1 || newPage > 7 || newPage === currentPage || isTransitioning || isFlipping) return;
    
    const direction = newPage > currentPage ? 'forward' : 'backward';
    setFlipDirection(direction);

    if (reducedMotion) {
      setCurrentPage(newPage);
      return;
    }

    setIsFlipping(true);
    setIsTransitioning(true);
    setTimeout(() => {
      setCurrentPage(newPage);
      setTimeout(() => {
        setIsFlipping(false);
        setIsTransitioning(false);
      }, 350);
    }, 280);
  };

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'ArrowRight' || e.key === 'PageDown') {
        handlePageChange(currentPage + 1);
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        handlePageChange(currentPage - 1);
      } else if (e.key === 'Escape' && onClose) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentPage, isTransitioning, isFlipping, reducedMotion, onClose]);

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      containerRef.current?.requestFullscreen?.();
      setIsFullscreen(true);
    } else {
      document.exitFullscreen?.();
      setIsFullscreen(false);
    }
  };

  return (
    <div 
      ref={containerRef}
      className="relative w-full flex flex-col bg-[#05010D] text-slate-100 font-sans"
    >
      {/* ========================================================================= */}
      {/* 1. HORIZONTAL PAGE NAVIGATION STRIP (With Direct Actions & Close) */}
      {/* ========================================================================= */}
      <nav 
        aria-label="Report Section Navigation"
        className="sticky top-0 z-40 px-3 sm:px-6 py-2 bg-[#0B0418]/95 backdrop-blur-md border-b border-[#2A154D] flex items-center justify-between gap-3 text-xs font-mono flex-shrink-0 shadow-lg"
      >
        {/* Horizontal Navigation Pills with smooth scrolling */}
        <div className="flex items-center space-x-1.5 overflow-x-auto py-1 scrollbar-thin max-w-full flex-1">
          {pagesInfo.map((p) => {
            const isActive = currentPage === p.num;
            return (
              <button
                key={p.num}
                onClick={() => handlePageChange(p.num)}
                className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all duration-300 flex items-center space-x-2 cursor-pointer whitespace-nowrap flex-shrink-0 ${
                  isActive 
                    ? 'bg-gradient-to-r from-[#6D28D9] via-[#7C3AED] to-[#A855F7] text-white shadow-lg shadow-[#7C3AED]/30 border border-[#C084FC]' 
                    : 'bg-[#120726] hover:bg-[#1C0D3A] text-slate-300 hover:text-white border border-[#2B144E]'
                }`}
                title={p.subtitle}
                aria-current={isActive ? 'page' : undefined}
              >
                <span className={`w-4 h-4 rounded-full flex items-center justify-center text-[10px] font-black ${
                  isActive ? 'bg-white text-[#581C87]' : 'bg-[#250F4D] text-[#C084FC]'
                }`}>
                  {p.num}
                </span>
                <span>{p.title.substring(2)}</span>
              </button>
            );
          })}
        </div>

        {/* Direct Action Controls: Download PDF, Print, Zoom, Fullscreen & Close */}
        <div className="flex items-center space-x-2 flex-shrink-0">
          
          {/* Zoom Controls */}
          <div className="hidden xl:flex items-center space-x-1 bg-[#120726] border border-[#2B144E] rounded-xl p-0.5">
            <button
              onClick={() => setZoomLevel(prev => Math.max(0.75, Number((prev - 0.05).toFixed(2))))}
              className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-[#200E3D] transition cursor-pointer"
              title="Zoom Out"
            >
              <ZoomOut className="w-3.5 h-3.5" />
            </button>
            <span className="px-1.5 text-[11px] text-[#C084FC] font-semibold">{Math.round(zoomLevel * 100)}%</span>
            <button
              onClick={() => setZoomLevel(prev => Math.min(1.3, Number((prev + 0.05).toFixed(2))))}
              className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-[#200E3D] transition cursor-pointer"
              title="Zoom In"
            >
              <ZoomIn className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => setZoomLevel(1)}
              className="px-2 py-0.5 text-[10px] text-slate-400 hover:text-white hover:bg-[#200E3D] rounded-lg transition cursor-pointer"
              title="Fit Width / Reset"
            >
              Fit
            </button>
          </div>

          <button
            onClick={toggleFullscreen}
            className="p-1.5 rounded-xl bg-[#120726] hover:bg-[#200E3D] border border-[#2B144E] text-slate-300 hover:text-white transition cursor-pointer"
            title="Toggle Fullscreen"
          >
            {isFullscreen ? <Minimize2 className="w-3.5 h-3.5" /> : <Maximize2 className="w-3.5 h-3.5" />}
          </button>

          {/* Download PDF Button */}
          {onDownloadPdf && (
            <button
              type="button"
              onClick={onDownloadPdf}
              className="px-3 py-1.5 rounded-xl bg-gradient-to-r from-[#6D28D9] to-[#7C3AED] hover:brightness-110 text-white font-bold text-xs flex items-center space-x-1.5 shadow-md shadow-[#7C3AED]/20 cursor-pointer transition"
              title="Download PDF Document"
            >
              <Download className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Download PDF</span>
            </button>
          )}

          {/* Print Button */}
          {onPrintPdf && (
            <button
              type="button"
              onClick={onPrintPdf}
              className="p-1.5 rounded-xl bg-[#120726] hover:bg-[#200E3D] border border-[#2B144E] text-slate-300 hover:text-white transition cursor-pointer"
              title="Print Clinical Report"
            >
              <Printer className="w-3.5 h-3.5" />
            </button>
          )}

          {/* Direct Close Button */}
          {onClose && (
            <button
              type="button"
              onClick={onClose}
              className="px-3 py-1.5 rounded-xl bg-red-500/20 hover:bg-red-500/30 border border-red-500/40 text-red-300 hover:text-white font-bold text-xs flex items-center space-x-1.5 transition cursor-pointer"
              title="Close Report (Esc)"
              aria-label="Close Report"
            >
              <X className="w-4 h-4" />
              <span>Close</span>
            </button>
          )}
        </div>
      </nav>

      {/* ========================================================================= */}
      {/* 2. REPORT CANVAS (Continuous Theme Background & 3D Book Flip Viewport) */}
      {/* ========================================================================= */}
      <div 
        className="relative flex-1 p-3 sm:p-6 flex flex-col items-center justify-start bg-[#05010D]"
        style={{ perspective: '2000px' }}
      >
        
        {/* Background Ambient Lighting & Continuous IT Geometry */}
        <div className="absolute inset-0 pointer-events-none opacity-35 overflow-hidden">
          <div className="absolute top-1/6 left-1/4 w-[600px] h-[600px] bg-[#6D28D9]/15 rounded-full blur-3xl" />
          <div className="absolute bottom-1/4 right-1/4 w-[600px] h-[600px] bg-[#9333EA]/15 rounded-full blur-3xl" />
          <svg className="w-full h-full opacity-20" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <pattern id="canvas-grid" width="48" height="48" patternUnits="userSpaceOnUse">
                <path d="M 48 0 L 0 0 0 48" fill="none" stroke="#7C3AED" strokeWidth="0.5" strokeOpacity="0.3" />
                <circle cx="48" cy="48" r="1.5" fill="#A855F7" fillOpacity="0.5" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#canvas-grid)" />
          </svg>
        </div>

        {/* Side Book Turn Click Zones on Desktop */}
        {currentPage > 1 && (
          <button
            onClick={() => handlePageChange(currentPage - 1)}
            className="hidden 2xl:flex fixed left-6 top-1/2 -translate-y-1/2 z-30 p-3 rounded-full bg-[#120726]/80 hover:bg-[#7C3AED]/40 border border-[#2B144E] text-[#C084FC] hover:text-white transition shadow-xl cursor-pointer group items-center space-x-1"
            title={`Turn to Page ${currentPage - 1}`}
          >
            <ChevronLeft className="w-6 h-6 group-hover:-translate-x-0.5 transition" />
          </button>
        )}

        {currentPage < 7 && (
          <button
            onClick={() => handlePageChange(currentPage + 1)}
            className="hidden 2xl:flex fixed right-6 top-1/2 -translate-y-1/2 z-30 p-3 rounded-full bg-[#120726]/80 hover:bg-[#7C3AED]/40 border border-[#2B144E] text-[#C084FC] hover:text-white transition shadow-xl cursor-pointer group items-center space-x-1"
            title={`Turn to Page ${currentPage + 1}`}
          >
            <ChevronRight className="w-6 h-6 group-hover:translate-x-0.5 transition" />
          </button>
        )}

        {/* ========================================================================= */}
        {/* 3. A4 REPORT DOCUMENT PAGE CONTAINER (With 3D Book Page Flip Effect) */}
        {/* ========================================================================= */}
        <article 
          className={`relative z-10 w-full max-w-[860px] rounded-3xl border border-[#3B1F75] bg-gradient-to-b from-[#080214] via-[#0A0318] to-[#070214] text-slate-100 shadow-[0_0_50px_rgba(124,58,237,0.22)] overflow-hidden flex flex-col my-2 transition-transform duration-300 ${
            isFlipping && !reducedMotion 
              ? (flipDirection === 'forward' ? 'animate-book-flip-forward' : 'animate-book-flip-backward') 
              : ''
          }`}
          style={{
            minHeight: '1120px',
            transform: zoomLevel !== 1 ? `scale(${zoomLevel})` : undefined,
            transformOrigin: 'top center',
            transformStyle: 'preserve-3d'
          }}
        >
          {/* Subtle Book Spine Crease Down Left Border */}
          <div className="absolute top-0 bottom-0 left-0 w-3.5 bg-gradient-to-r from-[#030008]/90 via-[#1A0A33]/70 to-transparent pointer-events-none z-30 border-r border-[#3B1F75]/30" />

          {/* Book Page Corner Turn Indicator */}
          {currentPage < 7 && (
            <div 
              onClick={() => handlePageChange(currentPage + 1)}
              className="absolute top-0 right-0 w-12 h-12 z-30 cursor-pointer group pointer-events-auto"
              title="Click to flip to next page"
            >
              <div className="absolute top-0 right-0 w-0 h-0 border-t-[32px] border-t-[#7C3AED]/40 border-l-[32px] border-l-transparent group-hover:border-t-[#A855F7] transition" />
            </div>
          )}

          {/* Universal Watermark Layer on Every Page */}
          <SmartCareWatermark />

          {/* PAGE HEADER (PAGES 2–7) */}
          {currentPage > 1 && (
            <header className="relative z-20 px-8 pt-6 pb-4 border-b border-[#2D1457]/80 flex items-center justify-between">
              <div className="flex items-center space-x-3.5">
                <Logo variant="full" size="sm" />
                <div>
                  <div className="text-xs font-mono font-bold text-[#C084FC] uppercase tracking-wider">
                    Healthcare Intelligence & IT Platform
                  </div>
                  <div className="text-[10px] text-slate-400 font-mono">
                    Official Clinical Health Assessment Report
                  </div>
                </div>
              </div>
              <div className="text-right font-mono">
                <div className="text-[11px] font-bold text-white">Patient #{data.patientId} • {data.patientName}</div>
                <div className="text-[10px] text-[#A78BFA]">Report: {data.reportId} | {data.assessmentDate}</div>
              </div>
            </header>
          )}

          {/* PAGE MAIN CONTENT */}
          <div className="relative z-20 flex-1 p-6 sm:p-8 flex flex-col justify-between space-y-6">
            
            {/* ========================================================================= */}
            {/* PAGE 1 — EXECUTIVE COVER */}
            {/* ========================================================================= */}
            {currentPage === 1 && (
              <div className="flex-1 flex flex-col justify-between space-y-6 animate-fade-in">
                
                {/* Cover Header */}
                <div className="flex items-center justify-between border-b border-[#2E145C] pb-5">
                  <div className="flex items-center space-x-3">
                    <Logo variant="full" size="md" />
                    <div className="hidden sm:block">
                      <div className="text-xs font-mono text-[#C084FC] uppercase font-bold tracking-wider">
                        CLINICAL OPERATING SYSTEM
                      </div>
                    </div>
                  </div>
                  <div className="text-right text-xs font-mono text-[#C084FC] font-semibold">
                    <div>Predict. Prevent. Personalize.</div>
                    <div className="text-[10px] text-slate-400">Healthier Lives Through AI</div>
                  </div>
                </div>

                {/* Hero Platform Banner */}
                <div className="relative rounded-3xl p-6 sm:p-8 bg-gradient-to-br from-[#1A0A38] via-[#110526] to-[#1E0B3D] border border-[#7C3AED]/70 shadow-[0_0_35px_rgba(124,58,237,0.25)] overflow-hidden">
                  <div className="absolute -right-10 -bottom-10 w-72 h-72 opacity-25 pointer-events-none">
                    <img src="/human_anatomical_hologram.png" alt="Digital Health Twin" className="w-full h-full object-contain" />
                  </div>
                  
                  <div className="relative z-10 max-w-xl space-y-3">
                    <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-[#7C3AED]/20 border border-[#A855F7]/50 text-[#E9D5FF] text-[10px] font-mono font-bold uppercase tracking-wider">
                      <Sparkles className="w-3 h-3 text-[#C084FC]" />
                      <span>NEXT-GEN HEALTHCARE INTELLIGENCE</span>
                    </div>

                    <h1 className="text-2xl sm:text-3xl font-black tracking-tight text-white uppercase leading-tight">
                      AI-POWERED HEALTHCARE INTELLIGENCE PLATFORM
                    </h1>

                    <p className="text-xs font-mono font-bold text-[#C084FC]">
                      Comprehensive Multi-Disease Predictive Assessment & Clinical Report
                    </p>

                    <p className="text-xs text-slate-300 leading-relaxed max-w-lg font-sans">
                      SmartCare AI unifies machine learning risk prediction, explainable game-theoretic attribution (SHAP), 
                      evidence-based clinical decision support, and personalized lifestyle medicine into an enterprise clinical document.
                    </p>
                  </div>
                </div>

                {/* 6 Platform Capabilities */}
                <div className="space-y-2.5">
                  <div className="text-xs font-mono font-bold uppercase tracking-wider text-[#C084FC] flex items-center space-x-2">
                    <div className="w-2 h-2 rounded-full bg-[#7C3AED] animate-pulse" />
                    <span>SMARTCARE AI PLATFORM CORE CAPABILITIES</span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                    {[
                      { icon: Activity, title: "AI Health Risk Prediction", desc: "Multi-disease gradient-boosted ensemble probabilities." },
                      { icon: Brain, title: "Explainable AI (XAI)", desc: "Exact SHAP game-theoretic biomarker feature contributions." },
                      { icon: Stethoscope, title: "Clinical Decision Support", desc: "Stratified risk protocols assisting physician decision-making." },
                      { icon: Heart, title: "Personalized Wellness", desc: "Targeted metabolic, nutritional, and physical interventions." },
                      { icon: TrendingUp, title: "Patient Health Monitoring", desc: "Longitudinal surveillance and physiological target tracking." },
                      { icon: ShieldCheck, title: "Secure Healthcare IT", desc: "Strict three-level RBAC data isolation & compliance." }
                    ].map((cap, idx) => {
                      const Icon = cap.icon;
                      return (
                        <div 
                          key={idx} 
                          className="p-3.5 rounded-2xl bg-[#12072E]/90 border border-[#3B1F75] hover:border-[#7C3AED] transition flex flex-col justify-between space-y-1.5 shadow-sm"
                        >
                          <div className="flex items-center space-x-2.5">
                            <div className="w-7 h-7 rounded-xl bg-[#250F52] flex items-center justify-center text-[#C084FC] border border-[#581C87]">
                              <Icon className="w-3.5 h-3.5" />
                            </div>
                            <span className="text-xs font-bold text-white">{cap.title}</span>
                          </div>
                          <p className="text-[10px] text-slate-300 leading-snug">{cap.desc}</p>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Patient Health Assessment Identification Panel */}
                <div className="space-y-2">
                  <div className="text-xs font-mono font-bold uppercase tracking-wider text-[#E9D5FF] flex items-center space-x-2">
                    <User className="w-3.5 h-3.5 text-[#A855F7]" />
                    <span>PATIENT HEALTH ASSESSMENT IDENTIFICATION</span>
                  </div>

                  <div className="rounded-2xl p-4 bg-[#11052B] border border-[#581C87] grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs font-mono">
                    <div>
                      <div className="text-[9px] text-[#A78BFA] uppercase font-bold">PATIENT NAME</div>
                      <div className="text-xs font-bold text-white mt-0.5">{data.patientName}</div>
                    </div>
                    <div>
                      <div className="text-[9px] text-[#A78BFA] uppercase font-bold">PATIENT ID</div>
                      <div className="text-xs font-bold text-[#C084FC] mt-0.5">#{data.patientId}</div>
                    </div>
                    <div>
                      <div className="text-[9px] text-[#A78BFA] uppercase font-bold">AGE & GENDER</div>
                      <div className="text-xs font-bold text-white mt-0.5">{data.patientAge} • {data.patientGender}</div>
                    </div>
                    <div>
                      <div className="text-[9px] text-[#A78BFA] uppercase font-bold">ASSESSMENT DATE</div>
                      <div className="text-xs font-bold text-white mt-0.5">{data.assessmentDate}</div>
                    </div>
                    <div>
                      <div className="text-[9px] text-[#A78BFA] uppercase font-bold">REPORT ID</div>
                      <div className="text-xs font-bold text-[#E9D5FF] mt-0.5">{data.reportId}</div>
                    </div>
                    <div>
                      <div className="text-[9px] text-[#A78BFA] uppercase font-bold">ASSIGNED DOCTOR</div>
                      <div className="text-xs font-bold text-white mt-0.5">{data.doctorName}</div>
                    </div>
                    <div>
                      <div className="text-[9px] text-[#A78BFA] uppercase font-bold">DEPARTMENT</div>
                      <div className="text-xs font-bold text-white mt-0.5">{data.doctorDept}</div>
                    </div>
                    <div>
                      <div className="text-[9px] text-[#A78BFA] uppercase font-bold">REPORT STATUS</div>
                      <div className="text-xs font-bold text-emerald-400 mt-0.5">{data.reportStatus}</div>
                    </div>
                  </div>
                </div>

              </div>
            )}

            {/* ========================================================================= */}
            {/* PAGE 2 — PATIENT PROFILE & BIOMETRIC VITALS */}
            {/* ========================================================================= */}
            {currentPage === 2 && (
              <div className="flex-1 flex flex-col justify-between space-y-5 animate-fade-in">
                <SectionHeader number="2" title="PATIENT PROFILE & CLINICAL BIOMETRICS" subtitle="SECTION 2 — DEMOGRAPHIC BASELINE, PHYSIOLOGICAL MEASUREMENTS & HISTORY" />

                {/* Identity & Vitals Grid */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  
                  {/* Demographic Details */}
                  <div className="p-4 rounded-2xl bg-[#11052B] border border-[#3B1F75] space-y-3 font-mono text-xs">
                    <div className="text-xs font-bold text-[#C084FC] uppercase flex items-center space-x-2 border-b border-[#2D1457] pb-2">
                      <User className="w-3.5 h-3.5 text-[#C084FC]" />
                      <span>Demographic Profile</span>
                    </div>
                    <div className="space-y-2">
                      <div className="flex justify-between"><span className="text-slate-400">Full Name:</span><span className="text-white font-bold">{data.patientName}</span></div>
                      <div className="flex justify-between"><span className="text-slate-400">Patient ID:</span><span className="text-[#C084FC] font-bold">#{data.patientId}</span></div>
                      <div className="flex justify-between"><span className="text-slate-400">Date of Birth:</span><span className="text-white">{data.patientDob}</span></div>
                      <div className="flex justify-between"><span className="text-slate-400">Age:</span><span className="text-white">{data.patientAge}</span></div>
                      <div className="flex justify-between"><span className="text-slate-400">Gender:</span><span className="text-white">{data.patientGender}</span></div>
                      <div className="flex justify-between"><span className="text-slate-400">Contact Email:</span><span className="text-white truncate max-w-[180px]">{data.patientEmail}</span></div>
                    </div>
                  </div>

                  {/* Attending Clinical Physician */}
                  <div className="p-4 rounded-2xl bg-[#11052B] border border-[#3B1F75] space-y-3 font-mono text-xs">
                    <div className="text-xs font-bold text-[#C084FC] uppercase flex items-center space-x-2 border-b border-[#2D1457] pb-2">
                      <Stethoscope className="w-3.5 h-3.5 text-[#C084FC]" />
                      <span>Clinical Care Team</span>
                    </div>
                    <div className="space-y-2">
                      <div className="flex justify-between"><span className="text-slate-400">Attending Doctor:</span><span className="text-white font-bold">{data.doctorName}</span></div>
                      <div className="flex justify-between"><span className="text-slate-400">License Number:</span><span className="text-[#D8B4FE] font-bold">{data.doctorLicense}</span></div>
                      <div className="flex justify-between"><span className="text-slate-400">Clinical Specialty:</span><span className="text-white">{data.doctorSpecialty}</span></div>
                      <div className="flex justify-between"><span className="text-slate-400">Department:</span><span className="text-white">{data.doctorDept}</span></div>
                      <div className="flex justify-between"><span className="text-slate-400">Assessment Date:</span><span className="text-white">{data.assessmentDate}</span></div>
                      <div className="flex justify-between"><span className="text-slate-400">Surveillance Status:</span><span className="text-emerald-400 font-bold">Active Protocol</span></div>
                    </div>
                  </div>
                </div>

                {/* Biometric Dashboard Cards */}
                <div className="space-y-2">
                  <div className="text-xs font-mono font-bold text-[#E9D5FF] flex items-center space-x-1.5">
                    <Activity className="w-3.5 h-3.5 text-[#C084FC]" />
                    <span>Recorded Clinical Biomarkers</span>
                  </div>

                  <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2.5 font-mono">
                    {[
                      { label: "BMI", val: data.vitals.bmi, status: data.vitals.bmiStatus, isGood: true },
                      { label: "Systolic BP", val: data.vitals.sbp, status: data.vitals.sbpStatus, isAlert: true },
                      { label: "Diastolic BP", val: data.vitals.dbp, status: data.vitals.dbpStatus, isWarn: true },
                      { label: "Glucose", val: data.vitals.glucose, status: data.vitals.glucoseStatus, isWarn: true },
                      { label: "Cholesterol", val: data.vitals.cholesterol, status: data.vitals.cholesterolStatus, isGood: true },
                      { label: "Heart Rate", val: data.vitals.heartRate, status: "Normal Sinus", isGood: true },
                    ].map((item, i) => (
                      <div key={i} className="p-3 rounded-2xl bg-[#0F0424] border border-[#3B1F75] space-y-1 text-center">
                        <div className="text-[10px] text-[#A78BFA] uppercase font-bold">{item.label}</div>
                        <div className="text-sm font-black text-white">{item.val}</div>
                        <span className={`px-2 py-0.5 rounded-full text-[9px] font-bold block truncate ${
                          item.isAlert ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40' :
                          item.isWarn ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' :
                          'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                        }`}>
                          {item.status}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Clinical History & Lifestyle Factors */}
                <div className="p-4 rounded-2xl bg-[#11052B] border border-[#3B1F75] space-y-3 font-mono text-xs">
                  <div className="text-xs font-bold text-[#C084FC] uppercase flex items-center space-x-2 border-b border-[#2D1457] pb-2">
                    <Shield className="w-3.5 h-3.5 text-[#C084FC]" />
                    <span>Clinical History & Lifestyle Factors</span>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <div className="p-2.5 rounded-xl bg-[#0A0217] border border-[#2A154D]">
                      <div className="text-[9px] text-[#A78BFA] uppercase">Smoking Status</div>
                      <div className="text-white font-bold text-xs mt-0.5">Non-smoker</div>
                    </div>
                    <div className="p-2.5 rounded-xl bg-[#0A0217] border border-[#2A154D]">
                      <div className="text-[9px] text-[#A78BFA] uppercase">Physical Activity</div>
                      <div className="text-white font-bold text-xs mt-0.5">Moderate (150+ min/wk)</div>
                    </div>
                    <div className="p-2.5 rounded-xl bg-[#0A0217] border border-[#2A154D]">
                      <div className="text-[9px] text-[#A78BFA] uppercase">Active Medications</div>
                      <div className="text-white font-bold text-xs mt-0.5">None Reported</div>
                    </div>
                  </div>
                </div>

              </div>
            )}

            {/* ========================================================================= */}
            {/* PAGE 3 — AI HEALTH RISK ENSEMBLE */}
            {/* ========================================================================= */}
            {currentPage === 3 && (
              <div className="flex-1 flex flex-col justify-between space-y-5 animate-fade-in">
                <SectionHeader number="3" title="AI HEALTH RISK ASSESSMENT & MULTI-DISEASE ENSEMBLE" subtitle="SECTION 3 — PREDICTIVE MODEL PROBABILITIES & RISK STRATIFICATION" />

                {/* 3 Risk Gauges */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  {[
                    { name: "Diabetes Mellitus", pct: data.risks.diabetes, tier: data.risks.diabetesTier, color: "#C084FC", stroke: "#A855F7" },
                    { name: "Cardiovascular (CVD)", pct: data.risks.cvd, tier: data.risks.cvdTier, color: "#F43F5E", stroke: "#F43F5E" },
                    { name: "Chronic Kidney (CKD)", pct: data.risks.ckd, tier: data.risks.ckdTier, color: "#38BDF8", stroke: "#38BDF8" }
                  ].map((gauge, i) => {
                    const radius = 38;
                    const circumference = 2 * Math.PI * radius;
                    const offset = circumference - (gauge.pct / 100) * circumference;

                    return (
                      <div key={i} className="p-4 rounded-2xl bg-[#11052B] border border-[#4C1D95] flex flex-col items-center justify-center space-y-2 shadow-inner">
                        <div className="text-xs font-bold text-white text-center font-mono">{gauge.name}</div>
                        
                        <div className="relative w-28 h-28 flex items-center justify-center">
                          <svg className="w-full h-full -rotate-90">
                            <circle cx="56" cy="56" r={radius} fill="transparent" stroke="#220D47" strokeWidth="9" />
                            <circle 
                              cx="56" cy="56" r={radius} 
                              fill="transparent" 
                              stroke={gauge.stroke} 
                              strokeWidth="9"
                              strokeDasharray={circumference}
                              strokeDashoffset={offset}
                              strokeLinecap="round"
                              className="transition-all duration-1000 ease-out"
                            />
                          </svg>
                          <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
                            <span className="text-xl font-black text-white font-mono">{gauge.pct}%</span>
                          </div>
                        </div>

                        <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase ${
                          gauge.tier.includes('High') ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40' :
                          gauge.tier.includes('Elevated') ? 'bg-purple-500/20 text-purple-300 border border-purple-500/40' :
                          'bg-sky-500/20 text-sky-300 border border-sky-500/40'
                        }`}>
                          Tier: {gauge.tier}
                        </span>
                      </div>
                    );
                  })}
                </div>

                {/* Risk Spectrum Bars */}
                <div className="rounded-2xl p-4 bg-[#11052B] border border-[#4C1D95] space-y-3 font-mono">
                  <div className="flex justify-between items-center text-xs font-bold text-[#E9D5FF]">
                    <span>Comparative Risk Spectrum</span>
                    <span className="text-[10px] text-slate-400">Calibrated Multi-Model Ensemble</span>
                  </div>
                  <div className="space-y-3 pt-1">
                    {[
                      { label: "Diabetes Mellitus", pct: data.risks.diabetes, barColor: "from-[#8B5CF6] to-[#C084FC]" },
                      { label: "Cardiovascular (CVD)", pct: data.risks.cvd, barColor: "from-[#E11D48] to-[#F43F5E]" },
                      { label: "Chronic Kidney (CKD)", pct: data.risks.ckd, barColor: "from-[#0284C7] to-[#38BDF8]" }
                    ].map((item, idx) => (
                      <div key={idx} className="space-y-1">
                        <div className="flex justify-between text-xs font-bold">
                          <span className="text-slate-200">{item.label}</span>
                          <span className="text-white">{item.pct}%</span>
                        </div>
                        <div className="w-full h-3 bg-[#200A47] rounded-full overflow-hidden p-0.5 border border-[#3B1F75]">
                          <div 
                            className={`h-full rounded-full bg-gradient-to-r ${item.barColor} transition-all duration-1000`}
                            style={{ width: `${item.pct}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Risk Stratification Protocol Table */}
                <div className="rounded-2xl overflow-hidden border border-[#4C1D95] bg-[#0E0424]">
                  <table className="w-full text-left text-xs font-mono">
                    <thead className="bg-[#210B47] text-white border-b border-[#4C1D95]">
                      <tr>
                        <th className="p-3 font-bold">Condition</th>
                        <th className="p-3 font-bold">AI Probability</th>
                        <th className="p-3 font-bold">Risk Category</th>
                        <th className="p-3 font-bold">Clinical Urgency</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[#260E4F]">
                      <tr className="bg-[#12062E]">
                        <td className="p-3 font-medium text-slate-200">Type 2 Diabetes Mellitus</td>
                        <td className="p-3 font-bold text-white">{data.risks.diabetes}%</td>
                        <td className="p-3"><span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40">Moderate</span></td>
                        <td className="p-3 text-slate-300 text-[11px]">HbA1c screening & carbohydrate regulation recommended.</td>
                      </tr>
                      <tr className="bg-[#0E0424]">
                        <td className="p-3 font-medium text-slate-200">Cardiovascular Disease (CVD)</td>
                        <td className="p-3 font-bold text-white">{data.risks.cvd}%</td>
                        <td className="p-3"><span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/40">Elevated / High</span></td>
                        <td className="p-3 text-slate-300 text-[11px]">Prioritize BP surveillance and dietary sodium restriction.</td>
                      </tr>
                      <tr className="bg-[#12062E]">
                        <td className="p-3 font-medium text-slate-200">Chronic Kidney Disease (CKD)</td>
                        <td className="p-3 font-bold text-white">{data.risks.ckd}%</td>
                        <td className="p-3"><span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">Low / Stable</span></td>
                        <td className="p-3 text-slate-300 text-[11px]">Maintain fluid balance; periodic renal function monitoring.</td>
                      </tr>
                    </tbody>
                  </table>
                </div>

              </div>
            )}

            {/* ========================================================================= */}
            {/* PAGE 4 — EXPLAINABLE AI (XAI) & SHAP (WITH NO EMPTY SPACE) */}
            {/* ========================================================================= */}
            {currentPage === 4 && (
              <div className="flex-1 flex flex-col justify-between space-y-4 animate-fade-in">
                <SectionHeader number="4" title="EXPLAINABLE AI (XAI) & SHAP ATTRIBUTION" subtitle="SECTION 4 — INTERPRETABLE MACHINE LEARNING FEATURE CONTRIBUTIONS" />

                {/* Understanding SHAP */}
                <div className="rounded-2xl p-4 bg-gradient-to-r from-[#180838] to-[#12052C] border border-[#7C3AED]/70 shadow-sm flex items-start space-x-3">
                  <div className="w-7 h-7 rounded-xl bg-[#2A0E5A] flex items-center justify-center text-[#C084FC] flex-shrink-0 mt-0.5 border border-[#581C87]">
                    <Brain className="w-4 h-4" />
                  </div>
                  <div className="space-y-0.5 text-xs font-sans">
                    <div className="font-bold text-white">Understanding SHAP (SHapley Additive exPlanations):</div>
                    <p className="text-slate-300 text-[11px] leading-relaxed">
                      SmartCare AI computes exact game-theoretic SHAP values to explain individual biomarker influences. 
                      Red/magenta values elevate predicted risk; blue values indicate protective physiological traits.
                    </p>
                  </div>
                </div>

                {/* Diverging SHAP Bar Chart */}
                <div className="rounded-2xl p-4 bg-[#11052B] border border-[#4C1D95] space-y-2.5 font-mono text-xs">
                  <div className="flex justify-between items-center text-[10px] text-slate-400 pb-1 border-b border-[#2D1457]">
                    <span className="text-sky-300">◀ PROTECTIVE FACTORS (- SHAP)</span>
                    <span className="text-[#C084FC]">BASE VALUE: 0.00</span>
                    <span className="text-rose-300">RISK INCREASING (+ SHAP) ▶</span>
                  </div>

                  <div className="space-y-1.5 pt-1">
                    {data.shapFactors.map((factor, idx) => {
                      const isRisk = factor.shap > 0;
                      const maxVal = 0.40;
                      const barWidth = Math.min(100, (Math.abs(factor.shap) / maxVal) * 100);

                      return (
                        <div key={idx} className="flex items-center space-x-3 py-1 px-2 rounded-lg hover:bg-[#1C0A42] transition">
                          <div className="w-44 text-[11px] font-semibold text-slate-200 truncate" title={factor.name}>
                            {factor.name}
                          </div>
                          <div className="flex-1 flex items-center h-4 bg-[#0A0317] rounded overflow-hidden relative border border-[#2D1457]">
                            <div className="w-1/2 flex justify-end pr-0.5 border-r border-[#4C1D95]">
                              {!isRisk && (
                                <div 
                                  className="h-2.5 rounded-l bg-gradient-to-l from-[#0284C7] to-[#38BDF8] transition-all duration-700"
                                  style={{ width: `${barWidth}%` }}
                                />
                              )}
                            </div>
                            <div className="w-1/2 flex justify-start pl-0.5">
                              {isRisk && (
                                <div 
                                  className="h-2.5 rounded-r bg-gradient-to-r from-[#D946EF] to-[#F43F5E] transition-all duration-700"
                                  style={{ width: `${barWidth}%` }}
                                />
                              )}
                            </div>
                          </div>
                          <div className={`w-16 text-right font-bold text-[11px] ${isRisk ? 'text-rose-300' : 'text-sky-300'}`}>
                            {factor.shap > 0 ? `+${factor.shap.toFixed(3)}` : factor.shap.toFixed(3)}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Biomarker Attribution Table */}
                <div className="rounded-2xl overflow-hidden border border-[#4C1D95] bg-[#0E0424]">
                  <table className="w-full text-left text-xs font-mono">
                    <thead className="bg-[#210B47] text-white border-b border-[#4C1D95]">
                      <tr>
                        <th className="p-2.5 font-bold">Biomarker</th>
                        <th className="p-2.5 font-bold">Patient Value</th>
                        <th className="p-2.5 font-bold">SHAP Impact</th>
                        <th className="p-2.5 font-bold">Direction</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[#260E4F]">
                      {data.shapFactors.slice(0, 4).map((f, i) => (
                        <tr key={i} className={i % 2 === 0 ? "bg-[#12062E]" : "bg-[#0E0424]"}>
                          <td className="p-2.5 font-medium text-slate-200">{f.name}</td>
                          <td className="p-2.5 font-bold text-white">{f.value}</td>
                          <td className="p-2.5 text-purple-200 font-bold">{f.shap > 0 ? `+${f.shap.toFixed(3)}` : f.shap.toFixed(3)}</td>
                          <td className="p-2.5">
                            {f.shap > 0 ? (
                              <span className="text-rose-300 text-[10px] font-bold">+ Risk-Elevating</span>
                            ) : (
                              <span className="text-sky-300 text-[10px] font-bold">- Protective</span>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {/* AI EXPLAINABILITY INSIGHT PANEL (Eliminating Empty Space) */}
                <div className="rounded-2xl p-4 bg-gradient-to-r from-[#14062E] via-[#100424] to-[#1A093D] border border-[#7C3AED]/60 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 font-mono text-xs">
                  <div className="space-y-1 max-w-md">
                    <div className="flex items-center space-x-2 text-[#C084FC] font-bold text-xs uppercase">
                      <Cpu className="w-4 h-4 text-[#A855F7]" />
                      <span>AI Model Explainability Synthesis</span>
                    </div>
                    <p className="text-slate-300 text-[11px] leading-relaxed font-sans">
                      Top risk-elevating contributions stem from systolic BP and elevated fasting glucose. 
                      Active physical exercise and non-smoking status provide significant protective counterbalances.
                    </p>
                  </div>
                  <div className="flex items-center space-x-2 shrink-0">
                    <div className="px-3 py-2 rounded-xl bg-[#200A47] border border-[#581C87] text-center">
                      <div className="text-[9px] text-slate-400 uppercase">Tree SHAP Version</div>
                      <div className="text-white font-bold text-xs">v0.44.1 Certified</div>
                    </div>
                  </div>
                </div>

              </div>
            )}

            {/* ========================================================================= */}
            {/* PAGE 5 — PERSONALIZED WELLNESS PLAN */}
            {/* ========================================================================= */}
            {currentPage === 5 && (
              <div className="flex-1 flex flex-col justify-between space-y-4 animate-fade-in">
                <SectionHeader number="5" title="PERSONALIZED WELLNESS & PREVENTIVE HEALTH PLAN" subtitle="SECTION 5 — EVIDENCE-BASED LIFESTYLE & NUTRITIONAL INTERVENTIONS" />

                {/* 7 Lifestyle Recommendation Cards */}
                <div className="space-y-2">
                  <div className="text-xs font-mono font-bold text-[#E9D5FF] flex items-center space-x-1.5">
                    <Sparkles className="w-3.5 h-3.5 text-[#C084FC]" />
                    <span>Actionable Evidence-Based Health Recommendations</span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                    {[
                      { num: "1", title: "Nutrition & Dietary Optimization", text: "Implement DASH dietary principles with sodium intake restricted to < 2,000 mg/day. Prioritize high-fiber complex carbohydrates and lean proteins." },
                      { num: "2", title: "Physical Activity & Exercise", text: "Engage in 150 minutes of moderate aerobic exercise weekly (brisk walking, cycling) combined with 2 days of resistance training." },
                      { num: "3", title: "Sleep Architecture & Rest", text: "Maintain 7–8 hours of restorative sleep nightly. Eliminate screen exposure 45 minutes before sleep to optimize cardiac regulation." },
                      { num: "4", title: "Stress Modulation", text: "Incorporate daily 10-minute diaphragmatic breathing or mindfulness exercises to mitigate cortisol-induced blood pressure elevation." },
                      { num: "5", title: "Hydration & Metabolic Balance", text: "Maintain daily fluid intake of 2.2 – 2.7 liters of pure water. Avoid sugar-sweetened beverages to preserve optimal renal perfusion." },
                      { num: "6", title: "Daily Habits & Blood Pressure", text: "Sustain non-smoking status. Limit alcohol. Conduct bi-weekly home blood pressure monitoring and record readings." },
                      { num: "7", title: "Clinical Follow-up Regimen", text: "Schedule follow-up clinical evaluation in 30 days. Repeat fasting lipid panel and fasting glucose screening." }
                    ].map((plan, idx) => (
                      <div 
                        key={idx} 
                        className={`p-3 rounded-2xl bg-[#11052B] border border-[#3B1F75] hover:border-[#7C3AED] transition flex items-start space-x-3 text-xs ${
                          idx === 6 ? 'sm:col-span-2' : ''
                        }`}
                      >
                        <div className="w-6 h-6 rounded-lg bg-[#2A0E5A] border border-[#581C87] flex items-center justify-center font-bold text-white text-[11px] flex-shrink-0 mt-0.5">
                          {plan.num}
                        </div>
                        <div className="space-y-0.5 font-sans">
                          <div className="font-bold text-white text-xs">{plan.title}</div>
                          <p className="text-slate-300 text-[11px] leading-relaxed">{plan.text}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Wellness Targets Table */}
                <div className="rounded-2xl overflow-hidden border border-[#4C1D95] bg-[#0E0424]">
                  <table className="w-full text-left text-xs font-mono">
                    <thead className="bg-[#210B47] text-white border-b border-[#4C1D95]">
                      <tr>
                        <th className="p-2.5 font-bold">Wellness Domain</th>
                        <th className="p-2.5 font-bold">Target Goal</th>
                        <th className="p-2.5 font-bold">Projected Risk Impact</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[#260E4F]">
                      <tr className="bg-[#12062E]">
                        <td className="p-2.5 font-medium text-slate-200">Aerobic Activity</td>
                        <td className="p-2.5 font-bold text-white">150 mins / week</td>
                        <td className="p-2.5 text-sky-300 font-bold">- 18% CVD Risk</td>
                      </tr>
                      <tr className="bg-[#0E0424]">
                        <td className="p-2.5 font-medium text-slate-200">Sodium Restriction</td>
                        <td className="p-2.5 font-bold text-white">&lt; 2,000 mg / day</td>
                        <td className="p-2.5 text-sky-300 font-bold">- 5 to 8 mmHg Systolic BP</td>
                      </tr>
                      <tr className="bg-[#12062E]">
                        <td className="p-2.5 font-medium text-slate-200">Dietary Fiber</td>
                        <td className="p-2.5 font-bold text-white">30 g / day</td>
                        <td className="p-2.5 text-sky-300 font-bold">- 14% Diabetes Risk</td>
                      </tr>
                    </tbody>
                  </table>
                </div>

              </div>
            )}

            {/* ========================================================================= */}
            {/* PAGE 6 — CLINICAL DECISION SUPPORT & SURVEILLANCE */}
            {/* ========================================================================= */}
            {currentPage === 6 && (
              <div className="flex-1 flex flex-col justify-between space-y-4 animate-fade-in">
                <SectionHeader number="6" title="CLINICAL DECISION SUPPORT & SURVEILLANCE" subtitle="SECTION 6 — PHYSICIAN CONSULTATION & CLINICAL MONITORING SCHEDULE" />

                {/* Synthesis Card */}
                <div className="rounded-2xl p-4 bg-gradient-to-r from-[#180838] to-[#12052C] border border-[#7C3AED]/70 shadow-sm space-y-1.5 font-sans text-xs">
                  <div className="font-bold text-white text-xs flex items-center space-x-2">
                    <Stethoscope className="w-4 h-4 text-[#C084FC]" />
                    <span>Clinical Synthesis for Patient #{data.patientId} ({data.patientName}):</span>
                  </div>
                  <p className="text-slate-300 text-[11px] leading-relaxed font-mono">
                    Ensemble prediction models identify primary clinical vulnerability in the <b>cardiovascular and metabolic domains</b>. 
                    Elevated systolic pressure with moderate fasting glucose warrants targeted lifestyle modification and 30-day longitudinal re-evaluation.
                  </p>
                </div>

                {/* Monitoring Schedule Table */}
                <div className="rounded-2xl overflow-hidden border border-[#4C1D95] bg-[#0E0424]">
                  <table className="w-full text-left text-xs font-mono">
                    <thead className="bg-[#210B47] text-white border-b border-[#4C1D95]">
                      <tr>
                        <th className="p-2.5 font-bold">Biomarker / Test</th>
                        <th className="p-2.5 font-bold">Target Goal</th>
                        <th className="p-2.5 font-bold">Recommended Frequency</th>
                        <th className="p-2.5 font-bold">Clinical Rationale</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[#260E4F]">
                      <tr className="bg-[#12062E]">
                        <td className="p-2.5 font-medium text-slate-200">Blood Pressure (BP)</td>
                        <td className="p-2.5 font-bold text-white">&lt; 120/80 mmHg</td>
                        <td className="p-2.5 text-purple-200 font-bold">Bi-weekly</td>
                        <td className="p-2.5 text-slate-300 text-[11px]">Hypertension prevention</td>
                      </tr>
                      <tr className="bg-[#0E0424]">
                        <td className="p-2.5 font-medium text-slate-200">Fasting Glucose / HbA1c</td>
                        <td className="p-2.5 font-bold text-white">&lt; 100 mg/dL</td>
                        <td className="p-2.5 text-purple-200 font-bold">Every 3 Months</td>
                        <td className="p-2.5 text-slate-300 text-[11px]">Glycemic monitoring</td>
                      </tr>
                      <tr className="bg-[#12062E]">
                        <td className="p-2.5 font-medium text-slate-200">Lipid Panel</td>
                        <td className="p-2.5 font-bold text-white">LDL &lt; 100 mg/dL</td>
                        <td className="p-2.5 text-purple-200 font-bold">Every 6 Months</td>
                        <td className="p-2.5 text-slate-300 text-[11px]">Atherosclerotic risk</td>
                      </tr>
                      <tr className="bg-[#0E0424]">
                        <td className="p-2.5 font-medium text-slate-200">Serum Creatinine & eGFR</td>
                        <td className="p-2.5 font-bold text-white">eGFR &gt; 90 mL/min</td>
                        <td className="p-2.5 text-purple-200 font-bold">Annual Screening</td>
                        <td className="p-2.5 text-slate-300 text-[11px]">Renal function check</td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                {/* Attending Clinician Notes */}
                <div className="rounded-2xl p-4 bg-[#11052B] border border-[#4C1D95] space-y-3 text-xs font-mono">
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 border-b border-[#2D1457] pb-3">
                    <div><span className="text-[9px] text-[#A78BFA] uppercase font-bold block">Attending Clinician:</span><span className="text-white font-bold text-xs">{data.doctorName}</span></div>
                    <div><span className="text-[9px] text-[#A78BFA] uppercase font-bold block">Specialty:</span><span className="text-white font-bold text-xs">{data.doctorSpecialty}</span></div>
                    <div><span className="text-[9px] text-[#A78BFA] uppercase font-bold block">License ID:</span><span className="text-[#D8B4FE] font-bold text-xs">{data.doctorLicense}</span></div>
                  </div>
                  <div className="space-y-1">
                    <span className="text-[9px] text-[#A78BFA] uppercase font-bold block">Clinician Assessment Notes:</span>
                    <p className="text-slate-300 text-[11px] leading-relaxed bg-[#0E0424] p-3 rounded-xl border border-[#2D1457]">
                      Assessment reviewed. Patient exhibits borderline systolic blood pressure and moderate cardiovascular risk profile. 
                      Recommended initiation of DASH dietary principles, 150 min/wk aerobic conditioning, and 30-day clinical re-evaluation.
                    </p>
                  </div>
                </div>

              </div>
            )}

            {/* ========================================================================= */}
            {/* PAGE 7 — AI TRANSPARENCY, SAFETY & SIGN-OFF */}
            {/* ========================================================================= */}
            {currentPage === 7 && (
              <div className="flex-1 flex flex-col justify-between space-y-4 animate-fade-in">
                <SectionHeader number="7" title="AI TRANSPARENCY, SAFETY & CLINICAL SIGN-OFF" subtitle="SECTION 7 — MODEL REGISTRY, REGULATORY NOTICE & PHYSICIAN SIGNATURE" />

                {/* Model Registry Table */}
                <div className="rounded-2xl overflow-hidden border border-[#4C1D95] bg-[#0E0424]">
                  <table className="w-full text-left text-xs font-mono">
                    <thead className="bg-[#210B47] text-white border-b border-[#4C1D95]">
                      <tr>
                        <th className="p-2.5 font-bold">Predictive Model</th>
                        <th className="p-2.5 font-bold">Architecture</th>
                        <th className="p-2.5 font-bold">Version</th>
                        <th className="p-2.5 font-bold">ROC-AUC</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[#260E4F]">
                      <tr className="bg-[#12062E]"><td className="p-2.5 font-medium text-slate-200">Diabetes Predictor</td><td className="p-2.5 text-white font-bold">XGBoost Classifier</td><td className="p-2.5 text-[#D8B4FE]">v1.2.0</td><td className="p-2.5 text-emerald-400 font-bold">0.924</td></tr>
                      <tr className="bg-[#0E0424]"><td className="p-2.5 font-medium text-slate-200">Cardiovascular Predictor</td><td className="p-2.5 text-white font-bold">Random Forest Classifier</td><td className="p-2.5 text-[#D8B4FE]">v1.1.0</td><td className="p-2.5 text-emerald-400 font-bold">0.901</td></tr>
                      <tr className="bg-[#12062E]"><td className="p-2.5 font-medium text-slate-200">Renal (CKD) Predictor</td><td className="p-2.5 text-white font-bold">Gradient Boosting</td><td className="p-2.5 text-[#D8B4FE]">v1.0.0</td><td className="p-2.5 text-emerald-400 font-bold">0.965</td></tr>
                      <tr className="bg-[#0E0424]"><td className="p-2.5 font-medium text-slate-200">Explainability Engine</td><td className="p-2.5 text-white font-bold">Tree / Kernel SHAP</td><td className="p-2.5 text-[#D8B4FE]">v0.44.1</td><td className="p-2.5 text-sky-400 font-bold">Game-Theoretic</td></tr>
                    </tbody>
                  </table>
                </div>

                {/* Regulatory Disclaimer */}
                <div className="rounded-2xl p-4 bg-gradient-to-br from-[#1C0528] to-[#12041D] border border-rose-500/60 shadow-[0_0_20px_rgba(244,63,94,0.15)] flex items-start space-x-3.5">
                  <div className="w-8 h-8 rounded-xl bg-[#36081F] flex items-center justify-center text-rose-400 flex-shrink-0 mt-0.5 border border-rose-500/50">
                    <ShieldAlert className="w-4 h-4" />
                  </div>
                  <div className="space-y-1 text-xs font-sans">
                    <div className="font-bold text-rose-300 uppercase tracking-wide">
                      OFFICIAL CLINICAL SAFETY & REGULATORY DISCLAIMER
                    </div>
                    <p className="text-slate-200 text-[11px] leading-relaxed">
                      This health assessment report is generated by the SmartCare AI Healthcare Platform for <b>clinical decision support only</b>. 
                      The predictions, risk probabilities, and wellness suggestions contained herein do <b>NOT</b> constitute 
                      a definitive medical diagnosis or prescription. All insights must be confirmed by a licensed healthcare professional.
                    </p>
                  </div>
                </div>

                {/* Clinician Review & Electronic Signature */}
                <div className="rounded-2xl p-4 bg-[#11052B] border border-[#7C3AED] grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs font-mono">
                  <div className="space-y-2">
                    <div><span className="text-[9px] text-[#A78BFA] uppercase font-bold block">Attending Clinician:</span><span className="text-white font-bold text-xs">{data.doctorName}</span></div>
                    <div><span className="text-[9px] text-[#A78BFA] uppercase font-bold block">License ID:</span><span className="text-[#D8B4FE] font-bold text-xs">{data.doctorLicense}</span></div>
                    <div><span className="text-[9px] text-[#A78BFA] uppercase font-bold block">Department:</span><span className="text-white font-bold text-xs">{data.doctorDept}</span></div>
                  </div>

                  <div className="space-y-2">
                    <div><span className="text-[9px] text-[#A78BFA] uppercase font-bold block">Assessment Date:</span><span className="text-white font-bold text-xs">{data.assessmentDate}</span></div>
                    <div><span className="text-[9px] text-[#A78BFA] uppercase font-bold block">Report ID:</span><span className="text-[#E9D5FF] font-bold text-xs">{data.reportId}</span></div>
                    <div><span className="text-[9px] text-[#A78BFA] uppercase font-bold block">Platform Engine:</span><span className="text-purple-300 font-bold text-xs">SmartCare AI Enterprise v2.4</span></div>
                  </div>

                  <div className="sm:col-span-2 pt-3 border-t border-[#2D1457] flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">
                    <div>
                      <div className="text-[9px] text-[#A78BFA] uppercase font-bold mb-1">Clinician Signature:</div>
                      <svg className="h-7 w-44 text-[#C084FC]" viewBox="0 0 160 35" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round">
                        <path d="M10 25 C25 5, 30 5, 35 25 C40 10, 45 15, 55 20 C65 25, 75 10, 85 22 C95 15, 110 5, 120 20 C130 30, 145 18, 155 15" />
                      </svg>
                      <div className="text-[10px] text-slate-300 font-bold italic">
                        {data.doctorName}, MD (Electronically Signed)
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-[9px] text-[#A78BFA] uppercase font-bold">Signature Timestamp:</div>
                      <div className="text-xs font-bold text-white mt-0.5">{data.timestamp}</div>
                    </div>
                  </div>
                </div>

              </div>
            )}

          </div>

          {/* ========================================================================= */}
          {/* UNIVERSAL PAGE FOOTER ON EVERY PAGE */}
          {/* ========================================================================= */}
          <footer className="relative z-20 px-8 py-3.5 border-t border-[#2A154D] bg-[#090317] flex items-center justify-between text-[10px] font-mono text-slate-400">
            <div className="flex items-center space-x-2">
              <Logo variant="symbol" size="xs" />
              <span className="font-bold text-slate-300">SmartCare AI Healthcare Intelligence & IT System</span>
            </div>
            <div className="flex items-center space-x-3">
              <span>Patient #{data.patientId}</span>
              <span className="text-slate-600">•</span>
              <span>Report {data.reportId}</span>
              <span className="text-slate-600">•</span>
              <span className="text-[#C084FC] font-bold">Page {currentPage} of 7</span>
            </div>
          </footer>

        </article>
      </div>

      {/* ========================================================================= */}
      {/* 4. BOTTOM FLOATING NAVIGATION BAR */}
      {/* ========================================================================= */}
      <footer className="relative z-20 px-4 sm:px-6 py-3 bg-[#0B0418] border-t border-[#2A154D] flex items-center justify-between text-xs font-mono flex-shrink-0">
        <button
          onClick={() => handlePageChange(currentPage - 1)}
          disabled={currentPage === 1 || isTransitioning}
          className="px-4 py-2 rounded-xl bg-[#15092A] hover:bg-[#200E3D] border border-[#2B144E] disabled:opacity-30 disabled:pointer-events-none text-white font-bold flex items-center space-x-1.5 transition cursor-pointer"
        >
          <ChevronLeft className="w-4 h-4" />
          <span>PREVIOUS</span>
        </button>

        <div className="flex items-center space-x-2 text-slate-300">
          <span className="text-[#C084FC] font-bold">PAGE {currentPage} OF 7</span>
          <span className="text-slate-600">•</span>
          <span className="text-slate-400 hidden sm:inline">{pagesInfo[currentPage - 1].title.substring(2)}</span>
        </div>

        <button
          onClick={() => handlePageChange(currentPage + 1)}
          disabled={currentPage === 7 || isTransitioning}
          className="px-4 py-2 rounded-xl bg-gradient-to-r from-[#6D28D9] to-[#7C3AED] hover:brightness-110 disabled:opacity-30 disabled:pointer-events-none text-white font-bold flex items-center space-x-1.5 transition cursor-pointer shadow-md shadow-[#7C3AED]/30"
        >
          <span>NEXT PAGE</span>
          <ChevronRight className="w-4 h-4" />
        </button>
      </footer>

    </div>
  );
}

// Section Header Helper
function SectionHeader({ number, title, subtitle }) {
  return (
    <div className="flex items-center space-x-3 pb-2 border-b border-[#3B1F75]">
      <div className="w-8 h-8 rounded-xl bg-[#7C3AED] border border-[#A855F7] flex items-center justify-center font-bold text-white text-sm shadow-[0_0_15px_rgba(124,58,237,0.5)]">
        {number}
      </div>
      <div>
        <h2 className="text-sm sm:text-base font-extrabold tracking-tight text-white">{title}</h2>
        <p className="text-[10px] font-mono text-[#C084FC] uppercase font-bold">{subtitle}</p>
      </div>
    </div>
  );
}

// Universal Watermark Component
function SmartCareWatermark() {
  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden select-none z-0">
      {/* Large SmartCare AI Official Watermark Logo (8-14% Opacity) */}
      <div className="absolute -right-20 top-1/4 w-[480px] h-[480px] opacity-[0.09] transform rotate-12">
        <img 
          src="/smartcare-logo.png" 
          alt="" 
          className="w-full h-full object-contain filter drop-shadow-2xl" 
        />
      </div>

      <div className="absolute -left-20 bottom-1/4 w-[400px] h-[400px] opacity-[0.07] transform -rotate-12">
        <img 
          src="/smartcare-logo.png" 
          alt="" 
          className="w-full h-full object-contain filter drop-shadow-2xl" 
        />
      </div>

      {/* Subtle ECG Waveform & Neural Node Network */}
      <svg className="absolute inset-0 w-full h-full opacity-[0.08]" xmlns="http://www.w3.org/2000/svg">
        <path 
          d="M 0 350 L 150 350 L 180 320 L 200 390 L 220 280 L 240 370 L 260 340 L 280 350 L 600 350 L 630 310 L 650 400 L 670 270 L 690 380 L 710 350 L 900 350" 
          fill="none" 
          stroke="#C084FC" 
          strokeWidth="1.5" 
        />
        <path 
          d="M 0 750 L 200 750 L 230 710 L 250 800 L 270 680 L 290 770 L 310 740 L 330 750 L 700 750 L 730 710 L 750 790 L 770 690 L 790 750 L 900 750" 
          fill="none" 
          stroke="#A855F7" 
          strokeWidth="1.5" 
        />
      </svg>

      {/* Low-Opacity Diagonal Healthcare IT Typography Watermark */}
      <div className="absolute inset-0 flex flex-col justify-around items-center opacity-[0.035] font-mono font-black text-2xl tracking-[0.4em] text-[#C084FC] transform -rotate-25 pointer-events-none">
        <div>SMARTCARE AI • HEALTHCARE INTELLIGENCE</div>
        <div>PREDICT • PREVENT • PERSONALIZE</div>
        <div>CLINICAL DECISION SUPPORT PLATFORM</div>
      </div>
    </div>
  );
}
