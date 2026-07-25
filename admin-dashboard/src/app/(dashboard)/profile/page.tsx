"use client";

import { useState, type FormEvent } from "react";
import { useAuth } from "@/lib/auth-context";
import { meApi, ApiError } from "@/lib/api";
import { apiErrorMessage } from "@/lib/use-fetch";
import { Card, CardHeader, CardBody } from "@/components/ui/Card";
import { ErrorBanner } from "@/components/ui/Feedback";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Input, Label } from "@/components/ui/Input";
import { formatDateTime } from "@/lib/format";

const ROLE_LABELS: Record<string, string> = {
  super_admin: "Super admin",
  admin: "Admin",
  viewer: "Lecteur",
};

function ChangePasswordForm() {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setSuccess(false);

    if (newPassword !== confirmPassword) {
      setError("Les deux mots de passe ne correspondent pas");
      return;
    }

    setSubmitting(true);
    try {
      await meApi.changePassword({ current_password: currentPassword, new_password: newPassword });
      setSuccess(true);
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (err) {
      setError(err instanceof ApiError ? apiErrorMessage(err) : "Changement impossible");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      {error && <ErrorBanner message={error} />}
      {success && (
        <div className="rounded-lg border border-success/30 bg-success-bg px-4 py-3 text-sm text-success">
          Mot de passe mis a jour.
        </div>
      )}

      <div>
        <Label htmlFor="current-password">Mot de passe actuel</Label>
        <Input
          id="current-password"
          type="password"
          required
          value={currentPassword}
          onChange={(e) => setCurrentPassword(e.target.value)}
        />
      </div>

      <div>
        <Label htmlFor="new-password">Nouveau mot de passe</Label>
        <Input
          id="new-password"
          type="password"
          required
          minLength={8}
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
        />
      </div>

      <div>
        <Label htmlFor="confirm-password">Confirmer le nouveau mot de passe</Label>
        <Input
          id="confirm-password"
          type="password"
          required
          minLength={8}
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        />
      </div>

      <div className="flex justify-end">
        <Button type="submit" loading={submitting}>
          Mettre a jour le mot de passe
        </Button>
      </div>
    </form>
  );
}

export default function ProfilePage() {
  const { admin } = useAuth();

  if (!admin) return null;

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-xl font-semibold text-foreground">Profil</h1>
        <p className="text-sm text-muted">Informations de votre compte administrateur.</p>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader title="Informations du compte" />
          <CardBody className="flex flex-col gap-3 text-sm">
            <div className="flex items-center justify-between">
              <span className="text-muted">Email</span>
              <span className="font-medium text-foreground">{admin.email}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-muted">Role</span>
              <Badge tone={admin.role === "super_admin" ? "info" : "neutral"}>
                {ROLE_LABELS[admin.role] ?? admin.role}
              </Badge>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-muted">Membre depuis</span>
              <span className="text-foreground">{formatDateTime(admin.created_at)}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-muted">Derniere connexion</span>
              <span className="text-foreground">{formatDateTime(admin.last_login_at)}</span>
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardHeader title="Changer mon mot de passe" />
          <CardBody>
            <ChangePasswordForm />
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
