#!/usr/bin/env node
import { writeFile } from "node:fs/promises";

const args = process.argv.slice(2);
const out = args[args.indexOf("--out") + 1];
if (!args.includes("--out") || !out) throw new Error("Usage: node fetch-source.mjs --out <new-registry.json>");
const key = process.env.MODULO_REGISTRY_KEY;
if (!key) throw new Error("Set MODULO_REGISTRY_KEY to an active mint key. Do not put the key in a command argument.");
const response = await fetch("https://modulo.maynkudu.com/r/sprite-racer.json", { headers: { Authorization: `Bearer ${key}` } });
if (!response.ok) throw new Error(`Source request failed (${response.status}). Check that the mint key is active.`);
const payload = await response.text();
const parsed = JSON.parse(payload);
if (!Array.isArray(parsed.files) || !parsed.files.some(file => typeof file.content === "string")) throw new Error("Registry response has no unlocked files.");
await writeFile(out, payload, { mode: 0o600, flag: "wx" });
console.log("Saved unlocked source to the requested local file.");
