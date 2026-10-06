import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

export default function Medical3DVisualization({ className = "w-full h-80", interactive = true }) {
  const mountRef = useRef(null);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    const width = container.clientWidth || 360;
    const height = container.clientHeight || 360;

    // 1. Scene & Camera Setup
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.set(0, 1, 16);

    // 2. WebGL Renderer
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // 3. Group for Human Anatomical Scanner
    const humanGroup = new THREE.Group();
    scene.add(humanGroup);

    // 3A. Head (Icosahedron Wireframe)
    const headGeo = new THREE.IcosahedronGeometry(1.1, 2);
    const headMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true, transparent: true, opacity: 0.4 });
    const headMesh = new THREE.Mesh(headGeo, headMat);
    headMesh.position.set(0, 3.8, 0);
    humanGroup.add(headMesh);

    // 3B. Torso (Cylinder Wireframe)
    const torsoGeo = new THREE.CylinderGeometry(1.6, 1.2, 4.0, 16, 8, true);
    const torsoMat = new THREE.MeshBasicMaterial({ color: 0x0284c7, wireframe: true, transparent: true, opacity: 0.35 });
    const torsoMesh = new THREE.Mesh(torsoGeo, torsoMat);
    torsoMesh.position.set(0, 1.2, 0);
    humanGroup.add(torsoMesh);

    // 3C. Hips & Legs Wireframe
    const legsGeo = new THREE.CylinderGeometry(1.1, 0.6, 4.5, 12, 6, true);
    const legsMat = new THREE.MeshBasicMaterial({ color: 0x0369a1, wireframe: true, transparent: true, opacity: 0.3 });
    const legsMesh = new THREE.Mesh(legsGeo, legsMat);
    legsMesh.position.set(0, -2.8, 0);
    humanGroup.add(legsMesh);

    // 4. Cardiovascular Heart Node (Chest Region)
    const heartGeo = new THREE.SphereGeometry(0.55, 16, 16);
    const heartMat = new THREE.MeshBasicMaterial({ color: 0xf87171, wireframe: true, transparent: true, opacity: 0.85 });
    const heartMesh = new THREE.Mesh(heartGeo, heartMat);
    heartMesh.position.set(-0.35, 2.2, 0.6);
    humanGroup.add(heartMesh);

    // Heart Pulsing Halo
    const heartGlowGeo = new THREE.SphereGeometry(0.8, 16, 16);
    const heartGlowMat = new THREE.MeshBasicMaterial({ color: 0xef4444, transparent: true, opacity: 0.25 });
    const heartGlow = new THREE.Mesh(heartGlowGeo, heartGlowMat);
    heartGlow.position.set(-0.35, 2.2, 0.6);
    humanGroup.add(heartGlow);

    // 5. Chronic Kidney Disease Nodes (Left & Right Lumbar Region)
    const kidneyGeo = new THREE.SphereGeometry(0.38, 12, 12);
    const kidneyMat = new THREE.MeshBasicMaterial({ color: 0xc084fc, wireframe: true, transparent: true, opacity: 0.8 });
    
    const leftKidney = new THREE.Mesh(kidneyGeo, kidneyMat);
    leftKidney.position.set(-0.75, 0.4, 0.4);
    humanGroup.add(leftKidney);

    const rightKidney = new THREE.Mesh(kidneyGeo, kidneyMat);
    rightKidney.position.set(0.75, 0.4, 0.4);
    humanGroup.add(rightKidney);

    // 6. DNA Double Helix Particle Spiral
    const dnaCount = 300;
    const dnaGeo = new THREE.BufferGeometry();
    const dnaPos = new Float32Array(dnaCount * 3);
    const dnaCols = new Float32Array(dnaCount * 3);

    const cyanColor = new THREE.Color(0x38bdf8);
    const tealColor = new THREE.Color(0x2dd4bf);

    for (let i = 0; i < dnaCount; i++) {
      const t = (i / dnaCount) * Math.PI * 8.0;
      const strand = i % 2 === 0 ? 1 : -1;
      const radius = 2.4;
      const y = (i / dnaCount) * 10.0 - 5.0;

      dnaPos[i * 3] = Math.cos(t + (strand * Math.PI)) * radius;
      dnaPos[i * 3 + 1] = y;
      dnaPos[i * 3 + 2] = Math.sin(t + (strand * Math.PI)) * radius;

      const c = strand === 1 ? cyanColor : tealColor;
      dnaCols[i * 3] = c.r;
      dnaCols[i * 3 + 1] = c.g;
      dnaCols[i * 3 + 2] = c.b;
    }

    dnaGeo.setAttribute('position', new THREE.BufferAttribute(dnaPos, 3));
    dnaGeo.setAttribute('color', new THREE.BufferAttribute(dnaCols, 3));

    const dnaMat = new THREE.PointsMaterial({ size: 0.1, vertexColors: true, transparent: true, opacity: 0.75 });
    const dnaParticles = new THREE.Points(dnaGeo, dnaMat);
    scene.add(dnaParticles);

    // 7. Holographic Scanning Ring
    const scanRingGeo = new THREE.RingGeometry(2.8, 2.9, 64);
    const scanRingMat = new THREE.MeshBasicMaterial({ color: 0x2dd4bf, side: THREE.DoubleSide, transparent: true, opacity: 0.5 });
    const scanRing = new THREE.Mesh(scanRingGeo, scanRingMat);
    scanRing.rotation.x = Math.PI / 2;
    scene.add(scanRing);

    // 8. Mouse Parallax Interaction
    let mouseX = 0;
    let mouseY = 0;

    const handleMouseMove = (e) => {
      if (!interactive) return;
      const rect = container.getBoundingClientRect();
      mouseX = ((e.clientX - rect.left) / rect.width - 0.5) * 0.8;
      mouseY = ((e.clientY - rect.top) / rect.height - 0.5) * 0.8;
    };

    window.addEventListener('mousemove', handleMouseMove);

    // 9. Animation Loop
    let animationFrameId;
    const clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const elapsedTime = clock.getElapsedTime();

      // Slow anatomical rotation
      humanGroup.rotation.y = elapsedTime * 0.2;
      dnaParticles.rotation.y = -elapsedTime * 0.15;

      // Heartbeat pulse simulation
      const pulse = 1.0 + Math.sin(elapsedTime * 6.0) * 0.12;
      heartMesh.scale.set(pulse, pulse, pulse);
      heartGlow.scale.set(pulse * 1.05, pulse * 1.05, pulse * 1.05);

      // Scanning Ring Movement along Body Height
      scanRing.position.y = Math.sin(elapsedTime * 1.5) * 4.5;
      scanRing.rotation.z = elapsedTime * 0.5;

      // Mouse Parallax
      scene.rotation.y += (mouseX - scene.rotation.y) * 0.05;
      scene.rotation.x += (-mouseY - scene.rotation.x) * 0.05;

      renderer.render(scene, camera);
    };

    animate();

    const handleResize = () => {
      if (!container) return;
      const newW = container.clientWidth;
      const newH = container.clientHeight;
      camera.aspect = newW / newH;
      camera.updateProjectionMatrix();
      renderer.setSize(newW, newH);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
      if (container && renderer.domElement) {
        container.removeChild(renderer.domElement);
      }
      headGeo.dispose(); headMat.dispose();
      torsoGeo.dispose(); torsoMat.dispose();
      legsGeo.dispose(); legsMat.dispose();
      heartGeo.dispose(); heartMat.dispose();
      heartGlowGeo.dispose(); heartGlowMat.dispose();
      kidneyGeo.dispose(); kidneyMat.dispose();
      dnaGeo.dispose(); dnaMat.dispose();
      scanRingGeo.dispose(); scanRingMat.dispose();
      renderer.dispose();
    };
  }, [interactive]);

  return (
    <div className={`relative flex items-center justify-center ${className}`}>
      <div ref={mountRef} className="w-full h-full cursor-grab active:cursor-grabbing" />
      
      {/* Biometric Overlay Labels */}
      <div className="absolute top-2 left-2 flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-slate-900/80 border border-slate-800 text-[10px] text-sky-400 font-mono">
        <span className="w-2 h-2 rounded-full bg-sky-400 animate-ping" />
        <span>3D HEALTH SCANNER</span>
      </div>

      <div className="absolute bottom-2 right-2 flex items-center space-x-2 px-2.5 py-1 rounded-full bg-slate-900/80 border border-slate-800 text-[10px] text-teal-400 font-mono">
        <span>ECG / RENAL / CARDIAC REGIONS ACTIVE</span>
      </div>
    </div>
  );
}
