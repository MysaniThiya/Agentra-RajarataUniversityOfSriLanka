import { useState } from 'react';
import { Mail, Link2, ShieldAlert } from 'lucide-react';
import { AnalysisInput } from '@/components/analysis/AnalysisInput';
import { AnalysisLoading } from '@/components/analysis/AnalysisLoading';
import { AnalysisResultCard } from '@/components/analysis/AnalysisResultCard';
import { Card } from '@/components/ui/Card';
import { analyzeEmail, analyzeUrl } from '@/services/api';
import type { AnalysisResult } from '@/types';

type Mode = 'email' | 'url';

interface DashboardProps {
  lastResult: AnalysisResult | null;
  onResult: (r: AnalysisResult | null) => void;
}

export function Dashboard({ lastResult, onResult }: DashboardProps) {
  const [mode, setMode] = useState<Mode>('email');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async (input: string) => {
    setLoading(true);
    setError(null);
    try {
      const result = mode === 'email' ? await analyzeEmail(input) : await analyzeUrl(input);
      onResult(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {lastResult ? (
        <AnalysisResultCard result={lastResult} onBack={() => onResult(null)} />
      ) : (
        <Card className="p-5 sm:p-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-5">
            <div>
              <h2 className="text-lg font-bold text-navy-900">Threat Analysis</h2>
              <p className="text-sm text-navy-500">Choose what to inspect — an email or a URL.</p>
            </div>
            <div className="inline-flex rounded-xl bg-navy-100 p-1 self-start sm:self-auto">
              <ModeButton active={mode === 'email'} onClick={() => setMode('email')} icon={Mail} label="Email" />
              <ModeButton active={mode === 'url'} onClick={() => setMode('url')} icon={Link2} label="URL" />
            </div>
          </div>

          {error && (
            <div className="mb-4 rounded-xl bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700 flex items-center gap-2">
              <ShieldAlert className="h-4.5 w-4.5 shrink-0" />
              {error}
            </div>
          )}

          {!loading && <AnalysisInput mode={mode} onAnalyze={handleAnalyze} loading={loading} />}
          {loading && <AnalysisLoading />}
        </Card>
      )}
    </div>
  );
}

function ModeButton({
  active,
  onClick,
  icon: Icon,
  label,
}: {
  active: boolean;
  onClick: () => void;
  icon: typeof Mail;
  label: string;
}) {
  return (
    <button
      onClick={onClick}
      className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all
        ${active ? 'bg-white text-navy-900 shadow-sm' : 'text-navy-600 hover:text-navy-900'}`}
    >
      <Icon className="h-4 w-4" />
      {label}
    </button>
  );
}
