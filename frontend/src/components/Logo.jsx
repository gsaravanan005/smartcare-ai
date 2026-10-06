import React from 'react';

/**
 * Official SmartCare AI Logo Component
 * Source of Truth: /smartcare-logo.png (D:\SmartCare AI\SmartCare AI logo.png)
 * Preserves 100% exact artwork, aspect ratio, transparency, and dark-purple theme compatibility.
 */
export default function Logo({ 
  variant = 'full', // 'full' | 'icon' | 'avatar' | 'favicon'
  size = 'md',      // 'xs' | 'sm' | 'md' | 'lg' | 'xl' | 'avatar'
  className = '',
  alt = "SmartCare AI Official Logo"
}) {
  const sizeClasses = {
    xs: 'h-6 max-h-6',
    sm: 'h-8 max-h-8 sm:h-9 sm:max-h-9',
    md: 'h-10 max-h-10 sm:h-12 sm:max-h-12',
    lg: 'h-16 max-h-16 sm:h-20 sm:max-h-20',
    xl: 'h-28 max-h-28 sm:h-36 sm:max-h-36 md:h-44 md:max-h-44',
    avatar: 'h-7 w-7 sm:h-8 sm:w-8 max-h-8 max-w-8'
  };

  const dimensions = sizeClasses[size] || sizeClasses.md;

  if (variant === 'icon' || variant === 'avatar' || variant === 'favicon') {
    return (
      <div className={`inline-flex items-center justify-center flex-shrink-0 ${className}`}>
        <img 
          src="/smartcare-logo.png" 
          alt={alt} 
          className={`${dimensions} object-contain rounded-lg drop-shadow-md select-none pointer-events-none`}
        />
      </div>
    );
  }

  return (
    <div className={`inline-flex items-center justify-center select-none ${className}`}>
      <img 
        src="/smartcare-logo.png" 
        alt={alt} 
        className={`${dimensions} w-auto object-contain drop-shadow-xl transition-all duration-300 hover:brightness-105 pointer-events-none`}
      />
    </div>
  );
}
