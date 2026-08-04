// ─── Feature Slugs ───────────────────────────────────────────────────────────
// All 44 figures on the roster have a content/features/<slug>.json (short card).
export const FEATURE_SLUGS = [
  // Ancient Philosophy
  "marcus-aurelius", "seneca", "epictetus", "aristotle", "plato",
  "heraclitus", "lao-tzu", "confucius", "diogenes", "boethius",
  // Literature
  "nietzsche", "dostoevsky", "tolstoy", "camus", "kafka",
  "hemingway", "pessoa", "borges", "cormac-mccarthy", "james-baldwin",
  "virginia-woolf", "rilke",
  // Warrior
  "musashi", "sun-tzu", "bruce-lee", "muhammad-ali", "kobe-bryant",
  "michael-jordan", "khabib", "mcgregor", "tyson-fury", "roger-federer",
  // Modern Thinkers
  "carl-jung", "viktor-frankl", "rumi", "alan-watts", "krishnamurti",
  "joseph-campbell", "simone-weil", "steve-jobs", "charlie-munger",
  "naval-ravikant", "ryan-holiday", "nassim-taleb"
];

// ─── Figure Slugs ────────────────────────────────────────────────────────────
// Slugs that also have a full content/figures/<slug>.json (rich detail page,
// the nine-step extraction). 12 of 44 as of 2026-07-30.
export const FIGURE_SLUGS = [
  "marcus-aurelius", "seneca", "epictetus", "aristotle",
  "camus", "nietzsche", "dostoevsky", "kafka",
  "musashi", "bruce-lee", "sun-tzu",
  "viktor-frankl", "carl-jung", "simone-weil", "alan-watts", "naval-ravikant"
];

// ─── Image Map ───────────────────────────────────────────────────────────────
// Maps slug -> relative path from project root. null = no image yet;
// getImagePath() returning null is what triggers the initials/placeholder
// fallback in figure.html and index.html -- never leave a path pointing at
// a file that doesn't exist, always null instead.
export const IMAGE_MAP = {
  // Ancient Philosophy
  "marcus-aurelius": "content/images/marcus-aurelius.avif",
  "seneca":          null, // still content/images/seneca.htm -- not a real image, needs replacing
  "epictetus":       "content/images/epictetus.jpg",
  "aristotle":       "content/images/aristotle.jpg",
  "plato":           "content/images/plato.jpg",
  "heraclitus":      "content/images/heraclitus.jpg",
  "lao-tzu":         "content/images/lao-tzu.jpg", // was "Sao Tzu.jpg" -- inferred, not confirmed by Kartik
  "confucius":       "content/images/confucius.jpg",
  "diogenes":        "content/images/diogenes.jpg",
  "boethius":        "content/images/boethius.jpg",

  // Literature
  "nietzsche":       "content/images/nietzsche.jpg",
  "dostoevsky":      "content/images/dostoevsky.jpg",
  "tolstoy":         "content/images/tolstoy.jpg",
  "camus":           "content/images/camus.jpg",
  "kafka":           "content/images/kafka.jpg",
  "hemingway":       "content/images/hemingway.jpg",
  "pessoa":          "content/images/pessoa.jpg",
  "borges":          "content/images/borges.jpg",
  "cormac-mccarthy": "content/images/cormac-mccarthy.jpg",
  "james-baldwin":   "content/images/james-baldwin.jpg",
  "virginia-woolf":  "content/images/virginia-woolf.jpg",
  "rilke":           "content/images/rilke.jpg",

  // Warrior
  "musashi":         "content/images/musashi.jpg",
  "sun-tzu":         "content/images/sun-tzu.jpg",
  "bruce-lee":       "content/images/bruce-lee.jpg",
  "muhammad-ali":    "content/images/muhammad-ali.jpg",
  "kobe-bryant":     "content/images/kobe-bryant.jpg",
  "michael-jordan":  "content/images/michael-jordan.jpg",
  "khabib":          "content/images/khabib.jpg",
  "mcgregor":        null, // no image file was ever provided
  "tyson-fury":      "content/images/tyson-fury.jpg",
  "roger-federer":   "content/images/roger-federer.jpg",

  // Modern Thinkers
  "carl-jung":       "content/images/carl-jung.jpg",
  "viktor-frankl":   "content/images/viktor-frankl.jpg",
  "rumi":            "content/images/rumi.jpg",
  "alan-watts":      "content/images/alan-watts.jpg",
  "krishnamurti":    "content/images/krishnamurti.jpg",
  "joseph-campbell": "content/images/joseph-campbell.jpg",
  "simone-weil":     "content/images/simone-weil.jpg",
  "steve-jobs":      "content/images/steve-jobs.jpg",
  "charlie-munger":  "content/images/charlie-munger.jpg",
  "naval-ravikant":  "content/images/naval-ravikant.jpg",
  "ryan-holiday":    "content/images/ryan-holiday.jpg",
  "nassim-taleb":    "content/images/nassim-taleb.jpg"
};

// ─── Loaders ─────────────────────────────────────────────────────────────────
export async function loadFeature(slug) {
  const res = await fetch(`content/features/${slug}.json`);
  if (!res.ok) throw new Error(`Feature not found: ${slug}`);
  return res.json();
}

export async function loadFigure(slug) {
  const res = await fetch(`content/figures/${slug}.json`);
  if (!res.ok) throw new Error(`Figure detail not found: ${slug}`);
  return res.json();
}

export async function loadAllFeatures() {
  const results = await Promise.allSettled(FEATURE_SLUGS.map(loadFeature));
  return results
    .filter(r => r.status === "fulfilled")
    .map(r => r.value);
}

export function hasFigureDetail(slug) {
  return FIGURE_SLUGS.includes(slug);
}

export function getImagePath(slug) {
  return IMAGE_MAP[slug] ?? null;
}

// ─── Recent sessions (localStorage) ──────────────────────────────────────────
const RECENT_KEY = "cv_recent_slugs";

export function getRecentSlugs() {
  try { return JSON.parse(localStorage.getItem(RECENT_KEY)) || []; }
  catch { return []; }
}

export function recordVisit(slug) {
  let recent = getRecentSlugs().filter(s => s !== slug);
  recent.unshift(slug);
  recent = recent.slice(0, 6);
  localStorage.setItem(RECENT_KEY, JSON.stringify(recent));
}
