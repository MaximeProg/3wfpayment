"use client";

import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { transactionsApi } from "@/lib/api";
import { useFetch } from "@/lib/use-fetch";
import { Card, CardHeader, CardBody } from "@/components/ui/Card";
import { PageSpinner, ErrorBanner } from "@/components/ui/Feedback";
import { StatusBadge } from "@/components/ui/Badge";
import { JsonViewer } from "@/components/ui/JsonViewer";
import { formatAmount, formatDateTime } from "@/lib/format";

export function TransactionDetailClient({ id }: { id: string }) {
  const { data: tx, loading, error } = useFetch(() => transactionsApi.get(id), [id]);

  if (loading) return <PageSpinner />;
  if (error) return <ErrorBanner message={error} />;
  if (!tx) return null;

  return (
    <div className="flex flex-col gap-6">
      <div>
        <Link href="/transactions" className="inline-flex items-center gap-1 text-sm text-muted hover:text-foreground">
          <ArrowLeft className="h-4 w-4" /> Retour aux transactions
        </Link>
        <div className="mt-2 flex flex-wrap items-center gap-3">
          <h1 className="text-xl font-semibold text-foreground">{tx.reference}</h1>
          <StatusBadge status={tx.status} />
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card className="p-4">
          <p className="text-xs font-medium uppercase text-muted">Type</p>
          <p className="mt-1 text-sm font-medium capitalize text-foreground">{tx.type.replace("_", " ")}</p>
        </Card>
        <Card className="p-4">
          <p className="text-xs font-medium uppercase text-muted">Montant</p>
          <p className="mt-1 text-sm font-medium text-foreground">{formatAmount(tx.amount, tx.currency_code)}</p>
        </Card>
        <Card className="p-4">
          <p className="text-xs font-medium uppercase text-muted">Reference client</p>
          <p className="mt-1 text-sm font-medium text-foreground">{tx.client_reference ?? "—"}</p>
        </Card>
        <Card className="p-4">
          <p className="text-xs font-medium uppercase text-muted">Reference Yellow Card</p>
          <p className="mt-1 break-all text-sm font-medium text-foreground">{tx.yellowcard_reference ?? "—"}</p>
        </Card>
      </div>

      {tx.failure_reason && (
        <ErrorBanner message={`Motif d'echec : ${tx.failure_reason}`} />
      )}

      <Card>
        <CardHeader title="Historique des statuts" />
        <CardBody className="flex flex-col gap-3">
          {tx.status_history.length === 0 ? (
            <p className="text-sm text-muted-foreground">Aucun historique</p>
          ) : (
            tx.status_history.map((entry) => (
              <div key={entry.id} className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  {entry.previous_status && (
                    <>
                      <StatusBadge status={entry.previous_status} />
                      <span className="text-muted">→</span>
                    </>
                  )}
                  <StatusBadge status={entry.new_status} />
                  <span className="text-xs text-muted-foreground">({entry.source})</span>
                </div>
                <span className="text-xs text-muted">{formatDateTime(entry.created_at)}</span>
              </div>
            ))
          )}
        </CardBody>
      </Card>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card>
          <CardHeader title="Donnees client" />
          <CardBody>
            <JsonViewer data={tx.customer_payload} />
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Requete envoyee a Yellow Card" />
          <CardBody>
            <JsonViewer data={tx.request_payload} />
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Derniere reponse Yellow Card" />
          <CardBody>
            <JsonViewer data={tx.response_payload} />
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
