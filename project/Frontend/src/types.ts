export type Classification =
  | 'safe'
  | 'suspicious'
  | 'malicious'
  | 'unknown';

export type ScanType = 'email' | 'url';

export interface Evidence {
  title: string;
  detail: string;
  severity: Classification;
}

export interface AgentFinding {
  agent: string;
  finding: string;
  classification: Classification;
  status: 'completed' | 'unavailable' | 'error';
  confidence?: number;
}

export interface AnalysisResult {
  id: string;
  type: ScanType;
  input: string;
  classification: Classification;
  riskScore: number | null;
  evidence: Evidence[];
  agentFindings: AgentFinding[];
  explanation: string;
  recommendedAction: string;
  scannedAt: string;
}

export type Page = 'dashboard' | 'history' | 'about';