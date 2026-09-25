import {
  Project, Prototype, Researcher, Milestone, ResearchPaper, PilotFeedback,
  INITIAL_PROJECTS, INITIAL_PROTOTYPES, INITIAL_RESEARCHERS, INITIAL_MILESTONES, INITIAL_RESEARCH_PAPERS
} from './data';

export type { Project, Prototype, Researcher, Milestone, ResearchPaper, PilotFeedback };

const FASTAPI_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Helper to check if backend is reachable
export async function checkBackendHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${FASTAPI_URL}/`, { cache: 'no-store' });
    if (!res.ok) return false;
    const data = await res.json();
    return data.status === 'running';
  } catch {
    return false;
  }
}

// Local Storage Handlers for client-side reactivity during pilot test
export function getProjectsFromStorage(): Project[] {
  if (typeof window === 'undefined') return INITIAL_PROJECTS;
  const stored = localStorage.getItem('agriros_projects');
  if (!stored) {
    localStorage.setItem('agriros_projects', JSON.stringify(INITIAL_PROJECTS));
    return INITIAL_PROJECTS;
  }
  try {
    return JSON.parse(stored);
  } catch {
    return INITIAL_PROJECTS;
  }
}

export function saveProjectsToStorage(projects: Project[]) {
  if (typeof window !== 'undefined') {
    localStorage.setItem('agriros_projects', JSON.stringify(projects));
  }
}

export function getPrototypesFromStorage(): Prototype[] {
  if (typeof window === 'undefined') return INITIAL_PROTOTYPES;
  const stored = localStorage.getItem('agriros_prototypes');
  if (!stored) {
    localStorage.setItem('agriros_prototypes', JSON.stringify(INITIAL_PROTOTYPES));
    return INITIAL_PROTOTYPES;
  }
  try {
    return JSON.parse(stored);
  } catch {
    return INITIAL_PROTOTYPES;
  }
}

export function savePrototypesToStorage(prototypes: Prototype[]) {
  if (typeof window !== 'undefined') {
    localStorage.setItem('agriros_prototypes', JSON.stringify(prototypes));
  }
}

export function getResearchFromStorage(): ResearchPaper[] {
  if (typeof window === 'undefined') return INITIAL_RESEARCH_PAPERS;
  const stored = localStorage.getItem('agriros_research_papers');
  if (!stored) {
    localStorage.setItem('agriros_research_papers', JSON.stringify(INITIAL_RESEARCH_PAPERS));
    return INITIAL_RESEARCH_PAPERS;
  }
  try {
    return JSON.parse(stored);
  } catch {
    return INITIAL_RESEARCH_PAPERS;
  }
}

export function saveResearchToStorage(papers: ResearchPaper[]) {
  if (typeof window !== 'undefined') {
    localStorage.setItem('agriros_research_papers', JSON.stringify(papers));
  }
}

export function getResearchersFromStorage(): Researcher[] {
  if (typeof window === 'undefined') return INITIAL_RESEARCHERS;
  const stored = localStorage.getItem('agriros_researchers');
  if (!stored) {
    localStorage.setItem('agriros_researchers', JSON.stringify(INITIAL_RESEARCHERS));
    return INITIAL_RESEARCHERS;
  }
  try {
    return JSON.parse(stored);
  } catch {
    return INITIAL_RESEARCHERS;
  }
}

export function saveResearchersToStorage(researchers: Researcher[]) {
  if (typeof window !== 'undefined') {
    localStorage.setItem('agriros_researchers', JSON.stringify(researchers));
  }
}

export function getFeedbackFromStorage(): PilotFeedback[] {
  if (typeof window === 'undefined') return [];
  const stored = localStorage.getItem('agriros_pilot_feedback');
  if (!stored) return [];
  try {
    return JSON.parse(stored);
  } catch {
    return [];
  }
}

export function submitPilotFeedback(feedback: Omit<PilotFeedback, 'id' | 'timestamp' | 'status'>): PilotFeedback {
  const current = getFeedbackFromStorage();
  const newItem: PilotFeedback = {
    ...feedback,
    id: `FB-${Date.now()}`,
    timestamp: new Date().toISOString(),
    status: 'New'
  };
  const updated = [newItem, ...current];
  if (typeof window !== 'undefined') {
    localStorage.setItem('agriros_pilot_feedback', JSON.stringify(updated));
  }
  return newItem;
}

// AI Query Processor
export async function queryAiSearch(userQuery: string): Promise<{
  answer: string;
  matchedProjects: Project[];
  matchedPrototypes: Prototype[];
  confidenceScore: number;
}> {
  const queryLower = userQuery.toLowerCase();
  const projects = getProjectsFromStorage();
  const prototypes = getPrototypesFromStorage();

  const matchedProjects = projects.filter(p =>
    p.title.toLowerCase().includes(queryLower) ||
    p.keywords.toLowerCase().includes(queryLower) ||
    p.status.toLowerCase().includes(queryLower) ||
    p.lead_researcher_name.toLowerCase().includes(queryLower) ||
    p.summary?.toLowerCase().includes(queryLower)
  );

  const matchedPrototypes = prototypes.filter(pr =>
    pr.name.toLowerCase().includes(queryLower) ||
    pr.target_crop.toLowerCase().includes(queryLower) ||
    pr.development_stage.toLowerCase().includes(queryLower) ||
    pr.description.toLowerCase().includes(queryLower)
  );

  let answer = "";
  if (queryLower.includes("behind schedule") || queryLower.includes("delayed")) {
    const delayed = projects.filter(p => p.status === 'Behind Schedule');
    if (delayed.length > 0) {
      answer = `Found **${delayed.length} project(s) behind schedule**. Highlighting **${delayed[0].title}** led by ${delayed[0].lead_researcher_name} in ${delayed[0].department_code || 'ESS'}. The primary delay relates to blade metallurgy stress testing under heavy soil drag.`;
    } else {
      answer = "Good news! Currently, no projects are flagged as behind schedule.";
    }
  } else if (queryLower.includes("solar") || queryLower.includes("irrigation")) {
    answer = `NCAM is actively developing the **Adaptive Solar-Powered Drip & Sprinkler Irrigation Rig (Project #2)** led by Engr. Fatima Usman. Prototype **AgriFlow Solar-Hydro Sub-Rig** is undergoing field trials in Kwara state with 12,000L/hr pumping capacity.`;
  } else if (queryLower.includes("commercial") || queryLower.includes("market") || queryLower.includes("sheller")) {
    answer = `The **NCAM Sheller-Pro Mk. IV** has achieved **Commercial Deployment** stage with 48 units fabricated and 35 distributed across North-Central & North-West farming cooperatives. It delivers 96.8% threshing efficiency.`;
  } else if (matchedProjects.length > 0) {
    answer = `Identified **${matchedProjects.length} relevant research project(s)** matching your query. Leading project: **"${matchedProjects[0].title}"** under ${matchedProjects[0].supervisor_name}.`;
  } else {
    answer = `Query analyzed across NCAM database index. Formulated focus response: 5 research projects and 4 active machinery prototypes are cataloged across FPM and ESS departments.`;
  }

  return {
    answer,
    matchedProjects: matchedProjects.length > 0 ? matchedProjects : projects.slice(0, 2),
    matchedPrototypes: matchedPrototypes.length > 0 ? matchedPrototypes : prototypes.slice(0, 2),
    confidenceScore: matchedProjects.length > 0 || matchedPrototypes.length > 0 ? 0.94 : 0.78
  };
}
