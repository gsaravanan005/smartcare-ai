import React from 'react';
import Live3DHealthBackground from './Live3DHealthBackground';

/**
 * WorkspaceBackground
 * Serves as the global backdrop container across the SmartCare AI application.
 * Renders the exact 3D holographic healthcare AI environment.
 */
export default function WorkspaceBackground() {
  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden bg-[#05020D]">
      <Live3DHealthBackground />
    </div>
  );
}
