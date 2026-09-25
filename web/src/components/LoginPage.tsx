'use client';

import React, { useState } from 'react';
import { ShieldCheck, UserCheck, ArrowRight, Lock, Building2, AlertCircle } from 'lucide-react';
import { UserSession } from '@/app/page';

interface LoginPageProps {
  onLoginSuccess: (user: UserSession) => void;
}

export const LoginPage: React.FC<LoginPageProps> = ({ onLoginSuccess }) => {
  const [selectedRole, setSelectedRole] = useState<'Management' | 'Staff'>('Management');
  const [department, setDepartment] = useState<'FPM' | 'ESS'>('FPM');
  const [email, setEmail] = useState('');
  const [passcode, setPasscode] = useState('');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);

    const enteredEmail = email.trim();
    const enteredPass = passcode.trim();

    if (!enteredEmail || !enteredEmail.includes('@')) {
      setErrorMsg('Please enter a valid official NCAM email address.');
      return;
    }

    if (selectedRole === 'Management') {
      if (enteredPass && enteredPass !== 'NCAM-EXEC-2026' && enteredPass !== 'admin') {
        setErrorMsg('Invalid Executive Passcode Key.');
        return;
      }
      onLoginSuccess({
        name: 'Dr. Abubakar Musa (Deputy Director)',
        role: 'Management',
        email: enteredEmail || 'a.musa@ncam.gov.ng'
      });
    } else {
      if (enteredPass && enteredPass !== 'NCAM-STAFF-2026' && enteredPass !== 'staff') {
        setErrorMsg('Invalid Department Staff Access Key.');
        return;
      }
      onLoginSuccess({
        name: department === 'FPM' ? 'Engr. Yusuf Abdullahi (FPM Data Officer)' : 'Dr. Kemi Ojo (ESS HOD)',
        role: 'Staff',
        department: department,
        email: enteredEmail || (department === 'FPM' ? 'y.abdullahi@ncam.gov.ng' : 'k.ojo@ncam.gov.ng')
      });
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col justify-between items-center p-4 sm:p-6 animate-fadeIn">
      <div className="w-full max-w-md my-auto space-y-6">
        {/* Top Institutional Branding */}
        <div className="text-center space-y-3">
          <div className="w-20 h-20 bg-white rounded-2xl p-2.5 mx-auto shadow-md border border-slate-200 flex items-center justify-center">
            <img src="/ncam-logo.png" alt="NCAM Official Logo" className="h-16 w-auto object-contain" />
          </div>
          <div>
            <h1 className="text-lg font-extrabold text-slate-900 tracking-tight leading-snug">
              National Centre for Agricultural Mechanization
            </h1>
            <p className="text-xs text-emerald-800 font-bold mt-0.5">
              AgriROS Research Intelligence System
            </p>
          </div>
        </div>

        {/* Clean Portal Selection Card */}
        <div className="bg-white rounded-2xl border border-slate-200 shadow-xl p-6 sm:p-8 space-y-6">
          <div className="border-b border-slate-200 pb-3 text-center">
            <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">System Portal Authentication</h2>
            <p className="text-xs text-slate-500 mt-0.5">Select system access level to authenticate</p>
          </div>

          {/* Distinct System Selectors */}
          <div className="grid grid-cols-2 gap-3">
            <button
              type="button"
              onClick={() => setSelectedRole('Management')}
              className={`p-3.5 rounded-xl border text-left transition-all ${
                selectedRole === 'Management'
                  ? 'border-emerald-600 bg-emerald-50 text-emerald-950 font-bold shadow-sm ring-1 ring-emerald-600'
                  : 'border-slate-200 bg-slate-50 text-slate-600 hover:border-slate-300'
              }`}
            >
              <ShieldCheck className={`w-5 h-5 mb-1.5 ${selectedRole === 'Management' ? 'text-emerald-700' : 'text-slate-400'}`} />
              <div className="text-xs font-bold">Executive Portal</div>
              <div className="text-[10px] text-slate-500 font-normal leading-tight mt-0.5">Leadership Telemetry & AI Query</div>
            </button>

            <button
              type="button"
              onClick={() => setSelectedRole('Staff')}
              className={`p-3.5 rounded-xl border text-left transition-all ${
                selectedRole === 'Staff'
                  ? 'border-emerald-600 bg-emerald-50 text-emerald-950 font-bold shadow-sm ring-1 ring-emerald-600'
                  : 'border-slate-200 bg-slate-50 text-slate-600 hover:border-slate-300'
              }`}
            >
              <UserCheck className={`w-5 h-5 mb-1.5 ${selectedRole === 'Staff' ? 'text-emerald-700' : 'text-slate-400'}`} />
              <div className="text-xs font-bold">Department Staff</div>
              <div className="text-[10px] text-slate-500 font-normal leading-tight mt-0.5">Data Entry & Faculty Registration</div>
            </button>
          </div>

          {errorMsg && (
            <div className="p-3 bg-rose-50 border border-rose-200 text-rose-800 rounded-xl text-xs font-medium flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
              <span>{errorMsg}</span>
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-4 text-xs">
            {selectedRole === 'Staff' && (
              <div>
                <label className="block text-slate-700 font-semibold mb-1">Select Department</label>
                <select
                  value={department}
                  onChange={(e) => setDepartment(e.target.value as 'FPM' | 'ESS')}
                  className="w-full p-2.5 rounded-lg border border-slate-300 text-slate-900 bg-slate-50 focus:outline-none focus:border-emerald-600 font-semibold"
                >
                  <option value="FPM">Farm Power & Machinery (FPM)</option>
                  <option value="ESS">Engineering Support Services (ESS)</option>
                </select>
              </div>
            )}

            <div>
              <label className="block text-slate-700 font-semibold mb-1">Official NCAM Email (@ncam.gov.ng)</label>
              <input
                type="email"
                required
                placeholder={selectedRole === 'Management' ? 'a.musa@ncam.gov.ng' : (department === 'FPM' ? 'y.abdullahi@ncam.gov.ng' : 'k.ojo@ncam.gov.ng')}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full p-2.5 rounded-lg border border-slate-300 text-slate-900 bg-slate-50 focus:outline-none focus:border-emerald-600 placeholder-slate-400"
              />
            </div>

            <div>
              <label className="block text-slate-700 font-semibold mb-1">Access Passcode / Key</label>
              <input
                type="password"
                required
                placeholder="Enter Access Key..."
                value={passcode}
                onChange={(e) => setPasscode(e.target.value)}
                className="w-full p-2.5 rounded-lg border border-slate-300 text-slate-900 bg-slate-50 focus:outline-none focus:border-emerald-600 placeholder-slate-400"
              />
            </div>

            <button
              type="submit"
              className="w-full py-3 bg-emerald-700 hover:bg-emerald-800 text-white font-bold rounded-xl text-xs shadow-md transition-all flex items-center justify-center space-x-2"
            >
              <span>Authenticate Portal Access</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>

      <footer className="text-[11px] text-slate-500 py-4 text-center">
        National Centre for Agricultural Mechanization (NCAM), Ilorin • Federal Ministry of Agriculture
      </footer>
    </div>
  );
};
