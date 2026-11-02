import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  Activity,
  Sparkles,
  UploadCloud,
  Bot,
  Brain,
  TrendingUp,
  ArrowUpRight,
  Clock,
  ShieldCheck,
  CheckCircle2,
  Zap
} from 'lucide-react';

export const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const displayName = 'Dr. Lakshmanan';

  const stats = [
    {
      title: 'Total Medical Scans Analyzed',
      value: '14,892',
      change: '+18.4% this month',
      icon: Activity,
      gradient: 'from-amber-500 via-orange-500 to-yellow-400',
      glow: 'glow-gold'
    },
    {
      title: 'Deep Learning Accuracy Rate',
      value: '98.65%',
      change: 'ResNet50 + EfficientNet',
      icon: Sparkles,
      gradient: 'from-cyan-500 via-blue-600 to-indigo-600',
      glow: 'glow-cyan'
    },
    {
      title: 'Agentic AI Diagnostic Runs',
      value: '3,410',
      change: 'LangGraph 9-Agent Consensus',
      icon: Bot,
      gradient: 'from-purple-600 via-pink-500 to-amber-500',
      glow: 'glow-purple'
    },
    {
      title: 'SLM Reports Generated',
      value: '8,950',
      change: 'Phi-3 SLM Clinical Summaries',
      icon: Brain,
      gradient: 'from-amber-500 via-cyan-500 to-blue-600',
      glow: 'glow-gold'
    }
  ];

  const quickActions = [
    {
      title: 'Upload & Analyze Scan',
      desc: 'Ingest CXR, Brain MRI, or CT Scan for instant deep learning prediction & Grad-CAM visual heatmap.',
      route: '/upload',
      icon: UploadCloud,
      badge: 'Real-Time AI',
      buttonBg: 'gold-button'
    },
    {
      title: 'SLM Clinical Reports',
      desc: 'Generate technical radiologist findings and patient-friendly explanations with Phi-3 SLM.',
      route: '/slm-reports',
      icon: Sparkles,
      badge: 'Language AI',
      buttonBg: 'bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500'
    },
    {
      title: 'Agentic AI Assistant',
      desc: 'Run multi-agent differential diagnosis consensus with Doctor-in-the-Loop approval workflows.',
      route: '/agentic-ai',
      icon: Bot,
      badge: '9 Agents Active',
      buttonBg: 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500'
    },
    {
      title: 'Synthetic GenAI Suite',
      desc: 'Synthesize rare disease pathology samples (DCGAN/Diffusion) for dataset augmentation.',
      route: '/genai',
      icon: Brain,
      badge: 'FID < 15.0',
      buttonBg: 'bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-400 hover:to-orange-500'
    }
  ];

  const recentScans = [
    {
      id: 'SCAN-2026-8801',
      patient: 'PAT-2026-001',
      modality: 'Chest X-Ray',
      diagnosis: 'Pneumonia (Lobar)',
      confidence: '98.4%',
      status: 'VERIFIED',
      time: '12 mins ago',
      severity: 'HIGH'
    },
    {
      id: 'SCAN-2026-8802',
      patient: 'PAT-2026-004',
      modality: 'Brain MRI',
      diagnosis: 'Glioma Tumor (Frontal Lobe)',
      confidence: '96.8%',
      status: 'REVIEW REQUIRED',
      time: '34 mins ago',
      severity: 'CRITICAL'
    },
    {
      id: 'SCAN-2026-8803',
      patient: 'PAT-2026-009',
      modality: 'Lung CT Scan',
      diagnosis: 'Pulmonary Nodules',
      confidence: '95.1%',
      status: 'VERIFIED',
      time: '1 hr ago',
      severity: 'MODERATE'
    },
    {
      id: 'SCAN-2026-8804',
      patient: 'PAT-2026-012',
      modality: 'Chest X-Ray',
      diagnosis: 'Normal CXR',
      confidence: '99.2%',
      status: 'VERIFIED',
      time: '2 hrs ago',
      severity: 'NORMAL'
    }
  ];

  return (
    <div className="space-y-8 pb-12">
      {/* Header Banner */}
      <div className="relative overflow-hidden rounded-3xl p-8 bg-gradient-to-r from-[#141208]/95 via-[#0e1824]/95 to-[#130b1e]/95 border border-amber-500/30 shadow-2xl gold-panel glow-gold">
        <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-amber-500/20 via-cyan-500/20 to-transparent rounded-full blur-3xl -mr-20 -mt-20 pointer-events-none" />
        <div className="absolute bottom-0 left-1/3 w-64 h-64 bg-cyan-500/10 rounded-full blur-2xl pointer-events-none" />

        <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-3">
            <div className="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-amber-500/15 border border-amber-500/40 text-amber-300 text-xs font-black uppercase tracking-wider shadow-inner">
              <Zap className="w-4 h-4 text-amber-400 stroke-[2.5]" />
              <span>Enterprise Clinical Intelligence Platform</span>
            </div>
            <h1 className="text-3xl md:text-5xl font-black text-white tracking-tight uppercase">
              Welcome Back, <span className="gold-gradient-text">{displayName}</span>
            </h1>
            <p className="text-sm text-slate-300 max-w-2xl font-medium leading-relaxed">
              Automated Medical Image Analysis platform online. Deep Learning Vision (ResNet50), Phi-3 SLM Medical Summarizer, DCGAN Synthetic Generator, and 9-Agent Consensus active.
            </p>
          </div>

          <button
            onClick={() => navigate('/upload')}
            className="gold-button px-6 py-3.5 rounded-2xl text-slate-950 font-black text-sm flex items-center space-x-2 shadow-xl whitespace-nowrap uppercase tracking-wider"
          >
            <UploadCloud className="w-5 h-5 stroke-[2.5]" />
            <span>Launch Rapid Diagnostic Scan</span>
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {stats.map((stat, idx) => {
          const IconComp = stat.icon;
          return (
            <div
              key={idx}
              className={`gold-panel p-6 rounded-2xl relative overflow-hidden transition-all duration-300 hover:-translate-y-1 hover:border-amber-500/50 ${stat.glow}`}
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-black text-slate-400 uppercase tracking-wider">{stat.title}</span>
                <div className={`p-2.5 rounded-xl bg-gradient-to-tr ${stat.gradient} text-slate-950 shadow-md`}>
                  <IconComp className="w-5 h-5 stroke-[2.5]" />
                </div>
              </div>
              <div className="mt-4">
                <span className="text-3xl font-black text-white tracking-tight">{stat.value}</span>
                <p className="text-xs font-extrabold text-amber-400 mt-1 flex items-center space-x-1">
                  <TrendingUp className="w-3.5 h-3.5 inline mr-1" />
                  <span>{stat.change}</span>
                </p>
              </div>
            </div>
          );
        })}
      </div>

      {/* Quick Action Cards Grid */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Activity className="w-5 h-5 text-amber-400 stroke-[2.5]" />
            <h2 className="text-xl font-black text-white uppercase tracking-tight">Clinical AI Workflows</h2>
          </div>
          <span className="text-xs font-black text-cyan-400 uppercase tracking-wider">
            All Systems Operational
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {quickActions.map((action, idx) => {
            const ActionIcon = action.icon;
            return (
              <div
                key={idx}
                onClick={() => navigate(action.route)}
                className="gold-panel-interactive p-6 rounded-2xl cursor-pointer group flex flex-col justify-between space-y-4"
              >
                <div className="flex items-start justify-between">
                  <div className="p-3 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-400 group-hover:scale-110 transition-transform">
                    <ActionIcon className="w-6 h-6 stroke-[2.5]" />
                  </div>
                  <span className="px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-wider bg-amber-500/20 border border-amber-500/40 text-amber-300">
                    {action.badge}
                  </span>
                </div>

                <div className="space-y-1">
                  <h3 className="text-lg font-black text-white group-hover:text-amber-300 transition-colors flex items-center space-x-2">
                    <span>{action.title}</span>
                    <ArrowUpRight className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity text-cyan-400" />
                  </h3>
                  <p className="text-xs text-slate-300 leading-relaxed font-normal">{action.desc}</p>
                </div>

                <div className="pt-2">
                  <div className={`w-full py-2.5 rounded-xl ${action.buttonBg} text-slate-950 font-black text-xs text-center shadow-lg transition-all uppercase tracking-wider`}>
                    Open Feature Viewport
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Recent Activity Table */}
      <div className="gold-panel rounded-2xl p-6 space-y-5">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Clock className="w-5 h-5 text-cyan-400" />
            <h3 className="text-lg font-black text-white uppercase tracking-tight">Recent Clinical Diagnostic Runs</h3>
          </div>
          <button
            onClick={() => navigate('/upload')}
            className="text-xs font-black text-amber-400 hover:text-amber-300 transition-colors flex items-center space-x-1 uppercase tracking-wider"
          >
            <span>View All Predictions</span>
            <ArrowUpRight className="w-4 h-4" />
          </button>
        </div>

        <div className="overflow-x-auto custom-scrollbar">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-amber-500/20 text-slate-400 uppercase text-[10px] font-black tracking-wider">
                <th className="py-3 px-4">Scan ID</th>
                <th className="py-3 px-4">Patient Code</th>
                <th className="py-3 px-4">Modality</th>
                <th className="py-3 px-4">Primary AI Diagnosis</th>
                <th className="py-3 px-4">DL Confidence</th>
                <th className="py-3 px-4">Severity</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4 text-right">Time</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-amber-500/10 text-slate-200 font-medium">
              {recentScans.map((scan, idx) => (
                <tr key={idx} className="hover:bg-amber-500/5 transition-colors">
                  <td className="py-3.5 px-4 font-mono font-black text-amber-400">{scan.id}</td>
                  <td className="py-3.5 px-4 font-mono text-slate-300">{scan.patient}</td>
                  <td className="py-3.5 px-4">{scan.modality}</td>
                  <td className="py-3.5 px-4 font-bold text-white">{scan.diagnosis}</td>
                  <td className="py-3.5 px-4 font-mono font-black text-emerald-400">{scan.confidence}</td>
                  <td className="py-3.5 px-4">
                    <span
                      className={`px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase ${
                        scan.severity === 'CRITICAL'
                          ? 'bg-rose-500/20 border border-rose-500/50 text-rose-300 shadow-sm'
                          : scan.severity === 'HIGH'
                          ? 'bg-amber-500/20 border border-amber-500/50 text-amber-300'
                          : scan.severity === 'MODERATE'
                          ? 'bg-purple-500/20 border border-purple-500/50 text-purple-300'
                          : 'bg-emerald-500/20 border border-emerald-500/50 text-emerald-400'
                      }`}
                    >
                      {scan.severity}
                    </span>
                  </td>
                  <td className="py-3.5 px-4">
                    <span className="inline-flex items-center space-x-1 text-[11px] font-semibold text-slate-200">
                      <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400 inline" />
                      <span>{scan.status}</span>
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-right text-slate-400 text-[11px]">{scan.time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
