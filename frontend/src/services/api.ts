import axios from 'axios';
import { useQuery } from '@tanstack/react-query';
import { Event } from '../types/Event';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://eventpulse-nc-backend-ea4ecf265b40.herokuapp.com';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const eventService = {
  // Get all events with higher limit to include 2025 events
  getEvents: async (): Promise<Event[]> => {
    const response = await api.get('/api/events', {
      params: { limit: 10000 } // Request more events to include 2025
    });
    return response.data;
  },

  // Get events with filters
  getEventsWithFilters: async (filters: any): Promise<Event[]> => {
    const response = await api.get('/api/events', { 
      params: { ...filters, limit: 10000 } // Include higher limit with filters
    });
    return response.data;
  },

  // Get 2025 events specifically for heatmap
  get2025Events: async (): Promise<Event[]> => {
    const response = await api.get('/api/events', {
      params: { year: 2025, limit: 10000 }
    });
    return response.data;
  },

  // Create a new event
  createEvent: async (event: Omit<Event, 'id' | 'created_at'>): Promise<Event> => {
    const response = await api.post('/api/events', event);
    return response.data;
  },

  // Get event by ID
  getEventById: async (id: number): Promise<Event> => {
    const response = await api.get(`/api/events/${id}`);
    return response.data;
  },

  // Ingest stats
  getIngestStats: async (): Promise<any> => {
    const response = await api.get('/api/ingest/stats');
    return response.data;
  },
};

export default api; 

// React Query hooks (opt-in replacement for direct service calls)
export function useEventsQuery(filters?: any) {
  return useQuery({
    queryKey: ['events', filters || {}],
    queryFn: async () => {
      if (filters) return eventService.getEventsWithFilters(filters);
      return eventService.getEvents();
    },
    staleTime: 5 * 60 * 1000,
    refetchOnWindowFocus: false,
  });
}