import React from 'react';
import { Target, Zap } from 'lucide-react';
import { getUIText } from '../../utils/translations';

export default function RiskFactorCard({ factors, language = 'en' }) {
  let items = factors;
  if (typeof items === 'string') {
    try { items = JSON.parse(items); } catch (e) {}
  }
  if (!items || !Array.isArray(items) || items.length === 0) return null;

  return (
    <div className="bg-[#0D0A1A]/90 border border-purple-900/40 rounded-2xl p-5 shadow-xl backdrop-blur-md">
      <div className="flex items-center space-x-2 border-b border-purple-900/30 pb-3 mb-4">
        <Target className="w-5 h-5 text-teal-400" />
        <h3 className="text-sm font-mono font-bold text-teal-200 uppercase tracking-wider">
          🎯 {getUIText('key_factors_title', language)}
        </h3>
      </div>

      <div className="flex flex-wrap gap-2.5">
        {items.map((f, i) => {
          const fn = (f.feature_name || '').replace('_', ' ').toUpperCase();
          const shapVal = f.abs_shap_value ? `+${f.abs_shap_value.toFixed(3)}` : null;

          return (
            <div 
              key={i} 
              className="flex items-center space-x-2 px-3 py-2 rounded-xl bg-[#14112B] border border-teal-500/30 text-xs font-mono text-slate-200 shadow-md hover:border-teal-400 transition"
            >
              <Zap className="w-3.5 h-3.5 text-teal-400 flex-shrink-0" />
              <span className="font-bold text-teal-300">{fn}</span>
              {shapVal && (
                <span className="text-[10px] bg-teal-950/80 text-teal-400 px-1.5 py-0.5 rounded border border-teal-800">
                  SHAP {shapVal}
                </span>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
