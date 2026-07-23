const path = require("path");
const { pathToFileURL } = require("url");
const { chromium } = require("playwright");

async function render() {
  const input = path.resolve(__dirname, "wmi/2026-07-23/worqai-linkedin-recruiter-view-final.html");
  const output = path.resolve(__dirname, "wmi/2026-07-23/worqai-linkedin-recruiter-view-final.png");

  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1080, height: 1350 },
    deviceScaleFactor: 2,
  });
  const page = await context.newPage();

  await page.goto(pathToFileURL(input).href, { waitUntil: "networkidle" });
  await page.evaluate(async () => {
    if (document.fonts) {
      await document.fonts.ready;
    }
  });
  await page.waitForTimeout(800);

  await page.screenshot({ path: output, type: "png", fullPage: false });

  await browser.close();
  console.log("Rendered:", output);
}

render().catch((error) => {
  console.error(error);
  process.exit(1);
});
