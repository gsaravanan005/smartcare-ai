import React, { useState, useEffect, useRef } from 'react';
import Logo from './Logo';
import { chatAPI } from '../services/api';
import { MessageSquare, X, Send, Bot, Sparkles, RefreshCw, ShieldCheck } from 'lucide-react';

export default function WellnessChatbotWidget({ user, onNavigate }) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const fetchHistory = async () => {
    try {
      const res = await chatAPI.getHistory();
      setMessages(res.data || []);
    } catch (e) {
      console.error("Widget history load error:", e);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchHistory();
    }
  }, [isOpen]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSend = async (textToSend) => {
    const text = textToSend || inputText;
    if (!text || !text.trim() || loading) return;

    const userMessageText = text.trim();
    setInputText('');
    setLoading(true);

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
      setMessages((prev) => [
        ...prev.filter(m => m.id !== tempUserMsg.id),
        turn.user_message,
        turn.assistant_message
      ]);
    } catch (err) {
      console.error("Widget send error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed bottom-20 right-6 z-50 select-none">
      
      {/* FLOATING TOGGLE BUTTON */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="p-3.5 rounded-2xl bg-gradient-to-r from-[#6D28D9] via-[#7C3AED] to-[#A855F7] hover:brightness-110 text-white shadow-2xl shadow-[#7C3AED]/50 border border-[#8B5CF6]/40 flex items-center space-x-2 transition cursor-pointer group scale-100 hover:scale-105"
        >
          <div className="relative flex items-center justify-center">
            <Logo variant="icon" size="avatar" className="w-6 h-6" />
            <span className="absolute -top-1 -right-1 w-2 h-2 bg-[#E879F9] rounded-full animate-ping" />
          </div>
          <span className="font-mono text-xs font-bold uppercase tracking-wider hidden sm:inline">Ask Wellness AI</span>
        </button>
      )}

      {/* POPUP CHAT WINDOW */}
      {isOpen && (
        <div className="w-[360px] sm:w-[400px] h-[520px] bg-[#0D0718]/95 backdrop-blur-2xl border border-[#7C3AED]/60 rounded-3xl shadow-2xl flex flex-col overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-200">
          
          {/* WINDOW HEADER WITH LOGO */}
          <div className="p-3.5 bg-[#120A24] border-b border-[#2A1A4E] flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Logo variant="icon" size="sm" />
              <div>
                <div className="text-xs font-extrabold text-white font-mono flex items-center space-x-1">
                  <span>WELLNESS AI</span>
                  <Sparkles className="w-3 h-3 text-[#C084FC]" />
                </div>
                <div className="text-[9px] text-purple-300/80 font-mono">Patient Health Telemetry Assistant</div>
              </div>
            </div>

            <div className="flex items-center space-x-1">
              <button
                onClick={() => { setIsOpen(false); if (onNavigate) onNavigate('wellness_chat'); }}
                className="text-[10px] font-mono text-[#C084FC] hover:text-white px-2 py-1 rounded bg-[#080512] border border-[#2A1A4E]"
              >
                Expand
              </button>
              <button
                onClick={() => setIsOpen(false)}
                className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-[#120A24] transition"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* MESSAGES BODY */}
          <div className="flex-1 p-3 overflow-y-auto space-y-3 font-sans text-xs custom-scrollbar">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-4 space-y-2 text-slate-400 font-mono text-[11px]">
                <Logo variant="icon" size="md" />
                <div className="text-white font-bold">Connected to SmartCare AI telemetry.</div>
                <div className="text-[10px] text-purple-300/80">Ask "What are my current risks?" to start.</div>
              </div>
            ) : (
              messages.map((m, idx) => {
                const isUser = m.role === 'user';
                return (
                  <div key={m.id || idx} className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[85%] p-3 rounded-2xl text-[11px] leading-relaxed shadow-md whitespace-pre-wrap ${
                      isUser
                        ? 'bg-[#7C3AED] text-white rounded-tr-none'
                        : 'bg-[#120A24] border border-[#2A1A4E] text-slate-200 rounded-tl-none'
                    }`}>
                      {m.message}
                    </div>
                  </div>
                );
              })
            )}

            {loading && (
              <div className="text-[10px] font-mono text-[#C084FC] animate-pulse bg-[#120A24] p-2 rounded-xl border border-[#2A1A4E]">
                Analyzing telemetry & preparing advice...
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* INPUT FORM */}
          <form 
            onSubmit={(e) => { e.preventDefault(); handleSend(); }}
            className="p-3 bg-[#080512] border-t border-[#2A1A4E] flex items-center space-x-2"
          >
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Ask Wellness AI..."
              className="flex-1 bg-[#120A24] border border-[#2A1A4E] rounded-xl px-3 py-2 text-xs text-white placeholder-slate-500 outline-none focus:border-[#7C3AED]"
            />
            <button
              type="submit"
              disabled={loading || !inputText.trim()}
              className="p-2 rounded-xl bg-[#7C3AED] hover:bg-[#8B5CF6] text-white disabled:opacity-40"
            >
              <Send className="w-3.5 h-3.5" />
            </button>
          </form>

        </div>
      )}

    </div>
  );
}
