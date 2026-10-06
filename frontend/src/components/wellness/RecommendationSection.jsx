import React from 'react';
import RecommendationCard from './RecommendationCard';
import { Layers } from 'lucide-react';
import { getUIText } from '../../utils/translations';

export default function RecommendationSection({ recommendations, language = 'en' }) {
  if (!recommendations || recommendations.length === 0) return null;

  return (
    <div className="space-y-4">
      <div className="flex items-center space-x-2 border-b border-purple-900/40 pb-2">
        <Layers className="w-5 h-5 text-purple-400" />
        <h3 className="text-sm font-mono font-bold text-purple-200 uppercase tracking-wider">
          {getUIText('tailored_title', language)} ({recommendations.length})
        </h3>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {recommendations.map((rec, i) => (
          <RecommendationCard key={rec.id || i} recommendation={rec} language={language} />
        ))}
      </div>
    </div>
  );
}
