import React from 'react';
import { Leaf, ShieldAlert, AlertTriangle } from 'lucide-react';
import { getUIText } from '../../utils/translations';

export default function HerbalWellnessCard({ herbalItems, language = 'en' }) {
  let items = herbalItems;
  if (typeof items === 'string') {
    try { items = JSON.parse(items); } catch (e) {}
  }
  if (!items || !Array.isArray(items) || items.length === 0) return null;

  return (
    <div className="bg-[#0D0A1A]/90 border border-purple-900/40 rounded-2xl p-5 shadow-xl backdrop-blur-md space-y-4">
      <div className="flex items-center justify-between border-b border-purple-900/30 pb-3">
        <div className="flex items-center space-x-2">
          <Leaf className="w-5 h-5 text-emerald-400" />
          <h3 className="text-sm font-mono font-bold text-emerald-200 uppercase tracking-wider">
            🌿 {getUIText('herbal_title', language)}
          </h3>
        </div>
        <span className="text-[10px] font-mono bg-emerald-950/80 text-emerald-300 px-2 py-0.5 rounded border border-emerald-800">
          {getUIText('culinary_badge', language)}
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {items.map((item, i) => (
          <div key={i} className="bg-[#130F26] border border-[#29213F] hover:border-emerald-500/40 rounded-xl p-4 space-y-2.5 transition">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Leaf className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                <h4 className="text-xs font-bold text-emerald-300 font-mono">{item.name}</h4>
              </div>
              {item.related_risk_factor && (
                <span className="text-[9px] font-mono text-purple-300 bg-purple-950/80 px-2 py-0.5 rounded border border-purple-800/60">
                  {item.related_risk_factor}
                </span>
              )}
            </div>

            <div className="space-y-1 text-xs">
              <div className="bg-[#0A0817] p-2.5 rounded-lg border border-[#1E1736] space-y-1">
                <span className="text-[10px] font-mono text-slate-400 uppercase block font-bold">
                  {getUIText('culinary_prep_header', language)}
                </span>
                <p className="text-slate-200 font-sans">{item.food_level_use}</p>
              </div>

              <div className="p-2 text-slate-300 font-sans text-xs">
                <strong>{getUIText('wellness_purpose_header', language)}</strong> {item.purpose}
              </div>
            </div>

            {item.safety_warning && (
              <div className="flex items-start space-x-1.5 text-[10px] font-mono text-amber-200 bg-amber-950/30 p-2 rounded border border-amber-800/40">
                <ShieldAlert className="w-3.5 h-3.5 text-amber-400 flex-shrink-0 mt-0.5" />
                <span>{item.safety_warning}</span>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Prominent Herbal Safety Banner */}
      <div className="bg-amber-950/40 border border-amber-800/60 rounded-xl p-3.5 flex items-start space-x-2.5 text-xs font-mono text-amber-200 shadow-md">
        <AlertTriangle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
        <p className="leading-relaxed">
          <strong>{getUIText('herbal_safety_notice_label', language)}</strong> {getUIText('herbal_safety_notice_text', language)}
        </p>
      </div>
    </div>
  );
}
