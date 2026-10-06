import React from 'react';
import { Activity, Sunrise, Sun, Moon, ShieldAlert } from 'lucide-react';
import { getUIText } from '../../utils/translations';

export default function ExercisePlanCard({ exercisePlan, language = 'en' }) {
  let plan = exercisePlan;
  if (typeof plan === 'string') {
    try { plan = JSON.parse(plan); } catch (e) {}
  }
  if (!plan) return null;

  const sessions = [
    { key: 'morning', titleKey: 'morning_movement', icon: Sunrise, data: plan.morning },
    { key: 'afternoon', titleKey: 'afternoon_activity', icon: Sun, data: plan.afternoon },
    { key: 'evening', titleKey: 'evening_stretch', icon: Moon, data: plan.evening }
  ];

  return (
    <div className="bg-[#0D0A1A]/90 border border-purple-900/40 rounded-2xl p-5 shadow-xl backdrop-blur-md space-y-4">
      <div className="flex items-center space-x-2 border-b border-purple-900/30 pb-3">
        <Activity className="w-5 h-5 text-emerald-400" />
        <h3 className="text-sm font-mono font-bold text-emerald-200 uppercase tracking-wider">
          🏃 {getUIText('exercise_plan_title', language)}
        </h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {sessions.map(({ key, titleKey, icon: Icon, data }) => {
          if (!data) return null;
          const sessionTitle = data.time_of_day || getUIText(titleKey, language);

          return (
            <div key={key} className="bg-[#130F26] border border-[#29213F] hover:border-emerald-500/40 rounded-xl p-4 space-y-3 flex flex-col justify-between transition">
              <div className="space-y-2">
                <div className="flex items-center justify-between border-b border-[#1F1936] pb-2">
                  <div className="flex items-center space-x-2">
                    <div className="p-1.5 rounded-lg bg-emerald-950/60 border border-emerald-800/50">
                      <Icon className="w-4 h-4 text-emerald-300" />
                    </div>
                    <span className="text-xs font-mono font-bold text-emerald-300">{sessionTitle}</span>
                  </div>
                  <div className="flex items-center space-x-1.5">
                    {data.related_risk_factor && (
                      <span className="text-[9px] font-mono text-purple-300 bg-purple-950/80 px-1.5 py-0.5 rounded border border-purple-800/60">
                        {data.related_risk_factor}
                      </span>
                    )}
                    <span className="text-[10px] font-mono text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800">
                      {data.intensity}
                    </span>
                  </div>
                </div>

                <p className="text-xs text-slate-100 font-sans leading-relaxed font-bold">
                  {data.activity}
                </p>

                <div className="flex flex-wrap gap-2 text-[10px] font-mono text-slate-300">
                  <span className="bg-[#0A0817] px-2 py-1 rounded border border-[#1E1736]">
                    {getUIText('duration_label', language)} <strong>{data.duration}</strong>
                  </span>
                  <span className="bg-[#0A0817] px-2 py-1 rounded border border-[#1E1736]">
                    {getUIText('frequency_label', language)} <strong>{data.frequency}</strong>
                  </span>
                </div>
              </div>

              {data.safety_note && (
                <div className="text-[10px] font-mono text-slate-400 bg-emerald-950/20 p-2 rounded border border-emerald-900/30 flex items-start space-x-1.5">
                  <ShieldAlert className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0 mt-0.5" />
                  <span>{data.safety_note}</span>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {plan.general_safety_warning && (
        <div className="bg-rose-950/30 border border-rose-800/50 rounded-xl p-3 flex items-start space-x-2 text-xs font-mono text-rose-200">
          <ShieldAlert className="w-4 h-4 text-rose-400 flex-shrink-0 mt-0.5" />
          <span>{plan.general_safety_warning}</span>
        </div>
      )}
    </div>
  );
}
