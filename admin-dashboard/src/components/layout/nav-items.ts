import {
  LayoutDashboard,
  ArrowLeftRight,
  FolderKanban,
  Webhook,
  Activity,
  ScrollText,
  Settings,
  Users,
  type LucideIcon,
} from "lucide-react";

export interface NavItem {
  href: string;
  label: string;
  icon: LucideIcon;
  superAdminOnly?: boolean;
}

export const NAV_ITEMS: NavItem[] = [
  { href: "/", label: "Vue d'ensemble", icon: LayoutDashboard },
  { href: "/transactions", label: "Transactions", icon: ArrowLeftRight },
  { href: "/projects", label: "Projets & cles API", icon: FolderKanban },
  { href: "/webhooks", label: "Webhooks", icon: Webhook },
  { href: "/monitoring", label: "Monitoring", icon: Activity },
  { href: "/audit", label: "Journal d'audit", icon: ScrollText },
  { href: "/admins", label: "Administrateurs", icon: Users, superAdminOnly: true },
  { href: "/settings", label: "Parametres", icon: Settings },
];
