import type { Classification } from '@/types';

export const classificationConfig: Record<
  Classification,
  { label: string; text: string; bg: string; border: string; ring: string; bar: string; dot: string }
> = {
  safe: {
    label: 'Safe',
    text: 'text-emerald-700',
    bg: 'bg-emerald-50',
    border: 'border-emerald-200',
    ring: 'ring-emerald-300',
    bar: 'bg-emerald-500',
    dot: 'bg-emerald-500',
  },
  suspicious: {
    label: 'Suspicious',
    text: 'text-amber-700',
    bg: 'bg-amber-50',
    border: 'border-amber-200',
    ring: 'ring-amber-300',
    bar: 'bg-amber-500',
    dot: 'bg-amber-500',
  },
  malicious: {
    label: 'Malicious',
    text: 'text-red-700',
    bg: 'bg-red-50',
    border: 'border-red-200',
    ring: 'ring-red-300',
    bar: 'bg-red-500',
    dot: 'bg-red-500',
  },
};

export function scoreColor(score: number): string {
  if (score < 40) return 'bg-emerald-500';
  if (score < 70) return 'bg-amber-500';
  return 'bg-red-500';
}

export function formatDate(iso: string): string {
  return new Date(iso).toLocaleString(undefined, {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}
