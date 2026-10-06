import React from 'react';
import Medical3DVisualization from './Medical3DVisualization';
import { Sparkles, ShieldCheck, Database, Cpu, Activity, ArrowRight, Zap, CheckCircle2, Shield, Layers } from 'lucide-react';

export default function DashboardHero({ user, onNavigate }) {
  return (
    <div className="relative overflow-hidden rounded-3xl glass-panel border border-slate-800/80 p-6 md:p-8 mb-8">
      {/* Background Radial Glow Mesh */}
      <div className="absolute top-0 right-1/4 -mt-16 w-96 h-96 bg-gradient-to-br from-sky-500/15 via-teal-500/10 to-transparent rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-0 -mb-16 -ml-16 w-80 h-80 bg-gradient-to-tr from-purple-500/15 via-sky-500/10 to-transparent rounded-full blur-3xl pointer-events-none" />

      {/* 3-Zone Visual Command Center Composition */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center relative z-10">
        
        {/* ZONE 1: Left Info & Capability Cards */}
        <div className="lg:col-span-4 space-y-5 text-left">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-sky-500/10 border border-sky-500/30 text-sky-400 text-xs font-bold uppercase tracking-wider">
            <Sparkles className="w-3.5 h-3.5" />
            <span>SmartCare AI Health Command Center</span>
          </div>

          <div className="space-y-1.5">
            <h1 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
              Intelligent Healthcare
            </h1>
            <h2 className="text-xl md:text-2xl font-bold bg-gradient-to-r from-sky-400 via-teal-300 to-white bg-clip-text text-transparent">
              Multi-Task Risk Intelligence
            </h2>
            <p className="text-slate-300 text-xs leading-relaxed max-w-sm pt-1">
              Calibrated multi-disease predictions for Diabetes, CVD, and CKD coupled with model-faithful SHAP factor attributions.
            </p>
          </div>

          {/* Compact AI Capability Cards Grid */}
          <div className="grid grid-cols-2 gap-2.5 pt-1">
            <div className="p-3 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-1 hover:border-sky-500/30 transition">
              <div className="flex items-center space-x-1.5 text-sky-400 font-bold text-[11px]">
                <Cpu className="w-3.5 h-3.5" />
                <span>AI-Powered Models</span>
              </div>
              <p className="text-[10px] text-slate-400">Calibrated XGBoost & RF</p>
            </div>

            <div className="p-3 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-1 hover:border-purple-500/30 transition">
              <div className="flex items-center space-x-1.5 text-purple-400 font-bold text-[11px]">
                <Sparkles className="w-3.5 h-3.5" />
                <span>Explainable AI</span>
              </div>
              <p className="text-[10px] text-slate-400">SHAP-based attributions</p>
            </div>

            <div className="p-3 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-1 hover:border-teal-500/30 transition">
              <div className="flex items-center space-x-1.5 text-teal-400 font-bold text-[11px]">
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>Zero Data Leakage</span>
              </div>
              <p className="text-[10px] text-slate-400">Strict train/val isolation</p>
            </div>

            <div className="p-3 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-1 hover:border-amber-500/30 transition">
              <div className="flex items-center space-x-1.5 text-amber-400 font-bold text-[11px]">
                <Layers className="w-3.5 h-3.5" />
                <span>Multi-Task Intelligence</span>
              </div>
              <p className="text-[10px] text-slate-400">Diabetes + CVD + CKD</p>
            </div>
          </div>

          <div className="pt-2">
            <button
              onClick={() => onNavigate && onNavigate('risk')}
              className="flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-sky-500 to-teal-400 hover:from-sky-400 hover:to-teal-300 text-slate-950 font-extrabold text-xs uppercase tracking-wider transition shadow-lg shadow-sky-500/20"
            >
              <Activity className="w-4 h-4" />
              <span>Execute Risk Assessment</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* ZONE 2: Center 3D Anatomical Body Scanner */}
        <div className="lg:col-span-5 flex flex-col items-center justify-center relative">
          <Medical3DVisualization className="w-full h-72 md:h-80" />
          
          {/* Floating Medical HUD Annotations */}
          <div className="absolute top-8 left-0 px-2.5 py-1 rounded-xl bg-slate-950/80 border border-red-500/40 text-[10px] text-red-400 font-mono shadow-lg flex items-center space-x-1">
            <span className="w-1.5 h-1.5 rounded-full bg-red-400 animate-ping" />
            <span>CARDIAC / HEART NODE</span>
          </div>

          <div className="absolute bottom-12 right-0 px-2.5 py-1 rounded-xl bg-slate-950/80 border border-purple-500/40 text-[10px] text-purple-300 font-mono shadow-lg flex items-center space-x-1">
            <span className="w-1.5 h-1.5 rounded-full bg-purple-400 animate-ping" />
            <span>RENAL / KIDNEY NODES</span>
          </div>
        </div>

        {/* ZONE 3: Right AI System Intelligence HUD Panel */}
        <div className="lg:col-span-3 space-y-3">
          <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-3">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <span className="text-[11px] font-extrabold text-white uppercase tracking-wider flex items-center space-x-1">
                <Zap className="w-3.5 h-3.5 text-teal-400 inline" />
                <span>AI ANALYSIS ENGINE</span>
              </span>
              <span className="flex items-center space-x-1 text-[10px] text-teal-400 font-bold">
                <span className="w-1.5 h-1.5 rounded-full bg-teal-400 animate-ping" />
                <span>ONLINE</span>
              </span>
            </div>

            <div className="space-y-2 text-xs">
              <div className="flex items-center justify-between">
                <span className="text-slate-400 text-[11px]">Prediction Engine</span>
                <span className="text-teal-400 font-bold font-mono text-[10px] bg-teal-500/10 px-2 py-0.5 rounded border border-teal-500/30">ACTIVE</span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-slate-400 text-[11px]">Risk Calibration</span>
                <span className="text-sky-400 font-bold font-mono text-[10px] bg-sky-500/10 px-2 py-0.5 rounded border border-sky-500/30">PLATT SIGMOID</span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-slate-400 text-[11px]">SHAP Engine</span>
                <span className="text-purple-300 font-bold font-mono text-[10px] bg-purple-500/10 px-2 py-0.5 rounded border border-purple-500/30">TREE EXPLAINER</span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-slate-400 text-[11px]">Data Leakage Guard</span>
                <span className="text-teal-400 font-bold font-mono text-[10px] bg-teal-500/10 px-2 py-0.5 rounded border border-teal-500/30">VERIFIED</span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-slate-400 text-[11px]">Preprocessing Pipeline</span>
                <span className="text-amber-300 font-bold font-mono text-[10px] bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/30">HEALTHY (v1.0)</span>
              </div>
            </div>
          </div>

          <div className="p-3.5 rounded-2xl bg-slate-900/60 border border-slate-800 text-[10px] text-slate-400 space-y-1 text-center">
            <div>Data Assets: <span className="text-white font-bold">70K+ BRFSS & Clinical Records</span></div>
            <div>Target Diseases: <span className="text-teal-300 font-bold">Diabetes / CVD / CKD</span></div>
          </div>
        </div>

      </div>
    </div>
  );
}
