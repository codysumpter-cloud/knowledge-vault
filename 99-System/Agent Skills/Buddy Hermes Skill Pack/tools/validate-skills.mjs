#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(process.argv[2] || "./buddy-agent/skills");
const required = [
  "id",
  "name",
  "version",
  "source",
  "platforms",
  "risk_class",
  "readable",
  "auto_executable",
  "requires_prismtek_approval",
  "adapters"
];

function walk(dir, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(p, out);
    else if (entry.name === "metadata.json") out.push(p);
  }
  return out;
}

let failed = false;
const files = walk(root);

if (!files.length) {
  console.error(`No metadata.json files found under ${root}`);
  process.exit(1);
}

for (const file of files) {
  const metadata = JSON.parse(fs.readFileSync(file, "utf8"));
  const missing = required.filter((key) => !(key in metadata));
  if (missing.length) {
    failed = true;
    console.error(`FAIL ${file}: missing ${missing.join(", ")}`);
    continue;
  }
  if (metadata.auto_executable && ["external-action", "destructive", "money"].includes(metadata.risk_class)) {
    failed = true;
    console.error(`FAIL ${file}: high-risk skill cannot default to auto_executable=true`);
    continue;
  }
  console.log(`OK   ${metadata.id} (${metadata.risk_class})`);
}

if (failed) process.exit(1);

console.log(`\nValidated ${files.length} skill metadata files.`);
