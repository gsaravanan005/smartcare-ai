import React, { useState, useEffect, useRef } from 'react';
import Logo from '../components/Logo';
import { chatAPI } from '../services/api';
import HolographicHUDPanel from '../components/HolographicHUDPanel';
import { 
  MessageSquare, Send, Sparkles, Bot, User, RefreshCw, 
  ShieldCheck, AlertTriangle, ChevronRight, HelpCircle, Activity, Lightbulb
} from 'lucide-react';

export default function WellnessChat({ user }) {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  const SUGGESTED_PROMPTS = [
    "What are my current risk scores?",
    "Why is my CVD risk high?",
    "What are my top risk factors?",
    "What should I focus on?",
    "Show my wellness recommendations."
  ];

  const fetchHistory = async () => {
    setInitialLoading(true);
    try {
      const res = await chatAPI.getHistory();
      setMessages(res.data || []);
    } catch (e) {
      console.error("Failed to load chat history:", e);
    } fontLoading: false;
    setInitialLoading(false);
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSendMessage = async (textToSend) => {
    const text = textToSend || inputText;
    if (!text || !text.trim() || loading) return;

    const userMessageText = text.trim();
    setInputText('');
    setError(null);
    setLoading(true);

    // Optimistic UI update
    const tempUserMsg = {
      id: Date.now(),
      role: 'user',
      message: userMessageText,
      created_at: new Date().toISOString()
    };
    setMessages((prev) => [...prev, tempUserMsg]);

    try {
      const res = await chatAPI.sendMessage(userMessageText);
      const turn = res.data;
      
      // Update with server responses
      setMessages((prev) => [
        ...prev.filter(m => m.id !== tempUserMsg.id),
        turn.user_message,
        turn.assistant_message
      ]);
    } catch (err) {
      console.error("Chat send error:", err);
      setError("Failed to reach Wellness Assistant. Please check server connection.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-5xl mx-auto space-y-4 font-sans pb-16">
      
      {/* 1. HEADER BANNER WITH SMARTCARE AI LOGO */}
      <div className="bg-[#0D0718] border border-[#2A1A4E] rounded-3xl p-6 shadow-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4 select-none">
        <div className="space-y-2">
          <div className="flex items-center space-x-2 text-xs font-mono text-[#C084FC] font-bold">
            <Sparkles className="w-4 h-4 text-[#C084FC]" />
            <span className="uppercase tracking-widest bg-[#120A24] px-2.5 py-0.5 rounded border border-[#7C3AED]/40">
              MODULE 6 — AI WELLNESS ASSISTANT
            </span>
          </div>

          <div className="flex items-center space-x-3">
            <Logo variant="icon" size="md" />
            <h1 className="text-xl md:text-2xl font-extrabold text-white tracking-tight">
              SmartCare AI Conversational Assistant
            </h1>
          </div>

          <p className="text-xs text-slate-300">
            Ask questions about your estimated risk probabilities, SHAP factors, wellness recommendations, and longitudinal trends.
          </p>
        </div>

        <button
          onClick={fetchHistory}
          className="px-3.5 py-2 rounded-xl bg-[#120A24] hover:bg-[#1C1633] border border-[#2A1A4E] text-slate-300 hover:text-white text-xs font-mono font-bold flex items-center space-x-1.5 transition cursor-pointer"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${initialLoading ? 'animate-spin' : ''}`} />
          <span>Reload History</span>
        </button>
      </div>

      {/* 2. CLINICAL SAFETY DISCLAIMER BANNER */}
      <div className="bg-amber-950/20 border border-amber-800/40 rounded-2xl p-3.5 flex items-start space-x-3 text-xs text-amber-200 font-sans">
        <ShieldCheck className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
        <div className="leading-relaxed">
          <span className="font-bold text-amber-300">Clinical Safety Notice: </span>
          SmartCare AI provides AI-based health risk intelligence and wellness decision support based on your clinical telemetry. 
          It does <strong>not</strong> provide medical diagnoses, prescribe medications, or replace professional clinical evaluation. 
          Always consult a qualified physician for clinical care.
        </div>
      </div>

      {/* 3. MAIN CHAT CONTAINER */}
      <div className="bg-[#0D0718]/95 border border-[#2A1A4E] rounded-3xl p-4 md:p-6 shadow-2xl flex flex-col min-h-[500px] max-h-[700px]">
        
        {/* MESSAGES AREA */}
        <div className="flex-1 overflow-y-auto space-y-4 pr-2 custom-scrollbar">
          {initialLoading ? (
            <div className="h-64 flex flex-col items-center justify-center space-y-3 font-mono text-xs text-[#C084FC]">
              <div className="w-8 h-8 rounded-full border-2 border-[#7C3AED] border-t-transparent animate-spin" />
              <div>LOADING CONVERSATION HISTORY...</div>
            </div>
          ) : messages.length === 0 ? (
            <div className="h-64 flex flex-col items-center justify-center space-y-3 text-center p-6 font-sans">
              <Logo variant="icon" size="lg" />
              <div className="font-bold text-white text-sm">Welcome to SmartCare AI Wellness Assistant</div>
              <p className="text-xs text-slate-400 max-w-md">
                I am connected to your authenticated SmartCare AI records. Ask me anything about your current risk summary, SHAP feature attributions, or wellness recommendations.
              </p>
            </div>
          ) : (
            messages.map((m, idx) => {
              const isUser = m.role === 'user';

              return (
                <div 
                  key={m.id || idx} 
                  className={`flex items-start space-x-3 ${isUser ? 'justify-end' : 'justify-start'}`}
                >
                  {!isUser && (
                    <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-[#6D28D9] to-[#C084FC] p-0.5 shadow-md flex-shrink-0 mt-0.5">
                      <div className="w-full h-full bg-[#080512] rounded-[10px] flex items-center justify-center">
                        <Logo variant="icon" size="sm" />
                      </div>
                    </div>
                  )}

                  <div className={`max-w-[80%] rounded-2xl p-4 text-xs font-sans shadow-lg ${
                    isUser
                      ? 'bg-gradient-to-r from-[#6D28D9] to-[#7C3AED] text-white rounded-tr-none'
                      : 'bg-[#120A24] border border-[#2A1A4E] text-slate-100 rounded-tl-none space-y-2'
                  }`}>
                    {/* Assistant Intent Tag */}
                    {!isUser && m.intent && (
                      <div className="flex items-center space-x-2 font-mono text-[9px] font-bold uppercase tracking-wider text-[#C084FC] border-b border-[#2A1A4E] pb-1.5 mb-1.5">
                        <Lightbulb className="w-3 h-3 text-[#C084FC]" />
                        <span>INTENT: {m.intent.replace('_', ' ')}</span>
                      </div>
                    )}

                    <div className="whitespace-pre-wrap leading-relaxed">
                      {m.message}
                    </div>

                    <div className={`text-[9px] font-mono text-right mt-1.5 ${isUser ? 'text-purple-200' : 'text-slate-400'}`}>
                      {m.created_at ? new Date(m.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : 'Just now'}
                    </div>
                  </div>

                  {isUser && (
                    <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-[#7C3AED] to-[#E879F9] text-white font-extrabold text-xs flex items-center justify-center flex-shrink-0 mt-0.5 shadow-md font-mono">
                      {user?.full_name ? user.full_name.charAt(0) : 'U'}
                    </div>
                  )}
                </div>
              );
            })
          )}

          {loading && (
            <div className="flex items-start space-x-3 justify-start">
              <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-[#6D28D9] to-[#C084FC] p-0.5 shadow-md flex-shrink-0 animate-pulse">
                <div className="w-full h-full bg-[#080612] rounded-[10px] flex items-center justify-center">
                  <Logo variant="icon" size="sm" />
                </div>
              </div>
              <div className="bg-[#120A24] border border-[#2A1A4E] rounded-2xl rounded-tl-none p-3.5 text-xs text-[#C084FC] font-mono flex items-center space-x-2">
                <div className="w-2 h-2 rounded-full bg-[#7C3AED] animate-ping" />
                <span>ANALYZING SMARTCARE AI TELEMETRY & GENERATING RESPONSE...</span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* 4. SUGGESTED PROMPTS CHIPS */}
        <div className="py-3 border-t border-[#2A1A4E] mt-3">
          <div className="text-[10px] font-mono font-bold text-slate-400 uppercase tracking-widest mb-2 flex items-center space-x-1">
            <Lightbulb className="w-3 h-3 text-[#C084FC]" />
            <span>Suggested Questions:</span>
          </div>

          <div className="flex flex-wrap gap-1.5">
            {SUGGESTED_PROMPTS.map((prompt, pIdx) => (
              <button
                key={pIdx}
                type="button"
                onClick={() => handleSendMessage(prompt)}
                className="px-2.5 py-1 rounded-xl bg-[#120A24] hover:bg-[#1C1633] border border-[#2A1A4E] hover:border-[#7C3AED] text-slate-300 hover:text-white text-[11px] font-sans transition cursor-pointer"
              >
                {prompt}
              </button>
            ))}
          </div>
        </div>

        {/* 5. INPUT FORM */}
        <form 
          onSubmit={(e) => { e.preventDefault(); handleSendMessage(); }}
          className="relative mt-2"
        >
          {error && (
            <div className="text-[11px] font-mono text-rose-400 mb-2 bg-rose-950/40 p-2 rounded-xl border border-rose-800 flex items-center justify-between">
              <span>{error}</span>
              <button type="button" onClick={() => setError(null)} className="text-xs font-bold px-1 font-mono">✕</button>
            </div>
          )}

          <div className="relative flex items-center">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Ask about your risk scores, SHAP factors, wellness plan, or history..."
              className="w-full bg-[#120A24] border border-[#2A1A4E] rounded-2xl pl-4 pr-12 py-3 text-xs text-white placeholder-slate-500 focus:border-[#7C3AED] outline-none transition font-sans"
            />

            <button
              type="submit"
              disabled={loading || !inputText.trim()}
              className="absolute right-2 p-2 rounded-xl bg-gradient-to-r from-[#6D28D9] to-[#7C3AED] hover:brightness-110 disabled:opacity-40 text-white transition cursor-pointer shadow-md"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </form>

      </div>

    </div>
  );
}
