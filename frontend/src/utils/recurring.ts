import { Event } from '../types/Event';

// Heuristic recurring detection: same title and weekday/time over 3+ weeks
export function detectRecurring(events: Event[]): Map<number, string> {
  const byTitle: Record<string, Event[]> = {};
  events.forEach(e => {
    const key = (e.title || '').trim().toLowerCase();
    if (!key) return;
    (byTitle[key] = byTitle[key] || []).push(e);
  });

  const result = new Map<number, string>();
  Object.values(byTitle).forEach(list => {
    if (list.length < 3) return;
    // Group by weekday + hour
    const buckets: Record<string, Event[]> = {};
    list.forEach(e => {
      const d = new Date(e.start_date);
      const bucket = `${d.getDay()}-${d.getHours()}`;
      (buckets[bucket] = buckets[bucket] || []).push(e);
    });
    Object.values(buckets).forEach(b => {
      if (b.length >= 3) {
        b.forEach(ev => result.set(ev.id, 'Recurring'));
      }
    });
  });
  return result;
}
