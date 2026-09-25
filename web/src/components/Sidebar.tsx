'use client';

import React from 'react';
import {
  LayoutDashboard, FolderKanban, Wrench, Sparkles,
  FileCheck, Users, MessageSquareQuote, CheckCircle2, ChevronRight
} from 'lucide-react';

export type NavTab = 'overview' | 'projects' | 'prototypes' | 'ai-search' | 'staging' | 'researchers' | 'feedback-history';

interface SidebarProps {
  activeTab: NavTab;
  setActiveTab: (tab: NavTab) => void;
  role: 'Management' | 'Researcher';
  feedbackCount: number;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab, role, feedbackCount }) => {
  const navItems = [
    { id: 'overview' as NavTab, label: 'Executive Overview', icon: LayoutDashboard, badge: null },
    { id: 'projects' as NavTab, label: 'Projects & Milestones', icon: FolderKanban, badge: '5' },
    { id: 'prototypes' as NavTab, label: 'Prototype Tracker', icon: Wrench, badge: '4' },
    { id: 'ai-search' as NavTab, label: 'AI Intelligence Engine', icon: Sparkles, badge: 'Groq' },
    { id: 'staging' as NavTab, label: 'Doc Extraction Staging', icon: FileCheck, badge: '2' },
    { id: 'researchers' as NavTab, label: 'Research Roster', icon: Users, badge: null },
    { id: 'feedback-history' as NavTab, label: 'Pilot Feedback Log', icon: MessageSquareQuote, badge: feedbackCount > 0 ? String(feedbackCount) : null },
  ];

  return (
    <aside className="w-64 glass-panel border-r border-slate-800/80 p-4 flex flex-col justify-between shrink-0 min-h-[calc(100vh-4.25rem)]">
      <div className="space-y-6">
        {/* Pilot Banner */}
        <div className="p-3.5 rounded-xl bg-gradient-to-r from-emerald-950/60 to-slate-900 border border-emerald-500/30">
          <div className="flex items-center space-x-2 text-xs font-bold text-emerald-400">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Pilot Test Environment</span>
          </div>
          <p className="text-[11px] text-slate-400 mt-1 leading-relaxed">
            Active view: <strong className="text-slate-200 font-semibold">{role}</strong>
          </p>
        </div>

        {/* Navigation Menu */}
        <nav className="space-y-1.5">
          <p className="px-3 text-[10px] font-bold text-slate-500 uppercase tracking-wider">
            Navigation Menu
          </p>

          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all group ${
                  isActive
                    ? 'bg-emerald-600/20 text-emerald-300 border border-emerald-500/40 shadow-lg shadow-emerald-950/50'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <Icon className={`w-4 h-4 transition-transform group-hover:scale-110 ${isActive ? 'text-emerald-400' : 'text-slate-500'}`} />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className={`px-2 py-0.5 rounded-md text-[10px] font-bold ${
                    item.badge === 'Groq'
                      ? 'bg-teal-500/20 text-teal-300 border border-teal-500/30'
                      : isActive
                      ? 'bg-emerald-500 text-slate-950 font-extrabold'
                      : 'bg-slate-800 text-slate-400'
                  }`}>
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Pilot Tester Quick Note */}
      <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 text-[11px] text-slate-400 space-y-2">
        <div className="flex items-center justify-between text-slate-300 font-semibold">
          <span>Need Help or Feedback?</span>
          <ChevronRight className="w-3.5 h-3.5 text-emerald-400" />
        </div>
        <p className="text-slate-400 leading-snug">
          Use the floating <span className="text-emerald-400 font-semibold">Pilot Feedback drawer</span> at bottom right to submit your thoughts per section.
        </p>
      </div>
    </aside>
  );
};
