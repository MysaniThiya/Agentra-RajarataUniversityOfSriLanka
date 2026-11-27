
import { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { Dashboard } from '@/pages/Dashboard';
import type { AnalysisResult } from '@/types';

function App() {
  const [lastResult, setLastResult] = useState<AnalysisResult | null>(null);

  return (
    <div className="min-h-screen bg-navy-50 flex flex-col">
      <Header />

      <main className="flex-1 w-full px-4 sm:px-6 lg:px-8 py-6">
        <div className="max-w-7xl mx-auto">
          <Dashboard
            lastResult={lastResult}
            onResult={setLastResult}
          />
        </div>
      </main>

      <footer className="px-4 sm:px-6 lg:px-8 py-5 border-t border-slate-200 bg-white">
        <div className="max-w-7xl mx-auto flex flex-col items-center justify-center text-center gap-1.5 text-xs text-navy-400">
          <p>PhishGuard AI — Intelligent Phishing Detection &amp; Investigation</p>
          <p>Protecting users through AI-powered threat analysis.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
