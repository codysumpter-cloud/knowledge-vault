#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const root = process.argv[2] || 'hermes-agent/skills';
const errors = [];
let count = 0;

function walk(dir) {
  if (!fs.existsSync(dir)) return;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(p);
    else if (entry.isFile() && entry.name === 'SKILL.md') validate(p);
  }
}

function parseFrontmatter(content, file) {
  if (!content.startsWith('---\n')) throw new Error('frontmatter must start at byte 0 with ---');
  const close = content.indexOf('\n---\n', 4);
  if (close === -1) throw new Error('missing closing frontmatter delimiter');
  const raw = content.slice(4, close);
  const body = content.slice(close + 5);
  if (!body.trim()) throw new Error('body is empty');
  const fm = {};
  const lines = raw.split(/\r?\n/);
  for (const line of lines) {
    const m = line.match(/^([A-Za-z0-9_.-]+):\s*(.*)$/);
    if (m) fm[m[1]] = m[2].trim();
  }
  return { fm, body };
}

function validate(file) {
  count++;
  const content = fs.readFileSync(file, 'utf8');
  try {
    const { fm, body } = parseFrontmatter(content, file);
    if (!fm.name) throw new Error('missing name');
    if (!fm.description) throw new Error('missing description');
    if (fm.name.length > 64) throw new Error('name > 64 chars');
    if (!/^[a-z0-9][a-z0-9-]*$/.test(fm.name)) throw new Error('name must be lowercase hyphenated');
    const desc = fm.description.replace(/^['"]|['"]$/g, '');
    if (!desc.startsWith('Use when')) throw new Error('description should start with "Use when"');
    if (desc.length > 1024) throw new Error('description > 1024 chars');
    for (const required of ['version:', 'author:', 'license:', 'metadata:', 'hermes:', 'tags:', 'related_skills:']) {
      if (!content.includes(required)) throw new Error(`missing peer metadata marker ${required}`);
    }
    for (const section of ['## Overview', '## When to Use', '## Common Pitfalls', '## Verification Checklist']) {
      if (!body.includes(section)) throw new Error(`missing section ${section}`);
    }
    if (content.length > 100000) throw new Error('SKILL.md exceeds 100,000 chars');
    console.log(`OK   ${file}`);
  } catch (err) {
    errors.push(`${file}: ${err.message}`);
    console.error(`FAIL ${file}: ${err.message}`);
  }
}

walk(root);
if (!count) {
  console.error(`No SKILL.md files found under ${root}`);
  process.exit(1);
}
if (errors.length) {
  console.error(`\n${errors.length} validation error(s).`);
  process.exit(1);
}
console.log(`\nValidated ${count} Hermes-style skill files.`);
