import React, { useState, useEffect } from 'react';
import { recommendationAPI } from '../services/api';
import LanguageSelector from '../components/wellness/LanguageSelector';
import RiskSummaryCard from '../components/wellness/RiskSummaryCard';
import RiskFactorCard from '../components/wellness/RiskFactorCard';
import RecommendationSection from '../components/wellness/RecommendationSection';
import DailyFoodPlanCard from '../components/wellness/DailyFoodPlanCard';
import ExercisePlanCard from '../components/wellness/ExercisePlanCard';
import DailyHabitsCard from '../components/wellness/DailyHabitsCard';
import HerbalWellnessCard from '../components/wellness/HerbalWellnessCard';
import MonitoringCard from '../components/wellness/MonitoringCard';
import ClinicalFollowupAlert from '../components/wellness/ClinicalFollowupAlert';
import SafetyNoticeCard from '../components/wellness/SafetyNoticeCard';
import ScrollRevealSection from '../components/wellness/ScrollRevealSection';
import { getUIText } from '../utils/translations';
import { 
  Sparkles, RefreshCw, HeartHandshake, ArrowLeft, AlertCircle, CheckCircle2,
  Activity, Layers, Utensils, Leaf, CheckSquare, ChevronDown
} from 'lucide-react';

export default function PersonalizedWellnessPlan({ user, currentAssessment, onNavigate }) {
  const [loading, setLoading] = useState(true);
  const [planData, setPlanData] = useState(null);
  const [error, setError] = useState(null);
  const [language, setLanguage] = useState(() => {
    return localStorage.getItem('smartcare_language') || 'en';
  });

  const fetchPlan = async (selectedLang = language) => {
    setLoading(true);
    setError(null);
    try {
      const predId = currentAssessment?.prediction_id || currentAssessment?.assessment_id;
      const res = await recommendationAPI.generatePlan({
        patient_id: user?.patient_profile?.id || user?.id,
        prediction_id: predId,
        language: selectedLang
      });
      setPlanData(res.data);
    } catch (err) {
      console.error("Error generating wellness plan:", err);
      setError(err.response?.data?.detail || "Failed to load personalized wellness plan. Please try running risk assessment first.");
    } finally {
      setLoading(false);
    }
  };

  const handleLanguageChange = (newLang) => {
    setLanguage(newLang);
    localStorage.setItem('smartcare_language', newLang);
    fetchPlan(newLang);
  };

  useEffect(() => {
    fetchPlan(language);
  }, [currentAssessment]);

  const navItems = [
    { id: 'risk-section', titleKey: 'risk_summary_title', defaultTitle: 'Risk Profile', icon: Activity },
    { id: 'recommendations-section', titleKey: 'tailored_title', defaultTitle: 'Tailored Recommendations', icon: Layers },
    { id: 'food-section', titleKey: 'food_plan_title', defaultTitle: 'Daily Food Plan', icon: Utensils },
    { id: 'exercise-section', titleKey: 'exercise_plan_title', defaultTitle: 'Exercise & Good Habits', icon: CheckSquare },
    { id: 'herbal-section', titleKey: 'herbal_title', defaultTitle: 'Herbal Wellness & Monitoring', icon: Leaf }
  ];

  const scrollToSection = (sectionId) => {
    const el = document.getElementById(sectionId);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  if (loading && !planData) {
    return (
      <div className="w-full min-h-[60vh] flex flex-col items-center justify-center space-y-4 font-mono text-xs">
        <div className="w-12 h-12 rounded-full border-2 border-purple-500 border-t-transparent animate-spin" />
        <div className="text-purple-300 font-bold uppercase tracking-widest animate-pulse">
          GENERATING PERSONALIZED WELLNESS & DAILY GUIDANCE FROM AI RISK & SHAP ATTRIBUTIONS...
        </div>
      </div>
    );
  }

  if (error && !planData) {
    return (
      <div className="w-full space-y-6 pb-12 font-sans">
        <div className="bg-rose-950/40 border border-rose-800/60 rounded-2xl p-6 text-center space-y-4 max-w-xl mx-auto mt-8">
          <AlertCircle className="w-12 h-12 text-rose-400 mx-auto" />
          <div className="space-y-1">
            <h3 className="text-lg font-bold text-white">Wellness Plan Unavailable</h3>
            <p className="text-xs text-rose-200">{error}</p>
          </div>
          <div className="flex items-center justify-center gap-3 pt-2">
            <button
              onClick={() => onNavigate && onNavigate('risk')}
              className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold font-mono uppercase tracking-wider transition cursor-pointer"
            >
              Run Risk Assessment
            </button>
            <button
              onClick={() => fetchPlan(language)}
              className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold font-mono uppercase tracking-wider transition cursor-pointer flex items-center space-x-1"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Retry</span>
            </button>
          </div>
        </div>
      </div>
    );
  }

  const {
    risk_summary,
    modifiable_factors,
    recommendations,
    daily_food_plan,
    exercise_plan,
    daily_habits,
    herbal_wellness,
    monitoring_guidance,
    clinical_followup_required,
    clinical_followup_message,
    disclaimer,
    timestamp
  } = planData || {};

  return (
    <div className="w-full space-y-8 z-10 font-sans pb-16">
      
      {/* 1. PAGE HEADER BAR & LANGUAGE SELECTOR */}
      <div className="bg-gradient-to-r from-[#0D0A1A] via-[#140F2E] to-[#0D0A1A] border border-[#2B2347] rounded-3xl p-6 sm:p-8 shadow-2xl relative overflow-hidden">
        <div className="absolute top-0 right-0 p-8 opacity-5 pointer-events-none">
          <HeartHandshake className="w-64 h-64 text-purple-400" />
        </div>

        <div className="relative z-10 space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center space-x-3">
              <div className="p-3 rounded-2xl bg-purple-600/20 border border-purple-500/40 text-purple-300 shadow-lg shadow-purple-900/30">
                <Sparkles className="w-6 h-6" />
              </div>
              <div>
                <span className="text-[11px] font-mono font-extrabold uppercase tracking-widest text-purple-400 bg-purple-950/60 px-2.5 py-0.5 rounded-md border border-purple-800/50">
                  {getUIText('module4_badge', language)}
                </span>
                <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight pt-1">
                  {getUIText('page_title', language)}
                </h1>
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-3">
              <LanguageSelector 
                currentLanguage={language} 
                onLanguageChange={handleLanguageChange} 
              />

              <button
                onClick={() => fetchPlan(language)}
                disabled={loading}
                className="px-3.5 py-1.5 rounded-xl bg-[#1A1536] hover:bg-[#251F4A] border border-[#372E5C] text-slate-200 text-xs font-mono font-bold flex items-center space-x-1.5 transition cursor-pointer shadow-md disabled:opacity-50"
              >
                <RefreshCw className={`w-3.5 h-3.5 text-purple-400 ${loading ? 'animate-spin' : ''}`} />
                <span>{getUIText('reevaluate_btn', language)}</span>
              </button>

              {onNavigate && (
                <button
                  onClick={() => onNavigate('dashboard')}
                  className="px-3.5 py-1.5 rounded-xl bg-purple-600/30 hover:bg-purple-600/40 border border-purple-500/50 text-purple-200 text-xs font-mono font-bold flex items-center space-x-1 transition cursor-pointer"
                >
                  <ArrowLeft className="w-3.5 h-3.5" />
                  <span>{getUIText('dashboard_btn', language)}</span>
                </button>
              )}
            </div>
          </div>

          <p className="text-sm text-slate-300 max-w-3xl font-sans leading-relaxed">
            {getUIText('page_subtitle', language)}
          </p>

          {timestamp && (
            <div className="text-[10px] font-mono text-slate-400 flex items-center space-x-2 pt-1">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
              <span>{getUIText('generated_on', language)} {new Date(timestamp).toLocaleString()}</span>
            </div>
          )}
        </div>
      </div>

      {/* 2. SECTION NAVIGATION QUICK LINKS */}
      <div className="bg-[#0D0A1A]/80 border border-purple-900/40 rounded-2xl p-3 shadow-lg backdrop-blur-md sticky top-4 z-20 overflow-x-auto scrollbar-thin">
        <div className="flex items-center space-x-2 min-w-max">
          {navItems.map((item) => {
            const ItemIcon = item.icon;
            const title = getUIText(item.titleKey, language) || item.defaultTitle;
            return (
              <button
                key={item.id}
                onClick={() => scrollToSection(item.id)}
                className="flex items-center space-x-2 px-3.5 py-2 rounded-xl bg-[#141029] hover:bg-[#211A42] border border-[#2B2347] hover:border-purple-500/50 text-xs font-mono font-bold text-slate-300 hover:text-white transition cursor-pointer"
              >
                <ItemIcon className="w-4 h-4 text-purple-400" />
                <span>{title}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* 3. SCROLL-REVEAL SECTIONS */}
      <div className="space-y-12">
        
        {/* SECTION 1: RISK PROFILE & MODIFIABLE FACTORS */}
        <ScrollRevealSection id="risk-section" className="space-y-6">
          {clinical_followup_required && (
            <ClinicalFollowupAlert message={clinical_followup_message} language={language} />
          )}
          <RiskSummaryCard riskSummary={risk_summary} language={language} />
          <RiskFactorCard factors={modifiable_factors} language={language} />
        </ScrollRevealSection>

        {/* SECTION 2: TAILORED RECOMMENDATIONS */}
        <ScrollRevealSection id="recommendations-section" className="space-y-6">
          <RecommendationSection recommendations={recommendations} language={language} />
        </ScrollRevealSection>

        {/* SECTION 3: DAILY FOOD PLAN */}
        <ScrollRevealSection id="food-section" className="space-y-6">
          <DailyFoodPlanCard foodPlan={daily_food_plan} language={language} />
        </ScrollRevealSection>

        {/* SECTION 4: EXERCISE & GOOD DAILY HABITS */}
        <ScrollRevealSection id="exercise-section" className="space-y-6">
          <ExercisePlanCard exercisePlan={exercise_plan} language={language} />
          <DailyHabitsCard habits={daily_habits} language={language} />
        </ScrollRevealSection>

        {/* SECTION 5: HERBAL WELLNESS & ROUTINE MONITORING & SAFETY NOTICE */}
        <ScrollRevealSection id="herbal-section" className="space-y-6">
          <HerbalWellnessCard herbalItems={herbal_wellness} language={language} />
          <MonitoringCard monitoring={monitoring_guidance} language={language} />
          <SafetyNoticeCard disclaimer={disclaimer} language={language} />
        </ScrollRevealSection>

      </div>

    </div>
  );
}
