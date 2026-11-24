import { ScanLine, Brain } from 'lucide-react';
import { useEffect, useState } from 'react';
import { analysisLoadingMessages } from '@/data/sampleData';

export function AnalysisLoading() {
  const [step, setStep] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setStep((s) => (s + 1) % analysisLoadingMessages.length);
    }, 1400);
    return () => clearInterval(id);
  }, []);

  return (
    <div className="card p-8 sm:p-10 animate-fade-in">
      <div className="flex flex-col items-center text-center">
        {/* pulse rings */}
        <div className="relative grid place-items-center h-20 w-20 mb-6">
          <span className="absolute h-16 w-16 rounded-full bg-iris-400/30 animate-pulse-ring" />
          <span
            className="absolute h-16 w-16 rounded-full bg-iris-400/30 animate-pulse-ring"
            style={{ animationDelay: '0.6s' }}
          />
          <div className="relative grid place-items-center h-16 w-16 rounded-full bg-gradient-to-br from-iris-500 to-navy-600 shadow-glow">
            <ScanLine className="h-7 w-7 text-white animate-pulse" />
          </div>
        </div>

        <h3 className="text-lg font-bold text-navy-900">Running multi-agent analysis</h3>
        <p className="mt-1.5 text-sm text-navy-500 max-w-sm">
          Our AI agents are inspecting indicators, reputation feeds, and linguistic patterns.
        </p>

        {/* message sequence */}
        <div className="mt-6 w-full max-w-sm space-y-2.5">
          {analysisLoadingMessages.map((msg, i) => {
            const done = i < step;
            const current = i === step;
            return (
              <div
                key={msg}
                className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-all duration-300
                  ${current ? 'bg-iris-50 border border-iris-200' : done ? 'opacity-70' : 'opacity-40'}`}
              >
                <div
                  className={`h-5 w-5 rounded-full grid place-items-center text-[10px] font-bold shrink-0 transition
                    ${done ? 'bg-emerald-500 text-white' : current ? 'bg-iris-500 text-white' : 'bg-navy-100 text-navy-400'}`}
                >
                  {done ? '✓' : i + 1}
                </div>
                <span
                  className={`${done ? 'text-navy-600 line-through' : current ? 'text-navy-900 font-semibold' : 'text-navy-400'}`}
                >
                  {msg}
                </span>
                {current && <Brain className="ml-auto h-4 w-4 text-iris-500 animate-pulse" />}
              </div>
            );
          })}
        </div>

        {/* progress bar */}
        <div className="mt-6 w-full max-w-sm h-1.5 rounded-full bg-navy-100 overflow-hidden">
          <div
            className="h-full rounded-full bg-gradient-to-r from-iris-500 to-navy-500 transition-all duration-700"
            style={{ width: `${((step + 1) / analysisLoadingMessages.length) * 100}%` }}
          />
        </div>
      </div>
    </div>
  );
}
