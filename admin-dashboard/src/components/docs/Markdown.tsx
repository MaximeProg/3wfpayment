import type { ReactNode } from "react";
import Link from "next/link";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function slugify(value: string): string {
  return value
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

function textContent(node: ReactNode): string {
  if (typeof node === "string") return node;
  if (typeof node === "number") return String(node);
  if (Array.isArray(node)) return node.map(textContent).join("");
  if (node && typeof node === "object" && "props" in node) {
    return textContent((node as { props: { children?: ReactNode } }).props.children);
  }
  return "";
}

function Heading({ level, children }: { level: 2 | 3; children: ReactNode }) {
  const id = slugify(textContent(children));
  const Tag = level === 2 ? "h2" : "h3";
  const className =
    level === 2
      ? "mt-10 scroll-mt-24 text-xl font-semibold text-foreground first:mt-0"
      : "mt-8 scroll-mt-24 text-base font-semibold text-foreground";
  return (
    <Tag id={id} className={`${className} text-balance`}>
      <a href={`#${id}`} className="no-underline hover:underline">
        {children}
      </a>
    </Tag>
  );
}

export function Markdown({ content }: { content: string }) {
  return (
    <div className="max-w-[72ch] text-[15px] leading-7 text-foreground">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({ children }) => <Heading level={2}>{children}</Heading>,
          h2: ({ children }) => <Heading level={2}>{children}</Heading>,
          h3: ({ children }) => <Heading level={3}>{children}</Heading>,
          p: ({ children }) => <p className="mt-4 first:mt-0">{children}</p>,
          a: ({ href, children }) => {
            if (href?.startsWith("/")) {
              return (
                <Link href={href} className="text-accent underline decoration-accent/30 underline-offset-2 hover:decoration-accent">
                  {children}
                </Link>
              );
            }
            return (
              <a
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                className="text-accent underline decoration-accent/30 underline-offset-2 hover:decoration-accent"
              >
                {children}
              </a>
            );
          },
          ul: ({ children }) => <ul className="mt-4 flex flex-col gap-2 pl-5 [&>li]:list-disc">{children}</ul>,
          ol: ({ children }) => <ol className="mt-4 flex flex-col gap-2 pl-5 [&>li]:list-decimal">{children}</ol>,
          li: ({ children }) => <li className="pl-1 marker:text-muted">{children}</li>,
          strong: ({ children }) => <strong className="font-semibold text-foreground">{children}</strong>,
          code: ({ className, children }) => {
            const isBlock = Boolean(className);
            if (isBlock) return <code className={className}>{children}</code>;
            return (
              <code className="rounded bg-border/50 px-1.5 py-0.5 font-mono text-[13px] text-foreground">
                {children}
              </code>
            );
          },
          pre: ({ children }) => (
            <pre className="mt-4 overflow-x-auto rounded-lg border border-border bg-background px-4 py-3.5 font-mono text-[13px] leading-6 text-foreground">
              {children}
            </pre>
          ),
          table: ({ children }) => (
            <div className="mt-4 overflow-x-auto rounded-lg border border-border">
              <table className="w-full min-w-[560px] border-collapse text-sm">{children}</table>
            </div>
          ),
          thead: ({ children }) => (
            <thead className="border-b border-border bg-border/20 text-left text-xs text-muted uppercase">
              {children}
            </thead>
          ),
          th: ({ children }) => <th className="px-3.5 py-2.5 font-medium">{children}</th>,
          tbody: ({ children }) => <tbody className="divide-y divide-border">{children}</tbody>,
          td: ({ children }) => <td className="px-3.5 py-2.5 align-top text-foreground">{children}</td>,
          hr: () => <hr className="my-8 border-border" />,
          blockquote: ({ children }) => (
            <blockquote className="mt-4 border-l-2 border-accent/40 pl-4 text-muted">{children}</blockquote>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
