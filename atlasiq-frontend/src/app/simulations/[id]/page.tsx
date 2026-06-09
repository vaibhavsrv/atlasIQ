'use client';
import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { Card, CardContent } from "@/components/ui/card";
import { ArrowLeft, TrendingUp, AlertTriangle, MapPin, Download, Loader2, SlidersHorizontal } from "lucide-react";
import { fetchSimulationById, runSimulation } from '@/lib/api';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function SimulationDetails() {
  const { id } = useParams();
  const [sim, setSim] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  
  // What-If Studio State
  const [budget, setBudget] = useState(500000);
  const [recalculating, setRecalculating] = useState(false);

  useEffect(() => {
    if (id) {
      fetchSimulationById(id as string)
        .then(data => {
            setSim(data);
            // set dummy budget for what-if based on query or assume 500k
        })
        .catch(console.error)
        .finally(() => setLoading(false));
    }
  }, [id]);

  const handleExport = () => {
    window.open(`http://127.0.0.1:8000/api/v1/simulations/${id}/export`, '_blank');
  };

  const handleRecalculate = async () => {
    setRecalculating(true);
    try {
      const res = await runSimulation({ project_id: sim.project_id, query: sim.query + ` with budget ${budget}` });
      setSim(res);
    } catch (error) {
      console.error(error);
      alert('Failed to recalculate');
    }
    setRecalculating(false);
  };

  if (loading) {
    return <div className="p-20 text-center"><Loader2 className="w-8 h-8 animate-spin mx-auto" /></div>;
  }

  if (!sim) {
    return <div className="p-20 text-center">Simulation not found.</div>;
  }

  const formatCurrency = (val: number) => `$${(val / 1000).toFixed(0)}k`;

  return (
    <main className="container mx-auto px-6 py-10 max-w-6xl flex-grow">
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
          className="inline-flex items-center gap-2 bg-neutral-900 hover:bg-neutral-800 text-white rounded-full px-5 h-10 text-sm font-medium transition-all shadow-lg"
        >
          <Download className="w-4 h-4" />
          Export Report
        </button>
      </div>

      {/* Projected Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <Card className="bg-white/80 backdrop-blur-md border border-neutral-200/60 shadow-lg rounded-3xl overflow-hidden hover:scale-[1.02] transition-transform">
          <CardContent className="p-8">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-green-400 to-emerald-600 flex items-center justify-center mb-6 shadow-sm">
              <TrendingUp className="w-6 h-6 text-white" />
            </div>
            <p className="text-sm font-medium text-neutral-500 mb-2 uppercase tracking-wide">Projected ROI (Year 1)</p>
            <div className="flex items-end gap-3">
                <p className="text-5xl font-bold tracking-tight text-neutral-900">{sim.revenue_projection?.year_1_roi || 'N/A'}%</p>
                <span className="text-sm font-semibold text-green-600 bg-green-100 px-2 py-1 rounded-full mb-2">Top 10%</span>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-white/80 backdrop-blur-md border border-neutral-200/60 shadow-lg rounded-3xl overflow-hidden hover:scale-[1.02] transition-transform">
          <CardContent className="p-8">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-400 to-indigo-600 flex items-center justify-center mb-6 shadow-sm">
              <MapPin className="w-6 h-6 text-white" />
            </div>
            <p className="text-sm font-medium text-neutral-500 mb-2 uppercase tracking-wide">Payback Period</p>
            <div className="flex items-end gap-3">
                <p className="text-5xl font-bold tracking-tight text-neutral-900">{sim.revenue_projection?.payback_months || 'N/A'}</p>
                <p className="text-lg font-medium text-neutral-500 mb-1">Months</p>
                <span className="text-sm font-semibold text-blue-600 bg-blue-100 px-2 py-1 rounded-full mb-2">Excellent</span>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-white/80 backdrop-blur-md border border-neutral-200/60 shadow-lg rounded-3xl overflow-hidden hover:scale-[1.02] transition-transform">
          <CardContent className="p-8">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-amber-400 to-orange-600 flex items-center justify-center mb-6 shadow-sm">
              <AlertTriangle className="w-6 h-6 text-white" />
            </div>
            <p className="text-sm font-medium text-neutral-500 mb-2 uppercase tracking-wide">Calculated Risk Score</p>
            <div className="flex items-end gap-3">
                <p className="text-5xl font-bold tracking-tight text-neutral-900 capitalize">{sim.risk_score?.category || sim.risk_score?.overall_risk || 'N/A'}</p>
                <p className="text-lg font-medium text-neutral-500 mb-1">{sim.risk_score?.score ? `(${sim.risk_score.score}/100)` : ''}</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
        {/* Prophet Forecast Chart */}
        <div className="lg:col-span-2 bg-white rounded-3xl border border-neutral-200/60 shadow-sm p-8">
            <h3 className="text-xl font-semibold text-neutral-900 tracking-tight mb-6">36-Month Revenue Projection</h3>
            {sim.forecast_data && sim.forecast_data.length > 0 ? (
                <div className="w-full h-[400px]">
                    <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={sim.forecast_data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                            <defs>
                                <linearGradient id="colorRev" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                                </linearGradient>
                            </defs>
                            <XAxis dataKey="month" stroke="#a3a3a3" fontSize={12} tickLine={false} axisLine={false} />
                            <YAxis stroke="#a3a3a3" fontSize={12} tickLine={false} axisLine={false} tickFormatter={formatCurrency} />
                            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e5e5" />
                            <Tooltip 
                                contentStyle={{ borderRadius: '16px', border: 'none', boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)' }}
                                formatter={(value: number) => [`$${value.toLocaleString()}`, "Revenue"]}
                            />
                            <Area type="monotone" dataKey="projected_revenue" stroke="#10b981" strokeWidth={3} fillOpacity={1} fill="url(#colorRev)" />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
            ) : (
                <div className="w-full h-[400px] flex items-center justify-center text-neutral-400 bg-neutral-50 rounded-2xl">
                    No forecast data available.
                </div>
            )}
        </div>

        {/* What-If Studio */}
        <div className="bg-neutral-900 rounded-3xl border border-neutral-800 shadow-xl p-8 text-white relative overflow-hidden">
            <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-500 opacity-20 blur-[80px] rounded-full"></div>
            <div className="relative z-10">
                <div className="flex items-center gap-3 mb-6">
                    <div className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center">
                        <SlidersHorizontal className="w-5 h-5 text-indigo-400" />
                    </div>
                    <h3 className="text-xl font-semibold tracking-tight">What-If Studio</h3>
                </div>
                <p className="text-neutral-400 text-sm mb-8 font-light leading-relaxed">
                    Adjust simulation variables to see how it impacts your projected ROI and risk in real-time.
                </p>
                
                <div className="mb-8">
                    <label className="block text-sm font-medium text-neutral-300 mb-4 flex justify-between">
                        <span>Initial Capital (Budget)</span>
                        <span className="text-white">${budget.toLocaleString()}</span>
                    </label>
                    <input 
                        type="range" 
                        min="50000" 
                        max="2000000" 
                        step="50000"
                        value={budget}
                        onChange={e => setBudget(Number(e.target.value))}
                        className="w-full accent-indigo-500 h-2 bg-neutral-700 rounded-lg appearance-none cursor-pointer"
                    />
                </div>

                <div className="mb-8">
                    <label className="block text-sm font-medium text-neutral-300 mb-4 flex justify-between">
                        <span>Marketing Spend (Monthly)</span>
                        <span className="text-white">$5,000</span>
                    </label>
                    <input type="range" min="1000" max="50000" defaultValue="5000" className="w-full accent-indigo-500 h-2 bg-neutral-700 rounded-lg appearance-none cursor-not-allowed opacity-50" disabled />
                    <p className="text-xs text-neutral-500 mt-2">Available in Pro Tier</p>
                </div>

                <button 
                    onClick={handleRecalculate}
                    disabled={recalculating}
                    className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-medium py-3 rounded-xl transition-all shadow-lg flex justify-center items-center gap-2"
                >
                    {recalculating ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Recalculate Model'}
                </button>
            </div>
        </div>
      </div>

      {/* AI Strategy Summary */}
      <div className="bg-white rounded-3xl border border-neutral-200/60 shadow-sm overflow-hidden mb-12">
        <div className="border-b border-neutral-100 p-6 bg-neutral-50/50">
          <h3 className="font-semibold text-neutral-900 tracking-tight">Executive Strategy Summary</h3>
        </div>
        <div className="p-8">
          <div className="prose prose-neutral max-w-none text-neutral-700 font-light leading-relaxed">
            {sim.recommendation.split('\n').map((paragraph: string, i: number) => (
                <p key={i} className="mb-4">{paragraph}</p>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}
