'use client';

import React from 'react';
import { Wrench, MapPin, Cpu, CheckCircle2 } from 'lucide-react';
import { Prototype } from '@/lib/data';

interface PrototypesViewProps {
  prototypes: Prototype[];
}

export const PrototypesView: React.FC<PrototypesViewProps> = ({ prototypes }) => {
  return (
    <div className="space-y-6 animate-fadeIn">
      <div className="ncam-card p-6 border-l-4 border-l-emerald-600 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Wrench className="w-5 h-5 text-emerald-700" /> NCAM Machinery Prototypes & Commercialization Tracker
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Physical machinery fabricated at NCAM Ilorin workshops for Nigerian smallholder farming.
          </p>
        </div>
        <div className="text-xs text-emerald-800 font-bold bg-emerald-50 px-3 py-1.5 rounded-lg border border-emerald-200">
          {prototypes.reduce((a, b) => a + b.units_produced, 0)} Total Units Fabricated
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {prototypes.map((proto) => (
          <div key={proto.id} className="ncam-card p-6 space-y-4 flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="px-2.5 py-0.5 rounded text-[10px] font-extrabold bg-slate-100 text-slate-700 border border-slate-300">
                  Prototype ID #{proto.id}
                </span>
                <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${
                  proto.development_stage === 'Commercial Deployment'
                    ? 'ncam-badge-green'
                    : 'ncam-badge-blue'
                }`}>
                  {proto.development_stage}
                </span>
              </div>

              <div>
                <h3 className="text-base font-bold text-slate-900 leading-snug">{proto.name}</h3>
                <p className="text-xs text-slate-600 mt-1 leading-relaxed">{proto.description}</p>
              </div>
            </div>

            <div className="pt-3 border-t border-slate-200 text-xs space-y-2">
              <div className="grid grid-cols-2 gap-2 bg-slate-50 p-3 rounded-lg border border-slate-200">
                <div>
                  <span className="text-[10px] text-slate-500 font-bold block uppercase">TARGET CROP</span>
                  <span className="font-bold text-slate-900">{proto.target_crop}</span>
                </div>
                <div>
                  <span className="text-[10px] text-slate-500 font-bold block uppercase">FABRICATED UNITS</span>
                  <span className="font-bold text-emerald-700">{proto.units_produced} Units ({proto.units_distributed} Fielded)</span>
                </div>
              </div>

              <div className="flex items-center justify-between text-[11px] text-slate-500 pt-1">
                <span className="flex items-center gap-1">
                  <MapPin className="w-3.5 h-3.5 text-emerald-700" /> Zone: <strong className="text-slate-700">{proto.target_region}</strong>
                </span>
                <span className="font-semibold text-slate-700">{proto.efficiency_rating}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
