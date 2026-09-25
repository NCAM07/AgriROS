'use client';

import React, { useState } from 'react';
import {
  FolderKanban, CheckCircle2, AlertTriangle, Wrench,
  DollarSign, Search, ChevronRight, X, User, Calendar
} from 'lucide-react';
import { Project, INITIAL_MILESTONES } from '@/lib/data';

interface OverviewViewProps {
  projects: Project[];
  onNavigate: (tab: 'overview' | 'prototypes' | 'ai-search') => void;
}

export const OverviewView: React.FC<OverviewViewProps> = ({ projects, onNavigate }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);

  const totalAllocated = projects.reduce((acc, p) => acc + (p.budget_allocated || 0), 0);
  const totalUtilized = projects.reduce((acc, p) => acc + (p.budget_utilized || 0), 0);
  const delayedCount = projects.filter(p => p.status === 'Behind Schedule').length;
  const machinesBuilt = projects.filter(p => p.machine_built).length;

  const filteredProjects = projects.filter(p =>
    p.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.lead_researcher_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.keywords.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* 4 Clean Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Active Projects */}
        <div className="ncam-card p-5 border-l-4 border-l-emerald-600 flex items-center justify-between">
          <div>
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Total Projects</span>
            <div className="text-2xl font-black text-slate-900 mt-1">{projects.length}</div>
            <span className="text-xs text-slate-500 font-medium">Across FPM & ESS</span>
          </div>
          <div className="p-3 bg-emerald-50 text-emerald-700 rounded-xl border border-emerald-200">
            <FolderKanban className="w-6 h-6" />
          </div>
        </div>

        {/* Machines Fabricated */}
        <div className="ncam-card p-5 border-l-4 border-l-blue-600 flex items-center justify-between">
          <div>
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Machines Built</span>
            <div className="text-2xl font-black text-slate-900 mt-1">{machinesBuilt} Prototypes</div>
            <span className="text-xs text-emerald-700 font-semibold">Physical Units Built</span>
          </div>
          <div className="p-3 bg-blue-50 text-blue-700 rounded-xl border border-blue-200">
            <Wrench className="w-6 h-6" />
          </div>
        </div>

        {/* Total Budget Absorbed */}
        <div className="ncam-card p-5 border-l-4 border-l-purple-600 flex items-center justify-between">
          <div>
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Total Funding</span>
            <div className="text-2xl font-black text-slate-900 mt-1">₦{(totalAllocated / 1000000).toFixed(1)}M</div>
            <span className="text-xs text-slate-500 font-medium">₦{(totalUtilized / 1000000).toFixed(1)}M Absorbed</span>
          </div>
          <div className="p-3 bg-purple-50 text-purple-700 rounded-xl border border-purple-200">
            <DollarSign className="w-6 h-6" />
          </div>
        </div>

        {/* Delayed Projects Alert */}
        <div className="ncam-card p-5 border-l-4 border-l-amber-500 flex items-center justify-between">
          <div>
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Behind Schedule</span>
            <div className="text-2xl font-black text-amber-700 mt-1">{delayedCount} Project</div>
            <span className="text-xs text-amber-600 font-semibold">Requires Management Attention</span>
          </div>
          <div className="p-3 bg-amber-50 text-amber-700 rounded-xl border border-amber-200">
            <AlertTriangle className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* Main Executive Projects Table Card */}
      <div className="ncam-card p-6 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-4">
          <div>
            <h2 className="text-base font-bold text-slate-900">NCAM Research & Development Projects</h2>
            <p className="text-xs text-slate-500">Click on any project to view detailed objectives, budgets, and milestones.</p>
          </div>

          <div className="relative w-full md:w-80">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search projects or researchers..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-4 py-2 text-xs rounded-lg border border-slate-300 focus:outline-none focus:border-emerald-600 bg-slate-50 text-slate-900 placeholder-slate-400"
            />
          </div>
        </div>

        {/* Clean Project Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="bg-slate-100/80 text-slate-600 border-b border-slate-200 font-bold uppercase text-[10px] tracking-wider">
                <th className="py-3 px-4">Dept</th>
                <th className="py-3 px-4">Project Title</th>
                <th className="py-3 px-4">Lead Researcher</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4 text-right">Budget (Utilized / Allocated)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {filteredProjects.map((project) => (
                <tr
                  key={project.id}
                  onClick={() => setSelectedProject(project)}
                  className="hover:bg-emerald-50/50 cursor-pointer transition-colors"
                >
                  <td className="py-3 px-4 font-bold text-emerald-800">
                    {project.department_code || 'FPM'}
                  </td>
                  <td className="py-3 px-4 font-bold text-slate-900 max-w-xs truncate">
                    {project.title}
                  </td>
                  <td className="py-3 px-4 text-slate-600">
                    {project.lead_researcher_name}
                  </td>
                  <td className="py-3 px-4">
                    <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold ${
                      project.status === 'Commercialized'
                        ? 'ncam-badge-green'
                        : project.status === 'Ongoing'
                        ? 'ncam-badge-blue'
                        : project.status === 'Behind Schedule'
                        ? 'ncam-badge-amber'
                        : 'bg-slate-100 text-slate-700 border border-slate-300'
                    }`}>
                      {project.status}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-right font-medium text-slate-900">
                    ₦{(project.budget_utilized / 1000000).toFixed(1)}M / ₦{(project.budget_allocated / 1000000).toFixed(1)}M
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Project Detail Modal */}
      {selectedProject && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4 animate-fadeIn">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl max-w-xl w-full p-6 space-y-5">
            <div className="flex items-center justify-between border-b border-slate-200 pb-3">
              <div>
                <span className="px-2.5 py-0.5 rounded text-[10px] font-extrabold bg-emerald-100 text-emerald-800 border border-emerald-300">
                  {selectedProject.department_code || 'FPM'} Department
                </span>
                <h3 className="text-base font-bold text-slate-900 mt-1 leading-snug">{selectedProject.title}</h3>
              </div>
              <button
                onClick={() => setSelectedProject(null)}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs text-slate-600 leading-relaxed bg-slate-50 p-3 rounded-xl border border-slate-200">
              {selectedProject.summary}
            </p>

            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
                <span className="text-[10px] text-slate-500 font-bold block uppercase">LEAD RESEARCHER</span>
                <span className="font-bold text-slate-900">{selectedProject.lead_researcher_name}</span>
                <span className="text-[11px] text-slate-500 block">{selectedProject.lead_researcher_designation}</span>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
                <span className="text-[10px] text-slate-500 font-bold block uppercase">SUPERVISOR</span>
                <span className="font-bold text-slate-900">{selectedProject.supervisor_name}</span>
                <span className="text-[11px] text-slate-500 block">{selectedProject.supervisor_designation}</span>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
                <span className="text-[10px] text-slate-500 font-bold block uppercase">FUNDING SOURCE</span>
                <span className="font-bold text-slate-900">{selectedProject.funding_source}</span>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
                <span className="text-[10px] text-slate-500 font-bold block uppercase">BUDGET ALLOCATED</span>
                <span className="font-bold text-emerald-800">₦{selectedProject.budget_allocated.toLocaleString()}</span>
              </div>
            </div>

            <div className="flex justify-end">
              <button
                onClick={() => setSelectedProject(null)}
                className="px-5 py-2 bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-bold rounded-lg transition-colors"
              >
                Close Project Summary
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
