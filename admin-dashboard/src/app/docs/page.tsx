import { DocArticle } from "@/components/docs/DocArticle";
import { getDocMarkdown } from "@/lib/docs-content";
import { findDocMeta } from "@/lib/docs-nav";

export default function DocsIndexPage() {
  const meta = findDocMeta("overview")!;
  const content = getDocMarkdown("overview");
  return <DocArticle meta={meta} content={content} />;
}
