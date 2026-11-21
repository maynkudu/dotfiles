#!/usr/bin/env node
import { createHash } from "node:crypto";
import { mkdir, readFile, readdir, realpath, writeFile } from "node:fs/promises";
import { basename, dirname, isAbsolute, relative, resolve, sep } from "node:path";
import { pathToFileURL } from "node:url";

/** Copies a verified installed game into an empty directory after validating every input. */
export async function createSpriteGame({ source, out, template = "racer", title, map = "coast", car = "pickup" }) {
  if (!["racer", "delivery"].includes(template)) throw new Error("Choose the racer or delivery template.");
  if (!["pine", "coast", "alpine", "harbor", "mesa", "yard"].includes(map) || !["rally", "club", "midgt", "turbo", "drift", "pickup"].includes(car)) throw new Error("Map and car must be shipped content IDs.");
  if (title !== undefined && (typeof title !== "string" || !title.trim() || title.length > 80)) throw new Error("Title must contain 1 to 80 characters.");
  const sourcePath = await realpath(source), target = resolve(out);
  let payload;
  try { payload = JSON.parse(await readFile(sourcePath, "utf8")); } catch (error) { if (error.code !== "EISDIR") throw error; }
  const sourceRoot = payload ? dirname(sourcePath) : sourcePath;
  if (!payload && (target === sourceRoot || target.startsWith(sourceRoot + sep) || sourceRoot.startsWith(target + sep))) {
    throw new Error("Sprite game destination must be separate from its installed source.");
  }
  let entries;
  try { entries = await readdir(target); } catch (error) { if (error.code !== "ENOENT") throw error; entries = []; }
  if (entries.length) throw new Error("Sprite game destination must be empty. Choose a new directory.");
  const registryFiles = new Map();
  if (payload) {
    if (!Array.isArray(payload.files)) throw new Error("Expected an unlocked registry JSON payload.");
    for (const file of payload.files) {
      if (typeof file.path !== "string" || typeof file.content !== "string") throw new Error("Registry files need text content.");
      const path = file.path.replace(/^src\/registry\/sprite-racer\//, "");
      if (registryFiles.has(path)) throw new Error(`Duplicate registry file: ${path}`);
      registryFiles.set(path, Buffer.from(file.content));
    }
  }
  const manifestBytes = payload ? registryFiles.get("sprite-racer.manifest.json") : await readFile(resolve(sourceRoot, "sprite-racer.manifest.json"));
  if (!manifestBytes) throw new Error("Sprite game source manifest is missing.");
  const manifest = JSON.parse(manifestBytes.toString());
  if (![1, 2].includes(manifest.version) || !Array.isArray(manifest.files) || !manifest.files.length) {
    throw new Error("Sprite game source manifest needs version 1 or 2 files.");
  }
  const copied = [];
  const paths = new Set();
  const generated = new Set(["game.config.ts", "race-preview.ts", "index.html", "package.json", "preview-server.ts"]);
  for (const file of manifest.files) {
    if (typeof file.path !== "string" || !file.path || typeof file.sha256 !== "string" || !/^[a-f0-9]{64}$/.test(file.sha256) || isAbsolute(file.path) || file.path.includes("\\") || file.path.split("/").some(part => !part || part === "." || part === "..") || paths.has(file.path)) {
      throw new Error("Sprite game manifest contains an unsafe file path.");
    }
    if (manifest.version === 2 && generated.has(file.path)) throw new Error("Manifest collides with a generated starter file.");
    paths.add(file.path);
    let bytes;
    if (payload) {
      bytes = registryFiles.get(file.path);
      if (!bytes) throw new Error(`Registry payload is missing: ${file.path}`);
    } else {
      const path = await realpath(resolve(sourceRoot, file.path));
      if (relative(sourceRoot, path).startsWith("..") || isAbsolute(relative(sourceRoot, path))) {
        throw new Error("Sprite game manifest points outside its source directory.");
      }
      bytes = await readFile(path);
    }
    if (createHash("sha256").update(bytes).digest("hex") !== file.sha256) {
      throw new Error(`Sprite game source checksum mismatch: ${file.path}`);
    }
    copied.push({ path: file.path, bytes });
  }
  await mkdir(target, { recursive: true });
  for (const file of copied) {
    const destination = resolve(target, file.path);
    await mkdir(dirname(destination), { recursive: true });
    await writeFile(destination, file.bytes, { flag: "wx" });
  }
  if (manifest.version === 2) {
    const gameTitle = title || (template === "delivery" ? "Coast Courier" : "Switchback");
    const config = { title: gameTitle, variant: template === "delivery" ? "delivery" : "circuit", initialMap: map, initialCar: car };
    await writeFile(resolve(target, "game.config.ts"), `import type { SwitchbackOptions } from "./mount-switchback";\n\nexport const gameConfig = ${JSON.stringify(config, null, 2)} satisfies SwitchbackOptions;\n`);
    await writeFile(resolve(target, "race-preview.ts"), `import { mountSwitchback } from "./mount-switchback";\nimport { gameConfig } from "./game.config";\nconst host = document.querySelector<HTMLElement>("#game-host");\nif (!host) throw new Error("Game host is missing.");\nmountSwitchback(host, { ...gameConfig, debug: true, demo: new URLSearchParams(location.search).has("demo") });\n`);
    await writeFile(resolve(target, "index.html"), `<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${gameTitle.replace(/[&<>\"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"})[c])}</title><link rel="stylesheet" href="/switchback.css"><style>html,body{margin:0;min-height:100%;background:#171c1a}#game-host{min-height:100dvh}</style></head><body><main id="game-host"></main><script type="module" src="/race-preview.js"></script></body></html>\n`);
    await writeFile(resolve(target, "package.json"), JSON.stringify({ name: basename(target).toLowerCase().replace(/[^a-z0-9-]/g, "-"), private: true, type: "module", scripts: { build: "bun build ./race-preview.ts --outfile ./race-preview.js --target browser", test: "bun verify-game.mjs", dev: "bun run preview-server.ts" } }, null, 2) + "\n");
    await writeFile(resolve(target, "preview-server.ts"), `const root = import.meta.dir;\nconst server = Bun.serve({ port: Number(process.env.PORT || 3000), async fetch(request) { const path = decodeURIComponent(new URL(request.url).pathname); if (path.split("/").includes("..")) return new Response("Not found", {status:404}); const file = Bun.file(root + (path === "/" ? "/index.html" : path)); return await file.exists() ? new Response(file) : new Response("Not found", {status:404}); } });\nconsole.log("Game preview listening on " + server.port);\n`);
  }
  return { directory: target, files: copied.length, engineVersion: manifest.version, template };
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const args = process.argv.slice(2);
  const source = args[args.indexOf("--source") + 1], out = args[args.indexOf("--out") + 1];
  if (!args.includes("--source") || !args.includes("--out") || !source || !out) {
    console.error("Usage: node create-game.mjs --source <source-directory-or-registry.json> --out <empty-directory> [--template racer|delivery] [--title name] [--map coast] [--car pickup]");
    process.exitCode = 1;
  } else {
    const option = name => args.includes(name) ? args[args.indexOf(name) + 1] : undefined;
    try { console.log(JSON.stringify(await createSpriteGame({ source, out, template: option("--template"), title: option("--title"), map: option("--map"), car: option("--car") }), null, 2)); }
    catch (error) { console.error(error.message); process.exitCode = 1; }
  }
}
