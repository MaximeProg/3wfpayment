import Link from "next/link";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { Markdown } from "./Markdown";
import { docHref, findAdjacentDocs, type DocPage } from "@/lib/docs-nav";

export function DocArticle({ meta, content }: { meta: DocPage; content: string }) {
  const { prev, next } = findAdjacentDocs(meta.slug);

  return (
    <article>
      <header>
        <h1 className="text-2xl font-semibold text-balance text-foreground">{meta.title}</h1>
        <p className="mt-2 text-[15px] text-muted">{meta.description}</p>
      </header>

      <div className="mt-8">
        <Markdown content={content} />
      </div>

      {(prev || next) && (
        <nav className="mt-14 flex items-center justify-between gap-4 border-t border-border pt-6">
          {prev ? (
            <Link
              href={docHref(prev.slug)}
              className="group flex flex-col items-start gap-0.5 rounded-lg px-3 py-2 text-left transition hover:bg-border/40"
            >
              <span className="flex items-center gap-1 text-xs text-muted">
                <ArrowLeft className="h-3 w-3" /> Precedent
              </span>
              <span className="text-sm font-medium text-foreground">{prev.title}</span>
            </Link>
          ) : (
            <span />
          )}
          {next ? (
            <Link
              href={docHref(next.slug)}
              className="group flex flex-col items-end gap-0.5 rounded-lg px-3 py-2 text-right transition hover:bg-border/40"
            >
              <span className="flex items-center gap-1 text-xs text-muted">
                Suivant <ArrowRight className="h-3 w-3" />
              </span>
              <span className="text-sm font-medium text-foreground">{next.title}</span>
            </Link>
          ) : (
            <span />
          )}
        </nav>
      )}
    </article>
  );
}
