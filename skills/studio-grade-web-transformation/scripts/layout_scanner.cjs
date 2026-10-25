// CommonJS core, shared by Playwright test transpiler and ESM CLI.
// Pure browser measurement only; no network/IO or aesthetic scoring.
async function inspectPage(page) {
  return await page.evaluate(() => {
    const root = document.documentElement;
    const viewport = root.clientWidth;
    const overflow = Math.max(0, root.scrollWidth - viewport);
    const smallTargets = [];
    const interactive = document.querySelectorAll(
      'button, [role="button"], input:not([type="hidden"]), select, textarea, a[href]'
    );
    for (const el of interactive) {
      const style = getComputedStyle(el);
      if (style.display === 'none' || style.visibility === 'hidden' ||
          Number(style.opacity) === 0 || el.closest('[aria-hidden="true"]')) continue;
      const rect = el.getBoundingClientRect();
      if (rect.width <= 0 || rect.height <= 0) continue;
      // Inline links in paragraph text have spacing exceptions; custom targets
      // are candidates for human inspection, not WCAG violations.
      if (el.tagName === 'A' && style.display === 'inline') continue;
      if (rect.width < 24 || rect.height < 24) {
        smallTargets.push({
          tag: el.tagName.toLowerCase(),
          label: (el.getAttribute('aria-label') || el.textContent || '').trim().slice(0, 64),
          width: Math.round(rect.width), height: Math.round(rect.height),
          reason: 'TARGET_BELOW_24PX_REVIEW'
        });
      }
      if (smallTargets.length >= 30) break;
    }
    // Loaded but unusable images damage the actual experience. Never mistake
    // an offscreen lazy image (not yet loaded) for a confirmed broken asset.
    const brokenImages = [];
    for (const el of document.images) {
      const style=getComputedStyle(el);
      if (style.display === 'none' || style.visibility === 'hidden') continue;
      const bounds=el.getBoundingClientRect();
      if (!bounds.width || !bounds.height || !el.complete || el.naturalWidth > 0) continue;
      brokenImages.push({
        tag:'img',
        alt:(el.getAttribute('alt') || '').slice(0,80),
        src:(el.currentSrc || el.getAttribute('src') || '').slice(0,160),
        reason:'IMAGE_RESOURCE_FAILED_REVIEW'
      });
      if (brokenImages.length >= 30) break;
    }
    const headings = [];
    for (const el of document.querySelectorAll('h1,h2,h3')) {
      const rect = el.getBoundingClientRect();
      if (rect.width && rect.height && el.scrollWidth > el.clientWidth + 3 &&
          getComputedStyle(el).overflowX !== 'visible') {
        headings.push({tag: el.tagName.toLowerCase(),
          text: (el.textContent || '').trim().slice(0, 64),
          reason: 'POSSIBLY_CLIPPED_HEADING_REVIEW'});
      }
      if (headings.length >= 30) break;
    }
    return {
      prefers_reduced_motion:window.matchMedia('(prefers-reduced-motion: reduce)').matches,
       viewport_css_px: viewport,
      document_scroll_width_css_px: root.scrollWidth,
      horizontal_overflow_px: overflow,
      flags: [
        ...(overflow > 2 ? [{code:'HORIZONTAL_OVERFLOW_REVIEW',px:overflow}] : []),
        ...smallTargets.map(x=>({code:x.reason,...x})),
        ...brokenImages.map(x=>({code:x.reason,...x})),
        ...headings.map(x=>({code:x.reason,...x}))
      ],
      interactive_elements_inspected: interactive.length,
      limitations: [
        'Viewport-state DOM rectangles only; no artistic quality measurement',
        '24px candidates are not automatic WCAG failures; spacing exceptions exist',
        'No hidden states, route transitions, assistive technology or user testing proved',
        'A blocked external image may appear broken; inspect asset/network provenance'
      ]
    };
  });
}

module.exports = { inspectPage };
