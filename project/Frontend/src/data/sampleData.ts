import type { AnalysisResult } from '@/types';

/**
 * SAMPLE DATA — used only for frontend preview.
 * Replace with real responses once the FastAPI backend is connected.
 */
export const sampleEmailResult: AnalysisResult = {
  id: 'scan-1004',
  type: 'email',
  input: 'From: security@paypa1-verify.com — Urgent: Your account has been limited. Verify your identity now to avoid suspension. http://paypa1-verify.com/login',
  classification: 'malicious',
  riskScore: 92,
  evidence: [
    { title: 'Spoofed sender domain', detail: 'Sender uses "paypa1-verify.com" with a "1" replacing the "l" — a common homoglyph attack.', severity: 'malicious' },
    { title: 'Urgency language', detail: 'Phrases like "Urgent" and "avoid suspension" pressure the recipient to act without verifying.', severity: 'suspicious' },
    { title: 'Suspicious embedded link', detail: 'The link destination does not match the legitimate PayPal domain and uses an IP-like lookalike.', severity: 'malicious' },
    { title: 'No personal salutation', detail: 'Generic greeting instead of the customer name is typical of mass phishing kits.', severity: 'suspicious' },
  ],
  agentFindings: [
    { agent: 'Header Analysis Agent', finding: 'SPF and DKIM alignment failed for the sending domain.', confidence: 96 },
    { agent: 'Content Heuristics Agent', finding: 'Detected 4 credential-harvesting linguistic markers.', confidence: 88 },
    { agent: 'URL Reputation Agent', finding: 'Linked domain registered 3 days ago, no known history.', confidence: 91 },
  ],
  explanation:
    'This email exhibits the classic structure of a credential-harvesting phishing attempt: a spoofed lookalike domain, urgency-driven copy, and a link to a newly registered, unrelated host. The combined signal strongly indicates a malicious impersonation of PayPal.',
  recommendedAction:
    'Do not click the link or enter credentials. Report the email to your security team and delete it. If you already entered credentials, reset your password immediately and enable multi-factor authentication.',
  scannedAt: new Date(Date.now() - 1000 * 60 * 24).toISOString(),
};

export const sampleUrlResult: AnalysisResult = {
  id: 'scan-1003',
  type: 'url',
  input: 'https://account-update.secure-banking-verify.net/login?id=4821',
  classification: 'suspicious',
  riskScore: 64,
  evidence: [
    { title: 'Deceptive subdomain chain', detail: 'Multiple keyword-stacked subdomains ("account-update.secure-banking-verify") aim to look legitimate.', severity: 'suspicious' },
    { title: 'Unrelated TLD', detail: 'The ".net" domain does not match the official banking domain.', severity: 'suspicious' },
    { title: 'Login form on non-HTTPS origin page', detail: 'The path leads directly to a credential form with no prior verified navigation.', severity: 'suspicious' },
  ],
  agentFindings: [
    { agent: 'URL Reputation Agent', finding: 'Domain age 41 days, low trust score from reputation feeds.', confidence: 72 },
    { agent: 'Content Heuristics Agent', finding: 'Login page mirrors a known bank template but hosted off-domain.', confidence: 68 },
  ],
  explanation:
    'The URL uses layered subdomains and security-themed keywords to mimic a bank, while the actual domain is unrelated and recently registered. No outright malware payload was detected, but the structure is consistent with credential phishing.',
  recommendedAction:
    'Do not enter credentials. Manually navigate to your bank by typing its official address. Forward the link to your IT security team for review.',
  scannedAt: new Date(Date.now() - 1000 * 60 * 60 * 5).toISOString(),
};

export const sampleHistory: AnalysisResult[] = [
  {
    id: 'scan-1002',
    type: 'email',
    input: 'Invoice attached — please review Q3 statement.pdf',
    classification: 'safe',
    riskScore: 12,
    evidence: [],
    agentFindings: [],
    explanation: 'Sender domain matched organizational records and no suspicious links were detected.',
    recommendedAction: 'No action required. Verify sender before opening attachments as a routine precaution.',
    scannedAt: new Date(Date.now() - 1000 * 60 * 60 * 26).toISOString(),
  },
  {
    id: 'scan-1001',
    type: 'url',
    input: 'https://micros0ft-update.io/security-patch',
    classification: 'malicious',
    riskScore: 88,
    evidence: [],
    agentFindings: [],
    explanation: 'Lookalike Microsoft domain using a zero instead of "o", serving a known drive-by exploit kit.',
    recommendedAction: 'Block the domain at the firewall. Do not visit under any circumstances.',
    scannedAt: new Date(Date.now() - 1000 * 60 * 60 * 50).toISOString(),
  },
  sampleUrlResult,
  sampleEmailResult,
];

export const analysisLoadingMessages = [
  'Analyzing email content.',
  'Checking URL indicators.',
  'Evaluating threat patterns.',
  'Collecting agent findings.',
];
