#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const packRoot = path.resolve(__dirname, "..");

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const token = argv[i];
    if (token === "--dry-run") {
      args.dryRun = true;
      continue;
    }
    if (token.startsWith("--")) {
      const key = token.slice(2);
      const value = argv[++i];
      if (!value) throw new Error(`Missing value for ${token}`);
      args[key] = value;
    }
  }
  return args;
}

function copyDir(src, dest, dryRun) {
  if (!fs.existsSync(src)) return [];
  const actions = [];
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const s = path.join(src, entry.name);
    const d = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      actions.push(...copyDir(s, d, dryRun));
    } else {
      actions.push({ src: s, dest: d });
      if (!dryRun) {
        fs.mkdirSync(path.dirname(d), { recursive: true });
        fs.copyFileSync(s, d);
      }
    }
  }
  return actions;
}

function writeJson(file, data, dryRun) {
  if (!dryRun) {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, JSON.stringify(data, null, 2) + "\n");
  }
  return { src: "<generated>", dest: file };
}

const args = parseArgs(process.argv);

if (!args.buddy && !args.hermes) {
  console.error("Usage: node tools/install-skill-pack.mjs --buddy /path/to/buddy-agent --hermes /path/to/hermes-agent --vault /path/to/KnowledgeVault [--dry-run]");
  process.exit(1);
}

const actions = [];

if (args.buddy) {
  const buddyTarget = path.resolve(args.buddy);
  actions.push(...copyDir(path.join(packRoot, "buddy-agent"), buddyTarget, args.dryRun));

  if (args.vault) {
    actions.push(writeJson(
      path.join(buddyTarget, "skills", "knowledge-vault-skill-sources.local.json"),
      {
        version: "1.0.0",
        local_override: true,
        sources: [
          {
            id: "knowledge-vault-agent-skills-local",
            label: "Local KnowledgeVault Agent Skills",
            path: path.resolve(args.vault, "99-System", "Agent Skills"),
            readable: true,
            auto_import: false,
            auto_execute: false
          }
        ]
      },
      args.dryRun
    ));
  }
}

if (args.hermes) {
  const hermesTarget = path.resolve(args.hermes);
  actions.push(...copyDir(path.join(packRoot, "hermes-agent"), hermesTarget, args.dryRun));
}

console.log(args.dryRun ? "Dry run copy plan:" : "Installed files:");
for (const action of actions) {
  console.log(`- ${action.dest}`);
}

if (args.dryRun) {
  console.log("\nNo files were written.");
} else {
  console.log("\nDone. Run `node tools/validate-skills.mjs <buddy-agent>/skills` to validate metadata.");
}
