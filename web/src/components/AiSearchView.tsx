'use client';

import React, { useState } from 'react';
import { Search, Sparkles, Send, Bot, CheckCircle2 } from 'lucide-react';
import { queryAiSearch } from '@/lib/api';

export const AiSearchView: React.FC = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<{
    answer: string;
    matchedProjects: any[];
    matchedPrototypes: any[];
  } | null>(null);

  const EXECUTIVE_QUESTIONS = [
    "Which research project is currently behind schedule?",
    "What solar irrigation machinery prototypes are being tested?",
    "Summarize commercial deployment progress of the grain sheller"
  ];

  const handleSearch = async (queryText: string) => {
    if (!queryText.trim()) return;
    setLoading(true);
    setQuery(queryText);

    try {
      const res = await queryAiSearch(queryText);
      setResponse(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-3xl mx-auto animate-fadeIn">
      <div className="text-center space-y-2 py-2">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold border border-emerald-300">
          <Sparkles className="w-3.5 h-3.5 text-emerald-700" /> Groq AI Intelligent Search Engine
        </div>
        <h2 className="text-xl font-black text-slate-900 tracking-tight">
          Executive Natural Language Assistant
        </h2>
        <p className="text-xs text-slate-500 max-w-lg mx-auto">
          Ask questions about NCAM agricultural research projects, machines, budgets, or delays in plain English.
        </p>
      </div>

      {/* Query Bar */}
      <div className="ncam-card p-4 space-y-3">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSearch(query);
          }}
          className="flex items-center gap-2"
        >
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
            <input
              type="text"
              placeholder="Ask a question (e.g. Which projects are delayed?)..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-3 rounded-xl border border-slate-300 text-xs text-slate-900 bg-slate-50 focus:outline-none focus:border-emerald-600 placeholder-slate-400"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="px-5 py-3 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs shadow-sm transition-all flex items-center space-x-2 shrink-0 disabled:opacity-50"
          >
            {loading ? <span>Analyzing...</span> : <span>Ask AI</span>}
          </button>
        </form>

        <div className="flex flex-wrap items-center gap-2 pt-1 text-xs">
          <span className="text-slate-500 font-bold text-[11px]">Quick Questions:</span>
          {EXECUTIVE_QUESTIONS.map((q, idx) => (
            <button
              key={idx}
              onClick={() => handleSearch(q)}
              className="px-3 py-1 rounded-lg bg-slate-100 border border-slate-200 text-slate-700 hover:bg-emerald-50 hover:text-emerald-800 hover:border-emerald-300 text-[11px] font-medium transition-all"
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      {/* Response Box */}
      {response && (
        <div className="ncam-card p-6 border-l-4 border-l-emerald-600 space-y-4 animate-scaleUp">
          <div className="flex items-center space-x-2 border-b border-slate-200 pb-3">
            <Bot className="w-5 h-5 text-emerald-700" />
            <h3 className="text-sm font-bold text-slate-900">NCAM AI Intelligence Answer</h3>
          </div>

          <p className="text-xs text-slate-700 leading-relaxed font-medium bg-slate-50 p-4 rounded-xl border border-slate-200">
            {response.answer}
          </p>

          {response.matchedProjects.length > 0 && (
            <div className="space-y-2">
              <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">
                Related Project Record
              </span>
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs">
                <span className="font-bold text-emerald-800 block">{response.matchedProjects[0].title}</span>
                <span className="text-slate-500 text-[11px] block">Lead: {response.matchedProjects[0].lead_researcher_name}</span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
