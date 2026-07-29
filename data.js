

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
