import React, { useMemo, useState } from 'react';
import { Event } from '../types/Event';

interface HourlyHeatmapProps {
  events: Event[];
  weekStart?: Date; // optional start of the week; if omitted, uses events' week span
  compact?: boolean;
  defaultCollapsed?: boolean;
  showHourLabels?: boolean;
}

const HourlyHeatmap: React.FC<HourlyHeatmapProps> = ({ events, compact = false, defaultCollapsed = false, showHourLabels = true }) => {
  const [collapsed, setCollapsed] = useState<boolean>(defaultCollapsed);
  const grid = useMemo(() => {
    // 7 days x 24 hours counts
    const counts: number[][] = Array.from({ length: 7 }, () => Array(24).fill(0));
    events.forEach(ev => {
      const d = new Date(ev.start_date);
      const day = d.getDay(); // 0-6
      const hr = d.getHours(); // 0-23
      if (day >= 0 && day < 7 && hr >= 0 && hr < 24) counts[day][hr]++;
    });
    return counts;
  }, [events]);

  const colorFor = (count: number) => {
    if (count === 0) return '#f3f4f6';
    if (count <= 2) return '#bfdbfe';
    if (count <= 5) return '#60a5fa';
    if (count <= 10) return '#2563eb';
    return '#1e40af';
  };

  const hourHeader = (hr: number) => hr;
  const cellSize = compact ? 14 : 16;

  return (
    <div className="text-xs">
      <div className="flex items-center justify-between mb-1">
        <div className="text-gray-700">Weekly Hourly Heatmap</div>
        <button onClick={() => setCollapsed(c => !c)} className="text-[10px] text-blue-600 hover:underline">
          {collapsed ? 'Expand' : 'Collapse'}
        </button>
      </div>
      {!compact && (
        <div className="mb-1 text-[11px] text-gray-600">
          Hours run left to right (0–23). Days run top to bottom (Sun–Sat). Darker cells mean more events.
        </div>
      )}
      {!compact && (
        <div className="mb-2 text-[10px] text-gray-500">Tip: Left‑click a calendar day to see its events listed below.</div>
      )}
      {!collapsed && (
        <div className="grid border border-gray-300 rounded" style={{ gridTemplateColumns: `${compact ? '48px repeat(24, minmax(12px, 1fr))' : '56px repeat(24, minmax(14px, 1fr))'}`, gap: 0 }}>
          <div className="text-[10px] text-gray-600 flex items-center justify-end pr-1 bg-gray-50 border-b border-gray-300">Day</div>
          {Array.from({ length: 24 }).map((_, hr) => (
            <div key={hr} className="text-[9px] text-center text-gray-700 bg-gray-50 border-b border-l border-gray-300" style={{ lineHeight: `${cellSize}px`, height: cellSize }}>{hourHeader(hr)}</div>
          ))}
          {['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].map((label, day) => (
            <React.Fragment key={label}>
              <div className="text-[10px] text-gray-800 font-medium pr-1 flex items-center justify-end border-t border-gray-300 bg-white">{label}</div>
              {Array.from({ length: 24 }).map((_, hr) => (
                <div
                  key={hr}
                  className="relative"
                  title={`${label} ${hr}:00 — ${grid[day][hr]} event${grid[day][hr] === 1 ? '' : 's'}`}
                  style={{
                    backgroundColor: colorFor(grid[day][hr]),
                    height: cellSize,
                    borderTop: '1px solid #d1d5db',
                    borderLeft: '1px solid #d1d5db'
                  }}
                >
                  {showHourLabels && (
                    <span className="absolute inset-0 flex items-center justify-center text-[8px] text-gray-700" style={{ lineHeight: 1 }}>
                      {hr}
                    </span>
                  )}
                </div>
              ))}
            </React.Fragment>
          ))}
        </div>
      )}
      {!compact && !collapsed && (
        <div className="flex items-center gap-2 mt-2 text-[10px] text-gray-600 flex-wrap">
          <span className="font-medium">Legend:</span>
          <span className="inline-flex items-center gap-1"><span style={{ width: 12, height: 12, background: '#f3f4f6', border: '1px solid #e5e7eb', borderRadius: 2 }}></span>0</span>
          <span className="inline-flex items-center gap-1"><span style={{ width: 12, height: 12, background: '#bfdbfe', border: '1px solid #e5e7eb', borderRadius: 2 }}></span>1–2</span>
          <span className="inline-flex items-center gap-1"><span style={{ width: 12, height: 12, background: '#60a5fa', border: '1px solid #e5e7eb', borderRadius: 2 }}></span>3–5</span>
          <span className="inline-flex items-center gap-1"><span style={{ width: 12, height: 12, background: '#2563eb', border: '1px solid #e5e7eb', borderRadius: 2 }}></span>6–10</span>
          <span className="inline-flex items-center gap-1"><span style={{ width: 12, height: 12, background: '#1e40af', border: '1px solid #e5e7eb', borderRadius: 2 }}></span>10+</span>
        </div>
      )}
    </div>
  );
};

export default HourlyHeatmap;

