const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

export const fetchProjects = async () => {
  const res = await fetch(`${API_BASE_URL}/projects`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch projects');
  return res.json();
};

export const createProject = async (data: { name: string; budget: number }) => {
  const res = await fetch(`${API_BASE_URL}/projects`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Failed to create project');
  return res.json();
};

export const fetchSimulations = async () => {
  const res = await fetch(`${API_BASE_URL}/simulations`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch simulations');
  return res.json();
};

export const fetchSimulationById = async (id: string) => {
  const res = await fetch(`${API_BASE_URL}/simulations/${id}`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch simulation');
  return res.json();
};

export const runSimulation = async (data: { project_id: string; query: string }) => {
  const res = await fetch(`${API_BASE_URL}/simulations/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Failed to run simulation');
  return res.json();
};
