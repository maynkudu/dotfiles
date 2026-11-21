import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdtemp, mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { test } from "node:test";
import { createSpriteGame } from "./create-game.mjs";

async function fixture() {
  const root = await mkdtemp("/tmp/opencode/sprite-skill-test-");
  const source = join(root, "source"); await mkdir(source);
  const content = "export const example = 1;\n";
  await writeFile(join(source, "example.ts"), content);
  await writeFile(join(source, "sprite-racer.manifest.json"), JSON.stringify({ version: 1, files: [{ path: "example.ts", sha256: createHash("sha256").update(content).digest("hex") }] }));
  return { root, source, content };
}

test("copies a verified source into a fresh fixture", async () => {
  const { root, source, content } = await fixture(), out = join(root, "out");
  assert.equal((await createSpriteGame({ source, out })).files, 1);
  assert.equal(await readFile(join(out, "example.ts"), "utf8"), content);
});

test("preserves existing files in a populated destination", async () => {
  const { root, source } = await fixture(), out = join(root, "out");
  await mkdir(out); await writeFile(join(out, "keep.txt"), "user work");
  await assert.rejects(createSpriteGame({ source, out }), /must be empty/);
  assert.equal(await readFile(join(out, "keep.txt"), "utf8"), "user work");
});

test("corrupt source fails before writing any destination", async () => {
  const { root, source } = await fixture(), out = join(root, "out");
  await writeFile(join(source, "example.ts"), "modified");
  await assert.rejects(createSpriteGame({ source, out }), /checksum mismatch/);
  await assert.rejects(readdir(out), { code: "ENOENT" });
});

test("rejects nested and escaping destinations", async () => {
  const { root, source } = await fixture();
  await assert.rejects(createSpriteGame({ source, out: join(source, "nested") }), /must be separate/);
  await writeFile(join(source, "sprite-racer.manifest.json"), JSON.stringify({ version: 1, files: [{ path: "../escape", sha256: "bad" }] }));
  await assert.rejects(createSpriteGame({ source, out: join(root, "out") }), /unsafe file path/);
});

test("generates a delivery starter from raw registry JSON beside its input", async () => {
  const { root, source, content } = await fixture();
  const manifest = JSON.parse(await readFile(join(source, "sprite-racer.manifest.json"), "utf8"));
  manifest.version = 2;
  const payload = { files: [
    { path: "src/registry/sprite-racer/example.ts", content },
    { path: "src/registry/sprite-racer/sprite-racer.manifest.json", content: JSON.stringify(manifest) },
  ] };
  const registry = join(root, "registry.json"), out = join(root, "courier");
  await writeFile(registry, JSON.stringify(payload));
  const result = await createSpriteGame({ source: registry, out, template: "delivery", title: "Coast Courier" });
  assert.equal(result.template, "delivery");
  assert.equal(await readFile(join(out, "example.ts"), "utf8"), content);
  assert.match(await readFile(join(out, "game.config.ts"), "utf8"), /"variant": "delivery"/);
  assert.match(await readFile(join(out, "index.html"), "utf8"), /Coast Courier/);
});

test("validates configuration before creating the destination", async () => {
  const { root, source } = await fixture(), out = join(root, "out");
  await assert.rejects(createSpriteGame({ source, out, title: " " }), /Title/);
  await assert.rejects(createSpriteGame({ source, out, map: "unknown" }), /content IDs/);
  await assert.rejects(readdir(out), { code: "ENOENT" });
});
