"use client";

import { monitoringApi } from "@/lib/api";
import { useFetch } from "@/lib/use-fetch";
import { Card, CardHeader, CardBody } from "@/components/ui/Card";
import { PageSpinner, ErrorBanner, EmptyState } from "@/components/ui/Feedback";
import { HealthBadge, ErrorLevelBadge } from "@/components/ui/Badge";
import { Table, Thead, Tbody, Tr, Th, Td } from "@/components/ui/Table";
import { formatDateTime } from "@/lib/format";

export default function MonitoringPage() {
  const health = useFetch(() => monitoringApi.health(), []);
  const errors = useFetch(() => monitoringApi.errors({ limit: 50 }), []);

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-xl font-semibold text-foreground">Monitoring</h1>
        <p className="text-sm text-muted">Disponibilite des services et erreurs recentes.</p>
      </div>

      <Card>
        <CardHeader title="Etat des services" />
        {health.loading ? (
          <PageSpinner />
        ) : health.error ? (
          <div className="p-5">
            <ErrorBanner message={health.error} />
          </div>
        ) : health.data ? (
          <CardBody className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div className="flex items-center justify-between rounded-lg border border-border p-3">
              <span className="text-sm text-foreground">Base de donnees</span>
              <HealthBadge value={health.data.database} />
            </div>
            <div className="flex items-center justify-between rounded-lg border border-border p-3">
              <span className="text-sm text-foreground">Yellow Card Sandbox</span>
              <HealthBadge value={health.data.yellowcard_sandbox} />
            </div>
            <div className="flex items-center justify-between rounded-lg border border-border p-3">
              <span className="text-sm text-foreground">Yellow Card Production</span>
              <HealthBadge value={health.data.yellowcard_production} />
            </div>
          </CardBody>
        ) : null}
      </Card>

      <Card>
        <CardHeader title="Erreurs recentes" />
        {errors.loading ? (
          <PageSpinner />
        ) : errors.error ? (
          <div className="p-5">
            <ErrorBanner message={errors.error} />
          </div>
        ) : errors.data && errors.data.length > 0 ? (
          <Table>
            <Thead>
              <Tr>
                <Th>Source</Th>
                <Th>Niveau</Th>
                <Th>Message</Th>
                <Th>Survenue le</Th>
              </Tr>
            </Thead>
            <Tbody>
              {errors.data.map((err) => (
                <Tr key={err.id}>
                  <Td className="whitespace-nowrap">{err.source}</Td>
                  <Td>
                    <ErrorLevelBadge level={err.level} />
                  </Td>
                  <Td className="max-w-md truncate" title={err.message}>
                    {err.message}
                  </Td>
                  <Td className="text-muted whitespace-nowrap">{formatDateTime(err.created_at)}</Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        ) : (
          <EmptyState title="Aucune erreur" hint="Bon signe : rien a signaler pour le moment." />
        )}
      </Card>
    </div>
  );
}
