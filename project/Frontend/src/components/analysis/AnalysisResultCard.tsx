import {
  AlertTriangle,
  ArrowLeft,
  Check,
  CheckCircle2,
  Download,
  FileText,
  Info,
  Laptop,
  Search,
  ShieldAlert,
  ShieldCheck,
  ShieldQuestion,
} from 'lucide-react';
import type { ReactNode } from 'react';
import type { AnalysisResult, Classification } from '@/types';
import { classificationConfig } from '@/lib/ui';

interface AnalysisResultCardProps {
  result: AnalysisResult;
  onBack: () => void;
}

const statusLabel: Record<Classification, string> = {
  safe: 'Low Risk',
  suspicious: 'Moderate Risk',
  malicious: 'High Risk',
  unknown: 'Inconclusive',
};

const actionItems: Record<Classification, string[]> = {
  safe: [
    'No immediate action is required.',
    'Continue verifying unexpected requests through official channels.',
    'Keep your security awareness practices up to date.',
  ],
  suspicious: [
    'Do not click suspicious links.',
    'Do not share credentials or sensitive information.',
    'Verify the communication through an official channel.',
    'Report the message to your security team for review.',
  ],
  malicious: [
    'Do not click suspicious links.',
    'Do not share credentials or sensitive information.',
    'Report the suspicious message to your security team.',
    'Verify communications through official channels.',
  ],
  unknown: [
    'The analysis is incomplete.',
    'Do not click unknown or suspicious links.',
    'Wait for the remaining security agents to complete their analysis.',
    'Verify the URL through its official website.',
  ],
};

function RiskGauge({
  score,
  classification,
}: {
  score: number | null;
  classification: Classification;
}) {
  const color =
    classification === 'safe'
      ? '#16a34a'
      : classification === 'suspicious'
        ? '#f59e0b'
        : classification === 'malicious'
          ? '#dc2626'
          : '#94a3b8';

  const radius = 72;
  const circumference = Math.PI * radius;

  const progress =
    score === null
      ? 0
      : circumference - (Math.min(score, 100) / 100) * circumference;

  return (
    <div className="relative h-[148px] w-[260px] max-w-full">
      <svg viewBox="0 0 180 100" className="h-full w-full overflow-visible">
        <path
          d="M 18 90 A 72 72 0 0 1 162 90"
          fill="none"
          stroke="#e3e7f2"
          strokeWidth="13"
          strokeLinecap="round"
        />

        {score !== null && (
          <path
            d="M 18 90 A 72 72 0 0 1 162 90"
            fill="none"
            stroke={color}
            strokeWidth="13"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={progress}
            className="transition-all duration-1000"
          />
        )}
      </svg>

      <div className="absolute inset-x-0 bottom-1 flex items-baseline justify-center gap-1">
        <span className="text-4xl font-bold tracking-tight text-slate-700">
          {score === null ? 'N/A' : score}
        </span>

        {score !== null && (
          <span className="text-2xl font-bold text-navy-800">/100</span>
        )}
      </div>

      <div className="absolute bottom-[-22px] inset-x-0 flex justify-center">
        <span
          className={`inline-flex items-center gap-1.5 rounded-full border px-4 py-1 text-sm font-bold ${classificationConfig[classification].bg} ${classificationConfig[classification].text} ${classificationConfig[classification].border}`}
        >
          {classification === 'safe' ? (
            <ShieldCheck className="h-4 w-4" />
          ) : classification === 'unknown' ? (
            <ShieldQuestion className="h-4 w-4" />
          ) : (
            <ShieldAlert className="h-4 w-4" />
          )}

          {statusLabel[classification]}
        </span>
      </div>
    </div>
  );
}

function formatCompletedAt(iso: string): string {
  return new Date(iso).toLocaleString(undefined, {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

export function AnalysisResultCard({ result, onBack }: AnalysisResultCardProps) {
  const config = classificationConfig[result.classification];
  const isMalicious = result.classification === 'malicious';
  const findings = result.agentFindings.length > 0 ? result.agentFindings : result.evidence;
  const indicators = result.evidence.length > 0 ? result.evidence : [];

  return (
    <div className="rounded-[22px] border border-indigo-100 bg-white shadow-card overflow-hidden animate-fade-in">
      <div className="relative overflow-hidden bg-gradient-to-br from-white via-white to-rose-50/70 px-5 py-5 sm:px-8 sm:py-6">
        <div className="pointer-events-none absolute -right-20 -top-28 h-72 w-72 rounded-full bg-rose-100/40 blur-3xl" />
        <div className="pointer-events-none absolute right-24 -top-20 h-44 w-[520px] rotate-12 rounded-[50%] border border-rose-100/70" />

        <div className="relative flex flex-wrap items-center justify-between gap-3">
          <button
            onClick={onBack}
            className="inline-flex items-center gap-2 rounded-xl border border-indigo-100 bg-white/80 px-3.5 py-2 text-sm font-semibold text-navy-800 shadow-sm transition hover:border-indigo-200 hover:bg-white"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Dashboard
          </button>
          <button
            onClick={() => window.print()}
            className="inline-flex items-center gap-2 rounded-xl border border-indigo-100 bg-white/80 px-3.5 py-2 text-sm font-semibold text-navy-800 shadow-sm transition hover:border-indigo-200 hover:bg-white"
          >
            <Download className="h-4 w-4" />
            Download Report
          </button>
        </div>

        <div className="relative mt-6 grid gap-5 lg:grid-cols-[120px_1fr] lg:items-center">
          <div className={`mx-auto grid h-28 w-28 place-items-center rounded-full border-[10px] ${isMalicious ? 'border-red-100 bg-red-50' : `${config.border} ${config.bg}`}`}>
            {result.classification === 'unknown' ? (
              <ShieldQuestion className="h-14 w-14 text-slate-500" />
            ) : isMalicious || result.classification === 'suspicious' ? (
              <ShieldAlert className={`h-14 w-14 ${config.text}`} />
            ) : (
              <ShieldCheck className={`h-14 w-14 ${config.text}`} />
            )}
          </div>
          <div className="text-center lg:text-left">
            <h2 className="text-2xl font-bold tracking-tight text-navy-900 sm:text-3xl">
              PhishGuard AI – Investigation Report
            </h2>
            <p className="mt-1 text-sm font-medium text-navy-700">
              Analysis completed on: {formatCompletedAt(result.scannedAt)}
            </p>
          </div>
        </div>

        <div className="relative mt-9 grid gap-8 lg:grid-cols-[380px_1fr] lg:items-center">
          <div className="flex justify-center">
            <RiskGauge score={result.riskScore} classification={result.classification} />
          </div>
          <div className={`rounded-2xl border px-5 py-5 sm:px-6 ${isMalicious ? 'border-red-200 bg-gradient-to-r from-red-50 to-pink-50' : `${config.border} ${config.bg}`}`}>
            <div className="flex gap-4">
              <div className={`grid h-12 w-12 shrink-0 place-items-center rounded-xl ${isMalicious ? 'bg-red-500 text-white' : `${config.bar} text-white`}`}>
                {isMalicious ? <AlertTriangle className="h-7 w-7" /> : <ShieldCheck className="h-7 w-7" />}
              </div>
              <div>
                <h3 className={`text-lg font-bold ${isMalicious ? 'text-red-800' : config.text}`}>
                  {isMalicious
                    ? 'This content is likely a phishing attempt!'
                    : result.classification === 'suspicious'
                      ? 'This content needs careful review.'
                      : result.classification === 'unknown'
                        ? 'The overall assessment is inconclusive.'
                        : 'This content appears safe.'}
                </h3>
                <p className="mt-1 text-sm leading-relaxed text-navy-800">
                  {isMalicious
                    ? 'Multiple indicators suggest this email or URL may be malicious. Please review the details below and follow the recommended actions.'
                    : result.explanation}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid gap-4 px-5 pb-5 sm:px-7 sm:pb-7 lg:grid-cols-2">
        <ReportPanel title="Investigation Findings" icon={Search} tone="blue">
          <div className="divide-y divide-indigo-100">
            {findings.slice(0, 4).map((finding, index) => {
              const label = 'agent' in finding ? finding.agent : finding.title;
              const detail = 'agent' in finding ? finding.finding : finding.detail;
              const classification ='agent' in finding? finding.classification: finding.severity;
              return (
                <div key={`${label}-${index}`} className="flex items-center gap-3 px-4 py-3">
                  <CheckCircle2 className="h-5 w-5 shrink-0 text-blue-700" />
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-semibold text-navy-800">{label}</p>
                    <p className="truncate text-xs text-navy-500">{detail}</p>
                  </div>
                  <span className={`shrink-0 rounded-full px-3 py-1 text-xs font-bold ${classificationConfig[classification].bg} ${classificationConfig[classification].text}`}>
                    {'agent' in finding && finding.status === 'unavailable'
                      ? 'Pending'
                      : 'agent' in finding && finding.status === 'error'
                        ? 'Error'
                        : classificationConfig[classification].label}
                  </span>
                </div>
              );  
            })}
          </div>
        </ReportPanel>

        <ReportPanel title="Agent Evidence" icon={FileText} tone="purple">
          <div className="divide-y divide-indigo-100">
            {indicators.slice(0, 4).map((indicator, index) => {
              const severity = indicator.severity;

              const iconConfig = {
                safe: {
                  background: 'bg-emerald-500',
                  icon: <ShieldCheck className="h-3.5 w-3.5" />,
                },
                suspicious: {
                  background: 'bg-amber-500',
                  icon: <AlertTriangle className="h-3.5 w-3.5" />,
                },
                malicious: {
                  background: 'bg-red-500',
                  icon: <ShieldAlert className="h-3.5 w-3.5" />,
                },
                unknown: {
                  background: 'bg-slate-400',
                  icon: <Info className="h-3.5 w-3.5" />,
                },
              };

              const config = iconConfig[severity];

              return (
                <div
                  key={`${indicator.title}-${index}`}
                  className="flex items-center gap-3 px-4 py-3"
                >
                  <span
                    className={`grid h-5 w-5 shrink-0 place-items-center rounded-full ${config.background} text-white`}
                  >
                    {config.icon}
                  </span>

                  <p className="text-sm font-medium text-navy-800">
                    {indicator.detail}
                  </p>
                </div>
              );
            })}
          </div>
        </ReportPanel>
      </div>

      <div className="mx-5 mb-5 rounded-2xl border border-emerald-300 bg-gradient-to-br from-emerald-50 to-cyan-50 px-5 py-5 sm:mx-7 sm:mb-7 sm:px-6">
        <div className="flex gap-3">
          <ShieldCheck className="h-8 w-8 shrink-0 text-emerald-700" />
          <div className="min-w-0 flex-1">
            <h3 className="text-lg font-bold text-emerald-800">Recommended Actions</h3>
            <div className="mt-3 grid gap-2 sm:grid-cols-2">
              {result.recommendedAction
                .split('\n')
                .filter((action) => action.trim().length > 0)
                .map((action, index) => (
                  <div
                    key={`${action}-${index}`}
                    className="flex items-start gap-2 text-sm font-medium text-navy-800"
                  >
                    <span className="mt-0.5 grid h-4 w-4 shrink-0 place-items-center rounded-full bg-emerald-600 text-white">
                      <Check className="h-3 w-3" />
                    </span>
                    {action}
                  </div>
                ))}
            </div>
          </div>
          <Laptop className="hidden h-20 w-20 shrink-0 self-end text-blue-700/30 sm:block" />
        </div>
      </div>

      <div className="mx-5 mb-5 flex items-center justify-center gap-2 rounded-xl bg-indigo-50 px-4 py-2.5 text-center text-xs font-medium text-navy-700 sm:mx-7 sm:mb-7">
        <Info className="h-4 w-4 shrink-0 text-blue-700" />
        <span>Always verify suspicious communications through official channels.</span>
    </div>
    </div>
  );
}

function ReportPanel({
  title,
  icon: Icon,
  tone,
  children,
}: {
  title: string;
  icon: typeof Search;
  tone: 'blue' | 'purple';
  children: ReactNode;
}) {
  const styles = tone === 'blue' ? 'border-blue-200 bg-blue-50/80 text-blue-950' : 'border-purple-200 bg-purple-50/80 text-purple-950';
  return (
    <section className={`overflow-hidden rounded-xl border ${styles}`}>
      <div className="flex items-center gap-3 border-b border-inherit px-4 py-3">
        <Icon className="h-6 w-6" />
        <h3 className="font-bold">{title}</h3>
      </div>
      <div className="bg-white">{children}</div>
    </section>
  );
}
