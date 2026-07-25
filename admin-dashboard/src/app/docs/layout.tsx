import type { Metadata } from "next";
import { DocsShell } from "@/components/docs/DocsShell";

export const metadata: Metadata = {
  title: {
    template: "%s — Documentation Payment Platform",
    default: "Documentation — Payment Platform",
  },
  description: "Guide d'integration pour les developpeurs consommant l'API Payment Platform.",
};

export default function DocsLayout({ children }: { children: React.ReactNode }) {
  return <DocsShell>{children}</DocsShell>;
}
