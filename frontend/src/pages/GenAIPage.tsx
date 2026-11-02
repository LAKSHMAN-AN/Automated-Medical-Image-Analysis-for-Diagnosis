import React, { useState } from 'react';
import { aiService } from '../services/aiService';
import { Sparkles, RefreshCw, CheckCircle2 } from 'lucide-react';

export const GenAIPage: React.FC = () => {
  const [pathology, setPathology] = useState('TUBERCULOSIS');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const res = await aiService.generateSyntheticScan(pathology);
      setResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white">Generative AI Data Augmentation Engine</h1>
        <p className="text-xs text-slate-400">Generate high-fidelity synthetic radiological scans for rare pathology class balancing (StyleGAN3 / Diffusion)</p>
      </div>

      <div className="glass-panel p-6 rounded-2xl border-slate-800 space-y-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="space-y-1 w-full md:w-1/2">
            <label className="text-xs text-slate-300">Target Rare Pathology Class</label>
            <select
              value={pathology}
              onChange={(e) => setPathology(e.target.value)}
              className="w-full p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
            >
              <option value="TUBERCULOSIS">Tuberculosis (Apical Cavitary Lesions)</option>
              <option value="COVID">COVID-19 (Bilateral Ground-Glass Opacities)</option>
              <option value="PNEUMONIA">Lobar Pneumonia (Consolidation)</option>
            </select>
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading}
            className="w-full md:w-auto px-6 py-2.5 rounded-xl bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-400 hover:to-purple-500 text-white font-bold text-xs transition-all shadow-lg flex items-center justify-center space-x-2"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            <span>{loading ? 'Synthesizing Image...' : 'Generate Synthetic Scan'}</span>
          </button>
        </div>

        {result && (
          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-white flex items-center space-x-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <span>Synthetic Scan Generated Successfully</span>
              </span>
              <span className="text-xs font-mono text-purple-400">FID Score: {result.fid_score}</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800">Filename: {result.filename}</div>
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800">Status: {result.status}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
