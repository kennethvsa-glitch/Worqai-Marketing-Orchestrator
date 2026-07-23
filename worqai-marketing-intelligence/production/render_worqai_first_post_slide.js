const path = require("path");
const { pathToFileURL } = require("url");
const { chromium } = require("playwright");

async function render() {
  const input = path.resolve(__dirname, "worqai-linkedin-first-post-slide.html");
  const output = path.resolve(__dirname, "worqai-linkedin-first-post-slide@2x.png");

  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1080, height: 1080 },
    deviceScaleFactor: 2,
  });
  const page = await context.newPage();

  await page.goto(pathToFileURL(input).href, { waitUntil: "networkidle" });
  await page.evaluate(async () => {
    if (document.fonts) {
      await document.fonts.ready;
    }
  });
  await page.waitForTimeout(400);

  const slide = page.locator("#slide");
  await slide.screenshot({ path: output, type: "png" });

  await browser.close();
  console.log(output);
}

render().catch((error) => {
  console.error(error);
  process.exit(1);
});
