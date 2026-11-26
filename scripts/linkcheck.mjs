#!/usr/bin/env node
// Reports external links in docs/*.html that do not return an OK status.
// Exits 0 always; results are printed for review (many official sites block automated requests).
import { readdirSync, readFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const DOCS = join(dirname(fileURLToPath(import.meta.url)), "..", "docs");
const urls = new Set();
for (const f of readdirSync(DOCS).filter((f) => f.endsWith(".html"))) {
  for (const m of readFileSync(join(DOCS, f), "utf8").matchAll(/href="(https:\/\/[^"]+)"/g)) urls.add(m[1].replace(/&amp;/g, "&"));
}
let bad = 0;
for (const u of urls) {
  try {
    const r = await fetch(u, { method: "GET", redirect: "follow", signal: AbortSignal.timeout(15000), headers: { "user-agent": "Mozilla/5.0 link-check" } });
    if (!r.ok) { bad++; console.log(`HTTP ${r.status}  ${u}`); }
  } catch (e) { bad++; console.log(`ERR       ${u}  (${e.cause?.code || e.name})`); }
}
console.log(`Checked ${urls.size} external links; ${bad} did not return OK (review manually).`);
