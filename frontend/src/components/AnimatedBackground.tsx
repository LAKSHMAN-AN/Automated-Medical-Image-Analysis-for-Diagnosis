import React, { useEffect, useRef } from 'react';

export const AnimatedBackground: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const handleResize = () => {
      if (!canvas) return;
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };
    window.addEventListener('resize', handleResize);

    // Particle nodes for video-like animated mesh
    const particleCount = Math.floor(Math.min(width, height) / 15);
    const particles: Array<{
      x: number;
      y: number;
      vx: number;
      vy: number;
      radius: number;
      alpha: number;
    }> = [];

    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.8,
        vy: (Math.random() - 0.5) * 0.8,
        radius: Math.random() * 2 + 1,
        alpha: Math.random() * 0.5 + 0.3
      });
    }

    let time = 0;

    const render = () => {
      time += 0.015;
      ctx.clearRect(0, 0, width, height);

      // 1. Draw Animated Fluid Gradient Video Waves
      const grad1 = ctx.createLinearGradient(
        Math.sin(time) * width, 
        0, 
        Math.cos(time) * width, 
        height
      );
      grad1.addColorStop(0, 'rgba(13, 4, 10, 0.95)');
      grad1.addColorStop(0.35, 'rgba(35, 8, 26, 0.85)');
      grad1.addColorStop(0.7, 'rgba(26, 6, 20, 0.9)');
      grad1.addColorStop(1, 'rgba(7, 2, 8, 0.98)');
      ctx.fillStyle = grad1;
      ctx.fillRect(0, 0, width, height);

      // 2. Draw Pulsing Glowing Energy Orbs
      const orbX1 = width * 0.3 + Math.sin(time * 0.8) * 150;
      const orbY1 = height * 0.4 + Math.cos(time * 0.6) * 100;
      const orbGrad1 = ctx.createRadialGradient(orbX1, orbY1, 10, orbX1, orbY1, 280);
      orbGrad1.addColorStop(0, 'rgba(244, 63, 94, 0.25)');
      orbGrad1.addColorStop(0.5, 'rgba(236, 72, 153, 0.12)');
      orbGrad1.addColorStop(1, 'rgba(0, 0, 0, 0)');
      ctx.fillStyle = orbGrad1;
      ctx.beginPath();
      ctx.arc(orbX1, orbY1, 280, 0, Math.PI * 2);
      ctx.fill();

      const orbX2 = width * 0.75 + Math.cos(time * 0.7) * 120;
      const orbY2 = height * 0.65 + Math.sin(time * 0.9) * 120;
      const orbGrad2 = ctx.createRadialGradient(orbX2, orbY2, 10, orbX2, orbY2, 320);
      orbGrad2.addColorStop(0, 'rgba(225, 29, 72, 0.22)');
      orbGrad2.addColorStop(0.5, 'rgba(168, 85, 247, 0.1)');
      orbGrad2.addColorStop(1, 'rgba(0, 0, 0, 0)');
      ctx.fillStyle = orbGrad2;
      ctx.beginPath();
      ctx.arc(orbX2, orbY2, 320, 0, Math.PI * 2);
      ctx.fill();

      // 3. Connect Particle Nodes with Animated Constellation Lines
      for (let i = 0; i < particles.length; i++) {
        const p1 = particles[i];
        p1.x += p1.vx;
        p1.y += p1.vy;

        if (p1.x < 0 || p1.x > width) p1.vx *= -1;
        if (p1.y < 0 || p1.y > height) p1.vy *= -1;

        // Draw particle dot
        ctx.beginPath();
        ctx.arc(p1.x, p1.y, p1.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(244, 63, 94, ${p1.alpha})`;
        ctx.shadowBlur = 10;
        ctx.shadowColor = 'rgba(236, 72, 153, 0.8)';
        ctx.fill();
        ctx.shadowBlur = 0;

        // Connect nearby particles
        for (let j = i + 1; j < particles.length; j++) {
          const p2 = particles[j];
          const dx = p1.x - p2.x;
          const dy = p1.y - p2.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 130) {
            const lineAlpha = (1 - dist / 130) * 0.25;
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = `rgba(236, 72, 153, ${lineAlpha})`;
            ctx.lineWidth = 0.8;
            ctx.stroke();
          }
        }
      }

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none z-0 w-full h-full"
    />
  );
};

export default AnimatedBackground;
