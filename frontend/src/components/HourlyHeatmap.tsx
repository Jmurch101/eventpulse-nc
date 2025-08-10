import React, { useMemo, useState } from 'react';
import { Event } from '../types/Event';

interface HourlyHeatmapProps {
  events: Event[];
  weekStart?: Date; // optional start of the week; if omitted, uses events' week span
  compact?: boolean;
  defaultCollapsed?: boolean;
  showHourLabels?: boolean;
}

const HourlyHeatmap: React.FC<HourlyHeatmapProps> = ({ events, compact = false, defaultCollapsed = false, showHourLabels = false }) => {
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

  const hourHeader = (hr: number) => {
    const h = hr % 24;
    if (h === 0) return '12 am';
    if (h < 12) return `${h} am`;
    if (h === 12) return '12 pm';
    return `${h - 12} pm`;
  };
  const cellSize = compact ? 14 : 16;

  return (
    <div className="text-xs">
      <div className="flex items-center justify-between mb-1">
        <div className="text-gray-700">Weekly Time Heatmap</div>
        <button onClick={() => setCollapsed(c => !c)} className="text-[10px] text-blue-600 hover:underline">
          {collapsed ? 'Expand' : 'Collapse'}
        </button>
      </div>
      {/* no global header or legend to keep compact */}
      {!collapsed && (
        <div style={{ overflowX: 'auto' }}>
          <div
            className="grid border border-gray-300 rounded"
            style={{
              gridTemplateColumns: `${compact ? '64px repeat(24, 48px)' : '72px repeat(24, 56px)'}`,
              gap: 0,
              rowGap: 12,
              whiteSpace: 'nowrap'
            }}
          >
            {/* Day rows with inline hour labels */}
            {['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].map((label, day) => (
              <React.Fragment key={label}>
                <div className="text-[10px] text-gray-800 font-medium pr-1 flex items-center justify-end bg-white" style={{ borderTop: '2px solid #cbd5e1' }}>{label}</div>
                {Array.from({ length: 24 }).map((_, hr) => (
                  <div
                    key={hr}
                    className="relative flex items-center justify-center"
                    title={`${label} ${hourHeader(hr)} — ${grid[day][hr]} event${grid[day][hr] === 1 ? '' : 's'}`}
                    style={{
                      backgroundColor: colorFor(grid[day][hr]),
                      height: cellSize,
                      borderTop: '1px solid #e5e7eb',
                      borderLeft: '1px solid #e5e7eb'
                    }}
                  >
                    <span className="text-[9px] text-gray-900" style={{ mixBlendMode: 'multiply' }}>{hourHeader(hr)}</span>
                  </div>
                ))}
              </React.Fragment>
            ))}
          </div>
        </div>
      )}
      {/* legend removed per spec */}
    </div>
  );
};

export default HourlyHeatmap;

