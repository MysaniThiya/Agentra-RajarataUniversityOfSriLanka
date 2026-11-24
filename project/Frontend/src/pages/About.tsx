import {
  ShieldCheck,
  Brain,
  Radar,
  FileSearch,
  ListChecks,
  Lightbulb,
  BookOpen,
  GraduationCap,
  Eye,
  Lock,
} from 'lucide-react';
import { Card } from '@/components/ui/Card';

export function About() {
  return (
    <div className="space-y-6">
      {/* hero */}
      <Card className="overflow-hidden">
        <div className="bg-gradient-to-br from-navy-800 to-navy-900 p-6 sm:p-8 text-white relative">
          <div className="absolute inset-0 opacity-10 [background-image:radial-gradient(circle_at_1px_1px,white_1px,transparent_0)] [background-size:20px_20px]" />
          <div className="relative flex items-start gap-4">
            <div className="grid place-items-center h-12 w-12 rounded-2xl bg-gradient-to-br from-iris-500 to-navy-500 shadow-glow shrink-0">
              <ShieldCheck className="h-6 w-6 text-white" />
            </div>
            <div>
              <h2 className="text-xl sm:text-2xl font-bold">About PhishGuard AI</h2>
              <p className="mt-1.5 text-navy-200 text-sm max-w-2xl leading-relaxed">
                PhishGuard AI is an intelligent, multi-agent phishing detection system that
                classifies suspicious emails and URLs as Safe, Suspicious, or Malicious —
                delivering transparent evidence and clear recommended actions.
              </p>
            </div>
          </div>
        </div>
      </Card>

      {/* how it works */}
      <Card className="p-6">
        <div className="flex items-center gap-2 mb-5">
          <Brain className="h-5 w-5 text-iris-600" />
          <h3 className="text-lg font-bold text-navy-900">How It Works</h3>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <Step icon={FileSearch} n={1} title="Submit" desc="Paste an email body or enter a URL for inspection." />
          <Step icon={Radar} n={2} title="Multi-Agent Scan" desc="Specialized AI agents evaluate headers, links, and language." />
          <Step icon={ListChecks} n={3} title="Evidence" desc="Suspicious indicators and agent findings are compiled." />
          <Step icon={Lightbulb} n={4} title="Action" desc="Get a classification, risk score, and clear next steps." />
        </div>
      </Card>

      {/* awareness */}
      <Card className="p-6">
        <div className="flex items-center gap-2 mb-5">
          <GraduationCap className="h-5 w-5 text-iris-600" />
          <h3 className="text-lg font-bold text-navy-900">Security Awareness</h3>
        </div>
        <div className="grid sm:grid-cols-2 gap-4">
          <Tip
            icon={Eye}
            title="Spot lookalike domains"
            desc="Attackers swap letters with numbers or use near-identical domains (paypa1.com vs paypal.com). Always verify the exact address."
          />
          <Tip
            icon={Lightbulb}
            title="Beware urgency cues"
            desc='"Your account will be suspended" and "act now" pressure victims to bypass verification. Treat urgency as a red flag.'
          />
          <Tip
            icon={Lock}
            title="Never share credentials"
            desc="Legitimate services never ask for your password by email. When unsure, go directly to the official site by typing the URL."
          />
          <Tip
            icon={BookOpen}
            title="Verify, don't click"
            desc="Hover over links to preview destinations, and cross-check sender addresses against known contacts before interacting."
          />
        </div>
      </Card>
    </div>
  );
}

function Step({ icon: Icon, n, title, desc }: { icon: typeof Brain; n: number; title: string; desc: string }) {
  return (
    <div className="relative rounded-xl border border-navy-100 p-4 hover:border-iris-200 hover:shadow-card-hover transition">
      <div className="flex items-center gap-2 mb-2">
        <div className="grid place-items-center h-9 w-9 rounded-lg bg-iris-50 text-iris-600">
          <Icon className="h-5 w-5" />
        </div>
        <span className="text-xs font-bold text-navy-300">0{n}</span>
      </div>
      <p className="font-semibold text-navy-900 text-sm">{title}</p>
      <p className="mt-1 text-xs text-navy-500 leading-relaxed">{desc}</p>
    </div>
  );
}

function Tip({ icon: Icon, title, desc }: { icon: typeof Eye; title: string; desc: string }) {
  return (
    <div className="flex gap-3 rounded-xl bg-navy-50/60 border border-navy-100 p-4">
      <div className="grid place-items-center h-9 w-9 rounded-lg bg-white text-iris-600 ring-1 ring-navy-100 shrink-0">
        <Icon className="h-5 w-5" />
      </div>
      <div>
        <p className="font-semibold text-navy-900 text-sm">{title}</p>
        <p className="mt-1 text-sm text-navy-600 leading-relaxed">{desc}</p>
      </div>
    </div>
  );
}
