import type { ButtonHTMLAttributes, ReactNode } from 'react';

type Variant = 'primary' | 'secondary' | 'ghost';
type Size = 'sm' | 'md' | 'lg';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: Size;
  children: ReactNode;
}

const variants: Record<Variant, string> = {
  primary:
    'bg-iris-600 text-white hover:bg-iris-700 shadow-sm hover:shadow-md focus:ring-iris-300',
  secondary:
    'bg-navy-800 text-white hover:bg-navy-900 shadow-sm focus:ring-navy-300',
  ghost:
    'bg-white text-navy-700 border border-navy-200 hover:bg-navy-50 focus:ring-navy-200',
};

const sizes: Record<Size, string> = {
  sm: 'px-3 py-1.5 text-sm rounded-lg gap-1.5',
  md: 'px-4 py-2.5 text-sm rounded-xl gap-2',
  lg: 'px-6 py-3 text-base rounded-xl gap-2.5',
};

export function Button({
  variant = 'primary',
  size = 'md',
  children,
  className = '',
  ...props
}: ButtonProps) {
  return (
    <button
      className={`inline-flex items-center justify-center font-semibold transition-all
        focus:outline-none focus:ring-2 disabled:opacity-50 disabled:cursor-not-allowed
        active:scale-[0.98] ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
