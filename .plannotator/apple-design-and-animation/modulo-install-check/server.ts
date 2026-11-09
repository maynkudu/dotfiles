import assert from "node:assert/strict";
import { randomBytes, scryptSync, createHash } from "node:crypto";
import { mkdtemp, mkdir, readFile, readdir, rm, symlink, writeFile } from "node:fs/promises";
import { resolve, dirname, extname } from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { NextRequest } from "next/server";
import { GET as registry } from "/home/maynkudu/Code/Projects/modulo/src/app/r/[name]/route";
import { POST as login } from "/home/maynkudu/Code/Projects/modulo/src/app/api/mint/session/route";
import { POST as createKey } from "/home/maynkudu/Code/Projects/modulo/src/app/api/mint/keys/route";
import { DELETE as revokeKey } from "/home/maynkudu/Code/Projects/modulo/src/app/api/mint/keys/[id]/route";
import { GET as sourceStatus, POST as unlockSource } from "/home/maynkudu/Code/Projects/modulo/src/app/api/source-access/route";
import { createdKeySchema, sourceItemSchema, sessionStatusSchema } from "/home/maynkudu/Code/Projects/modulo/src/lib/access-schema";
import { getMintStore } from "/home/maynkudu/Code/Projects/modulo/src/lib/mint-store";

const evidence = dirname(import.meta.path), root = process.cwd();
assert.equal(root, "/home/maynkudu/Code/Projects/modulo");
const runtime = await mkdtemp(resolve(evidence, "runtime-"));
const passphrase = randomBytes(24).toString("base64url"), salt = randomBytes(16).toString("hex");
process.env.MODULO_DATABASE_URL = `file:${runtime}/mint.db`;
process.env.MODULO_MINT_PASSPHRASE_HASH = `scrypt:${salt}:${scryptSync(passphrase, salt, 64).toString("hex")}`;
delete process.env.MODULO_DATABASE_AUTH_TOKEN;
delete process.env.VERCEL;
const origin = process.env.PORTLESS_URL;
assert(origin, "Run through portless.");
const run = promisify(execFile), names = ["elastic-slider", "snap-rail", "liquid-cluster"];
const secrets = [passphrase], keyIds: string[] = [];
const results: { component: string; check: string; passed: boolean }[] = [];
const hashes: { component: string; file: string; source: string; downloaded: string; installed: string; installedEqualsDownloaded: boolean }[] = [];
let mintCookie = "", cleaned = false, started = false;
function redact(value: string) { return secrets.reduce((text, secret) => text.replaceAll(secret, "[redacted]"), value); }
function check(component: string, message: string, passed: boolean) {
  results.push({ component, check: message, passed });
  assert(passed, `${component}: ${message}`);
}
const sha = (value: string) => createHash("sha256").update(value).digest("hex");
function cookie(response: Response) {
  const header = response.headers.get("set-cookie");
  assert(header, "Session cookie is present.");
  const value = header.split(";")[0];
  secrets.push(value, value.slice(value.indexOf("=") + 1));
  return value;
}
function call(path: string, options: { method?: string; key?: string; cookie?: string; body?: unknown } = {}) {
  const headers = new Headers({ origin });
  if (options.key) headers.set("Authorization", `Bearer ${options.key}`);
  if (options.cookie) headers.set("Cookie", options.cookie);
  if (options.body !== undefined) headers.set("Content-Type", "application/json");
  return fetch(`${origin}${path}`, { method: options.method ?? "GET", headers, body: options.body === undefined ? undefined : JSON.stringify(options.body) });
}
async function cleanup() {
  if (cleaned) return;
  cleaned = true;
  for (const id of keyIds) {
    const response = await revokeKey(new NextRequest(`${origin}/api/mint/keys/${id}`, { method: "DELETE", headers: { origin, host: new URL(origin).host, "x-forwarded-proto": new URL(origin).protocol.slice(0, -1), cookie: mintCookie } }), { params: Promise.resolve({ id }) });
    assert.equal(response.status, 200, "Every verification key is revoked.");
  }
  const keys = await (await getMintStore()).listKeys();
  assert(keys.every(key => key.revokedAt !== null), "No active verification keys remain.");
  await (await getMintStore()).close();
  await rm(runtime, { recursive: true, force: true });
  delete process.env.MODULO_DATABASE_URL;
  delete process.env.MODULO_MINT_PASSPHRASE_HASH;
}
async function verify() {
  assert(!started, "This disposable check runs once."); started = true;
  let failure: string | null = null;
  try {
    for (const name of names) await readFile(resolve(root, `.private-registry/${name}.json`), "utf8");
    const authenticated = await call("/api/mint/session", { method: "POST", body: { passphrase } });
    check("mint", "Disposable passphrase opens a mint session through the real handler", authenticated.status === 200);
    mintCookie = cookie(authenticated);
    for (const name of names) {
      const path = `/r/${name}.json`;
      check(name, "Anonymous source is denied", (await call(path)).status === 401);
      const minted = await call("/api/mint/keys", { method: "POST", cookie: mintCookie, body: { label: `${name} disposable install check` } });
      check(name, "Real mint handler creates an active key", minted.status === 201);
      const { key, info } = createdKeySchema.parse(await minted.json()); secrets.push(key); keyIds.push(info.id);
      const download = await call(path, { key });
      check(name, "Active bearer downloads protected source without caching", download.status === 200 && download.headers.get("cache-control") === "private, no-store");
      const manifest = sourceItemSchema.parse(await download.json());
      const unlock = await call("/api/source-access", { method: "POST", body: { key } });
      check(name, "Active key opens a source session through the real handler", unlock.status === 200);
      const sourceCookie = cookie(unlock);
      check(name, "Existing source session downloads the manifest", (await call(path, { cookie: sourceCookie })).status === 200);
      check(name, "Source session reports unlocked", sessionStatusSchema.parse(await (await call("/api/source-access", { cookie: sourceCookie })).json()).authenticated);
      check(name, "Invalid explicit bearer cannot fall back to an active session", (await call(path, { cookie: sourceCookie, key: "invalid" })).status === 401);
      const consumer = resolve(runtime, name);
      await mkdir(resolve(consumer, "src"), { recursive: true });
      await symlink(resolve(root, "node_modules"), resolve(consumer, "node_modules"), "dir");
      await writeFile(resolve(consumer, "package.json"), JSON.stringify({ name: `${name}-install-consumer`, version: "1.0.0", private: true, dependencies: { react: "19.3.0", "react-dom": "19.3.0", vite: "6.0.0", tailwindcss: "4.0.0" } }));
      await writeFile(resolve(consumer, "index.html"), '<div id="root"></div>');
      await writeFile(resolve(consumer, "src/index.css"), '@import "tailwindcss";');
      await writeFile(resolve(consumer, "tsconfig.json"), JSON.stringify({ compilerOptions: { target: "ES2017", lib: ["dom", "dom.iterable", "esnext"], strict: true, noEmit: true, module: "esnext", moduleResolution: "bundler", jsx: "react-jsx", skipLibCheck: true, paths: { "@/*": ["./src/*"] } }, include: ["src"] }));
      const config = { style: "base-nova", rsc: false, tsx: true, tailwind: { config: "", css: "src/index.css", baseColor: "neutral", cssVariables: true }, aliases: { components: "@/components", utils: "@/lib/utils", ui: "@/components/ui", lib: "@/lib", hooks: "@/hooks" }, registries: { "@modulo": { url: `${origin}/r/{name}.json`, headers: { Authorization: "Bearer ${MODULO_CHECK_KEY}" } } } };
      await writeFile(resolve(consumer, "components.json"), JSON.stringify(config));
      await writeFile(resolve(evidence, "consumer-components.json"), JSON.stringify(config, null, 2) + "\n");
      let installed = false;
      try {
        const cli = await run("node", [resolve(root, "node_modules/shadcn/dist/index.js"), "add", `@modulo/${name}`, "--yes", "--cwd", consumer], { env: { ...process.env, MODULO_CHECK_KEY: key, npm_config_offline: "true" }, maxBuffer: 1024 * 1024 });
        await writeFile(resolve(evidence, `${name}-install.txt`), redact(cli.stdout + cli.stderr)); installed = true;
      } catch (error) {
        if (error instanceof Error) await writeFile(resolve(evidence, `${name}-install.txt`), redact(error.message));
      }
      check(name, "Actual installed Shadcn CLI installs the @modulo entry with an env bearer", installed);
      const outputFiles = await readdir(resolve(consumer, `src/components/${name}`));
      check(name, "Installed file count equals the protected manifest", outputFiles.length === manifest.files.length);
      for (const file of manifest.files) {
        assert(file.target, "Registry file has an explicit consumer target.");
        const source = await readFile(resolve(root, file.path), "utf8"), output = await readFile(resolve(consumer, "src", file.target), "utf8");
        hashes.push({ component: name, file: file.target, source: sha(source), downloaded: sha(file.content), installed: sha(output), installedEqualsDownloaded: output === file.content });
        check(name, `${file.target} downloaded source exactly equals current local implementation`, source === file.content);
        check(name, `${file.target} installed source exactly equals downloaded source`, output === file.content);
        if ([".ts", ".tsx"].includes(extname(file.target))) {
          const imports = [...output.matchAll(/(?:from\s+|import\s+)["']([^"']+)["']/g)].map(match => match[1]);
          check(name, `${file.target} internal imports are relative or declared React imports`, imports.every(value => value.startsWith(".") || value === "react"));
        }
      }
      await run(resolve(root, "node_modules/.bin/tsc"), ["--project", resolve(consumer, "tsconfig.json")], { maxBuffer: 1024 * 1024 });
      check(name, "Installed consumer passes strict TypeScript", true);
      const revoked = await call(`/api/mint/keys/${info.id}`, { method: "DELETE", cookie: mintCookie });
      check(name, "Real mint revocation succeeds", revoked.status === 200);
      check(name, "Next bearer request is denied after revocation", (await call(path, { key })).status === 401);
      check(name, "Next existing source-session request is denied after revocation", (await call(path, { cookie: sourceCookie })).status === 401);
      check(name, "Revoked session reports locked", !sessionStatusSchema.parse(await (await call("/api/source-access", { cookie: sourceCookie })).json()).authenticated);
      check(name, "Revoked key cannot create another source session", (await call("/api/source-access", { method: "POST", body: { key } })).status === 401);
    }
  } catch (error) { failure = redact(error instanceof Error ? error.message : "Unknown verification failure."); }
  finally { try { await cleanup(); } catch (error) { failure ??= redact(error instanceof Error ? error.message : "Cleanup failed."); } }
  const report = { origin, handlerCwd: root, cli: "Installed shadcn 4.23.0", consumerDependencies: "Reused existing Modulo node_modules through a temporary symlink. No fresh dependency resolution claimed.", results, hashes, failure, cleanup: { completed: cleaned, revokedKeys: keyIds.length, runtimeRemoved: !(await Bun.file(`${runtime}/mint.db`).exists()) }, scope: "Real HTTP route handlers, local manifests and actual namespaced installation. No Next server rendering, remote publication, full-SHA source pin or fresh remote checkout claim." };
  await writeFile(resolve(evidence, "results.json"), JSON.stringify(report, null, 2) + "\n");
  return Response.json(report, { status: failure ? 500 : 200 });
}
const server = Bun.serve({ hostname: process.env.HOST ?? "127.0.0.1", port: Number(process.env.PORT), async fetch(raw) {
  const path = new URL(raw.url).pathname;
  if (path === "/__health") return Response.json({ ready: true, started, cleaned });
  if (path === "/__run" && raw.method === "POST") return verify();
  if (path === "/__stop" && raw.method === "POST") { await cleanup(); queueMicrotask(() => server.stop(true)); return Response.json({ stopped: true }); }
  const request = new NextRequest(raw);
  if (path.startsWith("/r/") && raw.method === "GET") return registry(request, { params: Promise.resolve({ name: path.slice(3) }) });
  if (path === "/api/mint/session" && raw.method === "POST") return login(request);
  if (path === "/api/mint/keys" && raw.method === "POST") return createKey(request);
  if (path.startsWith("/api/mint/keys/") && raw.method === "DELETE") return revokeKey(request, { params: Promise.resolve({ id: path.slice(15) }) });
  if (path === "/api/source-access") return raw.method === "POST" ? unlockSource(request) : sourceStatus(request);
  return new Response("Not found", { status: 404 });
} });
console.log(`Install-check handlers ready at ${origin}. Verification credentials stay in memory.`);
process.on("SIGINT", () => { void cleanup().finally(() => { server.stop(true); process.exit(); }); });
process.on("SIGTERM", () => { void cleanup().finally(() => { server.stop(true); process.exit(); }); });
