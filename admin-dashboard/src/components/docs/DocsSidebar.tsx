"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { X } from "lucide-react";
import { DOCS_NAV, docHref } from "@/lib/docs-nav";

function NavGroups({ onNavigate }: { onNavigate?: () => void }) {
  const pathname = usePathname();

  return (
    <nav className="flex flex-1 flex-col gap-6 px-3">
      {DOCS_NAV.map((group) => (
        <div key={group.title}>
          <p className="px-3 text-xs font-semibold tracking-wide text-muted uppercase">{group.title}</p>
          <div className="mt-1.5 flex flex-col gap-0.5">
            {group.items.map((item) => {
              const href = docHref(item.slug);
              const active = pathname === href;
              return (
                <Link
                  key={item.slug}
                  href={href}
                  onClick={onNavigate}
                  className={`rounded-lg px-3 py-1.5 text-sm font-medium transition-colors ${
                    active
                      ? "bg-accent text-accent-foreground"
                      : "text-muted hover:bg-border/40 hover:text-foreground"
                  }`}
                >
                  {item.title}
                </Link>
              );
            })}
          </div>
        </div>
      ))}
    </nav>
  );
}

export function DesktopDocsSidebar() {
  return (
    <aside className="hidden w-72 shrink-0 flex-col border-r border-border bg-surface md:flex">
      <div className="flex h-16 shrink-0 items-center gap-2 border-b border-border px-5">
        <div className="h-2.5 w-2.5 rounded-full bg-accent" />
        <span className="text-sm font-semibold text-foreground">Payment Platform</span>
        <span className="ml-auto rounded-full bg-border/50 px-2 py-0.5 text-[11px] font-medium text-muted">Docs</span>
      </div>
      <div className="flex flex-1 flex-col overflow-y-auto py-5">
        <NavGroups />
      </div>
    </aside>
  );
}

export function MobileDocsSidebar({ open, onClose }: { open: boolean; onClose: () => void }) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-40 md:hidden">
      <div className="absolute inset-0 bg-black/40" onClick={onClose} />
      <div className="absolute inset-y-0 left-0 flex w-80 flex-col bg-surface shadow-xl">
        <div className="flex h-16 shrink-0 items-center justify-between border-b border-border px-5">
          <div className="flex items-center gap-2">
            <div className="h-2.5 w-2.5 rounded-full bg-accent" />
            <span className="text-sm font-semibold text-foreground">Payment Platform</span>
          </div>
          <button onClick={onClose} aria-label="Fermer le menu" className="text-muted">
            <X className="h-5 w-5" />
          </button>
        </div>
        <div className="flex flex-1 flex-col overflow-y-auto py-5">
          <NavGroups onNavigate={onClose} />
        </div>
      </div>
    </div>
  );
}
