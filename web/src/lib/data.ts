export interface Project {
  id: number;
  title: string;
  department_id: number;
  department_code?: string;
  status: 'Ongoing' | 'Completed' | 'Behind Schedule' | 'Commercialized' | 'Pending Evaluation';
  supervisor_name: string;
  supervisor_designation: string;
  supervisor_email: string;
  supervisor_phone: string;
  lead_researcher_name: string;
  lead_researcher_designation: string;
  start_date: string;
  expected_end_date: string;
  actual_end_date?: string | null;
  budget_allocated: number;
  budget_utilized: number;
  funding_source: string;
  keywords: string;
  machine_built: boolean;
  prototype_id?: number | null;
  objectives?: string;
  summary?: string;
  progress_pct?: number;
}

export interface Prototype {
  id: number;
  project_id: number;
  project_title?: string;
  name: string;
  description: string;
  development_stage: 'Design & Modeling' | 'Fabrication' | 'Field Testing' | 'Refinement' | 'Commercial Deployment';
  stage_start_date: string;
  units_produced: number;
  units_distributed: number;
  target_crop: string;
  target_region: string;
  efficiency_rating?: string;
  power_source?: string;
  notes?: string;
}

export interface Researcher {
  id: number;
  full_name: string;
  designation: string;
  department_code: string;
  email: string;
  phone: string;
  specialization: string;
  active_projects_count: number;
  publications_count: number;
  linkedin?: string;
}

export interface Milestone {
  id: number;
  project_id: number;
  project_title: string;
  title: string;
  description: string;
  due_date: string;
  status: 'Completed' | 'In Progress' | 'Delayed' | 'Pending';
}

export interface ResearchPaper {
  id: number;
  title: string;
  department_code: string;
  lead_researcher: string;
  research_type: string;
  status: string;
  journal_name?: string;
  publication_date?: string;
  doi_or_link?: string;
  extracted_from_doc?: boolean;
}

export interface PilotFeedback {
  id: string;
  timestamp: string;
  role: string;
  user_name: string;
  email?: string;
  page: string;
  rating: number;
  category: 'UI/Usability' | 'Data Accuracy' | 'Feature Request' | 'Bug Report' | 'General Suggestion';
  feedback_text: string;
  status: 'New' | 'Reviewed' | 'Implemented';
}

export const INITIAL_PROJECTS: Project[] = [
  {
    id: 1,
    title: "Development of Low-Cost Multi-Crop Motorized Grain Sheller",
    department_id: 1,
    department_code: "FPM",
    status: "Commercialized",
    supervisor_name: "Dr. Abubakar Musa",
    supervisor_designation: "Chief Research Officer",
    supervisor_email: "a.musa@ncam.gov.ng",
    supervisor_phone: "08012345678",
    lead_researcher_name: "Engr. Yusuf Abdullahi",
    lead_researcher_designation: "Principal Research Engineer",
    start_date: "2022-01-15",
    expected_end_date: "2023-06-30",
    actual_end_date: "2023-08-10",
    budget_allocated: 4500000,
    budget_utilized: 4200000,
    funding_source: "Federal Ministry of Agric (FMARD)",
    keywords: "maize, shelling, motorization, post-harvest",
    machine_built: true,
    prototype_id: 101,
    progress_pct: 100,
    summary: "A dual-power (petrol & electric) sheller engineered for smallholder farmers with shelling efficiency above 96.4% and threshing capacity of 850kg/hr.",
    objectives: "1. Fabricate low-cost cylinder assembly\n2. Optimize threshing speed for maize and sorghum\n3. Conduct multi-regional field validation."
  },
  {
    id: 2,
    title: "Adaptive Solar-Powered Drip & Sprinkler Irrigation Rig for Arid Zones",
    department_id: 1,
    department_code: "FPM",
    status: "Ongoing",
    supervisor_name: "Dr. Suleiman Bello",
    supervisor_designation: "Director of Research",
    supervisor_email: "s.bello@ncam.gov.ng",
    supervisor_phone: "08023456789",
    lead_researcher_name: "Engr. Fatima Usman",
    lead_researcher_designation: "Senior Agricultural Engineer",
    start_date: "2023-03-01",
    expected_end_date: "2025-04-30",
    actual_end_date: null,
    budget_allocated: 8500000,
    budget_utilized: 5200000,
    funding_source: "World Bank Agri-Tech Fund",
    keywords: "solar, drip irrigation, renewable power, water conservation",
    machine_built: true,
    prototype_id: 102,
    progress_pct: 75,
    summary: "Automated solar pumping setup equipped with soil moisture telemetry sensors to optimize water usage in dryland vegetable production.",
    objectives: "1. Design 2.5kW solar array sub-rig\n2. Integrate smart solenoid valve distribution\n3. Benchmark flow rates across Kwara & Niger state soils."
  },
  {
    id: 3,
    title: "Evaluation of Heavy-Duty Tractor Cassava Harvester & Lifter Attachment",
    department_id: 2,
    department_code: "ESS",
    status: "Behind Schedule",
    supervisor_name: "Dr. Kemi Ojo",
    supervisor_designation: "Head of Department (ESS)",
    supervisor_email: "k.ojo@ncam.gov.ng",
    supervisor_phone: "08034567890",
    lead_researcher_name: "Engr. Chukwuemeka Obi",
    lead_researcher_designation: "Senior Research Officer",
    start_date: "2022-09-01",
    expected_end_date: "2024-03-31",
    actual_end_date: null,
    budget_allocated: 6200000,
    budget_utilized: 6150000,
    funding_source: "NCAM Internal Allocation",
    keywords: "cassava, tractor implement, root harvesting, mechanized digging",
    machine_built: true,
    prototype_id: 103,
    progress_pct: 60,
    summary: "Tractor 3-point hitch cassava root digger designed to reduce tuber damage below 3.5% during mass harvesting in hard clay soils.",
    objectives: "1. Stress test blade metallurgy against hard pan soils\n2. Reduce hydraulic drag force\n3. Finalize field trial validation."
  },
  {
    id: 4,
    title: "Precision Cassava Planter Attachment for Medium Horsepower Tractors",
    department_id: 1,
    department_code: "FPM",
    status: "Ongoing",
    supervisor_name: "Dr. Abubakar Musa",
    supervisor_designation: "Chief Research Officer",
    supervisor_email: "a.musa@ncam.gov.ng",
    supervisor_phone: "08012345678",
    lead_researcher_name: "Engr. Amina Garba",
    lead_researcher_designation: "Research Engineer II",
    start_date: "2024-01-10",
    expected_end_date: "2025-11-30",
    actual_end_date: null,
    budget_allocated: 5000000,
    budget_utilized: 2100000,
    funding_source: "TETFund Special Grant",
    keywords: "cassava planter, precision planting, tractor hitch",
    machine_built: false,
    prototype_id: null,
    progress_pct: 40,
    summary: "Two-row automated cassava stem cutter and planter attachment with adjustable tilt angles for uniform stake insertion depth.",
    objectives: "1. CAD modeling of metering wheel\n2. Fabrication of stem hopper mechanism\n3. Germination trial comparison."
  },
  {
    id: 5,
    title: "Bio-Mass Fueled Flash Dryer for High-Quality Cassava Flour (HQCF)",
    department_id: 2,
    department_code: "ESS",
    status: "Pending Evaluation",
    supervisor_name: "Dr. Kemi Ojo",
    supervisor_designation: "Head of Department (ESS)",
    supervisor_email: "k.ojo@ncam.gov.ng",
    supervisor_phone: "08034567890",
    lead_researcher_name: "Engr. David Okon",
    lead_researcher_designation: "Process Systems Engineer",
    start_date: "2023-06-01",
    expected_end_date: "2024-08-31",
    actual_end_date: "2024-09-15",
    budget_allocated: 7800000,
    budget_utilized: 7400000,
    funding_source: "FMARD Processing Initiative",
    keywords: "cassava flour, flash drying, biomass heat exchanger",
    machine_built: true,
    prototype_id: 104,
    progress_pct: 95,
    summary: "Industrial continuous pneumatic dryer utilizing palm kernel shell biomass for zero-carbon high-capacity flour drying.",
    objectives: "1. Heat transfer optimization in cyclone tube\n2. Thermal efficiency test above 78%\n3. Final commercial readiness review."
  }
];

export const INITIAL_PROTOTYPES: Prototype[] = [
  {
    id: 101,
    project_id: 1,
    project_title: "Development of Low-Cost Multi-Crop Motorized Grain Sheller",
    name: "NCAM Sheller-Pro Mk. IV",
    description: "Portable multi-grain threshing unit with interchangeable sieve screens for maize, sorghum, and cowpea.",
    development_stage: "Commercial Deployment",
    stage_start_date: "2023-09-01",
    units_produced: 48,
    units_distributed: 35,
    target_crop: "Maize & Sorghum",
    target_region: "North-Central & North-West Nigeria",
    efficiency_rating: "96.8% Clean Threshing",
    power_source: "7.5 HP Lifan Engine / 5kW Electric Motor",
    notes: "Licensed to 3 local fabrication partners in Ilorin, Kano, and Markurdi."
  },
  {
    id: 102,
    project_id: 2,
    project_title: "Adaptive Solar-Powered Drip & Sprinkler Irrigation Rig for Arid Zones",
    name: "AgriFlow Solar-Hydro Sub-Rig",
    description: "Trailer-mounted mobile solar pumping array with fold-out PV modules and GSM telemetry control module.",
    development_stage: "Field Testing",
    stage_start_date: "2024-02-15",
    units_produced: 5,
    units_distributed: 3,
    target_crop: "Tomatoes, Peppers, Onions",
    target_region: "Kwara & Niger River Basin",
    efficiency_rating: "12,000 Liters/Hour @ 35m Head",
    power_source: "3.2 kW Photovoltaic Array",
    notes: "Currently under 6-month continuous field trial at NCAM Research Farm Site B."
  },
  {
    id: 103,
    project_id: 3,
    project_title: "Evaluation of Heavy-Duty Tractor Cassava Harvester & Lifter Attachment",
    name: "RootLifter 2000 Blade Unit",
    description: "Dual-blade sub-surface lifting implement with vibratory root loosening action.",
    development_stage: "Refinement",
    stage_start_date: "2024-01-10",
    units_produced: 2,
    units_distributed: 1,
    target_crop: "Cassava & Yam",
    target_region: "South-West & North-Central Belt",
    efficiency_rating: "0.45 Hectares/Hour",
    power_source: "65-90 HP Tractor PTO & Hydraulics",
    notes: "Shear pin modifications undergoing fatigue re-testing."
  },
  {
    id: 104,
    project_id: 5,
    project_title: "Bio-Mass Fueled Flash Dryer for High-Quality Cassava Flour (HQCF)",
    name: "NCAM EcoDry HQCF-500",
    description: "Compact 500kg/hr flash drying tower with integrated heat exchanger and dust cyclone collector.",
    development_stage: "Fabrication",
    stage_start_date: "2024-04-01",
    units_produced: 1,
    units_distributed: 0,
    target_crop: "Cassava Tubers",
    target_region: "Oyo & Ogun Cassava Processing Clusters",
    efficiency_rating: "Thermal Efficiency: 82%",
    power_source: "Biomass Burner + 3-Phase Blower Motor",
    notes: "Awaiting final safety certification from NCAM Quality Assurance Board."
  }
];

export const INITIAL_RESEARCHERS: Researcher[] = [
  {
    id: 1,
    full_name: "Dr. Abubakar Musa",
    designation: "Chief Research Officer / Deputy Director",
    department_code: "FPM",
    email: "a.musa@ncam.gov.ng",
    phone: "+234 801 234 5678",
    specialization: "Post-Harvest Machinery & Mechanization Policy",
    active_projects_count: 3,
    publications_count: 24,
    linkedin: "https://linkedin.com"
  },
  {
    id: 2,
    full_name: "Engr. Yusuf Abdullahi",
    designation: "Principal Research Officer",
    department_code: "FPM",
    email: "y.abdullahi@ncam.gov.ng",
    phone: "+234 802 987 6543",
    specialization: "Grain Threshing, Power Machinery & Internal Combustion Rigs",
    active_projects_count: 2,
    publications_count: 14
  },
  {
    id: 3,
    full_name: "Engr. Fatima Usman",
    designation: "Senior Research Engineer",
    department_code: "FPM",
    email: "f.usman@ncam.gov.ng",
    phone: "+234 803 111 2233",
    specialization: "Solar Irrigation Automation & Hydraulic Systems",
    active_projects_count: 2,
    publications_count: 9
  },
  {
    id: 4,
    full_name: "Dr. Kemi Ojo",
    designation: "Head of Department",
    department_code: "ESS",
    email: "k.ojo@ncam.gov.ng",
    phone: "+234 805 444 5566",
    specialization: "Agricultural Process Engineering & Renewable Thermal Drying",
    active_projects_count: 4,
    publications_count: 31
  },
  {
    id: 5,
    full_name: "Engr. Chukwuemeka Obi",
    designation: "Senior Research Officer",
    department_code: "ESS",
    email: "c.obi@ncam.gov.ng",
    phone: "+234 807 888 9900",
    specialization: "Tractor Implements, Soil Dynamics & Metallurgy",
    active_projects_count: 1,
    publications_count: 7
  }
];

export const INITIAL_MILESTONES: Milestone[] = [
  {
    id: 1,
    project_id: 2,
    project_title: "Adaptive Solar-Powered Drip Irrigation Rig",
    title: "Solar Pump & Telemetry Array Bench Testing",
    description: "Verify flow rate output under variable cloud cover simulated conditions.",
    due_date: "2024-05-15",
    status: "Completed"
  },
  {
    id: 2,
    project_id: 2,
    project_title: "Adaptive Solar-Powered Drip Irrigation Rig",
    title: "Multi-Soil Site Deployment (Kwara Dry Belt)",
    description: "Install 3 test rigs with local farmer cooperatives for real-world usage logs.",
    due_date: "2024-11-30",
    status: "In Progress"
  },
  {
    id: 3,
    project_id: 3,
    project_title: "Evaluation of Heavy-Duty Tractor Cassava Harvester",
    title: "Hydraulic PTO Drag Force Optimization",
    description: "Modify lifting arm shear pin alignment to reduce tractor engine strain.",
    due_date: "2024-04-10",
    status: "Delayed"
  },
  {
    id: 4,
    project_id: 5,
    project_title: "Bio-Mass Fueled Flash Dryer for Cassava Flour",
    title: "Biomass Burner Thermal Chamber Inspection",
    description: "Inspect refractory brick lining and flue gas emissions compliance.",
    due_date: "2024-08-01",
    status: "Completed"
  }
];

export const INITIAL_RESEARCH_PAPERS: ResearchPaper[] = [
  {
    id: 1,
    title: "Performance Optimization of Motorized Multi-Crop Grain Sheller for Smallholders in West Africa",
    department_code: "FPM",
    lead_researcher: "Engr. Yusuf Abdullahi",
    research_type: "Applied Machine Design & Experimental Validation",
    status: "Published",
    journal_name: "Journal of Agricultural Mechanization in Tropics (JAMT)",
    publication_date: "2023-11-12",
    doi_or_link: "https://doi.org/10.1016/j.ageng.2023.109283",
    extracted_from_doc: false
  },
  {
    id: 2,
    title: "Field Performance and Economic Feasibility of Mobile Solar-Powered Pumping In Sub-Saharan Drylands",
    department_code: "FPM",
    lead_researcher: "Engr. Fatima Usman",
    research_type: "Field Evaluation & Energy Balance Analysis",
    status: "Published",
    journal_name: "African Journal of Renewable Energy & Agriculture",
    publication_date: "2024-02-18",
    doi_or_link: "https://ncam.gov.ng/research/paper-10492",
    extracted_from_doc: true
  },
  {
    id: 3,
    title: "Sub-Surface Drag & Soil Shear Stress Analysis for Tractor-Drawn Cassava Root Lifter Implement",
    department_code: "ESS",
    lead_researcher: "Engr. Chukwuemeka Obi",
    research_type: "Soil Mechanics & Metallurgy Investigation",
    status: "Published",
    journal_name: "International Journal of Farm Machinery Engineering",
    publication_date: "2024-05-10",
    doi_or_link: "https://doi.org/10.1080/agri.2024.99120",
    extracted_from_doc: false
  },
  {
    id: 4,
    title: "Thermal Efficiency Benchmarking of Biomass Pneumatic Flash Dryer for High-Quality Cassava Flour",
    department_code: "ESS",
    lead_researcher: "Engr. David Okon",
    research_type: "Process Systems & Heat Transfer Optimization",
    status: "Published",
    journal_name: "Nigerian Journal of Agricultural Technology (NJAT)",
    publication_date: "2024-07-22",
    doi_or_link: "https://ncam.gov.ng/research/paper-20831",
    extracted_from_doc: true
  }
];
