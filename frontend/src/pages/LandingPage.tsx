import React from 'react';
import { Link } from 'react-router-dom';
import { Activity, ShieldCheck, Cpu, Sparkles, Bot, ArrowRight, Zap } from 'lucide-react';

export const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-[#07080e] text-slate-100 flex flex-col justify-between relative overflow-hidden">
      {/* Ambient Background Accents */}
      <div className="absolute top-1/4 left-1/4 w-[600px] h-[600px] bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-[600px] h-[600px] bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />

      {/* Header */}
      <header className="h-20 border-b border-amber-500/20 px-8 flex items-center justify-between bg-[#0a0c16]/80 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-500 via-cyan-500 to-purple-600 flex items-center justify-center shadow-lg shadow-amber-500/20">
            <Activity className="w-6 h-6 text-slate-950 stroke-[2.5]" />
          </div>
          <div>
            <span className="text-xl font-black gold-gradient-text tracking-tight uppercase">
              RadAI Clinical Platform
            </span>
            <p className="text-[10px] text-amber-400 font-black tracking-widest uppercase flex items-center space-x-1">
              <span>Clinical Vision Intelligence</span>
              <Zap className="w-3 h-3 text-amber-400 inline" />
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <Link
            to="/login"
            className="px-6 py-2.5 rounded-xl gold-button text-slate-950 font-black text-xs transition-all shadow-lg flex items-center space-x-2 uppercase tracking-wider"
          >
            <span>Launch Portal</span>
            <ArrowRight className="w-4 h-4 stroke-[2.5]" />
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="px-8 py-20 max-w-5xl mx-auto text-center space-y-8 relative z-10">
        <div className="inline-flex items-center space-x-2 px-4 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-bold uppercase tracking-wider">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Next-Generation Autonomous Radiological Intelligence</span>
        </div>

        <h1 className="text-4xl md:text-6xl font-black tracking-tight text-white leading-tight uppercase">
          Automated Medical Image Analysis <br />
          <span className="gold-gradient-text">
            For Precision Diagnosis
          </span>
        </h1>

        <p className="max-w-2xl mx-auto text-amber-100/70 text-sm leading-relaxed font-medium">
          Multi-tier AI system combining Deep Convolutional Networks (ResNet50 / EfficientNet), 
          Grad-CAM explainability heatmaps, BioBERT NLP clinical entity parsing, 
          Small Language Models (Phi-3), Generative AI synthetic data generation, and Agentic AI workflows.
        </p>

        <div className="pt-4 flex justify-center space-x-4">
          <Link
            to="/login"
            className="px-8 py-4 rounded-2xl gold-button text-slate-950 font-black text-sm transition-all shadow-2xl flex items-center space-x-2 uppercase tracking-wider"
          >
            <span>ACCESS CLINICAL PORTAL & SCANS</span>
            <ArrowRight className="w-5 h-5 stroke-[2.5]" />
          </Link>
        </div>
      </section>

      {/* Feature Cards Grid */}
      <section className="px-8 py-12 max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6 relative z-10">
        <div className="gold-panel p-6 rounded-2xl space-y-3">
          <Cpu className="w-8 h-8 text-amber-400" />
          <h3 className="text-base font-black text-slate-100 uppercase tracking-tight">Deep Learning & Grad-CAM</h3>
          <p className="text-xs text-amber-200/70 leading-relaxed font-medium">
            High-sensitivity classification for Normal, COVID-19, Pneumonia, and Tuberculosis with pixel-level Grad-CAM visual heatmaps.
          </p>
        </div>

        <div className="gold-panel p-6 rounded-2xl space-y-3">
          <Sparkles className="w-8 h-8 text-cyan-400" />
          <h3 className="text-base font-black text-slate-100 uppercase tracking-tight">SLM Report Summarization</h3>
          <p className="text-xs text-amber-200/70 leading-relaxed font-medium">
            4-bit fine-tuned Small Language Models generate concise radiologist summaries and simplified patient explanations in real time.
          </p>
        </div>

        <div className="gold-panel p-6 rounded-2xl space-y-3">
          <Bot className="w-8 h-8 text-purple-400" />
          <h3 className="text-base font-black text-slate-100 uppercase tracking-tight">Agentic AI & Doctor-in-the-Loop</h3>
          <p className="text-xs text-amber-200/70 leading-relaxed font-medium">
            Multi-agent consensus workflows cross-reference patient history and differential diagnoses with mandatory Doctor approval guardrails.
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-amber-500/20 py-6 px-8 text-center text-xs text-amber-300/60 font-mono">
        © 2026 RadAI Clinical Platform. Enterprise Medical Vision Intelligence.
      </footer>
    </div>
  );
};

export default LandingPage;
