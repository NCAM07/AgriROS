'use client';

import React, { useState, useEffect } from 'react';
import { Header } from '@/components/Header';
import { OverviewView } from '@/components/OverviewView';
import { ResearchView } from '@/components/ResearchView';
import { PrototypesView } from '@/components/PrototypesView';
import { ResearchersView } from '@/components/ResearchersView';
import { AiSearchView } from '@/components/AiSearchView';
import { StaffPortalView } from '@/components/StaffPortalView';
import { PilotFeedbackModal } from '@/components/PilotFeedbackModal';
import { LoginPage } from '@/components/LoginPage';

import {
  Project, Prototype, ResearchPaper, Researcher,
  getProjectsFromStorage, saveProjectsToStorage,
  getPrototypesFromStorage, savePrototypesToStorage,
  getResearchFromStorage, saveResearchToStorage,
  getResearchersFromStorage, saveResearchersToStorage
} from '@/lib/api';

export interface UserSession {
  name: string;
  role: 'Management' | 'Staff';
  department?: string;
  email: string;
}

export default function Home() {
  const [user, setUser] = useState<UserSession | null>(null);
  const [isLoaded, setIsLoaded] = useState(false);

  const [activeTab, setActiveTab] = useState<string>('overview');
  const [projects, setProjects] = useState<Project[]>([]);
  const [prototypes, setPrototypes] = useState<Prototype[]>([]);
  const [researchPapers, setResearchPapers] = useState<ResearchPaper[]>([]);
  const [researchers, setResearchers] = useState<Researcher[]>([]);

  useEffect(() => {
    setProjects(getProjectsFromStorage());
    setPrototypes(getPrototypesFromStorage());
    setResearchPapers(getResearchFromStorage());
    setResearchers(getResearchersFromStorage());

    // Check if user session exists in localStorage
    const storedUser = localStorage.getItem('agriros_auth_user');
    if (storedUser) {
      try {
        const parsed: UserSession = JSON.parse(storedUser);
        setUser(parsed);
        setActiveTab(parsed.role === 'Staff' ? 'staff-portal' : 'overview');
      } catch {
        setUser(null);
      }
    } else {
      setUser(null);
    }
    setIsLoaded(true);
  }, []);

  const handleLoginSuccess = (session: UserSession) => {
    setUser(session);
    localStorage.setItem('agriros_auth_user', JSON.stringify(session));
    setActiveTab(session.role === 'Staff' ? 'staff-portal' : 'overview');
  };

  const handleLogout = () => {
    localStorage.removeItem('agriros_auth_user');
    setUser(null);
  };

  const handleAddResearch = (paper: ResearchPaper) => {
    const updated = [paper, ...researchPapers];
    setResearchPapers(updated);
    saveResearchToStorage(updated);
  };

  const handleAddResearcher = (researcher: Researcher) => {
    const updated = [researcher, ...researchers];
    setResearchers(updated);
    saveResearchersToStorage(updated);
  };

  const handleAddProject = (project: Project) => {
    const updated = [project, ...projects];
    setProjects(updated);
    saveProjectsToStorage(updated);
  };

  // Wait for client rehydration
  if (!isLoaded) {
    return <div className="min-h-screen bg-slate-100" />;
  }

  // If no logged in user, render dedicated Login Page as Default Screen
  if (!user) {
    return <LoginPage onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans">
      {/* Official NCAM Header with User Session & Sign Out */}
      <Header
        user={user}
        onLogout={handleLogout}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
      />

      {/* Main Content View - Strict Role Isolation */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6 md:p-8">
        {/* MANAGEMENT VIEWS */}
        {user.role === 'Management' && (
          <>
            {activeTab === 'overview' && (
              <OverviewView
                projects={projects}
                onNavigate={(tab) => setActiveTab(tab)}
              />
            )}

            {activeTab === 'research' && (
              <ResearchView
                papers={researchPapers}
              />
            )}

            {activeTab === 'prototypes' && (
              <PrototypesView
                prototypes={prototypes}
              />
            )}

            {activeTab === 'researchers' && (
              <ResearchersView
                researchers={researchers}
              />
            )}

            {activeTab === 'ai-search' && (
              <AiSearchView />
            )}
          </>
        )}

        {/* STAFF VIEWS */}
        {user.role === 'Staff' && (
          <>
            {activeTab === 'staff-portal' && (
              <StaffPortalView
                onAddResearch={handleAddResearch}
                onAddResearcher={handleAddResearcher}
                onAddProject={handleAddProject}
              />
            )}

            {activeTab === 'research' && (
              <ResearchView
                papers={researchPapers}
              />
            )}

            {activeTab === 'overview' && (
              <OverviewView
                projects={projects}
                onNavigate={(tab) => setActiveTab(tab)}
              />
            )}
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-500">
        National Centre for Agricultural Mechanization (NCAM), Ilorin
      </footer>

      {/* Floating System Support Widget */}
      <PilotFeedbackModal currentPage={activeTab} />
    </div>
  );
}
