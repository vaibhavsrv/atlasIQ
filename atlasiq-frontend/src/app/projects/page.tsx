import React from 'react';
import Link from 'next/link';
import { Card, CardContent } from "@/components/ui/card";
import { Folder, Plus } from "lucide-react";
import { fetchProjects } from '@/lib/api';

export default async function ProjectsPage() {
  const projects = await fetchProjects().catch(() => []);

  return (
    <main className="container mx-auto px-6 py-16 max-w-6xl flex-grow">
      <div className="flex items-center justify-between mb-12">
        <div>
          <h1 className="text-[2.5rem] leading-[1.1] font-semibold tracking-tight text-neutral-900 mb-2">
            Your Projects
          </h1>
          <p className="text-lg text-neutral-500 font-light">
            Manage your active expansion plans and view historical strategies.
          </p>
        </div>
        <Link href="/projects/new" className="inline-flex items-center gap-2 bg-neutral-900 hover:bg-neutral-800 text-white rounded-full px-6 h-10 font-medium transition-all shadow-sm">
          <Plus className="w-4 h-4" />
          New Project
        </Link>
      </div>
      
      {/* Project grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {projects.map((p: any) => (
          <Card key={p.id} className="bg-white border-neutral-200/60 shadow-sm hover:shadow-md transition-all duration-300 rounded-2xl group cursor-pointer">
            <CardContent className="p-6">
              <div className="w-10 h-10 rounded-lg bg-neutral-100 text-neutral-600 group-hover:bg-neutral-900 group-hover:text-white transition-colors duration-300 flex items-center justify-center mb-6">
                <Folder className="w-5 h-5" />
              </div>
              <h3 className="text-xl font-semibold text-neutral-900 tracking-tight mb-2">{p.name}</h3>
              <p className="text-sm text-neutral-500 font-light mb-4">Budget: ${p.budget.toLocaleString()}</p>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-green-50 text-green-700 text-xs font-medium capitalize">
                {p.status}
              </div>
            </CardContent>
          </Card>
        ))}
        {projects.length === 0 && (
          <div className="col-span-3 text-center py-12 text-neutral-500 font-light">
            No projects found. Create one to get started!
          </div>
        )}
      </div>
    </main>
  );
}
