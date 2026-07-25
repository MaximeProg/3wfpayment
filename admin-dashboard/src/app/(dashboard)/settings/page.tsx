"use client";

import { useState, type FormEvent } from "react";
import { Pencil, Plus, X } from "lucide-react";
import { settingsApi, ApiError } from "@/lib/api";
import { useFetch, apiErrorMessage } from "@/lib/use-fetch";
import { Card } from "@/components/ui/Card";
import { PageSpinner, ErrorBanner, EmptyState } from "@/components/ui/Feedback";
import { Table, Thead, Tbody, Tr, Th, Td } from "@/components/ui/Table";
import { Button } from "@/components/ui/Button";
import { Input, Label } from "@/components/ui/Input";
import { formatDateTime } from "@/lib/format";
import type { SystemSetting } from "@/lib/types";

function EditSettingModal({
  setting,
  onClose,
  onSaved,
}: {
  setting: SystemSetting | { key: string; value: unknown; description: string | null } | null;
  onClose: () => void;
  onSaved: () => void;
}) {
  const [key, setKey] = useState(setting?.key ?? "");
  const [valueText, setValueText] = useState(setting ? JSON.stringify(setting.value, null, 2) : "");
  const [description, setDescription] = useState(setting?.description ?? "");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const isNew = !setting || !("updated_at" in setting);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const parsedValue = JSON.parse(valueText);
      await settingsApi.update(key, { value: parsedValue, description: description || undefined });
      onSaved();
      onClose();
    } catch (err) {
      if (err instanceof SyntaxError) {
        setError("Valeur JSON invalide");
      } else {
        setError(err instanceof ApiError ? apiErrorMessage(err) : "Enregistrement impossible");
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
      <div className="w-full max-w-lg rounded-xl border border-border bg-surface p-6 shadow-xl">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-sm font-semibold text-foreground">{isNew ? "Nouveau parametre" : `Modifier ${key}`}</h2>
          <button onClick={onClose} className="text-muted hover:text-foreground">
            <X className="h-4 w-4" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          {error && <ErrorBanner message={error} />}

          <div>
            <Label htmlFor="key">Cle</Label>
            <Input id="key" required disabled={!isNew} value={key} onChange={(e) => setKey(e.target.value)} />
          </div>

          <div>
            <Label htmlFor="value">Valeur (JSON)</Label>
            <textarea
              id="value"
              required
              rows={6}
              value={valueText}
              onChange={(e) => setValueText(e.target.value)}
              className="w-full rounded-lg border border-border bg-surface px-3 py-2 font-mono text-xs text-foreground focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/20"
            />
          </div>

          <div>
            <Label htmlFor="description">Description (optionnel)</Label>
            <Input id="description" value={description ?? ""} onChange={(e) => setDescription(e.target.value)} />
          </div>

          <div className="mt-2 flex justify-end gap-2">
            <Button type="button" variant="secondary" onClick={onClose}>
              Annuler
            </Button>
            <Button type="submit" loading={submitting}>
              Enregistrer
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default function SettingsPage() {
  const settings = useFetch(() => settingsApi.list(), []);
  const [editing, setEditing] = useState<SystemSetting | { key: string; value: unknown; description: string | null } | null | undefined>(
    undefined
  );

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-xl font-semibold text-foreground">Parametres systeme</h1>
          <p className="text-sm text-muted">Configuration cle/valeur de la plateforme (reserve aux super admins).</p>
        </div>
        <Button onClick={() => setEditing({ key: "", value: {}, description: null })}>
          <Plus className="h-4 w-4" /> Nouveau parametre
        </Button>
      </div>

      <Card>
        {settings.loading ? (
          <PageSpinner />
        ) : settings.error ? (
          <div className="p-5">
            <ErrorBanner message={settings.error} />
          </div>
        ) : settings.data && settings.data.length > 0 ? (
          <Table>
            <Thead>
              <Tr>
                <Th>Cle</Th>
                <Th>Valeur</Th>
                <Th>Mis a jour le</Th>
                <Th></Th>
              </Tr>
            </Thead>
            <Tbody>
              {settings.data.map((setting) => (
                <Tr key={setting.key}>
                  <Td className="font-medium text-foreground">{setting.key}</Td>
                  <Td>
                    <code className="text-xs text-muted-foreground">{JSON.stringify(setting.value)}</code>
                  </Td>
                  <Td className="text-muted">{formatDateTime(setting.updated_at)}</Td>
                  <Td>
                    <Button variant="secondary" size="sm" onClick={() => setEditing(setting)}>
                      <Pencil className="h-3.5 w-3.5" /> Modifier
                    </Button>
                  </Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        ) : (
          <EmptyState title="Aucun parametre" hint="Ajoute un premier parametre systeme." />
        )}
      </Card>

      {editing !== undefined && (
        <EditSettingModal setting={editing} onClose={() => setEditing(undefined)} onSaved={() => settings.reload()} />
      )}
    </div>
  );
}
