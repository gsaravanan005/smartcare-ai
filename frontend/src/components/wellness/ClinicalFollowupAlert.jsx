import React from 'react';
import { ShieldAlert, AlertTriangle, Stethoscope } from 'lucide-react';
import { getUIText } from '../../utils/translations';

export default function ClinicalFollowupAlert({ message, language = 'en' }) {
  if (!message) return null;

  return (
    <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-rose-950/80 via-red-950/60 to-purple-950/80 border-2 border-rose-500/60 p-5 shadow-2xl shadow-rose-950/50 space-y-3">
      <div className="absolute top-0 right-0 p-4 opacity-10 pointer-events-none">
        <Stethoscope className="w-32 h-32 text-rose-300" />
      </div>

      <div className="flex items-start space-x-3">
        <div className="p-2 bg-rose-500/20 rounded-xl border border-rose-500/50 text-rose-300 flex-shrink-0 mt-0.5">
          <ShieldAlert className="w-6 h-6 animate-pulse" />
        </div>

        <div className="space-y-1.5 flex-1">
          <div className="flex items-center space-x-2">
            <span className="text-xs font-mono font-extrabold uppercase tracking-widest text-rose-300 bg-rose-500/20 px-2.5 py-0.5 rounded-md border border-rose-500/40">
              {getUIText('clinical_alert_badge', language)}
            </span>
            <span className="text-[11px] font-mono text-rose-200">
              {getUIText('clinical_alert_sub', language)}
            </span>
          </div>

          <h4 className="text-base font-bold text-white tracking-tight">
            {getUIText('clinical_alert_title', language)}
          </h4>

          <p className="text-xs text-rose-100/90 leading-relaxed font-sans max-w-4xl">
            {message}
          </p>
        </div>
      </div>

      <div className="bg-rose-950/60 border border-rose-800/60 rounded-xl p-3 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 text-xs font-mono text-rose-200">
        <div className="flex items-center space-x-2">
          <AlertTriangle className="w-4 h-4 text-rose-400 flex-shrink-0" />
          <span>
            {getUIText('clinical_alert_footer', language)}
          </span>
        </div>
        <span className="text-[10px] text-rose-300 font-bold bg-rose-900/60 px-2 py-1 rounded border border-rose-700/50 flex-shrink-0">
          {getUIText('seek_guidance_btn', language)}
        </span>
      </div>
    </div>
  );
}
