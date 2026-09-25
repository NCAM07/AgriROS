'use client';

import React, { useState } from 'react';
import { BookOpen, ExternalLink, Search, Filter, FileText, CheckCircle2 } from 'lucide-react';
import { ResearchPaper } from '@/lib/data';

interface ResearchViewProps {
  papers: ResearchPaper[];
}

export const ResearchView: React.FC<ResearchViewProps> = ({ papers }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [deptFilter, setDeptFilter] = useState('All');

  const filtered = papers.filter(p => {
    const matchesSearch = p.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.lead_researcher.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.journal_name?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesDept = deptFilter === 'All' || p.department_code === deptFilter;
    return matchesSearch && matchesDept;
  });

  return (
    <div className="space-y-6 animate-fadeIn">
      <div className="ncam-card p-6 border-l-4 border-l-emerald-600 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-emerald-700" /> NCAM Departmental Research Publications & Technical Papers
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Central repository of published research papers, technical bulletins, and experimental journal articles across all NCAM departments.
          </p>
        </div>

        <div className="text-xs text-emerald-800 font-bold bg-emerald-50 px-3.5 py-1.5 rounded-lg border border-emerald-200">
          {papers.length} Published Papers
        </div>
      </div>

      {/* Filter & Search */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-2.5" />
          <input
            type="text"
            placeholder="Search research title, author, or journal..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-4 py-2 text-xs rounded-lg border border-slate-300 focus:outline-none focus:border-emerald-600 bg-white text-slate-900 placeholder-slate-400"
          />
        </div>

        <div className="flex items-center space-x-2">
          {['All', 'FPM', 'ESS'].map(dept => (
            <button
              key={dept}
              onClick={() => setDeptFilter(dept)}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                deptFilter === dept
                  ? 'bg-emerald-700 text-white shadow-sm'
                  : 'bg-white text-slate-600 border border-slate-300 hover:bg-slate-50'
              }`}
            >
              {dept === 'All' ? 'All Departments' : `${dept} Dept`}
            </button>
          ))}
        </div>
      </div>

      {/* Research Papers Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filtered.map((paper) => (
          <div key={paper.id} className="ncam-card p-5 space-y-3 flex flex-col justify-between">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="px-2.5 py-0.5 rounded text-[10px] font-extrabold bg-emerald-100 text-emerald-800 border border-emerald-300">
                  {paper.department_code} Department
                </span>
                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold ncam-badge-green">
                  {paper.status}
                </span>
              </div>

              <h3 className="text-sm font-bold text-slate-900 leading-snug">{paper.title}</h3>
              <p className="text-xs text-slate-600 font-medium">Author: {paper.lead_researcher}</p>
            </div>

            <div className="pt-3 border-t border-slate-200 text-xs space-y-2">
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-200 space-y-1">
                <span className="text-[10px] text-slate-500 font-bold block uppercase">Journal / Technical Publisher</span>
                <span className="font-semibold text-slate-800 block">{paper.journal_name || 'NCAM Official Technical Bulletin'}</span>
                <span className="text-[11px] text-slate-500 block">Published: {paper.publication_date}</span>
              </div>

              {paper.doi_or_link && (
                <a
                  href={paper.doi_or_link}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-1.5 text-xs text-emerald-700 font-bold hover:underline pt-1"
                >
                  <ExternalLink className="w-3.5 h-3.5" /> Access Full Publication Document / DOI
                </a>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
