'use client';

import React from 'react';
import { Users, Mail, Phone, BookOpen, Award } from 'lucide-react';
import { Researcher } from '@/lib/data';

interface ResearchersViewProps {
  researchers: Researcher[];
}

export const ResearchersView: React.FC<ResearchersViewProps> = ({ researchers }) => {
  return (
    <div className="space-y-6 animate-fadeIn">
      <div className="ncam-card p-6 border-l-4 border-l-emerald-600 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Users className="w-5 h-5 text-emerald-700" /> NCAM Faculty & Research Officers Directory
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Registered research staff, engineers, designated department points of contact, and academic specializations.
          </p>
        </div>

        <div className="text-xs text-emerald-800 font-bold bg-emerald-50 px-3.5 py-1.5 rounded-lg border border-emerald-200">
          {researchers.length} Active Researchers
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {researchers.map((r) => (
          <div key={r.id} className="ncam-card p-5 space-y-3 flex flex-col justify-between">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="px-2.5 py-0.5 rounded text-[10px] font-extrabold bg-emerald-100 text-emerald-800 border border-emerald-300">
                  {r.department_code} Department
                </span>
                <span className="text-[11px] text-slate-500 font-bold flex items-center gap-1">
                  <BookOpen className="w-3.5 h-3.5 text-emerald-700" /> {r.publications_count} Publications
                </span>
              </div>

              <div>
                <h3 className="text-base font-bold text-slate-900 leading-snug">{r.full_name}</h3>
                <p className="text-xs text-slate-600 font-medium">{r.designation}</p>
              </div>

              <div className="bg-slate-50 p-3 rounded-lg border border-slate-200 text-xs">
                <span className="text-[10px] text-slate-500 font-bold block uppercase">Specialization</span>
                <p className="text-slate-800 font-medium mt-0.5 leading-relaxed">{r.specialization}</p>
              </div>
            </div>

            <div className="pt-3 border-t border-slate-200 text-xs text-slate-600 space-y-1">
              <div className="flex items-center gap-2">
                <Mail className="w-3.5 h-3.5 text-emerald-700 shrink-0" />
                <a href={`mailto:${r.email}`} className="hover:text-emerald-800 truncate">{r.email}</a>
              </div>
              <div className="flex items-center gap-2">
                <Phone className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                <span>{r.phone}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
