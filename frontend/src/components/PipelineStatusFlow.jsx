import React from 'react';
import { Database, Cpu, Layers, CheckCircle2, ArrowRight } from 'lucide-react';

export default function PipelineStatusFlow({ onNavigate }) {
  const PIPELINE_NODES = [
    { id: 1, title: 'Raw Data', status: 'Loaded', color: 'text-sky-400', icon: Database },
    { id: 2, title: 'Preprocessing', status: 'Complete', color: 'text-teal-400', icon: Cpu },
    { id: 3, title: 'Feature Eng.', status: 'Complete', color: 'text-purple-400', icon: Layers },
    { id: 4, title: 'Model Ready', status: 'Ready', color: 'text-teal-400', icon: CheckCircle2 }
  ];

  return (
    <div className="glass-card rounded-3xl p-6 border border-slate-800 space-y-5">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-extrabold text-white uppercase tracking-wider">PIPELINE STATUS</h3>
          <p className="text-[10px] text-slate-400">Leakage-free dataset transformation pipeline</p>
        </div>

        <button
          onClick={() => onNavigate && onNavigate('pipeline')}
          className="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 text-xs font-bold transition flex items-center space-x-1"
        >
          <span>View Pipeline</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* 4 Connected Flow Nodes */}
      <div className="grid grid-cols-4 gap-2 relative">
        <div className="absolute top-5 left-8 right-8 h-0.5 bg-gradient-to-r from-sky-500 via-teal-400 to-purple-500 z-0 opacity-40" />

        {PIPELINE_NODES.map((node) => {
          const Icon = node.icon;
          return (
            <div key={node.id} className="flex flex-col items-center text-center space-y-2 relative z-10">
              <div className="w-10 h-10 rounded-2xl bg-slate-950 border border-slate-800 flex items-center justify-center shadow-lg group-hover:scale-105 transition">
                <Icon className={`w-5 h-5 ${node.color}`} />
              </div>
              <div>
                <div className="text-xs font-extrabold text-white">{node.title}</div>
                <div className="text-[10px] text-teal-400 font-semibold">{node.status}</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
