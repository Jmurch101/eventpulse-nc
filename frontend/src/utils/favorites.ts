const KEY = 'eventpulse_favorites_v1';

export function getFavorites(): number[] {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return [];
    const arr = JSON.parse(raw);
    return Array.isArray(arr) ? arr : [];
  } catch {
    return [];
  }
}

export function isFavorite(id: number): boolean {
  return getFavorites().includes(id);
}

export function toggleFavorite(id: number): number[] {
  const curr = getFavorites();
  const idx = curr.indexOf(id);
  if (idx >= 0) curr.splice(idx, 1); else curr.push(id);
  localStorage.setItem(KEY, JSON.stringify(curr));
  return curr;
}

