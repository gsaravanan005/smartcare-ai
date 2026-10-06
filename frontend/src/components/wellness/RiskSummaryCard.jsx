import React from 'react';
import { Activity, HeartPulse, Stethoscope } from 'lucide-react';
import { getUIText } from '../../utils/translations';

export default function RiskSummaryCard({ riskSummary, language = 'en' }) {
  if (!riskSummary) return null;

  const getRiskBadge = (category, pct) => {
    const cat = (category || '').toUpperCase();
    if (cat === 'HIGH' || pct >= 60) {
      return 'bg-rose-500/20 text-rose-300 border-rose-500/50 shadow-rose-900/30';
    }
    if (cat === 'MODERATE' || pct >= 30) {
      return 'bg-amber-500/20 text-amber-300 border-amber-500/50 shadow-amber-900/30';
    }
    return 'bg-emerald-500/20 text-emerald-300 border-emerald-500/50 shadow-emerald-900/30';
  };

  const getProgressColor = (category, pct) => {
    const cat = (category || '').toUpperCase();
    if (cat === 'HIGH' || pct >= 60) return 'from-rose-500 to-red-600';
    if (cat === 'MODERATE' || pct >= 30) return 'from-amber-400 to-orange-500';
    return 'from-emerald-400 to-teal-500';
  };

  const diseases = [
    { key: 'diabetes', title: 'Diabetes Risk', icon: Activity, data: riskSummary.diabetes },
    { key: 'cardio', title: 'Cardiovascular (CVD) Risk', icon: HeartPulse, data: riskSummary.cardio },
    { key: 'ckd', title: 'Chronic Kidney (CKD) Risk', icon: Stethoscope, data: riskSummary.ckd }
  ];

  return (
    <div className="bg-[#0D0A1A]/90 border border-purple-900/40 rounded-2xl p-5 shadow-xl backdrop-blur-md">
      <div className="flex items-center space-x-2 border-b border-purple-900/30 pb-3 mb-4">
        <Activity className="w-5 h-5 text-purple-400" />
        <h3 className="text-sm font-mono font-bold text-purple-200 uppercase tracking-wider">
          📊 {getUIText('risk_summary_title', language)}
        </h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {diseases.map(({ key, title, icon: Icon, data }) => {
          if (!data) return null;
          const pct = data.risk_percentage ?? round((data.probability || 0) * 100, 1);
          const category = data.risk_category || (pct >= 60 ? 'HIGH' : pct >= 30 ? 'MODERATE' : 'LOW');
          const categoryLocalized = getUIText(category === 'HIGH' ? 'High' : category === 'MODERATE' ? 'Medium' : 'Low', language);

          return (
            <div key={key} className="bg-[#130F26] border border-[#29213F] rounded-xl p-4 flex flex-col justify-between space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="p-1.5 rounded-lg bg-purple-950/60 border border-purple-800/50">
                    <Icon className="w-4 h-4 text-purple-300" />
                  </div>
                  <span className="text-xs font-bold text-slate-200">{title}</span>
                </div>
                <span className={`px-2 py-0.5 rounded-md text-[10px] font-mono font-extrabold border ${getRiskBadge(category, pct)}`}>
                  {categoryLocalized}
                </span>
              </div>

              <div className="space-y-1.5">
                <div className="flex items-baseline justify-between">
                  <span className="text-2xl font-mono font-extrabold text-white">{pct}%</span>
                  <span className="text-[10px] text-slate-400 font-mono">Prob: {data.probability}</span>
                </div>
                <div className="w-full h-2 rounded-full bg-slate-900 overflow-hidden border border-slate-800">
                  <div 
                    className={`h-full rounded-full bg-gradient-to-r ${getProgressColor(category, pct)} transition-all duration-500`}
                    style={{ width: `${Math.min(100, Math.max(5, pct))}%` }}
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function round(val, dec) {
  return Number(Math.round(val + 'e' + dec) + 'e-' + dec);
}
