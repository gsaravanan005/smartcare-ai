import React from 'react';
import { Clock, Calendar, CheckSquare } from 'lucide-react';
import { getUIText } from '../../utils/translations';

export default function MonitoringCard({ monitoring, language = 'en' }) {
  let items = monitoring;
  if (typeof items === 'string') {
    try { items = JSON.parse(items); } catch (e) {}
  }
  if (!items || !Array.isArray(items) || items.length === 0) return null;

  return (
    <div className="bg-[#0D0A1A]/90 border border-purple-900/40 rounded-2xl p-5 shadow-xl backdrop-blur-md space-y-4">
      <div className="flex items-center space-x-2 border-b border-purple-900/30 pb-3">
        <Clock className="w-5 h-5 text-cyan-400" />
        <h3 className="text-sm font-mono font-bold text-cyan-200 uppercase tracking-wider">
          📊 {getUIText('monitoring_title', language)}
        </h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {items.map((m, i) => (
          <div key={i} className="bg-[#130F26] border border-[#29213F] rounded-xl p-4 space-y-2 flex flex-col justify-between">
            <div className="space-y-1">
              <div className="flex items-center justify-between gap-2">
                <span className="text-xs font-bold text-cyan-300 font-mono flex items-center space-x-1">
                  <CheckSquare className="w-3.5 h-3.5 text-cyan-400 flex-shrink-0" />
                  <span>{m.parameter}</span>
                </span>
                {m.related_risk_factor && (
                  <span className="text-[9px] font-mono text-purple-300 bg-purple-950/80 px-2 py-0.5 rounded border border-purple-800/60">
                    {m.related_risk_factor}
                  </span>
                )}
              </div>
              <p className="text-xs text-slate-300 font-sans leading-relaxed pt-1">
                {m.guidance}
              </p>
            </div>

            <div className="flex items-center space-x-1.5 pt-2 border-t border-[#1F1936] text-[10px] font-mono text-cyan-400">
              <Calendar className="w-3 h-3 text-cyan-400" />
              <span>{getUIText('recommended_freq_label', language)} <strong>{m.frequency}</strong></span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
