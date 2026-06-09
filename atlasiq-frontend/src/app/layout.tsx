import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import { Store } from "lucide-react";
import { Providers } from "@/components/Providers";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AtlasIQ",
  description: "Business Expansion Operating System",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable}`}>
      <body className="min-h-screen bg-[#fafafa] text-neutral-900 font-sans antialiased selection:bg-neutral-200 flex flex-col">
        <Providers>
          {/* Global Navigation */}
          <nav className="sticky top-0 z-50 bg-white/70 backdrop-blur-md border-b border-neutral-200/50">
            <div className="container mx-auto px-6 h-16 flex items-center justify-between">
              <Link href="/" className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-md bg-neutral-900 flex items-center justify-center shadow-sm">
                  <Store className="w-4 h-4 text-white" />
                </div>
                <span className="text-xl font-medium tracking-tight text-neutral-900">
                  AtlasIQ
                </span>
              </Link>
              <div className="flex items-center gap-6">
                <Link href="/projects" className="text-sm font-medium text-neutral-500 hover:text-neutral-900 transition-colors">
                  Projects
                </Link>
                <Link href="/simulations" className="text-sm font-medium text-neutral-500 hover:text-neutral-900 transition-colors">
                  Simulations
                </Link>
                <Link href="/projects/new" className="inline-flex items-center justify-center bg-neutral-900 hover:bg-neutral-800 text-white rounded-full px-6 h-9 text-sm font-medium shadow-sm transition-all hover:shadow-md">
                  New Plan
                </Link>
              </div>
            </div>
          </nav>

          {/* Page Content */}
          {children}
        </Providers>
      </body>
    </html>
  );
}
