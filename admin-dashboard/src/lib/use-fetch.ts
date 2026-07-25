"use client";

import { useCallback, useEffect, useState } from "react";
import { ApiError } from "./api";

export function useFetch<T>(fetcher: () => Promise<T>, deps: unknown[]) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(() => {
    setLoading(true);
    setError(null);
    fetcher()
      .then((result) => setData(result))
      .catch((err) => {
        setError(err instanceof ApiError ? apiErrorMessage(err) : "Une erreur est survenue");
      })
      .finally(() => setLoading(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  useEffect(() => {
    load();
  }, [load]);

  return { data, loading, error, reload: load };
}

export function apiErrorMessage(err: ApiError): string {
  if (typeof err.detail === "string") return err.detail;
  if (err.detail && typeof err.detail === "object") {
    const message = (err.detail as { message?: string }).message;
    if (message) return message;
    try {
      return JSON.stringify(err.detail);
    } catch {
      return err.message;
    }
  }
  return err.message;
}
