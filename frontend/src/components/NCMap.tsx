import React, { useEffect, useMemo, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { Event } from '../types/Event';

// Fix default marker icon paths when bundling
const DefaultIcon = L.icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});
L.Marker.prototype.options.icon = DefaultIcon as any;

interface NCMapProps {
  events: Event[];
  mode?: 'live' | 'all';
}

// Focus on the Triangle area
const TRIANGLE_CENTER: [number, number] = [35.88, -78.85];

function formatCountdown(ms: number): string {
  const totalSeconds = Math.max(0, Math.floor(ms / 1000));
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;
  if (hours > 0) return `${hours}h ${minutes}m`;
  if (minutes > 0) return `${minutes}m ${seconds}s`;
  return `${seconds}s`;
}

const FitToMarkers: React.FC<{ positions: Array<[number, number]> }> = ({ positions }) => {
  const map = useMap();
  useEffect(() => {
    if (positions.length === 0) return;
    const bounds = L.latLngBounds(positions);
    map.fitBounds(bounds, { padding: [40, 40], maxZoom: 12 });
  }, [positions, map]);
  return null;
};

export const NCMap: React.FC<NCMapProps> = ({ events, mode = 'live' }) => {
  const [, forceTick] = useState(0);

  // Refresh countdowns periodically
  useEffect(() => {
    const id = setInterval(() => forceTick(t => t + 1), 30000);
    return () => clearInterval(id);
  }, []);

  const now = Date.now();

  const validEvents = useMemo(() => {
    return events.filter(e =>
      Number.isFinite(e.latitude) &&
      Number.isFinite(e.longitude) &&
      Math.abs(e.latitude) <= 90 &&
      Math.abs(e.longitude) <= 180
    );
  }, [events]);

  const liveOrSoonEvents = useMemo(() => {
    const ONE_HOUR = 60 * 60 * 1000;
    return validEvents.filter(e => {
      const start = new Date(e.start_date).getTime();
      const end = new Date(e.end_date).getTime();
      if (!Number.isFinite(start) || !Number.isFinite(end)) return false;
      const isLive = start <= now && now < end;
      const isSoon = start > now && start - now <= ONE_HOUR;
      return isLive || isSoon;
    });
  }, [validEvents, now]);

  const displayEvents = mode === 'all' ? validEvents : liveOrSoonEvents;
  const positions: Array<[number, number]> = displayEvents.map(ev => [ev.latitude, ev.longitude]);

  return (
    <div style={{ height: 480, width: '100%', borderRadius: 12, overflow: 'hidden' }}>
      <MapContainer center={TRIANGLE_CENTER} zoom={10} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <FitToMarkers positions={positions} />
        {displayEvents.map(ev => {
          const start = new Date(ev.start_date).getTime();
          const end = new Date(ev.end_date).getTime();
          const isLive = start <= now && now < end;
          const ms = isLive ? end - now : start - now;
          const label = mode === 'all'
            ? (isLive ? 'Live' : '')
            : (isLive ? `Live • ends in ${formatCountdown(ms)}` : `Starts in ${formatCountdown(ms)}`);
          return (
          <Marker key={ev.id} position={[ev.latitude, ev.longitude] as [number, number]}>
            <Popup>
              <div style={{ maxWidth: 240 }}>
                <div style={{ fontWeight: 700 }}>{ev.title}</div>
                <div style={{ color: '#4b5563' }}>{ev.location_name}</div>
                {label && (
                  <div style={{ marginTop: 6, fontSize: 12, color: isLive ? '#059669' : '#2563eb', fontWeight: 600 }}>
                    {label}
                  </div>
                )}
                {ev.source_url && (
                  <div style={{ marginTop: 8 }}>
                    <a href={ev.source_url} target="_blank" rel="noreferrer" style={{ color: '#2563eb', fontWeight: 600, fontSize: 12 }}>
                      Official source
                    </a>
                  </div>
                )}
              </div>
            </Popup>
          </Marker>
          );
        })}
      </MapContainer>
    </div>
  );
};

export default NCMap;

