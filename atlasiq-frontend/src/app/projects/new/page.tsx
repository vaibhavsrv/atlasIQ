'use client';
import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { createProject } from '@/lib/api';
import { ArrowLeft } from "lucide-react";

export default function NewProjectPage() {
  const router = useRouter();
  const [name, setName] = useState('');
  const [budget, setBudget] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await createProject({ name, budget: parseFloat(budget) });
      router.push('/projects');
      router.refresh();
    } catch (error) {
      console.error(error);
      alert('Failed to create project');
      setLoading(false);
    }
  };

  return (
    <main className="container mx-auto px-6 py-16 max-w-3xl flex-grow">
      <Link href="/projects" className="inline-flex items-center gap-2 text-sm font-medium text-neutral-500 hover:text-neutral-900 transition-colors mb-8">
        <ArrowLeft className="w-4 h-4" /> Back to Projects
      </Link>
      <h1 className="text-3xl font-semibold tracking-tight text-neutral-900 mb-8">Create New Expansion Plan</h1>
      
      <form onSubmit={handleSubmit} className="bg-white rounded-3xl border border-neutral-200/60 shadow-sm p-8">
        <div className="mb-6">
          <label className="block text-sm font-medium text-neutral-700 mb-2">Project Name</label>
          <input 
            type="text" 
            required
            value={name}
            onChange={e => setName(e.target.value)}
            className="w-full px-4 py-3 bg-neutral-50 border border-neutral-200 rounded-xl text-neutral-900 focus:ring-2 focus:ring-neutral-900 outline-none transition-all"
            placeholder="e.g. North India Expansion Q3"
          />
        </div>
        <div className="mb-8">
          <label className="block text-sm font-medium text-neutral-700 mb-2">Estimated Budget ($)</label>
          <input 
            type="number" 
            required
            min="0"
            step="1000"
            value={budget}
            onChange={e => setBudget(e.target.value)}
            className="w-full px-4 py-3 bg-neutral-50 border border-neutral-200 rounded-xl text-neutral-900 focus:ring-2 focus:ring-neutral-900 outline-none transition-all"
            placeholder="500000"
          />
        </div>
        <button 
          type="submit" 
          disabled={loading}
          className="w-full bg-neutral-900 hover:bg-neutral-800 text-white rounded-xl py-3 font-medium transition-colors disabled:opacity-50"
        >
          {loading ? 'Creating...' : 'Create Project'}
        </button>
      </form>
    </main>
  );
}
