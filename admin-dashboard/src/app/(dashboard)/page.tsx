"use client";

import Link from "next/link";
import { dashboardApi } from "@/lib/api";
import { useFetch } from "@/lib/use-fetch";
import { StatTile, Card, CardHeader, CardBody } from "@/components/ui/Card";
import { PageSpinner, ErrorBanner, EmptyState } from "@/components/ui/Feedback";
import { Badge, StatusBadge } from "@/components/ui/Badge";
import { Table, Thead, Tbody, Tr, Th, Td } from "@/components/ui/Table";
import { formatAmount } from "@/lib/format";

const ENV_LABELS: Record<string, string> = {
  sandbox: "Sandbox",
  production: "Production",
};

function YellowCardBalanceCard() {
  const balances = useFetch(() => dashboardApi.yellowCardBalance(), []);

  return (
    <Card>
      <CardHeader title="Solde Yellow Card" />
      {balances.loading ? (
        <div className="p-5">
          <PageSpinner />
        </div>
      ) : balances.error ? (
        <div className="p-5">
          <ErrorBanner message={balances.error} />
        </div>
      ) : balances.data && balances.data.length > 0 ? (
        <CardBody className="flex flex-col gap-4">
          {balances.data.map((entry) => (
            <div key={entry.environment} className="flex flex-col gap-2">
              <Badge tone={entry.environment === "production" ? "info" : "neutral"}>
                {ENV_LABELS[entry.environment] ?? entry.environment}
              </Badge>
              {entry.accounts.length === 0 ? (
                <p className="text-xs text-muted-foreground">Aucun compte</p>
              ) : (
                <div className="flex flex-wrap gap-x-6 gap-y-1">
                  {entry.accounts.map((account) => (
                    <span key={account.currency} className="text-sm font-medium text-foreground">
                      {formatAmount(account.available, account.currency)}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </CardBody>
      ) : (
        <EmptyState title="Aucun environnement Yellow Card configure" />
      )}
    </Card>
  );
}

const STATUS_LABELS: Record<string, string> = {
  pending: "En attente",
  processing: "En cours",
  completed: "Terminees",
  failed: "Echouees",
  cancelled: "Annulees",
  expired: "Expirees",
};

const TYPE_LABELS: Record<string, string> = {
  deposit: "Depots",
  withdrawal: "Retraits",
  crypto_send: "Crypto sends",
};

export default function OverviewPage() {
  const overview = useFetch(() => dashboardApi.overview(), []);
  const byProject = useFetch(() => dashboardApi.byProject(), []);

  if (overview.loading || byProject.loading) return <PageSpinner />;
  if (overview.error) return <ErrorBanner message={overview.error} />;
  if (!overview.data) return null;

  const { total_transactions, total_projects, active_projects, by_status, by_type } = overview.data;

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-xl font-semibold text-foreground">Vue d&apos;ensemble</h1>
        <p className="text-sm text-muted">Activite globale de la plateforme, tous projets confondus.</p>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatTile label="Transactions totales" value={total_transactions} />
        <StatTile label="Projets actifs" value={`${active_projects} / ${total_projects}`} />
        <StatTile label="Terminees" value={by_status.completed} hint="Statut completed" />
        <StatTile
          label="A surveiller"
          value={by_status.failed + by_status.pending}
          hint="Echouees + en attente"
        />
      </div>

      <YellowCardBalanceCard />

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader title="Transactions par statut" />
          <CardBody className="flex flex-col gap-3">
            {Object.entries(by_status).map(([status, count]) => (
              <div key={status} className="flex items-center justify-between text-sm">
                <StatusBadge status={status} />
                <span className="font-medium text-foreground">
                  {count}
                  <span className="ml-1 text-xs font-normal text-muted">
                    {STATUS_LABELS[status] ?? status}
                  </span>
                </span>
              </div>
            ))}
          </CardBody>
        </Card>

        <Card>
          <CardHeader title="Transactions par type" />
          <CardBody className="flex flex-col gap-3">
            {Object.keys(TYPE_LABELS).map((type) => (
              <div key={type} className="flex items-center justify-between text-sm">
                <span className="text-muted">{TYPE_LABELS[type]}</span>
                <span className="font-medium text-foreground">{by_type[type] ?? 0}</span>
              </div>
            ))}
          </CardBody>
        </Card>
      </div>

      <Card>
        <CardHeader title="Activite par projet" />
        {byProject.data && byProject.data.length > 0 ? (
          <Table>
            <Thead>
              <Tr>
                <Th>Projet</Th>
                <Th>Total</Th>
                <Th>Terminees</Th>
                <Th>En attente</Th>
                <Th>Echouees</Th>
              </Tr>
            </Thead>
            <Tbody>
              {byProject.data.map((row) => (
                <Tr key={row.project_id}>
                  <Td>
                    <Link
                      href={`/projects/${row.project_id}`}
                      className="font-medium text-accent hover:underline"
                    >
                      {row.project_name}
                    </Link>
                    <span className="ml-2 text-xs text-muted">{row.project_slug}</span>
                  </Td>
                  <Td>{row.total_transactions}</Td>
                  <Td>{row.by_status.completed}</Td>
                  <Td>{row.by_status.pending + row.by_status.processing}</Td>
                  <Td>{row.by_status.failed}</Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        ) : (
          <EmptyState title="Aucun projet" hint="Cree un projet pour voir son activite ici." />
        )}
      </Card>
    </div>
  );
}
