import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Upload, 
  Users, 
  FileText, 
  Sparkles, 
  Bot, 
  BarChart3, 
  ShieldCheck, 
  Activity,
  Zap
} from 'lucide-react';

const navigation = [
  { name: 'Dashboard', to: '/dashboard', icon: LayoutDashboard },
  { name: 'Upload Medical Scan', to: '/upload', icon: Upload },
  { name: 'Patient Records', to: '/patients', icon: Users },
  { name: 'SLM Reports', to: '/slm-reports', icon: FileText },
  { name: 'GenAI Augmentation', to: '/genai', icon: Sparkles },
  { name: 'Agentic AI Assistant', to: '/agentic-ai', icon: Bot },
  { name: 'Analytics & KPIs', to: '/analytics', icon: BarChart3 },
  { name: 'Admin Control', to: '/admin', icon: ShieldCheck },
];

export const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 bg-[#0a0c16] border-r border-amber-500/20 flex flex-col justify-between p-4 hidden md:flex">
      <div className="space-y-6">
        <div className="px-3 text-[10px] font-black text-amber-400/80 uppercase tracking-widest flex items-center space-x-1.5 font-mono">
          <Zap className="w-3.5 h-3.5 text-amber-400 stroke-[2.5]" />
          <span>Clinical Intelligence Platform</span>
        </div>
        <nav className="space-y-1">
          {navigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center space-x-3 px-3.5 py-2.5 rounded-xl text-xs font-black transition-all ${
                  isActive
                    ? 'bg-gradient-to-r from-amber-500/20 via-cyan-500/15 to-purple-500/10 text-amber-300 border border-amber-500/40 shadow-lg shadow-amber-500/10'
                    : 'text-slate-400 hover:text-amber-300 hover:bg-amber-500/5'
                }`
              }
            >
              <item.icon className="w-4 h-4" />
              <span>{item.name}</span>
            </NavLink>
          ))}
        </nav>
      </div>

      <div className="p-3.5 gold-panel rounded-xl border-amber-500/30">
        <div className="flex items-center space-x-2 text-xs text-amber-300 font-black mb-1">
          <Activity className="w-4 h-4 text-amber-400 stroke-[2.5]" />
          <span>Clinical Engine Status</span>
        </div>
        <p className="text-[11px] text-slate-300 font-medium">98.65% Vision Accuracy</p>
      </div>
    </aside>
  );
};
