"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowLeft, KeyRound, RefreshCw, Ban } from "lucide-react";
import { projectsApi, ApiError } from "@/lib/api";
import { useFetch, apiErrorMessage } from "@/lib/use-fetch";
import { Card, CardHeader, CardBody } from "@/components/ui/Card";
import { PageSpinner, ErrorBanner, EmptyState } from "@/components/ui/Feedback";
import { Badge } from "@/components/ui/Badge";
import { Table, Thead, Tbody, Tr, Th, Td } from "@/components/ui/Table";
import { Button } from "@/components/ui/Button";
import { CopyField } from "@/components/ui/CopyField";
import { formatDateTime } from "@/lib/format";
import type { ApiKeyCreated } from "@/lib/types";

export function ProjectDetailClient({ id }: { id: string }) {
  const project = useFetch(() => projectsApi.get(id), [id]);
  const apiKeys = useFetch(() => projectsApi.listApiKeys(id), [id]);
  const [newKey, setNewKey] = useState<ApiKeyCreated | null>(null);
  const [busyKeyId, setBusyKeyId] = useState<string | null>(null);
  const [statusBusy, setStatusBusy] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);

  async function handleCreateKey() {
    setActionError(null);
    try {
      const created = await projectsApi.createApiKey(id);
      setNewKey(created);
      apiKeys.reload();
    } catch (err) {
      setActionError(err instanceof ApiError ? apiErrorMessage(err) : "Creation impossible");
    }
  }

  async function handleRotate(keyId: string) {
    setBusyKeyId(keyId);
    setActionError(null);
    try {
      const created = await projectsApi.rotateApiKey(keyId);
      setNewKey(created);
      apiKeys.reload();
    } catch (err) {
      setActionError(err instanceof ApiError ? apiErrorMessage(err) : "Rotation impossible");
    } finally {
      setBusyKeyId(null);
    }
  }

  async function handleRevoke(keyId: string) {
    setBusyKeyId(keyId);
    setActionError(null);
    try {
      await projectsApi.revokeApiKey(keyId);
      apiKeys.reload();
    } catch (err) {
      setActionError(err instanceof ApiError ? apiErrorMessage(err) : "Revocation impossible");
    } finally {
      setBusyKeyId(null);
    }
  }

  async function handleToggleStatus() {
    if (!project.data) return;
    setStatusBusy(true);
    setActionError(null);
    try {
      const nextStatus = project.data.status === "active" ? "inactive" : "active";
      await projectsApi.update(id, { status: nextStatus });
      project.reload();
    } catch (err) {
      setActionError(err instanceof ApiError ? apiErrorMessage(err) : "Mise a jour impossible");
    } finally {
      setStatusBusy(false);
    }
  }

  if (project.loading) return <PageSpinner />;
  if (project.error) return <ErrorBanner message={project.error} />;
  if (!project.data) return null;

  return (
    <div className="flex flex-col gap-6">
      <div>
        <Link href="/projects" className="inline-flex items-center gap-1 text-sm text-muted hover:text-foreground">
          <ArrowLeft className="h-4 w-4" /> Retour aux projets
        </Link>
        <div className="mt-2 flex flex-wrap items-center gap-3">
          <h1 className="text-xl font-semibold text-foreground">{project.data.name}</h1>
          <Badge tone={project.data.status === "active" ? "success" : project.data.status === "suspended" ? "danger" : "neutral"}>
            {project.data.status}
          </Badge>
          <Badge tone="neutral">{project.data.environment}</Badge>
        </div>
        {project.data.description && <p className="mt-1 text-sm text-muted">{project.data.description}</p>}
      </div>

      {actionError && <ErrorBanner message={actionError} />}

      {newKey && (
        <Card className="border-accent/40">
          <CardHeader title="Nouvelle cle API — a copier maintenant" action={
            <Button variant="ghost" size="sm" onClick={() => setNewKey(null)}>Fermer</Button>
          } />
          <CardBody className="flex flex-col gap-2">
            <p className="text-xs text-warning">
              Cette cle complete ne sera plus jamais affichee. Copie-la et transmets-la de facon securisee au projet consommateur.
            </p>
            <CopyField value={newKey.full_key} />
          </CardBody>
        </Card>
      )}

      <Card>
        <CardHeader title="Parametres du projet" action={
          <Button variant="secondary" size="sm" loading={statusBusy} onClick={handleToggleStatus}>
            {project.data.status === "active" ? "Desactiver" : "Activer"}
          </Button>
        } />
        <CardBody className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          <div>
            <p className="text-xs font-medium uppercase text-muted">Slug</p>
            <p className="text-sm text-foreground">{project.data.slug}</p>
          </div>
          <div>
            <p className="text-xs font-medium uppercase text-muted">Cree le</p>
            <p className="text-sm text-foreground">{formatDateTime(project.data.created_at)}</p>
          </div>
        </CardBody>
      </Card>

      <Card>
        <CardHeader
          title="Cles API"
          action={
            <Button size="sm" onClick={handleCreateKey}>
              <KeyRound className="h-4 w-4" /> Generer une cle
            </Button>
          }
        />
        {apiKeys.loading ? (
          <PageSpinner />
        ) : apiKeys.data && apiKeys.data.length > 0 ? (
          <Table>
            <Thead>
              <Tr>
                <Th>Prefixe</Th>
                <Th>Scopes</Th>
                <Th>Statut</Th>
                <Th>Derniere utilisation</Th>
                <Th>Actions</Th>
              </Tr>
            </Thead>
            <Tbody>
              {apiKeys.data.map((key) => (
                <Tr key={key.id}>
                  <Td>
                    <code className="text-xs">pp_{key.key_prefix}_…</code>
                  </Td>
                  <Td>
                    <div className="flex flex-wrap gap-1">
                      {key.scopes.map((scope) => (
                        <Badge key={scope} tone="neutral">
                          {scope}
                        </Badge>
                      ))}
                    </div>
                  </Td>
                  <Td>
                    <Badge tone={key.status === "active" ? "success" : "neutral"}>{key.status}</Badge>
                  </Td>
                  <Td className="text-muted">{formatDateTime(key.last_used_at)}</Td>
                  <Td>
                    {key.status === "active" && (
                      <div className="flex gap-2">
                        <Button
                          variant="secondary"
                          size="sm"
                          loading={busyKeyId === key.id}
                          onClick={() => handleRotate(key.id)}
                        >
                          <RefreshCw className="h-3.5 w-3.5" /> Roter
                        </Button>
                        <Button
                          variant="danger"
                          size="sm"
                          loading={busyKeyId === key.id}
                          onClick={() => handleRevoke(key.id)}
                        >
                          <Ban className="h-3.5 w-3.5" /> Revoquer
                        </Button>
                      </div>
                    )}
                  </Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        ) : (
          <EmptyState title="Aucune cle API" hint="Genere une premiere cle pour que ce projet puisse appeler l'API." />
        )}
      </Card>
    </div>
  );
}
