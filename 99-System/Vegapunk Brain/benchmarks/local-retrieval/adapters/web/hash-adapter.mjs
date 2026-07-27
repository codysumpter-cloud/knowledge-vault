#!/usr/bin/env node
import crypto from "node:crypto";
import readline from "node:readline";

const dimension = 256;

function tokens(text) {
  return text.toLowerCase().match(/[a-z0-9_-]+/g) ?? [];
}

function embedding(text) {
  const vector = new Array(dimension).fill(0);
  const base = tokens(text);
  const features = [...base, ...base.slice(0, -1).map((item, index) => `${item}::${base[index + 1]}`)];
  for (const feature of features) {
    const digest = crypto.createHash("sha256").update(feature).digest();
    const index = digest.readUInt32BE(0) % dimension;
    vector[index] += digest[4] % 2 === 0 ? 1 : -1;
  }
  const norm = Math.sqrt(vector.reduce((sum, value) => sum + value * value, 0)) || 1;
  return vector.map((value) => value / norm);
}

function respond(request) {
  if (request.op === "metadata") {
    return {
      metadata: {
        name: "hash-ngram-web-fallback",
        runtime: "node-web-compatible",
        model: "none",
        model_download_mb: 0,
        offline: true,
        native_acceleration: false,
        browser_fallback: true,
        dimension,
      },
    };
  }
  if (request.op === "embed" && Array.isArray(request.texts)) {
    return { vectors: request.texts.map(embedding) };
  }
  throw new Error("unsupported request");
}

const rl = readline.createInterface({ input: process.stdin, crlfDelay: Infinity });
for await (const line of rl) {
  if (!line.trim()) continue;
  try {
    console.log(JSON.stringify(respond(JSON.parse(line))));
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
