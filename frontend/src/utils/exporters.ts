import { Event } from '../types/Event';

function toICSDate(dateStr: string): string {
  const d = new Date(dateStr);
  const pad = (n: number) => String(n).padStart(2, '0');
  return (
    d.getUTCFullYear().toString() +
    pad(d.getUTCMonth() + 1) +
    pad(d.getUTCDate()) +
    'T' +
    pad(d.getUTCHours()) +
    pad(d.getUTCMinutes()) +
    pad(d.getUTCSeconds()) +
    'Z'
  );
}

export function buildICS(events: Event[], calendarName = 'EventPulse NC'): string {
  const lines: string[] = [];
  lines.push('BEGIN:VCALENDAR');
  lines.push('VERSION:2.0');
  lines.push('PRODID:-//EventPulse NC//EN');
  lines.push(`X-WR-CALNAME:${calendarName}`);

  events.forEach((ev) => {
    const uid = `eventpulse-${ev.id}@eventpulse-nc`;
    const dtStart = toICSDate(ev.start_date);
    const dtEnd = toICSDate(ev.end_date);
    const title = (ev.title || '').replace(/\n/g, ' ');
    const desc = (ev.description || '').replace(/\n/g, ' ');
    const loc = (ev.location_name || '').replace(/\n/g, ' ');
    lines.push('BEGIN:VEVENT');
    lines.push(`UID:${uid}`);
    lines.push(`DTSTAMP:${toICSDate(new Date().toISOString())}`);
    lines.push(`DTSTART:${dtStart}`);
    lines.push(`DTEND:${dtEnd}`);
    lines.push(`SUMMARY:${title}`);
    if (desc) lines.push(`DESCRIPTION:${desc}`);
    if (loc) lines.push(`LOCATION:${loc}`);
    if (ev.source_url) lines.push(`URL:${ev.source_url}`);
    lines.push('END:VEVENT');
  });

  lines.push('END:VCALENDAR');
  return lines.join('\r\n');
}

export function downloadICS(events: Event[], filename = 'eventpulse.ics', calendarName?: string) {
  const ics = buildICS(events, calendarName);
  const blob = new Blob([ics], { type: 'text/calendar;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

