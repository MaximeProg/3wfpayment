import { chromium } from "playwright";

const browser = await chromium.launch({ args: ["--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage"] });
const page = await browser.newPage();
page.on("console", (msg) => console.log(`[console:${msg.type()}] ${msg.text()}`));
page.on("pageerror", (err) => console.log(`[pageerror] ${err.message}`));
page.on("requestfailed", (req) => console.log(`[requestfailed] ${req.url()} ${req.failure()?.errorText}`));
page.on("response", (res) => {
  if (res.status() >= 400) console.log(`[response ${res.status()}] ${res.url()}`);
});

console.log("-> goto /docs");
try {
  await page.goto("http://localhost:3000/docs", { waitUntil: "domcontentloaded", timeout: 30000 });
  console.log("-> domcontentloaded ok, url:", page.url());
} catch (e) {
  console.log("-> domcontentloaded FAILED:", e.message);
}
await page.waitForTimeout(5000);
console.log("-> title:", await page.title().catch(() => "N/A"));
await page.screenshot({ path: "diag-docs.png" }).catch((e) => console.log("screenshot failed:", e.message));
await browser.close();
console.log("done");
