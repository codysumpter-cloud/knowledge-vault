#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
function getArg(name) {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : null;
}
const dryRun = args.includes('--dry-run');
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const hermesRepo = getArg('--hermes-repo');
const hermesHome = getArg('--hermes-home');
const buddy = getArg('--buddy');
const vault = getArg('--vault');

function copyDir(src, dst) {
  if (!fs.existsSync(src)) return;
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const sp = path.join(src, entry.name);
    const dp = path.join(dst, entry.name);
    if (entry.isDirectory()) copyDir(sp, dp);
    else {
      console.log(`${dryRun ? 'would copy' : 'copy'} ${sp} -> ${dp}`);
      if (!dryRun) {
        fs.mkdirSync(path.dirname(dp), { recursive: true });
        fs.copyFileSync(sp, dp);
      }
    }
  }
}

if (!hermesRepo && !hermesHome && !buddy && !vault) {
  console.error('Provide at least one target: --hermes-repo, --hermes-home, --buddy, or --vault');
  process.exit(1);
}

if (hermesRepo) copyDir(path.join(root, 'hermes-agent', 'skills'), path.join(hermesRepo, 'skills'));
if (hermesHome) copyDir(path.join(root, 'hermes-user-skills'), path.join(hermesHome, 'skills'));
if (buddy) copyDir(path.join(root, 'buddy-agent', 'skills'), path.join(buddy, 'skills'));
if (vault) copyDir(path.join(root, 'KnowledgeVault', '99-System', 'Agent Skills'), path.join(vault, '99-System', 'Agent Skills'));

console.log(dryRun ? '\nDry run complete.' : '\nInstall complete. Restart Hermes or run /reload-skills in a live session.');
