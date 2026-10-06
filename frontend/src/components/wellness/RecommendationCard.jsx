import React from 'react';
import { Sparkles, HelpCircle, ShieldCheck, Tag, Info } from 'lucide-react';
import { getUIText } from '../../utils/translations';

export default function RecommendationCard({ recommendation, language = 'en' }) {
  if (!recommendation) return null;

  const {
    category,
    risk_factor,
    source_feature,
    patient_value,
    shap_value,
    effect_direction,
    recommendation: text,
    reason,
    priority,
    priority_localized,
    related_disease,
    safety_note
  } = recommendation;

  const getPriorityBadge = (prio) => {
    const p = (prio || 'Medium').toLowerCase();
    if (p === 'high') {
      return 'bg-rose-500/20 text-rose-300 border-rose-500/50 shadow-rose-900/20';
    }
    if (p === 'low') {
      return 'bg-emerald-500/20 text-emerald-300 border-emerald-500/50 shadow-emerald-900/20';
    }
    return 'bg-amber-500/20 text-amber-300 border-amber-500/50 shadow-amber-900/20';
  };

  const prioText = priority_localized || priority;

  return (
    <div className="bg-[#110D24] border border-[#2B2347] hover:border-purple-500/50 rounded-2xl p-5 space-y-4 shadow-lg transition-all duration-200">
      
      {/* Top Header Row */}
      <div className="flex items-start justify-between gap-3 border-b border-[#231C3B] pb-3">
        <div className="space-y-1">
          <div className="flex items-center space-x-2">
            <span className="px-2 py-0.5 rounded-md bg-purple-950/80 text-purple-300 border border-purple-800/60 text-[10px] font-mono font-bold tracking-wide uppercase">
              {category}
            </span>
            {related_disease && (
              <span className="px-2 py-0.5 rounded-md bg-slate-900 text-slate-400 border border-slate-800 text-[10px] font-mono">
                {related_disease}
              </span>
            )}
          </div>
          <h4 className="text-base font-bold text-white tracking-tight flex items-center space-x-1.5 pt-1">
            <span>{risk_factor}</span>
          </h4>
        </div>

        <div className="flex-shrink-0">
          <span className={`px-2.5 py-1 rounded-lg text-xs font-mono font-extrabold border ${getPriorityBadge(priority)}`}>
            {getUIText('priority_label', language)} {prioText}
          </span>
        </div>
      </div>

      {/* SHAP Traceability / Patient Measurement Strip */}
      {(source_feature || patient_value || shap_value !== undefined) && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 bg-[#080612] p-2.5 rounded-xl border border-[#1F1838] text-[11px] font-mono">
          {source_feature && (
            <div>
              <span className="text-[9px] text-slate-400 block uppercase font-semibold">Source Feature:</span>
              <span className="text-purple-300 font-bold">{source_feature}</span>
            </div>
          )}
          {patient_value && (
            <div>
              <span className="text-[9px] text-slate-400 block uppercase font-semibold">Patient Value:</span>
              <span className="text-teal-300 font-bold">{patient_value}</span>
            </div>
          )}
          {shap_value !== undefined && shap_value !== null && (
            <div>
              <span className="text-[9px] text-slate-400 block uppercase font-semibold">SHAP Contribution:</span>
              <span className={`font-bold ${shap_value > 0 ? 'text-rose-400' : 'text-emerald-400'}`}>
                {shap_value > 0 ? `+${typeof shap_value === 'number' ? shap_value.toFixed(4) : shap_value}` : (typeof shap_value === 'number' ? shap_value.toFixed(4) : shap_value)}
              </span>
            </div>
          )}
          {effect_direction && (
            <div>
              <span className="text-[9px] text-slate-400 block uppercase font-semibold">Effect Direction:</span>
              <span className="text-amber-300 font-bold">{effect_direction}</span>
            </div>
          )}
        </div>
      )}

      {/* Recommendation Body */}
      <div className="space-y-2">
        <div className="text-xs font-mono uppercase tracking-wider text-purple-400 font-bold flex items-center space-x-1">
          <Sparkles className="w-3.5 h-3.5 text-purple-400" />
          <span>{getUIText('guidance_label', language)}</span>
        </div>
        <p className="text-sm text-slate-200 leading-relaxed font-sans bg-[#0A0817] p-3.5 rounded-xl border border-[#1E1736]">
          {text}
        </p>
      </div>

      {/* Reason ("Why this was suggested") */}
      <div className="space-y-1 bg-[#16122E]/80 p-3 rounded-xl border border-[#272045] text-xs">
        <div className="flex items-center space-x-1 text-slate-400 font-mono font-bold text-[11px] uppercase">
          <HelpCircle className="w-3.5 h-3.5 text-teal-400" />
          <span>{getUIText('why_suggested_label', language)}</span>
        </div>
        <p className="text-slate-300 font-sans text-xs leading-normal pl-4 border-l-2 border-teal-500/50">
          {reason}
        </p>
      </div>

      {/* Optional Safety Note */}
      {safety_note && (
        <div className="flex items-start space-x-2 text-[11px] text-slate-400 font-mono bg-purple-950/20 p-2.5 rounded-lg border border-purple-900/30">
          <Info className="w-3.5 h-3.5 text-purple-400 flex-shrink-0 mt-0.5" />
          <span>{safety_note}</span>
        </div>
      )}

    </div>
  );
}
