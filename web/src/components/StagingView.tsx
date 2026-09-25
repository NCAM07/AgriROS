'use client';

import React, { useState } from 'react';
import { FileCheck, Upload, FileText, CheckCircle2, XCircle, Sparkles, ArrowRight } from 'lucide-react';

export const StagingView: React.FC = () => {
  const [stagedDocs, setStagedDocs] = useState([
    {
      id: 1,
      fileName: "NCAM_Solar_Pump_Field_Evaluation_2024.pdf",
      extractedTitle: "Field Performance & Efficiency Logging of Solar Drip Rig in Kwara Soil",
      leadResearcher: "Engr. Fatima Usman",
      supervisor: "Dr. Suleiman Bello",
      funding: "World Bank Agri-Tech Fund",
      journal: "African Journal of Renewable Energy & Agriculture",
      status: "Pending Confirmation",
      uploadDate: "2024-09-20"
    },
    {
      id: 2,
      fileName: "Cassava_Harvester_Stress_Metallurgy_Report.docx",
      extractedTitle: "Sub-Surface Drag Stress Analysis for Tractor Cassava Harvester Blade",
      leadResearcher: "Engr. Chukwuemeka Obi",
      supervisor: "Dr. Kemi Ojo",
      funding: "NCAM Internal Allocation",
      journal: "NCAM Technical Bulletin Vol. 14",
      status: "Pending Confirmation",
      uploadDate: "2024-09-22"
    }
  ]);

  const [activeTab, setActiveTab] = useState<'pending' | 'upload'>('pending');
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [extracting, setExtracting] = useState(false);

  const handleConfirm = (id: number) => {
    setStagedDocs(stagedDocs.map(d => d.id === id ? { ...d, status: 'Confirmed & Database Published' } : d));
  };

  const handleReject = (id: number) => {
    setStagedDocs(stagedDocs.filter(d => d.id !== id));
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setUploadFile(file);
      setExtracting(true);

      setTimeout(() => {
        const newStaged = {
          id: Date.now(),
          fileName: file.name,
          extractedTitle: `Extracted Research: ${file.name.replace(/\.[^/.]+$/, "")}`,
          leadResearcher: "Engr. Yusuf Abdullahi",
          supervisor: "Dr. Abubakar Musa",
          funding: "FMARD Grant",
          journal: "Journal of Agricultural Engineering",
          status: "Pending Confirmation",
          uploadDate: new Date().toISOString().split('T')[0]
        };

        setStagedDocs([newStaged, ...stagedDocs]);
        setExtracting(false);
        setUploadFile(null);
        setActiveTab('pending');
      }, 2000);
    }
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Header */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-extrabold text-white flex items-center gap-2">
            <FileCheck className="w-6 h-6 text-emerald-400" /> Document Extraction Staging Hub
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            AI auto-extracts project titles, objectives, researchers, and findings from uploaded PDF/Word documents into staging for review before database publication.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => setActiveTab('pending')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              activeTab === 'pending'
                ? 'bg-emerald-600 text-slate-950 shadow-md'
                : 'bg-slate-900 text-slate-400 hover:text-white'
            }`}
          >
            Pending Review ({stagedDocs.filter(d => d.status.includes('Pending')).length})
          </button>
          <button
            onClick={() => setActiveTab('upload')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              activeTab === 'upload'
                ? 'bg-emerald-600 text-slate-950 shadow-md'
                : 'bg-slate-900 text-slate-400 hover:text-white'
            }`}
          >
            Upload Document
          </button>
        </div>
      </div>

      {activeTab === 'upload' ? (
        <div className="glass-panel p-10 rounded-2xl border border-dashed border-emerald-500/40 text-center space-y-4 max-w-xl mx-auto">
          <div className="w-16 h-16 bg-emerald-500/10 text-emerald-400 rounded-full flex items-center justify-center mx-auto border border-emerald-500/30">
            <Upload className="w-8 h-8" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">Upload Research Document or Report</h3>
            <p className="text-xs text-slate-400 mt-1">Supports PDF or DOCX format (Max 25MB)</p>
          </div>

          <label className="inline-flex items-center justify-center px-5 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold text-xs cursor-pointer shadow-lg transition-all">
            <span>{extracting ? 'AI Extracting Metadata...' : 'Browse Computer Files'}</span>
            <input type="file" accept=".pdf,.docx,.doc" onChange={handleFileUpload} disabled={extracting} className="hidden" />
          </label>
        </div>
      ) : (
        <div className="space-y-4">
          {stagedDocs.map((doc) => (
            <div key={doc.id} className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
              <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-slate-800 pb-3 gap-2">
                <div className="flex items-center space-x-2.5">
                  <FileText className="w-5 h-5 text-emerald-400" />
                  <div>
                    <span className="text-xs font-bold text-slate-200">{doc.fileName}</span>
                    <span className="text-[10px] text-slate-500 block">Uploaded {doc.uploadDate}</span>
                  </div>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                  doc.status.includes('Confirmed')
                    ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                    : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                }`}>
                  {doc.status}
                </span>
              </div>

              {/* Extracted Card */}
              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-3 text-xs">
                <div>
                  <span className="text-[10px] font-bold text-emerald-400 block uppercase">Extracted Research Title</span>
                  <h4 className="text-sm font-bold text-white mt-0.5">{doc.extractedTitle}</h4>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  <div>
                    <span className="text-[10px] text-slate-500 font-bold block">LEAD RESEARCHER</span>
                    <span className="text-slate-300 font-medium">{doc.leadResearcher}</span>
                  </div>
                  <div>
                    <span className="text-[10px] text-slate-500 font-bold block">SUPERVISOR</span>
                    <span className="text-slate-300">{doc.supervisor}</span>
                  </div>
                  <div>
                    <span className="text-[10px] text-slate-500 font-bold block">TARGET JOURNAL</span>
                    <span className="text-slate-300">{doc.journal}</span>
                  </div>
                </div>
              </div>

              {doc.status.includes('Pending') && (
                <div className="flex items-center justify-end space-x-3 pt-2">
                  <button
                    onClick={() => handleReject(doc.id)}
                    className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-rose-400 font-semibold text-xs border border-rose-500/20 flex items-center gap-1.5"
                  >
                    <XCircle className="w-4 h-4" />
                    <span>Reject Extraction</span>
                  </button>
                  <button
                    onClick={() => handleConfirm(doc.id)}
                    className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-extrabold text-xs shadow-md flex items-center gap-1.5"
                  >
                    <CheckCircle2 className="w-4 h-4" />
                    <span>Confirm & Publish to Database</span>
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
