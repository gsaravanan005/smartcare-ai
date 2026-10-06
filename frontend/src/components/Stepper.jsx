import React from 'react';
import { Check } from 'lucide-react';

export default function Stepper({ steps, currentStep, onStepClick }) {
  return (
    <div className="w-full py-4 mb-8">
      <div className="flex items-center justify-between relative">
        {/* Background Connecting Line */}
        <div className="absolute left-0 top-1/2 transform -translate-y-1/2 w-full h-1 bg-slate-800 -z-0 rounded" />
        <div 
          className="absolute left-0 top-1/2 transform -translate-y-1/2 h-1 bg-gradient-to-r from-sky-500 to-teal-400 transition-all duration-500 -z-0 rounded"
          style={{ width: `${((currentStep - 1) / (steps.length - 1)) * 100}%` }}
        />

        {steps.map((step, idx) => {
          const stepNum = idx + 1;
          const isCompleted = stepNum < currentStep;
          const isCurrent = stepNum === currentStep;

          return (
            <div 
              key={step.id} 
              onClick={() => stepNum <= currentStep && onStepClick(stepNum)}
              className={`flex flex-col items-center relative z-10 cursor-pointer group`}
            >
              <div 
                className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm transition-all duration-300 ${
                  isCompleted
                    ? 'bg-teal-500 text-slate-950 shadow-lg shadow-teal-500/30'
                    : isCurrent
                    ? 'bg-sky-500 text-slate-950 ring-4 ring-sky-500/20 shadow-lg shadow-sky-500/40'
                    : 'bg-slate-800 text-slate-400 border border-slate-700'
                }`}
              >
                {isCompleted ? <Check className="w-5 h-5 stroke-[3]" /> : stepNum}
              </div>
              <span className={`mt-2 text-xs font-medium transition-colors ${
                isCurrent ? 'text-sky-400 font-bold' : isCompleted ? 'text-teal-400' : 'text-slate-500'
              }`}>
                {step.title}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
