"""Test manuel bout en bout de l'API admin (pas un test automatise formel -
verification rapide apres implementation). Necessite le serveur demarre et un
admin existant (scripts/seed_admin_user.py)."""

import sys

import httpx

BASE = "http://127.0.0.1:8000/admin/v1"
EMAIL = sys.argv[1] if len(sys.argv) > 1 else "kouassimaxime540@gmail.com"
PASSWORD = sys.argv[2] if len(sys.argv) > 2 else "ChangeMe123!"


def main() -> None:
    with httpx.Client(base_url=BASE, timeout=30.0) as client:
        r = client.post("/auth/login", json={"email": EMAIL, "password": PASSWORD})
        print("login:", r.status_code, r.json())
        assert r.status_code == 200

        r = client.get("/stats/overview")
        print("overview:", r.status_code, r.json())

        r = client.get("/stats/by-project")
        print("by-project:", r.status_code, r.json())

        r = client.get("/projects")
        print("projects list:", r.status_code, len(r.json()), "projet(s)")
        projects = r.json()
        assert len(projects) > 0
        project_id = projects[0]["id"]

        r = client.get(f"/projects/{project_id}/api-keys")
        print("api-keys list:", r.status_code, len(r.json()), "cle(s)")

        r = client.get("/transactions", params={"limit": 5})
        print("transactions list:", r.status_code, len(r.json()), "transaction(s)")

        r = client.get("/webhooks", params={"limit": 5})
        print("webhooks list:", r.status_code, len(r.json()), "webhook(s)")

        r = client.get("/monitoring/health")
        print("monitoring health:", r.status_code, r.json())

        r = client.get("/monitoring/errors", params={"limit": 5})
        print("monitoring errors:", r.status_code, len(r.json()), "erreur(s)")

        r = client.get("/audit-logs")
        print("audit-logs:", r.status_code, len(r.json()), "entree(s)")

        r = client.get("/settings")
        print("settings:", r.status_code, r.json())

        # Creation d'un projet de test + cle + rotation + revoke
        r = client.post(
            "/projects",
            json={"name": "Admin Test Project", "slug": "admin-test-project", "environment": "sandbox"},
        )
        print("create project:", r.status_code, r.json())
        if r.status_code == 201:
            new_project_id = r.json()["id"]

            r = client.post(f"/projects/{new_project_id}/api-keys", json={})
            print("create api-key:", r.status_code, r.json().get("full_key", "")[:20] + "...")
            key_id = r.json()["id"]

            r = client.post(f"/projects/api-keys/{key_id}/rotate")
            print("rotate api-key:", r.status_code)
            new_key_id = r.json()["id"]

            r = client.post(f"/projects/api-keys/{new_key_id}/revoke")
            print("revoke api-key:", r.status_code, r.json()["status"])

            r = client.patch(f"/projects/{new_project_id}", json={"status": "inactive"})
            print("update project:", r.status_code, r.json()["status"])

        r = client.post("/auth/logout")
        print("logout:", r.status_code)

        r = client.get("/stats/overview")
        print("overview apres logout (doit etre 401):", r.status_code)


if __name__ == "__main__":
    main()
