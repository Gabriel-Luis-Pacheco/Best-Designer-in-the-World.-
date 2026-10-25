import {test,expect} from '@playwright/test';
import {runAudit} from '../../skills/studio-grade-web-transformation/scripts/layout_audit.mjs';
test('normal and reduced-motion sessions are different browser conditions',async()=>{
  const url='http://127.0.0.1:4173/examples/vesper-sculptural-light-study.html';
  const reduce=await runAudit({url,motion:'reduce'});
  const normal=await runAudit({url,motion:'normal'});
  expect(reduce.motion_mode).toBe('reduce');
  expect(normal.motion_mode).toBe('normal');
  for(const frame of reduce.viewports)expect(frame.prefers_reduced_motion).toBe(true);
  for(const frame of normal.viewports)expect(frame.prefers_reduced_motion).toBe(false);
  // This verifies correct browser preference only, not temporal design quality.
});
