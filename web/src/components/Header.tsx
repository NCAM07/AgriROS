'use client';

import React from 'react';
import { LogOut } from 'lucide-react';

interface HeaderProps {
  user: { name: string; role: 'Management' | 'Staff'; department?: string; email: string };
  onLogout: () => void;
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Header: React.FC<HeaderProps> = ({ user, onLogout, activeTab, setActiveTab }) => {
  const managementTabs = [
    { id: 'overview', label: 'Executive Dashboard' },
    { id: 'research', label: 'Research Publications' },
    { id: 'prototypes', label: 'Machinery Prototypes' },
    { id: 'researchers', label: 'Faculty Directory' },
    { id: 'ai-search', label: 'AI Intelligence Query' },
  ];

  const staffTabs = [
    { id: 'staff-portal', label: 'Staff Management Portal' },
    { id: 'research', label: 'Department Research Library' },
    { id: 'overview', label: 'Projects Overview' },
  ];

  const isManagement = user.role === 'Management';
  const currentTabs = isManagement ? managementTabs : staffTabs;

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-sm">
      {/* Top NCAM Official Header - Distinct Banner per System */}
      <div className={`text-white px-6 py-3 flex items-center justify-between transition-all ${
        isManagement
          ? 'bg-gradient-to-r from-emerald-800 to-emerald-900'
          : 'bg-gradient-to-r from-teal-800 to-slate-900'
      }`}>
        <div className="flex items-center space-x-3.5">
          <div className="bg-white p-1 rounded-xl shadow-md flex items-center justify-center">
            <img
              src="/ncam-logo.png"
              alt="NCAM Official Logo"
              className="h-10 w-auto object-contain"
              onError={(e) => {
                (e.target as HTMLElement).style.display = 'none';
              }}
            />
          </div>
          <div>
            <h1 className="text-base font-bold tracking-tight text-white flex items-center gap-2">
              National Centre for Agricultural Mechanization
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${
                isManagement
                  ? 'bg-emerald-950/80 text-emerald-200 border-emerald-500/40'
                  : 'bg-teal-950/80 text-teal-200 border-teal-500/40'
              }`}>
                {isManagement ? 'Executive Leadership Portal' : `${user.department || 'FPM'} Staff Data Portal`}
              </span>
            </h1>
            <p className="text-xs text-emerald-100/90 font-medium">
              AgriROS System • {isManagement ? 'Management Telemetry & AI Query' : `${user.department || 'FPM'} Department Data Management`}
            </p>
          </div>
        </div>

        {/* User Session Profile & Sign Out */}
        <div className="flex items-center space-x-3">
          <div className="hidden sm:block text-right">
            <span className="text-xs font-bold text-white block">{user.name}</span>
            <span className="text-[10px] text-emerald-200 block font-medium">
              {user.email}
            </span>
          </div>

          <button
            onClick={onLogout}
            title="Sign Out to Login Screen"
            className="px-3.5 py-1.5 rounded-lg bg-slate-900/80 hover:bg-slate-950 border border-white/20 text-xs font-bold text-white flex items-center space-x-1.5 transition-colors shadow-sm"
          >
            <LogOut className="w-3.5 h-3.5 text-emerald-300" />
            <span>Sign Out</span>
          </button>
        </div>
      </div>

      {/* Dynamic Navigation Bar Restricted to System */}
      <div className="max-w-7xl mx-auto px-6 flex items-center justify-between h-12">
        <nav className="flex space-x-1">
          {currentTabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2.5 text-xs font-bold transition-all border-b-2 ${
                activeTab === tab.id
                  ? 'border-emerald-700 text-emerald-800 bg-emerald-50/70'
                  : 'border-transparent text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>

        <div className="text-xs text-slate-500 font-medium hidden md:block">
          System Access: <strong className="text-emerald-800 font-bold">{isManagement ? 'Executive Management System' : `${user.department || 'FPM'} Department Data Officer System`}</strong>
        </div>
      </div>
    </header>
  );
};
