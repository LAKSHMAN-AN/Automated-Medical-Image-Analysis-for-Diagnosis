import React, { useState } from 'react';
import { aiService } from '../services/aiService';
import { AgentDecision } from '../types';
import { Bot } from 'lucide-react';

export const AgenticAIPage: React.FC = () => {
  const [decision, setDecision] = useState<AgentDecision | null>(null);
  const [loading, setLoading] = useState(false);

  const handleRunAgent = async () => {
    setLoading(true);
    try {
      const res = await aiService.runAgenticWorkflow('PAT-2026-001', 'sample_image_id');
      setDecision(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white">Agentic AI Autonomous Diagnostic Assistant</h1>
        <p className="text-xs text-slate-400">Multi-agent state machine (LangGraph/CrewAI) coordinating perception, differential reasoning, and HITL approval</p>
      </div>

      <div className="glass-panel p-6 rounded-2xl border-slate-800 space-y-6">
        <div className="flex items-center justify-between">
          <div className="space-y-1">
            <h3 className="text-sm font-bold text-white">Autonomous Multi-Agent Consensus System</h3>
            <p className="text-xs text-slate-400">Orchestrates Image Analyst, Clinical History, and Reasoning Agents</p>
          </div>

          <button
            onClick={handleRunAgent}
            disabled={loading}
            className="px-6 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs transition-all shadow-lg flex items-center space-x-2"
          >
            <Bot className="w-4 h-4" />
            <span>{loading ? 'Agent Orchestration Running...' : 'Execute Agentic Diagnostic Workflow'}</span>
          </button>
        </div>

        {decision && (
          <div className="space-y-4 pt-4 border-t border-slate-800">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
                <span className="text-[10px] font-mono text-cyan-400 uppercase">Primary Diagnosis</span>
                <p className="text-lg font-bold text-white">{decision.primary_diagnosis}</p>
              </div>

              <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
                <span className="text-[10px] font-mono text-purple-400 uppercase">Confidence Score</span>
                <p className="text-lg font-bold text-emerald-400">{(decision.confidence_score * 100).toFixed(1)}%</p>
              </div>

              <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
                <span className="text-[10px] font-mono text-amber-400 uppercase">HITL Doctor Guardrail</span>
                <p className="text-xs font-bold text-amber-300">
                  {decision.requires_hitl_approval ? 'Mandatory Doctor Approval Required' : 'Auto-Verified'}
                </p>
              </div>
            </div>

            <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
              <span className="text-xs font-bold text-white">Agent Reasoning Summary</span>
              <p className="text-xs text-slate-300 font-sans leading-relaxed">{decision.reasoning_summary}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AgenticAIPage;
