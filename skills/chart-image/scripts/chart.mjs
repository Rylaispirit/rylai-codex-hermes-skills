#!/usr/bin/env node
/**
 * Portable SVG chart generator for Codex, Hermes, and Claude.
 * Authored by Rylai as a dependency-free replacement for the missing legacy CLI.
 */

import fs from "node:fs";
import path from "node:path";
import process from "node:process";

const PALETTE = [
  "#2563eb",
  "#dc2626",
  "#059669",
  "#d97706",
  "#7c3aed",
  "#0891b2",
];

function usage() {
  console.log(`Usage:
  node scripts/chart.mjs --data '[{"x":"A","y":3}]' [options]
  type data.json | node scripts/chart.mjs [options]

Options:
  --type line|bar|area|point   Chart type (default: line)
  --data JSON                 JSON array; stdin is used when omitted
  --output PATH               .svg output (default: chart.svg)
  --title TEXT                Chart title
  --width N                   Width in pixels (default: 800)
  --height N                  Height in pixels (default: 450)
  --x-field NAME              X field (default: x)
  --y-field NAME              Y field (default: y)
  --series-field NAME         Optional multi-series field
  --color HEX                 Primary color
  --x-title TEXT              X-axis title
  --y-title TEXT              Y-axis title
  --y-domain MIN,MAX          Explicit Y domain
  --focus-recent N            Keep the last N records
  --show-values               Label points or bars
  --show-change               Show first-to-last percentage change
  --dark                      Dark theme
  --sparkline                 Hide axes and use compact defaults
  --help                      Show this message

PNG output is supported only when the optional "sharp" package is available.`);
}

function parseArgs(argv) {
  const options = {};
  const flags = new Set([
    "dark",
    "show-values",
    "show-change",
    "sparkline",
    "help",
  ]);
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      throw new Error(`Unexpected argument: ${token}`);
    }
    const key = token.slice(2);
    if (flags.has(key)) {
      options[key] = true;
      continue;
    }
    const value = argv[index + 1];
    if (value === undefined || value.startsWith("--")) {
      throw new Error(`Missing value for --${key}`);
    }
    options[key] = value;
    index += 1;
  }
  return options;
}

function escapeXml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&apos;");
}

function finiteNumber(value, label) {
  const number = Number(value);
  if (!Number.isFinite(number)) {
    throw new Error(`${label} must be numeric; received ${JSON.stringify(value)}`);
  }
  return number;
}

async function readData(options) {
  let raw = options.data;
  if (!raw) {
    raw = fs.readFileSync(0, "utf8").trim();
  }
  if (!raw) {
    throw new Error("Provide --data JSON or pipe a JSON array through stdin.");
  }
  const parsed = JSON.parse(raw);
  if (!Array.isArray(parsed) || parsed.length === 0) {
    throw new Error("Data must be a non-empty JSON array.");
  }
  return parsed;
}

function groupData(data, seriesField) {
  if (!seriesField) {
    return [["Series", data]];
  }
  const groups = new Map();
  for (const row of data) {
    const key = String(row[seriesField] ?? "Unspecified");
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(row);
  }
  return [...groups.entries()];
}

function linePath(points) {
  return points
    .map(([x, y], index) => `${index === 0 ? "M" : "L"} ${x.toFixed(2)} ${y.toFixed(2)}`)
    .join(" ");
}

function renderSvg(data, options) {
  const type = options.type ?? "line";
  if (!["line", "bar", "area", "point"].includes(type)) {
    throw new Error(`Unsupported chart type: ${type}`);
  }

  const sparkline = Boolean(options.sparkline);
  const width = finiteNumber(options.width ?? (sparkline ? 160 : 800), "width");
  const height = finiteNumber(options.height ?? (sparkline ? 48 : 450), "height");
  const margin = sparkline
    ? { top: 4, right: 4, bottom: 4, left: 4 }
    : { top: 64, right: 28, bottom: 64, left: 72 };
  const plotWidth = width - margin.left - margin.right;
  const plotHeight = height - margin.top - margin.bottom;
  if (plotWidth <= 0 || plotHeight <= 0) {
    throw new Error("Width and height are too small for the selected layout.");
  }

  const xField = options["x-field"] ?? "x";
  const yField = options["y-field"] ?? "y";
  const recent = options["focus-recent"]
    ? Math.max(1, Number.parseInt(options["focus-recent"], 10))
    : null;
  if (recent) data = data.slice(-recent);

  const rows = data.map((row, index) => ({
    row,
    index,
    x: row[xField] ?? index + 1,
    y: finiteNumber(row[yField], `${yField} at row ${index + 1}`),
  }));
  const yValues = rows.map((item) => item.y);
  let yMin = Math.min(0, ...yValues);
  let yMax = Math.max(0, ...yValues);
  if (options["y-domain"]) {
    const parts = String(options["y-domain"]).split(",").map(Number);
    if (parts.length !== 2 || parts.some((value) => !Number.isFinite(value))) {
      throw new Error("--y-domain must be MIN,MAX");
    }
    [yMin, yMax] = parts;
  }
  if (yMin === yMax) {
    const pad = Math.abs(yMin || 1) * 0.1;
    yMin -= pad;
    yMax += pad;
  }

  const dark = Boolean(options.dark);
  const colors = {
    background: dark ? "#111827" : "#ffffff",
    text: dark ? "#f3f4f6" : "#111827",
    muted: dark ? "#9ca3af" : "#6b7280",
    grid: dark ? "#374151" : "#e5e7eb",
  };
  const primary = options.color ?? PALETTE[0];
  const xAt = (index) =>
    rows.length === 1
      ? margin.left + plotWidth / 2
      : margin.left + (index / (rows.length - 1)) * plotWidth;
  const yAt = (value) =>
    margin.top + plotHeight - ((value - yMin) / (yMax - yMin)) * plotHeight;

  const svg = [];
  svg.push(
    `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">`,
    `<rect width="100%" height="100%" fill="${colors.background}"/>`,
    `<style>text{font-family:Arial,Helvetica,sans-serif;letter-spacing:0}</style>`,
  );

  if (!sparkline && options.title) {
    svg.push(
      `<text x="${margin.left}" y="34" font-size="22" font-weight="700" fill="${colors.text}">${escapeXml(options.title)}</text>`,
    );
  }

  if (!sparkline) {
    const ticks = 5;
    for (let index = 0; index <= ticks; index += 1) {
      const value = yMin + ((yMax - yMin) * index) / ticks;
      const y = yAt(value);
      svg.push(
        `<line x1="${margin.left}" y1="${y}" x2="${margin.left + plotWidth}" y2="${y}" stroke="${colors.grid}" stroke-width="1"/>`,
        `<text x="${margin.left - 10}" y="${y + 4}" text-anchor="end" font-size="12" fill="${colors.muted}">${escapeXml(Number(value.toPrecision(4)))}</text>`,
      );
    }
    const labelStep = Math.max(1, Math.ceil(rows.length / 10));
    rows.forEach((item, index) => {
      if (index % labelStep !== 0 && index !== rows.length - 1) return;
      svg.push(
        `<text x="${xAt(index)}" y="${margin.top + plotHeight + 24}" text-anchor="middle" font-size="12" fill="${colors.muted}">${escapeXml(item.x)}</text>`,
      );
    });
    if (options["x-title"]) {
      svg.push(
        `<text x="${margin.left + plotWidth / 2}" y="${height - 14}" text-anchor="middle" font-size="13" fill="${colors.text}">${escapeXml(options["x-title"])}</text>`,
      );
    }
    if (options["y-title"]) {
      svg.push(
        `<text x="18" y="${margin.top + plotHeight / 2}" text-anchor="middle" font-size="13" fill="${colors.text}" transform="rotate(-90 18 ${margin.top + plotHeight / 2})">${escapeXml(options["y-title"])}</text>`,
      );
    }
  }

  if (type === "bar") {
    const gap = Math.max(2, plotWidth * 0.015);
    const barWidth = Math.max(2, plotWidth / rows.length - gap);
    rows.forEach((item, index) => {
      const x = margin.left + (index / rows.length) * plotWidth + gap / 2;
      const y = yAt(Math.max(item.y, 0));
      const base = yAt(Math.min(item.y, 0));
      const top = Math.min(y, base);
      const barHeight = Math.max(1, Math.abs(base - y));
      svg.push(
        `<rect x="${x}" y="${top}" width="${barWidth}" height="${barHeight}" rx="2" fill="${primary}"/>`,
      );
      if (options["show-values"]) {
        svg.push(
          `<text x="${x + barWidth / 2}" y="${top - 6}" text-anchor="middle" font-size="11" fill="${colors.text}">${escapeXml(item.y)}</text>`,
        );
      }
    });
  } else {
    const groups = groupData(data, options["series-field"]);
    groups.forEach(([seriesName, groupRows], seriesIndex) => {
      const pointMap = new Map(groupRows.map((row) => [row, true]));
      const points = rows
        .filter((item) => pointMap.has(item.row))
        .map((item) => [xAt(item.index), yAt(item.y), item]);
      if (!points.length) return;
      const color = seriesIndex === 0 && options.color
        ? primary
        : PALETTE[seriesIndex % PALETTE.length];
      const pathData = linePath(points);
      if (type === "area") {
        const base = yAt(Math.max(yMin, 0));
        const area = `${pathData} L ${points.at(-1)[0]} ${base} L ${points[0][0]} ${base} Z`;
        svg.push(`<path d="${area}" fill="${color}" opacity="0.2"/>`);
      }
      if (type !== "point") {
        svg.push(
          `<path d="${pathData}" fill="none" stroke="${color}" stroke-width="${sparkline ? 2 : 3}" stroke-linejoin="round" stroke-linecap="round"/>`,
        );
      }
      points.forEach(([x, y, item]) => {
        if (type === "point" || options["show-values"]) {
          svg.push(`<circle cx="${x}" cy="${y}" r="${sparkline ? 2 : 4}" fill="${color}"/>`);
        }
        if (options["show-values"] && !sparkline) {
          svg.push(
            `<text x="${x}" y="${y - 9}" text-anchor="middle" font-size="11" fill="${colors.text}">${escapeXml(item.y)}</text>`,
          );
        }
      });
      if (!sparkline && groups.length > 1) {
        svg.push(
          `<text x="${margin.left + plotWidth - 4}" y="${margin.top + 16 + seriesIndex * 18}" text-anchor="end" font-size="12" fill="${color}">${escapeXml(seriesName)}</text>`,
        );
      }
    });
  }

  if (options["show-change"] && rows.length > 1 && !sparkline) {
    const first = rows[0].y;
    const last = rows.at(-1).y;
    const label = first === 0
      ? `Change: ${last - first >= 0 ? "+" : ""}${last - first}`
      : `Change: ${((last - first) / Math.abs(first) * 100).toFixed(1)}%`;
    svg.push(
      `<text x="${margin.left + plotWidth}" y="34" text-anchor="end" font-size="14" font-weight="700" fill="${last >= first ? "#059669" : "#dc2626"}">${escapeXml(label)}</text>`,
    );
  }

  svg.push("</svg>");
  return svg.join("\n");
}

async function writeOutput(svg, outputPath) {
  fs.mkdirSync(path.dirname(path.resolve(outputPath)), { recursive: true });
  if (path.extname(outputPath).toLowerCase() !== ".png") {
    fs.writeFileSync(outputPath, svg, "utf8");
    return;
  }
  let sharp;
  try {
    sharp = (await import("sharp")).default;
  } catch {
    throw new Error(
      'PNG output requires the optional "sharp" package. Use an .svg output path or install sharp.',
    );
  }
  await sharp(Buffer.from(svg)).png().toFile(outputPath);
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    usage();
    return;
  }
  const data = await readData(options);
  const svg = renderSvg(data, options);
  const output = options.output ?? "chart.svg";
  await writeOutput(svg, output);
  console.log(`Wrote ${output}`);
}

main().catch((error) => {
  console.error(`ERROR: ${error.message}`);
  process.exitCode = 1;
});
