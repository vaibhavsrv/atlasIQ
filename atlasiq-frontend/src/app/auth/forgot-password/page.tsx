'use client';
import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Loader2, AlertCircle, CheckCircle2, KeyRound, ArrowLeft } from 'lucide-react';

type Step = 'IDENTIFIER' | 'OTP' | 'NEW_PASSWORD';

export default function ForgotPasswordPage() {
  const router = useRouter();
  const [step, setStep] = useState<Step>('IDENTIFIER');
  
  // Form State
  const [identifier, setIdentifier] = useState('');
  const [otpCode, setOtpCode] = useState('');
  const [newPassword, setNewPassword] = useState('');
  
  // UI State
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [cooldown, setCooldown] = useState(0);

  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (cooldown > 0) {
      timer = setTimeout(() => setCooldown(cooldown - 1), 1000);
    }
    return () => clearTimeout(timer);
  }, [cooldown]);

  const handleSendOtp = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res = await fetch('http://localhost:8000/api/v1/auth/forgot-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ identifier }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Failed to send OTP');
      
      setCooldown(60);
      setStep('OTP');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOtp = async (e: React.FormEvent) => {
    e.preventDefault();
    // We just transition to new password screen, verification happens atomically at reset-password
    // However, the backend doesn't have a standalone verify step for forgot password, it's checked on reset.
    // For UI flow, we'll just allow them to proceed if it's 6 digits.
    if (otpCode.length === 6) {
        setStep('NEW_PASSWORD');
    } else {
        setError('OTP must be 6 digits');
    }
  };

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res = await fetch('http://localhost:8000/api/v1/auth/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ identifier, otp_code: otpCode, new_password: newPassword }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Password reset failed');
      
      setSuccess('Password reset successfully!');
      setTimeout(() => {
        router.push('/auth/login');
      }, 2000);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col items-center justify-center py-20 px-4">
      <div className="w-full max-w-md bg-white rounded-3xl border border-neutral-200/60 shadow-xl p-8 sm:p-10 relative overflow-hidden">
        
        <Link href="/auth/login" className="inline-flex items-center gap-2 text-sm font-medium text-neutral-500 hover:text-neutral-900 transition-colors mb-8">
            <ArrowLeft className="w-4 h-4" />
            Back to Login
        </Link>

        <div className="mb-8 text-center">
          <div className="w-12 h-12 rounded-xl bg-indigo-50 flex items-center justify-center mx-auto mb-4">
              <KeyRound className="w-6 h-6 text-indigo-600" />
          </div>
          <h1 className="text-2xl font-semibold tracking-tight text-neutral-900 mb-2">Reset Password</h1>
          <p className="text-neutral-500 font-light text-sm">
            {step === 'IDENTIFIER' && "Enter your email or phone to receive a reset code."}
            {step === 'OTP' && `We sent a 6-digit code to ${identifier}`}
            {step === 'NEW_PASSWORD' && "Enter your new strong password."}
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-50 text-red-600 rounded-xl flex items-start gap-3 text-sm font-medium border border-red-100">
            <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
            <p className="leading-snug">{error}</p>
          </div>
        )}

        {success && (
          <div className="mb-6 p-4 bg-green-50 text-green-700 rounded-xl flex items-center gap-3 text-sm font-medium border border-green-100">
            <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
            <p>{success}</p>
          </div>
        )}

        {/* STEP 1: IDENTIFIER */}
        {step === 'IDENTIFIER' && (
          <form onSubmit={handleSendOtp} className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-neutral-700 mb-2">Registered Email or Phone</label>
              <input 
                type="text" 
                required
                value={identifier}
                onChange={(e) => setIdentifier(e.target.value)}
                className="w-full px-4 py-3 bg-neutral-50 border border-neutral-200 rounded-xl focus:ring-2 focus:ring-neutral-900 focus:border-neutral-900 outline-none transition-all"
                placeholder="e.g. hello@atlasiq.com"
              />
            </div>
            <button 
              type="submit" 
              disabled={loading || !identifier}
              className="w-full bg-neutral-900 hover:bg-neutral-800 disabled:opacity-50 text-white font-medium py-3 rounded-xl transition-all shadow-lg flex justify-center items-center gap-2"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Send Reset Code'}
            </button>
          </form>
        )}

        {/* STEP 2: OTP */}
        {step === 'OTP' && (
          <form onSubmit={handleVerifyOtp} className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-neutral-700 mb-2 text-center">Enter 6-digit Code</label>
              <input 
                type="text" 
                required
                maxLength={6}
                value={otpCode}
                onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, ''))}
                className="w-full px-4 py-4 text-center text-3xl tracking-widest bg-neutral-50 border border-neutral-200 rounded-xl focus:ring-2 focus:ring-neutral-900 focus:border-neutral-900 outline-none transition-all font-mono"
                placeholder="000000"
              />
            </div>
            
            <button 
              type="submit" 
              disabled={loading || otpCode.length !== 6}
              className="w-full bg-neutral-900 hover:bg-neutral-800 disabled:opacity-50 text-white font-medium py-3 rounded-xl transition-all shadow-lg flex justify-center items-center gap-2"
            >
              Verify Code
            </button>

            <div className="text-center mt-4">
              <button
                type="button"
                onClick={() => handleSendOtp()}
                disabled={cooldown > 0 || loading}
                className="text-sm font-medium text-indigo-600 hover:text-indigo-500 disabled:text-neutral-400 transition-colors"
              >
                {cooldown > 0 ? `Resend OTP in ${cooldown}s` : 'Resend OTP'}
              </button>
            </div>
          </form>
        )}

        {/* STEP 3: NEW PASSWORD */}
        {step === 'NEW_PASSWORD' && !success && (
          <form onSubmit={handleResetPassword} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-neutral-700 mb-2">New Password</label>
              <input 
                type="password" 
                required
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                className="w-full px-4 py-3 bg-neutral-50 border border-neutral-200 rounded-xl focus:ring-2 focus:ring-neutral-900 outline-none transition-all"
                placeholder="Min 8 chars, 1 uppercase, 1 symbol"
              />
            </div>

            <button 
              type="submit" 
              disabled={loading || !newPassword}
              className="w-full bg-neutral-900 hover:bg-neutral-800 disabled:opacity-50 text-white font-medium py-3 rounded-xl transition-all shadow-lg flex justify-center items-center gap-2 mt-4"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Save New Password'}
            </button>
          </form>
        )}

      </div>
    </div>
  );
}
