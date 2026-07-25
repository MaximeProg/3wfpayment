"use client";

import { useState, type ReactNode } from "react";
import { useRequireAuth } from "@/lib/auth-context";
import { DesktopSidebar, MobileSidebar } from "./Sidebar";
import { Topbar } from "./Topbar";
import { PageSpinner } from "@/components/ui/Feedback";

export function DashboardShell({ children }: { children: ReactNode }) {
  const { admin, loading } = useRequireAuth();
  const [mobileOpen, setMobileOpen] = useState(false);

  if (loading || !admin) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background">
        <PageSpinner />
      </div>
    );
  }

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <DesktopSidebar />
      <MobileSidebar open={mobileOpen} onClose={() => setMobileOpen(false)} />
      <div className="flex min-w-0 flex-1 flex-col">
        <Topbar onMenuClick={() => setMobileOpen(true)} />
        <main className="flex-1 overflow-y-auto px-4 py-6 sm:px-6 lg:px-8">
          <div className="mx-auto w-full max-w-7xl">{children}</div>
        </main>
      </div>
    </div>
  );
}
