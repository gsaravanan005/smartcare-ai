import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

/**
 * SMARTCARE AI — PREMIUM FUTURISTIC HEALTHCARE BACKGROUND
 * EXACT VISUAL RECREATION MATCHING REFERENCE IMAGE
 * 
 * 100% Pure Background System:
 * - pointer-events-none, select-none, z-0
 * - NO login UI, NO form elements, NO buttons, NO user inputs
 * - Center kept dark & clear (#05020D / #080316) for foreground login card
 * 
 * Reference Breakdown:
 * 1. TOP-LEFT: Exact Official SmartCare AI Logo + "CONNECTING PEOPLE ↓ TECHNOLOGY BETTER HEALTH"
 * 2. TOP-RIGHT: "● SMARTCARE AI HEALTHCARE PLATFORM" pill capsule
 * 3. LEFT: High-Tech Holographic Digital Earth with luminous purple continents, orbital rings, and atmospheric rim
 * 4. BACKGROUND: Faint medical network world map watermark + dark purple atmosphere
 * 5. SWEEPING RIBBON: Dense glowing cosmic data stream flowing from Earth across to Human chest
 * 6. RIGHT: Realistic anatomical human hologram with glowing neural brain, ribcage, vascular tree, and pulsating magenta anatomical heart
 * 7. HUD AROUND HUMAN:
 *    - Left: "AI for Healthier Tomorrows" script, "HEART RATE 72 bpm" + mini ECG, Brain hexagon, Medical Cross badges
 *    - Right: Vertical HUD stack of 3 rounded cards: Lungs, DNA double helix, Bar analytics chart
 * 8. ACROSS: Continuous glowing neon-purple horizontal medical ECG waveform (P-QRS-T)
 * 9. BOTTOM STAGE: Curved glossy deck with glowing purple neon dashes, specular floor reflections, and left/right pedestals
 */
export default function Live3DHealthBackground() {
  const mountRef = useRef(null);
  const ecgCanvasRef = useRef(null);
  const miniEcgCanvasRef = useRef(null);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    const width = container.clientWidth || window.innerWidth;
    const height = container.clientHeight || window.innerHeight;

    // =========================================================================
    // 1. THREE.JS SCENE SETUP & CINEMATIC FOG
    // =========================================================================
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x05020D, 0.022);

    const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 1000);
    camera.position.set(0, 0, 15);

    const renderer = new THREE.WebGLRenderer({
      alpha: true,
      antialias: true,
      powerPreference: 'high-performance'
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.40;
    container.appendChild(renderer.domElement);

    const textureLoader = new THREE.TextureLoader();

    // =========================================================================
    // 2. LIGHTING (DEEP PURPLE / VIOLET ATMOSPHERE)
    // =========================================================================
    const ambientLight = new THREE.AmbientLight(0x3B0764, 3.6);
    scene.add(ambientLight);

    const mainLight = new THREE.DirectionalLight(0xD8B4FE, 4.0);
    mainLight.position.set(4, 8, 12);
    scene.add(mainLight);

    // Left Violet Light (Earth illumination)
    const earthPointLight = new THREE.PointLight(0xC084FC, 9.5, 45);
    earthPointLight.position.set(-7.0, 0.6, 6.0);
    scene.add(earthPointLight);

    // Right Magenta / Violet Light (Directly illuminating anatomical heart and human)
    const heartPointLight = new THREE.PointLight(0xFF1493, 9.5, 32);
    heartPointLight.position.set(6.8, -0.65, 3.5);
    scene.add(heartPointLight);

    // Floor edge bounce lights
    const floorBounceLight = new THREE.PointLight(0x8B5CF6, 5.0, 30);
    floorBounceLight.position.set(0, -5.5, 4);
    scene.add(floorBounceLight);

    const isMobile = width < 768;
    const isTablet = width >= 768 && width < 1024;
    const baseScale = isMobile ? 0.68 : isTablet ? 0.88 : 1.05;

    // =========================================================================
    // 3. LEFT SIDE: 3D HOLOGRAPHIC DIGITAL EARTH (LUMINOUS CONTINENTS)
    // =========================================================================
    const earthGroup = new THREE.Group();
    const earthX = isMobile ? -2.4 : isTablet ? -4.9 : -6.8;
    const earthY = isMobile ? -0.4 : 0.05;
    earthGroup.position.set(earthX, earthY, -0.5);
    // Face the Americas directly towards the camera with a slight cinematic forward tilt
    earthGroup.rotation.y = 0.18;
    earthGroup.rotation.x = 0.14;
    earthGroup.scale.set(baseScale, baseScale, baseScale);
    scene.add(earthGroup);

    const globeRadius = 3.05;

    // 3A. Luminous Earth Globe with High-Resolution Continent Emissive Texture
    const earthTexture = textureLoader.load('/earth_continents_texture.jpg');
    earthTexture.wrapS = THREE.RepeatWrapping;
    earthTexture.wrapT = THREE.ClampToEdgeWrapping;

    const globeGeo = new THREE.SphereGeometry(globeRadius, 64, 64);
    const globeMat = new THREE.MeshStandardMaterial({
      color: 0x060212,
      emissive: 0xD8B4FE,
      emissiveMap: earthTexture,
      emissiveIntensity: 2.6,
      roughness: 0.15,
      metalness: 0.85,
      transparent: true,
      opacity: 0.95
    });
    const globeMesh = new THREE.Mesh(globeGeo, globeMat);
    earthGroup.add(globeMesh);

    // 3B. Delicate Latitude/Longitude Coordinate Wireframe
    const gridGeo = new THREE.SphereGeometry(globeRadius + 0.025, 36, 36);
    const gridMat = new THREE.MeshBasicMaterial({
      color: 0x7C3AED,
      wireframe: true,
      transparent: true,
      opacity: 0.28
    });
    const gridMesh = new THREE.Mesh(gridGeo, gridMat);
    earthGroup.add(gridMesh);

    // 3C. Atmospheric Violet Glowing Rim
    const atmosGeo = new THREE.SphereGeometry(globeRadius * 1.10, 48, 48);
    const atmosMat = new THREE.MeshBasicMaterial({
      color: 0xA855F7,
      transparent: true,
      opacity: 0.42,
      side: THREE.BackSide,
      blending: THREE.AdditiveBlending
    });
    const atmosMesh = new THREE.Mesh(atmosGeo, atmosMat);
    earthGroup.add(atmosMesh);

    // 3D. Concentric Orbital Rings & Sparkling Data Particles
    const ring1Geo = new THREE.TorusGeometry(globeRadius * 1.34, 0.018, 16, 96);
    const ringMat1 = new THREE.MeshBasicMaterial({ color: 0xA855F7, transparent: true, opacity: 0.75, blending: THREE.AdditiveBlending });
    const ring1 = new THREE.Mesh(ring1Geo, ringMat1);
    ring1.rotation.x = Math.PI / 3.2;
    ring1.rotation.y = Math.PI / 7;
    earthGroup.add(ring1);

    const ring2Geo = new THREE.TorusGeometry(globeRadius * 1.54, 0.014, 16, 96);
    const ringMat2 = new THREE.MeshBasicMaterial({ color: 0xC084FC, transparent: true, opacity: 0.60, blending: THREE.AdditiveBlending });
    const ring2 = new THREE.Mesh(ring2Geo, ringMat2);
    ring2.rotation.x = -Math.PI / 3.6;
    ring2.rotation.y = -Math.PI / 5;
    earthGroup.add(ring2);

    // Orbiting Data Sparkles
    const ringSparkleCount = 90;
    const ringSparklePos = new Float32Array(ringSparkleCount * 3);
    for (let rp = 0; rp < ringSparkleCount; rp++) {
      const angle = (rp / ringSparkleCount) * Math.PI * 2;
      const rad = globeRadius * 1.34 + (Math.random() - 0.5) * 0.16;
      ringSparklePos[rp * 3] = Math.cos(angle) * rad;
      ringSparklePos[rp * 3 + 1] = Math.sin(angle) * rad * Math.sin(Math.PI / 3.2);
      ringSparklePos[rp * 3 + 2] = Math.sin(angle) * rad * Math.cos(Math.PI / 3.2);
    }
    const ringSparkleGeo = new THREE.BufferGeometry();
    ringSparkleGeo.setAttribute('position', new THREE.BufferAttribute(ringSparklePos, 3));
    const ringSparkleMat = new THREE.PointsMaterial({ color: 0xFFFFFF, size: 0.085, transparent: true, opacity: 0.95, blending: THREE.AdditiveBlending });
    const ringSparkles = new THREE.Points(ringSparkleGeo, ringSparkleMat);
    earthGroup.add(ringSparkles);

    // Global Network Connecting Arcs over Earth
    const arcsGroup = new THREE.Group();
    for (let a = 0; a < 12; a++) {
      const u1 = Math.random() * Math.PI * 2;
      const v1 = Math.acos(2 * Math.random() - 1);
      const p1 = new THREE.Vector3(
        globeRadius * Math.sin(v1) * Math.cos(u1),
        globeRadius * Math.cos(v1),
        globeRadius * Math.sin(v1) * Math.sin(u1)
      );

      const u2 = u1 + (Math.random() - 0.5) * 1.5;
      const v2 = Math.acos(2 * Math.random() - 1);
      const p2 = new THREE.Vector3(
        globeRadius * Math.sin(v2) * Math.cos(u2),
        globeRadius * Math.cos(v2),
        globeRadius * Math.sin(v2) * Math.sin(u2)
      );

      const mid = p1.clone().add(p2).multiplyScalar(0.5).normalize().multiplyScalar(globeRadius * 1.22);
      const curve = new THREE.QuadraticBezierCurve3(p1, mid, p2);
      const curvePts = curve.getPoints(24);
      const curveGeo = new THREE.BufferGeometry().setFromPoints(curvePts);
      const curveMat = new THREE.LineBasicMaterial({
        color: 0xC084FC,
        transparent: true,
        opacity: 0.70,
        blending: THREE.AdditiveBlending
      });
      const arcLine = new THREE.Line(curveGeo, curveMat);
      arcsGroup.add(arcLine);
    }
    earthGroup.add(arcsGroup);


    // =========================================================================
    // 4. RIGHT SIDE: NATURAL HUMAN ANATOMICAL MEDICAL HOLOGRAM
    // =========================================================================
    const humanGroup = new THREE.Group();
    const humanX = isMobile ? 2.4 : isTablet ? 5.2 : 7.2;
    const humanY = isMobile ? -0.3 : 0.0;
    humanGroup.position.set(humanX, humanY, 0.1);
    humanGroup.scale.set(baseScale, baseScale, baseScale);
    scene.add(humanGroup);

    // 4A. High-Resolution Natural Anatomical Human Hologram Texture Plane
    let humanPlaneMesh = null;
    textureLoader.load(
      '/human_anatomical_hologram.png',
      (texture) => {
        texture.minFilter = THREE.LinearFilter;
        texture.magFilter = THREE.LinearFilter;
        texture.generateMipmaps = false;

        const planeGeo = new THREE.PlaneGeometry(6.4, 8.53);
        const planeMat = new THREE.MeshBasicMaterial({
          map: texture,
          transparent: true,
          opacity: 0.96,
          side: THREE.DoubleSide,
          depthWrite: false
        });

        humanPlaneMesh = new THREE.Mesh(planeGeo, planeMat);
        humanPlaneMesh.position.set(0, 0, 0);
        humanGroup.add(humanPlaneMesh);
      },
      undefined,
      (err) => console.error('Error loading human anatomical hologram texture:', err)
    );

    // 4B. REALISTIC MEDICAL HEARTBEAT VISUALIZATION
    const heartHaloGroup = new THREE.Group();
    heartHaloGroup.position.set(0.11, -0.90, 0.22);
    humanGroup.add(heartHaloGroup);

    // 4B-1. Volumetric Heart Bloom Glow Sprite (Soft Gaussian falloff)
    const bloomTexture = textureLoader.load('/heart_glow_bloom.png');
    const heartBloomMat = new THREE.SpriteMaterial({
      map: bloomTexture,
      color: 0xFF1493,
      transparent: true,
      opacity: 0.75,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });
    const heartBloomSprite = new THREE.Sprite(heartBloomMat);
    heartBloomSprite.scale.set(2.4, 2.4, 1.0);
    heartHaloGroup.add(heartBloomSprite);

    // 4B-2. Hot Inner Core Ventricular Flash Sprite
    const heartCoreMat = new THREE.SpriteMaterial({
      map: bloomTexture,
      color: 0xFFE4E6,
      transparent: true,
      opacity: 0.88,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });
    const heartCoreSprite = new THREE.Sprite(heartCoreMat);
    heartCoreSprite.scale.set(1.15, 1.15, 1.0);
    heartHaloGroup.add(heartCoreSprite);

    // 4B-3. Subtle Cardiac Capillary / Vascular Points inside Heart
    const vascularCount = 55;
    const vascularPos = new Float32Array(vascularCount * 3);
    for (let v = 0; v < vascularCount; v++) {
      const u = Math.random() * Math.PI * 2;
      const phi = Math.random() * Math.PI;
      const rad = 0.45 * Math.sin(phi);
      vascularPos[v * 3] = rad * Math.cos(u) * 0.75;
      vascularPos[v * 3 + 1] = rad * Math.sin(u) * 0.85;
      vascularPos[v * 3 + 2] = (Math.random() - 0.5) * 0.3;
    }
    const vascularGeo = new THREE.BufferGeometry();
    vascularGeo.setAttribute('position', new THREE.BufferAttribute(vascularPos, 3));
    const vascularMat = new THREE.PointsMaterial({
      color: 0xFFE4E6,
      size: 0.045,
      transparent: true,
      opacity: 0.85,
      blending: THREE.AdditiveBlending
    });
    const vascularPoints = new THREE.Points(vascularGeo, vascularMat);
    heartHaloGroup.add(vascularPoints);


    // =========================================================================
    // 5. SWEEPING COSMIC HEALTHCARE DATA STREAM (EARTH → CENTER → HUMAN CHEST)
    // =========================================================================
    const ribbonCurve = new THREE.CatmullRomCurve3([
      new THREE.Vector3(earthX + 1.2, earthY + 2.8, -1.0),
      new THREE.Vector3(earthX + 3.8, earthY + 1.6, -0.8),
      new THREE.Vector3(0.0, 0.45, -0.6),
      new THREE.Vector3(humanX - 3.8, -0.2, -0.3),
      new THREE.Vector3(humanX + 0.1, humanY - 0.9, 0.2)
    ]);

    const ribbonParticleCount = 1400;
    const ribbonPositions = new Float32Array(ribbonParticleCount * 3);
    const ribbonColors = new Float32Array(ribbonParticleCount * 3);
    const ribbonProgress = new Float32Array(ribbonParticleCount);
    const ribbonSpeeds = new Float32Array(ribbonParticleCount);
    const ribbonOffsets = new Float32Array(ribbonParticleCount * 3);

    const colBright = new THREE.Color(0xFFFFFF);
    const colLav = new THREE.Color(0xE9D5FF);
    const colPurp = new THREE.Color(0xC084FC);
    const colMag = new THREE.Color(0xE879F9);

    for (let r = 0; r < ribbonParticleCount; r++) {
      ribbonProgress[r] = Math.random();
      ribbonSpeeds[r] = 0.0009 + Math.random() * 0.0018;

      ribbonOffsets[r * 3] = (Math.random() - 0.5) * 0.95;
      ribbonOffsets[r * 3 + 1] = (Math.random() - 0.5) * 0.80;
      ribbonOffsets[r * 3 + 2] = (Math.random() - 0.5) * 0.70;

      const p = ribbonCurve.getPoint(ribbonProgress[r]);
      ribbonPositions[r * 3] = p.x + ribbonOffsets[r * 3];
      ribbonPositions[r * 3 + 1] = p.y + ribbonOffsets[r * 3 + 1];
      ribbonPositions[r * 3 + 2] = p.z + ribbonOffsets[r * 3 + 2];

      const cRand = Math.random();
      const col = cRand > 0.65 ? colBright : cRand > 0.40 ? colLav : cRand > 0.20 ? colPurp : colMag;
      ribbonColors[r * 3] = col.r;
      ribbonColors[r * 3 + 1] = col.g;
      ribbonColors[r * 3 + 2] = col.b;
    }

    const ribbonGeo = new THREE.BufferGeometry();
    ribbonGeo.setAttribute('position', new THREE.BufferAttribute(ribbonPositions, 3));
    ribbonGeo.setAttribute('color', new THREE.BufferAttribute(ribbonColors, 3));

    const ribbonMat = new THREE.PointsMaterial({
      size: 0.11,
      vertexColors: true,
      transparent: true,
      opacity: 0.95,
      blending: THREE.AdditiveBlending
    });
    const ribbonPoints = new THREE.Points(ribbonGeo, ribbonMat);
    scene.add(ribbonPoints);

    // Background Ambient Data Nodes
    const bgNodeCount = 180;
    const bgNodePos = new Float32Array(bgNodeCount * 3);
    for (let b = 0; b < bgNodeCount; b++) {
      bgNodePos[b * 3] = (Math.random() - 0.5) * 36;
      bgNodePos[b * 3 + 1] = (Math.random() - 0.5) * 22;
      bgNodePos[b * 3 + 2] = -5 - Math.random() * 6;
    }
    const bgNodeGeo = new THREE.BufferGeometry();
    bgNodeGeo.setAttribute('position', new THREE.BufferAttribute(bgNodePos, 3));
    const bgNodeMat = new THREE.PointsMaterial({ color: 0x8B5CF6, size: 0.065, transparent: true, opacity: 0.50, blending: THREE.AdditiveBlending });
    const bgNodePoints = new THREE.Points(bgNodeGeo, bgNodeMat);
    scene.add(bgNodePoints);


    // =========================================================================
    // 6. 2D LIVE ECG TRAVELLING WAVEFORM CANVAS
    // =========================================================================
    const ecgCanvas = ecgCanvasRef.current;
    let ecgCtx = null;
    if (ecgCanvas) {
      ecgCanvas.width = width;
      ecgCanvas.height = height;
      ecgCtx = ecgCanvas.getContext('2d');
    }
    let ecgOffset = 0;

    // Mini ECG Canvas inside HUD panel
    const miniCanvas = miniEcgCanvasRef.current;
    let miniCtx = null;
    if (miniCanvas) {
      miniCanvas.width = 110;
      miniCanvas.height = 36;
      miniCtx = miniCanvas.getContext('2d');
    }
    let miniOffset = 0;


    // =========================================================================
    // 7. ANIMATION LOOP (GPU-ACCELERATED VIA requestAnimationFrame)
    // =========================================================================
    let animationFrameId;
    const clock = new THREE.Clock();
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const elapsedTime = clock.getElapsedTime();

      // Earth Continuous Rotation
      const earthRotSpeed = prefersReducedMotion ? 0.0003 : 0.0016;
      earthGroup.rotation.y += earthRotSpeed;
      ringSparkles.rotation.y -= earthRotSpeed * 1.5;

      // Heartbeat Rhythm
      const cycleSpeed = prefersReducedMotion ? 1.2 : 3.5;
      const cycle = (elapsedTime * cycleSpeed) % (2 * Math.PI);
      const systole = Math.pow(Math.max(0, Math.sin(cycle)), 12);
      const diastole = Math.pow(Math.max(0, Math.sin(cycle - 0.38)), 12);
      const pulseAmp = prefersReducedMotion ? 0.05 : 0.16;

      // Natural Human subtle breathing elevation
      const breathing = Math.sin(elapsedTime * 0.9) * 0.035;
      humanGroup.position.y = humanY + breathing;

      // Synchronize Heartbeat Pulse directly at anatomical heart
      const heartGlowScale = 2.4 * (1.0 + pulseAmp * systole * 2.2 + (pulseAmp / 2) * diastole);
      heartBloomSprite.scale.set(heartGlowScale, heartGlowScale, 1.0);
      heartBloomMat.opacity = 0.55 + 0.45 * systole + 0.15 * diastole;

      const coreScale = 1.15 * (1.0 + pulseAmp * systole * 1.8);
      heartCoreSprite.scale.set(coreScale, coreScale, 1.0);
      heartCoreMat.opacity = 0.65 + 0.35 * systole;

      // Volumetric light flash centered on heart
      heartPointLight.position.set(humanX + 0.11, humanGroup.position.y - 0.90, 2.5);
      heartPointLight.intensity = 5.5 + 9.5 * systole;

      // Flowing Cosmic Data Ribbon Particles
      const rPos = ribbonGeo.attributes.position.array;
      for (let r = 0; r < ribbonParticleCount; r++) {
        ribbonProgress[r] += prefersReducedMotion ? ribbonSpeeds[r] * 0.3 : ribbonSpeeds[r];
        if (ribbonProgress[r] > 1) ribbonProgress[r] = 0;

        const pt = ribbonCurve.getPoint(ribbonProgress[r]);
        rPos[r * 3] = pt.x + ribbonOffsets[r * 3];
        rPos[r * 3 + 1] = pt.y + ribbonOffsets[r * 3 + 1];
        rPos[r * 3 + 2] = pt.z + ribbonOffsets[r * 3 + 2];
      }
      ribbonGeo.attributes.position.needsUpdate = true;

      // Background Node subtle floating drift
      const bgArr = bgNodeGeo.attributes.position.array;
      for (let b = 0; b < bgNodeCount; b++) {
        bgArr[b * 3 + 1] += Math.sin(elapsedTime * 0.6 + b) * 0.001;
      }
      bgNodeGeo.attributes.position.needsUpdate = true;

      // Render 3D Scene
      renderer.render(scene, camera);

      // Render 2D Neon ECG Waveform Line
      if (ecgCtx && ecgCanvas) {
        drawLiveECGLine(ecgCtx, ecgCanvas.width, ecgCanvas.height, ecgOffset, systole);
        ecgOffset += prefersReducedMotion ? 0.8 : 3.4;
      }

      // Render Mini HUD ECG Line
      if (miniCtx && miniCanvas) {
        drawMiniECG(miniCtx, miniCanvas.width, miniCanvas.height, miniOffset, systole);
        miniOffset += prefersReducedMotion ? 0.6 : 2.5;
      }
    };

    animate();

    // =========================================================================
    // 8. RESIZE HANDLER
    // =========================================================================
    const handleResize = () => {
      const w = container.clientWidth || window.innerWidth;
      const h = container.clientHeight || window.innerHeight;

      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);

      if (ecgCanvas) {
        ecgCanvas.width = w;
        ecgCanvas.height = h;
      }

      const mob = w < 768;
      const tab = w >= 768 && w < 1024;
      const newScale = mob ? 0.68 : tab ? 0.88 : 1.05;
      const newEarthX = mob ? -2.4 : tab ? -4.9 : -6.8;
      const newHumanX = mob ? 2.4 : tab ? 5.2 : 7.2;

      earthGroup.position.x = newEarthX;
      earthGroup.scale.set(newScale, newScale, newScale);
      humanGroup.position.x = newHumanX;
      humanGroup.scale.set(newScale, newScale, newScale);
    };

    window.addEventListener('resize', handleResize);

    // =========================================================================
    // 9. CLEANUP
    // =========================================================================
    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', handleResize);

      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }

      globeGeo.dispose();
      globeMat.dispose();
      earthTexture.dispose();
      gridGeo.dispose();
      gridMat.dispose();
      atmosGeo.dispose();
      atmosMat.dispose();
      ring1Geo.dispose();
      ring2Geo.dispose();
      ringMat1.dispose();
      ringMat2.dispose();
      ringSparkleGeo.dispose();
      ringSparkleMat.dispose();

      bloomTexture.dispose();
      heartBloomMat.dispose();
      heartCoreMat.dispose();
      vascularGeo.dispose();
      vascularMat.dispose();

      ribbonGeo.dispose();
      ribbonMat.dispose();
      bgNodeGeo.dispose();
      bgNodeMat.dispose();

      renderer.dispose();
    };
  }, []);

  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden bg-[#05020D] select-none">
      {/* 1. Subtle Background Medical World Map Watermark (Upper Half) */}
      <div 
        className="absolute top-0 left-0 w-full h-[65%] opacity-[0.12] pointer-events-none mix-blend-screen bg-no-repeat bg-cover bg-center"
        style={{ backgroundImage: "url('/earth_continents_texture.jpg')" }}
      />

      {/* 2. 3D Three.js WebGL Canvas Layer */}
      <div ref={mountRef} className="absolute inset-0 w-full h-full" />

      {/* 3. 2D Live Horizontal ECG Travelling Waveform Canvas */}
      <canvas ref={ecgCanvasRef} className="absolute inset-0 w-full h-full pointer-events-none z-0" />

      {/* 4. Deep Purple Atmospheric Lighting & Clean Dark Center Safe Zone */}
      <div className="absolute top-0 left-0 w-full h-32 bg-gradient-to-b from-[#05020D]/90 via-[#05020D]/50 to-transparent pointer-events-none" />
      <div className="absolute bottom-0 left-0 w-full h-44 bg-gradient-to-t from-[#05020D] via-[#05020D]/70 to-transparent pointer-events-none" />

      {/* Clean Dark Center Radial Safe Area (Reserved for foreground login UI) */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[720px] h-[580px] bg-[#05020D]/85 rounded-full blur-[115px] pointer-events-none" />


      {/* ===================================================================== */}
      {/* 5. TOP-LEFT: EXACT OFFICIAL SMARTCARE AI LOGO + SUBTITLE */}
      {/* ===================================================================== */}
      <div className="absolute top-6 left-7 md:left-9 flex flex-col items-start z-10 pointer-events-none">
        {/* Exact Official SmartCare AI Logo with screen blend for seamless dark integration */}
        <img
          src="/smartcare-logo.png"
          alt="SmartCare AI Official Logo"
          className="w-[145px] sm:w-[160px] h-auto object-contain mix-blend-screen drop-shadow-[0_0_18px_rgba(168,85,247,0.50)]"
        />

        {/* Left-Side Futuristic Subtitle */}
        <div className="mt-8 sm:mt-11 text-[10.5px] sm:text-[11px] font-mono uppercase tracking-[0.26em] text-[#C084FC]/85 leading-[1.8] font-bold">
          <div>CONNECTING</div>
          <div className="flex items-center space-x-1">
            <span>PEOPLE</span>
            <span className="text-purple-400 text-xs font-normal">↓</span>
          </div>
          <div>TECHNOLOGY</div>
          <div className="text-[#E9D5FF]/95">BETTER HEALTH</div>
        </div>
      </div>


      {/* ===================================================================== */}
      {/* 6. TOP-RIGHT: SMARTCARE AI HEALTHCARE PLATFORM CAPSULE */}
      {/* ===================================================================== */}
      <div className="absolute top-6 right-7 md:right-9 z-10 pointer-events-none">
        <div className="flex items-center space-x-2.5 px-4 py-1.5 rounded-full bg-[#0B031A]/80 border border-[#7C3AED]/50 backdrop-blur-md shadow-[0_0_18px_rgba(124,58,237,0.30)]">
          <span className="relative flex h-2.5 w-2.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#C084FC] opacity-75" />
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-[#A855F7] shadow-[0_0_8px_#A855F7]" />
          </span>
          <span className="text-[10.5px] sm:text-[11px] font-mono font-bold tracking-widest text-purple-200 uppercase">
            SMARTCARE AI HEALTHCARE PLATFORM
          </span>
        </div>
      </div>


      {/* ===================================================================== */}
      {/* 7. FLOATING MEDICAL CROSS BADGES (AUTHENTIC COMMAND CENTER ACCENTS) */}
      {/* ===================================================================== */}
      {/* Upper-Center Medical Cross */}
      <div className="hidden lg:flex absolute top-[18%] left-[43%] w-7 h-7 items-center justify-center rounded-lg border border-[#A855F7]/30 bg-[#120529]/40 backdrop-blur-sm z-10 pointer-events-none">
        <span className="text-[#C084FC]/60 text-xs font-bold">+</span>
      </div>

      {/* Mid-Left Medical Cross (Near Earth) */}
      <div className="hidden lg:flex absolute top-[28%] left-[28%] w-8 h-8 items-center justify-center rounded-lg border border-[#A855F7]/30 bg-[#120529]/40 backdrop-blur-sm z-10 pointer-events-none">
        <span className="text-[#C084FC]/60 text-sm font-bold">+</span>
      </div>

      {/* Lower-Center Medical Cross */}
      <div className="hidden lg:flex absolute bottom-[26%] left-[45%] w-8 h-8 items-center justify-center rounded-lg border border-[#A855F7]/30 bg-[#120529]/40 backdrop-blur-sm z-10 pointer-events-none">
        <span className="text-[#C084FC]/60 text-sm font-bold">+</span>
      </div>


      {/* ===================================================================== */}
      {/* 8. HUD ELEMENTS TO THE LEFT OF HUMAN (SCRIPT + 72 BPM + BRAIN + CROSS) */}
      {/* ===================================================================== */}
      {/* 8A. "AI for Healthier Tomorrows" Script */}
      <div className="hidden lg:block absolute top-[10%] right-[22%] xl:right-[24%] z-10 pointer-events-none text-left">
        <div 
          className="text-[#E9D5FF] text-2xl xl:text-3xl leading-[1.18] drop-shadow-[0_0_18px_rgba(192,132,252,0.55)]"
          style={{ fontFamily: "'Caveat', cursive, serif" }}
        >
          AI for<br />
          Healthier<br />
          Tomorrows
        </div>
      </div>

      {/* 8B. Heart Rate Card & Badges */}
      <div className="hidden md:flex absolute top-[26%] right-[22%] xl:right-[24%] flex-col space-y-3 z-10 pointer-events-none items-end">
        {/* Row with Medical Cross Badge + Heart Rate Card */}
        <div className="flex items-center space-x-3">
          {/* Hexagonal Medical Cross Badge */}
          <div className="relative w-10 h-10 flex items-center justify-center">
            <svg className="absolute inset-0 w-full h-full text-[#A855F7]/70 drop-shadow-[0_0_8px_rgba(168,85,247,0.45)]" viewBox="0 0 100 100" fill="none" stroke="currentColor" strokeWidth="4">
              <polygon points="50 3, 90 25, 90 75, 50 97, 10 75, 10 25" fill="#130528" fillOpacity="0.80" />
            </svg>
            <span className="relative text-[#E9D5FF] text-sm font-bold leading-none">+</span>
          </div>

          {/* Heart Rate 72 bpm Glass HUD Card */}
          <div className="relative px-3.5 py-2.5 rounded-xl bg-[#110526]/85 border border-[#A855F7]/50 backdrop-blur-md shadow-[0_0_22px_rgba(168,85,247,0.30)] flex flex-col space-y-1 w-36">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-1.5">
                <svg className="w-3.5 h-3.5 text-rose-400 animate-pulse" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
                </svg>
                <span className="text-[9px] font-mono uppercase tracking-wider text-purple-300 font-semibold">HEART RATE</span>
              </div>
              <span className="text-xs font-mono font-bold text-rose-300">72 <span className="text-[9px] font-normal text-purple-400">bpm</span></span>
            </div>
            <div className="w-full h-7 overflow-hidden rounded">
              <canvas ref={miniEcgCanvasRef} className="w-full h-full" />
            </div>
          </div>
        </div>

        {/* Hexagonal Brain Analysis Badge below 72 bpm */}
        <div className="relative w-11 h-11 flex items-center justify-center mr-2">
          <svg className="absolute inset-0 w-full h-full text-[#A855F7]/70 drop-shadow-[0_0_10px_rgba(168,85,247,0.45)]" viewBox="0 0 100 100" fill="none" stroke="currentColor" strokeWidth="4">
            <polygon points="50 3, 90 25, 90 75, 50 97, 10 75, 10 25" fill="#130528" fillOpacity="0.80" />
          </svg>
          <svg className="relative w-5 h-5 text-purple-200" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7">
            <path strokeLinecap="round" strokeLinejoin="round" d="M9.5 2A4.5 4.5 0 005 6.5c0 .77.19 1.5.54 2.14A4.5 4.5 0 004 12.5a4.5 4.5 0 002.09 3.81A4.5 4.5 0 009.5 21c.5 0 .97-.08 1.42-.23" />
            <path strokeLinecap="round" strokeLinejoin="round" d="M14.5 2A4.5 4.5 0 0119 6.5c0 .77-.19 1.5-.54 2.14A4.5 4.5 0 0120 12.5a4.5 4.5 0 01-2.09 3.81A4.5 4.5 0 0114.5 21c-.5 0-.97-.08-1.42-.23" />
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16" />
            <path strokeLinecap="round" strokeLinejoin="round" d="M8 8c1 1 2 1 4 0" />
            <path strokeLinecap="round" strokeLinejoin="round" d="M16 8c-1 1-2 1-4 0" />
            <path strokeLinecap="round" strokeLinejoin="round" d="M8 14c1-1 2-1 4 0" />
            <path strokeLinecap="round" strokeLinejoin="round" d="M16 14c-1-1-2-1-4 0" />
          </svg>
        </div>
      </div>


      {/* ===================================================================== */}
      {/* 9. HUD ELEMENTS TO THE RIGHT OF HUMAN (LUNGS, DNA, BAR ANALYTICS) */}
      {/* ===================================================================== */}
      <div className="hidden xl:flex absolute top-[24%] right-[2.5%] 2xl:right-[3.5%] flex-col space-y-4 z-10 pointer-events-none">
        {/* Card 1: Anatomical Lungs */}
        <div className="relative w-14 h-14 rounded-2xl bg-[#110526]/80 border border-[#A855F7]/50 backdrop-blur-md shadow-[0_0_16px_rgba(168,85,247,0.25)] flex items-center justify-center">
          <svg className="w-8 h-8 text-[#C084FC] drop-shadow-[0_0_8px_rgba(192,132,252,0.6)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6">
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 2v6m0 0l-3 3m3-3l3 3" />
            <path strokeLinecap="round" strokeLinejoin="round" d="M9 11c-2.5 0-4.5 2-4.5 5 0 3.5 2 5.5 4.5 5.5 1.5 0 2.5-1 2.5-2.5V11z" />
            <path strokeLinecap="round" strokeLinejoin="round" d="M15 11c2.5 0 4.5 2 4.5 5 0 3.5-2 5.5-4.5 5.5-1.5 0-2.5-1-2.5-2.5V11z" />
            <path strokeLinecap="round" strokeLinejoin="round" d="M7 16h2m6 0h2" />
          </svg>
        </div>

        {/* Card 2: DNA Double Helix */}
        <div className="relative w-14 h-14 rounded-2xl bg-[#110526]/80 border border-[#A855F7]/50 backdrop-blur-md shadow-[0_0_16px_rgba(168,85,247,0.25)] flex items-center justify-center">
          <svg className="w-8 h-8 text-[#C084FC] drop-shadow-[0_0_8px_rgba(192,132,252,0.6)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6">
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 3c3 4.5 9 7.5 12 12m-12 0c3-4.5 9-7.5 12-12" />
            <path strokeLinecap="round" strokeLinejoin="round" d="M7 6.5h10M6 12h12M7 17.5h10" />
            <circle cx="6" cy="3" r="1" fill="currentColor" />
            <circle cx="18" cy="3" r="1" fill="currentColor" />
            <circle cx="6" cy="15" r="1" fill="currentColor" />
            <circle cx="18" cy="15" r="1" fill="currentColor" />
          </svg>
        </div>

        {/* Card 3: Health Analytics Bar Chart */}
        <div className="relative w-14 h-16 rounded-2xl bg-[#110526]/80 border border-[#A855F7]/50 backdrop-blur-md shadow-[0_0_16px_rgba(168,85,247,0.25)] flex flex-col items-center justify-center px-1.5 pt-1">
          <div className="flex items-end space-x-1 h-8">
            <div className="w-1.5 bg-[#A855F7] rounded-t h-4" />
            <div className="w-1.5 bg-[#C084FC] rounded-t h-6" />
            <div className="w-1.5 bg-[#E879F9] rounded-t h-8" />
            <div className="w-1.5 bg-[#D8B4FE] rounded-t h-5" />
          </div>
          <div className="flex space-x-1 mt-1 text-[7px] font-mono text-purple-300">
            <span>24%</span>
            <span>89%</span>
          </div>
        </div>
      </div>


      {/* ===================================================================== */}
      {/* 10. BOTTOM COMMAND DECK (ILLUMINATED PEDESTALS & SPECULAR FLOOR TRACK) */}
      {/* ===================================================================== */}
      {/* Curved Stage Edge Track Lines */}
      <div className="absolute bottom-0 left-0 w-full h-28 pointer-events-none z-10 overflow-hidden">
        {/* Outer Circular Track Ellipse */}
        <div className="absolute -bottom-24 left-1/2 -translate-x-1/2 w-[110%] max-w-[1700px] h-48 border-t-2 border-[#7C3AED]/40 rounded-[100%] pointer-events-none" />
        {/* Inner Circular Track Ellipse */}
        <div className="absolute -bottom-16 left-1/2 -translate-x-1/2 w-[88%] max-w-[1400px] h-36 border-t border-[#A855F7]/30 rounded-[100%] pointer-events-none" />

        {/* Floor Neon Purple Dashes with Specular Vertical Reflections */}
        <div className="absolute bottom-5 left-1/2 -translate-x-1/2 w-[85%] max-w-[1250px] flex items-center justify-around pointer-events-none">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="flex flex-col items-center">
              {/* Neon Purple Track Light Dash */}
              <div className="w-10 sm:w-16 h-1.5 rounded-full bg-[#D8B4FE] shadow-[0_0_16px_#C084FC]" />
              {/* Specular Light Trail on Glossy Floor */}
              <div className="w-8 sm:w-12 h-8 bg-gradient-to-b from-[#A855F7]/50 via-[#7C3AED]/20 to-transparent blur-[2px]" />
            </div>
          ))}
        </div>
      </div>

      {/* Bottom-Left Cylindrical Dais (3D Perspective Platform Matching Reference) */}
      <div className="absolute bottom-3 sm:bottom-6 left-4 sm:left-10 z-20 pointer-events-none">
        <div className="relative w-[190px] sm:w-[230px]">
          {/* Elliptical Glowing Top Rim */}
          <div className="w-full h-7 rounded-[100%] bg-gradient-to-r from-[#A855F7] via-[#F3E8FF] to-[#A855F7] p-[2px] shadow-[0_0_24px_#C084FC,0_0_8px_#FFF]">
            <div className="w-full h-full rounded-[100%] bg-[#1A0936]" />
          </div>
          {/* Cylindrical Curved Body */}
          <div className="-mt-3.5 w-full rounded-b-2xl bg-gradient-to-b from-[#180735] via-[#0E0322] to-[#05010E] border-x border-b border-[#7C3AED]/40 shadow-[0_12px_24px_rgba(0,0,0,0.8)] pt-4 pb-3 px-4">
            <div className="text-[9.5px] sm:text-[10.5px] font-mono tracking-[0.24em] font-bold text-[#E9D5FF] uppercase leading-[1.65] drop-shadow-[0_0_10px_rgba(192,132,252,0.6)]">
              <div>SMARTCARE AI</div>
              <div>HEALTHCARE FOR A</div>
              <div className="text-white">BRIGHTER TOMORROW</div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom-Right Cylindrical Console Pedestal Matching Reference */}
      <div className="absolute bottom-3 sm:bottom-6 right-4 sm:right-10 z-20 pointer-events-none text-left">
        <div className="relative w-[150px] sm:w-[180px]">
          {/* Glowing Top Rim */}
          <div className="w-full h-6 rounded-[100%] bg-gradient-to-r from-[#7C3AED] via-[#E9D5FF] to-[#7C3AED] p-[2px] shadow-[0_0_20px_#A855F7]">
            <div className="w-full h-full rounded-[100%] bg-[#14062E]" />
          </div>
          {/* Cylindrical Body */}
          <div className="-mt-3 w-full rounded-b-2xl bg-gradient-to-b from-[#180735] via-[#0E0322] to-[#05010E] border-x border-b border-[#7C3AED]/40 shadow-[0_12px_24px_rgba(0,0,0,0.8)] pt-4 pb-3 px-4">
            <div className="text-[9.5px] sm:text-[10.5px] font-mono tracking-[0.24em] font-bold text-purple-200 uppercase leading-[1.7] drop-shadow-[0_0_10px_rgba(168,85,247,0.5)]">
              <div>DATA</div>
              <div>INSIGHTS</div>
              <div>CARE</div>
              <div className="text-white">A HEALTHIER</div>
              <div className="text-white">TOMORROW</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// =============================================================================
// HELPER FUNCTIONS: LIVE 2D DYNAMIC NEON ECG SIGNAL LINE
// =============================================================================

function drawLiveECGLine(ctx, width, height, offset, pulseIntensity) {
  ctx.clearRect(0, 0, width, height);

  const centerY = height * 0.48;
  ctx.lineWidth = 2.0;

  // Linear gradient with soft attenuation in the middle (for pristine login card contrast)
  const grad = ctx.createLinearGradient(0, 0, width, 0);
  grad.addColorStop(0, 'rgba(216, 180, 254, 0.95)');
  grad.addColorStop(0.32, 'rgba(192, 132, 252, 0.85)');
  grad.addColorStop(0.42, 'rgba(124, 58, 237, 0.15)'); // soft in center
  grad.addColorStop(0.58, 'rgba(124, 58, 237, 0.15)'); // soft in center
  grad.addColorStop(0.68, 'rgba(192, 132, 252, 0.85)');
  grad.addColorStop(1, 'rgba(216, 180, 254, 0.95)');

  ctx.strokeStyle = grad;
  ctx.shadowColor = '#C084FC';
  ctx.shadowBlur = 8 + pulseIntensity * 12;

  ctx.beginPath();

  const period = 380;
  let isFirst = true;

  for (let x = 0; x <= width; x += 3.5) {
    const pos = (x + offset) % period;
    let y = centerY;

    if (pos > 50 && pos <= 90) {
      // P Wave
      y -= Math.sin(((pos - 50) / 40) * Math.PI) * 13;
    } else if (pos > 110 && pos <= 125) {
      // Q Dip
      y += ((pos - 110) / 15) * 12;
    } else if (pos > 125 && pos <= 150) {
      // R Peak (Sharp High Spike)
      const rPos = (pos - 125) / 25;
      if (rPos < 0.5) {
        y -= (rPos / 0.5) * (80 + pulseIntensity * 32);
      } else {
        y -= ((1 - rPos) / 0.5) * (80 + pulseIntensity * 32);
      }
    } else if (pos > 150 && pos <= 170) {
      // S Dip
      y += Math.sin(((pos - 150) / 20) * Math.PI) * 22;
    } else if (pos > 200 && pos <= 260) {
      // T Wave
      y -= Math.sin(((pos - 200) / 60) * Math.PI) * 20;
    } else {
      // Baseline micro-fluctuation
      y += Math.sin(pos * 0.08) * 1.5;
    }

    if (isFirst) {
      ctx.moveTo(x, y);
      isFirst = false;
    } else {
      ctx.lineTo(x, y);
    }
  }

  ctx.stroke();
}

function drawMiniECG(ctx, width, height, offset, pulseIntensity) {
  ctx.clearRect(0, 0, width, height);

  const centerY = height * 0.5;
  ctx.lineWidth = 1.5;
  ctx.strokeStyle = '#FB7185';
  ctx.shadowColor = '#F43F5E';
  ctx.shadowBlur = 5;

  ctx.beginPath();
  const period = 100;
  let isFirst = true;

  for (let x = 0; x <= width; x += 2) {
    const pos = (x + offset) % period;
    let y = centerY;

    if (pos > 30 && pos <= 38) {
      y += ((pos - 30) / 8) * 4;
    } else if (pos > 38 && pos <= 46) {
      const rPos = (pos - 38) / 8;
      y -= (rPos < 0.5 ? rPos / 0.5 : (1 - rPos) / 0.5) * (15 + pulseIntensity * 4);
    } else if (pos > 46 && pos <= 52) {
      y += Math.sin(((pos - 46) / 6) * Math.PI) * 5;
    } else if (pos > 60 && pos <= 76) {
      y -= Math.sin(((pos - 60) / 16) * Math.PI) * 5;
    }

    if (isFirst) {
      ctx.moveTo(x, y);
      isFirst = false;
    } else {
      ctx.lineTo(x, y);
    }
  }

  ctx.stroke();
}
