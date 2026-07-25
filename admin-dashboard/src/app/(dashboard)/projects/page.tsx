"use client";

import { useState, type FormEvent } from "react";
import Link from "next/link";
import { Plus, X } from "lucide-react";
import { projectsApi, ApiError } from "@/lib/api";
import { useFetch, apiErrorMessage } from "@/lib/use-fetch";
import { Card, CardHeader } from "@/components/ui/Card";
import { PageSpinner, ErrorBanner, EmptyState } from "@/components/ui/Feedback";
import { Badge } from "@/components/ui/Badge";
import { Table, Thead, Tbody, Tr, Th, Td } from "@/components/ui/Table";
import { Button } from "@/components/ui/Button";
import { Input, Label, Select } from "@/components/ui/Input";
import { formatDateTime } from "@/lib/format";

function slugify(value: string): string {
  return value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

function CreateProjectModal({ onClose, onCreated }: { onClose: () => void; onCreated: () => void }) {
  const [name, setName] = useState("");
  const [slug, setSlug] = useState("");
  const [slugTouched, setSlugTouched] = useState(false);
  const [environment, setEnvironment] = useState("sandbox");
  const [description, setDescription] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await projectsApi.create({ name, slug, description: description || undefined, environment });
      onCreated();
      onClose();
    } catch (err) {
      setError(err instanceof ApiError ? apiErrorMessage(err) : "Creation impossible");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
      <div className="w-full max-w-md rounded-xl border border-border bg-surface p-6 shadow-xl">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-sm font-semibold text-foreground">Nouveau projet</h2>
          <button onClick={onClose} className="text-muted hover:text-foreground">
            <X className="h-4 w-4" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          {error && <ErrorBanner message={error} />}

          <div>
            <Label htmlFor="name">Nom</Label>
            <Input
              id="name"
              required
              value={name}
              onChange={(e) => {
                setName(e.target.value);
                if (!slugTouched) setSlug(slugify(e.target.value));
              }}
              placeholder="3WF"
            />
          </div>

          <div>
            <Label htmlFor="slug">Slug</Label>
            <Input
              id="slug"
              required
              value={slug}
              onChange={(e) => {
                setSlug(e.target.value);
                setSlugTouched(true);
              }}
              placeholder="3wf"
            />
          </div>

          <div>
            <Label htmlFor="environment">Environnement</Label>
            <Select id="environment" value={environment} onChange={(e) => setEnvironment(e.target.value)}>
              <option value="sandbox">Sandbox</option>
              <option value="production">Production</option>
            </Select>
          </div>

          <div>
            <Label htmlFor="description">Description (optionnel)</Label>
            <Input id="description" value={description} onChange={(e) => setDescription(e.target.value)} />
          </div>

          <div className="mt-2 flex justify-end gap-2">
            <Button type="button" variant="secondary" onClick={onClose}>
              Annuler
            </Button>
            <Button type="submit" loading={submitting}>
              Creer
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default function ProjectsPage() {
  const [modalOpen, setModalOpen] = useState(false);
  const projects = useFetch(() => projectsApi.list(), []);

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-xl font-semibold text-foreground">Projets & cles API</h1>
          <p className="text-sm text-muted">3WF, GeMTI-Cash et futurs projets consommant la plateforme.</p>
        </div>
        <Button onClick={() => setModalOpen(true)}>
          <Plus className="h-4 w-4" /> Nouveau projet
        </Button>
      </div>

      <Card>
        {projects.loading ? (
          <PageSpinner />
        ) : projects.error ? (
          <div className="p-5">
            <ErrorBanner message={projects.error} />
          </div>
        ) : projects.data && projects.data.length > 0 ? (
          <Table>
            <Thead>
              <Tr>
                <Th>Nom</Th>
                <Th>Environnement</Th>
                <Th>Statut</Th>
                <Th>Cree le</Th>
              </Tr>
            </Thead>
            <Tbody>
              {projects.data.map((project) => (
                <Tr key={project.id}>
                  <Td>
                    <Link href={`/projects/${project.id}`} className="font-medium text-accent hover:underline">
                      {project.name}
                    </Link>
                    <div className="text-xs text-muted-foreground">{project.slug}</div>
                  </Td>
                  <Td className="capitalize">{project.environment}</Td>
                  <Td>
                    <Badge tone={project.status === "active" ? "success" : project.status === "suspended" ? "danger" : "neutral"}>
                      {project.status}
                    </Badge>
                  </Td>
                  <Td className="text-muted">{formatDateTime(project.created_at)}</Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        ) : (
          <EmptyState title="Aucun projet" hint="Cree le premier projet pour generer une cle API." />
        )}
      </Card>

      {modalOpen && (
        <CreateProjectModal onClose={() => setModalOpen(false)} onCreated={() => projects.reload()} />
      )}
    </div>
  );
}
