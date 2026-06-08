'use client';
import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Card, CardContent } from "@/components/ui/card";
import { Activity, Search, Play, Loader2 } from "lucide-react";
import { fetchSimulations, runSimulation, fetchProjects } from '@/lib/api';

export default function SimulationsPage() {
  const router = useRouter();
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [recentSims, setRecentSims] = useState([]);
  const [projects, setProjects] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState('');

  useEffect(() => {
    fetchSimulations().then(setRecentSims).catch(console.error);
    fetchProjects().then(data => {
      setProjects(data);
      if (data.length > 0) setSelectedProjectId(data[0].id);
    }).catch(console.error);
  }, []);

  const handleRun = async () => {
    if (!query || !selectedProjectId) return;
    setLoading(true);
    try {
      const res = await runSimulation({ project_id: selectedProjectId, query });
      router.push(`/simulations/${res.id}`);
    } catch (error) {
      console.error(error);
      alert('Failed to run simulation');
      setLoading(false);
    }
  };

  return (
    <main className="container mx-auto px-6 py-16 max-w-6xl flex-grow">
      <div className="flex items-center justify-between mb-12">
        <div>
          <h1 className="text-[2.5rem] leading-[1.1] font-semibold tracking-tight text-neutral-900 mb-2">
            Simulations
          </h1>
          <p className="text-lg text-neutral-500 font-light">
            Run What-If scenarios with your Multi-Agent Swarm.
          </p>
        </div>
      </div>
      
      {/* Simulation Workspace */}
      <div className="bg-white rounded-3xl border border-neutral-200/60 shadow-sm overflow-hidden mb-12">
        <div className="border-b border-neutral-100 p-6">
          <div className="mb-4">
            <select 
              value={selectedProjectId} 
              onChange={e => setSelectedProjectId(e.target.value)}
              className="px-4 py-2 bg-neutral-50 border border-neutral-200 rounded-lg text-neutral-900 focus:outline-none"
            >
              <option value="" disabled>Select Project</option>
              {projects.map((p: any) => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
            {projects.length === 0 && (
              <p className="text-sm text-amber-600 mt-2 font-medium">
                You must create a Project first before running a simulation. <Link href="/projects/new" className="underline">Create one here.</Link>
              </p>
            )}
          </div>
          <div className="flex gap-4">
            <div className="flex-1 relative">
              <Search className="w-5 h-5 text-neutral-400 absolute left-4 top-1/2 -translate-y-1/2" />
              <input 
                type="text" 
                value={query}
                onChange={e => setQuery(e.target.value)}
                placeholder="E.g., What happens if I open 2 stores in Mumbai?" 
                className="w-full pl-12 pr-4 py-3 bg-neutral-50 border-none outline-none rounded-xl text-neutral-900 placeholder-neutral-400 font-light focus:ring-2 focus:ring-neutral-200 transition-shadow disabled:opacity-50"
                onKeyDown={e => e.key === 'Enter' && handleRun()}
                disabled={projects.length === 0}
              />
            </div>
            <button 
              onClick={handleRun}
              disabled={loading || !query || !selectedProjectId}
              className="bg-neutral-900 hover:bg-neutral-800 disabled:opacity-50 disabled:cursor-not-allowed text-white px-8 rounded-xl font-medium transition-colors flex items-center gap-2"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4 fill-current" />}
              Run
            </button>
          </div>
        </div>
        {!loading && (
          <div className="p-16 flex flex-col items-center justify-center text-center bg-neutral-50/50">
            <div className="w-16 h-16 rounded-2xl bg-white border border-neutral-100 flex items-center justify-center mb-6 shadow-sm">
              <Activity className="w-8 h-8 text-neutral-300" />
            </div>
            <h3 className="text-xl font-semibold text-neutral-900 tracking-tight mb-2">Ready to Simulate</h3>
            <p className="text-neutral-500 font-light max-w-sm">
              Select a project and enter a scenario above to trigger the Multi-Agent Swarm.
            </p>
          </div>
        )}
        {loading && (
          <div className="p-16 flex flex-col items-center justify-center text-center bg-neutral-50/50">
            <Loader2 className="w-12 h-12 text-neutral-900 animate-spin mb-4" />
            <h3 className="text-xl font-semibold text-neutral-900 tracking-tight mb-2">Swarm Agents Analyzing...</h3>
            <p className="text-neutral-500 font-light max-w-sm">
              Gathering competitor data, projecting revenue, and analyzing risk.
            </p>
          </div>
        )}
      </div>

      <h3 className="text-lg font-semibold tracking-tight text-neutral-900 mb-4">Recent Results</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {recentSims.map((sim: any) => (
          <Link href={`/simulations/${sim.id}`} key={sim.id} className="block">
            <Card className="bg-white border-neutral-200/60 shadow-sm hover:shadow-md transition-all duration-300 rounded-2xl cursor-pointer h-full">
              <CardContent className="p-6">
                <div className="flex items-center gap-3 mb-3">
                  <span className="w-2 h-2 rounded-full bg-green-500"></span>
                  <span className="text-xs font-medium text-neutral-500 uppercase tracking-wider">{sim.status}</span>
                </div>
                <p className="text-neutral-900 font-medium mb-1 line-clamp-1">{sim.query}</p>
                <p className="text-sm text-neutral-500 font-light truncate">ROI: {sim.revenue_projection?.year_1_roi || 'N/A'}% • Risk: {sim.risk_score?.overall_risk || 'N/A'}</p>
              </CardContent>
            </Card>
          </Link>
        ))}
        {recentSims.length === 0 && <p className="text-neutral-500 font-light">No recent simulations found.</p>}
      </div>
    </main>
  );
}
