import React, { useMemo } from 'react';
import { Event } from '../types/Event';

interface HourlyHeatmapProps {
  events: Event[];
  weekStart?: Date; // optional start of the week; if omitted, uses events' week span
}

const HourlyHeatmap: React.FC<HourlyHeatmapProps> = ({ events }) => {
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

  return (
    <div className="text-xs">
      <div className="mb-1 text-gray-700">Weekly Hourly Heatmap</div>
      <div className="grid" style={{ gridTemplateColumns: '64px repeat(24, minmax(16px, 1fr))', gap: 1 }}>
        <div></div>
        {Array.from({ length: 24 }).map((_, hr) => (
          <div key={hr} className="text-[9px] text-center text-gray-600">{hr}</div>
        ))}
        {['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].map((label, day) => (
          <React.Fragment key={label}>
            <div className="text-[10px] text-gray-700 pr-1 flex items-center justify-end">{label}</div>
            {Array.from({ length: 24 }).map((_, hr) => (
              <div key={hr} className="rounded" style={{ backgroundColor: colorFor(grid[day][hr]), height: 12 }} />
            ))}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};

export default HourlyHeatmap;

