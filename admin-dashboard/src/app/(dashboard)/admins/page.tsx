"use client";

import { useState, type FormEvent } from "react";
import { Plus, X } from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { adminsApi, ApiError } from "@/lib/api";
import { useFetch, apiErrorMessage } from "@/lib/use-fetch";
import { Card } from "@/components/ui/Card";
import { PageSpinner, ErrorBanner, EmptyState } from "@/components/ui/Feedback";
import { Badge } from "@/components/ui/Badge";
import { Table, Thead, Tbody, Tr, Th, Td } from "@/components/ui/Table";
import { Button } from "@/components/ui/Button";
import { Input, Label, Select } from "@/components/ui/Input";
import { formatDateTime } from "@/lib/format";
import type { AdminManaged } from "@/lib/types";

const ROLE_LABELS: Record<string, string> = {
  super_admin: "Super admin",
  admin: "Admin",
  viewer: "Lecteur",
};

function InviteAdminModal({ onClose, onInvited }: { onClose: () => void; onInvited: () => void }) {
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("viewer");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await adminsApi.invite({ email, role });
      onInvited();
      onClose();
    } catch (err) {
      setError(err instanceof ApiError ? apiErrorMessage(err) : "Invitation impossible");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
      <div className="w-full max-w-md rounded-xl border border-border bg-surface p-6 shadow-xl">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-sm font-semibold text-foreground">Inviter un administrateur</h2>
          <button onClick={onClose} className="text-muted hover:text-foreground">
            <X className="h-4 w-4" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          {error && <ErrorBanner message={error} />}

          <div>
            <Label htmlFor="invite-email">Email</Label>
            <Input
              id="invite-email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="prenom.nom@entreprise.com"
            />
          </div>

          <div>
            <Label htmlFor="invite-role">Role</Label>
            <Select id="invite-role" value={role} onChange={(e) => setRole(e.target.value)}>
              <option value="viewer">Lecteur</option>
              <option value="admin">Admin</option>
              <option value="super_admin">Super admin</option>
            </Select>
          </div>

          <p className="text-xs text-muted-foreground">
            Un mot de passe temporaire sera genere et envoye par email a cette adresse.
          </p>

          <div className="mt-2 flex justify-end gap-2">
            <Button type="button" variant="secondary" onClick={onClose}>
              Annuler
            </Button>
            <Button type="submit" loading={submitting}>
              Envoyer l&apos;invitation
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}

function AdminRow({
  row,
  isSelf,
  canManage,
  onChanged,
}: {
  row: AdminManaged;
  isSelf: boolean;
  canManage: boolean;
  onChanged: () => void;
}) {
  const [busy, setBusy] = useState(false);

  async function handleRoleChange(role: string) {
    setBusy(true);
    try {
      await adminsApi.updateRole(row.id, role);
      onChanged();
    } catch {
      // l'erreur est silencieuse ici, le select reprend sa valeur au prochain reload
    } finally {
      setBusy(false);
    }
  }

  async function handleToggleActive() {
    setBusy(true);
    try {
      await adminsApi.setActive(row.id, !row.is_active);
      onChanged();
    } catch {
      // idem
    } finally {
      setBusy(false);
    }
  }

  return (
    <Tr>
      <Td className="font-medium text-foreground">
        {row.email}
        {isSelf && <span className="ml-2 text-xs text-muted">(vous)</span>}
      </Td>
      <Td>
        {canManage && !isSelf ? (
          <Select
            value={row.role}
            disabled={busy}
            onChange={(e) => handleRoleChange(e.target.value)}
            className="w-auto"
          >
            <option value="viewer">Lecteur</option>
            <option value="admin">Admin</option>
            <option value="super_admin">Super admin</option>
          </Select>
        ) : (
          <Badge tone={row.role === "super_admin" ? "info" : "neutral"}>
            {ROLE_LABELS[row.role] ?? row.role}
          </Badge>
        )}
      </Td>
      <Td>
        <Badge tone={row.is_active ? "success" : "danger"}>{row.is_active ? "Actif" : "Desactive"}</Badge>
      </Td>
      <Td className="text-muted">{formatDateTime(row.last_login_at)}</Td>
      <Td className="text-muted">{formatDateTime(row.created_at)}</Td>
      <Td>
        {canManage && !isSelf && (
          <Button
            variant={row.is_active ? "danger" : "secondary"}
            size="sm"
            loading={busy}
            onClick={handleToggleActive}
          >
            {row.is_active ? "Desactiver" : "Reactiver"}
          </Button>
        )}
      </Td>
    </Tr>
  );
}

export default function AdminsPage() {
  const { admin } = useAuth();
  const [modalOpen, setModalOpen] = useState(false);
  const admins = useFetch(() => adminsApi.list(), []);
  const canManage = admin?.role === "super_admin";

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-xl font-semibold text-foreground">Administrateurs</h1>
          <p className="text-sm text-muted">Gestion des comptes ayant acces au dashboard.</p>
        </div>
        {canManage && (
          <Button onClick={() => setModalOpen(true)}>
            <Plus className="h-4 w-4" /> Inviter un administrateur
          </Button>
        )}
      </div>

      <Card>
        {admins.loading ? (
          <PageSpinner />
        ) : admins.error ? (
          <div className="p-5">
            <ErrorBanner message={admins.error} />
          </div>
        ) : admins.data && admins.data.length > 0 ? (
          <Table>
            <Thead>
              <Tr>
                <Th>Email</Th>
                <Th>Role</Th>
                <Th>Statut</Th>
                <Th>Derniere connexion</Th>
                <Th>Cree le</Th>
                <Th></Th>
              </Tr>
            </Thead>
            <Tbody>
              {admins.data.map((row) => (
                <AdminRow
                  key={row.id}
                  row={row}
                  isSelf={row.id === admin?.id}
                  canManage={canManage}
                  onChanged={() => admins.reload()}
                />
              ))}
            </Tbody>
          </Table>
        ) : (
          <EmptyState title="Aucun administrateur" />
        )}
      </Card>

      {modalOpen && (
        <InviteAdminModal onClose={() => setModalOpen(false)} onInvited={() => admins.reload()} />
      )}
    </div>
  );
}
