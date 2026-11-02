import React from 'react';
import { ShieldCheck, UserCheck, Cpu, Database, KeyRound } from 'lucide-react';

export const AdminPanelPage: React.FC = () => {
  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white">System Admin Control Center</h1>
        <p className="text-xs text-slate-400">Node cluster status, user permission management, and audit log monitoring</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-panel p-5 rounded-2xl border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-medium">FastAPI Backend Gateway</span>
            <Cpu className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-lg font-bold text-white">Healthy (100% Uptime)</p>
          <p className="text-[10px] text-emerald-400 font-mono">Port 8000 / Uvicorn</p>
        </div>

        <div className="glass-panel p-5 rounded-2xl border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-medium">PostgreSQL Database</span>
            <Database className="w-4 h-4 text-cyan-400" />
          </div>
          <p className="text-lg font-bold text-white">Connected (3 Pool Conns)</p>
          <p className="text-[10px] text-cyan-400 font-mono">PostgreSQL 15</p>
        </div>

        <div className="glass-panel p-5 rounded-2xl border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-medium">PyTorch DL Model Weights</span>
            <ShieldCheck className="w-4 h-4 text-purple-400" />
          </div>
          <p className="text-lg font-bold text-white">Loaded (ResNet50 / EffNet)</p>
          <p className="text-[10px] text-purple-400 font-mono">CUDA / CPU Execution</p>
        </div>
      </div>

      <div className="glass-panel p-6 rounded-2xl border-slate-800 space-y-4">
        <h3 className="text-sm font-bold text-white">Registered Clinical Accounts</h3>
        <div className="divide-y divide-slate-800 text-xs">
          <div className="py-3 flex justify-between items-center">
            <div>
              <p className="font-bold text-white">System Administrator (admin@medicalai.org)</p>
              <p className="text-[10px] text-slate-400 font-mono">Role: ADMIN</p>
            </div>
            <span className="px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 font-mono text-[10px]">Active</span>
          </div>

          <div className="py-3 flex justify-between items-center">
            <div>
              <p className="font-bold text-white">Dr. Eleanor Vance, MD (radiologist@hospital.org)</p>
              <p className="text-[10px] text-slate-400 font-mono">Role: RADIOLOGIST</p>
            </div>
            <span className="px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 font-mono text-[10px]">Active</span>
          </div>
        </div>
      </div>
    </div>
  );
};
