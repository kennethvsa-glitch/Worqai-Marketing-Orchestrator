"use strict";

/**
 * Render every `.slide` element in a carousel HTML file to PNG.
 *
 * Usage:
 *   node render_carousel.cjs path/to/carousel.html --out path/to/output
 */

const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");
const { chromium } = require("playwright");

function parseArgs(argv) {
  const html = argv[2];
  const outIndex = argv.indexOf("--out");
  const output = outIndex >= 0 ? argv[outIndex + 1] : null;

  if (!html || !output) {
    throw new Error(
      "Usage: node render_carousel.cjs path/to/carousel.html --out path/to/output",
    );
  }

  return {
    html: path.resolve(html),
    output: path.resolve(output),
  };
}

async function render() {
  const { html, output } = parseArgs(process.argv);
  fs.mkdirSync(output, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    viewport: { width: 1080, height: 1350 },
    deviceScaleFactor: 1,
  });

  await page.goto(pathToFileURL(html).href, { waitUntil: "networkidle" });
  await page.evaluate(async () => {
    document.body.style.padding = "0";
    document.body.style.gap = "0";
    document.querySelectorAll(".slide").forEach((slide) => {
      slide.classList.add("is-rendering");
    });
    await document.fonts.ready;
  });

  const slides = page.locator(".slide");
  const count = await slides.count();
  if (!count) throw new Error("No elements matching .slide were found");

  const rendered = [];
  for (let index = 0; index < count; index += 1) {
    const slide = slides.nth(index);
    const box = await slide.boundingBox();
    if (!box) throw new Error(`Slide ${index + 1} has no bounding box`);
    if (Math.round(box.width) !== 1080 || Math.round(box.height) !== 1350) {
      throw new Error(
        `Slide ${index + 1} is ${box.width}x${box.height}; expected 1080x1350`,
      );
    }

    const filename = `slide_${String(index + 1).padStart(2, "0")}.png`;
    const destination = path.join(output, filename);
    await slide.screenshot({ path: destination, animations: "disabled" });
    rendered.push(filename);
  }

  const contactHtml = `<!doctype html>
  <html>
  <head>
    <meta charset="utf-8">
    <style>
      * { box-sizing: border-box; }
      html, body { margin: 0; background: #050608; }
      body {
        width: 1540px;
        padding: 20px;
        display: grid;
        grid-template-columns: repeat(4, 360px);
        gap: 20px;
        color: #b7ff00;
        font: 700 15px Consolas, monospace;
      }
      figure { margin: 0; }
      img {
        display: block;
        width: 360px;
        height: 450px;
        object-fit: cover;
        border: 1px solid #2a3038;
      }
      figcaption { padding-top: 9px; }
    </style>
  </head>
  <body>
    ${rendered
      .map(
        (filename, index) =>
          `<figure><img src="${filename}"><figcaption>SLIDE ${String(index + 1).padStart(2, "0")}</figcaption></figure>`,
      )
      .join("")}
  </body>
  </html>`;

  const contactSource = path.join(output, "contact-sheet.html");
  fs.writeFileSync(contactSource, contactHtml, "utf8");

  const contactPage = await browser.newPage({
    viewport: { width: 1540, height: 1020 },
    deviceScaleFactor: 1,
  });
  await contactPage.goto(pathToFileURL(contactSource).href, {
    waitUntil: "networkidle",
  });
  await contactPage.screenshot({
    path: path.join(output, "contact-sheet.png"),
    fullPage: true,
  });

  await browser.close();
  console.log(`Rendered ${rendered.length} slides to ${output}`);
  console.log(`Contact sheet: ${path.join(output, "contact-sheet.png")}`);
}

render().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
