import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { format } from 'date-fns';
import { eventService } from '../services/api';
import { Event } from '../types/Event';
import NCMap from '../components/NCMap';

const DayEventsPage: React.FC = () => {
  const { date } = useParams<{ date: string }>();
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);

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
        <Link to="/" className="text-blue-500 hover:underline">Back to Dashboard</Link>
      </div>
      {/* Hourly heat grid */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold mb-2">Hourly Activity</h2>
        <div className="grid grid-cols-6 gap-1">
          {Array.from({ length: 24 }).map((_, hr) => {
            const count = events.filter(ev => {
              const d = new Date(ev.start_date);
              return format(d, 'yyyy-MM-dd') === date && d.getHours() === hr;
            }).length;
            const intensity = count === 0 ? '#f3f4f6' : count <= 2 ? '#bfdbfe' : count <= 5 ? '#60a5fa' : '#2563eb';
            return (
              <div key={hr} className="p-3 text-center rounded" style={{ backgroundColor: intensity }}>
                <div className="text-xs text-gray-700">{hr}:00</div>
                {count > 0 && <div className="text-sm font-semibold">{count}</div>}
              </div>
            );
          })}
        </div>
      </div>
      {events.length > 0 ? (
        <ul className="space-y-4">
          {events.map(ev => (
            <li key={ev.id} className="bg-white p-4 rounded shadow">
              <h2 className="text-xl font-semibold">{ev.title}</h2>
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