'use client';
import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { Card, CardContent } from "@/components/ui/card";
import { ArrowLeft, TrendingUp, AlertTriangle, MapPin, Download, Loader2 } from "lucide-react";
import { fetchSimulationById } from '@/lib/api';

export default function SimulationDetails() {
  const { id } = useParams();
  const [sim, setSim] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      fetchSimulationById(id as string)
        .then(setSim)
        .catch(console.error)
        .finally(() => setLoading(false));
    }
  }, [id]);

  const handleExport = () => {
    window.open(`http://localhost:8000/api/v1/simulations/${id}/export`, '_blank');
  };

  if (loading) {
    return <div className="p-20 text-center"><Loader2 className="w-8 h-8 animate-spin mx-auto" /></div>;
  }

  if (!sim) {
    return <div className="p-20 text-center">Simulation not found.</div>;
  }

  return (
    <main className="container mx-auto px-6 py-10 max-w-5xl flex-grow">
      {/* Back navigation */}
      <Link href="/simulations" className="inline-flex items-center gap-2 text-sm font-medium text-neutral-500 hover:text-neutral-900 transition-colors mb-8">
        <ArrowLeft className="w-4 h-4" />
        Back to Simulations
      </Link>

      {/* Header */}
      <div className="flex items-start justify-between mb-12">
        <div>
          <div className="flex items-center gap-3 mb-4">
            <span className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.4)]"></span>
            <span className="text-xs font-medium text-neutral-500 uppercase tracking-wider">Simulation Completed</span>
          </div>
          <h1 className="text-[2.5rem] leading-[1.1] font-semibold tracking-tight text-neutral-900 mb-4 max-w-2xl capitalize">
            {sim.query}
          </h1>
        </div>
        <button 
          onClick={handleExport}
          className="inline-flex items-center gap-2 bg-white border border-neutral-200/60 hover:bg-neutral-50 text-neutral-900 rounded-full px-5 h-10 text-sm font-medium transition-all shadow-sm"
        >
          <Download className="w-4 h-4" />
          Export Report
        </button>
      </div>

      {/* Projected Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <Card className="bg-white border-neutral-200/60 shadow-sm rounded-2xl">
          <CardContent className="p-6">
            <div className="w-10 h-10 rounded-lg bg-green-50 flex items-center justify-center mb-4">
              <TrendingUp className="w-5 h-5 text-green-600" />
            </div>
            <p className="text-sm font-medium text-neutral-500 mb-1">Projected ROI (Year 1)</p>
            <p className="text-3xl font-semibold tracking-tight text-neutral-900">{sim.revenue_projection?.year_1_roi || 'N/A'}%</p>
          </CardContent>
        </Card>

        <Card className="bg-white border-neutral-200/60 shadow-sm rounded-2xl">
          <CardContent className="p-6">
            <div className="w-10 h-10 rounded-lg bg-blue-50 flex items-center justify-center mb-4">
              <MapPin className="w-5 h-5 text-blue-600" />
            </div>
            <p className="text-sm font-medium text-neutral-500 mb-1">Payback Period</p>
            <p className="text-3xl font-semibold tracking-tight text-neutral-900">{sim.revenue_projection?.payback_months || 'N/A'} Months</p>
          </CardContent>
        </Card>

        <Card className="bg-white border-neutral-200/60 shadow-sm rounded-2xl">
          <CardContent className="p-6">
            <div className="w-10 h-10 rounded-lg bg-amber-50 flex items-center justify-center mb-4">
              <AlertTriangle className="w-5 h-5 text-amber-600" />
            </div>
            <p className="text-sm font-medium text-neutral-500 mb-1">Calculated Risk Score</p>
            <p className="text-3xl font-semibold tracking-tight text-neutral-900 capitalize">{sim.risk_score?.overall_risk || 'N/A'}</p>
          </CardContent>
        </Card>
      </div>

      {/* AI Strategy Summary */}
      <div className="bg-white rounded-3xl border border-neutral-200/60 shadow-sm overflow-hidden">
        <div className="border-b border-neutral-100 p-6 bg-neutral-50/50">
          <h3 className="font-semibold text-neutral-900">Strategy Agent Recommendation</h3>
        </div>
        <div className="p-8">
          <p className="text-neutral-700 leading-relaxed font-light mb-6">
            {sim.recommendation}
          </p>
        </div>
      </div>
    </main>
  );
}
