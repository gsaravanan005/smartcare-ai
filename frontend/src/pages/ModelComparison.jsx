import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Layers, BarChart2, ShieldCheck, RefreshCw, GitCompare, CheckCircle2 } from 'lucide-react';

export default function ModelComparison() {
  const [disease, setDisease] = useState('diabetes');
  const [evalData, setEvalData] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadEvaluation = async (dis) => {
    setLoading(true);
    try {
      const res = await api.get(`/models/evaluations/${dis}`);
      setEvalData(res.data);
    } catch (err) {
      console.error("Evaluation record error:", err);
      setEvalData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEvaluation(disease);
  }, [disease]);

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center space-x-2 text-xs font-bold uppercase tracking-widest text-teal-400 mb-1">
            <GitCompare className="w-4 h-4" />
            <span>MLOps Research & Model Comparison Hub</span>
          </div>
          <h1 className="text-2xl font-extrabold text-white">Comorbidity & Multi-Task Model Performance Benchmark</h1>
        </div>

        <div className="flex items-center space-x-2 bg-slate-900 p-1.5 rounded-xl border border-slate-800">
          {[
            { id: 'diabetes', label: 'Diabetes Model' },
            { id: 'cardio', label: 'CVD Model' },
            { id: 'ckd', label: 'CKD Model' }
          ].map(d => (
            <button
              key={d.id}
              onClick={() => setDisease(d.id)}
              className={`px-4 py-2 rounded-lg text-xs font-bold transition ${
                disease === d.id
                  ? 'bg-sky-500 text-slate-950 shadow-md shadow-sky-500/20'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              {d.label}
            </button>
          ))}
        </div>
      </div>

      {/* Independent vs Multi-Task Benchmark Table */}
      <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
        <h3 className="text-base font-bold text-white flex items-center space-x-2">
          <Layers className="w-5 h-5 text-sky-400" />
          <span>Independent vs Multi-Task Empirical Benchmark (Isolated Test Set)</span>
        </h3>

        <div className="overflow-x-auto border border-slate-800 rounded-xl">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900 text-slate-400 uppercase font-semibold">
              <tr>
                <th className="p-3">Disease Target</th>
                <th className="p-3">Independent Model</th>
                <th className="p-3">Independent ROC-AUC</th>
                <th className="p-3">Independent Recall</th>
                <th className="p-3">Multi-Task ROC-AUC</th>
                <th className="p-3">Multi-Task Recall</th>
                <th className="p-3">Winning Architecture</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 font-mono text-slate-300">
              <tr className="hover:bg-slate-800/40">
                <td className="p-3 font-bold text-white">DIABETES</td>
                <td className="p-3 text-sky-400">XGBoost</td>
                <td className="p-3">0.8233</td>
                <td className="p-3">0.8485</td>
                <td className="p-3">0.8233</td>
                <td className="p-3">0.8485</td>
                <td className="p-3"><span className="text-amber-400 font-bold">COMPARABLE</span></td>
              </tr>
              <tr className="hover:bg-slate-800/40">
                <td className="p-3 font-bold text-white">CARDIO (CVD)</td>
                <td className="p-3 text-red-400">XGBoost</td>
                <td className="p-3">0.7876</td>
                <td className="p-3">0.8060</td>
                <td className="p-3">0.7876</td>
                <td className="p-3">0.8060</td>
                <td className="p-3"><span className="text-amber-400 font-bold">COMPARABLE</span></td>
              </tr>
              <tr className="hover:bg-slate-800/40">
                <td className="p-3 font-bold text-white">CKD (KIDNEY)</td>
                <td className="p-3 text-purple-400">RandomForest</td>
                <td className="p-3 font-bold text-teal-400">0.9953</td>
                <td className="p-3 font-bold text-teal-400">1.0000</td>
                <td className="p-3">0.9824</td>
                <td className="p-3">0.7568</td>
                <td className="p-3"><span className="text-teal-400 font-bold">INDEPENDENT WINNER</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400">Loading model evaluation metrics...</div>
      ) : evalData && (
        <div className="space-y-8">
          
          {/* Performance Metric Cards */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="glass-card rounded-xl p-5 border border-slate-800">
              <span className="text-xs font-semibold text-slate-400 uppercase">Test ROC-AUC</span>
              <div className="text-2xl font-extrabold text-sky-400 mt-1">{evalData.roc_auc}</div>
              <span className="text-[10px] text-slate-500">PR-AUC: {evalData.pr_auc || 'N/A'}</span>
            </div>

            <div className="glass-card rounded-xl p-5 border border-slate-800">
              <span className="text-xs font-semibold text-slate-400 uppercase">Test Recall (Sensitivity)</span>
              <div className="text-2xl font-extrabold text-teal-400 mt-1">{evalData.recall}</div>
              <span className="text-[10px] text-slate-500">Medical safety target &gt;0.75</span>
            </div>

            <div className="glass-card rounded-xl p-5 border border-slate-800">
              <span className="text-xs font-semibold text-slate-400 uppercase">Precision & F1</span>
              <div className="text-2xl font-extrabold text-white mt-1">{evalData.f1_score}</div>
              <span className="text-[10px] text-slate-500">Precision: {evalData.precision}</span>
            </div>

            <div className="glass-card rounded-xl p-5 border border-slate-800">
              <span className="text-xs font-semibold text-slate-400 uppercase">Calibrated Brier Score</span>
              <div className="text-2xl font-extrabold text-purple-400 mt-1">{evalData.brier_score}</div>
              <span className="text-[10px] text-slate-500">Lower score = better calibration</span>
            </div>
          </div>

          {/* Confusion Matrix & Calibration Curve Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* Confusion Matrix Card */}
            {evalData.confusion_matrix && (
              <div className="glass-card rounded-2xl p-6 border border-slate-800">
                <h3 className="text-base font-bold text-white mb-4">Confusion Matrix (Test Split)</h3>
                
                <div className="grid grid-cols-2 gap-3 text-center">
                  <div className="p-4 rounded-xl bg-teal-500/10 border border-teal-500/30">
                    <span className="text-[10px] uppercase font-bold text-teal-400">True Positives (TP)</span>
                    <div className="text-2xl font-extrabold text-teal-300 mt-1">{evalData.confusion_matrix.tp}</div>
                  </div>

                  <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30">
                    <span className="text-[10px] uppercase font-bold text-amber-400">False Positives (FP)</span>
                    <div className="text-2xl font-extrabold text-amber-300 mt-1">{evalData.confusion_matrix.fp}</div>
                  </div>

                  <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30">
                    <span className="text-[10px] uppercase font-bold text-red-400">False Negatives (FN)</span>
                    <div className="text-2xl font-extrabold text-red-300 mt-1">{evalData.confusion_matrix.fn}</div>
                  </div>

                  <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
                    <span className="text-[10px] uppercase font-bold text-slate-400">True Negatives (TN)</span>
                    <div className="text-2xl font-extrabold text-white mt-1">{evalData.confusion_matrix.tn}</div>
                  </div>
                </div>
              </div>
            )}

            {/* Calibration Reliability Points */}
            {evalData.calibration_details && (
              <div className="glass-card rounded-2xl p-6 border border-slate-800">
                <h3 className="text-base font-bold text-white mb-4">Probability Calibration Curve Points</h3>
                
                <div className="space-y-2 max-h-48 overflow-y-auto font-mono text-xs text-slate-300">
                  <div className="grid grid-cols-2 border-b border-slate-800 pb-1 text-slate-400 font-bold">
                    <span>Predicted Probability</span>
                    <span>Observed Frequency</span>
                  </div>
                  {evalData.calibration_details.predicted_probabilities.map((pred, i) => (
                    <div key={i} className="grid grid-cols-2">
                      <span className="text-sky-400">{pred}</span>
                      <span className="text-teal-400">{evalData.calibration_details.observed_frequencies[i]}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

          </div>

        </div>
      )}

    </div>
  );
}
