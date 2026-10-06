import React from 'react';
import { Globe, ChevronDown } from 'lucide-react';

export default function LanguageSelector({ currentLanguage, onLanguageChange }) {
  const languages = [
    { code: 'en', label: 'English', flag: '🇬🇧' },
    { code: 'ta', label: 'Tamil (தமிழ்)', flag: '🇮🇳' },
    { code: 'hi', label: 'Hindi (हिन्दी)', flag: '🇮🇳' },
    { code: 'te', label: 'Telugu (తెలుగు)', flag: '🇮🇳' },
    { code: 'ml', label: 'Malayalam (മലയാളം)', flag: '🇮🇳' },
    { code: 'kn', label: 'Kannada (ಕನ್ನಡ)', flag: '🇮🇳' }
  ];

  return (
    <div className="flex items-center space-x-2 bg-[#120E29] border border-[#2B2347] px-3.5 py-1.5 rounded-xl shadow-lg font-mono text-xs text-slate-200">
      <Globe className="w-4 h-4 text-purple-400 flex-shrink-0" />
      <span className="text-[11px] text-slate-400 font-bold uppercase hidden sm:inline">Language:</span>
      
      <div className="relative">
        <select
          value={currentLanguage || 'en'}
          onChange={(e) => onLanguageChange && onLanguageChange(e.target.value)}
          className="bg-[#1A1438] text-white font-bold text-xs py-1 pl-2.5 pr-7 rounded-lg border border-[#3A2F5E] cursor-pointer outline-none focus:border-purple-400 transition appearance-none"
        >
          {languages.map((lang) => (
            <option key={lang.code} value={lang.code} className="bg-[#120E29] text-white">
              {lang.flag} {lang.label}
            </option>
          ))}
        </select>
        <ChevronDown className="w-3.5 h-3.5 text-purple-300 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none" />
      </div>
    </div>
  );
}
