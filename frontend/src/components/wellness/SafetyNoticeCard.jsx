import React from 'react';
import { ShieldCheck } from 'lucide-react';
import { getUIText } from '../../utils/translations';

export default function SafetyNoticeCard({ disclaimer, language = 'en' }) {
  return (
    <div className="bg-[#0A0817] border border-[#231C3D] rounded-2xl p-4 flex items-start space-x-3 text-xs text-slate-400 font-mono shadow-md">
      <ShieldCheck className="w-5 h-5 text-purple-400 flex-shrink-0 mt-0.5" />
      <div className="space-y-1">
        <span className="text-purple-300 font-bold uppercase tracking-wider block">
          {getUIText('safety_notice_title', language)}
        </span>
        <p className="leading-relaxed">
          {disclaimer || getUIText('disclaimer_text', language)}
        </p>
      </div>
    </div>
  );
}
