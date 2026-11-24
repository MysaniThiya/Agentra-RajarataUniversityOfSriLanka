import { useEffect, useState } from 'react';
import { Mail, Link2, Search, Loader2, History as HistoryIcon } from 'lucide-react';
import { Card } from '@/components/ui/Card';
import { ClassificationBadge } from '@/components/ui/Badge';
import { fetchHistory } from '@/services/api';
import { classificationConfig, formatDate, scoreColor } from '@/lib/ui';
import type { AnalysisResult } from '@/types';

export function ScanHistory() {
  const [rows, setRows] = useState<AnalysisResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState('');

  useEffect(() => {
    fetchHistory().then((r) => {
      setRows(r);
      setLoading(false);
    });
  }, []);

  const filtered = rows.filter(
    (r) =>
      r.input.toLowerCase().includes(query.toLowerCase()) ||
      classificationConfig[r.classification].label.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <Card className="p-4 sm:p-5">
        <div className="flex flex-col sm:flex-row sm:items-center gap-3 justify-between mb-4">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4.5 w-4.5 text-navy-300" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search by content or classification..."
              className="input-field pl-10 py-2.5"
            />
          </div>
          <p className="text-sm text-navy-500">{filtered.length} scans</p>
        </div>

        {loading ? (
          <div className="py-16 grid place-items-center text-navy-400">
            <Loader2 className="h-6 w-6 animate-spin mb-2" />
            Loading history...
          </div>
        ) : filtered.length === 0 ? (
          <div className="py-16 grid place-items-center text-navy-400">
            <HistoryIcon className="h-8 w-8 mb-2" />
            No matching scans found.
          </div>
        ) : (
          <div className="overflow-x-auto -mx-4 sm:mx-0">
            <table className="w-full min-w-[640px] text-sm">
              <thead>
                <tr className="text-left text-[11px] uppercase tracking-wider text-navy-400 border-b border-navy-100">
                  <th className="font-semibold px-4 py-3">Scan Type</th>
                  <th className="font-semibold px-4 py-3">Submitted Content</th>
                  <th className="font-semibold px-4 py-3">Classification</th>
                  <th className="font-semibold px-4 py-3">Risk Score</th>
                  <th className="font-semibold px-4 py-3">Date & Time</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-navy-50">
                {filtered.map((r) => (
                  <tr key={r.id} className="hover:bg-navy-50/50 transition-colors">
                    <td className="px-4 py-3.5">
                      <span className="inline-flex items-center gap-2 font-medium text-navy-700">
                        {r.type === 'email' ? (
                          <Mail className="h-4 w-4 text-iris-600" />
                        ) : (
                          <Link2 className="h-4 w-4 text-iris-600" />
                        )}
                        <span className="capitalize">{r.type}</span>
                      </span>
                    </td>
                    <td className="px-4 py-3.5 max-w-xs">
                      <p className="font-mono text-[12px] text-navy-700 truncate" title={r.input}>
                        {r.input}
                      </p>
                    </td>
                    <td className="px-4 py-3.5">
                      <ClassificationBadge classification={r.classification} size="sm" />
                    </td>
                    <td className="px-4 py-3.5">
                      <div className="flex items-center gap-2 w-28">
                        <div className="flex-1 h-1.5 rounded-full bg-navy-100 overflow-hidden">
                          <div
                            className={`h-full rounded-full ${scoreColor(r.riskScore)}`}
                            style={{ width: `${r.riskScore}%` }}
                          />
                        </div>
                        <span className="text-xs font-bold text-navy-700 w-8 text-right">{r.riskScore}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3.5 text-navy-500 whitespace-nowrap">
                      {formatDate(r.scannedAt)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  );
}
