import React from 'react';
import { CheckSquare } from 'lucide-react';
import { getUIText } from '../../utils/translations';

export default function DailyHabitsCard({ habits, language = 'en' }) {
  let items = habits;
  if (typeof items === 'string') {
    try { items = JSON.parse(items); } catch (e) {}
  }
  if (!items || !Array.isArray(items) || items.length === 0) return null;

  return (
    <div className="bg-[#0D0A1A]/90 border border-purple-900/40 rounded-2xl p-5 shadow-xl backdrop-blur-md space-y-4">
      <div className="flex items-center space-x-2 border-b border-purple-900/30 pb-3">
        <CheckSquare className="w-5 h-5 text-teal-400" />
        <h3 className="text-sm font-mono font-bold text-teal-200 uppercase tracking-wider">
          🌱 {getUIText('habits_title', language)}
        </h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5">
        {items.map((habit, i) => (
          <div key={i} className="bg-[#130F26] border border-[#29213F] hover:border-teal-500/40 rounded-xl p-3.5 space-y-2 flex items-start space-x-3 transition">
            <div className="p-1.5 rounded-lg bg-teal-950/60 border border-teal-800/50 text-teal-400 flex-shrink-0 mt-0.5">
              <CheckSquare className="w-4 h-4" />
            </div>

            <div className="space-y-1">
              <div className="flex items-center justify-between gap-1 flex-wrap">
                <span className="text-xs font-bold text-teal-300 font-mono">{habit.title}</span>
                <div className="flex items-center space-x-1">
                  {habit.related_risk_factor && (
                    <span className="text-[9px] font-mono text-purple-300 bg-purple-950/80 px-1.5 py-0.5 rounded border border-purple-800/60">
                      {habit.related_risk_factor}
                    </span>
                  )}
                  <span className="text-[9px] font-mono text-slate-400 bg-slate-900 px-1.5 py-0.5 rounded border border-slate-800">
                    {habit.category}
                  </span>
                </div>
              </div>
              <p className="text-xs text-slate-200 font-sans leading-relaxed">
                {habit.description}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
