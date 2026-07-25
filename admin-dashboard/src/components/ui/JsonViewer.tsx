export function JsonViewer({ data }: { data: unknown }) {
  const empty = data === null || data === undefined || (typeof data === "object" && Object.keys(data as object).length === 0);
  if (empty) {
    return <p className="text-xs text-muted-foreground">Vide</p>;
  }
  return (
    <pre className="max-h-96 overflow-auto rounded-lg bg-background p-3 text-xs text-foreground">
      {JSON.stringify(data, null, 2)}
    </pre>
  );
}
