import type { Classification } from '@/types';
import { classificationConfig } from '@/lib/ui';

interface BadgeProps {
  classification: Classification;
  withDot?: boolean;
  size?: 'sm' | 'md';
}

export function ClassificationBadge({ classification, withDot = true, size = 'md' }: BadgeProps) {
  const c = classificationConfig[classification];
  const pad = size === 'sm' ? 'px-2.5 py-0.5 text-xs' : 'px-3 py-1 text-sm';
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border font-semibold ${c.bg} ${c.text} ${c.border} ${pad}`}
    >
      {withDot && <span className={`h-1.5 w-1.5 rounded-full ${c.dot}`} />}
      {c.label}
    </span>
  );
}
