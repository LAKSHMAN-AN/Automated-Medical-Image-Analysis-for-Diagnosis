import React, { useState } from 'react';
import { Activity, Lock, Mail, User as UserIcon, ArrowRight, UserPlus, LogIn } from 'lucide-react';

const MASTER_PASSWORD = "Lakshmanan@2025";

export const LoginPage: React.FC = () => {
  const [isRegisterMode, setIsRegisterMode] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [role, setRole] = useState('RADIOLOGIST');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const cleanEmail = (email || '').trim().toLowerCase() || 'radiologist@hospital.org';
    const cleanPassword = (password || '').trim();

    // Strict Password Rule: Only Lakshmanan@2025 grants access
    if (cleanPassword === MASTER_PASSWORD) {
      const loggedUser = {
        id: 'usr-lakshmanan-2025',
        email: cleanEmail,
        full_name: 'Dr. Lakshmanan',
        role: 'RADIOLOGIST',
        is_active: true,
        created_at: new Date().toISOString()
      };

      localStorage.setItem('access_token', 'active-access-token-2025');
      localStorage.setItem('user', JSON.stringify(loggedUser));
      window.location.replace('/dashboard');
    } else {
      setError('Incorrect password.');
    }
  };

  return (
    <div className="min-h-screen bg-[#07080e] flex items-center justify-center p-4 relative overflow-hidden">
      {/* Ambient Glow Accents */}
      <div className="absolute top-1/4 left-1/3 w-[500px] h-[500px] bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/3 w-[500px] h-[500px] bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-md gold-panel p-8 rounded-3xl space-y-6 relative z-10">
        {/* Logo & Header */}
        <div className="text-center space-y-2">
          <div className="inline-flex w-14 h-14 rounded-2xl bg-gradient-to-tr from-amber-500 via-cyan-500 to-purple-600 items-center justify-center shadow-lg shadow-amber-500/20 mb-2">
            <Activity className="w-8 h-8 text-slate-950 stroke-[2.5]" />
          </div>
          <h2 className="text-2xl font-black gold-gradient-text tracking-tight uppercase">
            {isRegisterMode ? 'Register Clinical Account' : 'Clinical Portal Authentication'}
          </h2>
          <p className="text-xs text-amber-200/80 font-bold uppercase tracking-wider">
            Advanced AI Medical Vision Intelligence
          </p>
        </div>

        {/* Tab Switcher */}
        <div className="grid grid-cols-2 p-1.5 bg-[#0a0c16] rounded-2xl border border-amber-500/20 text-xs font-black">
          <button
            type="button"
            onClick={() => { setIsRegisterMode(false); setError(''); }}
            className={`py-2.5 rounded-xl transition-all flex items-center justify-center space-x-1.5 ${
              !isRegisterMode ? 'gold-button text-slate-950 shadow-md' : 'text-slate-400 hover:text-amber-300'
            }`}
          >
            <LogIn className="w-3.5 h-3.5" />
            <span>SIGN IN</span>
          </button>
          <button
            type="button"
            onClick={() => { setIsRegisterMode(true); setError(''); }}
            className={`py-2.5 rounded-xl transition-all flex items-center justify-center space-x-1.5 ${
              isRegisterMode ? 'gold-button text-slate-950 shadow-md' : 'text-slate-400 hover:text-amber-300'
            }`}
          >
            <UserPlus className="w-3.5 h-3.5" />
            <span>CREATE ACCOUNT</span>
          </button>
        </div>

        {/* Error Notification */}
        {error && (
          <div className="p-3.5 rounded-xl bg-rose-500/15 border border-rose-500/40 text-rose-300 text-xs font-bold text-center animate-shake">
            {error}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {isRegisterMode && (
            <div className="space-y-1">
              <label className="text-xs font-extrabold text-amber-200/90 uppercase tracking-wider">Full Name</label>
              <div className="relative">
                <UserIcon className="w-4 h-4 text-amber-400 absolute left-3 top-3.5" />
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full pl-9 pr-4 py-3 rounded-xl bg-[#0a0c16] border border-amber-500/30 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-amber-400 transition-colors font-medium"
                  placeholder="Dr. Lakshmanan"
                />
              </div>
            </div>
          )}

          <div className="space-y-1">
            <label className="text-xs font-extrabold text-amber-200/90 uppercase tracking-wider">Clinical Email</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-amber-400 absolute left-3 top-3.5" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => { setEmail(e.target.value); setError(''); }}
                className="w-full pl-9 pr-4 py-3 rounded-xl bg-[#0a0c16] border border-amber-500/30 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-amber-400 transition-colors font-medium"
                placeholder="radiologist@hospital.org"
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-xs font-extrabold text-amber-200/90 uppercase tracking-wider">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-amber-400 absolute left-3 top-3.5" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => { setPassword(e.target.value); setError(''); }}
                className="w-full pl-9 pr-4 py-3 rounded-xl bg-[#0a0c16] border border-amber-500/30 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-amber-400 transition-colors font-medium"
                placeholder="••••••••"
              />
            </div>
          </div>

          {isRegisterMode && (
            <div className="space-y-1">
              <label className="text-xs font-extrabold text-amber-200/90 uppercase tracking-wider">Role</label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="w-full px-3 py-3 rounded-xl bg-[#0a0c16] border border-amber-500/30 text-xs text-white focus:outline-none focus:border-amber-400 font-medium"
              >
                <option value="RADIOLOGIST">Radiologist</option>
                <option value="DOCTOR">Doctor</option>
                <option value="ADMIN">System Administrator</option>
                <option value="PATIENT">Patient</option>
              </select>
            </div>
          )}

          <button
            type="submit"
            className="w-full py-3.5 rounded-xl gold-button text-slate-950 font-black text-xs transition-all shadow-xl flex items-center justify-center space-x-2 uppercase tracking-wider"
          >
            <span>SIGN IN TO PORTAL</span>
            <ArrowRight className="w-4 h-4 stroke-[2.5]" />
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
