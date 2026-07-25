import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { DocArticle } from "@/components/docs/DocArticle";
import { getDocMarkdown } from "@/lib/docs-content";
import { findDocMeta, getAllDocSlugs } from "@/lib/docs-nav";

export function generateStaticParams() {
  return getAllDocSlugs().map((slug) => ({ slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const meta = findDocMeta(slug);
  return { title: meta?.title ?? "Documentation" };
}

export default async function DocSlugPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const meta = findDocMeta(slug);
  if (!meta || slug === "overview") notFound();

  const content = getDocMarkdown(slug);
  return <DocArticle meta={meta} content={content} />;
}
