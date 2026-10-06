import React, { useState } from 'react';
import HolographicHUDPanel from '../components/HolographicHUDPanel';
import { Box, Sparkles, ShieldCheck, Cpu, CheckCircle2, Layers, ZoomIn, X, ChevronRight, GitBranch } from 'lucide-react';

export default function ModelRegistry() {
  const [selectedModel, setSelectedModel] = useState(null);
  const [drawerOpen, setDrawerOpen] = useState(false);

  const REGISTRY_MODELS = [
    {
      name: 'XGBoost - Diabetes Risk Model',
      disease: 'Diabetes Mellitus',
      version: 'v1.4.0',
      status: 'PRODUCTION',
      auc: '0.942',
      pr: '0.910',
      f1: '0.912',
      calibration: 'Isotonic (Brier: 0.041)',
      pipeline: 'v1.8.0',
      dataset: 'BRFSS 50/50 Split',
      created: '2026-08-25'
    },
    {
      name: 'Random Forest - CVD Risk Model',
      disease: 'Cardiovascular Disease',
      version: 'v1.3.2',
      status: 'PRODUCTION',
      auc: '0.918',
      pr: '0.887',
      f1: '0.884',
      calibration: 'Platt Scaling (Brier: 0.054)',
      pipeline: 'v1.3.0',
      dataset: 'Cardio 68K Corpus',
      created: '2026-08-20'
    },
    {
      name: 'Multi-Task Shared Neural Model',
      disease: 'Diabetes + CVD + CKD',
      version: 'v2.1.0',
      status: 'PRIMARY PRODUCTION',
      auc: '0.956',
      pr: '0.932',
      f1: '0.938',
      calibration: 'Isotonic (Brier: 0.032)',
      pipeline: 'v2.0.0',
      dataset: 'Multi-Task Unified Matrix',
      created: '2026-08-28'
    },
    {
      name: 'Logistic Regression Baseline',
      disease: 'Multi-Disease Baseline',
      version: 'v1.0.0',
      status: 'ARCHIVED',
      auc: '0.885',
      pr: '0.840',
      f1: '0.842',
      calibration: 'Uncalibrated',
      pipeline: 'v1.0.0',
      dataset: 'Baseline Synthetic',
      created: '2026-08-10'
    }
  ];

  const handleSelectModel = (m) => {
    setSelectedModel(m);
    setDrawerOpen(true);
  };

  return (
    <div className="w-full space-y-6 z-10 font-sans pb-12 relative">
      
      {/* 1. MAIN MODEL REGISTRY WORKSPACE TABLE */}
      <div className="w-full">
        <HolographicHUDPanel 
          title="PRODUCTION MODEL REGISTRY & ARTIFACT VAULT" 
          subtitle="Validated ML model artifacts, calibrated weights & pipeline lineage"
          glowColor="cyan"
        >
          <div className="overflow-x-auto">
            <table className="w-full text-left font-mono text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-[10px] text-slate-400 uppercase tracking-wider">
                  <th className="py-2.5 px-3">MODEL</th>
                  <th className="py-2.5 px-3">DISEASE TARGET</th>
                  <th className="py-2.5 px-3">VERSION</th>
                  <th className="py-2.5 px-3">STATUS</th>
                  <th className="py-2.5 px-3">ROC-AUC</th>
                  <th className="py-2.5 px-3">PR-AUC</th>
                  <th className="py-2.5 px-3">F1-SCORE</th>
                  <th className="py-2.5 px-3">PIPELINE</th>
                  <th className="py-2.5 px-3">CREATED</th>
                  <th className="py-2.5 px-3">ACTION</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-300">
                {REGISTRY_MODELS.map((m, idx) => (
                  <tr 
                    key={idx}
                    onClick={() => handleSelectModel(m)}
                    className="hover:bg-slate-900/60 transition cursor-pointer"
                  >
                    <td className="py-3 px-3 font-bold text-white flex items-center space-x-2">
                      <Cpu className="w-4 h-4 text-cyan-400 flex-shrink-0" />
                      <span>{m.name}</span>
                    </td>
                    <td className="py-3 px-3 text-slate-400">{m.disease}</td>
                    <td className="py-3 px-3 text-cyan-300 font-bold">{m.version}</td>
                    <td className="py-3 px-3">
                      <span className={`px-2 py-0.5 rounded text-[9px] font-bold border ${
                        m.status.includes('PRIMARY') ? 'bg-purple-500/20 text-purple-300 border-purple-500/30' :
                        m.status.includes('PRODUCTION') ? 'bg-teal-500/20 text-teal-300 border-teal-500/30' :
                        'bg-slate-800 text-slate-400 border-slate-700'
                      }`}>
                        {m.status}
                      </span>
                    </td>
                    <td className="py-3 px-3 text-cyan-400 font-bold">{m.auc}</td>
                    <td className="py-3 px-3 text-teal-300 font-bold">{m.pr}</td>
                    <td className="py-3 px-3 text-purple-300 font-bold">{m.f1}</td>
                    <td className="py-3 px-3 text-slate-400">{m.pipeline}</td>
                    <td className="py-3 px-3 text-slate-400 text-[11px]">{m.created}</td>
                    <td className="py-3 px-3">
                      <button className="px-2.5 py-1 rounded bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 text-[10px] font-bold border border-cyan-500/30">
                        INSPECT
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </HolographicHUDPanel>
      </div>

      {/* 2. RIGHT-SIDE DETAIL DRAWER FOR MODEL ARTIFACT */}
      {drawerOpen && selectedModel && (
        <div className="fixed inset-y-0 right-0 z-50 w-full max-w-md bg-[#070d1e] border-l border-cyan-500/30 p-6 shadow-2xl space-y-6 font-mono text-xs overflow-y-auto animate-slideIn">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div>
              <div className="text-[10px] text-cyan-400 font-bold">MODEL ARTIFACT DRAWER</div>
              <h3 className="text-base font-extrabold text-white">{selectedModel.name}</h3>
            </div>
            <button 
              onClick={() => setDrawerOpen(false)}
              className="p-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-white cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="space-y-4">
            <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
              <span className="text-[9px] text-slate-400 uppercase">TARGET DISEASE</span>
              <div className="text-sm font-bold text-white">{selectedModel.disease}</div>
            </div>

            <div className="grid grid-cols-3 gap-2 text-center font-mono">
              <div className="bg-slate-900 p-2.5 rounded-xl border border-slate-800">
                <span className="text-[8px] text-slate-400 block">ROC-AUC</span>
                <div className="text-cyan-300 font-extrabold text-xs mt-0.5">{selectedModel.auc}</div>
              </div>
              <div className="bg-slate-900 p-2.5 rounded-xl border border-slate-800">
                <span className="text-[8px] text-slate-400 block">PR-AUC</span>
                <div className="text-teal-300 font-extrabold text-xs mt-0.5">{selectedModel.pr}</div>
              </div>
              <div className="bg-slate-900 p-2.5 rounded-xl border border-slate-800">
                <span className="text-[8px] text-slate-400 block">F1 SCORE</span>
                <div className="text-purple-300 font-extrabold text-xs mt-0.5">{selectedModel.f1}</div>
              </div>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
              <span className="text-[9px] text-slate-400 uppercase">CALIBRATION PROTOCOL</span>
              <div className="text-teal-300 font-bold">{selectedModel.calibration}</div>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
              <span className="text-[9px] text-slate-400 uppercase">TRAINING DATASET CORPUS</span>
              <div className="text-white font-bold">{selectedModel.dataset}</div>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
              <span className="text-[9px] text-slate-400 uppercase">PIPELINE LINEAGE</span>
              <div className="text-cyan-400 font-bold flex items-center space-x-1.5">
                <GitBranch className="w-3.5 h-3.5 text-cyan-400" />
                <span>{selectedModel.pipeline}</span>
              </div>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
