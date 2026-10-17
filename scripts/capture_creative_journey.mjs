#!/usr/bin/env node
// Full-repository convenience entry point; portable implementation is under the skill.
// No top-level await: compatible with Playwright test loading via Node's ESM bridge.
import {capture} from '../skills/studio-grade-web-transformation/scripts/capture_creative_journey.mjs';
import {readFile} from 'node:fs/promises';
import {resolve} from 'node:path';
export {capture};
async function main(){
  const index=process.argv.indexOf('--config');
  if(index<0||!process.argv[index+1])throw new Error('Usage: node scripts/capture_creative_journey.mjs --config path/to/storyboard.json');
  const config=JSON.parse(await readFile(resolve(process.argv[index+1]),'utf8'));
  console.log(JSON.stringify(await capture(config),null,2));
}
if(process.argv[1] && import.meta.url===new URL('file://'+resolve(process.argv[1])).href)
  main().catch(error=>{console.error('FAILED_CAPTURE:',error.message);process.exitCode=1;});
