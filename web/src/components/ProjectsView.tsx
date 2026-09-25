'use client';

import React, { useState } from 'react';
import {
  FolderKanban, Search, Filter, Plus, Calendar, DollarSign,
  User, CheckCircle, Clock, AlertTriangle, ChevronRight, X
} from 'lucide-react';
import { Project, Milestone, INITIAL_MILESTONES } from '@/lib/data';

interface ProjectsViewProps {
  projects: Project[];
  setProjects: (projects: Project[]) => void;
  role: 'Management' | 'Researcher';
}

export const ProjectsView: React.FC<ProjectsViewProps> = ({ projects, setProjects, role }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('All');
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [showAddModal, setShowAddModal] = useState(false);

  // New Project Form State
  const [newTitle, setNewTitle] = useState('');
  const [newDept, setNewDept] = useState(1);
  const [newLead, setNewLead] = useState('');
  const [newSupervisor, setNewSupervisor] = useState('');
  const [newBudget, setNewBudget] = useState(3000000);
  const [newFunding, setNewFunding] = useState('NCAM Internal');

  const filteredProjects = projects.filter(p => {
    const matchesSearch = p.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.keywords.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.lead_researcher_name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'All' || p.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const handleAddProject = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim() || !newLead.trim()) return;

    const newProject: Project = {
      id: Date.now(),
      title: newTitle,
      department_id: newDept,
      department_code: newDept === 1 ? 'FPM' : 'ESS',
      status: 'Ongoing',
      supervisor_name: newSupervisor || 'Dr. Abubakar Musa',
      supervisor_designation: 'Chief Research Officer',
      supervisor_email: 'a.musa@ncam.gov.ng',
      supervisor_phone: '08012345678',
      lead_researcher_name: newLead,
      lead_researcher_designation: 'Research Officer',
      start_date: new Date().toISOString().split('T')[0],
      expected_end_date: '2025-12-31',
      budget_allocated: Number(newBudget),
      budget_utilized: 0,
      funding_source: newFunding,
      keywords: 'agricultural machinery, pilot test',
      machine_built: false,
      progress_pct: 10,
      summary: 'Newly created agricultural research initiative submitted by pilot officer.'
    };

    setProjects([newProject, ...projects]);
    setShowAddModal(false);
    setNewTitle('');
    setNewLead('');
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Header Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 glass-panel p-5 rounded-2xl border border-slate-800">
        <div>
          <h2 className="text-xl font-extrabold text-white flex items-center gap-2">
            <FolderKanban className="w-6 h-6 text-emerald-400" /> Research Projects Catalog
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Monitor timelines, budget absorption, milestone deliverables, and lead researchers
          </p>
        </div>

        {role === 'Management' && (
          <button
            onClick={() => setShowAddModal(true)}
            className="px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-950/40 transition-all flex items-center space-x-2 shrink-0"
          >
            <Plus className="w-4 h-4" />
            <span>Create Research Project</span>
          </button>
        )}
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col md:flex-row items-center gap-4">
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
          <input
            type="text"
            placeholder="Search projects by title, researcher, or crop keywords..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
          />
        </div>

        <div className="flex items-center space-x-2 overflow-x-auto w-full md:w-auto pb-1 md:pb-0">
          {['All', 'Ongoing', 'Completed', 'Commercialized', 'Behind Schedule'].map((status) => (
            <button
              key={status}
              onClick={() => setStatusFilter(status)}
              className={`px-3.5 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all ${
                statusFilter === status
                  ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 shadow-md'
                  : 'bg-slate-950/60 text-slate-400 border border-slate-800 hover:border-slate-700'
              }`}
            >
              {status}
            </button>
          ))}
        </div>
      </div>

      {/* Project Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredProjects.map((project) => (
          <div
            key={project.id}
            onClick={() => setSelectedProject(project)}
            className="glass-panel glass-panel-hover p-5 rounded-2xl border border-slate-800 cursor-pointer space-y-4 flex flex-col justify-between"
          >
            <div className="space-y-2">
              <div className="flex items-center justify-between gap-2">
                <span className="px-2.5 py-0.5 rounded-md text-[10px] font-extrabold bg-slate-800 text-emerald-400 border border-slate-700">
                  {project.department_code || 'FPM'} Dept
                </span>
                <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-extrabold ${
                  project.status === 'Commercialized'
                    ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                    : project.status === 'Ongoing'
                    ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                    : project.status === 'Behind Schedule'
                    ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                    : 'bg-purple-500/20 text-purple-400 border border-purple-500/30'
                }`}>
                  {project.status}
                </span>
              </div>

              <h3 className="text-base font-bold text-white group-hover:text-emerald-400 transition-colors leading-snug">
                {project.title}
              </h3>
              <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed">
                {project.summary || 'NCAM agricultural mechanization project under field validation.'}
              </p>
            </div>

            <div className="space-y-3 pt-2 border-t border-slate-800/80">
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span className="text-[10px] text-slate-500 block font-semibold">LEAD RESEARCHER</span>
                  <span className="text-slate-200 font-medium truncate block">{project.lead_researcher_name}</span>
                </div>
                <div>
                  <span className="text-[10px] text-slate-500 block font-semibold">SUPERVISOR</span>
                  <span className="text-slate-300 truncate block">{project.supervisor_name}</span>
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between text-[10px] font-bold text-slate-400 mb-1">
                  <span>BUDGET UTILIZATION</span>
                  <span className="text-white">₦{(project.budget_utilized / 1000000).toFixed(1)}M / ₦{(project.budget_allocated / 1000000).toFixed(1)}M</span>
                </div>
                <div className="w-full bg-slate-900 h-2 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full ${
                      project.status === 'Behind Schedule' ? 'bg-amber-500' : 'bg-emerald-500'
                    }`}
                    style={{ width: `${Math.min(100, Math.round((project.budget_utilized / (project.budget_allocated || 1)) * 100))}%` }}
                  />
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Selected Project Detail Drawer */}
      {selectedProject && (
        <div className="fixed inset-0 z-50 flex justify-end bg-slate-950/70 backdrop-blur-sm animate-fadeIn">
          <div className="w-full max-w-xl bg-slate-900 border-l border-slate-800 shadow-2xl p-6 flex flex-col justify-between overflow-y-auto space-y-6">
            <div className="space-y-6">
              <div className="flex items-center justify-between border-b border-slate-800 pb-4">
                <span className="px-2.5 py-1 rounded text-xs font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                  {selectedProject.department_code || 'FPM'} • ID #{selectedProject.id}
                </span>
                <button
                  onClick={() => setSelectedProject(null)}
                  className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div>
                <h3 className="text-lg font-black text-white leading-snug">{selectedProject.title}</h3>
                <p className="text-xs text-slate-400 mt-2 leading-relaxed">
                  {selectedProject.summary}
                </p>
              </div>

              {/* Specs Grid */}
              <div className="grid grid-cols-2 gap-3 p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs">
                <div>
                  <span className="text-slate-500 block text-[10px] font-bold">STATUS</span>
                  <span className="text-emerald-400 font-bold">{selectedProject.status}</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[10px] font-bold">FUNDING SOURCE</span>
                  <span className="text-slate-200">{selectedProject.funding_source}</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[10px] font-bold">START DATE</span>
                  <span className="text-slate-300">{selectedProject.start_date}</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[10px] font-bold">EXPECTED END</span>
                  <span className="text-slate-300">{selectedProject.expected_end_date}</span>
                </div>
              </div>

              {/* Objectives */}
              <div className="space-y-2">
                <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Project Objectives</h4>
                <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800 text-xs text-slate-300 leading-relaxed whitespace-pre-line">
                  {selectedProject.objectives || '1. Complete machine CAD design\n2. Fabricate prototype body\n3. Execute multi-soil field trial.'}
                </div>
              </div>

              {/* Milestones for this project */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Project Milestones</h4>
                <div className="space-y-2">
                  {INITIAL_MILESTONES.filter(m => m.project_id === selectedProject.id).map(m => (
                    <div key={m.id} className="p-3 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between text-xs">
                      <div>
                        <span className="font-bold text-white block">{m.title}</span>
                        <span className="text-[11px] text-slate-400">{m.description}</span>
                      </div>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        m.status === 'Completed' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'
                      }`}>
                        {m.status}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <button
              onClick={() => setSelectedProject(null)}
              className="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs transition-colors"
            >
              Close Project Drawer
            </button>
          </div>
        </div>
      )}

      {/* Add Project Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4 animate-fadeIn">
          <div className="w-full max-w-lg bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-base font-bold text-white">Create New Research Project</h3>
              <button onClick={() => setShowAddModal(false)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleAddProject} className="space-y-4 text-xs">
              <div>
                <label className="block text-slate-300 font-semibold mb-1">Project Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Design & Optimization of Cassava Starch Extractor"
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white placeholder-slate-600 focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Department</label>
                  <select
                    value={newDept}
                    onChange={(e) => setNewDept(Number(e.target.value))}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white focus:outline-none focus:border-emerald-500"
                  >
                    <option value={1}>FPM - Farm Power & Machinery</option>
                    <option value={2}>ESS - Engineering Support Services</option>
                  </select>
                </div>
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Funding Source</label>
                  <input
                    type="text"
                    value={newFunding}
                    onChange={(e) => setNewFunding(e.target.value)}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white focus:outline-none focus:border-emerald-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Lead Researcher</label>
                  <input
                    type="text"
                    required
                    placeholder="Engr. Name"
                    value={newLead}
                    onChange={(e) => setNewLead(e.target.value)}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white placeholder-slate-600 focus:outline-none focus:border-emerald-500"
                  />
                </div>
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Allocated Budget (₦)</label>
                  <input
                    type="number"
                    value={newBudget}
                    onChange={(e) => setNewBudget(Number(e.target.value))}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-white focus:outline-none focus:border-emerald-500"
                  />
                </div>
              </div>

              <div className="flex justify-end space-x-3 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 font-semibold hover:bg-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl bg-emerald-600 text-slate-950 font-bold hover:bg-emerald-500"
                >
                  Save & Publish
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
