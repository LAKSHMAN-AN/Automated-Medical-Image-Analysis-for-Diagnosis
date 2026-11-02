import React, { useState } from 'react';
import { useLocation, Link } from 'react-router-dom';
import { Prediction, MedicalImage } from '../types';
import { aiService } from '../services/aiService';
import { Activity, Eye, CheckCircle2, AlertTriangle, FileText, Bot, ArrowLeft } from 'lucide-react';

export const PredictionPage: React.FC = () => {
  const location = useLocation();
  const prediction = location.state?.prediction as Prediction;
  const image = location.state?.image as MedicalImage;

  const [showGradCAM, setShowGradCAM] = useState(true);
  const [reportText, setReportText] = useState<string | null>(null);
  const [loadingReport, setLoadingReport] = useState(false);
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);

  if (!prediction) {
    return (
      <div className="text-center py-20 space-y-4">
        <p className="text-slate-400 text-sm">No prediction data loaded.</p>
        <Link to="/upload" className="text-cyan-400 text-xs hover:underline">Upload a scan to view predictions</Link>
      </div>
    );
  }

  const handleGenerateReport = async () => {
    setLoadingReport(true);
    try {
      const rep = await aiService.generateSLMReport(prediction.id);
      setReportText(rep.slm_clinical_summary);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingReport(false);
    }
  };

  const handleDoctorAction = async (action: 'APPROVED' | 'REJECTED') => {
    try {
      await aiService.submitDoctorFeedback(prediction.id, action, 'Verified by radiologist.');
      setFeedbackSubmitted(true);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Top Controls */}
      <div className="flex items-center justify-between">
        <Link to="/upload" className="inline-flex items-center space-x-2 text-xs text-slate-400 hover:text-white">
          <ArrowLeft className="w-4 h-4" />
          <span>Upload Another Scan</span>
        </Link>
        <div className="flex items-center space-x-2">
          <span className="text-xs font-mono text-cyan-400">ID: {prediction.id.substring(0, 8)}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Left: Scan Viewport */}
        <div className="glass-panel p-6 rounded-2xl border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-white flex items-center space-x-2">
              <Eye className="w-4 h-4 text-cyan-400" />
              <span>Radiological Image Viewport</span>
            </h3>
            <button
              onClick={() => setShowGradCAM(!showGradCAM)}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono transition-all ${
                showGradCAM ? 'bg-cyan-500 text-slate-950 font-bold' : 'bg-slate-900 text-slate-400 hover:text-white'
              }`}
            >
              Grad-CAM Overlay: {showGradCAM ? 'ON' : 'OFF'}
            </button>
          </div>

          <div className="relative rounded-xl overflow-hidden bg-slate-950 border border-slate-800 min-h-[300px] flex items-center justify-center">
            {image?.image_url ? (
              <img src={image.image_url} alt="Medical Scan" className="max-h-80 object-contain" />
            ) : (
              <div className="p-8 text-center space-y-2">
                <Activity className="w-10 h-10 text-cyan-500 mx-auto animate-pulse" />
                <p className="text-xs font-mono text-slate-400">Chest Radiograph Scan (Normalized Tensor)</p>
              </div>
            )}
          </div>
        </div>

        {/* Right: Diagnosis Details */}
        <div className="space-y-6">
          <div className="glass-panel p-6 rounded-2xl border-slate-800 space-y-4">
            <div className="space-y-1">
              <span className="text-[10px] uppercase tracking-wider font-mono text-cyan-400">Deep Learning Prediction</span>
              <h2 className="text-3xl font-extrabold text-white flex items-center justify-between">
                <span>{prediction.predicted_class}</span>
                <span className="text-lg font-mono text-emerald-400">{(prediction.confidence_score * 100).toFixed(1)}%</span>
              </h2>
            </div>

            {/* Probability Breakdown */}
            <div className="space-y-2 border-t border-slate-900 pt-4">
              <span className="text-xs font-medium text-slate-400">Class Probabilities</span>
              {Object.entries(prediction.class_probabilities || {}).map(([cls, prob]) => (
                <div key={cls} className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-300 font-mono">{cls}</span>
                    <span className="text-slate-400 font-mono">{(prob * 100).toFixed(1)}%</span>
                  </div>
                  <div className="w-full h-1.5 rounded-full bg-slate-900 overflow-hidden">
                    <div className="h-full bg-cyan-500" style={{ width: `${prob * 100}%` }}></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* SLM Summary Box */}
          <div className="glass-panel p-6 rounded-2xl border-slate-800 space-y-3">
            <h3 className="text-xs font-bold text-white flex items-center space-x-2">
              <Bot className="w-4 h-4 text-purple-400" />
              <span>Small Language Model (Phi-3) Summary</span>
            </h3>

            {reportText ? (
              <p className="text-xs text-slate-300 leading-relaxed font-sans bg-slate-900/60 p-3 rounded-xl border border-slate-800">
                {reportText}
              </p>
            ) : (
              <button
                onClick={handleGenerateReport}
                disabled={loadingReport}
                className="w-full py-2.5 rounded-xl bg-purple-600/20 hover:bg-purple-600/30 border border-purple-500/30 text-purple-300 text-xs font-semibold transition-all"
              >
                {loadingReport ? 'Generating SLM Report...' : 'Generate Contextual Clinical Report'}
              </button>
            )}
          </div>

          {/* Doctor Approval Workflow */}
          <div className="glass-panel p-4 rounded-2xl border-slate-800 flex items-center justify-between">
            <span className="text-xs font-medium text-slate-300">Doctor Verification</span>
            {feedbackSubmitted ? (
              <span className="text-xs text-emerald-400 font-mono flex items-center space-x-1">
                <CheckCircle2 className="w-4 h-4" />
                <span>Feedback Saved</span>
              </span>
            ) : (
              <div className="flex space-x-2">
                <button
                  onClick={() => handleDoctorAction('APPROVED')}
                  className="px-4 py-2 rounded-lg bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 text-xs font-semibold hover:bg-emerald-500/30"
                >
                  Approve
                </button>
                <button
                  onClick={() => handleDoctorAction('REJECTED')}
                  className="px-4 py-2 rounded-lg bg-rose-500/20 border border-rose-500/40 text-rose-300 text-xs font-semibold hover:bg-rose-500/30"
                >
                  Reject / Flag
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
