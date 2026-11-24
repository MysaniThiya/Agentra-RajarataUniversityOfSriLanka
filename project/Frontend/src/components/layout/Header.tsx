import { Menu, Bell, UserCircle } from 'lucide-react';
import type { Page } from '@/types';

interface HeaderProps {
  page: Page;
  onOpenMobile: () => void;
}

const titles: Record<Page, { title: string; subtitle: string }> = {
  dashboard: {
    title: 'Welcome to PhishGuard AI',
    subtitle: 'Your intelligent shield against phishing threats.',
  },
  history: { title: 'Scan History', subtitle: 'Review every analysis your account has run.' },
  about: { title: 'About PhishGuard AI', subtitle: 'Understand the technology keeping you safe.' },

};

export function Header({ page, onOpenMobile }: HeaderProps) {
  const { title, subtitle } = titles[page];
  return (
    <header className="sticky top-0 z-20 bg-white/80 backdrop-blur-md border-b border-navy-100">
      <div className="flex items-center gap-4 px-4 sm:px-6 lg:px-8 h-16">
        <button
          className="lg:hidden text-navy-700 hover:text-navy-900"
          onClick={onOpenMobile}
          aria-label="Open menu"
        >
          <Menu className="h-6 w-6" />
        </button>

        <div className="min-w-0">
          <h1 className="text-base sm:text-lg font-bold text-navy-900 leading-tight truncate">
            {title}
          </h1>
          <p className="text-xs sm:text-sm text-navy-500 truncate">{subtitle}</p>
        </div>

        <div className="ml-auto flex items-center gap-1.5 sm:gap-2">
          <button
            className="relative grid place-items-center h-9 w-9 rounded-lg text-navy-600 hover:bg-navy-50 transition"
            aria-label="Notifications"
          >
            <Bell className="h-5 w-5" />
            <span className="absolute top-2 right-2 h-2 w-2 rounded-full bg-iris-500 ring-2 ring-white" />
          </button>
          <button
            className="grid place-items-center h-9 w-9 rounded-lg text-navy-600 hover:bg-navy-50 transition"
            aria-label="Profile"
          >
            <UserCircle className="h-6 w-6" />
          </button>
          <div className="hidden sm:flex items-center gap-2 pl-2 ml-1 border-l border-navy-100">
            <div className="grid place-items-center h-9 w-9 rounded-full bg-gradient-to-br from-iris-500 to-navy-600 text-white font-semibold text-sm">
              AK
            </div>
            <div className="leading-tight">
              <p className="text-sm font-semibold text-navy-900">Alex Kim</p>
              <p className="text-[11px] text-navy-500">Security Analyst</p>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
