"use client";

import { useState } from "react";
import Link from "next/link";
import { transactionsApi, projectsApi } from "@/lib/api";
import { useFetch } from "@/lib/use-fetch";
import { Card, CardHeader } from "@/components/ui/Card";
import { PageSpinner, ErrorBanner, EmptyState } from "@/components/ui/Feedback";
import { StatusBadge } from "@/components/ui/Badge";
import { Table, Thead, Tbody, Tr, Th, Td } from "@/components/ui/Table";
import { Input, Select } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { formatAmount, formatDateTime } from "@/lib/format";

const PAGE_SIZE = 25;

export default function TransactionsPage() {
  const [projectId, setProjectId] = useState("");
  const [type, setType] = useState("");
  const [status, setStatus] = useState("");
  const [search, setSearch] = useState("");
  const [offset, setOffset] = useState(0);

  const projects = useFetch(() => projectsApi.list(), []);
  const transactions = useFetch(
    () =>
      transactionsApi.list({
        project_id: projectId || undefined,
        type: type || undefined,
        status: status || undefined,
        search: search || undefined,
        limit: PAGE_SIZE,
        offset,
      }),
    [projectId, type, status, search, offset]
  );

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-xl font-semibold text-foreground">Transactions</h1>
        <p className="text-sm text-muted">Depots, retraits et crypto sends, tous projets confondus.</p>
      </div>

      <Card>
        <CardHeader
          title="Filtres"
          action={
            <Button
              variant="secondary"
              size="sm"
              onClick={() => {
                setProjectId("");
                setType("");
                setStatus("");
                setSearch("");
                setOffset(0);
              }}
            >
              Reinitialiser
            </Button>
          }
        />
        <div className="grid grid-cols-1 gap-3 p-4 sm:grid-cols-2 lg:grid-cols-4 sm:p-5">
          <Select value={projectId} onChange={(e) => { setProjectId(e.target.value); setOffset(0); }}>
            <option value="">Tous les projets</option>
            {projects.data?.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name}
              </option>
            ))}
          </Select>
          <Select value={type} onChange={(e) => { setType(e.target.value); setOffset(0); }}>
            <option value="">Tous les types</option>
            <option value="deposit">Depot</option>
            <option value="withdrawal">Retrait</option>
            <option value="crypto_send">Crypto send</option>
          </Select>
          <Select value={status} onChange={(e) => { setStatus(e.target.value); setOffset(0); }}>
            <option value="">Tous les statuts</option>
            <option value="pending">En attente</option>
            <option value="processing">En cours</option>
            <option value="completed">Terminee</option>
            <option value="failed">Echouee</option>
            <option value="cancelled">Annulee</option>
            <option value="expired">Expiree</option>
          </Select>
          <Input
            placeholder="Reference, client_reference..."
            value={search}
            onChange={(e) => { setSearch(e.target.value); setOffset(0); }}
          />
        </div>
      </Card>

      <Card>
        {transactions.loading ? (
          <PageSpinner />
        ) : transactions.error ? (
          <div className="p-5">
            <ErrorBanner message={transactions.error} />
          </div>
        ) : transactions.data && transactions.data.length > 0 ? (
          <>
            <Table>
              <Thead>
                <Tr>
                  <Th>Reference</Th>
                  <Th>Type</Th>
                  <Th>Montant</Th>
                  <Th>Statut</Th>
                  <Th>Cree le</Th>
                </Tr>
              </Thead>
              <Tbody>
                {transactions.data.map((tx) => (
                  <Tr key={tx.id}>
                    <Td>
                      <Link href={`/transactions/${tx.id}`} className="font-medium text-accent hover:underline">
                        {tx.reference}
                      </Link>
                      {tx.client_reference && (
                        <div className="text-xs text-muted-foreground">{tx.client_reference}</div>
                      )}
                    </Td>
                    <Td className="capitalize">{tx.type.replace("_", " ")}</Td>
                    <Td>{formatAmount(tx.amount, tx.currency_code)}</Td>
                    <Td>
                      <StatusBadge status={tx.status} />
                    </Td>
                    <Td className="text-muted">{formatDateTime(tx.created_at)}</Td>
                  </Tr>
                ))}
              </Tbody>
            </Table>
            <div className="flex items-center justify-between border-t border-border px-4 py-3 sm:px-5">
              <Button
                variant="secondary"
                size="sm"
                disabled={offset === 0}
                onClick={() => setOffset(Math.max(0, offset - PAGE_SIZE))}
              >
                Precedent
              </Button>
              <span className="text-xs text-muted">Page {Math.floor(offset / PAGE_SIZE) + 1}</span>
              <Button
                variant="secondary"
                size="sm"
                disabled={transactions.data.length < PAGE_SIZE}
                onClick={() => setOffset(offset + PAGE_SIZE)}
              >
                Suivant
              </Button>
            </div>
          </>
        ) : (
          <EmptyState title="Aucune transaction" hint="Ajuste les filtres ou attends la premiere transaction." />
        )}
      </Card>
    </div>
  );
}
