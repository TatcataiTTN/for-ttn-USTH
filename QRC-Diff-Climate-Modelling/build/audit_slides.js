// Quet moi slide cua moi module bang Chrome that (puppeteer-core), kiem tra:
// tran chu (overflow), tieu de dang cau hoi, anh vo. Chay: node audit_slides.js
const puppeteer = require('/opt/homebrew/lib/node_modules/@mermaid-js/mermaid-cli/node_modules/puppeteer-core');
const MODULES = ['01-nen-tang-enso-pdo-easm','02-reservoir-computing-qrc','03-reservoir-computing-lineage',
  '04-generative-model-drifting','05-ung-dung-mo-rong-2-bai-bao','06-literature-textbook',
  '07-cac-the-he-mo-hinh-thoi-tiet'];
const BASE = 'http://localhost:8930';
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new' });
  const page = await browser.newPage();
  await page.setViewport({ width: 1180, height: 900 });
  let totalOverflow = 0, totalQuestionTitles = 0, totalBrokenImg = 0, totalSlides = 0;
  const report = [];
  for (const slug of MODULES) {
    const url = `${BASE}/vi/${slug}/index.html`;
    await page.goto(url, { waitUntil: 'networkidle0', timeout: 20000 });
    await page.waitForSelector('.mdeck-slide', { timeout: 10000 });
    await new Promise(r => setTimeout(r, 300)); // let deck.js fit() run on slide 0
    const nSlides = await page.$$eval('.mdeck-slide', els => els.length);
    const modResult = { slug, nSlides, issues: [] };
    for (let i = 0; i < nSlides; i++) {
      // Click "Sau" (next) i times from a fresh reload each time is slow; instead use dots to jump.
      if (i > 0) {
        const dots = await page.$$('.mdeck-dots button');
        if (dots[i]) { await dots[i].click(); await new Promise(r => setTimeout(r, 180)); await page.evaluate(() => new Promise(res => { const imgs=[...document.querySelectorAll(".mdeck-slide.active img")]; if(!imgs.length) return res(); let left=imgs.length; imgs.forEach(im => { if(im.complete) { if(--left<=0) res(); } else { im.onload=im.onerror=()=>{ if(--left<=0) res(); }; } }); setTimeout(res, 800); })); }
      }
      const data = await page.evaluate(() => {
        const s = document.querySelector('.mdeck-slide.active');
        if (!s) return null;
        const h2 = s.querySelector('h2'); const h1 = s.querySelector('h1');
        const title = h2 ? h2.textContent.trim() : (h1 ? h1.textContent.trim() : '(no title)');
        const imgs = [...s.querySelectorAll('img')].map(im => ({ src: im.getAttribute('src'), ok: im.complete && im.naturalWidth > 0 }));
        return {
          title, scrollH: s.scrollHeight, clientH: s.clientHeight,
          overflow: s.scrollHeight > s.clientHeight + 3,
          fontSize: s.style.fontSize,
          isDivider: s.classList.contains('part-divider'), isCover: s.classList.contains('cover'),
          brokenImgs: imgs.filter(x => !x.ok).map(x => x.src),
          textLen: s.textContent.length
        };
      });
      if (!data) continue;
      totalSlides++;
      const issues = [];
      if (data.overflow) { issues.push(`OVERFLOW scrollH=${data.scrollH} clientH=${data.clientH}`); totalOverflow++; }
      if (!data.isDivider && !data.isCover && /\?\s*$/.test(data.title)) { issues.push('TITLE_IS_QUESTION'); totalQuestionTitles++; }
      if (data.brokenImgs.length) { issues.push(`BROKEN_IMG: ${data.brokenImgs.join(',')}`); totalBrokenImg += data.brokenImgs.length; }
      if (issues.length) modResult.issues.push({ idx: i, title: data.title, issues, textLen: data.textLen });
    }
    report.push(modResult);
    console.log(`${slug}: ${nSlides} slides, ${modResult.issues.length} flagged`);
  }
  await browser.close();
  console.log('\n=== SUMMARY ===');
  console.log(`Total slides scanned: ${totalSlides}`);
  console.log(`Overflow (tràn chữ): ${totalOverflow}`);
  console.log(`Title is question: ${totalQuestionTitles}`);
  console.log(`Broken images: ${totalBrokenImg}`);
  console.log('\n=== DETAIL (only flagged) ===');
  for (const m of report) {
    if (m.issues.length) {
      console.log(`\n--- ${m.slug} ---`);
      for (const it of m.issues) console.log(`  slide ${it.idx} "${it.title}": ${it.issues.join(' | ')}`);
    }
  }
  require('fs').writeFileSync('/tmp/slide_audit.json', JSON.stringify(report, null, 1));
})();
