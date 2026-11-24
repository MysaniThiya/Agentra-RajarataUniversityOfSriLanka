/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        navy: {
          50: '#f0f4fa',
          100: '#dae6f5',
          200: '#b8cced',
          300: '#8aa9df',
          400: '#5a80cc',
          500: '#3a61b8',
          600: '#2a4a9c',
          700: '#1f3a80',
          800: '#15294f',
          900: '#0f1d3a',
          950: '#0a1228',
        },
        iris: {
          50: '#f5f3ff',
          100: '#ede9fe',
          200: '#ddd6fe',
          300: '#c4b5fd',
          400: '#a78bfa',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95',
        },
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'monospace'],
      },
      boxShadow: {
        card: '0 1px 3px rgba(15, 29, 58, 0.06), 0 1px 2px rgba(15, 29, 58, 0.04)',
        'card-hover': '0 10px 30px -8px rgba(15, 29, 58, 0.12), 0 4px 10px -4px rgba(15, 29, 58, 0.06)',
        glow: '0 0 0 1px rgba(139, 92, 246, 0.2), 0 8px 30px -6px rgba(139, 92, 246, 0.25)',
      },
      keyframes: {
        'fade-in': {
          '0%': { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'slide-in': {
          '0%': { opacity: '0', transform: 'translateX(-12px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        'pulse-ring': {
          '0%': { transform: 'scale(0.8)', opacity: '0.8' },
          '100%': { transform: 'scale(2.2)', opacity: '0' },
        },
        shimmer: {
          '100%': { transform: 'translateX(100%)' },
        },
      },
      animation: {
        'fade-in': 'fade-in 0.4s ease-out both',
        'slide-in': 'slide-in 0.35s ease-out both',
        'pulse-ring': 'pulse-ring 1.8s ease-out infinite',
        shimmer: 'shimmer 1.6s infinite',
      },
    },
  },
  plugins: [],
};
