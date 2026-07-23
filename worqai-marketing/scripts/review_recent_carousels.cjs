const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const sharp = require("sharp");

const ROOT = process.cwd();
const OUT = path.join(ROOT, "production", "_review_recent");
const CHROME = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

const files = [
  "production/carousel_tres-ajustes-doble-entrevistas_s11.html",
  "production/carousel_rrhh-no-dice-filtro_s01.html",
  "production/carousel_reclutador-vs-bot_s25.html",
  "production/carousel_palabras-que-busca-bot_s27.html",
  "production/carousel_experiencia-valida-formato-no_s06.html",
  "production/carousel_errores-6-segundos_s01.html",
  "production/carousel_cv-perfecto-no-pasa_s17.html",
  "production/carousel_cincuenta-a-cinco_s21.html",
  "production/carousel_ats-no-lee-como-humano_s04.html",
  "production/carousel_73-porciento-muere-filtro_s17.html",
];

async function ensureDir(dir) {
  await fs.promises.mkdir(dir, { recursive: true });
}

async function screenshotCarousel(browser, file) {
  const abs = path.resolve(ROOT, file);
  const name = path.basename(file, ".html");
  const dir = path.join(OUT, name);
  await ensureDir(dir);

  const page = await browser.newPage({ viewport: { width: 1080, height: 1080 }, deviceScaleFactor: 1 });
  await page.goto("file:///" + abs.replace(/\\/g, "/"), { waitUntil: "networkidle", timeout: 30000 });
  await page.waitForTimeout(1200);

  const count = await page.locator(".slide").count();
  const slidePaths = [];
  for (let i = 0; i < count; i++) {
    await page.evaluate((idx) => {
      const slides = Array.from(document.querySelectorAll(".slide"));
      slides.forEach((s, j) => {
        s.style.display = j === idx ? "flex" : "none";
        s.style.visibility = j === idx ? "visible" : "hidden";
        s.style.opacity = j === idx ? "1" : "0";
        s.style.position = j === idx ? "relative" : "absolute";
        s.style.transform = "none";
      });
      const track = document.querySelector(".track");
      if (track) track.style.transform = "none";
    }, i);
    await page.waitForTimeout(250);
    const out = path.join(dir, `slide_${String(i + 1).padStart(2, "0")}.png`);
    await page.locator(".slide").nth(i).screenshot({ path: out, type: "png" });
    slidePaths.push(out);
  }
  await page.close();

  const thumb = 360;
  const gap = 18;
  const labelH = 34;
  const cols = 2;
  const rows = Math.ceil(count / cols);
  const sheetW = cols * thumb + (cols + 1) * gap;
  const sheetH = labelH + rows * thumb + (rows + 1) * gap;
  const composites = [];

  for (let i = 0; i < slidePaths.length; i++) {
    const x = gap + (i % cols) * (thumb + gap);
    const y = labelH + gap + Math.floor(i / cols) * (thumb + gap);
    const buf = await sharp(slidePaths[i]).resize(thumb, thumb).png().toBuffer();
    composites.push({ input: buf, left: x, top: y });
  }

  const titleSvg = Buffer.from(`
  <svg width="${sheetW}" height="${labelH}" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="#111"/>
    <text x="18" y="23" fill="#fff" font-size="16" font-family="Arial, sans-serif">${name}</text>
  </svg>`);

  const sheet = path.join(OUT, `${name}_sheet.png`);
  await sharp({
    create: {
      width: sheetW,
      height: sheetH,
      channels: 4,
      background: "#151515",
    },
  })
    .composite([{ input: titleSvg, left: 0, top: 0 }, ...composites])
    .png()
    .toFile(sheet);

  return { file, name, count, sheet };
}

(async () => {
  await ensureDir(OUT);
  const browser = await chromium.launch({
    executablePath: CHROME,
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--allow-file-access-from-files"],
  });
  const results = [];
  for (const file of files) {
    results.push(await screenshotCarousel(browser, file));
  }
  await browser.close();
  console.log(JSON.stringify(results, null, 2));
})();
