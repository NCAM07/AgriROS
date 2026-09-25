'use client';

import React, { useState } from 'react';
import { ShieldCheck, UserCheck, Key, Lock, ArrowRight, Building2, AlertCircle, CheckCircle2 } from 'lucide-react';

interface LoginModalProps {
  onLoginSuccess: (user: { name: string; role: 'Management' | 'Staff'; department?: string; email: string }) => void;
  onCancel?: () => void;
}

export const LoginModal: React.FC<LoginModalProps> = ({ onLoginSuccess, onCancel }) => {
  const [selectedRole, setSelectedRole] = useState<'Management' | 'Staff'>('Management');
  const [department, setDepartment] = useState<'FPM' | 'ESS'>('FPM');
  const [email, setEmail] = useState('');
  const [passcode, setPasscode] = useState('');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);

    if (selectedRole === 'Management') {
      if (passcode && passcode !== 'NCAM-EXEC-2026' && passcode !== 'admin') {
        setErrorMsg('Invalid Executive Key. Official credential: NCAM-EXEC-2026 (or click Executive Management below).');
        return;
      }
      onLoginSuccess({
        name: 'Dr. Abubakar Musa (Deputy Director)',
        role: 'Management',
        email: email || 'a.musa@ncam.gov.ng'
      });
    } else {
      if (passcode && passcode !== 'NCAM-STAFF-2026' && passcode !== 'staff') {
        setErrorMsg('Invalid Staff Access Key. Official credential: NCAM-STAFF-2026 (or click Department Staff below).');
        return;
      }
      onLoginSuccess({
        name: department === 'FPM' ? 'Engr. Yusuf Abdullahi (FPM Data Officer)' : 'Dr. Kemi Ojo (ESS HOD)',
        role: 'Staff',
        department: department,
        email: email || (department === 'FPM' ? 'y.abdullahi@ncam.gov.ng' : 'k.ojo@ncam.gov.ng')
      });
    }
  };

  const handleQuickLogin = (role: 'Management' | 'Staff', dept: 'FPM' | 'ESS' = 'FPM') => {
    if (role === 'Management') {
      onLoginSuccess({
        name: 'Dr. Abubakar Musa (Deputy Director)',
        role: 'Management',
        email: 'a.musa@ncam.gov.ng'
      });
    } else {
      onLoginSuccess({
        name: dept === 'FPM' ? 'Engr. Yusuf Abdullahi (FPM Data Officer)' : 'Dr. Kemi Ojo (ESS HOD)',
        role: 'Staff',
        department: dept,
        email: dept === 'FPM' ? 'y.abdullahi@ncam.gov.ng' : 'k.ojo@ncam.gov.ng'
      });
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/80 backdrop-blur-sm p-4 animate-fadeIn">
      <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl max-w-lg w-full overflow-hidden">
        {/* Top Header */}
        <div className="ncam-header-bg text-white p-6 text-center relative space-y-2">
          <div className="w-14 h-14 bg-white rounded-xl p-1.5 mx-auto shadow-md flex items-center justify-center">
            <img src="/ncam-logo.png" alt="NCAM Logo" className="h-11 w-auto object-contain" />
          </div>
          <h2 className="text-lg font-bold text-white tracking-tight">
            National Centre for Agricultural Mechanization
          </h2>
          <p className="text-xs text-emerald-100 font-medium">
            AgriROS System Authentication & Access Gate
          </p>
        </div>

        {/* Form Body */}
        <div className="p-6 space-y-5">
          {/* Role Selection Tabs */}
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Select Portal Access Level
            </label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setSelectedRole('Management')}
                className={`p-3 rounded-xl border text-left flex items-center space-x-3 transition-all ${
                  selectedRole === 'Management'
                    ? 'border-emerald-600 bg-emerald-50 text-emerald-900 font-bold shadow-sm'
                    : 'border-slate-200 bg-slate-50 text-slate-600 hover:border-slate-300'
                }`}
              >
                <ShieldCheck className={`w-5 h-5 ${selectedRole === 'Management' ? 'text-emerald-700' : 'text-slate-400'}`} />
                <div>
                  <div className="text-xs font-bold">Executive Management</div>
                  <div className="text-[10px] text-slate-500 font-normal">Leadership Telemetry & Reports</div>
                </div>
              </button>

              <button
                type="button"
                onClick={() => setSelectedRole('Staff')}
                className={`p-3 rounded-xl border text-left flex items-center space-x-3 transition-all ${
                  selectedRole === 'Staff'
                    ? 'border-emerald-600 bg-emerald-50 text-emerald-900 font-bold shadow-sm'
                    : 'border-slate-200 bg-slate-50 text-slate-600 hover:border-slate-300'
                }`}
              >
                <UserCheck className={`w-5 h-5 ${selectedRole === 'Staff' ? 'text-emerald-700' : 'text-slate-400'}`} />
                <div>
                  <div className="text-xs font-bold">Department Data Officer</div>
                  <div className="text-[10px] text-slate-500 font-normal">Research & Staff Registration</div>
                </div>
              </button>
            </div>
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
                placeholder="Enter Access Passcode..."
                value={passcode}
                onChange={(e) => setPasscode(e.target.value)}
                className="w-full p-2.5 rounded-lg border border-slate-300 text-slate-900 bg-slate-50 focus:outline-none focus:border-emerald-600 placeholder-slate-400"
              />
            </div>

            <button
              type="submit"
              className="w-full py-3 bg-emerald-700 hover:bg-emerald-800 text-white font-bold rounded-xl text-xs shadow-md transition-all flex items-center justify-center space-x-2"
            >
              <span>Authenticate System Access</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          {/* Institutional Credentials Access Buttons */}
          <div className="pt-3 border-t border-slate-200 space-y-2">
            <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider block text-center">
              Official Institutional Accounts (Click to Select)
            </span>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <button
                type="button"
                onClick={() => handleQuickLogin('Management')}
                className="px-3 py-2 bg-slate-100 hover:bg-emerald-50 text-slate-700 hover:text-emerald-900 font-semibold rounded-lg border border-slate-200 transition-colors text-left flex items-center justify-between"
              >
                <span>Executive Management</span>
                <ArrowRight className="w-3 h-3 text-emerald-700" />
              </button>
              <button
                type="button"
                onClick={() => handleQuickLogin('Staff', 'FPM')}
                className="px-3 py-2 bg-slate-100 hover:bg-emerald-50 text-slate-700 hover:text-emerald-900 font-semibold rounded-lg border border-slate-200 transition-colors text-left flex items-center justify-between"
              >
                <span>FPM Data Officer</span>
                <ArrowRight className="w-3 h-3 text-emerald-700" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
