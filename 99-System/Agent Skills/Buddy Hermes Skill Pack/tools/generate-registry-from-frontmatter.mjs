#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const skillsRoot = path.resolve(process.argv[2] || "./buddy-agent/skills/imported");
const outFile = path.resolve(process.argv[3] || "./buddy-agent/skills/registry.generated.json");

function walk(dir, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(p, out);
    else if (entry.name === "metadata.json") out.push(p);
  }
  return out;
}

const skills = walk(skillsRoot).map((file) => {
  const m = JSON.parse(fs.readFileSync(file, "utf8"));
  return {
    id: m.id,
    name: m.name,
    path: path.posix.join("skills", path.relative(path.resolve(path.dirname(outFile)), path.join(path.dirname(file), "SKILL.md")).split(path.sep).join("/")),
    source: m.source,
    risk_class: m.risk_class,
    default_mode: m.default_mode,
    platforms: m.platforms,
    adapters: m.adapters,
    readable: m.readable,
    auto_executable: m.auto_executable,
    requires_prismtek_approval: m.requires_prismtek_approval,
    manual_only_by_default: Boolean(m.manual_only_by_default),
    status: "reviewed-buddy-compatible-skill"
  };
});

fs.mkdirSync(path.dirname(outFile), { recursive: true });
fs.writeFileSync(outFile, JSON.stringify({ version: "1.0.0", skills }, null, 2) + "\n");
console.log(`Wrote ${outFile}`);
