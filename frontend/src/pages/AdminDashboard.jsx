import React, { useState, useEffect } from 'react';
import { datasetAPI, pipelineAPI } from '../services/api';
import { Database, AlertTriangle, Layers, Activity, Play, RefreshCw, BarChart2, CheckCircle2, Shield } from 'lucide-react';

export default function AdminDashboard() {
  const [selectedDataset, setSelectedDataset] = useState('diabetes');
  const [profile, setProfile] = useState(null);
  const [missingness, setMissingness] = useState(null);
  const [vifData, setVifData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [runningPipeline, setRunningPipeline] = useState(false);
  const [pipelineMessage, setPipelineMessage] = useState(null);

  // Experiment Config Modal State
  const [config, setConfig] = useState({
    imputation_method: 'median',
    outlier_strategy: 'iqr_capping',
    encoding_strategy: 'onehot',
    scaling_strategy: 'standard',
    feature_selection_method: 'select_k_best',
    k_features: 15,
    class_imbalance_method: 'smote',
    missingness_injection_scenario: '',
    missingness_injection_rate: 0.0,
    random_seed: 42
  });

  const loadDatasetData = async (name) => {
    setLoading(true);
    setPipelineMessage(null);
    try {
      const [profRes, missRes, vifRes] = await Promise.all([
        datasetAPI.getProfile(name),
        datasetAPI.getMissingness(name),
        datasetAPI.getVif(name)
      ]);
      setProfile(profRes.data);
      setMissingness(missRes.data);
      setVifData(vifRes.data);
    } catch (err) {
      console.error("Failed to load dataset details:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDatasetData(selectedDataset);
  }, [selectedDataset]);

  const handleRunPipeline = async () => {
    setRunningPipeline(true);
    setPipelineMessage(null);
    try {
      const res = await pipelineAPI.run({
        ...config,
        dataset_name: selectedDataset,
        missingness_injection_scenario: config.missingness_injection_scenario || null
      });
      setPipelineMessage({
        type: 'success',
        text: `Pipeline execution complete! Version: ${res.data[0].pipeline_version}`
      });
      loadDatasetData(selectedDataset);
    } catch (err) {
      setPipelineMessage({
        type: 'error',
        text: err.response?.data?.detail || "Pipeline run failed."
      });
    } finally {
      setRunningPipeline(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
      
      {/* Header & Dataset Selector */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center space-x-2 text-xs font-bold uppercase tracking-widest text-teal-400 mb-1">
            <Shield className="w-4 h-4" />
            <span>Authorized Research & Data-Quality Hub</span>
          </div>
          <h1 className="text-2xl font-extrabold text-white">SmartCare AI Data Quality & Profiling Dashboard</h1>
        </div>

        {/* Dataset Buttons */}
        <div className="flex items-center space-x-2 bg-slate-900 p-1.5 rounded-xl border border-slate-800">
          {[
            { id: 'diabetes', label: 'Diabetes BRFSS' },
            { id: 'cardio', label: 'CVD Cardiovascular' },
            { id: 'ckd', label: 'CKD Kidney Disease' }
          ].map(d => (
            <button
              key={d.id}
              onClick={() => setSelectedDataset(d.id)}
              className={`px-4 py-2 rounded-lg text-xs font-bold transition ${
                selectedDataset === d.id
                  ? 'bg-sky-500 text-slate-950 shadow-md shadow-sky-500/20'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              {d.label}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400 font-medium">Loading statistical dataset profiles...</div>
      ) : profile && (
        <>
          {/* Summary Metric Cards */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="glass-card rounded-xl p-5 border border-slate-800">
              <span className="text-xs font-semibold text-slate-400 uppercase">Dataset Rows</span>
              <div className="text-2xl font-extrabold text-white mt-1">{profile.num_rows.toLocaleString()}</div>
              <span className="text-[10px] text-slate-500">Unfiltered total records</span>
            </div>

            <div className="glass-card rounded-xl p-5 border border-slate-800">
              <span className="text-xs font-semibold text-slate-400 uppercase">Feature Count</span>
              <div className="text-2xl font-extrabold text-sky-400 mt-1">{profile.num_columns}</div>
              <span className="text-[10px] text-slate-500">Including target variable</span>
            </div>

            <div className="glass-card rounded-xl p-5 border border-slate-800">
              <span className="text-xs font-semibold text-slate-400 uppercase">Duplicates</span>
              <div className="text-2xl font-extrabold text-yellow-400 mt-1">{profile.duplicate_count} ({profile.duplicate_pct.toFixed(2)}%)</div>
              <span className="text-[10px] text-slate-500">Logged for removal</span>
            </div>

            <div className="glass-card rounded-xl p-5 border border-slate-800">
              <span className="text-xs font-semibold text-slate-400 uppercase">Positive Target %</span>
              <div className="text-2xl font-extrabold text-teal-400 mt-1">
                {profile.target_distribution.positive_percentage.toFixed(1)}%
              </div>
              <span className="text-[10px] text-slate-500">Imbalance ratio: {profile.target_distribution.imbalance_ratio.toFixed(2)}</span>
            </div>
          </div>

          {/* Missingness & Target Distribution Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* Missingness Summary */}
            <div className="glass-card rounded-2xl p-6 border border-slate-800">
              <h3 className="text-base font-bold text-white mb-4 flex items-center space-x-2">
                <AlertTriangle className="w-5 h-5 text-amber-400" />
                <span>Missingness Summary & Pattern Analysis</span>
              </h3>
              
              <div className="space-y-3 max-h-60 overflow-y-auto pr-2">
                {Object.entries(profile.missing_summary).map(([col, count]) => {
                  const pct = profile.missing_pcts[col];
                  return (
                    <div key={col} className="flex items-center justify-between text-xs">
                      <span className="font-mono text-slate-300">{col}</span>
                      <div className="flex items-center space-x-3">
                        <div className="w-32 bg-slate-800 h-2 rounded-full overflow-hidden">
                          <div className="bg-amber-400 h-full" style={{ width: `${Math.min(100, pct)}%` }} />
                        </div>
                        <span className="w-16 text-right text-slate-400">{count} ({pct.toFixed(1)}%)</span>
                      </div>
                    </div>
                  );
                })}
              </div>

              {missingness?.pattern_notes && (
                <div className="mt-4 p-3 rounded-lg bg-slate-900 border border-slate-800 text-xs text-slate-400 space-y-1">
                  {missingness.pattern_notes.map((note, idx) => (
                    <div key={idx}>• {note}</div>
                  ))}
                </div>
              )}
            </div>

            {/* Target Distribution Card */}
            <div className="glass-card rounded-2xl p-6 border border-slate-800">
              <h3 className="text-base font-bold text-white mb-4 flex items-center space-x-2">
                <BarChart2 className="w-5 h-5 text-sky-400" />
                <span>Target Distribution ({profile.target_column})</span>
              </h3>

              <div className="space-y-4">
                <div className="flex justify-between text-xs text-slate-300">
                  <span>Class 0 (Negative): <strong className="text-white">{profile.target_distribution.negative_count}</strong> ({profile.target_distribution.negative_percentage.toFixed(1)}%)</span>
                  <span>Class 1 (Positive): <strong className="text-sky-400">{profile.target_distribution.positive_count}</strong> ({profile.target_distribution.positive_percentage.toFixed(1)}%)</span>
                </div>

                <div className="h-6 w-full bg-slate-800 rounded-xl overflow-hidden flex">
                  <div 
                    className="bg-slate-600 h-full flex items-center justify-center text-[10px] font-bold text-white" 
                    style={{ width: `${profile.target_distribution.negative_percentage}%` }}
                  >
                    Negative
                  </div>
                  <div 
                    className="bg-gradient-to-r from-sky-500 to-teal-400 h-full flex items-center justify-center text-[10px] font-extrabold text-slate-950" 
                    style={{ width: `${profile.target_distribution.positive_percentage}%` }}
                  >
                    Positive
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-300 space-y-2">
                  <div className="font-semibold text-sky-400">Class Imbalance Strategy Recommendation:</div>
                  <p>
                    {profile.target_distribution.imbalance_ratio > 2.0
                      ? 'High imbalance detected. SMOTE or class-weight adjustment inside training folds is recommended.'
                      : 'Balanced dataset distribution. Standard cross-validation stratification is sufficient.'}
                  </p>
                </div>
              </div>
            </div>

          </div>

          {/* Multicollinearity VIF Table & Experiment Controls */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            {/* VIF Table */}
            <div className="md:col-span-2 glass-card rounded-2xl p-6 border border-slate-800">
              <h3 className="text-base font-bold text-white mb-4 flex items-center space-x-2">
                <Layers className="w-5 h-5 text-purple-400" />
                <span>Multicollinearity Analysis (Variance Inflation Factor - VIF)</span>
              </h3>

              <div className="overflow-x-auto max-h-72 border border-slate-800 rounded-xl">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-900 text-slate-400 uppercase font-semibold sticky top-0">
                    <tr>
                      <th className="p-3">Feature Name</th>
                      <th className="p-3">VIF Score</th>
                      <th className="p-3">Multicollinearity Risk</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800 font-mono text-slate-300">
                    {vifData?.vif_summary && Object.entries(vifData.vif_summary).map(([feat, score]) => (
                      <tr key={feat} className="hover:bg-slate-800/40">
                        <td className="p-3 font-semibold text-white">{feat}</td>
                        <td className="p-3">{score}</td>
                        <td className="p-3">
                          {score > 10.0 ? (
                            <span className="text-red-400 font-bold">High Collinearity (&gt;10)</span>
                          ) : score > 5.0 ? (
                            <span className="text-amber-400">Moderate (5-10)</span>
                          ) : (
                            <span className="text-teal-400">Low (&lt;5)</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Experiment Runner Controls */}
            <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
              <h3 className="text-base font-bold text-white flex items-center space-x-2">
                <Play className="w-5 h-5 text-teal-400" />
                <span>Pipeline Experiment Runner</span>
              </h3>

              <div className="space-y-3 text-xs">
                <div>
                  <label className="block text-slate-400 mb-1">Imputation Strategy</label>
                  <select
                    value={config.imputation_method}
                    onChange={(e) => setConfig({ ...config, imputation_method: e.target.value })}
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-white"
                  >
                    <option value="median">Median</option>
                    <option value="mean">Mean</option>
                    <option value="knn">KNN Imputer</option>
                    <option value="iterative">Iterative (MICE)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-slate-400 mb-1">Outlier Treatment</label>
                  <select
                    value={config.outlier_strategy}
                    onChange={(e) => setConfig({ ...config, outlier_strategy: e.target.value })}
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-white"
                  >
                    <option value="iqr_capping">IQR Capping</option>
                    <option value="zscore_capping">Z-Score Capping</option>
                    <option value="removal">Removal</option>
                  </select>
                </div>

                <div>
                  <label className="block text-slate-400 mb-1">Imbalance Handling</label>
                  <select
                    value={config.class_imbalance_method}
                    onChange={(e) => setConfig({ ...config, class_imbalance_method: e.target.value })}
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-white"
                  >
                    <option value="smote">SMOTE</option>
                    <option value="oversampling">Random Oversampling</option>
                    <option value="undersampling">Random Undersampling</option>
                    <option value="class_weights">Class Weights</option>
                  </select>
                </div>
              </div>

              {pipelineMessage && (
                <div className={`p-3 rounded-lg text-xs font-semibold ${
                  pipelineMessage.type === 'success' ? 'bg-teal-500/10 text-teal-300 border border-teal-500/30' : 'bg-red-500/10 text-red-300 border border-red-500/30'
                }`}>
                  {pipelineMessage.text}
                </div>
              )}

              <button
                onClick={handleRunPipeline}
                disabled={runningPipeline}
                className="w-full py-3 rounded-xl bg-gradient-to-r from-sky-500 to-teal-400 text-slate-950 font-extrabold text-xs tracking-wider uppercase transition hover:opacity-90 shadow-lg shadow-sky-500/20"
              >
                {runningPipeline ? 'Executing Leakage-Free Pipeline...' : 'Run Preprocessing Pipeline'}
              </button>
            </div>

          </div>
        </>
      )}

    </div>
  );
}
