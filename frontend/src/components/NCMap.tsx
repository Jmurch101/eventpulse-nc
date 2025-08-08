import React, { useMemo } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
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
}

const NC_CENTER: [number, number] = [35.782169, -80.793457];

export const NCMap: React.FC<NCMapProps> = ({ events }) => {
  const validEvents = useMemo(
    () =>
      events.filter(e =>
        Number.isFinite(e.latitude) &&
        Number.isFinite(e.longitude) &&
        Math.abs(e.latitude) <= 90 &&
        Math.abs(e.longitude) <= 180
      ),
    [events]
  );

  return (
    <div style={{ height: 480, width: '100%', borderRadius: 12, overflow: 'hidden' }}>
      <MapContainer center={NC_CENTER} zoom={7} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {validEvents.map(ev => (
          <Marker key={ev.id} position={[ev.latitude, ev.longitude] as [number, number]}>
            <Popup>
              <div style={{ maxWidth: 240 }}>
                <div style={{ fontWeight: 700 }}>{ev.title}</div>
                <div style={{ color: '#4b5563' }}>{ev.location_name}</div>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default NCMap;

