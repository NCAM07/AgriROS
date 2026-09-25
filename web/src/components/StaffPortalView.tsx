'use client';

import React, { useState } from 'react';
import { UserCheck, BookOpen, UserPlus, FolderPlus, Send, CheckCircle2, Upload } from 'lucide-react';
import { ResearchPaper, Researcher, Project } from '@/lib/data';

interface StaffPortalViewProps {
  onAddResearch: (paper: ResearchPaper) => void;
  onAddResearcher: (researcher: Researcher) => void;
  onAddProject: (project: Project) => void;
}

export const StaffPortalView: React.FC<StaffPortalViewProps> = ({
  onAddResearch,
  onAddResearcher,
  onAddProject
}) => {
  const [activeForm, setActiveForm] = useState<'research' | 'researcher' | 'project'>('research');
  const [toastMsg, setToastMsg] = useState<string | null>(null);

  // 1. Research Form State
  const [resTitle, setResTitle] = useState('');
  const [resDept, setResDept] = useState('FPM');
  const [resAuthor, setResAuthor] = useState('');
  const [resJournal, setResJournal] = useState('');
  const [resLink, setResLink] = useState('');
  const [resDate, setResDate] = useState(new Date().toISOString().split('T')[0]);

  // 2. Researcher Form State
  const [name, setName] = useState('');
  const [designation, setDesignation] = useState('Senior Research Engineer');
  const [dept, setDept] = useState('FPM');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [specialization, setSpecialization] = useState('');

  // 3. Project Form State
  const [projTitle, setProjTitle] = useState('');
  const [projDept, setProjDept] = useState('FPM');
  const [projLead, setProjLead] = useState('');
  const [projBudget, setProjBudget] = useState(3500000);

  const showToast = (msg: string) => {
    setToastMsg(msg);
    setTimeout(() => setToastMsg(null), 3000);
  };

  const handleResearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!resTitle || !resAuthor) return;

    onAddResearch({
      id: Date.now(),
      title: resTitle,
      department_code: resDept,
      lead_researcher: resAuthor,
      research_type: "Departmental Research Paper",
      status: "Published",
      journal_name: resJournal || "NCAM Technical Bulletin",
      publication_date: resDate,
      doi_or_link: resLink || "https://ncam.gov.ng/research/latest",
      extracted_from_doc: false
    });

    setResTitle('');
    setResAuthor('');
    setResJournal('');
    setResLink('');
    showToast('Research Publication successfully registered into NCAM Database!');
  };

  const handleResearcherSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !email) return;

    onAddResearcher({
      id: Date.now(),
      full_name: name,
      designation: designation,
      department_code: dept,
      email: email,
      phone: phone || '+234 800 000 0000',
      specialization: specialization || 'Agricultural Mechanization',
      active_projects_count: 1,
      publications_count: 1
    });

    setName('');
    setEmail('');
    setPhone('');
    setSpecialization('');
    showToast('Department Researcher registered successfully!');
  };

  const handleProjectSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!projTitle || !projLead) return;

    onAddProject({
      id: Date.now(),
      title: projTitle,
      department_id: projDept === 'FPM' ? 1 : 2,
      department_code: projDept,
      status: 'Ongoing',
      supervisor_name: 'Dr. Abubakar Musa',
      supervisor_designation: 'Chief Research Officer',
      supervisor_email: 'a.musa@ncam.gov.ng',
      supervisor_phone: '08012345678',
      lead_researcher_name: projLead,
      lead_researcher_designation: 'Research Officer',
      start_date: new Date().toISOString().split('T')[0],
      expected_end_date: '2025-12-31',
      budget_allocated: Number(projBudget),
      budget_utilized: 0,
      funding_source: 'NCAM Internal Allocation',
      keywords: 'machinery, agricultural research',
      machine_built: false,
      summary: 'Newly registered R&D project submitted by Department Data Officer.'
    });

    setProjTitle('');
    setProjLead('');
    showToast('R&D Project registered successfully!');
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto animate-fadeIn">
      {/* Header Banner */}
      <div className="ncam-card p-6 border-l-4 border-l-emerald-600 space-y-2">
        <div className="flex items-center space-x-2 text-emerald-800">
          <UserCheck className="w-5 h-5 text-emerald-700" />
          <h2 className="text-lg font-bold text-slate-900">Departmental Data Officer Portal</h2>
        </div>
        <p className="text-xs text-slate-600 leading-relaxed">
          Designated staff entry point for registering new research publications, onboarding department researchers, and updating active project statuses across FPM & ESS.
        </p>
      </div>

      {toastMsg && (
        <div className="p-4 bg-emerald-100 border border-emerald-300 text-emerald-900 rounded-xl text-xs font-bold flex items-center space-x-2 animate-scaleUp">
          <CheckCircle2 className="w-5 h-5 text-emerald-700 shrink-0" />
          <span>{toastMsg}</span>
        </div>
      )}

      {/* Form Navigation Tabs */}
      <div className="flex items-center space-x-2 border-b border-slate-200 pb-2">
        <button
          onClick={() => setActiveForm('research')}
          className={`px-4 py-2 rounded-lg text-xs font-bold flex items-center space-x-2 transition-all ${
            activeForm === 'research'
              ? 'bg-emerald-700 text-white shadow-sm'
              : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
          }`}
        >
          <BookOpen className="w-4 h-4" />
          <span>Publish Research Paper</span>
        </button>

        <button
          onClick={() => setActiveForm('researcher')}
          className={`px-4 py-2 rounded-lg text-xs font-bold flex items-center space-x-2 transition-all ${
            activeForm === 'researcher'
              ? 'bg-emerald-700 text-white shadow-sm'
              : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
          }`}
        >
          <UserPlus className="w-4 h-4" />
          <span>Register Staff / Researcher</span>
        </button>

        <button
          onClick={() => setActiveForm('project')}
          className={`px-4 py-2 rounded-lg text-xs font-bold flex items-center space-x-2 transition-all ${
            activeForm === 'project'
              ? 'bg-emerald-700 text-white shadow-sm'
              : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
          }`}
        >
          <FolderPlus className="w-4 h-4" />
          <span>Register R&D Project</span>
        </button>
      </div>

      {/* 1. Research Publication Form */}
      {activeForm === 'research' && (
        <form onSubmit={handleResearchSubmit} className="ncam-card p-6 space-y-4 text-xs">
          <h3 className="text-sm font-bold text-slate-900 border-b border-slate-200 pb-2">
            Upload & Register Published Research Paper
          </h3>

          <div>
            <label className="block text-slate-700 font-semibold mb-1">Research Paper Title *</label>
            <input
              type="text"
              required
              placeholder="e.g. Field Optimization & Moisture Sensor Calibration for Yam Mounds"
              value={resTitle}
              onChange={(e) => setResTitle(e.target.value)}
              className="w-full p-2.5 rounded-lg border border-slate-300 text-slate-900 bg-slate-50 focus:outline-none focus:border-emerald-600"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-slate-700 font-semibold mb-1">Department *</label>
              <select
                value={resDept}
                onChange={(e) => setResDept(e.target.value)}
                className="w-full p-2.5 rounded-lg border border-slate-300 text-slate-900 bg-slate-50 focus:outline-none focus:border-emerald-600"
              >
                <option value="FPM">Farm Power & Machinery (FPM)</option>
                <option value="ESS">Engineering Support Services (ESS)</option>
              </select>
            </div>

            <div>
              <label className="block text-slate-700 font-semibold mb-1">Lead Author / Researcher *</label>
              <input
                type="text"
                required
                placeholder="e.g. Engr. Yusuf Abdullahi"
                value={resAuthor}
                onChange={(e) => setResAuthor(e.target.value)}
                className="w-full p-2.5 rounded-lg border border-slate-300 text-slate-900 bg-slate-50 focus:outline-none focus:border-emerald-600"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-slate-700 font-semibold mb-1">Journal / Technical Publisher Name</label>
              <input
                type="text"
                placeholder="e.g. Journal of Agricultural Engineering & Tech"
                value={resJournal}
                onChange={(e) => setResJournal(e.target.value)}
                className="w-full p-2.5 rounded-lg border border-slate-300 text-slate-900 bg-slate-50 focus:outline-none focus:border-emerald-600"
              />
            </div>

            <div>
              <label className="block text-slate-700 font-semibold mb-1">Publication Link / DOI URL</label>
              <input
                type="url"
                placeholder="https://doi.org/10.1016/..."
                value={resLink}
                onChange={(e) => setResLink(e.target.value)}
                className="w-full p-2.5 rounded-lg border border-slate-300 text-slate-900 bg-slate-50 focus:outline-none focus:border-emerald-600"
              />
            </div>
          </div>

          <div className="flex justify-end pt-2">
            <button
              type="submit"
              className="px-5 py-2.5 rounded-lg bg-emerald-700 hover:bg-emerald-800 text-white font-bold flex items-center space-x-2 shadow-sm"
            >
              <Send className="w-4 h-4" />
              <span>Publish Research Record</span>
            </button>
          </div>
        </form>
      )}

      {/* 2. Researcher Registration Form */}
      {activeForm === 'researcher' && (
        <form onSubmit={handleResearcherSubmit} className="ncam-card p-6 space-y-4 text-xs">
          <h3 className="text-sm font-bold text-slate-900 border-b border-slate-200 pb-2">
            Register Department Researcher / Staff
          </h3>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-slate-700 font-semibold mb-1">Full Name *</label>
              <input
                type="text"
                required
                placeholder="e.g. Dr. Ibrahim Garba"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full p-2.5 rounded-lg border border-slate-300 text-slate-900 bg-slate-50 focus:outline-none focus:border-emerald-600"
              />
            </div>

            <div>
              <label className="block text-slate-700 font-semibold mb-1">Designation</label>
              <input
                type="text"
                value={designation}
                onChange={(e) => setDesignation(e.target.value)}
                className="w-full p-2.5 rounded-lg border border-slate-300 text-slate-900 bg-slate-50 focus:outline-none focus:border-emerald-600"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-slate-700 font-semibold mb-1">Department *</label>
              <select
                value={dept}
                onChange={(e) => setDept(e.target.value)}
                className="w-full p-2.5 rounded-lg border border-slate-300 text-slate-900 bg-slate-50 focus:outline-none focus:border-emerald-600"
              >
                <option value="FPM">Farm Power & Machinery (FPM)</option>
                <option value="ESS">Engineering Support Services (ESS)</option>
              </select>
            </div>

            <div>
              <label className="block text-slate-700 font-semibold mb-1">Official Email *</label>
              <input
                type="email"
                required
                placeholder="i.garba@ncam.gov.ng"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full p-2.5 rounded-lg border border-slate-300 text-slate-900 bg-slate-50 focus:outline-none focus:border-emerald-600"
              />
            </div>
          </div>

          <div>
            <label className="block text-slate-700 font-semibold mb-1">Area of Specialization</label>
            <input
              type="text"
              placeholder="e.g. Grain Drying Systems & Renewable Biomass Heat Exchangers"
              value={specialization}
              onChange={(e) => setSpecialization(e.target.value)}
              className="w-full p-2.5 rounded-lg border border-slate-300 text-slate-900 bg-slate-50 focus:outline-none focus:border-emerald-600"
            />
          </div>

          <div className="flex justify-end pt-2">
            <button
              type="submit"
              className="px-5 py-2.5 rounded-lg bg-emerald-700 hover:bg-emerald-800 text-white font-bold flex items-center space-x-2 shadow-sm"
            >
              <Send className="w-4 h-4" />
              <span>Register Faculty Member</span>
            </button>
          </div>
        </form>
      )}

      {/* 3. Project Registration Form */}
      {activeForm === 'project' && (
        <form onSubmit={handleProjectSubmit} className="ncam-card p-6 space-y-4 text-xs">
          <h3 className="text-sm font-bold text-slate-900 border-b border-slate-200 pb-2">
            Register New R&D Project
          </h3>

          <div>
            <label className="block text-slate-700 font-semibold mb-1">Project Title *</label>
            <input
              type="text"
              required
              placeholder="e.g. Design & Optimization of Cassava Starch Extraction Rig"
              value={projTitle}
              onChange={(e) => setProjTitle(e.target.value)}
              className="w-full p-2.5 rounded-lg border border-slate-300 text-slate-900 bg-slate-50 focus:outline-none focus:border-emerald-600"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-slate-700 font-semibold mb-1">Department *</label>
              <select
                value={projDept}
                onChange={(e) => setProjDept(e.target.value)}
                className="w-full p-2.5 rounded-lg border border-slate-300 text-slate-900 bg-slate-50 focus:outline-none focus:border-emerald-600"
              >
                <option value="FPM">Farm Power & Machinery (FPM)</option>
                <option value="ESS">Engineering Support Services (ESS)</option>
              </select>
            </div>

            <div>
              <label className="block text-slate-700 font-semibold mb-1">Lead Researcher *</label>
              <input
                type="text"
                required
                placeholder="Engr. Name"
                value={projLead}
                onChange={(e) => setProjLead(e.target.value)}
                className="w-full p-2.5 rounded-lg border border-slate-300 text-slate-900 bg-slate-50 focus:outline-none focus:border-emerald-600"
              />
            </div>
          </div>

          <div className="flex justify-end pt-2">
            <button
              type="submit"
              className="px-5 py-2.5 rounded-lg bg-emerald-700 hover:bg-emerald-800 text-white font-bold flex items-center space-x-2 shadow-sm"
            >
              <Send className="w-4 h-4" />
              <span>Register Project</span>
            </button>
          </div>
        </form>
      )}
    </div>
  );
};
