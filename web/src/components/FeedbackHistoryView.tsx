'use client';

import React from 'react';
import { MessageSquareQuote, Star, CheckCircle2, Clock, User, Filter } from 'lucide-react';
import { PilotFeedback } from '@/lib/data';

interface FeedbackHistoryViewProps {
  feedbackList: PilotFeedback[];
}

export const FeedbackHistoryView: React.FC<FeedbackHistoryViewProps> = ({ feedbackList }) => {
  return (
    <div className="space-y-6 animate-fadeIn">
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-extrabold text-white flex items-center gap-2">
            <MessageSquareQuote className="w-6 h-6 text-emerald-400" /> Pilot Feedback & Evaluation Log
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Submitted ratings, usability reports, and feature requests from NCAM pilot testers
          </p>
        </div>

        <span className="px-3.5 py-1.5 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
          {feedbackList.length} Feedback Item(s) Submitted
        </span>
      </div>

      {feedbackList.length === 0 ? (
        <div className="glass-panel p-12 rounded-2xl border border-slate-800 text-center space-y-3">
          <div className="w-12 h-12 bg-slate-900 text-slate-500 rounded-full flex items-center justify-center mx-auto border border-slate-800">
            <MessageSquareQuote className="w-6 h-6" />
          </div>
          <h3 className="text-base font-bold text-white">No Pilot Feedback Submitted Yet</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto leading-relaxed">
            Click the floating <strong className="text-emerald-400 font-semibold">Pilot User Feedback button</strong> at the bottom right corner of any page to submit your first evaluation report.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {feedbackList.map((item) => (
            <div key={item.id} className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-800 pb-3 gap-2">
                <div className="flex items-center space-x-3">
                  <span className="px-2.5 py-1 rounded text-[10px] font-extrabold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                    {item.category}
                  </span>
                  <span className="text-xs text-slate-400">
                    Target Page: <strong className="text-white capitalize">{item.page}</strong>
                  </span>
                </div>

                <div className="flex items-center space-x-2">
                  <div className="flex items-center">
                    {[1, 2, 3, 4, 5].map((s) => (
                      <Star key={s} className={`w-3.5 h-3.5 ${s <= item.rating ? 'text-amber-400 fill-amber-400' : 'text-slate-700'}`} />
                    ))}
                  </div>
                  <span className="text-xs text-slate-500">
                    {new Date(item.timestamp).toLocaleDateString()}
                  </span>
                </div>
              </div>

              <p className="text-xs text-slate-200 leading-relaxed font-medium bg-slate-950 p-4 rounded-xl border border-slate-800">
                "{item.feedback_text}"
              </p>

              <div className="flex items-center justify-between text-[11px] text-slate-400">
                <span className="flex items-center gap-1.5">
                  <User className="w-3.5 h-3.5 text-emerald-400" />
                  Submitted by: <strong className="text-slate-200">{item.user_name}</strong> ({item.role})
                </span>
                <span className="px-2.5 py-0.5 rounded bg-emerald-950 text-emerald-400 font-bold border border-emerald-500/20">
                  Status: {item.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
