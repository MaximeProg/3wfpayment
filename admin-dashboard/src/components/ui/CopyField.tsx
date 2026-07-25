"use client";

import { useState } from "react";
import { Copy, Check } from "lucide-react";

export function CopyField({ value }: { value: string }) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    await navigator.clipboard.writeText(value);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }

  return (
    <div className="flex items-center gap-2 rounded-lg border border-border bg-background px-3 py-2">
      <code className="flex-1 overflow-x-auto whitespace-nowrap text-xs text-foreground">{value}</code>
      <button
        onClick={handleCopy}
        aria-label="Copier"
        className="shrink-0 text-muted hover:text-foreground"
      >
        {copied ? <Check className="h-4 w-4 text-success" /> : <Copy className="h-4 w-4" />}
      </button>
    </div>
  );
}
