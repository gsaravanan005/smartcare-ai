import React from 'react';
import { Utensils, Coffee, Sun, Sunset, Moon, ShieldAlert } from 'lucide-react';
import { getUIText } from '../../utils/translations';

export default function DailyFoodPlanCard({ foodPlan, language = 'en' }) {
  let plan = foodPlan;
  if (typeof plan === 'string') {
    try { plan = JSON.parse(plan); } catch (e) {}
  }
  if (!plan) return null;

  const meals = [
    { key: 'breakfast', defaultTitle: 'Breakfast', icon: Coffee, data: plan.breakfast },
    { key: 'mid_morning', defaultTitle: 'Mid-Morning', icon: Sun, data: plan.mid_morning },
    { key: 'lunch', defaultTitle: 'Lunch', icon: Utensils, data: plan.lunch },
    { key: 'evening_snack', defaultTitle: 'Evening Snack', icon: Sunset, data: plan.evening_snack },
    { key: 'dinner', defaultTitle: 'Dinner', icon: Moon, data: plan.dinner }
  ];

  return (
    <div className="bg-[#0D0A1A]/90 border border-purple-900/40 rounded-2xl p-5 shadow-xl backdrop-blur-md space-y-4">
      <div className="flex items-center space-x-2 border-b border-purple-900/30 pb-3">
        <Utensils className="w-5 h-5 text-amber-400" />
        <h3 className="text-sm font-mono font-bold text-amber-200 uppercase tracking-wider">
          🍽️ {getUIText('food_plan_title', language)}
        </h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {meals.map(({ key, defaultTitle, icon: Icon, data }) => {
          if (!data) return null;
          const mealTitle = data.meal_localized || getUIText(key, language) || data.meal || defaultTitle;

          return (
            <div key={key} className="bg-[#130F26] border border-[#29213F] hover:border-amber-500/40 rounded-xl p-4 space-y-2.5 flex flex-col justify-between transition">
              <div className="space-y-2">
                <div className="flex items-center justify-between border-b border-[#1F1936] pb-2">
                  <div className="flex items-center space-x-2">
                    <div className="p-1.5 rounded-lg bg-amber-950/60 border border-amber-800/50">
                      <Icon className="w-4 h-4 text-amber-300" />
                    </div>
                    <span className="text-xs font-mono font-bold text-amber-300">{mealTitle}</span>
                  </div>
                  {data.related_risk_factor && (
                    <span className="text-[9px] font-mono text-purple-300 bg-purple-950/80 px-2 py-0.5 rounded border border-purple-800/60">
                      {getUIText('target_factor', language)} {data.related_risk_factor}
                    </span>
                  )}
                </div>

                <p className="text-xs text-slate-100 font-sans leading-relaxed">
                  {data.suggestion}
                </p>

                <div className="bg-[#0A0817] p-2.5 rounded-lg border border-[#1E1736] text-[11px] text-slate-300 font-sans space-y-1">
                  <strong className="text-amber-400 font-mono text-[10px] uppercase block">
                    {getUIText('why_suitable', language)}
                  </strong>
                  <span>{data.why}</span>
                  {data.why_relevant && (
                    <p className="text-[10px] text-purple-300 font-mono pt-1 border-t border-[#1F1936]">
                      <strong>{getUIText('risk_driver_link', language)}</strong> {data.why_relevant}
                    </p>
                  )}
                </div>
              </div>

              {data.safety_note && (
                <div className="flex items-start space-x-1.5 text-[10px] font-mono text-amber-200 bg-amber-950/30 p-2 rounded border border-amber-800/40 mt-1">
                  <ShieldAlert className="w-3.5 h-3.5 text-amber-400 flex-shrink-0 mt-0.5" />
                  <span>{data.safety_note}</span>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
