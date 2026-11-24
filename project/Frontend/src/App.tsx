import { useState } from 'react';
import { Sidebar } from '@/components/layout/Sidebar';
import { Header } from '@/components/layout/Header';
import { Dashboard } from '@/pages/Dashboard';
import { ScanHistory } from '@/pages/ScanHistory';
import { About } from '@/pages/About';

import type { AnalysisResult, Page } from '@/types';

function App() {
  const [page, setPage] = useState<Page>('dashboard');
  const [mobileOpen, setMobileOpen] = useState(false);
  const [lastResult, setLastResult] = useState<AnalysisResult | null>(null);

  return (
    <div className="flex min-h-screen bg-navy-50">
      <Sidebar
        current={page}
        onNavigate={setPage}
        mobileOpen={mobileOpen}
        onCloseMobile={() => setMobileOpen(false)}
      />

      <div className="flex-1 min-w-0 flex flex-col">
        <Header page={page} onOpenMobile={() => setMobileOpen(true)} />

        <main className="flex-1 px-4 sm:px-6 lg:px-8 py-6">
          <div className="max-w-6xl mx-auto">
            {page === 'dashboard' && (
              <Dashboard lastResult={lastResult} onResult={setLastResult} />
            )}
            {page === 'history' && <ScanHistory />}
            {page === 'about' && <About />}
            
          </div>
        </main>

        <footer className="px-4 sm:px-6 lg:px-8 py-5 border-t border-slate-200 bg-white">
          <div className="max-w-6xl mx-auto flex flex-col items-center justify-center text-center gap-1.5 text-xs text-navy-400">
            <p>PhishGuard AI — Intelligent Phishing Detection & Investigation</p>
            <p>Protecting users through AI-powered threat analysis.</p>
          </div>
        </footer>
      </div>
    </div>
  );
}

export default App;
