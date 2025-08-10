import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { format } from 'date-fns';
import { eventService } from '../services/api';
import { Event } from '../types/Event';
import NCMap from '../components/NCMap';
import HourlyHeatmap from '../components/HourlyHeatmap';

const DayEventsPage: React.FC = () => {
  const { date } = useParams<{ date: string }>();
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);

  const exportDayAsCSV = () => {
    const rows = [
      ['Title', 'Start', 'End', 'Location', 'Type', 'Source URL'],
      ...events.map(ev => [
        ev.title,
        new Date(ev.start_date).toISOString(),
        new Date(ev.end_date).toISOString(),
        ev.location_name || '',
        ev.event_type,
        ev.source_url || ''
      ])
    ];
    const csv = rows.map(r => r.map(f => `"${String(f).replace(/"/g, '""')}"`).join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `eventpulse_${date}_export.csv`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  };

  useEffect(() => {
    (async () => {
      setLoading(true);
      const data = await eventService.getEvents();
      const filtered = data.filter(e => format(new Date(e.start_date), 'yyyy-MM-dd') === date);
      setEvents(filtered);
      setLoading(false);
    })();
  }, [date]);

  if (loading) return <div className="flex justify-center p-6">Loading...</div>;

  return (
    <div className="p-6 max-w-4xl mx-auto font-sans">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Events on {date}</h1>
        <div className="flex items-center gap-3">
          <button onClick={exportDayAsCSV} className="px-3 py-1 rounded bg-green-500 text-white hover:bg-green-600 text-sm">Export CSV</button>
          <Link to="/" className="text-blue-500 hover:underline">Back to Dashboard</Link>
        </div>
      </div>
      {/* Hourly heat grid */}
      <div className="mb-4">
        <h2 className="text-lg font-semibold mb-2">Hourly Activity</h2>
        <HourlyHeatmap events={events} />
      </div>
      <p className="text-sm text-gray-600 mb-3">Events listed below are for the selected date. Click an item to view its official source when available.</p>
      {events.length > 0 ? (
        <ul className="space-y-4">
          {events.map(ev => (
            <li key={ev.id} className="bg-white p-4 rounded shadow hover:shadow-md transition">
              <h2 className="text-lg font-semibold">{ev.title}</h2>
              <p className="text-gray-600">{ev.location_name}</p>
              <p className="text-gray-500">
                {format(new Date(ev.start_date), 'h:mm a')} - {format(new Date(ev.end_date), 'h:mm a')}
              </p>
              {ev.source_url && (
                <p className="mt-2 text-sm">
                  <a className="text-blue-600 hover:underline" href={ev.source_url} target="_blank" rel="noreferrer">
                    Official source
                  </a>
                </p>
              )}
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-center text-gray-600">No events scheduled for this day.</p>
      )}
      <div className="mt-6">
        <h2 className="text-lg font-semibold mb-2">Map</h2>
        <NCMap events={events} mode={'all'} />
      </div>
    </div>
  );
};

export default DayEventsPage;