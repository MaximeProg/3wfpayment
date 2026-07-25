"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { LogOut, X } from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { NAV_ITEMS } from "./nav-items";

const ROLE_LABELS: Record<string, string> = {
  super_admin: "Super admin",
  admin: "Admin",
  viewer: "Lecteur",
};

function SidebarFooter() {
  const { admin, logout } = useAuth();
  const router = useRouter();
  const [loggingOut, setLoggingOut] = useState(false);

  if (!admin) return null;

  async function handleLogout() {
    setLoggingOut(true);
    await logout();
    router.replace("/login");
  }

  return (
    <div className="mt-auto flex items-center gap-3 border-t border-border px-3 py-3">
      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-accent text-xs font-semibold text-accent-foreground">
        {admin.email.slice(0, 2).toUpperCase()}
      </div>
      <div className="min-w-0 flex-1 leading-tight">
        <p className="truncate text-sm font-medium text-foreground">{admin.email}</p>
        <p className="text-xs text-muted">{ROLE_LABELS[admin.role] ?? admin.role}</p>
      </div>
      <button
        onClick={handleLogout}
        disabled={loggingOut}
        aria-label="Se deconnecter"
        className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-muted transition hover:bg-border/40 hover:text-foreground disabled:opacity-50"
      >
        <LogOut className="h-4 w-4" />
      </button>
    </div>
  );
}

function isActive(pathname: string, href: string): boolean {
  if (href === "/") return pathname === "/";
  return pathname === href || pathname.startsWith(`${href}/`);
}

function NavLinks({ onNavigate }: { onNavigate?: () => void }) {
  const pathname = usePathname();
  const { admin } = useAuth();
  const items = NAV_ITEMS.filter((item) => !item.superAdminOnly || admin?.role === "super_admin");
  return (
    <nav className="flex flex-1 flex-col gap-1 px-3">
      {items.map((item) => {
        const active = isActive(pathname, item.href);
        const Icon = item.icon;
        return (
          <Link
            key={item.href}
            href={item.href}
            onClick={onNavigate}
            className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
              active
                ? "bg-accent text-accent-foreground"
                : "text-muted hover:bg-border/40 hover:text-foreground"
            }`}
          >
            <Icon className="h-4 w-4 shrink-0" />
            {item.label}
          </Link>
        );
      })}
    </nav>
  );
}

export function DesktopSidebar() {
  return (
    <aside className="hidden w-64 shrink-0 flex-col border-r border-border bg-surface md:flex">
      <div className="flex h-16 shrink-0 items-center gap-2 border-b border-border px-5">
        <div className="h-2.5 w-2.5 rounded-full bg-accent" />
        <span className="text-sm font-semibold text-foreground">Payment Platform</span>
      </div>
      <div className="flex flex-1 flex-col overflow-y-auto py-4">
        <NavLinks />
      </div>
      <SidebarFooter />
    </aside>
  );
}

export function MobileSidebar({ open, onClose }: { open: boolean; onClose: () => void }) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-40 md:hidden">
      <div className="absolute inset-0 bg-black/40" onClick={onClose} />
      <div className="absolute inset-y-0 left-0 flex w-72 flex-col bg-surface shadow-xl">
        <div className="flex h-16 items-center justify-between border-b border-border px-5">
          <div className="flex items-center gap-2">
            <div className="h-2.5 w-2.5 rounded-full bg-accent" />
            <span className="text-sm font-semibold text-foreground">Payment Platform</span>
          </div>
          <button onClick={onClose} aria-label="Fermer le menu" className="text-muted">
            <X className="h-5 w-5" />
          </button>
        </div>
        <div className="flex flex-1 flex-col overflow-y-auto py-4">
          <NavLinks onNavigate={onClose} />
        </div>
        <SidebarFooter />
      </div>
    </div>
  );
}
