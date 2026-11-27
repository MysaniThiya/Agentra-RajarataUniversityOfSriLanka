import { ShieldCheck, LayoutDashboard, X } from 'lucide-react';
import type { Page } from '@/types';

interface SidebarProps {
  current: Page;
  onNavigate: (page: Page) => void;
  mobileOpen: boolean;
  onCloseMobile: () => void;
}

const navItems: { id: Page; label: string; icon: typeof LayoutDashboard }[] = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
];

export function Sidebar({ current, onNavigate, mobileOpen, onCloseMobile }: SidebarProps) {
  return (
    <>
      {/* mobile backdrop */}
      {mobileOpen && (
        <div
          className="fixed inset-0 z-30 bg-navy-950/60 backdrop-blur-sm lg:hidden"
          onClick={onCloseMobile}
        />
      )}

      <aside
        className={`fixed z-40 inset-y-0 left-0 w-64 bg-navy-900 flex flex-col transition-transform duration-300
          lg:translate-x-0 lg:static lg:z-auto
          ${mobileOpen ? 'translate-x-0' : '-translate-x-full'}`}
      >
        {/* logo */}
        <div className="flex items-center justify-between px-5 h-16 border-b border-white/5">
          <div className="flex items-center gap-2.5">
            <div className="grid place-items-center h-9 w-9 rounded-xl bg-gradient-to-br from-iris-500 to-navy-600 shadow-glow">
              <ShieldCheck className="h-5 w-5 text-white" />
            </div>
            <div className="leading-tight">
              <p className="text-white font-bold text-[15px] tracking-tight">PhishGuard</p>
              <p className="text-iris-300 text-[10px] font-semibold tracking-[0.18em] uppercase">AI</p>
            </div>
          </div>
          <button
            className="lg:hidden text-navy-200 hover:text-white"
            onClick={onCloseMobile}
            aria-label="Close menu"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* nav */}
        <nav className="flex-1 px-3 py-5 space-y-1">
          <p className="px-3.5 pb-2 text-[10px] font-semibold uppercase tracking-wider text-navy-400">
            Menu
          </p>
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = current === item.id;
            return (
              <button
                key={item.id}
                onClick={() => {
                  onNavigate(item.id);
                  onCloseMobile();
                }}
                className={`nav-item w-full ${active ? 'nav-item-active' : ''}`}
              >
                <Icon className="h-[18px] w-[18px]" />
                {item.label}
                {active && <span className="ml-auto h-1.5 w-1.5 rounded-full bg-iris-400" />}
              </button>
            );
          })}
        </nav>

        {/* status footer */}
        <div className="m-3 rounded-xl bg-navy-800/60 p-3.5 border border-white/5">
          <div className="flex items-center gap-2">
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75 animate-ping" />
              <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-500" />
            </span>
            <p className="text-xs font-medium text-navy-100">Detection engine online</p>
          </div>
          <p className="mt-2 text-[11px] text-navy-400">Multi-agent analysis ready</p>
        </div>
      </aside>
    </>
  );
}
