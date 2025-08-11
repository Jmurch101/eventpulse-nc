import React, { useEffect, useState } from 'react';

type Settings = {
  defaultView: 'events' | 'holidays' | 'map' | 'favorites';
  defaultCity: string;
  defaultRadius: number;
};

interface Props {
  onSave: (s: Settings) => void;
}

const SettingsPanel: React.FC<Props> = ({ onSave }) => {
  const [defaultView, setDefaultView] = useState<Settings['defaultView']>('events');
  const [defaultCity, setDefaultCity] = useState<string>('');
  const [defaultRadius, setDefaultRadius] = useState<number>(25);

  useEffect(() => {
    try {
      const raw = localStorage.getItem('eventpulse_settings_v1');
      if (raw) {
        const s: Settings = JSON.parse(raw);
        if (s.defaultView) setDefaultView(s.defaultView);
        if (s.defaultCity !== undefined) setDefaultCity(s.defaultCity);
        if (s.defaultRadius !== undefined) setDefaultRadius(s.defaultRadius);
      }
    } catch {}
  }, []);

  return (
    <div className="space-y-3 text-sm">
      <div>
        <label className="block text-gray-700 mb-1">Default view</label>
        <select value={defaultView} onChange={e => setDefaultView(e.target.value as Settings['defaultView'])} className="w-full border rounded px-2 py-1">
          <option value="events">Events</option>
          <option value="holidays">Holidays</option>
          <option value="map">Map</option>
          <option value="favorites">Favorites</option>
        </select>
      </div>
      <div>
        <label className="block text-gray-700 mb-1">Default city</label>
        <select value={defaultCity} onChange={e => setDefaultCity(e.target.value)} className="w-full border rounded px-2 py-1">
          <option value="">None</option>
          <option value="raleigh">Raleigh</option>
          <option value="durham">Durham</option>
          <option value="chapel_hill">Chapel Hill</option>
          <option value="cary">Cary</option>
          <option value="morrisville">Morrisville</option>
          <option value="apex">Apex</option>
          <option value="holly_springs">Holly Springs</option>
          <option value="fuquay_varina">Fuquay-Varina</option>
        </select>
      </div>
      <div>
        <label className="block text-gray-700 mb-1">Default radius (miles)</label>
        <input type="number" min={5} max={100} value={defaultRadius} onChange={e => setDefaultRadius(Number(e.target.value))} className="w-full border rounded px-2 py-1" />
      </div>
      <div className="pt-2 flex justify-end gap-2">
        <button onClick={() => onSave({ defaultView, defaultCity, defaultRadius })} className="px-3 py-1 rounded bg-blue-600 text-white">Save</button>
      </div>
    </div>
  );
};

export default SettingsPanel;

