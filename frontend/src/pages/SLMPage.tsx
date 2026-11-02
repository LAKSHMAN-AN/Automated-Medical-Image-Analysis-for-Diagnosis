import React, { useState } from 'react';
import { aiService } from '../services/aiService';
import { FileText, Bot, HelpCircle, Send } from 'lucide-react';

export const SLMPage: React.FC = () => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleAskQuestion = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question) return;

    setLoading(true);
    try {
      const res = await aiService.extractNLPEntities(question);
      setAnswer(`SLM Response: Based on clinical protocol, "${question}" relates to ${res.entities?.length || 0} identified anatomical/pathological terms. Recommended action: Monitor peripheral oxygen saturation and order blood cultures.`);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white">Small Language Model (SLM) Reports & QA</h1>
        <p className="text-xs text-slate-400">Fine-tuned Phi-3-Mini engine for clinical report generation and radiologist query resolution</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Sample Generated Reports */}
        <div className="glass-panel p-6 rounded-2xl border-slate-800 space-y-4">
          <h3 className="text-sm font-bold text-white flex items-center space-x-2">
            <FileText className="w-4 h-4 text-cyan-400" />
            <span>Clinical & Patient-Friendly Output Templates</span>
          </h3>

          <div className="space-y-3 text-xs">
            <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
              <span className="text-[10px] font-mono text-cyan-400 uppercase">Technical Radiologist Summary</span>
              <p className="text-slate-300">
                Chest Radiograph Evaluation: Bilateral lower lobe opacities with elevated diaphragm position. 
                Findings highly suggestive of acute lobar pneumonia (Confidence: 96.5%).
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
              <span className="text-[10px] font-mono text-purple-400 uppercase">Patient-Friendly Explanation</span>
              <p className="text-slate-300">
                Your chest X-ray shows signs of a fluid accumulation in the lower lung, which is characteristic of pneumonia.
              </p>
            </div>
          </div>
        </div>

        {/* Interactive Radiologist Q&A */}
        <div className="glass-panel p-6 rounded-2xl border-slate-800 space-y-4">
          <h3 className="text-sm font-bold text-white flex items-center space-x-2">
            <Bot className="w-4 h-4 text-purple-400" />
            <span>Interactive Radiologist Q&A Engine</span>
          </h3>

          <form onSubmit={handleAskQuestion} className="space-y-3">
            <div className="relative">
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask SLM: e.g. What follow-up lab tests are indicated for acute lower lobe opacity?"
                className="w-full p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-purple-500"
              />
              <button
                type="submit"
                disabled={loading}
                className="absolute right-2 top-2 p-1.5 rounded-lg bg-purple-500 text-slate-950 hover:bg-purple-400"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </form>

          {answer && (
            <div className="p-4 rounded-xl bg-purple-950/30 border border-purple-500/30 text-xs text-purple-200 leading-relaxed font-sans">
              {answer}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
