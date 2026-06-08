import React from 'react';
import Link from 'next/link';
import { Card, CardContent } from "@/components/ui/card";
import { MapPin, TrendingUp, AlertTriangle, Briefcase, Activity, ArrowRight, ChevronRight } from "lucide-react";

export default function Dashboard() {
  return (
    <main className="container mx-auto px-6 py-16 max-w-6xl flex-grow">
      <header className="mb-16 max-w-2xl">
        <h1 className="text-[2.75rem] leading-[1.1] font-semibold tracking-tight text-neutral-900 mb-4">
          Intelligence for your next expansion.
        </h1>
        <p className="text-xl text-neutral-500 leading-relaxed font-light">
          Monitor markets, run complex simulations, and execute growth strategies with absolute clarity.
        </p>
      </header>

      {/* Top KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-16">
        {[
          { label: "Active Plans", value: "12", icon: Briefcase },
          { label: "Locations Analyzed", value: "847", icon: MapPin },
          { label: "Projected ROI", value: "24.5%", icon: TrendingUp },
          { label: "Market Alerts", value: "3", icon: AlertTriangle },
        ].map((kpi, idx) => (
          <Card key={idx} className="bg-white border-neutral-200/60 shadow-sm hover:shadow-md transition-all duration-300 rounded-2xl group">
            <CardContent className="p-6">
              <div className="flex justify-between items-start mb-4">
                <div className="p-2 rounded-lg bg-neutral-100 text-neutral-600 group-hover:bg-neutral-900 group-hover:text-white transition-colors duration-300">
                  <kpi.icon className="w-5 h-5" />
                </div>
              </div>
              <div>
                <p className="text-3xl font-semibold tracking-tight text-neutral-900 mb-1">{kpi.value}</p>
                <p className="text-sm font-medium text-neutral-500">{kpi.label}</p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Simulation Studio Teaser */}
        <div className="col-span-1 lg:col-span-2 relative bg-white rounded-3xl border border-neutral-200/60 shadow-sm overflow-hidden group hover:shadow-lg transition-all duration-500">
          <div className="absolute top-0 right-0 p-8 opacity-5">
            <Activity className="w-64 h-64" />
          </div>
          <div className="relative z-10 p-10 h-full flex flex-col justify-between">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-neutral-100 text-neutral-600 text-xs font-medium mb-6">
                <Activity className="w-3 h-3" />
                Simulation Engine
              </div>
              <h2 className="text-3xl font-semibold tracking-tight text-neutral-900 mb-4 max-w-md">
                What-If Expansion Studio
              </h2>
              <p className="text-neutral-500 text-lg mb-8 max-w-md leading-relaxed font-light">
                Simulate the impact of opening 3 stores in Delhi and closing 1 in Noida. Get projected revenue, risk analysis, and growth curves instantly.
              </p>
            </div>
            <div className="flex gap-4 items-center">
              <Link href="/simulations" className="inline-flex items-center justify-center bg-neutral-900 hover:bg-neutral-800 text-white rounded-full px-6 h-10 font-medium transition-colors">
                Run Simulation
              </Link>
              <Link href="/simulations" className="inline-flex items-center gap-1 text-sm font-medium text-neutral-500 hover:text-neutral-900 transition-colors">
                View past results <ChevronRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>

        {/* Active Agents Status */}
        <div className="bg-white rounded-3xl border border-neutral-200/60 shadow-sm p-8">
          <h3 className="text-lg font-semibold tracking-tight text-neutral-900 mb-6">Swarm Intelligence</h3>
          <div className="space-y-6">
            {[
              { name: "Market Intelligence", status: "Active", dot: "bg-green-500" },
              { name: "Competitor Radar", status: "Active", dot: "bg-green-500" },
              { name: "Revenue Forecaster", status: "Calculating", dot: "bg-amber-400 animate-pulse" },
              { name: "Risk Assessor", status: "Idle", dot: "bg-neutral-300" },
            ].map((agent, i) => (
              <div key={i} className="group flex items-center justify-between">
                <span className="text-sm font-medium text-neutral-600 group-hover:text-neutral-900 transition-colors">{agent.name}</span>
                <div className="flex items-center gap-3">
                  <span className="text-xs text-neutral-400 font-medium">{agent.status}</span>
                  <span className={`w-2 h-2 rounded-full ${agent.dot}`}></span>
                </div>
              </div>
            ))}
          </div>
          
          <div className="mt-8 pt-6 border-t border-neutral-100">
             <Link href="#" className="inline-flex items-center gap-1 text-sm font-medium text-neutral-900 hover:text-neutral-600 transition-colors">
                System Settings <ArrowRight className="w-4 h-4" />
              </Link>
          </div>
        </div>
        
      </div>
    </main>
  );
}
