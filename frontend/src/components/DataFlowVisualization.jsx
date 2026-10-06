import React from 'react';
import { Activity, Heart, Zap, Cpu, Sparkles, ArrowRight, ShieldCheck } from 'lucide-react';

export default function DataFlowVisualization({ className = "w-full" }) {
  return (
    <div className={`p-6 rounded-2xl bg-slate-900/40 backdrop-blur-xl border border-slate-800 shadow-2xl relative overflow-hidden ${className}`}>
      
      {/* Background Ambient Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="text-[10px] font-mono text-cyan-400 font-extrabold uppercase tracking-widest mb-4 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
          <span>MULTI-TASK AI DATA PIPELINE FLOW</span>
        </div>
        <span className="text-slate-500 font-normal">REAL-TIME 2.5D ENGINE</span>
      </div>

      {/* 2.5D Animated Data Flow Diagram */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-4 items-center relative z-10 py-2">
        
        {/* LEFT COLUMN: 3 DISEASE INPUT SOURCES */}
        <div className="md:col-span-4 space-y-2.5">
          {/* CVD Stream Source */}
          <div className="p-2.5 rounded-xl bg-slate-900/80 border border-red-500/30 flex items-center space-x-3 transition-all hover:border-red-400 hover:scale-102">
            <div className="p-2 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400">
              <Heart className="w-4 h-4 animate-pulse" />
            </div>
            <div>
              <div className="text-xs font-extrabold text-white font-mono">CARDIOVASCULAR (CVD)</div>
              <div className="text-[9px] text-slate-400 font-mono">BP, Cholesterol, Pulse Data</div>
            </div>
          </div>

          {/* CKD Stream Source */}
          <div className="p-2.5 rounded-xl bg-slate-900/80 border border-purple-500/30 flex items-center space-x-3 transition-all hover:border-purple-400 hover:scale-102">
            <div className="p-2 rounded-lg bg-purple-500/10 border border-purple-500/30 text-purple-400">
              <Activity className="w-4 h-4" />
            </div>
            <div>
              <div className="text-xs font-extrabold text-white font-mono">RENAL SYSTEM (CKD)</div>
              <div className="text-[9px] text-slate-400 font-mono">Creatinine, GFR, Urea</div>
            </div>
          </div>

          {/* Diabetes Stream Source */}
          <div className="p-2.5 rounded-xl bg-slate-900/80 border border-cyan-500/30 flex items-center space-x-3 transition-all hover:border-cyan-400 hover:scale-102">
            <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
              <Zap className="w-4 h-4" />
            </div>
            <div>
              <div className="text-xs font-extrabold text-white font-mono">METABOLIC (DIABETES)</div>
              <div className="text-[9px] text-slate-400 font-mono">Glucose, BMI, Glycemic</div>
            </div>
          </div>
        </div>

        {/* CENTER COLUMN: MULTI-TASK AI PROCESSING CORE NODE */}
        <div className="md:col-span-4 flex flex-col items-center justify-center p-4 rounded-2xl bg-gradient-to-b from-cyan-950/40 to-slate-900/80 border border-cyan-500/40 text-center relative shadow-lg">
          <div className="p-3 rounded-xl bg-cyan-500/10 border border-cyan-400/50 text-cyan-300 mb-2 animate-bounce">
            <Cpu className="w-6 h-6 text-cyan-400" />
          </div>
          <div className="text-sm font-extrabold text-white font-mono">MULTI-TASK AI CORE</div>
          <div className="text-[10px] text-cyan-400 font-mono font-bold mt-0.5">XGBoost & RandomForest</div>
          
          <div className="w-full bg-slate-950/80 rounded-lg p-1.5 border border-slate-800 text-[9px] font-mono text-slate-400 mt-3 flex items-center justify-center space-x-1">
            <Sparkles className="w-3 h-3 text-teal-400" />
            <span>CALIBRATION: ISOTONIC</span>
          </div>
        </div>

        {/* RIGHT COLUMN: CALIBRATED RISK INTELLIGENCE OUTPUT */}
        <div className="md:col-span-4 space-y-2.5">
          <div className="p-3 rounded-xl bg-slate-900/80 border border-teal-500/40 text-center font-mono">
            <div className="text-[10px] text-slate-400 font-bold">RISK PREDICTION OUTPUT</div>
            <div className="text-xs font-extrabold text-teal-300 mt-1 flex items-center justify-center space-x-1">
              <ShieldCheck className="w-3.5 h-3.5 text-teal-400" />
              <span>CALIBRATED ATTRIBUTIONS</span>
            </div>
            <div className="text-[9px] text-slate-500 mt-1">SHAP Explainability Included</div>
          </div>
        </div>

      </div>

      {/* SVG Animated Flow Lines Overlay */}
      <div className="hidden md:block w-full h-8 mt-2">
        <svg className="w-full h-full text-cyan-500/50" viewBox="0 0 500 30">
          <line x1="150" y1="15" x2="350" y2="15" stroke="currentColor" strokeWidth="2" strokeDasharray="6,6" className="animate-pulse" />
        </svg>
      </div>

    </div>
  );
}
