import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Bell, LogOut, Activity, Zap } from 'lucide-react';

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();

  const displayName = 'Dr. Lakshmanan';
  const roleName = user?.role || 'RADIOLOGIST';

  return (
    <header className="h-16 border-b border-amber-500/25 bg-[#0a0c16]/90 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-30">
      <div className="flex items-center space-x-3">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-amber-500 via-cyan-500 to-purple-600 flex items-center justify-center shadow-lg shadow-amber-500/20">
          <Activity className="w-5 h-5 text-slate-950 stroke-[2.5]" />
        </div>
        <div>
          <h1 className="text-base font-black tracking-tight gold-gradient-text uppercase">
            RadAI Clinical Platform
          </h1>
          <p className="text-[10px] text-amber-400 font-black tracking-widest uppercase flex items-center space-x-1">
            <span>Clinical Vision Intelligence</span>
            <Zap className="w-3 h-3 text-amber-400 inline" />
          </p>
        </div>
      </div>

      <div className="flex items-center space-x-4">
        <button className="p-2 rounded-xl text-slate-400 hover:text-amber-300 hover:bg-amber-500/10 transition-colors relative">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-amber-400 animate-ping"></span>
        </button>

        <div className="flex items-center space-x-3 pl-3 border-l border-amber-500/20">
          <div className="w-8 h-8 rounded-full bg-amber-500/20 border border-amber-500/50 flex items-center justify-center text-amber-300 font-black text-xs shadow-md">
            R
          </div>
          <div className="hidden md:block text-left">
            <p className="text-xs font-black text-slate-100">{displayName}</p>
            <p className="text-[10px] text-amber-400 font-black uppercase tracking-wider">{roleName}</p>
          </div>

          <button
            onClick={logout}
            className="p-2 rounded-xl text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition-colors ml-2"
            title="Sign Out"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
};
