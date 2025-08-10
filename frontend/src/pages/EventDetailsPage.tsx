import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { format } from 'date-fns';
import { eventService } from '../services/api';
import { Event } from '../types/Event';
import NCMap from '../components/NCMap';

const EventDetailsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [event, setEvent] = useState<Event | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        setError(null);
        if (!id) { setError('Missing event id'); setLoading(false); return; }
        const ev = await eventService.getEventById(Number(id));
        setEvent(ev);
      } catch (e) {
        setError('Failed to load event');
      } finally {
        setLoading(false);
      }
    })();
  }, [id]);

  if (loading) return <div className="p-6 text-center">Loading…</div>;
  if (error || !event) return <div className="p-6 text-center text-red-600">{error || 'Event not found'}</div>;

  const eventsForMap: Event[] = [event];

  return (
    <div className="p-6 max-w-3xl mx-auto font-sans">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-bold">{event.title}</h1>
        <Link to="/" className="text-blue-600 hover:underline text-sm">Back to Dashboard</Link>
      </div>

      <div className="bg-white rounded-lg shadow p-4 space-y-2">
        <div className="text-gray-700">
          {format(new Date(event.start_date), 'EEE, MMM d yyyy, h:mm a')} – {format(new Date(event.end_date), 'h:mm a')}
        </div>
        {event.location_name && (
          <div className="text-gray-600">{event.location_name}</div>
        )}
        {event.event_type && (
          <div className="inline-flex items-center px-2 py-0.5 rounded bg-gray-100 text-gray-800 text-xs font-medium">
            {event.event_type}
          </div>
        )}
        {event.description && (
          <p className="text-sm text-gray-800 mt-2 whitespace-pre-line">{event.description}</p>
        )}
        {event.source_url && (
          <div className="pt-2">
            <a href={event.source_url} target="_blank" rel="noreferrer" className="text-blue-600 hover:underline text-sm">
              Official source
            </a>
          </div>
        )}
      </div>

      <div className="mt-6">
        <h2 className="text-lg font-semibold mb-2">Location</h2>
        <div className="rounded overflow-hidden">
          <NCMap events={eventsForMap} mode="all" />
        </div>
      </div>
    </div>
  );
};

export default EventDetailsPage;

