
import type { AnalysisResult, ScanType } from '@/types';

const API_BASE_URL = 'http://127.0.0.1:8000';

interface BackendAgentResult {
  agent: string;
  status: 'completed' | 'unavailable' | 'error';
  classification: 'safe' | 'suspicious' | 'malicious' | 'unknown';
  risk_score: number | null;
  indicators: string[];
  explanation: string;
  evidence: string[];
}

interface BackendResponse {
  message: string;
  results: {
    email: BackendAgentResult | null;
    url: BackendAgentResult | null;
    threat_intelligence: BackendAgentResult | null;
    risk_assessment: {
      status: string;
      explanation: string;
      risk_score?: number | null;
      classification?: 'safe' | 'suspicious' | 'malicious' | 'unknown';
    } | null;
  };
}

export async function analyzeEmail(input: string): Promise<AnalysisResult> {
  return analyzeWithBackend({ email_content: input }, input, 'email');
}

export async function analyzeUrl(input: string): Promise<AnalysisResult> {
  return analyzeWithBackend({ submitted_url: input }, input, 'url');
}

async function analyzeWithBackend(
  payload: { email_content?: string; submitted_url?: string },
  input: string,
  type: ScanType
): Promise<AnalysisResult> {
  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => null);
    throw new Error(
      errorBody?.detail ?? `Analysis failed with status ${response.status}`
    );
  }

  const data: BackendResponse = await response.json();

  const agents = [
    data.results.email,
    data.results.url,
    data.results.threat_intelligence,
  ].filter(
    (agent): agent is BackendAgentResult =>
      agent !== null && agent !== undefined
  );

  const maliciousAgent = agents.find(
    (agent) =>
      agent.status === 'completed' &&
      agent.classification === 'malicious'
  );

  const suspiciousAgent = agents.find(
    (agent) =>
      agent.status === 'completed' &&
      agent.classification === 'suspicious'
  );

  const completedAgents = agents.filter(
    (agent) => agent.status === 'completed'
  );

  const riskAssessment = data.results.risk_assessment;

  const classification =
    riskAssessment?.classification ??
    maliciousAgent?.classification ??
    suspiciousAgent?.classification ??
    completedAgents.find(
      (agent) => agent.classification === 'safe'
    )?.classification ??
    'unknown';

  const riskScore =
    riskAssessment?.risk_score ??
    agents.find(
      (agent) => agent.status === 'completed' &&
        agent.risk_score !== null
    )?.risk_score ??
    null;

  const evidence = agents.flatMap((agent) =>
    agent.evidence.map((detail) => ({
      title: `${agent.agent} evidence`,
      detail,
      severity: agent.classification,
    }))
  );

  const agentFindings = agents.map((agent) => ({
    agent: agent.agent,
    finding: agent.explanation,
    classification: agent.classification,
    status: agent.status,
  }));

  const explanation =
    riskAssessment?.explanation ||
    maliciousAgent?.explanation ||
    suspiciousAgent?.explanation ||
    completedAgents.map((agent) => agent.explanation).join(' ') ||
    'The analysis did not produce a conclusive result.';

  const recommendedAction =
    classification === 'malicious'
      ? 'Do not interact with this content. Avoid clicking links, opening attachments, or sharing information.'
      : classification === 'suspicious'
        ? 'Proceed with caution. Verify the sender or URL through an official channel before interacting.'
        : classification === 'safe'
          ? 'No known threat was detected. Continue following normal security practices.'
          : 'The result is inconclusive. Do not assume this content is safe; verify it independently.';

  return {
    id: `scan-${Date.now()}`,
    type,
    input,
    classification,
    riskScore,
    evidence,
    agentFindings,
    explanation,
    recommendedAction,
    scannedAt: new Date().toISOString(),
  };
}

export async function fetchHistory(): Promise<AnalysisResult[]> {
  // History API is not implemented in the backend yet.
  // Return an empty list instead of sample data.

  return [];
}
export type { ScanType };
