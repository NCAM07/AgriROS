'use client';

import React, { useState } from 'react';
import { MessageSquarePlus, X, Star, Send, CheckCircle2 } from 'lucide-react';
import { submitPilotFeedback } from '@/lib/api';

interface PilotFeedbackModalProps {
  currentPage: string;
  onFeedbackSubmitted?: () => void;
}

export const PilotFeedbackModal: React.FC<PilotFeedbackModalProps> = ({ currentPage, onFeedbackSubmitted }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [rating, setRating] = useState<number>(5);
  const [feedbackText, setFeedbackText] = useState('');
  const [submittedToast, setSubmittedToast] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!feedbackText.trim()) return;

    submitPilotFeedback({
      role: 'System User',
      user_name: 'NCAM Portal User',
      page: currentPage,
      rating,
      category: 'UI/Usability',
      feedback_text: feedbackText
    });

    setFeedbackText('');
    setSubmittedToast(true);
    if (onFeedbackSubmitted) onFeedbackSubmitted();

    setTimeout(() => {
      setSubmittedToast(false);
      setIsOpen(false);
    }, 1800);
  };

  return (
    <>
      {/* Floating Trigger Button */}
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 z-50 flex items-center space-x-2 px-4 py-2.5 rounded-full bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs shadow-lg border border-emerald-600 transition-all hover:scale-105"
      >
        <MessageSquarePlus className="w-4 h-4" />
        <span>System Support & Feedback</span>
      </button>

      {/* Clean White Modal */}
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4 animate-fadeIn">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl max-w-md w-full p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-200 pb-3">
              <h3 className="text-base font-bold text-slate-900">Institutional Feedback & Support</h3>
              <button onClick={() => setIsOpen(false)} className="text-slate-400 hover:text-slate-700">
                <X className="w-5 h-5" />
              </button>
            </div>

            {submittedToast ? (
              <div className="py-8 text-center space-y-2">
                <div className="w-12 h-12 bg-emerald-100 text-emerald-700 rounded-full flex items-center justify-center mx-auto border border-emerald-300">
                  <CheckCircle2 className="w-6 h-6" />
                </div>
                <h4 className="text-base font-bold text-slate-900">Feedback Received</h4>
                <p className="text-xs text-slate-500">Your message has been submitted to NCAM IT Administration.</p>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4 text-xs">
                <div>
                  <label className="block text-slate-700 font-semibold mb-1.5">Rating</label>
                  <div className="flex items-center space-x-2">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <button
                        key={star}
                        type="button"
                        onClick={() => setRating(star)}
                        className="p-1 text-slate-300 hover:text-amber-400"
                      >
                        <Star className={`w-6 h-6 ${star <= rating ? 'text-amber-400 fill-amber-400' : 'text-slate-300'}`} />
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-slate-700 font-semibold mb-1">Feedback & Technical Comments</label>
                  <textarea
                    rows={4}
                    required
                    placeholder="Describe any issues, inquiries, or suggestions for NCAM system administration..."
                    value={feedbackText}
                    onChange={(e) => setFeedbackText(e.target.value)}
                    className="w-full p-3 rounded-xl border border-slate-300 text-slate-900 bg-slate-50 text-xs focus:outline-none focus:border-emerald-600"
                  />
                </div>

                <div className="flex justify-end space-x-2 pt-2">
                  <button
                    type="button"
                    onClick={() => setIsOpen(false)}
                    className="px-4 py-2 rounded-lg bg-slate-100 text-slate-600 font-semibold hover:bg-slate-200"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-5 py-2 rounded-lg bg-emerald-700 hover:bg-emerald-800 text-white font-bold flex items-center gap-1.5 shadow-sm"
                  >
                    <Send className="w-3.5 h-3.5" />
                    <span>Submit Report</span>
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </>
  );
};
