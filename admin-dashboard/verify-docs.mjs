import { chromium } from "playwright";

const BASE = "http://localhost:3000";
const errors = [];

function logConsole(page, tag) {
  page.on("console", (msg) => {
    if (msg.type() === "error") errors.push(`[console:${tag}] ${msg.text()}`);
  });
  page.on("pageerror", (err) => errors.push(`[pageerror:${tag}] ${err.message}`));
}

async function main() {
  const browser = await chromium.launch({ args: ["--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage"] });
  try {
    await run(browser);
  } finally {
    await browser.close();
  }
}

async function run(browser) {
  const context = await browser.newContext({ viewport: { width: 1400, height: 900 } });
  const page = await context.newPage();
  logConsole(page, "desktop");

  console.log("-> goto /docs (no auth, should render directly)");
  await page.goto(`${BASE}/docs`, { waitUntil: "commit", timeout: 45000 });
  await page.getByRole("heading", { level: 1, name: "Vue d'ensemble" }).waitFor({ timeout: 20000 });
  console.log("   overview page ok");

  console.log("-> checking sidebar nav links");
  const sidebar = page.getByRole("complementary");
  await sidebar.getByRole("link", { name: "Depots" }).waitFor({ timeout: 5000 });
  console.log("   sidebar present with nav links");

  console.log("-> nav to /docs/deposits via sidebar click");
  await sidebar.getByRole("link", { name: "Depots" }).click();
  await page.getByRole("heading", { level: 1, name: "Depots" }).waitFor({ timeout: 20000 });
  console.log("   deposits page ok, url:", page.url());

  console.log("-> checking code block + table render on deposits page");
  await page.locator("pre").first().waitFor({ timeout: 5000 });
  await page.locator("table").first().waitFor({ timeout: 5000 });
  console.log("   code block and table present");

  console.log("-> checking prev/next nav");
  await page.getByRole("link", { name: /Suivant/ }).waitFor({ timeout: 5000 });
  console.log("   prev/next nav present");

  console.log("-> checking internal cross-link (reference-data)");
  const crossLink = page.getByRole("link", { name: "Donnees de reference" }).first();
  await crossLink.waitFor({ timeout: 5000 });
  await crossLink.click();
  await page.getByRole("heading", { level: 1, name: "Donnees de reference" }).waitFor({ timeout: 20000 });
  console.log("   cross-link navigation works, url:", page.url());

  console.log("-> checking heading anchor id exists on transactions page (idempotence)");
  await page.goto(`${BASE}/docs/transactions`, { waitUntil: "commit", timeout: 45000 });
  await page.getByRole("heading", { level: 1, name: "Statuts et transactions" }).waitFor({ timeout: 20000 });
  const anchorExists = await page.locator("#idempotence").count();
  console.log("   #idempotence heading anchor count:", anchorExists);
  if (anchorExists === 0) errors.push("Missing #idempotence heading anchor on /docs/transactions");

  console.log("-> checking login page has doc link");
  await page.goto(`${BASE}/login`, { waitUntil: "commit", timeout: 45000 });
  await page.getByRole("link", { name: "Voir la documentation" }).waitFor({ timeout: 10000 });
  console.log("   login page links to docs");

  await page.screenshot({ path: "verify-docs-desktop.png", fullPage: false });

  console.log("-> resize to mobile 375x667");
  await page.setViewportSize({ width: 375, height: 667 });
  await page.goto(`${BASE}/docs`, { waitUntil: "commit", timeout: 45000 });
  await page.getByRole("heading", { level: 1, name: "Vue d'ensemble" }).waitFor({ timeout: 20000 });
  await page.screenshot({ path: "verify-docs-mobile.png", fullPage: false });
  console.log("-> mobile overview screenshot taken");

  console.log("-> opening mobile menu");
  await page.getByLabel("Ouvrir le menu").click();
  await page.getByRole("link", { name: "Erreurs" }).waitFor({ timeout: 5000 });
  await page.screenshot({ path: "verify-docs-mobile-menu.png", fullPage: false });
  console.log("   mobile menu opens correctly");

  console.log("\n=== Console errors/pageerrors ===");
  if (errors.length === 0) {
    console.log("OK - none");
  } else {
    for (const e of errors) console.log(e);
    process.exitCode = 1;
  }
}

main().catch((err) => {
  console.error("FATAL", err.message);
  process.exitCode = 1;
});
