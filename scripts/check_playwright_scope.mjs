#!/usr/bin/env node
/** Reject accidental discovery of vendored or unrelated test suites.
 * Playwright JSON lists tests without starting a browser or webServer.
 */
import { spawnSync } from 'node:child_process';
import path from 'node:path';
const runner = process.platform === 'win32' ? 'npx.cmd' : 'npx';
const result = spawnSync(runner, ['playwright','test','--list','--reporter=json'], {
  cwd: path.resolve(import.meta.dirname, '..'),
  encoding: 'utf8', maxBuffer: 16 * 1024 * 1024
});
if (result.error || result.status !== 0) {
  console.error(result.stderr || result.error || result.stdout);
  process.exit(1);
}
let listing;
try { listing = JSON.parse(result.stdout); }
catch (error) { console.error('Invalid Playwright --list JSON:', error.message); process.exit(1); }
const files = new Set();
let count = 0;
function inspect(suites) {
  for (const suite of suites || []) {
    for (const spec of suite.specs || []) {
      count += (spec.tests || []).length;
      const file = spec.file || suite.file;
      if (!file) { console.error('Missing spec path'); process.exitCode = 1; continue; }
      let normalized = path.isAbsolute(file) ? path.relative(process.cwd(), file) : file;
      normalized = normalized.replaceAll('\\', '/').replace(/^\.\//, '');
      files.add(normalized);
      if (!(/^tests\/browser\/.+\.spec\.ts$/.test(normalized) || normalized === 'examples/playwright-visual.spec.ts')) {
        console.error('OUT OF SCOPE test discovered: ' + normalized);
        process.exitCode = 1;
      }
    }
    inspect(suite.suites);
  }
}
inspect(listing.suites);
if (count === 0 || files.size === 0) { console.error('No first-party browser tests discovered'); process.exitCode = 1; }
if (process.exitCode) process.exit(process.exitCode);
console.log('PASS: ' + count + ' first-party test cases in ' + files.size + ' files; no vendored suites discovered.');
