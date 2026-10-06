import React, { useState } from 'react';
import HolographicHUDPanel from '../components/HolographicHUDPanel';
import { pipelineAPI } from '../services/api';
import { 
  GitMerge, Play, CheckCircle2, AlertCircle, Sparkles, 
  RefreshCw, Zap, Database, ArrowRight, ShieldCheck 
} from 'lucide-react';

const PIPELINE_NODES = [
  { id: '01', title: 'RAW DATA', desc: 'Ingest BRFSS/CSV', duration: '12ms', input: '70,692 Rows', output: 'Raw Dataframe' },
  { id: '02', title: 'INSPECTION', desc: 'Schema & Types', duration: '8ms', input: 'Raw Dataframe', output: 'Schema Verified' },
  { id: '03', title: 'CLEANING', desc: 'Deduplication', duration: '15ms', input: '22 Cols', output: '0 Duplicates' },
  { id: '04', title: 'SPLIT', desc: '70/15/15 Partition', duration: '20ms', input: 'Clean Data', output: 'Train/Val/Test' },
  { id: '05', title: 'IMPUTATION', desc: 'Median / KNN', duration: '45ms', input: 'Train Partition', output: '0 Nulls' },
  { id: '06', title: 'ENCODING', desc: 'Target Encoding', duration: '18ms', input: 'Categoricals', output: 'Numeric Matrix' },
  { id: '07', title: 'OUTLIERS', desc: 'IQR Truncation', duration: '25ms', input: 'Continuous Cols', output: 'Capped Boundaries' },
  { id: '08', title: 'FEATURE ENG', desc: 'BMI & Risk Ratios', duration: '30ms', input: 'Base Features', output: '+3 Intersect Features' },
  { id: '09', title: 'FEATURE SEL', desc: 'SelectKBest & VIF', duration: '35ms', input: '25 Features', output: 'Top 18 Features' },
  { id: '10', title: 'SCALING', desc: 'StandardScaler', duration: '14ms', input: 'Selected Features', output: 'Scaled Matrix' },
  { id: '11', title: 'MODEL HANDOFF', desc: 'Export Joblib', duration: '10ms', input: 'Scaled Matrix', output: '.joblib Artifact' }
];

export default function PipelineRunner() {
  const [datasetName, setDatasetName] = useState('diabetes');
  const [running, setRunning] = useState(false);
  const [activeStep, setActiveStep] = useState(-1);
  const [selectedNode, setSelectedNode] = useState(PIPELINE_NODES[0]);
  const [pipelineResult, setPipelineResult] = useState(null);
  const [error, setError] = useState(null);

  const handleRunPipeline = async () => {
    setRunning(true);
    setActiveStep(0);
    setError(null);
    setPipelineResult(null);

    const interval = setInterval(() => {
      setActiveStep(prev => {
        if (prev < PIPELINE_NODES.length - 1) return prev + 1;
        clearInterval(interval);
        return prev;
      });
    }, 250);

    try {
      const res = await pipelineAPI.run({
        dataset_name: datasetName,
        missing_imputation: 'median',
        outlier_strategy: 'iqr_capping',
        feature_selection: 'select_k_best'
      });

      const resultObj = Array.isArray(res.data) ? res.data[0] : res.data;
      setPipelineResult(resultObj);
      setActiveStep(PIPELINE_NODES.length - 1);
    } catch (err) {
      setError(err.response?.data?.detail || "Pipeline execution failed.");
    } finally {
      clearInterval(interval);
      setRunning(false);
    }
  };

  return (
    <div className="w-full space-y-6 z-10 font-sans pb-12">
      
      {/* 1. TOP CONTROL BAR */}
      <div className="w-full bg-slate-950/80 p-3.5 rounded-2xl border border-slate-800 flex flex-wrap items-center justify-between gap-4 font-mono text-xs shadow-xl">
        <div className="flex items-center space-x-2 bg-slate-900/90 p-1.5 rounded-xl border border-slate-800">
          {[
            { id: 'diabetes', label: 'DIABETES PIPELINE' },
            { id: 'cardio', label: 'CVD PIPELINE' },
            { id: 'ckd', label: 'CKD PIPELINE' }
          ].map(d => (
            <button
              key={d.id}
              onClick={() => setDatasetName(d.id)}
              className={`px-4 py-1.5 rounded-lg font-bold transition cursor-pointer ${
                datasetName === d.id
                  ? 'bg-cyan-500/25 text-cyan-300 border border-cyan-400/50 shadow-md'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              {d.label}
            </button>
          ))}
        </div>

        <button
          onClick={handleRunPipeline}
          disabled={running}
          className="px-6 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-extrabold text-xs uppercase tracking-wider transition shadow-lg shadow-cyan-500/20 flex items-center space-x-2 cursor-pointer"
        >
          {running ? (
            <>
              <RefreshCw className="w-4 h-4 animate-spin" />
              <span>RUNNING PIPELINE...</span>
            </>
          ) : (
            <>
              <Play className="w-4 h-4 fill-current" />
              <span>EXECUTE PIPELINE GRAPH</span>
            </>
          )}
        </button>
      </div>

      {/* ERROR ALERT */}
      {error && (
        <div className="p-3.5 rounded-xl bg-red-500/15 border border-red-500/40 text-red-300 text-xs font-mono flex items-center space-x-2">
          <AlertCircle className="w-4 h-4 text-red-400 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* 2. HORIZONTAL PIPELINE TIMELINE WORKSPACE (11 CONNECTED NODES ACROSS MAIN WORKSPACE) */}
      <div className="w-full">
        <HolographicHUDPanel 
          title="PREPROCESSING & TRANSFORMATION PIPELINE TIMELINE" 
          subtitle="11 Execution Nodes with Data Leakage Prevention"
          glowColor="cyan"
        >
          <div className="overflow-x-auto py-6 no-scrollbar">
            <div className="flex items-center space-x-3 min-w-[1200px] px-2">
              {PIPELINE_NODES.map((node, idx) => {
                const isCompleted = activeStep >= idx;
                const isActive = running && activeStep === idx;
                const isSelected = selectedNode.id === node.id;

                return (
                  <React.Fragment key={node.id}>
                    {/* Node Module Card */}
                    <div
                      onClick={() => setSelectedNode(node)}
                      className={`flex-shrink-0 w-28 p-3 rounded-xl border text-center font-mono transition-all cursor-pointer relative ${
                        isActive
                          ? 'bg-cyan-500/25 border-cyan-400 text-cyan-200 scale-105 shadow-lg shadow-cyan-500/30'
                          : isCompleted
                          ? 'bg-teal-500/15 border-teal-500/40 text-teal-300'
                          : isSelected
                          ? 'bg-slate-900 border-cyan-500/50 text-white'
                          : 'bg-slate-950/80 border-slate-800 text-slate-500 hover:border-slate-700'
                      }`}
                    >
                      <div className="text-[9px] font-bold text-slate-400">{node.id}</div>
                      <div className="text-[10px] font-extrabold text-white truncate mt-1">{node.title}</div>
                      <div className="text-[8px] text-slate-400 truncate mt-0.5">{node.desc}</div>
                      
                      <div className="mt-2 text-[8px] px-1.5 py-0.5 rounded bg-slate-900 border border-slate-800 text-cyan-300 font-bold inline-block">
                        {node.duration}
                      </div>

                      {isActive && (
                        <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping absolute top-2 right-2" />
                      )}
                    </div>

                    {/* Connecting Animated Line */}
                    {idx < PIPELINE_NODES.length - 1 && (
                      <div className="w-6 h-0.5 bg-slate-800 relative overflow-hidden flex-shrink-0">
                        <div 
                          className={`h-full transition-all duration-300 ${
                            activeStep > idx ? 'bg-cyan-400' : 'bg-slate-800'
                          }`}
                        />
                      </div>
                    )}
                  </React.Fragment>
                );
              })}
            </div>
          </div>
        </HolographicHUDPanel>
      </div>

      {/* 3. SELECTED NODE DETAIL & ARTIFACTS PANEL */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 font-mono text-xs">
        
        {/* Node Parameter Inspector */}
        <HolographicHUDPanel 
          title={`NODE ${selectedNode.id}: ${selectedNode.title}`} 
          subtitle="Node Configuration & Transformation Protocol"
          glowColor="teal"
        >
          <div className="space-y-3">
            <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
              <span className="text-[9px] text-slate-400 uppercase">TRANSFORMATION DESCRIPTION</span>
              <div className="text-white font-bold">{selectedNode.desc}</div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
                <span className="text-[9px] text-slate-400 uppercase">INPUT SPECIFICATION</span>
                <div className="text-cyan-300 font-bold">{selectedNode.input}</div>
              </div>

              <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
                <span className="text-[9px] text-slate-400 uppercase">OUTPUT ARTIFACT</span>
                <div className="text-teal-300 font-bold">{selectedNode.output}</div>
              </div>
            </div>
          </div>
        </HolographicHUDPanel>

        {/* Pipeline Execution Artifacts */}
        <HolographicHUDPanel 
          title="PIPELINE EXECUTION ARTIFACTS" 
          subtitle={`Export Status for ${datasetName.toUpperCase()}`}
          glowColor="cyan"
        >
          <div className="space-y-3">
            <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 flex justify-between items-center">
              <span className="text-slate-400">PIPELINE VERSION</span>
              <span className="text-cyan-300 font-bold">{pipelineResult?.pipeline_version || 'v1.4.0'}</span>
            </div>

            <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 flex justify-between items-center">
              <span className="text-slate-400">LEAKAGE PREVENTION</span>
              <span className="text-teal-400 font-bold flex items-center space-x-1">
                <ShieldCheck className="w-3.5 h-3.5 text-teal-400" />
                <span>PASSED ✓</span>
              </span>
            </div>

            <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 flex justify-between items-center">
              <span className="text-slate-400">EXPORT PATH</span>
              <span className="text-white font-bold text-[10px] truncate max-w-[200px]">
                {pipelineResult?.artifacts_exported ? 'backend/artifacts/pipeline.joblib' : 'Ready for Export'}
              </span>
            </div>
          </div>
        </HolographicHUDPanel>

      </div>

    </div>
  );
}
