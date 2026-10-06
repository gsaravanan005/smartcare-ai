import React from 'react';

export default function HolographicHUDPanel({ 
  children, 
  title = null, 
  subtitle = null,
  headerAction = null,
  glowColor = 'purple', // purple | neon | teal | red | amber
  className = '',
  style = {}
}) {
  const getGlowBorder = () => {
    switch (glowColor) {
      case 'red':
        return 'border-red-500/40 hover:border-red-500/70 shadow-red-500/10';
      case 'neon':
        return 'border-[#E879F9]/40 hover:border-[#E879F9]/70 shadow-[#E879F9]/10';
      case 'teal':
        return 'border-[#22C55E]/40 hover:border-[#22C55E]/70 shadow-[#22C55E]/10';
      case 'amber':
        return 'border-amber-500/40 hover:border-amber-500/70 shadow-amber-500/10';
      case 'purple':
      default:
        return 'border-[#2A1A4E] hover:border-[#7C3AED] shadow-[#7C3AED]/15';
    }
  };

  const getAccentColor = () => {
    switch (glowColor) {
      case 'red': return 'bg-red-400';
      case 'neon': return 'bg-[#E879F9]';
      case 'teal': return 'bg-[#22C55E]';
      case 'amber': return 'bg-amber-400';
      case 'purple':
      default: return 'bg-[#C084FC]';
    }
  };

  return (
    <div 
      style={style}
      className={`relative group rounded-2xl backdrop-blur-xl bg-[#0D0718]/85 border ${getGlowBorder()} p-4 md:p-5 shadow-2xl transition-all duration-300 ${className}`}
    >
      {/* Corner Brackets */}
      <div className="absolute top-0 left-0 w-2.5 h-2.5 border-t-2 border-l-2 border-[#7C3AED]/60 rounded-tl-2xl pointer-events-none" />
      <div className="absolute top-0 right-0 w-2.5 h-2.5 border-t-2 border-r-2 border-[#7C3AED]/60 rounded-tr-2xl pointer-events-none" />
      <div className="absolute bottom-0 left-0 w-2.5 h-2.5 border-b-2 border-l-2 border-[#7C3AED]/60 rounded-bl-2xl pointer-events-none" />
      <div className="absolute bottom-0 right-0 w-2.5 h-2.5 border-b-2 border-r-2 border-[#7C3AED]/60 rounded-br-2xl pointer-events-none" />

      {/* Inner Glow Light Layer */}
      <div className="absolute inset-0 rounded-2xl bg-gradient-to-b from-[#7C3AED]/[0.04] to-transparent pointer-events-none" />

      {/* Panel Header */}
      {(title || subtitle || headerAction) && (
        <div className="flex items-center justify-between border-b border-[#2A1A4E] pb-3 mb-3 relative z-10">
          <div>
            {title && (
              <h3 className="text-xs font-extrabold text-white uppercase tracking-widest flex items-center space-x-2">
                <span className={`w-1.5 h-1.5 rounded-full ${getAccentColor()} animate-pulse`} />
                <span>{title}</span>
              </h3>
            )}
            {subtitle && (
              <p className="text-[10px] font-mono text-purple-300/80 mt-0.5">{subtitle}</p>
            )}
          </div>
          {headerAction && <div>{headerAction}</div>}
        </div>
      )}

      {/* Panel Content Body */}
      <div className="relative z-10">{children}</div>
    </div>
  );
}
