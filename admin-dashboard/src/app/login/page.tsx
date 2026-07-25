"use client";

import { useEffect, useState, type FormEvent } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth, ApiError } from "@/lib/auth-context";
import { apiErrorMessage } from "@/lib/use-fetch";
import { Button } from "@/components/ui/Button";
import { Input, Label } from "@/components/ui/Input";
import { ErrorBanner } from "@/components/ui/Feedback";

export default function LoginPage() {
  const { admin, loading, login } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!loading && admin) {
      router.replace("/");
    }
  }, [loading, admin, router]);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await login(email, password);
      router.replace("/");
    } catch (err) {
      setError(err instanceof ApiError ? apiErrorMessage(err) : "Connexion impossible");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4">
      <div className="w-full max-w-sm">
        <div className="mb-8 flex flex-col items-center gap-2 text-center">
          <div className="h-3 w-3 rounded-full bg-accent" />
          <h1 className="text-lg font-semibold text-foreground">Payment Platform</h1>
          <p className="text-sm text-muted">Connexion administrateur</p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="rounded-xl border border-border bg-surface p-6 shadow-sm"
        >
          {error && (
            <div className="mb-4">
              <ErrorBanner message={error} />
            </div>
          )}

          <div className="mb-4">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="mb-6">
            <Label htmlFor="password">Mot de passe</Label>
            <Input
              id="password"
              type="password"
              autoComplete="current-password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <Button type="submit" loading={submitting} className="w-full">
            Se connecter
          </Button>
        </form>

        <p className="mt-6 text-center text-sm text-muted">
          Vous integrez un produit a la plateforme ?{" "}
          <Link href="/docs" className="text-accent hover:underline">
            Voir la documentation
          </Link>
        </p>
      </div>
    </div>
  );
}
