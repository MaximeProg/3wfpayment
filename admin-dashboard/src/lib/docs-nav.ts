export interface DocPage {
  slug: string;
  title: string;
  description: string;
}

export interface DocGroup {
  title: string;
  items: DocPage[];
}

export const DOCS_NAV: DocGroup[] = [
  {
    title: "Demarrage",
    items: [
      { slug: "overview", title: "Vue d'ensemble", description: "Ce qu'est Payment Platform et comment demarrer." },
      { slug: "getting-started", title: "Obtenir un projet et une cle API", description: "Projets, cles API et scopes." },
      { slug: "authentication", title: "Authentification", description: "Echanger une cle API contre un token." },
    ],
  },
  {
    title: "Integration",
    items: [
      { slug: "reference-data", title: "Donnees de reference", description: "Pays, reseaux, channels, devises." },
      { slug: "deposits", title: "Depots", description: "Encaisser un paiement entrant (cash-in)." },
      { slug: "withdrawals", title: "Retraits", description: "Envoyer un paiement sortant (cash-out)." },
      { slug: "crypto-sends", title: "Crypto sends", description: "Fonctionnalite actuellement en pause." },
    ],
  },
  {
    title: "Suivi et fiabilite",
    items: [
      { slug: "transactions", title: "Statuts et transactions", description: "Cycle de vie, polling, idempotence, pagination." },
      { slug: "errors", title: "Erreurs", description: "Codes HTTP et formats d'erreur." },
      { slug: "security", title: "Securite et limites", description: "Bonnes pratiques et quotas." },
    ],
  },
  {
    title: "Ressources",
    items: [
      { slug: "resources", title: "Doc interactive et support", description: "Swagger, ReDoc, contacts." },
    ],
  },
];

export function docHref(slug: string): string {
  return slug === "overview" ? "/docs" : `/docs/${slug}`;
}

export function findDocMeta(slug: string): DocPage | undefined {
  for (const group of DOCS_NAV) {
    const found = group.items.find((item) => item.slug === slug);
    if (found) return found;
  }
  return undefined;
}

export function getAllDocSlugs(): string[] {
  return DOCS_NAV.flatMap((group) => group.items.map((item) => item.slug)).filter((slug) => slug !== "overview");
}

export function findAdjacentDocs(slug: string): { prev: DocPage | null; next: DocPage | null } {
  const flat = DOCS_NAV.flatMap((group) => group.items);
  const index = flat.findIndex((item) => item.slug === slug);
  if (index === -1) return { prev: null, next: null };
  return {
    prev: index > 0 ? flat[index - 1] : null,
    next: index < flat.length - 1 ? flat[index + 1] : null,
  };
}
